"""User education and training tools for the Convergent coordination library.

Provides a framework for creating interactive training modules that guide
users through Convergent's features. Includes:

- Structured training modules with ordered steps
- Step types: conceptual explanations, hands-on exercises, and validations
- Progress tracking with SQLite persistence
- Built-in training content for core Convergent features
- Self-help guidance based on the user's current training state

Training modules are composable: each module covers one subsystem
(e.g., Intent Graph, Stigmergy, Voting) and can be completed independently.
"""

from __future__ import annotations

import contextlib
import json
import logging
import sqlite3
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum

logger = logging.getLogger(__name__)


class TrainingLevel(str, Enum):
    """Difficulty level for training modules.

    Determines prerequisite knowledge and depth of content.
    """

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class StepType(str, Enum):
    """Classification of a training step.

    Determines how the step is presented and validated.
    """

    CONCEPT = "concept"  # Explanation of a concept — read and understand
    EXERCISE = "exercise"  # Hands-on task — the user does something
    VALIDATION = "validation"  # Check understanding — quiz or code review


class StepStatus(str, Enum):
    """Completion status of a training step."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"


def _utc_now_iso() -> str:
    """Return current UTC time as ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class TrainingStep:
    """A single step in a training module.

    Attributes:
        step_id: Unique identifier for this step.
        title: Short title for the step.
        description: Full description of what to learn or do.
        step_type: Whether this is a concept, exercise, or validation.
        content: The actual training content (markdown-formatted).
        hint: Optional hint for exercises and validations.
        validation_criteria: What constitutes successful completion.
        order: Position within the module (0-indexed).
    """

    step_id: str
    title: str
    description: str
    step_type: StepType
    content: str
    hint: str = ""
    validation_criteria: str = ""
    order: int = 0

    def to_json(self) -> str:
        """Serialize to JSON string."""
        d = asdict(self)
        d["step_type"] = self.step_type.value
        return json.dumps(d)

    @classmethod
    def from_json(cls, data: str) -> TrainingStep:
        """Deserialize from JSON string."""
        d = json.loads(data)
        d["step_type"] = StepType(d["step_type"])
        return cls(**d)


@dataclass(frozen=True)
class TrainingModule:
    """A collection of training steps covering one topic.

    Attributes:
        module_id: Unique identifier for this module.
        title: Module title.
        description: What the module teaches.
        level: Difficulty level.
        topic: The Convergent subsystem this covers (e.g. "intent_graph").
        steps: Ordered list of training steps.
        prerequisites: Module IDs that should be completed first.
        estimated_steps: Total number of steps.
    """

    module_id: str
    title: str
    description: str
    level: TrainingLevel
    topic: str
    steps: list[TrainingStep] = field(default_factory=list)
    prerequisites: list[str] = field(default_factory=list)
    estimated_steps: int = 0

    def to_json(self) -> str:
        """Serialize to JSON string."""
        d = asdict(self)
        d["level"] = self.level.value
        for i, step in enumerate(self.steps):
            d["steps"][i]["step_type"] = step.step_type.value
        return json.dumps(d)

    @classmethod
    def from_json(cls, data: str) -> TrainingModule:
        """Deserialize from JSON string."""
        d = json.loads(data)
        d["level"] = TrainingLevel(d["level"])
        d["steps"] = [
            TrainingStep(**{**s, "step_type": StepType(s["step_type"])})
            for s in d["steps"]
        ]
        return cls(**d)


@dataclass
class TrainingProgress:
    """Tracks a user's progress through a training module.

    Not frozen because step statuses change as the user progresses.

    Attributes:
        progress_id: Unique identifier for this progress record.
        user_id: The user being tracked.
        module_id: The training module being tracked.
        step_statuses: Map of step_id to StepStatus.
        started_at: When the user started the module.
        completed_at: When the user finished (None if still in progress).
        current_step_index: Index of the step the user is currently on.
    """

    progress_id: str
    user_id: str
    module_id: str
    step_statuses: dict[str, str] = field(default_factory=dict)
    started_at: str = field(default_factory=_utc_now_iso)
    completed_at: str | None = None
    current_step_index: int = 0

    @property
    def completed_steps(self) -> int:
        """Count of completed steps."""
        return sum(
            1 for s in self.step_statuses.values()
            if s == StepStatus.COMPLETED.value
        )

    @property
    def total_steps(self) -> int:
        """Total number of tracked steps."""
        return len(self.step_statuses)

    @property
    def completion_ratio(self) -> float:
        """Fraction of steps completed (0.0 to 1.0)."""
        if not self.step_statuses:
            return 0.0
        return self.completed_steps / self.total_steps

    @property
    def is_complete(self) -> bool:
        """Whether all steps are completed or skipped."""
        if not self.step_statuses:
            return False
        return all(
            s in (StepStatus.COMPLETED.value, StepStatus.SKIPPED.value)
            for s in self.step_statuses.values()
        )

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, data: str) -> TrainingProgress:
        """Deserialize from JSON string."""
        return cls(**json.loads(data))


_SCHEMA = """\
CREATE TABLE IF NOT EXISTS training_modules (
    module_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    level TEXT NOT NULL,
    topic TEXT NOT NULL,
    module_json TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_modules_topic ON training_modules(topic);
CREATE INDEX IF NOT EXISTS idx_modules_level ON training_modules(level);

CREATE TABLE IF NOT EXISTS training_progress (
    progress_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    module_id TEXT NOT NULL,
    step_statuses TEXT NOT NULL,
    started_at TEXT NOT NULL,
    completed_at TEXT,
    current_step_index INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_progress_user ON training_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_progress_module ON training_progress(module_id);
CREATE UNIQUE INDEX IF NOT EXISTS idx_progress_user_module
    ON training_progress(user_id, module_id);
"""


class TrainingManager:
    """Manages training modules, progress tracking, and self-help guidance.

    Provides CRUD operations for training modules, tracks per-user
    progress through each module, and generates context-aware guidance
    based on the user's current training state.

    Args:
        db_path: SQLite database path, or ":memory:" for in-memory.
        auto_register_builtins: If True, register built-in training modules
            on initialization.
    """

    def __init__(
        self,
        db_path: str = ":memory:",
        auto_register_builtins: bool = True,
    ) -> None:
        self._db_path = db_path
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

        if auto_register_builtins:
            self._register_builtin_modules()

    def register_module(self, module: TrainingModule) -> None:
        """Register a training module.

        Args:
            module: The training module to register.
        """
        self._conn.execute(
            "INSERT OR REPLACE INTO training_modules "
            "(module_id, title, description, level, topic, module_json) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                module.module_id,
                module.title,
                module.description,
                module.level.value,
                module.topic,
                module.to_json(),
            ),
        )
        self._conn.commit()
        logger.info("Registered training module: %s (%s)", module.title, module.module_id)

    def get_module(self, module_id: str) -> TrainingModule | None:
        """Retrieve a training module by ID.

        Args:
            module_id: The module to look up.

        Returns:
            The TrainingModule, or None if not found.
        """
        cursor = self._conn.execute(
            "SELECT module_json FROM training_modules WHERE module_id = ?",
            (module_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return TrainingModule.from_json(row["module_json"])

    def list_modules(
        self,
        level: TrainingLevel | None = None,
        topic: str | None = None,
    ) -> list[TrainingModule]:
        """List available training modules with optional filters.

        Args:
            level: Filter by difficulty level. None for all.
            topic: Filter by topic. None for all.

        Returns:
            List of matching TrainingModule objects.
        """
        clauses: list[str] = []
        params: list[str] = []

        if level is not None:
            clauses.append("level = ?")
            params.append(level.value)
        if topic is not None:
            clauses.append("topic = ?")
            params.append(topic)

        where = ""
        if clauses:
            where = "WHERE " + " AND ".join(clauses)

        cursor = self._conn.execute(
            f"SELECT module_json FROM training_modules {where} "  # noqa: S608
            "ORDER BY level, title",
            params,
        )
        return [TrainingModule.from_json(row["module_json"]) for row in cursor]

    def start_module(self, user_id: str, module_id: str) -> TrainingProgress:
        """Start a user on a training module.

        Creates a progress record with all steps set to PENDING.
        If the user already has progress for this module, returns
        the existing progress.

        Args:
            user_id: The user starting the module.
            module_id: The module to start.

        Returns:
            The TrainingProgress record.

        Raises:
            ValueError: If the module does not exist.
        """
        # Check for existing progress
        existing = self.get_progress(user_id, module_id)
        if existing is not None:
            return existing

        module = self.get_module(module_id)
        if module is None:
            raise ValueError(f"Training module not found: {module_id}")

        step_statuses = {
            step.step_id: StepStatus.PENDING.value
            for step in module.steps
        }

        progress = TrainingProgress(
            progress_id=str(uuid.uuid4()),
            user_id=user_id,
            module_id=module_id,
            step_statuses=step_statuses,
        )
        self._save_progress(progress)
        logger.info(
            "User %s started module %s (%s)",
            user_id,
            module.title,
            module_id,
        )
        return progress

    def advance_step(
        self,
        user_id: str,
        module_id: str,
        step_id: str,
        status: StepStatus = StepStatus.COMPLETED,
    ) -> TrainingProgress:
        """Update the status of a training step.

        Args:
            user_id: The user.
            module_id: The training module.
            step_id: The step to update.
            status: The new status for the step.

        Returns:
            The updated TrainingProgress.

        Raises:
            ValueError: If no progress record exists for this user/module.
        """
        progress = self.get_progress(user_id, module_id)
        if progress is None:
            raise ValueError(
                f"No progress found for user {user_id} on module {module_id}"
            )

        if step_id not in progress.step_statuses:
            raise ValueError(f"Step {step_id} not found in module {module_id}")

        progress.step_statuses[step_id] = status.value

        # Advance current_step_index if completing current step
        module = self.get_module(module_id)
        if module is not None and status in (StepStatus.COMPLETED, StepStatus.SKIPPED):
            for i, step in enumerate(module.steps):
                if step.step_id == step_id and i >= progress.current_step_index:
                    progress.current_step_index = min(i + 1, len(module.steps) - 1)
                    break

        # Mark module complete if all steps done
        if progress.is_complete and progress.completed_at is None:
            progress.completed_at = _utc_now_iso()
            logger.info(
                "User %s completed module %s",
                user_id,
                module_id,
            )

        self._save_progress(progress)
        return progress

    def get_progress(self, user_id: str, module_id: str) -> TrainingProgress | None:
        """Get a user's progress on a specific module.

        Args:
            user_id: The user.
            module_id: The training module.

        Returns:
            The TrainingProgress, or None if the user hasn't started this module.
        """
        cursor = self._conn.execute(
            "SELECT * FROM training_progress "
            "WHERE user_id = ? AND module_id = ?",
            (user_id, module_id),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return TrainingProgress(
            progress_id=row["progress_id"],
            user_id=row["user_id"],
            module_id=row["module_id"],
            step_statuses=json.loads(row["step_statuses"]),
            started_at=row["started_at"],
            completed_at=row["completed_at"],
            current_step_index=row["current_step_index"],
        )

    def get_all_progress(self, user_id: str) -> list[TrainingProgress]:
        """Get a user's progress across all modules.

        Args:
            user_id: The user.

        Returns:
            List of TrainingProgress records.
        """
        cursor = self._conn.execute(
            "SELECT * FROM training_progress WHERE user_id = ? ORDER BY started_at DESC",
            (user_id,),
        )
        return [
            TrainingProgress(
                progress_id=row["progress_id"],
                user_id=row["user_id"],
                module_id=row["module_id"],
                step_statuses=json.loads(row["step_statuses"]),
                started_at=row["started_at"],
                completed_at=row["completed_at"],
                current_step_index=row["current_step_index"],
            )
            for row in cursor
        ]

    def get_current_step(
        self,
        user_id: str,
        module_id: str,
    ) -> TrainingStep | None:
        """Get the current step for a user in a module.

        Args:
            user_id: The user.
            module_id: The training module.

        Returns:
            The current TrainingStep, or None if no progress or module not found.
        """
        progress = self.get_progress(user_id, module_id)
        if progress is None:
            return None

        module = self.get_module(module_id)
        if module is None or not module.steps:
            return None

        idx = min(progress.current_step_index, len(module.steps) - 1)
        return module.steps[idx]

    def generate_guidance(self, user_id: str) -> str:
        """Generate personalized training guidance for a user.

        Analyzes the user's progress across all modules and recommends
        next steps based on completion status, level, and prerequisites.

        Args:
            user_id: The user to generate guidance for.

        Returns:
            Markdown-formatted guidance string.
        """
        all_modules = self.list_modules()
        all_progress = self.get_all_progress(user_id)

        progress_map = {p.module_id: p for p in all_progress}
        completed_ids = {
            p.module_id for p in all_progress if p.is_complete
        }

        sections: list[str] = []
        sections.append("## Training Guidance\n")

        # In-progress modules
        in_progress = [
            p for p in all_progress
            if not p.is_complete
        ]
        if in_progress:
            lines = ["### Continue Learning\n"]
            for p in in_progress:
                module = self.get_module(p.module_id)
                if module is None:
                    continue
                pct = int(p.completion_ratio * 100)
                current_step = self.get_current_step(user_id, p.module_id)
                step_info = f" — Next: {current_step.title}" if current_step else ""
                lines.append(f"- **{module.title}** ({pct}% complete){step_info}")
            sections.append("\n".join(lines))

        # Recommended next modules
        available = [
            m for m in all_modules
            if m.module_id not in progress_map
            and all(pre in completed_ids for pre in m.prerequisites)
        ]
        if available:
            # Sort by level (beginner first)
            level_order = {
                TrainingLevel.BEGINNER: 0,
                TrainingLevel.INTERMEDIATE: 1,
                TrainingLevel.ADVANCED: 2,
            }
            available.sort(key=lambda m: level_order.get(m.level, 99))

            lines = ["### Recommended Next\n"]
            for m in available[:5]:
                lines.append(
                    f"- **{m.title}** [{m.level.value}] — {m.description}"
                )
            sections.append("\n".join(lines))

        # Completed summary
        if completed_ids:
            lines = ["### Completed\n"]
            for mid in completed_ids:
                module = self.get_module(mid)
                if module:
                    lines.append(f"- ~~{module.title}~~")
            sections.append("\n".join(lines))

        if len(sections) == 1:
            sections.append(
                "No training progress yet. Start with a beginner module!"
            )

        return "\n\n".join(sections)

    def reset_progress(self, user_id: str, module_id: str) -> bool:
        """Reset a user's progress on a module.

        Args:
            user_id: The user.
            module_id: The module to reset.

        Returns:
            True if progress was found and reset, False otherwise.
        """
        cursor = self._conn.execute(
            "DELETE FROM training_progress "
            "WHERE user_id = ? AND module_id = ?",
            (user_id, module_id),
        )
        self._conn.commit()
        return cursor.rowcount > 0

    def close(self) -> None:
        """Close the database connection."""
        self._conn.close()

    def __del__(self) -> None:
        with contextlib.suppress(Exception):
            self._conn.close()

    def _save_progress(self, progress: TrainingProgress) -> None:
        """Persist a progress record."""
        self._conn.execute(
            "INSERT OR REPLACE INTO training_progress "
            "(progress_id, user_id, module_id, step_statuses, "
            "started_at, completed_at, current_step_index) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                progress.progress_id,
                progress.user_id,
                progress.module_id,
                json.dumps(progress.step_statuses),
                progress.started_at,
                progress.completed_at,
                progress.current_step_index,
            ),
        )
        self._conn.commit()

    def _register_builtin_modules(self) -> None:
        """Register the built-in training modules for Convergent's features."""
        for module in _BUILTIN_MODULES:
            cursor = self._conn.execute(
                "SELECT 1 FROM training_modules WHERE module_id = ?",
                (module.module_id,),
            )
            if cursor.fetchone() is None:
                self.register_module(module)


# --- Built-in Training Modules ---

_BUILTIN_MODULES: list[TrainingModule] = [
    TrainingModule(
        module_id="convergent-basics",
        title="Convergent Basics",
        description="Introduction to multi-agent coordination with Convergent.",
        level=TrainingLevel.BEGINNER,
        topic="overview",
        estimated_steps=4,
        steps=[
            TrainingStep(
                step_id="basics-1",
                title="What is Convergent?",
                description="Understand the purpose and architecture of Convergent.",
                step_type=StepType.CONCEPT,
                content=(
                    "Convergent is a multi-agent coordination library with two layers:\n\n"
                    "1. **Intent Graph** — Agents observe a shared intent graph and\n"
                    "   independently converge on compatible outputs.\n"
                    "2. **Coordination Protocol** — Bio-inspired patterns for active\n"
                    "   coordination: voting, stigmergy, flocking, and signaling.\n\n"
                    "Key principle: agents can *see* what others are doing (intent graph)\n"
                    "and *decide together* (coordination protocol)."
                ),
                order=0,
            ),
            TrainingStep(
                step_id="basics-2",
                title="Creating Your First Intent",
                description="Learn to create and publish an intent to the graph.",
                step_type=StepType.EXERCISE,
                content=(
                    "Create an Intent with an InterfaceSpec and publish it:\n\n"
                    "```python\n"
                    "from convergent import Intent, InterfaceSpec, InterfaceKind\n"
                    "from convergent import PythonGraphBackend, IntentResolver\n\n"
                    "backend = PythonGraphBackend()\n"
                    "resolver = IntentResolver(backend=backend)\n\n"
                    "intent = Intent(\n"
                    "    agent_id='agent-1',\n"
                    "    intent='Implement user authentication',\n"
                    "    provides=[InterfaceSpec(\n"
                    "        name='authenticate',\n"
                    "        kind=InterfaceKind.FUNCTION,\n"
                    "        signature='(username: str, password: str) -> bool',\n"
                    "    )],\n"
                    ")\n"
                    "resolver.publish(intent)\n"
                    "```"
                ),
                hint="Use InterfaceKind.FUNCTION for function signatures.",
                validation_criteria="Intent is published and retrievable from the resolver.",
                order=1,
            ),
            TrainingStep(
                step_id="basics-3",
                title="Detecting Overlaps",
                description="Learn how agents detect overlapping work.",
                step_type=StepType.EXERCISE,
                content=(
                    "Publish two intents that provide the same interface and\n"
                    "check for overlaps:\n\n"
                    "```python\n"
                    "overlaps = resolver.find_overlaps()\n"
                    "for pair in overlaps:\n"
                    "    print(f'Overlap: {pair}')\n"
                    "```\n\n"
                    "Overlaps indicate agents working on the same functionality."
                ),
                hint="Two intents overlap when they provide interfaces with matching names.",
                validation_criteria="At least one overlap is detected between two intents.",
                order=2,
            ),
            TrainingStep(
                step_id="basics-4",
                title="Review: Core Concepts",
                description="Validate your understanding of Convergent basics.",
                step_type=StepType.VALIDATION,
                content=(
                    "Answer these questions:\n\n"
                    "1. What are the two layers of Convergent?\n"
                    "2. What does an Intent represent?\n"
                    "3. How are overlaps detected between agents?\n"
                    "4. Why is the intent graph append-only?"
                ),
                validation_criteria="User can articulate the core concepts clearly.",
                order=3,
            ),
        ],
    ),
    TrainingModule(
        module_id="coordination-protocol",
        title="Coordination Protocol",
        description="Learn the Phase 3 coordination features: voting, stigmergy, and flocking.",
        level=TrainingLevel.INTERMEDIATE,
        topic="coordination",
        prerequisites=["convergent-basics"],
        estimated_steps=5,
        steps=[
            TrainingStep(
                step_id="coord-1",
                title="Phi-Weighted Scoring",
                description="Understand how agent trust scores work.",
                step_type=StepType.CONCEPT,
                content=(
                    "Phi scores measure agent reliability using Bayesian smoothing\n"
                    "with exponential decay:\n\n"
                    "- New agents start at 0.5 (neutral)\n"
                    "- Successful outcomes increase the score\n"
                    "- Failed outcomes decrease it\n"
                    "- Recent outcomes weigh more than old ones\n"
                    "- Scores are bounded [0.1, 0.95] to prevent extremes"
                ),
                order=0,
            ),
            TrainingStep(
                step_id="coord-2",
                title="Triumvirate Voting",
                description="Use the voting engine for consensus decisions.",
                step_type=StepType.EXERCISE,
                content=(
                    "Set up a voting round:\n\n"
                    "```python\n"
                    "from convergent import (\n"
                    "    GorgonBridge, CoordinationConfig\n"
                    ")\n\n"
                    "bridge = GorgonBridge(CoordinationConfig(db_path=':memory:'))\n"
                    "request_id = bridge.request_consensus(\n"
                    "    task_id='task-1',\n"
                    "    question='Should we merge this PR?',\n"
                    "    context='All tests pass, code review complete.',\n"
                    ")\n"
                    "bridge.submit_agent_vote(\n"
                    "    request_id, 'agent-1', 'reviewer',\n"
                    "    'claude:sonnet', 'approve', 0.9,\n"
                    "    'Tests pass and code is clean.',\n"
                    ")\n"
                    "decision = bridge.evaluate(request_id)\n"
                    "print(decision.outcome)\n"
                    "```"
                ),
                hint="Use CoordinationConfig(db_path=':memory:') for testing.",
                validation_criteria="A Decision is produced with a valid outcome.",
                order=1,
            ),
            TrainingStep(
                step_id="coord-3",
                title="Stigmergy Markers",
                description="Learn to leave and read trail markers.",
                step_type=StepType.EXERCISE,
                content=(
                    "Leave markers for other agents to find:\n\n"
                    "```python\n"
                    "bridge.leave_marker(\n"
                    "    agent_id='agent-1',\n"
                    "    marker_type='pattern_found',\n"
                    "    target='src/auth.py',\n"
                    "    content='Uses repository pattern for DB access',\n"
                    ")\n"
                    "context = bridge.enrich_prompt(\n"
                    "    agent_id='agent-2',\n"
                    "    task_description='Add password reset',\n"
                    "    file_paths=['src/auth.py'],\n"
                    ")\n"
                    "print(context)  # Shows the marker info\n"
                    "```"
                ),
                hint="Markers decay over time — recent markers are stronger.",
                validation_criteria="Context string includes the marker content.",
                order=2,
            ),
            TrainingStep(
                step_id="coord-4",
                title="Flocking Coordination",
                description="Understand alignment, cohesion, and separation.",
                step_type=StepType.CONCEPT,
                content=(
                    "Three bio-inspired rules for swarm coordination:\n\n"
                    "- **Alignment**: Agents follow consistent patterns/style\n"
                    "- **Cohesion**: Agents stay focused on the task goal\n"
                    "- **Separation**: Agents avoid modifying the same files\n\n"
                    "These produce emergent group coordination from simple\n"
                    "local rules, like birds flocking."
                ),
                order=3,
            ),
            TrainingStep(
                step_id="coord-5",
                title="Review: Coordination Protocol",
                description="Validate your understanding of coordination features.",
                step_type=StepType.VALIDATION,
                content=(
                    "Answer these questions:\n\n"
                    "1. How does phi scoring prevent score extremes?\n"
                    "2. What quorum levels are available for voting?\n"
                    "3. How do stigmergy markers decay over time?\n"
                    "4. What is the difference between alignment and cohesion?"
                ),
                validation_criteria="User can explain each coordination subsystem.",
                order=4,
            ),
        ],
    ),
    TrainingModule(
        module_id="cross-platform",
        title="Cross-Platform Integration",
        description="Learn to share coordination state across platforms and devices.",
        level=TrainingLevel.ADVANCED,
        topic="cross_platform",
        prerequisites=["convergent-basics", "coordination-protocol"],
        estimated_steps=3,
        steps=[
            TrainingStep(
                step_id="xplat-1",
                title="Platform Detection",
                description="Detect and register platform capabilities.",
                step_type=StepType.EXERCISE,
                content=(
                    "Detect the current platform and register it:\n\n"
                    "```python\n"
                    "from convergent.cross_platform import (\n"
                    "    CrossPlatformHub, detect_platform\n"
                    ")\n\n"
                    "hub = CrossPlatformHub(':memory:')\n"
                    "ctx = detect_platform()\n"
                    "hub.register_platform(ctx)\n"
                    "print(ctx.platform_type, ctx.capabilities)\n"
                    "```"
                ),
                hint="detect_platform() auto-detects OS, Python version, and capabilities.",
                validation_criteria="Platform is registered and retrievable from the hub.",
                order=0,
            ),
            TrainingStep(
                step_id="xplat-2",
                title="State Snapshots",
                description="Create and restore coordination state snapshots.",
                step_type=StepType.EXERCISE,
                content=(
                    "Export state on one platform and restore on another:\n\n"
                    "```python\n"
                    "session_id = hub.create_session(ctx.platform_id)\n"
                    "snapshot = hub.create_snapshot(\n"
                    "    platform_context=ctx,\n"
                    "    session_id=session_id,\n"
                    "    scores={'agent-1': {'code_review': 0.8}},\n"
                    "    metadata={'project': 'my-app'},\n"
                    ")\n\n"
                    "# On another platform:\n"
                    "restored = hub.get_latest_snapshot(session_id)\n"
                    "print(restored.scores)  # Same data!\n"
                    "```"
                ),
                hint="Snapshots are JSON-serializable for network transfer.",
                validation_criteria="Snapshot round-trips correctly across platforms.",
                order=1,
            ),
            TrainingStep(
                step_id="xplat-3",
                title="Session Transfer",
                description="Transfer a coordination session between platforms.",
                step_type=StepType.EXERCISE,
                content=(
                    "Move an active session to a different platform:\n\n"
                    "```python\n"
                    "# Register a second platform\n"
                    "mobile_ctx = PlatformContext(\n"
                    "    platform_id='mobile-1',\n"
                    "    platform_type=PlatformType.MOBILE,\n"
                    "    os_name='android',\n"
                    "    python_version='3.11.0',\n"
                    "    architecture='arm64',\n"
                    ")\n"
                    "hub.register_platform(mobile_ctx)\n\n"
                    "# Transfer session\n"
                    "hub.transfer_session(session_id, 'mobile-1')\n"
                    "session = hub.get_session(session_id)\n"
                    "print(session['current_platform'])  # 'mobile-1'\n"
                    "```"
                ),
                validation_criteria="Session current_platform changes to the target.",
                order=2,
            ),
        ],
    ),
]

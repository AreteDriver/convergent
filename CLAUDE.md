# CLAUDE.md — Convergent: Multi-Agent Coordination Protocol

## What This Project Is

Convergent is a multi-agent coherence and coordination library. It has two layers:

1. **Intent Graph (built, v0.4.0)** — Agents observe a shared intent graph and independently converge on compatible outputs. No inter-agent communication required. This is the ambient awareness layer.

2. **Coordination Protocol (Phase 3, planned)** — Three bio-inspired patterns that sit on top of the intent graph: Triumvirate voting, stigmergy (ant-trail markers), and flocking (emergent group behavior from simple local rules). This is the active coordination layer.

Think of it this way: the intent graph lets agents *see* what others are doing. The coordination protocol lets agents *decide together*, *learn from outcomes*, and *avoid collisions*.

This is an open-source companion to [Gorgon](https://github.com/AreteDriver/Gorgon). It can be used standalone for any multi-agent system that needs coordination, not just Gorgon.

## Tech Stack

- **Python >=3.10** — pure Python, zero production dependencies
- **Rust (optional)** — PyO3 bindings for performance-critical graph operations
- **SQLite** — persistence for intent graph, scores, stigmergy markers, vote history
- **No frameworks** — this is a library, not an application
- **pytest** — testing (430+ tests, 97% coverage)

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         GORGON                                  │
│                   (orchestrator, external)                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       CONVERGENT                                │
│                                                                 │
│  Phase 3: Coordination Protocol (PLANNED)                       │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐             │
│  │ Triumvirate  │  │  Stigmergy   │  │  Flocking  │             │
│  │ (voting)     │  │  (markers)   │  │  (swarm)   │             │
│  │              │  │              │  │            │             │
│  │ N agents     │  │ Leave trails │  │ Alignment  │             │
│  │ phi-weighted │  │ for future   │  │ Cohesion   │             │
│  │ quorum rules │  │ agents       │  │ Separation │             │
│  └──────┬──────┘  └──────┬───────┘  └─────┬──────┘             │
│         └────────┬───────┴─────────────────┘                    │
│                  ▼                                               │
│  Phase 1-2: Intent Graph + Intelligence (BUILT)                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Intent Graph  │  Contracts  │  Governor  │  Economics   │   │
│  │  Constraints   │  Gates      │  Semantic  │  Versioning  │   │
│  │  Matching      │  Replay     │  Benchmark │  Backends    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                  ▼                                               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Backends: PythonGraphBackend │ SQLiteBackend │ Rust(opt) │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
convergent/
├── CLAUDE.md                  ← YOU ARE HERE
├── pyproject.toml             ← v0.4.0, python >=3.10, zero deps
├── Cargo.toml                 ← Rust/PyO3 build config
├── README.md
├── CHANGELOG.md
├── LICENSE                    ← MIT
│
├── python/convergent/         ← Python package (all new modules go here)
│   ├── __init__.py            ← Public API exports (~50 classes)
│   ├── __main__.py            ← CLI inspector
│   ├── intent.py              ← Core: Intent, InterfaceSpec, Constraint, Evidence
│   ├── resolver.py            ← IntentResolver, GraphBackend, PythonGraphBackend
│   ├── matching.py            ← Structural overlap, signature compatibility
│   ├── semantic.py            ← LLM-powered semantic matching (optional anthropic)
│   ├── constraints.py         ← ConstraintEngine, TypedConstraint
│   ├── contract.py            ← IntentGraphContract, validation, conflict detection
│   ├── economics.py           ← Budget, CostModel, EscalationPolicy
│   ├── gates.py               ← GateRunner, PytestGate, MypyGate, CompileGate
│   ├── governor.py            ← MergeGovernor, final decision authority
│   ├── versioning.py          ← VersionedGraph, branching, merging, snapshots
│   ├── sqlite_backend.py      ← SQLite persistence (WAL mode)
│   ├── rust_backend.py        ← Optional Rust PyO3 wrapper (HAS_RUST flag)
│   ├── async_backend.py       ← Async wrapper for graph operations
│   ├── agent.py               ← Simulated agent harness for demos
│   ├── replay.py              ← Replay system for debugging
│   ├── visualization.py       ← Text tables, dot graphs, HTML reports
│   ├── benchmark.py           ← Scaling & performance benchmarks
│   ├── _serialization.py      ← JSON serialization utilities
│   ├── demo.py                ← Demo workflows
│   ├── codegen_demo.py        ← Code generation example
│   │
│   │── # --- Phase 3: Coordination Protocol (PLANNED) ---
│   ├── protocol.py            ← (TODO 1) ConsensusRequest, Vote, Decision, Signal
│   ├── coordination_config.py ← (TODO 1) CoordinationConfig dataclass
│   ├── scoring.py             ← (TODO 2) PhiScorer, phi-weighted trust scores
│   ├── score_store.py         ← (TODO 2) SQLite persistence for scores & votes
│   ├── triumvirate.py         ← (TODO 3) Voting engine with quorum rules
│   ├── signal_bus.py          ← (TODO 4) Pub/sub for agent events
│   ├── stigmergy.py           ← (TODO 5) Trail markers for inter-agent learning
│   ├── flocking.py            ← (TODO 6) Swarm coordination rules
│   └── gorgon_bridge.py       ← (TODO 7) Integration bridge to Gorgon
│
├── src/                       ← Rust core (PyO3) — DO NOT BREAK
│   ├── lib.rs                 ← PyO3 module entry point
│   ├── graph.rs               ← IntentGraph implementation
│   ├── models.rs              ← Rust data models
│   ├── matching.rs            ← Structural matching
│   └── stability.rs           ← Stability scoring
│
├── tests/                     ← 430+ tests, 97% coverage
│   ├── test_convergence.py    ← Core convergence properties
│   ├── test_contract.py       ← Contract validation
│   ├── test_three_layer.py    ← 3-layer coordination stack
│   ├── test_coverage_push.py  ← Edge case coverage
│   ├── test_semantic.py       ← Semantic matching
│   ├── test_sqlite_backend.py ← SQLite backend
│   ├── test_async_backend.py  ← Async backend
│   ├── test_rust_backend.py   ← Rust backend (skips if no Rust)
│   ├── test_hooks.py          ← Hook system
│   ├── test_cli.py            ← CLI inspector
│   ├── test_benchmark_gates_demo.py
│   ├── test_delegation_factory.py
│   ├── test_visualization.py
│   │
│   │── # --- Phase 3 tests (PLANNED) ---
│   ├── test_protocol.py       ← (TODO 1)
│   ├── test_scoring.py        ← (TODO 2)
│   ├── test_triumvirate.py    ← (TODO 3)
│   ├── test_signal_bus.py     ← (TODO 4)
│   ├── test_stigmergy.py      ← (TODO 5)
│   ├── test_flocking.py       ← (TODO 6)
│   └── test_gorgon_bridge.py  ← (TODO 7)
│
├── examples/                  ← (TODO 3, 7) To be created
│   ├── basic_vote.py
│   ├── code_review_consensus.py
│   └── gorgon_integration.py
│
└── scripts/
    └── smoke_test_llm.py      ← Live LLM smoke test
```

## Coding Standards

Same as Gorgon:
- **Type hints on all function signatures.** No exceptions.
- **Docstrings**: Google style. Every public function and class.
- **Imports**: stdlib → third-party → local, separated by blank lines.
- **Naming**: `snake_case` functions/variables, `PascalCase` classes, `UPPER_SNAKE` constants.
- **Error handling**: Specific exceptions only. Log with context.
- **Logging**: `logging` module, never `print()` in library code.
- **No global mutable state.** Dependencies passed explicitly.
- **Tests**: Every module gets a test file. Happy path + edge case + error case minimum.
- **Commits**: Conventional commits.
- **Line length**: 100 chars max (matches ruff config).
- **Target version**: Python 3.10 (matches pyproject.toml).

**Additional for Convergent (library-specific):**
- **No side effects on import.** Importing a module must not create files, open connections, or start threads.
- **Everything is composable.** User should be able to use Triumvirate without Stigmergy, or Signal Bus without voting.
- **Dataclasses over dicts.** All protocol messages are typed dataclasses.
- **Thread-safe where noted.** Signal bus and score store must support concurrent access.
- **Don't break existing modules.** Phase 3 modules are additive — they must not modify existing Phase 1-2 code.
- **Existing SQLite pattern:** See `sqlite_backend.py` for the established pattern (WAL mode, `check_same_thread=False`). New persistence code should follow the same conventions.

## Current State

### What Exists (Phase 1-2: Complete)
- **v0.4.0** — 22 production modules, 430+ tests, 97% coverage
- **Intent graph** — Core data model: Intent, InterfaceSpec, Constraint, Evidence
- **Contract system** — Validation, conflict detection, mutation tracking
- **Three-layer stack** — Constraints → Intent Graph → Economics
- **Governor** — MergeGovernor for final merge/reject decisions
- **Semantic matching** — Structural + optional LLM-powered (anthropic)
- **Backends** — PythonGraphBackend (memory), SQLiteBackend (persistent), RustGraphBackend (optional PyO3)
- **Versioning** — VersionedGraph with branching, merging, snapshots
- **Gates** — Subprocess-backed evidence (pytest, mypy, compile, custom commands)
- **CLI** — Inspector via `__main__.py`
- **Gorgon integration** — `create_delegation_checker()` factory

### What's Missing (Phase 3: Coordination Protocol)
The bio-inspired coordination layer. All items below are additive — they build on top of the existing intent graph, not replace it.

---

## TODO — Build Order (Phase 3)

Complete these in order. Each item is a single Claude Code session.

---

### TODO 1: Coordination Protocol — Data Models
**Branch:** `feat/protocol-core`
**Priority:** P0 — Everything in Phase 3 depends on this
**Estimated tokens:** 15,000

**What:**
Define the foundational data models for the coordination protocol. These are the "words" agents use to communicate during consensus, signaling, and learning.

**Important:** The project already has `pyproject.toml` (v0.4.0), `__init__.py` (50+ exports), and `intent.py` (core data models). This TODO adds *new* modules alongside them. Do NOT recreate or overwrite existing files.

**New files to create:**
- `python/convergent/protocol.py` — coordination-specific dataclasses
- `python/convergent/coordination_config.py` — config for Phase 3 features
- `tests/test_protocol.py` — tests

**Acceptance criteria:**
- [ ] `protocol.py` with all coordination dataclasses (see below)
- [ ] `coordination_config.py` with CoordinationConfig (separate from existing config)
- [ ] New classes exported from `__init__.py` (append to existing exports)
- [ ] All models are immutable where possible (frozen dataclasses)
- [ ] JSON serialization/deserialization on all models
- [ ] Existing tests still pass (`pytest tests/ -v`)

**Data models to implement:**

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import json
from datetime import datetime, timezone


class QuorumLevel(str, Enum):
    """How many agents must agree for a decision to pass."""
    ANY = "any"                    # 1 of N — low-risk reads
    MAJORITY = "majority"          # >50% — medium-risk, recoverable
    UNANIMOUS = "unanimous"        # all — high-risk, irreversible
    UNANIMOUS_HUMAN = "unanimous_human"  # all + human confirm — critical


class VoteChoice(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    ABSTAIN = "abstain"
    ESCALATE = "escalate"  # Agent says "I'm not qualified to judge this"


class DecisionOutcome(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    DEADLOCK = "deadlock"      # No quorum reached
    ESCALATED = "escalated"    # One or more agents escalated


@dataclass(frozen=True)
class AgentIdentity:
    """Identifies an agent in the system."""
    agent_id: str
    role: str          # "planner", "builder", "tester", "reviewer"
    model: str         # "claude:sonnet", "ollama:qwen2.5-coder"
    phi_score: float = 0.5  # Current trust score (0.0 - 1.0)


@dataclass(frozen=True)
class Vote:
    """A single agent's vote on a consensus request."""
    agent: AgentIdentity
    choice: VoteChoice
    confidence: float      # 0.0 - 1.0, how sure the agent is
    reasoning: str         # Why the agent voted this way
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    weighted_score: float = 0.0  # phi_score * confidence, calculated after creation


@dataclass(frozen=True)
class ConsensusRequest:
    """A request for agents to vote on."""
    request_id: str
    task_id: str           # Gorgon task this relates to
    question: str          # What are we deciding?
    context: str           # Relevant information for voters
    quorum: QuorumLevel
    artifacts: list[str] = field(default_factory=list)  # File paths, PR URLs, etc.
    timeout_seconds: int = 300
    requested_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class Decision:
    """The outcome of a consensus round."""
    request: ConsensusRequest
    votes: list[Vote]
    outcome: DecisionOutcome
    total_weighted_approve: float = 0.0
    total_weighted_reject: float = 0.0
    decided_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    human_override: Optional[str] = None  # If human overrode the decision
    reasoning_summary: str = ""  # Aggregated reasoning from votes


@dataclass(frozen=True)
class StigmergyMarker:
    """A trail marker left by an agent for future agents to find."""
    marker_id: str
    agent_id: str
    marker_type: str       # "file_modified", "known_issue", "pattern_found", "dependency"
    target: str            # What this marker refers to (file path, module name, etc.)
    content: str           # The actual information
    strength: float = 1.0  # Decays over time (pheromone evaporation)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expires_at: Optional[str] = None


@dataclass(frozen=True)
class Signal:
    """A message on the signal bus."""
    signal_type: str   # "task_complete", "blocked", "conflict", "resource_available"
    source_agent: str
    target_agent: Optional[str] = None  # None = broadcast
    payload: str = ""   # JSON string with signal-specific data
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
```

**Prompt for Claude Code:**
```
Read CLAUDE.md for project context. Build coordination protocol data models (TODO 1):
1. Create python/convergent/protocol.py with all dataclasses exactly as specified
2. Add to_json() and from_json() class methods on each dataclass
3. Create python/convergent/coordination_config.py with CoordinationConfig dataclass:
   - db_path: str = "./convergent_coordination.db"
   - default_quorum: QuorumLevel = QuorumLevel.MAJORITY
   - phi_decay_rate: float = 0.05 (how fast old scores lose weight)
   - stigmergy_evaporation_rate: float = 0.1 (marker strength decay per day)
   - signal_bus_type: str = "filesystem" (or "redis" later)
   - vote_timeout_seconds: int = 300
4. Export new classes from __init__.py (APPEND to existing exports, don't replace)
5. Write tests/test_protocol.py:
   - Test creating each dataclass
   - Test JSON round-trip serialization
   - Test frozen immutability (vote can't be modified after creation)
   - Test enum values
6. Run full test suite: PYTHONPATH=python pytest tests/ -v (all existing tests must pass)
```

---

### TODO 2: Phi-Weighted Scoring Engine
**Branch:** `feat/phi-scoring`
**Priority:** P0 — Core differentiator
**Estimated tokens:** 15,000

**What:**
Implement the scoring system that tracks agent performance over time and weights their votes accordingly. An agent that consistently produces approved work earns higher vote weight.

The "phi" in phi-weighted references the golden ratio as an aspirational principle — the system seeks the optimal balance between exploitation (trusting proven agents) and exploration (giving newer agents a chance).

**Note:** The project already has `sqlite_backend.py` for intent graph persistence. The scoring system uses a *separate* SQLite database (via `CoordinationConfig.db_path`) to keep concerns isolated. Follow the same SQLite patterns (WAL mode, `check_same_thread=False`).

**New files:**
- `python/convergent/scoring.py`
- `python/convergent/score_store.py` (NOT `store.py` — avoids confusion with existing storage)
- `tests/test_scoring.py`

**Acceptance criteria:**
- [ ] `scoring.py` with PhiScorer class
- [ ] Score calculation: `phi_score = (approved * weight) / total_decisions` with decay
- [ ] Score bounded between 0.1 and 0.95 (never fully trusted, never fully distrusted)
- [ ] Recent decisions weighted more heavily than old ones (exponential decay)
- [ ] Per agent AND per skill domain (an agent good at code review might be bad at testing)
- [ ] SQLite persistence via score_store.py
- [ ] Score recalculation is idempotent

**Algorithm:**
```python
def calculate_phi_score(
    outcomes: list[tuple[str, float]],  # (outcome, timestamp_age_days)
    decay_rate: float = 0.05,
    prior_score: float = 0.5,
    min_score: float = 0.1,
    max_score: float = 0.95,
) -> float:
    """
    Calculate phi-weighted trust score for an agent in a skill domain.

    Each outcome is weighted by recency: weight = e^(-decay_rate * age_days)
    Recent outcomes count more. Very old outcomes fade toward zero influence.

    The prior_score (0.5 = neutral) is used when few observations exist,
    creating a Bayesian-style "pull toward center" that prevents extreme
    scores from small sample sizes.

    Args:
        outcomes: List of ("approved"/"rejected"/"failed", age_in_days) tuples
        decay_rate: How fast old outcomes lose influence (higher = faster decay)
        prior_score: Starting assumption (0.5 = neutral)
        min_score: Floor — agents are never fully distrusted
        max_score: Ceiling — agents are never fully trusted

    Returns:
        Phi score between min_score and max_score
    """
    if not outcomes:
        return prior_score

    weighted_successes = 0.0
    weighted_total = 0.0
    prior_weight = 2.0  # Equivalent to 2 "virtual" neutral observations

    for outcome, age_days in outcomes:
        weight = math.exp(-decay_rate * age_days)
        weighted_total += weight
        if outcome == "approved":
            weighted_successes += weight

    # Bayesian smoothing: mix observed rate with prior
    raw_score = (weighted_successes + prior_weight * prior_score) / (weighted_total + prior_weight)
    return max(min_score, min(max_score, raw_score))
```

**Prompt for Claude Code:**
```
Read CLAUDE.md for project context. Implement phi-weighted scoring (TODO 2):
1. Create python/convergent/scoring.py with PhiScorer class:
   - __init__(store: ScoreStore) — takes persistence layer
   - calculate_phi_score() — implements the algorithm above
   - record_outcome(agent_id, skill_domain, outcome) — records and recalculates
   - get_score(agent_id, skill_domain) -> float — returns current score
   - get_all_scores(agent_id) -> dict[str, float] — all domains for an agent
   - apply_vote_weight(vote: Vote) -> Vote — returns new Vote with weighted_score set
2. Create python/convergent/score_store.py with ScoreStore class:
   - SQLite backend (follow patterns from sqlite_backend.py: WAL mode, check_same_thread=False)
   - Tables: outcomes (agent_id, skill_domain, outcome, timestamp), scores (agent_id, skill_domain, phi_score, last_updated)
   - Thread-safe
3. Export new classes from __init__.py (APPEND to existing exports)
4. Write tests/test_scoring.py:
   - test_new_agent_gets_prior_score (0.5)
   - test_all_approvals_trends_toward_max (but never reaches 0.95)
   - test_all_rejections_trends_toward_min (but never reaches 0.1)
   - test_recent_outcomes_weighted_higher (approve old, reject recent → score drops)
   - test_mixed_outcomes_converge_to_ratio
   - test_score_bounded (never below 0.1, never above 0.95)
   - test_per_domain_independence (good at review, bad at testing)
5. Run full test suite: PYTHONPATH=python pytest tests/ -v
```

---

### TODO 3: Triumvirate Voting Engine
**Branch:** `feat/triumvirate`
**Priority:** P0 — Core consensus mechanism
**Estimated tokens:** 18,000

**What:**
Implement the voting engine that collects votes from agents, applies phi-weighted scoring, evaluates quorum, and produces a Decision.

**New files:**
- `python/convergent/triumvirate.py`
- `tests/test_triumvirate.py`
- `examples/basic_vote.py`

**Acceptance criteria:**
- [ ] `triumvirate.py` with Triumvirate class
- [ ] Supports all QuorumLevel values
- [ ] Votes are phi-weighted: `weighted_score = phi_score * confidence`
- [ ] Quorum evaluation considers weights, not just counts
- [ ] Handles edge cases: abstentions, escalations, timeouts, ties
- [ ] Disagreement resolution: highest-weighted vote breaks ties
- [ ] Full vote audit trail (every vote recorded with reasoning)
- [ ] Works with 2-5 agents (not hardcoded to exactly 3)

**Quorum rules:**

| Level | Rule |
|-------|------|
| ANY | Weighted approve sum > 0 (at least one agent approves) |
| MAJORITY | Weighted approve sum > weighted reject sum |
| UNANIMOUS | All votes are approve (abstain/escalate don't count against) |
| UNANIMOUS_HUMAN | All votes approve AND human confirms |

**Prompt for Claude Code:**
```
Read CLAUDE.md for project context. Implement Triumvirate voting engine (TODO 3):
1. Create python/convergent/triumvirate.py with Triumvirate class:
   - __init__(scorer: PhiScorer, config: CoordinationConfig)
   - create_request(task_id, question, context, quorum, artifacts) -> ConsensusRequest
   - submit_vote(request_id, vote: Vote) -> None
   - evaluate(request_id) -> Decision
     - Collect all votes for request
     - Apply phi weights via scorer.apply_vote_weight()
     - Sum weighted approve vs reject
     - Check quorum rules
     - Handle ties: highest weighted_score wins
     - Handle escalations: if any agent escalates, outcome = ESCALATED
     - Handle timeouts: if vote_timeout exceeded, outcome = DEADLOCK
   - get_decision(request_id) -> Optional[Decision]
   - get_vote_history(task_id) -> list[Decision]
2. Store votes and decisions in SQLite via score_store.py (add tables)
3. Export new classes from __init__.py (APPEND to existing exports)
4. Write tests/test_triumvirate.py:
   - test_majority_approve (2/3 approve, passes)
   - test_majority_reject (2/3 reject, fails)
   - test_unanimous_with_abstain (2 approve + 1 abstain = passes)
   - test_unanimous_with_reject (2 approve + 1 reject = fails)
   - test_phi_weight_breaks_tie (1 high-trust approve vs 1 low-trust reject)
   - test_escalation_overrides (any escalate → ESCALATED)
   - test_any_quorum_single_approve
   - test_deadlock_on_timeout
5. Create examples/ directory and write examples/basic_vote.py:
   - Create 3 agents with different phi scores
   - Submit a code review consensus request
   - Each agent votes
   - Evaluate and print decision
6. Run full test suite: PYTHONPATH=python pytest tests/ -v
```

---

### TODO 4: Signal Bus
**Branch:** `feat/signal-bus`
**Priority:** P1 — Agent-to-agent communication
**Estimated tokens:** 12,000

**What:**
Lightweight pub/sub system for agents to signal each other. Filesystem-based for simplicity (Redis adapter later).

Signals are how agents say: "I'm blocked on X", "I finished Y, you can start Z", "I found a conflict in file W."

**New files:**
- `python/convergent/signal_bus.py`
- `tests/test_signal_bus.py`

**Acceptance criteria:**
- [ ] `signal_bus.py` with SignalBus class
- [ ] Publish signals (broadcast or targeted to specific agent)
- [ ] Subscribe to signal types with callback functions
- [ ] Filesystem backend: signals written as JSON to a signals/ directory
- [ ] Polling-based consumption (configurable interval)
- [ ] Signal expiry (auto-delete after TTL)
- [ ] Thread-safe publish and consume

**Prompt for Claude Code:**
```
Read CLAUDE.md for project context. Implement Signal Bus (TODO 4):
1. Create python/convergent/signal_bus.py with SignalBus class:
   - __init__(signals_dir: Path, poll_interval: float = 1.0)
   - publish(signal: Signal) -> None — write JSON to signals_dir
   - subscribe(signal_type: str, callback: Callable[[Signal], None]) -> None
   - start_polling() -> None — background thread that reads new signals and dispatches
   - stop_polling() -> None
   - get_signals(signal_type: str, since: datetime) -> list[Signal]
   - cleanup_expired(max_age_seconds: int = 3600) -> int — returns count deleted
2. Filesystem format: signals/{timestamp}_{signal_type}_{source_agent}.json
3. Polling reads new files since last check, calls matching subscribers, then optionally deletes
4. Export new classes from __init__.py (APPEND to existing exports)
5. Write tests/test_signal_bus.py:
   - test_publish_creates_file
   - test_subscribe_receives_signal
   - test_targeted_signal_only_reaches_target
   - test_broadcast_reaches_all_subscribers
   - test_expired_signals_cleaned_up
6. Run full test suite: PYTHONPATH=python pytest tests/ -v
```

---

### TODO 5: Stigmergy — Trail Markers
**Branch:** `feat/stigmergy`
**Priority:** P1 — Inter-agent learning
**Estimated tokens:** 12,000

**What:**
Agents leave markers that influence future agents. Like ant pheromone trails — "this file was recently modified", "this function has a known bug", "this pattern worked well here."

Markers decay over time (evaporation), so stale information fades naturally.

**New files:**
- `python/convergent/stigmergy.py`
- `tests/test_stigmergy.py`

**Acceptance criteria:**
- [ ] `stigmergy.py` with StigmergyField class
- [ ] Leave markers (type, target, content, initial strength)
- [ ] Query markers by target or type
- [ ] Strength decays over time (exponential, configurable rate)
- [ ] Markers below minimum strength auto-removed
- [ ] Reinforcement: multiple agents marking the same target increases strength
- [ ] SQLite persistence via score_store.py

**Marker types:**
- `file_modified` — "I changed src/auth.py" (warns other agents of potential conflicts)
- `known_issue` — "The login endpoint has a race condition" (knowledge sharing)
- `pattern_found` — "This repo uses repository pattern for DB access" (style guidance)
- `dependency` — "Module X depends on Module Y being complete" (sequencing hints)
- `quality_signal` — "Tests in test_auth.py are flaky" (reliability info)

**Prompt for Claude Code:**
```
Read CLAUDE.md for project context. Implement Stigmergy system (TODO 5):
1. Create python/convergent/stigmergy.py with StigmergyField class:
   - __init__(store: ScoreStore, evaporation_rate: float = 0.1)
   - leave_marker(agent_id, marker_type, target, content, strength=1.0) -> StigmergyMarker
   - get_markers(target: str) -> list[StigmergyMarker] — all markers for a target
   - get_markers_by_type(marker_type: str) -> list[StigmergyMarker]
   - reinforce(marker_id: str, amount: float = 0.5) — increase strength
   - evaporate() — decay all marker strengths, remove below threshold (0.05)
   - get_context_for_agent(file_paths: list[str]) -> str — build a context string
     from all relevant markers for files an agent is about to work on
2. Add stigmergy_markers table to score_store.py:
   (marker_id, agent_id, marker_type, target, content, strength, created_at, expires_at)
3. Evaporation formula: new_strength = strength * e^(-evaporation_rate * age_days)
4. get_context_for_agent() is the key integration point with Gorgon:
   before an agent starts work, Gorgon calls this to get "here's what previous agents
   learned about these files" and injects it into the agent prompt
5. Export new classes from __init__.py (APPEND to existing exports)
6. Write tests/test_stigmergy.py:
   - test_leave_and_retrieve_marker
   - test_evaporation_reduces_strength
   - test_expired_markers_removed
   - test_reinforcement_increases_strength
   - test_context_for_agent_includes_relevant_markers
   - test_context_excludes_expired_markers
7. Run full test suite: PYTHONPATH=python pytest tests/ -v
```

---

### TODO 6: Flocking — Swarm Coordination
**Branch:** `feat/flocking`
**Priority:** P2 — Emergent behavior optimization
**Estimated tokens:** 15,000

**What:**
Implement the three flocking rules (alignment, cohesion, separation) adapted for AI agents. This governs how agents behave as a group when working on related tasks.

- **Alignment:** Agents working on related code should use consistent patterns/style
- **Cohesion:** Agents should stay focused on the overall goal, not drift
- **Separation:** Agents should not step on each other's work (file scope isolation)

**New files:**
- `python/convergent/flocking.py`
- `tests/test_flocking.py`

**Acceptance criteria:**
- [ ] `flocking.py` with FlockingCoordinator class
- [ ] Alignment: detect when agents are working on related files, share style context
- [ ] Cohesion: measure drift from original task scope, flag when agent wanders
- [ ] Separation: enforce file-scope boundaries, detect overlapping modifications
- [ ] Generates constraints that are injected into agent prompts
- [ ] Works with stigmergy markers (reads file_modified markers for separation)

**Prompt for Claude Code:**
```
Read CLAUDE.md for project context. Implement Flocking coordination (TODO 6):
1. Create python/convergent/flocking.py with FlockingCoordinator class:
   - __init__(stigmergy: StigmergyField, config: CoordinationConfig)
   - check_alignment(agent_id: str, file_paths: list[str]) -> list[str]
     Returns style/pattern constraints based on what other agents did in related files
   - check_cohesion(agent_id: str, task_description: str, current_work: str) -> float
     Returns 0.0-1.0 drift score. High = agent is wandering from task scope.
   - check_separation(agent_id: str, file_paths: list[str]) -> list[str]
     Returns list of files that another agent is currently modifying (conflict risk)
   - generate_constraints(agent_id, task, files) -> str
     Combines all three checks into a constraint block for the agent prompt
2. Alignment uses stigmergy pattern_found markers
3. Separation uses stigmergy file_modified markers
4. Cohesion uses keyword overlap between task description and current work
5. Export new classes from __init__.py (APPEND to existing exports)
6. Write tests/test_flocking.py:
   - test_separation_detects_file_overlap
   - test_alignment_shares_patterns
   - test_cohesion_detects_drift
   - test_generate_constraints_combines_all_three
7. Run full test suite: PYTHONPATH=python pytest tests/ -v
```

---

### TODO 7: Gorgon Integration Bridge
**Branch:** `feat/gorgon-integration`
**Priority:** P1 — Connects Phase 3 to Gorgon
**Estimated tokens:** 12,000

**What:**
Create the bridge module that Gorgon imports to use Convergent's coordination protocol for consensus decisions, agent scoring, and context enrichment. This complements the existing `create_delegation_checker()` factory which handles intent graph delegation.

**New files:**
- `python/convergent/gorgon_bridge.py`
- `tests/test_gorgon_bridge.py`
- `examples/gorgon_integration.py`

**Acceptance criteria:**
- [ ] `gorgon_bridge.py` with GorgonBridge class
- [ ] Single entry point: Gorgon calls bridge, bridge coordinates internally
- [ ] Before task dispatch: enrich prompt with stigmergy context + flocking constraints
- [ ] After task completion: record outcome, update phi scores, leave markers
- [ ] For quality gates: run Triumvirate vote, return decision
- [ ] Clean API that Gorgon's pipeline.py can call with minimal changes
- [ ] Graceful degradation if subsystems aren't configured

**Prompt for Claude Code:**
```
Read CLAUDE.md for project context. Implement Gorgon integration bridge (TODO 7):
1. Create python/convergent/gorgon_bridge.py with GorgonBridge class:
   - __init__(config: CoordinationConfig)
     Initializes all subsystems: PhiScorer, Triumvirate, StigmergyField, FlockingCoordinator, SignalBus
   - enrich_prompt(agent_id, task_description, file_paths) -> str
     Returns additional context to inject into the agent prompt:
     stigmergy markers + flocking constraints + agent's phi score context
   - request_consensus(task_id, question, context, quorum, artifacts) -> str
     Creates a ConsensusRequest, returns request_id
   - submit_agent_vote(request_id, agent_id, role, model, choice, confidence, reasoning) -> None
   - get_decision(request_id) -> Optional[Decision]
   - record_task_outcome(agent_id, skill_domain, outcome, file_paths) -> None
     Updates phi score + leaves stigmergy markers
   - get_agent_score(agent_id, skill_domain) -> float
2. Export new classes from __init__.py (APPEND to existing exports)
3. Write examples/gorgon_integration.py showing:
   - Pipeline creates a task
   - Bridge enriches the prompt with context
   - Agent executes
   - Bridge runs consensus
   - Bridge records outcome
4. Write tests/test_gorgon_bridge.py:
   - test_full_lifecycle (create → enrich → execute → vote → record)
   - test_enrichment_includes_markers
   - test_outcome_updates_score
5. Run full test suite: PYTHONPATH=python pytest tests/ -v
```

---

### TODO 8: README Update
**Branch:** `feat/readme-update`
**Priority:** P0 — Must be done before announcing Phase 3
**Estimated tokens:** 10,000

**What:**
Update the existing README to cover both the intent graph (Phase 1-2) and the coordination protocol (Phase 3). Don't replace — extend.

**Acceptance criteria:**
- [ ] Updated one-sentence description covering both layers
- [ ] Mermaid diagram of the full architecture (intent graph + coordination)
- [ ] "Why Convergent?" section explaining both ambient awareness and bio-inspired coordination
- [ ] Quick start examples: intent graph usage AND basic vote
- [ ] API reference for core classes (both layers)
- [ ] Gorgon integration guide (both `create_delegation_checker` and `GorgonBridge`)
- [ ] Feature matrix with status
- [ ] Version bumped to 0.5.0

**Prompt for Claude Code:**
```
Read CLAUDE.md for project context. Update the Convergent README (TODO 8):
1. Read the existing README.md first — preserve what's there, extend it
2. Updated opening: "Convergent is a multi-agent coherence and coordination library
   for AI systems, combining ambient intent awareness with bio-inspired coordination."
3. Add sections for Phase 3 features:
   - Triumvirate: weighted voting for collective decisions
   - Stigmergy: trail markers for indirect communication
   - Flocking: local rules for emergent group coordination
4. Add Mermaid diagram showing both layers
5. Add quick start for basic voting alongside existing intent graph examples
6. Update feature matrix to show Phase 1-2 (complete) and Phase 3 (complete)
7. Bump version to 0.5.0 in pyproject.toml and __init__.py
8. Run full test suite: PYTHONPATH=python pytest tests/ -v
```

---

## What NOT To Modify

- The **append-only invariant** of IntentGraph (core design principle)
- **Stability scoring weights** without updating tests
- **PyO3 bindings** without matching Python fallback implementations
- **Existing module APIs** — Phase 3 is additive, not a rewrite
- **pyproject.toml** structure — only append new optional deps if needed
- **Rust source** (`src/`) — Phase 3 is pure Python

## Build & Test

```bash
# Python only (no Rust needed)
PYTHONPATH=python pytest tests/ -v

# With Rust core (optional, for performance)
maturin develop --release
pytest tests/ -v

# Run demo
PYTHONPATH=python python -m convergent

# Lint
ruff check python/ tests/
ruff format python/ tests/
```

## Rules for All Claude Code Sessions

1. **Read this file first.** Every session starts by reading CLAUDE.md.
2. **One TODO per session.** Don't combine items. Each has its own branch.
3. **Branch naming:** Use the branch name specified in the TODO.
4. **This is a library, not an app.** No servers, no daemons. The existing CLI inspector is the only entry point.
5. **Test before committing.** Run `PYTHONPATH=python pytest tests/ -v`. ALL tests must pass (existing + new).
6. **Commit messages:** Conventional commits. Reference the TODO number.
7. **Don't modify files outside scope.** Each TODO lists what it creates. Existing modules are read-only unless the TODO explicitly says otherwise.
8. **Composable design.** Every component must work independently. No circular imports. No hidden dependencies between modules.
9. **Append to __init__.py.** New exports go at the bottom. Don't reorganize existing exports.
10. **Ask if unclear.** Document assumptions in code comments.
11. **Budget awareness.** If tokens are running low, finish the current file cleanly and document remaining work in `# TODO:` comments.
12. **All new files go in `python/convergent/`.** Not in a top-level `convergent/` directory.

## Related Skills

From [ai-skills](https://github.com/AreteDriver/ai-skills):
- `intent-author` — teaches agents how to publish well-structured intents
- `entity-resolver` — shared entity identity across parallel agents

"""Tests for convergent.training user education and training tools."""

from __future__ import annotations

import pytest
from convergent.training import (
    StepStatus,
    StepType,
    TrainingLevel,
    TrainingManager,
    TrainingModule,
    TrainingProgress,
    TrainingStep,
)

# --- Enum tests ---


class TestTrainingLevel:
    def test_values(self) -> None:
        assert TrainingLevel.BEGINNER == "beginner"
        assert TrainingLevel.INTERMEDIATE == "intermediate"
        assert TrainingLevel.ADVANCED == "advanced"

    def test_from_string(self) -> None:
        assert TrainingLevel("beginner") is TrainingLevel.BEGINNER

    def test_all_members(self) -> None:
        assert len(TrainingLevel) == 3


class TestStepType:
    def test_values(self) -> None:
        assert StepType.CONCEPT == "concept"
        assert StepType.EXERCISE == "exercise"
        assert StepType.VALIDATION == "validation"

    def test_all_members(self) -> None:
        assert len(StepType) == 3


class TestStepStatus:
    def test_values(self) -> None:
        assert StepStatus.PENDING == "pending"
        assert StepStatus.IN_PROGRESS == "in_progress"
        assert StepStatus.COMPLETED == "completed"
        assert StepStatus.SKIPPED == "skipped"

    def test_all_members(self) -> None:
        assert len(StepStatus) == 4


# --- TrainingStep ---


class TestTrainingStep:
    def test_creation(self) -> None:
        step = TrainingStep(
            step_id="step-1",
            title="Test Step",
            description="A test step.",
            step_type=StepType.CONCEPT,
            content="Learn about testing.",
        )
        assert step.step_id == "step-1"
        assert step.title == "Test Step"
        assert step.step_type == StepType.CONCEPT
        assert step.content == "Learn about testing."
        assert step.hint == ""
        assert step.order == 0

    def test_json_round_trip(self) -> None:
        step = TrainingStep(
            step_id="step-1",
            title="Exercise",
            description="Do something.",
            step_type=StepType.EXERCISE,
            content="Code example here.",
            hint="Use the PythonGraphBackend.",
            validation_criteria="Test passes.",
            order=2,
        )
        json_str = step.to_json()
        restored = TrainingStep.from_json(json_str)
        assert restored.step_id == step.step_id
        assert restored.step_type == StepType.EXERCISE
        assert restored.hint == "Use the PythonGraphBackend."
        assert restored.order == 2

    def test_frozen(self) -> None:
        step = TrainingStep(
            step_id="step-1",
            title="Test",
            description="Test",
            step_type=StepType.CONCEPT,
            content="Content",
        )
        with pytest.raises(AttributeError):
            step.title = "New Title"  # type: ignore[misc]


# --- TrainingModule ---


class TestTrainingModule:
    def test_creation(self) -> None:
        module = TrainingModule(
            module_id="mod-1",
            title="Test Module",
            description="A test module.",
            level=TrainingLevel.BEGINNER,
            topic="testing",
            estimated_steps=2,
        )
        assert module.module_id == "mod-1"
        assert module.level == TrainingLevel.BEGINNER
        assert module.steps == []
        assert module.prerequisites == []

    def test_with_steps(self) -> None:
        steps = [
            TrainingStep(
                step_id="s1",
                title="Step 1",
                description="First",
                step_type=StepType.CONCEPT,
                content="Content 1",
                order=0,
            ),
            TrainingStep(
                step_id="s2",
                title="Step 2",
                description="Second",
                step_type=StepType.EXERCISE,
                content="Content 2",
                order=1,
            ),
        ]
        module = TrainingModule(
            module_id="mod-1",
            title="Test Module",
            description="Test",
            level=TrainingLevel.INTERMEDIATE,
            topic="testing",
            steps=steps,
            estimated_steps=2,
        )
        assert len(module.steps) == 2
        assert module.steps[0].step_id == "s1"
        assert module.steps[1].step_type == StepType.EXERCISE

    def test_json_round_trip(self) -> None:
        module = TrainingModule(
            module_id="mod-1",
            title="Test Module",
            description="A module.",
            level=TrainingLevel.ADVANCED,
            topic="coordination",
            prerequisites=["mod-0"],
            estimated_steps=1,
            steps=[
                TrainingStep(
                    step_id="s1",
                    title="Step 1",
                    description="Do it",
                    step_type=StepType.VALIDATION,
                    content="Quiz here",
                    order=0,
                ),
            ],
        )
        json_str = module.to_json()
        restored = TrainingModule.from_json(json_str)
        assert restored.module_id == module.module_id
        assert restored.level == TrainingLevel.ADVANCED
        assert restored.prerequisites == ["mod-0"]
        assert len(restored.steps) == 1
        assert restored.steps[0].step_type == StepType.VALIDATION

    def test_frozen(self) -> None:
        module = TrainingModule(
            module_id="mod-1",
            title="Test",
            description="Test",
            level=TrainingLevel.BEGINNER,
            topic="test",
        )
        with pytest.raises(AttributeError):
            module.title = "New"  # type: ignore[misc]


# --- TrainingProgress ---


class TestTrainingProgress:
    def test_creation(self) -> None:
        progress = TrainingProgress(
            progress_id="prog-1",
            user_id="user-1",
            module_id="mod-1",
            step_statuses={"s1": "pending", "s2": "pending"},
        )
        assert progress.user_id == "user-1"
        assert progress.completed_at is None
        assert progress.current_step_index == 0

    def test_completed_steps(self) -> None:
        progress = TrainingProgress(
            progress_id="prog-1",
            user_id="user-1",
            module_id="mod-1",
            step_statuses={
                "s1": StepStatus.COMPLETED.value,
                "s2": StepStatus.COMPLETED.value,
                "s3": StepStatus.PENDING.value,
            },
        )
        assert progress.completed_steps == 2
        assert progress.total_steps == 3

    def test_completion_ratio(self) -> None:
        progress = TrainingProgress(
            progress_id="prog-1",
            user_id="user-1",
            module_id="mod-1",
            step_statuses={
                "s1": StepStatus.COMPLETED.value,
                "s2": StepStatus.PENDING.value,
            },
        )
        assert progress.completion_ratio == pytest.approx(0.5)

    def test_completion_ratio_empty(self) -> None:
        progress = TrainingProgress(
            progress_id="prog-1",
            user_id="user-1",
            module_id="mod-1",
        )
        assert progress.completion_ratio == 0.0

    def test_is_complete_all_done(self) -> None:
        progress = TrainingProgress(
            progress_id="prog-1",
            user_id="user-1",
            module_id="mod-1",
            step_statuses={
                "s1": StepStatus.COMPLETED.value,
                "s2": StepStatus.SKIPPED.value,
            },
        )
        assert progress.is_complete is True

    def test_is_complete_not_done(self) -> None:
        progress = TrainingProgress(
            progress_id="prog-1",
            user_id="user-1",
            module_id="mod-1",
            step_statuses={
                "s1": StepStatus.COMPLETED.value,
                "s2": StepStatus.PENDING.value,
            },
        )
        assert progress.is_complete is False

    def test_is_complete_empty(self) -> None:
        progress = TrainingProgress(
            progress_id="prog-1",
            user_id="user-1",
            module_id="mod-1",
        )
        assert progress.is_complete is False

    def test_json_round_trip(self) -> None:
        progress = TrainingProgress(
            progress_id="prog-1",
            user_id="user-1",
            module_id="mod-1",
            step_statuses={"s1": "completed", "s2": "pending"},
            current_step_index=1,
        )
        json_str = progress.to_json()
        restored = TrainingProgress.from_json(json_str)
        assert restored.progress_id == progress.progress_id
        assert restored.step_statuses == progress.step_statuses
        assert restored.current_step_index == 1

    def test_mutable(self) -> None:
        progress = TrainingProgress(
            progress_id="prog-1",
            user_id="user-1",
            module_id="mod-1",
            step_statuses={"s1": "pending"},
        )
        progress.step_statuses["s1"] = StepStatus.COMPLETED.value
        assert progress.step_statuses["s1"] == "completed"


# --- TrainingManager ---


class TestTrainingManagerModules:
    def test_register_and_get_module(self) -> None:
        mgr = TrainingManager(":memory:", auto_register_builtins=False)
        module = TrainingModule(
            module_id="mod-1",
            title="Test Module",
            description="A module.",
            level=TrainingLevel.BEGINNER,
            topic="testing",
            steps=[
                TrainingStep(
                    step_id="s1",
                    title="Step 1",
                    description="Do it",
                    step_type=StepType.CONCEPT,
                    content="Content",
                    order=0,
                ),
            ],
            estimated_steps=1,
        )
        mgr.register_module(module)
        retrieved = mgr.get_module("mod-1")
        assert retrieved is not None
        assert retrieved.title == "Test Module"
        assert len(retrieved.steps) == 1

    def test_get_nonexistent_module(self) -> None:
        mgr = TrainingManager(":memory:", auto_register_builtins=False)
        assert mgr.get_module("nonexistent") is None

    def test_list_modules(self) -> None:
        mgr = TrainingManager(":memory:", auto_register_builtins=False)
        mgr.register_module(TrainingModule(
            module_id="mod-1",
            title="Basics",
            description="Basics",
            level=TrainingLevel.BEGINNER,
            topic="overview",
        ))
        mgr.register_module(TrainingModule(
            module_id="mod-2",
            title="Advanced",
            description="Advanced",
            level=TrainingLevel.ADVANCED,
            topic="coordination",
        ))
        modules = mgr.list_modules()
        assert len(modules) == 2

    def test_list_modules_by_level(self) -> None:
        mgr = TrainingManager(":memory:", auto_register_builtins=False)
        mgr.register_module(TrainingModule(
            module_id="mod-1",
            title="Basics",
            description="Basics",
            level=TrainingLevel.BEGINNER,
            topic="overview",
        ))
        mgr.register_module(TrainingModule(
            module_id="mod-2",
            title="Advanced",
            description="Advanced",
            level=TrainingLevel.ADVANCED,
            topic="coordination",
        ))
        beginners = mgr.list_modules(level=TrainingLevel.BEGINNER)
        assert len(beginners) == 1
        assert beginners[0].module_id == "mod-1"

    def test_list_modules_by_topic(self) -> None:
        mgr = TrainingManager(":memory:", auto_register_builtins=False)
        mgr.register_module(TrainingModule(
            module_id="mod-1",
            title="Basics",
            description="Basics",
            level=TrainingLevel.BEGINNER,
            topic="overview",
        ))
        mgr.register_module(TrainingModule(
            module_id="mod-2",
            title="Coordination",
            description="Coordination",
            level=TrainingLevel.INTERMEDIATE,
            topic="coordination",
        ))
        coord = mgr.list_modules(topic="coordination")
        assert len(coord) == 1
        assert coord[0].module_id == "mod-2"


class TestTrainingManagerBuiltins:
    def test_builtin_modules_registered(self) -> None:
        mgr = TrainingManager(":memory:", auto_register_builtins=True)
        modules = mgr.list_modules()
        assert len(modules) >= 3

    def test_basics_module_exists(self) -> None:
        mgr = TrainingManager(":memory:")
        module = mgr.get_module("convergent-basics")
        assert module is not None
        assert module.title == "Convergent Basics"
        assert module.level == TrainingLevel.BEGINNER
        assert len(module.steps) >= 3

    def test_coordination_module_exists(self) -> None:
        mgr = TrainingManager(":memory:")
        module = mgr.get_module("coordination-protocol")
        assert module is not None
        assert "convergent-basics" in module.prerequisites

    def test_cross_platform_module_exists(self) -> None:
        mgr = TrainingManager(":memory:")
        module = mgr.get_module("cross-platform")
        assert module is not None
        assert module.level == TrainingLevel.ADVANCED
        assert "convergent-basics" in module.prerequisites
        assert "coordination-protocol" in module.prerequisites

    def test_builtins_not_duplicated_on_reopen(self, tmp_path: object) -> None:
        import pathlib

        db_path = str(pathlib.Path(str(tmp_path)) / "training.db")
        mgr1 = TrainingManager(db_path)
        count1 = len(mgr1.list_modules())
        mgr1.close()

        mgr2 = TrainingManager(db_path)
        count2 = len(mgr2.list_modules())
        mgr2.close()
        assert count1 == count2


class TestTrainingManagerProgress:
    def _make_manager_with_module(self) -> tuple[TrainingManager, TrainingModule]:
        mgr = TrainingManager(":memory:", auto_register_builtins=False)
        module = TrainingModule(
            module_id="mod-1",
            title="Test Module",
            description="Test",
            level=TrainingLevel.BEGINNER,
            topic="testing",
            steps=[
                TrainingStep(
                    step_id="s1", title="Step 1", description="First",
                    step_type=StepType.CONCEPT, content="Content 1", order=0,
                ),
                TrainingStep(
                    step_id="s2", title="Step 2", description="Second",
                    step_type=StepType.EXERCISE, content="Content 2", order=1,
                ),
                TrainingStep(
                    step_id="s3", title="Step 3", description="Third",
                    step_type=StepType.VALIDATION, content="Content 3", order=2,
                ),
            ],
            estimated_steps=3,
        )
        mgr.register_module(module)
        return mgr, module

    def test_start_module(self) -> None:
        mgr, module = self._make_manager_with_module()
        progress = mgr.start_module("user-1", "mod-1")
        assert progress.user_id == "user-1"
        assert progress.module_id == "mod-1"
        assert len(progress.step_statuses) == 3
        assert all(s == StepStatus.PENDING.value for s in progress.step_statuses.values())
        assert progress.current_step_index == 0

    def test_start_module_nonexistent_raises(self) -> None:
        mgr = TrainingManager(":memory:", auto_register_builtins=False)
        with pytest.raises(ValueError, match="not found"):
            mgr.start_module("user-1", "nonexistent")

    def test_start_module_idempotent(self) -> None:
        mgr, _ = self._make_manager_with_module()
        p1 = mgr.start_module("user-1", "mod-1")
        p2 = mgr.start_module("user-1", "mod-1")
        assert p1.progress_id == p2.progress_id

    def test_advance_step(self) -> None:
        mgr, _ = self._make_manager_with_module()
        mgr.start_module("user-1", "mod-1")
        progress = mgr.advance_step("user-1", "mod-1", "s1", StepStatus.COMPLETED)
        assert progress.step_statuses["s1"] == StepStatus.COMPLETED.value
        assert progress.current_step_index == 1

    def test_advance_step_skip(self) -> None:
        mgr, _ = self._make_manager_with_module()
        mgr.start_module("user-1", "mod-1")
        progress = mgr.advance_step("user-1", "mod-1", "s1", StepStatus.SKIPPED)
        assert progress.step_statuses["s1"] == StepStatus.SKIPPED.value
        assert progress.current_step_index == 1

    def test_advance_step_no_progress_raises(self) -> None:
        mgr, _ = self._make_manager_with_module()
        with pytest.raises(ValueError, match="No progress"):
            mgr.advance_step("user-1", "mod-1", "s1")

    def test_advance_step_bad_step_raises(self) -> None:
        mgr, _ = self._make_manager_with_module()
        mgr.start_module("user-1", "mod-1")
        with pytest.raises(ValueError, match="Step .* not found"):
            mgr.advance_step("user-1", "mod-1", "nonexistent")

    def test_complete_all_steps(self) -> None:
        mgr, _ = self._make_manager_with_module()
        mgr.start_module("user-1", "mod-1")
        mgr.advance_step("user-1", "mod-1", "s1", StepStatus.COMPLETED)
        mgr.advance_step("user-1", "mod-1", "s2", StepStatus.COMPLETED)
        progress = mgr.advance_step("user-1", "mod-1", "s3", StepStatus.COMPLETED)
        assert progress.is_complete is True
        assert progress.completed_at is not None

    def test_get_progress(self) -> None:
        mgr, _ = self._make_manager_with_module()
        mgr.start_module("user-1", "mod-1")
        progress = mgr.get_progress("user-1", "mod-1")
        assert progress is not None
        assert progress.user_id == "user-1"

    def test_get_progress_nonexistent(self) -> None:
        mgr, _ = self._make_manager_with_module()
        assert mgr.get_progress("user-1", "mod-1") is None

    def test_get_all_progress(self) -> None:
        mgr = TrainingManager(":memory:", auto_register_builtins=False)
        mgr.register_module(TrainingModule(
            module_id="mod-1", title="A", description="A",
            level=TrainingLevel.BEGINNER, topic="a",
            steps=[TrainingStep(
                step_id="s1", title="S1", description="D",
                step_type=StepType.CONCEPT, content="C",
            )],
        ))
        mgr.register_module(TrainingModule(
            module_id="mod-2", title="B", description="B",
            level=TrainingLevel.BEGINNER, topic="b",
            steps=[TrainingStep(
                step_id="s2", title="S2", description="D",
                step_type=StepType.CONCEPT, content="C",
            )],
        ))
        mgr.start_module("user-1", "mod-1")
        mgr.start_module("user-1", "mod-2")
        progress = mgr.get_all_progress("user-1")
        assert len(progress) == 2

    def test_get_current_step(self) -> None:
        mgr, _ = self._make_manager_with_module()
        mgr.start_module("user-1", "mod-1")
        step = mgr.get_current_step("user-1", "mod-1")
        assert step is not None
        assert step.step_id == "s1"

    def test_get_current_step_after_advance(self) -> None:
        mgr, _ = self._make_manager_with_module()
        mgr.start_module("user-1", "mod-1")
        mgr.advance_step("user-1", "mod-1", "s1", StepStatus.COMPLETED)
        step = mgr.get_current_step("user-1", "mod-1")
        assert step is not None
        assert step.step_id == "s2"

    def test_get_current_step_no_progress(self) -> None:
        mgr, _ = self._make_manager_with_module()
        assert mgr.get_current_step("user-1", "mod-1") is None

    def test_reset_progress(self) -> None:
        mgr, _ = self._make_manager_with_module()
        mgr.start_module("user-1", "mod-1")
        assert mgr.reset_progress("user-1", "mod-1") is True
        assert mgr.get_progress("user-1", "mod-1") is None

    def test_reset_progress_nonexistent(self) -> None:
        mgr, _ = self._make_manager_with_module()
        assert mgr.reset_progress("user-1", "mod-1") is False


class TestTrainingManagerGuidance:
    def test_guidance_no_progress(self) -> None:
        mgr = TrainingManager(":memory:")
        guidance = mgr.generate_guidance("user-1")
        assert "Training Guidance" in guidance
        assert "Recommended Next" in guidance

    def test_guidance_in_progress(self) -> None:
        mgr = TrainingManager(":memory:")
        mgr.start_module("user-1", "convergent-basics")
        mgr.advance_step("user-1", "convergent-basics", "basics-1", StepStatus.COMPLETED)
        guidance = mgr.generate_guidance("user-1")
        assert "Continue Learning" in guidance
        assert "Convergent Basics" in guidance

    def test_guidance_completed(self) -> None:
        mgr = TrainingManager(":memory:")
        module = mgr.get_module("convergent-basics")
        assert module is not None
        mgr.start_module("user-1", "convergent-basics")
        for step in module.steps:
            mgr.advance_step("user-1", "convergent-basics", step.step_id, StepStatus.COMPLETED)
        guidance = mgr.generate_guidance("user-1")
        assert "Completed" in guidance

    def test_guidance_recommends_next_after_prerequisite(self) -> None:
        mgr = TrainingManager(":memory:")
        # Complete the basics
        module = mgr.get_module("convergent-basics")
        assert module is not None
        mgr.start_module("user-1", "convergent-basics")
        for step in module.steps:
            mgr.advance_step("user-1", "convergent-basics", step.step_id, StepStatus.COMPLETED)
        guidance = mgr.generate_guidance("user-1")
        # Should recommend coordination-protocol since basics is done
        assert "Coordination Protocol" in guidance


class TestTrainingManagerPersistence:
    def test_file_persistence(self, tmp_path: object) -> None:
        import pathlib

        db_path = str(pathlib.Path(str(tmp_path)) / "training.db")
        mgr1 = TrainingManager(db_path)
        mgr1.start_module("user-1", "convergent-basics")
        mgr1.advance_step("user-1", "convergent-basics", "basics-1", StepStatus.COMPLETED)
        mgr1.close()

        mgr2 = TrainingManager(db_path)
        progress = mgr2.get_progress("user-1", "convergent-basics")
        assert progress is not None
        assert progress.step_statuses["basics-1"] == StepStatus.COMPLETED.value
        mgr2.close()


class TestTrainingManagerClose:
    def test_close_prevents_operations(self) -> None:
        mgr = TrainingManager(":memory:", auto_register_builtins=False)
        mgr.close()
        with pytest.raises(Exception):  # noqa: B017
            mgr.list_modules()


class TestPublicAPI:
    def test_import_from_convergent(self) -> None:
        import convergent

        assert hasattr(convergent, "TrainingManager")
        assert hasattr(convergent, "TrainingModule")
        assert hasattr(convergent, "TrainingStep")
        assert hasattr(convergent, "TrainingProgress")
        assert hasattr(convergent, "TrainingLevel")
        assert hasattr(convergent, "StepType")
        assert hasattr(convergent, "StepStatus")

    def test_all_exports_listed(self) -> None:
        import convergent

        assert "TrainingManager" in convergent.__all__
        assert "TrainingModule" in convergent.__all__
        assert "TrainingStep" in convergent.__all__
        assert "TrainingProgress" in convergent.__all__
        assert "TrainingLevel" in convergent.__all__
        assert "StepType" in convergent.__all__
        assert "StepStatus" in convergent.__all__

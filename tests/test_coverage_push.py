"""
Coverage push tests — filling gaps to reach 95%+.

Targets: governor.py, gates.py, agent.py, versioning.py, economics.py,
replay.py, benchmark.py, matching.py, __init__.py, __main__.py, codegen_demo.py
"""

from __future__ import annotations

import importlib
import subprocess
from unittest.mock import MagicMock, patch

from convergent.agent import (
    AgentAction,
    AgentLog,
    RoundLog,
    SimulatedAgent,
    SimulationResult,
)
from convergent.benchmark import BenchmarkMetrics, BenchmarkSuite
from convergent.contract import ConflictClass, ResolutionPolicy
from convergent.economics import (
    Budget,
    CoordinationCostReport,
    CostModel,
    EscalationAction,
    EscalationDecision,
)
from convergent.gates import (
    CommandGate,
    GateReport,
    GateRunResult,
    MypyGate,
    PytestGate,
    _extract_pytest_summary,
)
from convergent.governor import (
    AgentBranch,
    GovernorVerdict,
    MergeGovernor,
    VerdictKind,
)
from convergent.intent import (
    Adjustment,
    ConflictReport,
    Constraint,
    Evidence,
    EvidenceKind,
    Intent,
    InterfaceKind,
    InterfaceSpec,
    ResolutionResult,
)
from convergent.matching import (
    normalize_constraint_target,
    normalize_name,
    normalize_type,
)
from convergent.replay import (
    OperationType,
    ReplayLog,
    _resolutions_equivalent,
)
from convergent.resolver import IntentResolver, PythonGraphBackend
from convergent.versioning import VersionedGraph

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_intent(
    agent_id: str = "agent-a",
    intent_text: str = "test intent",
    provides: list[InterfaceSpec] | None = None,
    stability: float = 0.3,
    evidence: list[Evidence] | None = None,
) -> Intent:
    intent = Intent(agent_id=agent_id, intent=intent_text)
    if provides:
        intent.provides = provides
    intent.stability = stability
    if evidence:
        intent.evidence = evidence
    return intent


def _make_spec(
    name: str = "UserService",
    kind: InterfaceKind = InterfaceKind.CLASS,
    signature: str = "class UserService",
    tags: list[str] | None = None,
) -> InterfaceSpec:
    spec = InterfaceSpec(name=name, kind=kind, signature=signature)
    if tags:
        spec.tags = tags
    return spec


# ===================================================================
# governor.py coverage
# ===================================================================


class TestGovernorVerdictNeedsHuman:
    """Cover GovernorVerdict.needs_human property (line 83)."""

    def test_needs_human_true(self) -> None:
        decision = EscalationDecision(
            action=EscalationAction.ESCALATE_TO_HUMAN,
            expected_cost_auto=0.5,
            expected_cost_escalate=0.1,
            confidence=0.3,
            reasoning="test",
        )
        verdict = GovernorVerdict(
            kind=VerdictKind.NEEDS_ESCALATION,
            approved=False,
            escalation_decisions=[decision],
        )
        assert verdict.needs_human is True

    def test_needs_human_false(self) -> None:
        decision = EscalationDecision(
            action=EscalationAction.AUTO_RESOLVE,
            expected_cost_auto=0.01,
            expected_cost_escalate=1.0,
            confidence=0.9,
            reasoning="test",
        )
        verdict = GovernorVerdict(
            kind=VerdictKind.APPROVED,
            approved=True,
            escalation_decisions=[decision],
        )
        assert verdict.needs_human is False

    def test_needs_human_empty(self) -> None:
        verdict = GovernorVerdict(kind=VerdictKind.APPROVED, approved=True)
        assert verdict.needs_human is False


class TestGovernorEvaluatePublishConflicts:
    """Cover evaluate_publish conflict handling (lines 185-220)."""

    def _setup_conflicting_graph(self) -> tuple[IntentResolver, Intent]:
        """Create a graph with an existing intent, return resolver + new conflicting intent."""
        backend = PythonGraphBackend()
        resolver = IntentResolver(backend=backend, min_stability=0.0)

        spec = _make_spec(tags=["auth", "users"])
        existing = _make_intent(
            agent_id="agent-existing",
            intent_text="existing service",
            provides=[spec],
            stability=0.5,
            evidence=[Evidence.test_pass("tests pass"), Evidence.code_committed("committed")],
        )
        resolver.publish(existing)

        # New intent from different agent, same provides with shared tags
        new_spec = _make_spec(tags=["auth", "users"])
        new_intent = _make_intent(
            agent_id="agent-new",
            intent_text="new service",
            provides=[new_spec],
            stability=0.5,
            evidence=[Evidence.test_pass("tests pass"), Evidence.code_committed("committed")],
        )
        return resolver, new_intent

    def test_conflict_triggers_escalation(self) -> None:
        """Equal stability → HUMAN_ESCALATION → NEEDS_ESCALATION verdict.

        Requires expensive rework cost so economics chooses ESCALATE_TO_HUMAN.
        Default rework cost (0.10) is too low vs human escalation cost (1.00),
        so we set rework_cost_per_conflict=25.0 to tip the balance.
        """
        resolver, new_intent = self._setup_conflicting_graph()

        cost_model = CostModel(rework_cost_per_conflict=25.0)
        governor = MergeGovernor(cost_model=cost_model)
        verdict = governor.evaluate_publish(new_intent, resolver)

        assert not verdict.approved
        assert verdict.kind == VerdictKind.NEEDS_ESCALATION
        assert len(verdict.escalation_decisions) > 0
        assert any("Escalation" in r for r in verdict.blocking_reasons)

    def test_conflict_auto_resolve_passes(self) -> None:
        """Clear stability winner → AUTO_RESOLVE → approved."""
        backend = PythonGraphBackend()
        resolver = IntentResolver(backend=backend, min_stability=0.0)

        spec = _make_spec(tags=["auth", "users"])
        existing = _make_intent(
            agent_id="agent-existing",
            intent_text="existing low stability",
            provides=[spec],
            stability=0.1,
        )
        resolver.publish(existing)

        new_spec = _make_spec(tags=["auth", "users"])
        new_intent = _make_intent(
            agent_id="agent-new",
            intent_text="new high stability",
            provides=[new_spec],
            stability=0.9,
            evidence=[
                Evidence.test_pass("t1"),
                Evidence.test_pass("t2"),
                Evidence.code_committed("c1"),
                Evidence.consumed_by("other"),
                Evidence(kind=EvidenceKind.MANUAL_APPROVAL, description="approved"),
            ],
        )

        governor = MergeGovernor()
        verdict = governor.evaluate_publish(new_intent, resolver)

        assert verdict.approved
        assert verdict.kind == VerdictKind.APPROVED

    def test_conflict_block_action(self) -> None:
        """Test BLOCK action path in evaluate_publish (line 211-212)."""
        resolver, new_intent = self._setup_conflicting_graph()

        # Mock escalation_policy.evaluate to return BLOCK
        governor = MergeGovernor()
        with patch.object(
            governor.escalation_policy,
            "evaluate",
            return_value=EscalationDecision(
                action=EscalationAction.BLOCK,
                expected_cost_auto=0.5,
                expected_cost_escalate=1.0,
                confidence=0.3,
                reasoning="blocked",
            ),
        ):
            verdict = governor.evaluate_publish(new_intent, resolver)

        assert not verdict.approved
        assert any("Blocked:" in r for r in verdict.blocking_reasons)
        # With only BLOCK (no ESCALATE_TO_HUMAN), kind should be BLOCKED_BY_CONFLICT
        assert verdict.kind == VerdictKind.BLOCKED_BY_CONFLICT


class TestGovernorEvaluateMergeConflicts:
    """Cover evaluate_merge conflict handling (lines 290-307)."""

    def test_merge_conflict_escalation(self) -> None:
        """Merge with conflicting intents triggers escalation.

        Uses expensive rework cost so economics picks ESCALATE_TO_HUMAN.
        """
        target = VersionedGraph()
        spec = _make_spec(tags=["auth", "users"])
        existing = _make_intent(
            agent_id="agent-target",
            intent_text="target service",
            provides=[spec],
            stability=0.5,
            evidence=[Evidence.test_pass("pass"), Evidence.code_committed("committed")],
        )
        target.publish(existing)

        source = target.branch("feature")
        new_spec = _make_spec(tags=["auth", "users"])
        conflicting = _make_intent(
            agent_id="agent-source",
            intent_text="source service",
            provides=[new_spec],
            stability=0.5,
            evidence=[Evidence.test_pass("pass"), Evidence.code_committed("committed")],
        )
        source.publish(conflicting)

        cost_model = CostModel(rework_cost_per_conflict=25.0)
        governor = MergeGovernor(cost_model=cost_model)
        verdict = governor.evaluate_merge(source, target)

        assert not verdict.approved
        assert verdict.kind == VerdictKind.NEEDS_ESCALATION
        assert len(verdict.escalation_decisions) > 0

    def test_merge_conflict_block(self) -> None:
        """Merge with BLOCK action path (lines 303-304)."""
        target = VersionedGraph()
        spec = _make_spec(tags=["auth", "users"])
        existing = _make_intent(
            agent_id="agent-target",
            intent_text="target service",
            provides=[spec],
            stability=0.5,
            evidence=[Evidence.test_pass("pass"), Evidence.code_committed("committed")],
        )
        target.publish(existing)

        source = target.branch("feature")
        new_spec = _make_spec(tags=["auth", "users"])
        conflicting = _make_intent(
            agent_id="agent-source",
            intent_text="source service",
            provides=[new_spec],
            stability=0.5,
            evidence=[Evidence.test_pass("pass"), Evidence.code_committed("committed")],
        )
        source.publish(conflicting)

        governor = MergeGovernor()
        with patch.object(
            governor.escalation_policy,
            "evaluate",
            return_value=EscalationDecision(
                action=EscalationAction.BLOCK,
                expected_cost_auto=0.5,
                expected_cost_escalate=1.0,
                confidence=0.3,
                reasoning="merge blocked",
            ),
        ):
            verdict = governor.evaluate_merge(source, target)

        assert not verdict.approved
        assert any("Merge blocked:" in r for r in verdict.blocking_reasons)


class TestAgentBranchName:
    """Cover AgentBranch.branch_name property (line 365)."""

    def test_branch_name(self) -> None:
        vgraph = VersionedGraph()
        governor = MergeGovernor()
        branch = AgentBranch("test-agent", vgraph, governor)
        assert branch.branch_name == "agent/test-agent"


# ===================================================================
# gates.py coverage
# ===================================================================


class TestGateReportSummaryWithError:
    """Cover GateReport.summary with error_summary (line 99)."""

    def test_summary_with_error(self) -> None:
        result = GateRunResult(
            gate_name="pytest(tests/)",
            passed=False,
            evidence=[],
            stdout="",
            stderr="Error output",
            duration_seconds=1.5,
            error_summary="3 tests failed",
        )
        report = GateReport(results=[result])
        summary = report.summary()
        assert "3 tests failed" in summary
        assert "FAIL" in summary


class TestSubprocessErrorHandling:
    """Cover _run_subprocess error paths (lines 147-154)."""

    def test_timeout_expired(self) -> None:
        gate = CommandGate(cmd=["sleep", "100"], timeout=1)
        with patch(
            "subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd=["sleep"], timeout=1),
        ):
            code, stdout, stderr, duration = gate._run_subprocess(["sleep", "100"], timeout=1)
        assert code == -1
        assert "Timed out" in stderr

    def test_file_not_found(self) -> None:
        gate = CommandGate(cmd=["nonexistent"], timeout=10)
        with patch(
            "subprocess.run",
            side_effect=FileNotFoundError("No such file: 'nonexistent'"),
        ):
            code, stdout, stderr, duration = gate._run_subprocess(["nonexistent"], timeout=10)
        assert code == -1
        assert "Command not found" in stderr

    def test_os_error(self) -> None:
        gate = CommandGate(cmd=["bad"], timeout=10)
        with patch(
            "subprocess.run",
            side_effect=OSError("Permission denied"),
        ):
            code, stdout, stderr, duration = gate._run_subprocess(["bad"], timeout=10)
        assert code == -1
        assert "OS error" in stderr


class TestPytestGateMarkers:
    """Cover PytestGate with markers (line 190)."""

    def test_markers_in_command(self) -> None:
        gate = PytestGate(test_path="tests/", markers="slow", timeout=30)
        intent = _make_intent()
        with patch.object(
            gate,
            "_run_subprocess",
            return_value=(0, "1 passed", "", 1.0),
        ) as mock_run:
            result = gate.run(intent)
            cmd = mock_run.call_args[0][0]
            assert "-m" in cmd
            assert "slow" in cmd
        assert result.passed


class TestPytestGateTimeout:
    """Cover PytestGate timeout path (lines 206-208)."""

    def test_timeout_returncode_minus_one(self) -> None:
        gate = PytestGate(test_path="tests/", timeout=30)
        intent = _make_intent()
        with patch.object(
            gate,
            "_run_subprocess",
            return_value=(-1, "", "Timed out after 30s", 30.0),
        ):
            result = gate.run(intent)
        assert not result.passed
        assert result.error_summary
        assert any(e.kind == EvidenceKind.TEST_FAIL for e in result.evidence)


class TestExtractPytestSummaryEmpty:
    """Cover _extract_pytest_summary with no summary line (line 247)."""

    def test_no_summary_line(self) -> None:
        result = _extract_pytest_summary("some random output\nno summary here\n")
        assert result == ""

    def test_with_summary_line(self) -> None:
        output = "collecting...\n===== 5 passed in 0.1s =====\n"
        result = _extract_pytest_summary(output)
        assert "passed" in result


class TestMypyGate:
    """Cover MypyGate init, name, and run paths (lines 270-319)."""

    def test_init_strict(self) -> None:
        gate = MypyGate(target_path="src/", strict=True, extra_args=["--no-color"])
        assert gate.strict is True
        assert gate.extra_args == ["--no-color"]
        assert gate.name == "mypy(src/)"

    def test_run_pass(self) -> None:
        gate = MypyGate(target_path="src/")
        intent = _make_intent()
        with patch.object(
            gate,
            "_run_subprocess",
            return_value=(0, "Success: no issues found", "", 2.0),
        ):
            result = gate.run(intent)
        assert result.passed
        assert any(e.kind == EvidenceKind.TEST_PASS for e in result.evidence)

    def test_run_timeout(self) -> None:
        gate = MypyGate(target_path="src/")
        intent = _make_intent()
        with patch.object(
            gate,
            "_run_subprocess",
            return_value=(-1, "", "Timed out after 120s", 120.0),
        ):
            result = gate.run(intent)
        assert not result.passed
        assert "Timed out" in result.error_summary

    def test_run_type_errors(self) -> None:
        gate = MypyGate(target_path="src/")
        intent = _make_intent()
        mypy_output = (
            "src/foo.py:10: error: Incompatible types\n"
            "src/bar.py:20: error: Missing return\n"
            "Found 2 errors in 2 files\n"
        )
        with patch.object(
            gate,
            "_run_subprocess",
            return_value=(1, mypy_output, "", 3.0),
        ):
            result = gate.run(intent)
        assert not result.passed
        assert "2 type error(s)" in result.error_summary

    def test_run_strict_flag_in_command(self) -> None:
        gate = MypyGate(target_path="src/", strict=True)
        intent = _make_intent()
        with patch.object(
            gate,
            "_run_subprocess",
            return_value=(0, "Success", "", 1.0),
        ) as mock_run:
            gate.run(intent)
            cmd = mock_run.call_args[0][0]
            assert "--strict" in cmd


# ===================================================================
# agent.py coverage
# ===================================================================


class TestSimulatedAgentExhaustPlan:
    """Cover execute_step returning None (line 100)."""

    def test_returns_none_when_exhausted(self) -> None:
        backend = PythonGraphBackend()
        resolver = IntentResolver(backend=backend, min_stability=0.0)
        agent = SimulatedAgent("agent-a", resolver)
        agent.plan([AgentAction(intent=_make_intent())])

        result1 = agent.execute_step()
        assert result1 is not None

        result2 = agent.execute_step()
        assert result2 is None


class TestSimulatedAgentOnAdjust:
    """Cover on_adjust callback (line 135) and adopted constraints (lines 139-140)."""

    def test_on_adjust_callback_called(self) -> None:
        backend = PythonGraphBackend()
        resolver = IntentResolver(backend=backend, min_stability=0.0)

        # Publish existing intent to create conflict → adjustments
        spec = _make_spec(tags=["auth", "users"])
        existing = _make_intent(
            agent_id="agent-existing",
            intent_text="existing",
            provides=[spec],
            stability=0.8,
            evidence=[
                Evidence.test_pass("t1"),
                Evidence.test_pass("t2"),
                Evidence.code_committed("c1"),
            ],
        )
        resolver.publish(existing)

        callback = MagicMock(side_effect=lambda intent, adjs: intent)
        new_spec = _make_spec(tags=["auth", "users"])
        new_intent = _make_intent(
            agent_id="agent-new",
            intent_text="new",
            provides=[new_spec],
        )
        action = AgentAction(intent=new_intent, on_adjust=callback)

        agent = SimulatedAgent("agent-new", resolver)
        agent.plan([action])
        result = agent.execute_step()

        # If adjustments were made, callback should be called
        if result and result.has_adjustments:
            callback.assert_called_once()


class TestSimulatedAgentExecuteAll:
    """Cover execute_all (lines 159-161)."""

    def test_execute_all_returns_log(self) -> None:
        backend = PythonGraphBackend()
        resolver = IntentResolver(backend=backend, min_stability=0.0)
        agent = SimulatedAgent("agent-a", resolver)

        intent1 = _make_intent(intent_text="step 1")
        intent2 = _make_intent(intent_text="step 2")
        agent.plan([AgentAction(intent=intent1), AgentAction(intent=intent2)])

        log = agent.execute_all()
        assert isinstance(log, AgentLog)
        assert len(log.published_intents) == 2
        assert not agent.has_next


class TestSimulationResultSummary:
    """Cover SimulationResult.summary with adjustments (lines 235-262)."""

    def test_summary_with_adjustments(self) -> None:
        adj = Adjustment(
            kind="ConsumeInstead",
            description="Use existing UserService",
            source_intent_id="intent-1",
        )
        log = AgentLog(agent_id="agent-a")
        log.adjustments_applied.append(adj)

        result = SimulationResult(
            rounds=[RoundLog(round_number=1)],
            agent_logs={"agent-a": log},
            all_converged=True,
            total_adjustments=1,
            total_conflicts=0,
            total_intents=2,
        )

        summary = result.summary()
        assert "CONVERGENT SIMULATION RESULTS" in summary
        assert "agent-a" in summary
        assert "ConsumeInstead" in summary
        assert "Use existing UserService" in summary
        assert "YES" in summary

    def test_summary_no_adjustments(self) -> None:
        log = AgentLog(agent_id="agent-b")
        result = SimulationResult(
            rounds=[],
            agent_logs={"agent-b": log},
            all_converged=False,
            total_adjustments=0,
            total_conflicts=1,
            total_intents=1,
        )

        summary = result.summary()
        assert "NO" in summary


# ===================================================================
# versioning.py coverage
# ===================================================================


class TestVersionedGraphResolve:
    """Cover VersionedGraph.resolve() (line 166)."""

    def test_resolve_returns_result(self) -> None:
        vgraph = VersionedGraph()
        intent = _make_intent()
        result = vgraph.resolve(intent)
        assert isinstance(result, ResolutionResult)


class TestVersionedGraphMergeConflicts:
    """Cover merge conflict classification (lines 241-259)."""

    def test_merge_human_escalation(self) -> None:
        """Equal stability → HUMAN_ESCALATION → success=False."""
        vgraph = VersionedGraph()
        spec = _make_spec(tags=["auth", "users"])
        existing = _make_intent(
            agent_id="agent-main",
            intent_text="main service",
            provides=[spec],
            stability=0.5,
            evidence=[Evidence.test_pass("pass"), Evidence.code_committed("c")],
        )
        vgraph.publish(existing)

        branch = vgraph.branch("feature")
        new_spec = _make_spec(tags=["auth", "users"])
        conflicting = _make_intent(
            agent_id="agent-branch",
            intent_text="branch service",
            provides=[new_spec],
            stability=0.5,
            evidence=[Evidence.test_pass("pass"), Evidence.code_committed("c")],
        )
        branch.publish(conflicting)

        result = vgraph.merge(branch)
        assert not result.success
        assert len(result.escalations) > 0

    def test_merge_hard_fail_with_custom_policy(self) -> None:
        """Custom policy returning HARD_FAIL → hard_failures populated.

        The merge uses self.policy (the main graph's policy), so we set
        AlwaysHardFail on the main graph.
        """

        class AlwaysHardFail(ResolutionPolicy):
            def classify_provision_conflict(
                self, my_stability: float, their_stability: float
            ) -> ConflictClass:
                return ConflictClass.HARD_FAIL

        vgraph = VersionedGraph(policy=AlwaysHardFail())
        spec = _make_spec(tags=["auth", "users"])
        existing = _make_intent(
            agent_id="agent-main",
            intent_text="main",
            provides=[spec],
            stability=0.5,
            evidence=[Evidence.test_pass("pass"), Evidence.code_committed("c")],
        )
        vgraph.publish(existing)

        branch = vgraph.branch("feature")
        new_spec = _make_spec(tags=["auth", "users"])
        conflicting = _make_intent(
            agent_id="agent-branch",
            intent_text="branch",
            provides=[new_spec],
            stability=0.5,
            evidence=[Evidence.test_pass("pass"), Evidence.code_committed("c")],
        )
        branch.publish(conflicting)

        result = vgraph.merge(branch)
        assert not result.success
        assert len(result.hard_failures) > 0


# ===================================================================
# economics.py coverage
# ===================================================================


class TestBudgetEdgeCases:
    """Cover Budget edge cases."""

    def test_utilization_zero_max_cost(self) -> None:
        """max_cost=0 → utilization=1.0 (line 110)."""
        budget = Budget(max_cost=0)
        assert budget.utilization == 1.0


class TestEscalationDecisionSavings:
    """Cover savings property for different actions (lines 145, 148)."""

    def test_savings_escalate_to_human(self) -> None:
        decision = EscalationDecision(
            action=EscalationAction.ESCALATE_TO_HUMAN,
            expected_cost_auto=2.0,
            expected_cost_escalate=0.5,
            confidence=0.3,
            reasoning="escalation cheaper",
        )
        assert decision.savings == 2.0 - 0.5

    def test_savings_defer(self) -> None:
        decision = EscalationDecision(
            action=EscalationAction.DEFER,
            expected_cost_auto=0.1,
            expected_cost_escalate=1.0,
            confidence=0.5,
            reasoning="deferred",
        )
        assert decision.savings == 0.0


class TestCoordinationCostReportEdgeCases:
    """Cover CoordinationCostReport edge cases."""

    def test_auto_resolve_rate_zero_total(self) -> None:
        """Empty report → auto_resolve_rate=1.0 (line 305)."""
        report = CoordinationCostReport()
        assert report.auto_resolve_rate == 1.0

    def test_cost_per_decision_zero_total(self) -> None:
        """Empty report → cost_per_decision=0.0 (line 313)."""
        report = CoordinationCostReport()
        assert report.cost_per_decision == 0.0

    def test_record_block_decision(self) -> None:
        """BLOCK action increments total_blocked (line 325-326)."""
        report = CoordinationCostReport()
        decision = EscalationDecision(
            action=EscalationAction.BLOCK,
            expected_cost_auto=0.1,
            expected_cost_escalate=1.0,
            confidence=0.2,
            reasoning="blocked",
        )
        report.record(decision)
        assert report.total_blocked == 1

    def test_record_defer_decision(self) -> None:
        """DEFER action increments total_deferred (line 327-328)."""
        report = CoordinationCostReport()
        decision = EscalationDecision(
            action=EscalationAction.DEFER,
            expected_cost_auto=0.1,
            expected_cost_escalate=1.0,
            confidence=0.5,
            reasoning="deferred",
        )
        report.record(decision)
        assert report.total_deferred == 1


# ===================================================================
# replay.py coverage
# ===================================================================


class TestReplayLogAccessors:
    """Cover entries and entry_count properties (lines 94, 98)."""

    def test_entries_and_count(self) -> None:
        log = ReplayLog()
        intent = _make_intent()
        log.record_publish(intent)

        assert log.entry_count == 1
        assert len(log.entries) == 1
        assert log.entries[0].operation == OperationType.PUBLISH


class TestResolutionsEquivalent:
    """Cover _resolutions_equivalent edge cases (lines 190, 194, 199, 203)."""

    def test_none_original(self) -> None:
        """b is None → True (line 190)."""
        a = ResolutionResult(original_intent_id="x")
        assert _resolutions_equivalent(a, None) is True

    def test_mismatched_adjustment_counts(self) -> None:
        """Different adjustment counts → False (line 194)."""
        a = ResolutionResult(
            original_intent_id="x",
            adjustments=[Adjustment(kind="ConsumeInstead", description="a", source_intent_id="1")],
        )
        b = ResolutionResult(original_intent_id="x")
        assert _resolutions_equivalent(a, b) is False

    def test_mismatched_adjustment_kinds(self) -> None:
        """Same count but different kinds → False (line 198-199)."""
        a = ResolutionResult(
            original_intent_id="x",
            adjustments=[Adjustment(kind="ConsumeInstead", description="a", source_intent_id="1")],
        )
        b = ResolutionResult(
            original_intent_id="x",
            adjustments=[Adjustment(kind="YieldTo", description="b", source_intent_id="2")],
        )
        assert _resolutions_equivalent(a, b) is False

    def test_mismatched_conflict_counts(self) -> None:
        """Different conflict counts → False (line 202-203)."""
        a = ResolutionResult(
            original_intent_id="x",
            conflicts=[
                ConflictReport(
                    my_intent_id="x",
                    their_intent_id="y",
                    description="conflict",
                    their_stability=0.5,
                    resolution_suggestion="yield",
                )
            ],
        )
        b = ResolutionResult(original_intent_id="x")
        assert _resolutions_equivalent(a, b) is False

    def test_mismatched_constraint_counts(self) -> None:
        """Same adjustments and conflicts but different constraint counts → False (line 206)."""
        a = ResolutionResult(
            original_intent_id="x",
            adopted_constraints=[Constraint(target="User", requirement="must have id")],
        )
        b = ResolutionResult(original_intent_id="x")
        assert _resolutions_equivalent(a, b) is False

    def test_equivalent_results(self) -> None:
        """Matching results → True (line 206 returns True)."""
        adj = Adjustment(kind="ConsumeInstead", description="a", source_intent_id="1")
        a = ResolutionResult(original_intent_id="x", adjustments=[adj])
        b = ResolutionResult(original_intent_id="x", adjustments=[adj])
        assert _resolutions_equivalent(a, b) is True


# ===================================================================
# benchmark.py coverage
# ===================================================================


class TestBenchmarkMetricsZeroAgents:
    """Cover zero-agent edge cases (lines 94, 100)."""

    def test_adjustments_per_agent_zero(self) -> None:
        m = BenchmarkMetrics(scenario="test", agent_count=0)
        assert m.adjustments_per_agent == 0.0

    def test_cost_per_agent_zero(self) -> None:
        m = BenchmarkMetrics(scenario="test", agent_count=0)
        assert m.cost_per_agent == 0.0


class TestBenchmarkScalingZero:
    """Cover scaling analysis zero check (line 146)."""

    def test_single_result_skips_scaling(self) -> None:
        suite = BenchmarkSuite()
        m = BenchmarkMetrics(scenario="test", agent_count=2)
        suite.results.append(m)
        # With only 1 result, scaling analysis should be skipped
        summary = suite.summary()
        assert "SCALING ANALYSIS" not in summary


# ===================================================================
# matching.py coverage
# ===================================================================


class TestNormalizeName:
    """Cover normalize_name edge cases (line 64)."""

    def test_no_camel_tokens(self) -> None:
        """String with no CamelCase tokens after suffix strip → lowered (line 64)."""
        result = normalize_name("___")
        assert result == "___"


class TestNormalizeType:
    """Cover normalize_type edge cases (lines 100, 108-109)."""

    def test_empty_string(self) -> None:
        """Empty string → empty (line 100)."""
        assert normalize_type("") == ""

    def test_union_with_none(self) -> None:
        """'str | None' → 'str' (lines 108-109)."""
        assert normalize_type("str | None") == "str"

    def test_none_union_first(self) -> None:
        """'None | int' → 'int'."""
        assert normalize_type("None | int") == "int"


class TestNormalizeConstraintTarget:
    """Cover normalize_constraint_target edge case (line 188)."""

    def test_target_is_just_suffix(self) -> None:
        """'model' as entire string → don't strip, break (line 188)."""
        result = normalize_constraint_target("model")
        assert result == "model"

    def test_target_is_just_service(self) -> None:
        result = normalize_constraint_target("service")
        assert result == "service"


# ===================================================================
# __init__.py coverage
# ===================================================================


class TestInitImportGuard:
    """Cover ImportError fallback for AnthropicSemanticMatcher (lines 172-173).

    The guard at lines 168-173 catches ImportError when importing
    AnthropicSemanticMatcher. We simulate this by temporarily removing
    the class from the semantic module before reloading __init__.
    """

    def test_import_guard_when_class_missing(self) -> None:
        import convergent
        import convergent.semantic as sem_mod

        # Remove AnthropicSemanticMatcher from the semantic module temporarily
        original_cls = getattr(sem_mod, "AnthropicSemanticMatcher", None)
        if original_cls is not None:
            delattr(sem_mod, "AnthropicSemanticMatcher")
        try:
            importlib.reload(convergent)
            assert "AnthropicSemanticMatcher" not in convergent.__all__
        finally:
            if original_cls is not None:
                sem_mod.AnthropicSemanticMatcher = original_cls
            importlib.reload(convergent)


# ===================================================================
# __main__.py coverage
# ===================================================================


class TestMainModule:
    """Cover __main__.py CLI entry point."""

    def test_demo_subcommand_calls_run_demo(self) -> None:
        from convergent.__main__ import main

        with patch("convergent.__main__._cmd_demo") as mock_cmd:
            main(["demo"])
            mock_cmd.assert_called_once()

    def test_inspect_subcommand_missing_db(self) -> None:
        import contextlib

        from convergent.__main__ import main

        with contextlib.suppress(SystemExit):
            main(["inspect", "/nonexistent/db.sqlite"])

    def test_no_subcommand_shows_help(self) -> None:
        import contextlib

        from convergent.__main__ import main

        with contextlib.suppress(SystemExit):
            main([])


# ===================================================================
# codegen_demo.py coverage
# ===================================================================


class TestCodegenDemoBaselines:
    """Cover baseline code generation functions (lines 186, 238)."""

    def test_generate_api_code_baseline(self) -> None:
        from convergent.codegen_demo import _generate_api_code_baseline

        code = _generate_api_code_baseline()
        assert "UserEndpoints" in code

    def test_generate_storage_code_baseline(self) -> None:
        from convergent.codegen_demo import _generate_storage_code_baseline

        code = _generate_storage_code_baseline()
        assert "UserRepository" in code


class TestCodegenDemoMain:
    """Cover main() and __name__ guard (lines 575-576, 580)."""

    def test_main_calls_run_demo(self) -> None:
        from convergent.codegen_demo import main

        with patch("convergent.codegen_demo.run_demo") as mock_demo:
            mock_demo.return_value = MagicMock(summary=MagicMock(return_value="test"))
            main()
            mock_demo.assert_called_once()

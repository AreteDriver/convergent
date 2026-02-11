#!/usr/bin/env python3
"""Live LLM smoke test for AnthropicSemanticMatcher.

Requires:
    pip install -e ".[llm]"
    export ANTHROPIC_API_KEY=sk-ant-...

NOT a pytest suite — this hits a real API and costs real tokens.
Run manually: python scripts/smoke_test_llm.py
"""

from __future__ import annotations

import os
import sys
import time

# ---------------------------------------------------------------------------
# Prerequisite check
# ---------------------------------------------------------------------------


def check_prerequisites() -> bool:
    """Verify API key and anthropic package are available."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("SKIP: ANTHROPIC_API_KEY not set")
        return False
    try:
        import anthropic  # noqa: F401
    except ImportError:
        print("SKIP: anthropic package not installed (pip install -e '.[llm]')")
        return False
    return True


# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------

passed = 0
failed = 0


def section(name: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {name}")
    print("=" * 60)


def check(label: str, condition: bool, detail: str = "") -> None:
    global passed, failed
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {label}")
    if detail:
        print(f"         {detail}")
    if condition:
        passed += 1
    else:
        failed += 1


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_overlap_detection() -> None:
    """AccountManager vs UserHandler (should overlap),
    AccountManager vs DatabaseMigration (should not)."""
    from convergent.semantic import AnthropicSemanticMatcher

    section("1. Overlap Detection")
    matcher = AnthropicSemanticMatcher()

    spec_account = {
        "name": "AccountManager",
        "kind": "class",
        "signature": "id: UUID, email: str",
        "tags": ["user", "account"],
    }
    spec_user = {
        "name": "UserHandler",
        "kind": "class",
        "signature": "id: UUID, email: str",
        "tags": ["user", "handler"],
    }
    spec_migration = {
        "name": "DatabaseMigration",
        "kind": "class",
        "signature": "version: int, sql: str",
        "tags": ["db", "migration"],
    }

    t0 = time.monotonic()
    result_overlap = matcher.check_overlap(spec_account, spec_user)
    dt1 = time.monotonic() - t0

    t0 = time.monotonic()
    result_no_overlap = matcher.check_overlap(spec_account, spec_migration)
    dt2 = time.monotonic() - t0

    check(
        "AccountManager ↔ UserHandler overlaps",
        result_overlap.overlap,
        f"confidence={result_overlap.confidence:.2f}, {dt1:.2f}s",
    )
    check(
        "AccountManager ↔ DatabaseMigration does NOT overlap",
        not result_no_overlap.overlap,
        f"confidence={result_no_overlap.confidence:.2f}, {dt2:.2f}s",
    )


def test_batch_processing() -> None:
    """3 pairs in one call, verify timing."""
    from convergent.semantic import AnthropicSemanticMatcher

    section("2. Batch Processing")
    matcher = AnthropicSemanticMatcher()

    pairs = [
        (
            {"name": "UserService", "kind": "class", "signature": "", "tags": ["user"]},
            {"name": "AccountService", "kind": "class", "signature": "", "tags": ["account"]},
        ),
        (
            {"name": "EmailSender", "kind": "function", "signature": "", "tags": ["email"]},
            {"name": "NotificationMailer", "kind": "function", "signature": "", "tags": ["notify"]},
        ),
        (
            {"name": "PaymentGateway", "kind": "class", "signature": "", "tags": ["payment"]},
            {"name": "LogRotator", "kind": "class", "signature": "", "tags": ["logging"]},
        ),
    ]

    t0 = time.monotonic()
    results = matcher.check_overlap_batch(pairs)
    dt = time.monotonic() - t0

    check("Batch returns 3 results", len(results) == 3, f"{dt:.2f}s for 3 pairs")
    check(
        "UserService ↔ AccountService overlaps",
        results[0].overlap,
        f"confidence={results[0].confidence:.2f}",
    )
    check(
        "PaymentGateway ↔ LogRotator does NOT overlap",
        not results[2].overlap,
        f"confidence={results[2].confidence:.2f}",
    )


def test_constraint_applicability() -> None:
    """API versioning constraint against GraphQL endpoint."""
    from convergent.semantic import AnthropicSemanticMatcher

    section("3. Constraint Applicability")
    matcher = AnthropicSemanticMatcher()

    constraint = {
        "target": "API endpoints",
        "requirement": "must include version prefix /v1/",
        "affects_tags": ["api", "endpoint"],
    }
    intent_rest = {
        "agent_id": "backend",
        "intent": "Build REST API for user management",
        "provides": [{"name": "GET /users", "kind": "endpoint", "tags": ["api", "rest", "user"]}],
    }
    intent_graphql = {
        "agent_id": "backend",
        "intent": "Build GraphQL schema for recipes",
        "provides": [{"name": "RecipeQuery", "kind": "endpoint", "tags": ["graphql", "recipe"]}],
    }

    result_rest = matcher.check_constraint_applies(constraint, intent_rest)
    result_gql = matcher.check_constraint_applies(constraint, intent_graphql)

    check(
        "Version prefix applies to REST API",
        result_rest.applies,
        f"confidence={result_rest.confidence:.2f}: {result_rest.reasoning[:80]}",
    )
    # GraphQL doesn't use URL path versioning — the constraint may or may not apply,
    # but we at least verify we get a response
    check(
        "Constraint check returns for GraphQL",
        result_gql.confidence >= 0.0,
        f"applies={result_gql.applies}, confidence={result_gql.confidence:.2f}",
    )


def test_trajectory_prediction() -> None:
    """Auth agent history -> predicted next provisions."""
    from convergent.semantic import AnthropicSemanticMatcher

    section("4. Trajectory Prediction")
    matcher = AnthropicSemanticMatcher()

    history = [
        {
            "agent_id": "auth-agent",
            "intent": "Build User model with email/password",
            "provides": [{"name": "User", "kind": "model", "tags": ["user", "auth"]}],
        },
        {
            "agent_id": "auth-agent",
            "intent": "Build JWT token service",
            "provides": [{"name": "TokenService", "kind": "class", "tags": ["auth", "jwt"]}],
        },
    ]

    t0 = time.monotonic()
    prediction = matcher.predict_trajectory(history)
    dt = time.monotonic() - t0

    check(
        "Prediction returns agent_id",
        prediction.agent_id == "auth-agent",
        f"agent_id={prediction.agent_id}",
    )
    check(
        "Prediction has provisions",
        len(prediction.predicted_provisions) > 0,
        f"{prediction.predicted_provisions[:3]}, {dt:.2f}s",
    )
    check(
        "Prediction has confidence",
        prediction.confidence > 0.0,
        f"confidence={prediction.confidence:.2f}",
    )


def test_cache_validation() -> None:
    """Second call should be >10x faster than first."""
    from convergent.semantic import AnthropicSemanticMatcher

    section("5. Cache Validation")
    matcher = AnthropicSemanticMatcher()

    spec_a = {"name": "CacheTestA", "kind": "class", "signature": "id: int", "tags": ["test"]}
    spec_b = {"name": "CacheTestB", "kind": "class", "signature": "id: int", "tags": ["test"]}

    # First call — hits API
    t0 = time.monotonic()
    result1 = matcher.check_overlap(spec_a, spec_b)
    dt_first = time.monotonic() - t0

    # Second call — should hit cache
    t0 = time.monotonic()
    result2 = matcher.check_overlap(spec_a, spec_b)
    dt_second = time.monotonic() - t0

    check(
        "Cache hit returns same result",
        result1.overlap == result2.overlap and result1.confidence == result2.confidence,
        f"first={dt_first:.3f}s, cached={dt_second:.6f}s",
    )
    # Cache should be effectively instant (<1ms) vs API call (>100ms)
    speedup = dt_first / dt_second if dt_second > 0 else float("inf")
    check("Cache >10x faster", speedup > 10, f"speedup={speedup:.0f}x")


def test_full_demo() -> None:
    """Run three-agent demo with SemanticMatcher wired in."""
    from convergent.agent import AgentAction, SimulatedAgent, SimulationRunner
    from convergent.intent import (
        Constraint,
        Evidence,
        Intent,
        InterfaceKind,
        InterfaceSpec,
    )
    from convergent.resolver import IntentResolver
    from convergent.semantic import AnthropicSemanticMatcher

    section("6. Full Demo (3 agents + SemanticMatcher)")
    matcher = AnthropicSemanticMatcher()
    resolver = IntentResolver(min_stability=0.2, semantic_matcher=matcher)

    # Agent A: Auth
    agent_a = SimulatedAgent("agent-a", resolver)
    agent_a.plan(
        [
            AgentAction(
                intent=Intent(
                    agent_id="agent-a",
                    intent="Build authentication module",
                    provides=[
                        InterfaceSpec(
                            "User",
                            InterfaceKind.MODEL,
                            "id: UUID, email: str, hashed_password: str",
                            tags=["user", "auth", "model"],
                        ),
                    ],
                    constraints=[
                        Constraint(
                            "User model", "must have email: str", affects_tags=["user", "account"]
                        ),
                    ],
                ),
                post_evidence=[
                    Evidence.code_committed("auth/models.py"),
                    Evidence.test_pass("test_user"),
                ],
            ),
        ]
    )

    # Agent B: Recipes (requires User)
    agent_b = SimulatedAgent("agent-b", resolver)
    agent_b.plan(
        [
            AgentAction(
                intent=Intent(
                    agent_id="agent-b",
                    intent="Build recipe module",
                    provides=[
                        InterfaceSpec(
                            "Recipe",
                            InterfaceKind.MODEL,
                            "id: UUID, title: str, author_id: UUID",
                            tags=["recipe", "model"],
                        ),
                    ],
                    requires=[
                        InterfaceSpec(
                            "User",
                            InterfaceKind.MODEL,
                            "id: UUID, email: str",
                            tags=["user", "auth", "model"],
                        ),
                    ],
                ),
                post_evidence=[Evidence.code_committed("recipes/models.py")],
            ),
        ]
    )

    # Agent C: Meal plan (overlapping User concept)
    agent_c = SimulatedAgent("agent-c", resolver)
    agent_c.plan(
        [
            AgentAction(
                intent=Intent(
                    agent_id="agent-c",
                    intent="Build meal planning module",
                    provides=[
                        InterfaceSpec(
                            "User",
                            InterfaceKind.MODEL,
                            "id: UUID, name: str",
                            tags=["user", "meal", "model"],
                        ),
                        InterfaceSpec(
                            "MealPlan",
                            InterfaceKind.MODEL,
                            "id: UUID, user_id: UUID",
                            tags=["meal", "plan", "model"],
                        ),
                    ],
                ),
                post_evidence=[Evidence.code_committed("meals/models.py")],
            ),
        ]
    )

    runner = SimulationRunner(resolver)
    runner.add_agent(agent_a)
    runner.add_agent(agent_b)
    runner.add_agent(agent_c)

    t0 = time.monotonic()
    result = runner.run()
    dt = time.monotonic() - t0

    check(
        "All agents converged",
        result.all_converged,
        f"{result.total_adjustments} adjustments, {result.total_conflicts} conflicts",
    )
    check(
        "Agent C yielded User to Agent A",
        any(
            a.kind == "ConsumeInstead"
            for log in result.agent_logs.values()
            for a in log.adjustments_applied
        ),
        f"demo completed in {dt:.2f}s",
    )
    check("Graph has intents", resolver.intent_count >= 3, f"intent_count={resolver.intent_count}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    global passed, failed

    print("Convergent LLM Smoke Test")
    print(f"{'=' * 60}")

    if not check_prerequisites():
        return 0  # Skip gracefully, not a failure

    test_overlap_detection()
    test_batch_processing()
    test_constraint_applicability()
    test_trajectory_prediction()
    test_cache_validation()
    test_full_demo()

    print(f"\n{'=' * 60}")
    print(f"  RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

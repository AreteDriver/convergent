"""
Intent Resolver — reads the shared intent graph and adjusts local plans
for compatibility. Not a coordinator — a lens.

Uses the Rust core when available for performance. Falls back to pure
Python implementation for development and testing.
"""

from __future__ import annotations

import logging
from typing import Protocol

from convergent.intent import (
    Adjustment,
    ConflictReport,
    Constraint,
    Intent,
    InterfaceSpec,
    ResolutionResult,
)

logger = logging.getLogger(__name__)


class GraphBackend(Protocol):
    """Protocol for intent graph backends (Rust or Python)."""

    def publish(self, intent: Intent) -> float: ...
    def query_all(self, min_stability: float | None = None) -> list[Intent]: ...
    def query_by_agent(self, agent_id: str) -> list[Intent]: ...
    def find_overlapping(
        self, specs: list[InterfaceSpec], exclude_agent: str, min_stability: float
    ) -> list[Intent]: ...
    def resolve(self, intent: Intent, min_stability: float) -> ResolutionResult: ...
    def count(self) -> int: ...


class PythonGraphBackend:
    """Pure Python intent graph for development and testing.
    Production should use the Rust-backed IntentGraph."""

    def __init__(self) -> None:
        self._intents: list[Intent] = []

    def publish(self, intent: Intent) -> float:
        """Publish intent and return computed stability."""
        stability = intent.compute_stability()
        self._intents.append(intent)
        logger.debug(
            f"Published intent '{intent.intent}' from {intent.agent_id} "
            f"(stability: {stability:.2f})"
        )
        return stability

    def query_all(self, min_stability: float | None = None) -> list[Intent]:
        min_stab = min_stability or 0.0
        return [i for i in self._intents if i.compute_stability() >= min_stab]

    def query_by_agent(self, agent_id: str) -> list[Intent]:
        return [i for i in self._intents if i.agent_id == agent_id]

    def find_overlapping(
        self, specs: list[InterfaceSpec], exclude_agent: str, min_stability: float
    ) -> list[Intent]:
        results = []
        for intent in self._intents:
            if intent.agent_id == exclude_agent:
                continue
            if intent.compute_stability() < min_stability:
                continue

            their_specs = intent.provides + intent.requires
            for my_spec in specs:
                if any(my_spec.structurally_overlaps(ts) for ts in their_specs):
                    results.append(intent)
                    break

        return results

    def count(self) -> int:
        return len(self._intents)


class IntentResolver:
    """Reads the shared intent graph and adjusts local plans for compatibility.

    This is the core intelligence of Convergent. Before each major decision,
    an agent runs its intent through the resolver to check for:

    1. Duplicate provisions (another agent already provides this)
    2. Interface mismatches (signatures don't match)
    3. Applicable constraints (other agents' decisions constrain mine)
    4. Conflicts (irreconcilable differences)
    """

    def __init__(
        self,
        backend: GraphBackend | None = None,
        min_stability: float = 0.3,
    ) -> None:
        self.backend: GraphBackend = backend or PythonGraphBackend()
        self.min_stability = min_stability

    def publish(self, intent: Intent) -> float:
        """Publish an intent to the shared graph. Returns computed stability."""
        return self.backend.publish(intent)

    def resolve(self, intent: Intent) -> ResolutionResult:
        """Resolve an intent against the current graph state.

        Returns adjustments the agent should make for compatibility,
        any conflicts found, and constraints to adopt.
        """
        adjustments: list[Adjustment] = []
        conflicts: list[ConflictReport] = []
        adopted_constraints: list[Constraint] = []

        my_specs = intent.provides + intent.requires
        my_stability = intent.compute_stability()

        # 1. Find overlapping intents from other agents
        overlapping = self.backend.find_overlapping(my_specs, intent.agent_id, self.min_stability)

        for other in overlapping:
            other_stability = other.compute_stability()

            # Check for duplicate provisions
            for my_provision in intent.provides:
                for their_provision in other.provides:
                    if my_provision.structurally_overlaps(their_provision):
                        if other_stability > my_stability:
                            adjustments.append(
                                Adjustment(
                                    kind="ConsumeInstead",
                                    description=(
                                        f"Drop '{my_provision.name}', consume "
                                        f"'{their_provision.name}' from agent "
                                        f"{other.agent_id} (stability {other_stability:.2f})"
                                    ),
                                    source_intent_id=other.id,
                                )
                            )
                        else:
                            conflicts.append(
                                ConflictReport(
                                    my_intent_id=intent.id,
                                    their_intent_id=other.id,
                                    description=(
                                        f"Both provide '{my_provision.name}' — "
                                        f"my stability {my_stability:.2f} vs "
                                        f"their {other_stability:.2f}"
                                    ),
                                    their_stability=other_stability,
                                    resolution_suggestion=(
                                        "Higher stability should provide; other should consume"
                                    ),
                                )
                            )

            # Check for signature mismatches in required→provided pairs
            for my_req in intent.requires:
                for their_prov in other.provides:
                    if (
                        my_req.structurally_overlaps(their_prov)
                        and not my_req.signature_compatible(their_prov)
                        and other_stability > my_stability
                    ):
                        adjustments.append(
                            Adjustment(
                                kind="AdaptSignature",
                                description=(
                                    f"Adapt '{my_req.name}' signature to match "
                                    f"'{their_prov.name}' from agent {other.agent_id} — "
                                    f"expected '{my_req.signature}', "
                                    f"they provide '{their_prov.signature}'"
                                ),
                                source_intent_id=other.id,
                            )
                        )

        # 2. Find applicable constraints from other agents
        all_intents = self.backend.query_all(self.min_stability)
        for other in all_intents:
            if other.agent_id == intent.agent_id:
                continue

            for constraint in other.constraints:
                if constraint.applies_to(intent):
                    # Check for conflicts with our constraints
                    has_conflict = any(mc.conflicts_with(constraint) for mc in intent.constraints)

                    if has_conflict:
                        other_stability = other.compute_stability()
                        conflicts.append(
                            ConflictReport(
                                my_intent_id=intent.id,
                                their_intent_id=other.id,
                                description=(f"Constraint conflict on '{constraint.target}'"),
                                their_stability=other_stability,
                                resolution_suggestion=("Higher stability constraint should win"),
                            )
                        )
                    else:
                        adopted_constraints.append(constraint)
                        adjustments.append(
                            Adjustment(
                                kind="AdoptConstraint",
                                description=(
                                    f"Adopt constraint: {constraint.target} — "
                                    f"{constraint.requirement}"
                                ),
                                source_intent_id=other.id,
                            )
                        )

        result = ResolutionResult(
            original_intent_id=intent.id,
            adjustments=adjustments,
            conflicts=conflicts,
            adopted_constraints=adopted_constraints,
        )

        logger.info(
            f"Resolved intent '{intent.intent}' from {intent.agent_id}: "
            f"{len(adjustments)} adjustments, {len(conflicts)} conflicts"
        )

        return result

    @property
    def intent_count(self) -> int:
        return self.backend.count()

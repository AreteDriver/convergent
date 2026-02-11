"""Convergent — Multi-agent coherence through ambient intent awareness."""

__version__ = "0.3.0"

from convergent.constraints import (
    ConstraintCheckResult,
    ConstraintEngine,
    ConstraintKind,
    GateResult,
    TypedConstraint,
)
from convergent.contract import (
    ConflictClass,
    ContractViolation,
    DEFAULT_CONTRACT,
    DEFAULT_RESOLUTION_POLICY,
    DEFAULT_STABILITY_WEIGHTS,
    EdgeType,
    GraphInvariant,
    IntentGraphContract,
    MutationType,
    ResolutionPolicy,
    StabilityWeights,
    content_hash_intent,
    content_hash_intents,
    validate_publish,
)
from convergent.economics import (
    Budget,
    CoordinationCostReport,
    CostModel,
    EscalationAction,
    EscalationDecision,
    EscalationPolicy,
)
from convergent.governor import (
    AgentBranch,
    GovernorVerdict,
    MergeGovernor,
    ProposalResult,
    VerdictKind,
)
from convergent.intent import (
    Constraint,
    ConstraintSeverity,
    Evidence,
    EvidenceKind,
    Intent,
    InterfaceKind,
    InterfaceSpec,
)
from convergent.matching import (
    names_overlap,
    normalize_constraint_target,
    normalize_name,
    normalize_type,
    parse_signature,
    signatures_compatible,
)
from convergent.replay import ReplayLog, ReplayResult
from convergent.resolver import IntentResolver
from convergent.semantic import (
    ConstraintApplicability,
    SemanticMatch,
    SemanticMatcher,
    TrajectoryPrediction,
)
from convergent.versioning import GraphSnapshot, MergeResult, VersionedGraph

__all__ = [
    # Layer 1: Constraint Engine
    "ConstraintCheckResult",
    "ConstraintEngine",
    "ConstraintKind",
    "GateResult",
    "TypedConstraint",
    # Layer 3: Economics
    "Budget",
    "CoordinationCostReport",
    "CostModel",
    "EscalationAction",
    "EscalationDecision",
    "EscalationPolicy",
    # Governor (integrates all 3 layers)
    "AgentBranch",
    "GovernorVerdict",
    "MergeGovernor",
    "ProposalResult",
    "VerdictKind",
    # Contract
    "ConflictClass",
    "ContractViolation",
    "DEFAULT_CONTRACT",
    "DEFAULT_RESOLUTION_POLICY",
    "DEFAULT_STABILITY_WEIGHTS",
    "EdgeType",
    "GraphInvariant",
    "IntentGraphContract",
    "MutationType",
    "ResolutionPolicy",
    "StabilityWeights",
    "content_hash_intent",
    "content_hash_intents",
    "validate_publish",
    # Core types
    "Constraint",
    "ConstraintApplicability",
    "ConstraintSeverity",
    "Evidence",
    "EvidenceKind",
    "Intent",
    "IntentResolver",
    "InterfaceKind",
    "InterfaceSpec",
    # Replay
    "ReplayLog",
    "ReplayResult",
    # Semantic
    "SemanticMatch",
    "SemanticMatcher",
    "TrajectoryPrediction",
    # Versioning
    "GraphSnapshot",
    "MergeResult",
    "VersionedGraph",
    # Matching utilities
    "names_overlap",
    "normalize_constraint_target",
    "normalize_name",
    "normalize_type",
    "parse_signature",
    "signatures_compatible",
]

# Conditional export: AnthropicSemanticMatcher (only when anthropic installed)
try:
    from convergent.semantic import AnthropicSemanticMatcher  # noqa: F401

    __all__.append("AnthropicSemanticMatcher")
except ImportError:
    pass

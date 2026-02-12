"""Convergent — Multi-agent coherence through ambient intent awareness."""

__version__ = "0.4.0"

from convergent.async_backend import AsyncBackendWrapper, AsyncGraphBackend
from convergent.benchmark import (
    BenchmarkMetrics,
    BenchmarkSuite,
    ScenarioType,
    run_benchmark,
    run_scaling_suite,
)
from convergent.constraints import (
    ConstraintCheckResult,
    ConstraintEngine,
    ConstraintKind,
    GateResult,
    TypedConstraint,
)
from convergent.contract import (
    DEFAULT_CONTRACT,
    DEFAULT_RESOLUTION_POLICY,
    DEFAULT_STABILITY_WEIGHTS,
    ConflictClass,
    ContractViolation,
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
from convergent.gates import (
    CommandGate,
    CompileGate,
    ConstraintGate,
    GateReport,
    GateRunner,
    GateRunResult,
    MypyGate,
    PytestGate,
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
from convergent.resolver import GraphBackend, IntentResolver, PythonGraphBackend
from convergent.rust_backend import HAS_RUST, RustGraphBackend
from convergent.semantic import (
    ConstraintApplicability,
    SemanticMatch,
    SemanticMatcher,
    TrajectoryPrediction,
)
from convergent.sqlite_backend import SQLiteBackend
from convergent.versioning import GraphSnapshot, MergeResult, VersionedGraph
from convergent.visualization import dot_graph, html_report, overlap_matrix, text_table

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
    # Backends
    "AsyncBackendWrapper",
    "AsyncGraphBackend",
    "GraphBackend",
    "HAS_RUST",
    "PythonGraphBackend",
    "RustGraphBackend",
    "SQLiteBackend",
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
    # Benchmark
    "BenchmarkMetrics",
    "BenchmarkSuite",
    "ScenarioType",
    "run_benchmark",
    "run_scaling_suite",
    # Gates (subprocess-backed evidence)
    "CommandGate",
    "CompileGate",
    "ConstraintGate",
    "GateReport",
    "GateRunResult",
    "GateRunner",
    "MypyGate",
    "PytestGate",
    # Visualization
    "dot_graph",
    "html_report",
    "overlap_matrix",
    "text_table",
    # Factories
    "create_delegation_checker",
]

# Conditional export: AnthropicSemanticMatcher (only when anthropic installed)
try:
    from convergent.semantic import AnthropicSemanticMatcher  # noqa: F401

    __all__.append("AnthropicSemanticMatcher")
except ImportError:
    pass


def create_delegation_checker(
    min_stability: float = 0.0,
    backend: GraphBackend | None = None,
) -> IntentResolver:
    """Create an IntentResolver configured for delegation coherence checking.

    Convenience factory for Gorgon integration. Uses a PythonGraphBackend
    by default (in-memory, no persistence needed for delegation checks).

    Args:
        min_stability: Minimum stability threshold for overlap detection.
        backend: Optional custom backend (e.g., SQLiteBackend for persistence).

    Returns:
        Configured IntentResolver ready for delegation checking.
    """
    return IntentResolver(
        backend=backend or PythonGraphBackend(),
        min_stability=min_stability,
    )

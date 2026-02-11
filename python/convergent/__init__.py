"""Convergent — Multi-agent coherence through ambient intent awareness."""

__version__ = "0.1.0"

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
from convergent.resolver import IntentResolver
from convergent.semantic import (
    ConstraintApplicability,
    SemanticMatch,
    SemanticMatcher,
    TrajectoryPrediction,
)

__all__ = [
    "Constraint",
    "ConstraintApplicability",
    "ConstraintSeverity",
    "Evidence",
    "EvidenceKind",
    "Intent",
    "IntentResolver",
    "InterfaceKind",
    "InterfaceSpec",
    "SemanticMatch",
    "SemanticMatcher",
    "TrajectoryPrediction",
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

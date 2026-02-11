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

__all__ = [
    "Constraint",
    "ConstraintSeverity",
    "Evidence",
    "EvidenceKind",
    "Intent",
    "InterfaceKind",
    "InterfaceSpec",
    "IntentResolver",
    "names_overlap",
    "normalize_constraint_target",
    "normalize_name",
    "normalize_type",
    "parse_signature",
    "signatures_compatible",
]

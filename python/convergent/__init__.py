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
]

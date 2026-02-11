# Convergent — Claude Code Context

## What This Is
Multi-agent coherence library. Agents observe a shared intent graph and independently converge on compatible outputs. No inter-agent communication.

## Architecture
- `src/` — Rust core (PyO3): IntentGraph, StabilityScorer, query engine, SQLite persistence
- `python/convergent/` — Python layer: IntentResolver, SimulatedAgent, demo
- `tests/` — Pytest suite proving convergence properties

## Key Concepts
- **IntentNode**: A decision an agent publishes (what it provides, requires, constrains)
- **Stability**: Confidence score (0.0–1.0) based on evidence (tests, commits, dependents)
- **Resolution**: Reading the graph and adjusting for compatibility
- **Convergence**: Agents independently arriving at compatible outputs

## Build & Test
```bash
# Python only (no Rust needed)
PYTHONPATH=python pytest tests/ -v

# With Rust core
maturin develop --release
pytest tests/ -v

# Run demo
PYTHONPATH=python python -m convergent
```

## Coding Standards
- Type hints on all function signatures
- Docstrings on public methods
- Rust: cargo fmt && cargo clippy
- Python: ruff check && mypy

## What NOT To Modify
- The append-only invariant of IntentGraph (core design principle)
- Stability scoring weights without updating tests
- PyO3 bindings without matching Python fallback implementations

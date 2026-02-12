# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-02-12

### Added
- **3-layer coordination stack**: Constraints (hard truth) → Intent Graph (decisions) → Economics (optimization)
- `constraints.py` — Constraint engine with severity levels and gate integration
- `gates.py` — Subprocess-backed evidence producers (Pytest, Mypy, Compile, Command gates)
- `governor.py` — MergeGovernor single entry point enforcing 3-layer ordering
- `versioning.py` — VersionedGraph with snapshots, branching, merge conflict classification
- `economics.py` — Budget tracking, EV-based escalation policy (auto-resolve vs escalate)
- `replay.py` — Deterministic replay engine proving same intents + same policy = same state
- `contract.py` — Formal coordination contract with content hashing and verification
- `benchmark.py` — Performance benchmark suite for graph operations
- `codegen_demo.py` — End-to-end demo of 3-agent coordination
- Dependabot for pip, cargo, and GitHub Actions

### Fixed
- `VersionedGraph.merge()` publishing intents with HUMAN_ESCALATION conflicts
- `Budget.record_resolve/record_escalation` silently ignoring charge failures
- `CoordinationCostReport` dropping BLOCK decisions
- Dead `weights`/`policy` params in `ReplayLog.replay()`
- `codegen_demo` returning hardcoded 0 for conflict/adjustment metrics
- 1,322 ruff lint violations and Rust formatting drift

### Changed
- Version synced from 0.4.0 to 0.2.0 (correct semver after v0.1.0)
- Coverage omit for `semantic.py` and `demo.py` (LLM-dependent + legacy)

### Tests
- 322 Python tests + 36 Rust tests (99% coverage on testable code)
- 7 modules at 100% coverage

## [0.1.0] - 2026-02-10

### Added
- Initial Convergent library — multi-agent coherence through ambient intent awareness
- Rust core (PyO3): IntentGraph, StabilityScorer, query engine, SQLite persistence
- Python layer: IntentResolver, SimulatedAgent, PythonGraphBackend
- Structural semantic matching (name normalization, signature compatibility, tag overlap)
- LLM-powered semantic matching via AnthropicSemanticMatcher (optional)
- Formal coordination contract with content hashing
- Live LLM smoke test script (15/15 against Anthropic API)
- Pure-Python install via setuptools (no Rust toolchain required)
- Optional Rust acceleration via `maturin develop --release`
- GitHub Actions CI for Rust + Python matrix (3.10/3.11/3.12)

[Unreleased]: https://github.com/AreteDriver/convergent/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/AreteDriver/convergent/releases/tag/v0.2.0
[0.1.0]: https://github.com/AreteDriver/convergent/commit/73e2b29

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-02-14

### Changed
- **Stable API contract** — v1.0.0 declares the public API stable under semver
- Published to PyPI (`pip install convergent`)
- PEP 561 `py.typed` marker for type checker support
- Classifier upgraded to Production/Stable
- Added Python 3.13 classifier
- Tag-triggered publish workflow (trusted publishing via OIDC)

## [0.6.0] - 2026-02-14

### Added
- **Pluggable signal bus architecture** — `SignalBackend` protocol with two implementations
- `signal_backend.py` — `SignalBackend` protocol (runtime_checkable) + `FilesystemSignalBackend` extracted from original SignalBus
- `sqlite_signal_backend.py` — `SQLiteSignalBackend` for cross-process coordination (WAL mode, consumer-based tracking, ACID guarantees, zero new dependencies)
- **Decision history query API** — persisted consensus decisions and vote records
- `ScoreStore.record_decision()` — persist full Decision + individual vote records
- `ScoreStore.get_decision_history()` — query with task_id, outcome, since, limit filters
- `ScoreStore.get_decision_json()` — retrieve full Decision JSON by request_id
- `ScoreStore.get_vote_records()` — query individual vote records by agent or request
- `ScoreStore.get_agent_vote_stats()` — aggregated voting statistics per agent
- `GorgonBridge.get_decision_history()` / `get_agent_vote_stats()` — bridge delegation methods

### Changed
- `SignalBus` refactored to accept pluggable `backend` parameter (backward-compatible: `signals_dir` still works)
- `SignalBus` gains `consumer_id`, `close()`, and `backend` property
- `CoordinationConfig.signal_bus_type` default changed from `"filesystem"` to `"sqlite"`
- `GorgonBridge` uses SQLiteSignalBackend by default (filesystem still available via config)
- `Triumvirate` accepts optional `store` parameter for decision persistence (graceful degradation)
- Version bumped to 0.6.0

### Tests
- 130+ new tests across 8 test files (800+ total, 99% coverage)

## [0.5.0] - 2026-02-14

### Added
- **Phase 3: Coordination Protocol** — bio-inspired multi-agent coordination layer
- `protocol.py` — Coordination data models: AgentIdentity, Vote, ConsensusRequest, Decision, StigmergyMarker, Signal, QuorumLevel, VoteChoice, DecisionOutcome enums
- `coordination_config.py` — CoordinationConfig dataclass for Phase 3 settings
- `scoring.py` + `score_store.py` — Phi-weighted scoring engine with Bayesian smoothing, exponential decay, per-agent per-domain trust scores, SQLite persistence
- `triumvirate.py` — Voting engine with ANY/MAJORITY/UNANIMOUS/UNANIMOUS_HUMAN quorum, phi-weighted votes, tie-breaking, escalation, timeout handling
- `signal_bus.py` — Filesystem-backed pub/sub for inter-agent communication with polling, targeted/broadcast delivery, expiry cleanup
- `stigmergy.py` — Trail markers with exponential evaporation, reinforcement, context generation for agent prompts, SQLite persistence
- `flocking.py` — Swarm coordination: alignment (pattern sharing), cohesion (drift detection), separation (file conflict avoidance)
- `gorgon_bridge.py` — Single entry point for Gorgon integration: prompt enrichment, consensus voting, outcome recording, marker management

### Changed
- Version bumped to 0.5.0
- Updated README with Phase 3 documentation, Mermaid architecture diagram, quick start examples, feature matrix
- Description updated: "Multi-agent coherence and coordination for AI systems"

### Tests
- 240+ new tests across 7 test files (670+ total, 97% coverage)

## [0.4.0] - 2026-02-12

### Added
- **CLI inspector** (`__main__.py`): `python -m convergent inspect <db>` with `--format {table,dot,html,matrix}`, `--min-stability`, `--agent`, `--show-evidence`, `--output` options. `python -m convergent demo` runs existing demo
- **Async backend** (`async_backend.py`): `AsyncGraphBackend` protocol and `AsyncBackendWrapper` using `asyncio.to_thread()` — zero new dependencies, wraps any sync backend
- **Rust backend parity** (`rust_backend.py`): `RustGraphBackend` wrapper for PyO3 `IntentGraph` with dict conversion handling InterfaceKind capitalization, missing severity, RFC3339 timestamps
- **Serialization module** (`_serialization.py`): Extracted shared serialization helpers from `sqlite_backend.py` for reuse across backends

### Changed
- `sqlite_backend.py` imports serialization helpers from `_serialization.py` instead of defining inline

### Tests
- ~49 new tests: CLI inspector (~15), async backend (~14), Rust backend (~20)

## [0.3.0] - 2026-02-12

### Added
- **SQLite backend** (`sqlite_backend.py`): Persistent intent graph using stdlib `sqlite3` with WAL mode, denormalized `intent_interfaces` table for efficient overlap queries, and full serialization round-trips
- **Graph visualization** (`visualization.py`): Four output formats — `text_table`, `dot_graph` (graphviz DOT), `html_report` (self-contained), `overlap_matrix` (text matrix)
- **Event callbacks**: Hook system on `IntentResolver` — `add_hook`/`remove_hook` for `"publish"`, `"resolve"`, and `"conflict"` events with exception-safe firing
- **Delegation checker factory**: `create_delegation_checker()` convenience function for Gorgon integration
- `GraphBackend` and `PythonGraphBackend` now exported from package
- `VersionedGraph` accepts `backend_factory` kwarg for custom backend construction

### Changed
- Gorgon `convergence.py`: Added `create_checker()` factory and `format_convergence_alert()` formatter
- Gorgon `supervisor.py`: Enhanced conflict handling with formatted alerts and dropped agent count logging
- Gorgon API and TUI: Wired `convergence_checker=create_checker()` with graceful degradation

### Tests
- 403 Python tests + 36 Rust tests (81 new: 40 SQLite, 18 hooks, 20 visualization, 3 factory)

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

[Unreleased]: https://github.com/AreteDriver/convergent/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/AreteDriver/convergent/compare/v0.6.0...v1.0.0
[0.6.0]: https://github.com/AreteDriver/convergent/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/AreteDriver/convergent/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/AreteDriver/convergent/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/AreteDriver/convergent/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/AreteDriver/convergent/releases/tag/v0.2.0
[0.1.0]: https://github.com/AreteDriver/convergent/commit/73e2b29

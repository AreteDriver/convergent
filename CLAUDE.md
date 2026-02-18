# CLAUDE.md — Convergent: Multi-Agent Coordination Protocol

## What This Project Is

Convergent is a multi-agent coherence and coordination library. It has two layers:

1. **Intent Graph (Phase 1-2, v0.1.0-v0.4.0)** — Agents observe a shared intent graph and independently converge on compatible outputs. No inter-agent communication required. This is the ambient awareness layer.

2. **Coordination Protocol (Phase 3, v0.5.0)** — Bio-inspired patterns that sit on top of the intent graph: Triumvirate voting, stigmergy (ant-trail markers), flocking (emergent group behavior from simple local rules), signal bus (pub/sub), and phi-weighted scoring. This is the active coordination layer.

Think of it this way: the intent graph lets agents *see* what others are doing. The coordination protocol lets agents *decide together*, *learn from outcomes*, and *avoid collisions*.

This is an open-source companion to [Gorgon](https://github.com/AreteDriver/Gorgon). It can be used standalone for any multi-agent system that needs coordination, not just Gorgon.

## Tech Stack

- **Python >=3.10** — pure Python, zero production dependencies
- **Rust (optional)** — PyO3 bindings for performance-critical graph operations
- **SQLite** — persistence for intent graph, scores, stigmergy markers, vote history
- **No frameworks** — this is a library, not an application
- **pytest** — testing (880+ tests, 97% coverage)

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         GORGON                                  │
│                   (orchestrator, external)                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       CONVERGENT                                │
│                                                                 │
│  Phase 3: Coordination Protocol (BUILT, v0.5.0)                 │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐             │
│  │ Triumvirate  │  │  Stigmergy   │  │  Flocking  │             │
│  │ (voting)     │  │  (markers)   │  │  (swarm)   │             │
│  │              │  │              │  │            │             │
│  │ N agents     │  │ Leave trails │  │ Alignment  │             │
│  │ phi-weighted │  │ for future   │  │ Cohesion   │             │
│  │ quorum rules │  │ agents       │  │ Separation │             │
│  └──────┬──────┘  └──────┬───────┘  └─────┬──────┘             │
│         └────────┬───────┴─────────────────┘                    │
│                  ▼                                               │
│  Phase 1-2: Intent Graph + Intelligence (BUILT)                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Intent Graph  │  Contracts  │  Governor  │  Economics   │   │
│  │  Constraints   │  Gates      │  Semantic  │  Versioning  │   │
│  │  Matching      │  Replay     │  Benchmark │  Backends    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                  ▼                                               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Backends: PythonGraphBackend │ SQLiteBackend │ Rust(opt) │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
convergent/
├── CLAUDE.md                  ← YOU ARE HERE
├── pyproject.toml             ← v1.0.0, python >=3.10, zero deps
├── Cargo.toml                 ← Rust/PyO3 build config
├── README.md
├── CHANGELOG.md
├── LICENSE                    ← MIT
│
├── python/convergent/         ← Python package (all new modules go here)
│   ├── __init__.py            ← Public API exports (~70 classes)
│   ├── __main__.py            ← CLI inspector
│   ├── intent.py              ← Core: Intent, InterfaceSpec, Constraint, Evidence
│   ├── resolver.py            ← IntentResolver, GraphBackend, PythonGraphBackend
│   ├── matching.py            ← Structural overlap, signature compatibility
│   ├── semantic.py            ← LLM-powered semantic matching (optional anthropic)
│   ├── constraints.py         ← ConstraintEngine, TypedConstraint
│   ├── contract.py            ← IntentGraphContract, validation, conflict detection
│   ├── economics.py           ← Budget, CostModel, EscalationPolicy
│   ├── gates.py               ← GateRunner, PytestGate, MypyGate, CompileGate
│   ├── governor.py            ← MergeGovernor, final decision authority
│   ├── versioning.py          ← VersionedGraph, branching, merging, snapshots
│   ├── sqlite_backend.py      ← SQLite persistence (WAL mode)
│   ├── rust_backend.py        ← Optional Rust PyO3 wrapper (HAS_RUST flag)
│   ├── async_backend.py       ← Async wrapper for graph operations
│   ├── agent.py               ← Simulated agent harness for demos
│   ├── replay.py              ← Replay system for debugging
│   ├── visualization.py       ← Text tables, dot graphs, HTML reports
│   ├── benchmark.py           ← Scaling & performance benchmarks
│   ├── _serialization.py      ← JSON serialization utilities
│   ├── demo.py                ← Demo workflows
│   ├── codegen_demo.py        ← Code generation example
│   │
│   │── # --- Phase 3: Coordination Protocol (v0.5.0) ---
│   ├── protocol.py            ← ConsensusRequest, Vote, Decision, Signal, AgentIdentity
│   ├── coordination_config.py ← CoordinationConfig dataclass
│   ├── scoring.py             ← PhiScorer, phi-weighted trust scores (Bayesian + decay)
│   ├── score_store.py         ← SQLite persistence for scores, votes, decisions
│   ├── triumvirate.py         ← Voting engine (ANY/MAJORITY/UNANIMOUS/UNANIMOUS_HUMAN)
│   ├── signal_backend.py      ← SignalBackend protocol + FilesystemSignalBackend
│   ├── signal_bus.py          ← Pluggable pub/sub with backend injection
│   ├── sqlite_signal_backend.py ← SQLite signal backend (cross-process, WAL)
│   ├── stigmergy.py           ← Trail markers with evaporation/reinforcement (own SQLite)
│   ├── flocking.py            ← Swarm coordination (alignment/cohesion/separation)
│   ├── gorgon_bridge.py       ← Single entry point for Gorgon integration
│   │
│   │── # --- Phase 4: Observability & Analysis (v1.1.0) ---
│   ├── health.py              ← CoordinationHealth dashboard + grading (A-F)
│   ├── cycles.py              ← Dependency cycle detection + topological sort
│   └── event_log.py           ← Append-only coordination event log + timeline
│
├── src/                       ← Rust core (PyO3) — DO NOT BREAK
│   ├── lib.rs                 ← PyO3 module entry point
│   ├── graph.rs               ← IntentGraph implementation
│   ├── models.rs              ← Rust data models
│   ├── matching.rs            ← Structural matching
│   └── stability.rs           ← Stability scoring
│
├── tests/                     ← 880+ tests, 97% coverage
│   ├── test_convergence.py    ← Core convergence properties
│   ├── test_contract.py       ← Contract validation
│   ├── test_three_layer.py    ← 3-layer coordination stack
│   ├── test_coverage_push.py  ← Edge case coverage
│   ├── test_semantic.py       ← Semantic matching
│   ├── test_sqlite_backend.py ← SQLite backend
│   ├── test_async_backend.py  ← Async backend (requires Rust)
│   ├── test_rust_backend.py   ← Rust backend (requires Rust)
│   ├── test_hooks.py          ← Hook system
│   ├── test_cli.py            ← CLI inspector
│   ├── test_benchmark_gates_demo.py
│   ├── test_delegation_factory.py
│   ├── test_visualization.py
│   │
│   │── # --- Phase 3 tests ---
│   ├── test_protocol.py       ← Protocol data models + JSON round-trips
│   ├── test_scoring.py        ← Phi scoring + score store persistence
│   ├── test_triumvirate.py    ← Voting engine + quorum rules
│   ├── test_signal_backend.py  ← SignalBackend protocol + FilesystemSignalBackend
│   ├── test_signal_bus.py     ← Pub/sub + polling + multi-consumer + SQLite backend
│   ├── test_sqlite_signal_backend.py ← SQLite signal backend tests
│   ├── test_stigmergy.py      ← Markers + evaporation + context
│   ├── test_flocking.py       ← Alignment/cohesion/separation
│   ├── test_gorgon_bridge.py  ← Bridge lifecycle + enrichment
│   │
│   │── # --- Phase 4 tests ---
│   ├── test_health.py         ← Health dashboard + grading
│   ├── test_cycles.py         ← Cycle detection + topological sort
│   └── test_event_log.py      ← Event log + timeline renderer
│
└── scripts/
    └── smoke_test_llm.py      ← Live LLM smoke test
```

## Coding Standards

Same as Gorgon:
- **Type hints on all function signatures.** No exceptions.
- **Docstrings**: Google style. Every public function and class.
- **Imports**: stdlib → third-party → local, separated by blank lines.
- **Naming**: `snake_case` functions/variables, `PascalCase` classes, `UPPER_SNAKE` constants.
- **Error handling**: Specific exceptions only. Log with context.
- **Logging**: `logging` module, never `print()` in library code.
- **No global mutable state.** Dependencies passed explicitly.
- **Tests**: Every module gets a test file. Happy path + edge case + error case minimum.
- **Commits**: Conventional commits.
- **Line length**: 100 chars max (matches ruff config).
- **Target version**: Python 3.10 (matches pyproject.toml).

**Additional for Convergent (library-specific):**
- **No side effects on import.** Importing a module must not create files, open connections, or start threads.
- **Everything is composable.** User should be able to use Triumvirate without Stigmergy, or Signal Bus without voting.
- **Dataclasses over dicts.** All protocol messages are typed dataclasses.
- **Thread-safe where noted.** Signal bus and score store must support concurrent access.
- **Don't break existing modules.** New features are additive — they must not modify existing code.
- **SQLite pattern:** See `sqlite_backend.py` and `score_store.py` for the established patterns (WAL mode, `check_same_thread=False`). New persistence code should follow the same conventions.
- **Stigmergy has its own SQLite DB** — separate from score_store for composability. GorgonBridge uses `Path(db_path).with_suffix(".stigmergy.db")`.

## Current State (v1.0.0)

### Phase 1-2: Intent Graph + Intelligence (Complete)
- **36 production modules**, 880+ tests, 97% coverage
- **Intent graph** — Core data model: Intent, InterfaceSpec, Constraint, Evidence
- **Contract system** — Validation, conflict detection, mutation tracking
- **Three-layer stack** — Constraints → Intent Graph → Economics
- **Governor** — MergeGovernor for final merge/reject decisions
- **Semantic matching** — Structural + optional LLM-powered (anthropic)
- **Backends** — PythonGraphBackend (memory), SQLiteBackend (persistent), RustGraphBackend (optional PyO3)
- **Versioning** — VersionedGraph with branching, merging, snapshots
- **Gates** — Subprocess-backed evidence (pytest, mypy, compile, custom commands)
- **CLI** — Inspector via `__main__.py`

### Phase 3: Coordination Protocol (Complete, v0.5.0)
- **Protocol data models** — AgentIdentity, Vote, ConsensusRequest, Decision, Signal, StigmergyMarker (frozen dataclasses, JSON round-trips)
- **CoordinationConfig** — Centralized config for Phase 3 settings
- **Phi-weighted scoring** — Bayesian smoothing with exponential decay, per-agent per-domain trust scores, bounded [0.1, 0.95], SQLite persistence
- **Triumvirate voting** — ANY/MAJORITY/UNANIMOUS/UNANIMOUS_HUMAN quorum, phi-weighted votes, tie-breaking, escalation, timeout handling, decision persistence
- **Signal bus** — Pluggable backend architecture with FilesystemSignalBackend and SQLiteSignalBackend, polling thread, targeted/broadcast delivery, multi-consumer support, expiry cleanup
- **Decision history** — Persisted decisions and vote records with query API (filter by task, outcome, agent; aggregated vote statistics)
- **Stigmergy** — Trail markers with exponential evaporation, reinforcement, context generation, own SQLite DB
- **Flocking** — Alignment (pattern sharing), cohesion (Jaccard keyword drift detection), separation (file conflict avoidance)
- **GorgonBridge** — Single entry point for Gorgon: prompt enrichment, consensus voting, outcome recording, marker management, decision history queries

### Phase 4: Observability & Analysis (v1.1.0)
- **Health dashboard** — HealthChecker aggregates metrics from intent graph, stigmergy, phi scores, voting. Grading A-F based on issue count. CLI `convergent health <db>`
- **Cycle detection** — DependencyGraph from provides/requires edges, DFS cycle detection, Kahn's topological sort for execution ordering. CLI `convergent cycles <db>`
- **Event log** — Append-only SQLite log with 10 event types, correlation IDs, time-range queries, timeline renderer. CLI `convergent events <db>`

### Gorgon Integration
- `create_delegation_checker()` — Intent graph delegation (Phase 1-2)
- `GorgonBridge` — Full coordination protocol (Phase 3)

---

## What NOT To Modify

- The **append-only invariant** of IntentGraph (core design principle)
- **Stability scoring weights** without updating tests
- **PyO3 bindings** without matching Python fallback implementations
- **Existing module APIs** — new features are additive, not rewrites
- **pyproject.toml** structure — only append new optional deps if needed
- **Rust source** (`src/`) — coordination protocol is pure Python

## Build & Test

```bash
# Python only (no Rust needed)
PYTHONPATH=python pytest tests/ -v

# With Rust core (optional, for performance)
maturin develop --release
pytest tests/ -v

# Run demo
PYTHONPATH=python python -m convergent

# Lint
ruff check python/ tests/
ruff format python/ tests/
```

## Rules for All Claude Code Sessions

1. **Read this file first.** Every session starts by reading CLAUDE.md.
2. **This is a library, not an app.** No servers, no daemons. The existing CLI inspector is the only entry point.
3. **Test before committing.** Run `PYTHONPATH=python pytest tests/ -v`. ALL tests must pass (existing + new).
4. **Commit messages:** Conventional commits.
5. **Composable design.** Every component must work independently. No circular imports. No hidden dependencies between modules.
6. **Append to __init__.py.** New exports go at the bottom. Don't reorganize existing exports.
7. **All new files go in `python/convergent/`.** Not in a top-level `convergent/` directory.
8. **Ask if unclear.** Document assumptions in code comments.

## Related Skills

From [ai-skills](https://github.com/AreteDriver/ai-skills):
- `intent-author` — teaches agents how to publish well-structured intents
- `entity-resolver` — shared entity identity across parallel agents

# Convergent

Coordination library for multi-agent AI systems. Agents share an intent graph, detect overlaps before building, and converge on compatible outputs — eliminating rework cycles from parallel code generation.

[![CI](https://github.com/AreteDriver/convergent/actions/workflows/ci.yml/badge.svg)](https://github.com/AreteDriver/convergent/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-800+-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-99%25-brightgreen.svg)]()

## Why This Exists

- **Problem:** Parallel AI agents generating code independently produce incompatible outputs. Agent A builds `User` with `int` IDs while Agent B uses `UUID`. Code fails to merge. 2-3 rework cycles before anything integrates.
- **Audience:** Multi-agent orchestration frameworks, distributed systems with autonomous agents, anyone running parallel AI code generation.
- **Outcome:** Agents publish what they're building to a shared intent graph. Before starting work, they check for overlaps and adopt existing decisions. Compatible output on first try. Zero rework.

## What It Does

- **Intent graph** — Shared, append-only graph of architectural decisions. Agents publish intents (what they build, what they need) and query for overlaps
- **Structural matching** — Detect when two agents plan to build the same interface based on name, kind, and tag similarity
- **Stability scoring** — Evidence-weighted confidence (test passes, code commits, downstream consumers) determines which intent wins conflicts
- **Constraint enforcement** — Hard requirements that must hold (type checks pass, no circular deps) validated by subprocess gates
- **Triumvirate voting** — Phi-weighted consensus engine with configurable quorum (ANY, MAJORITY, UNANIMOUS)
- **Stigmergy** — Trail markers that agents leave for future agents, with exponential decay (inspired by ant pheromone trails)
- **Flocking** — Emergent group behavior from local rules: alignment (adopt patterns), cohesion (detect drift), separation (avoid file conflicts)
- **Zero dependencies** — Pure Python, stdlib only. Optional Rust acceleration via PyO3

## Quickstart

### Prerequisites

- Python 3.10+

### Install

```bash
pip install convergent
# or from source:
git clone https://github.com/AreteDriver/convergent.git
cd convergent
pip install -e .
```

### Run

```python
from convergent import IntentResolver, PythonGraphBackend, Intent, InterfaceSpec

resolver = IntentResolver(backend=PythonGraphBackend())

# Agent A publishes what it's building
resolver.publish(Intent(
    intent_id="auth-service",
    agent_id="agent-a",
    description="JWT authentication service",
    interfaces=[
        InterfaceSpec(name="User", kind="class", tags=["auth", "model"]),
    ],
))

# Agent B checks for overlapping work before starting
overlaps = resolver.find_overlapping(Intent(
    intent_id="user-module",
    agent_id="agent-b",
    description="User management",
    interfaces=[
        InterfaceSpec(name="User", kind="class", tags=["auth", "model"]),
    ],
))
# → overlaps shows agent-a already owns the User class
# → agent-b adopts agent-a's schema instead of building its own
```

## Usage Examples

### Example 1: Persistent intent graph with SQLite

```python
from convergent import IntentResolver, SQLiteBackend

# WAL mode, concurrent reads, persistent across restarts
resolver = IntentResolver(backend=SQLiteBackend("./intents.db"))
resolver.publish(intent)

# Inspect from CLI
# python -m convergent inspect ./intents.db --format table
```

### Example 2: Consensus voting

```python
from convergent import GorgonBridge, CoordinationConfig

bridge = GorgonBridge(CoordinationConfig(db_path="./coordination.db"))

# Request a vote
request_id = bridge.request_consensus(
    task_id="pr-42",
    question="Should we merge this PR?",
    context="All tests pass, adds new auth endpoint",
)

# Agents vote (phi-weighted by historical trust)
bridge.submit_agent_vote(
    request_id, "agent-1", "reviewer", "claude:sonnet",
    "approve", 0.9, "LGTM"
)

decision = bridge.evaluate(request_id)
# → DecisionOutcome.APPROVED
```

### Example 3: Enrich agent prompts with coordination context

```python
context = bridge.enrich_prompt(
    agent_id="agent-1",
    task_description="implement auth",
    file_paths=["src/auth.py"],
)
# → Returns stigmergy markers + flocking constraints + phi score context
# → Inject into agent's system prompt for coordination-aware generation
```

## Architecture

```text
Gorgon (orchestrator)
    │
    ▼
┌── Convergent ───────────────────────────────────────┐
│                                                      │
│  Coordination Protocol (Phase 3)                     │
│  ┌────────────┐  ┌───────────┐  ┌─────────┐        │
│  │ Triumvirate │  │ Stigmergy │  │Flocking │        │
│  │ (voting)    │  │ (trails)  │  │ (swarm) │        │
│  └──────┬──────┘  └─────┬─────┘  └────┬────┘        │
│         └───────┬───────┴─────────────┘              │
│                 ▼                                     │
│  Intent Graph + Intelligence (Phase 1-2)             │
│  ┌──────────────────────────────────────────┐        │
│  │ Resolver │ Contracts │ Governor │ Gates  │        │
│  └──────────────────────────────────────────┘        │
│                 ▼                                     │
│  ┌──────────────────────────────────────────┐        │
│  │ Python (memory) │ SQLite │ Rust (opt)    │        │
│  └──────────────────────────────────────────┘        │
└──────────────────────────────────────────────────────┘
```

**Key components:**

| Component | Purpose |
|-----------|---------|
| `IntentResolver` | Query the intent graph, detect overlaps, resolve conflicts |
| `MergeGovernor` | Three-layer decision authority: constraints → intents → economics |
| `Triumvirate` | Phi-weighted voting with configurable quorum levels |
| `StigmergyField` | Trail markers with exponential decay for indirect agent communication |
| `FlockingCoordinator` | Alignment, cohesion, separation rules for emergent coordination |
| `GorgonBridge` | Single entry point for orchestrator integration |

## Testing

```bash
# Python-only (no Rust needed)
PYTHONPATH=python pytest tests/ -v

# With optional Rust acceleration
maturin develop --release && pytest tests/ -v

# Lint
ruff check python/ tests/ && ruff format --check python/ tests/
```

800+ tests, 99% coverage, CI green.

## Roadmap

- **v1.0.0** (current): Stable API contract, published to PyPI, PEP 561 py.typed
- **v0.6.0**: Pluggable signal bus (SQLite cross-process + filesystem), decision history query API
- **v0.5.0**: Coordination protocol (triumvirate voting, stigmergy, flocking, signal bus)
- **v0.4.0**: CLI inspector, async backend, Rust backend parity

## License

[MIT](LICENSE)

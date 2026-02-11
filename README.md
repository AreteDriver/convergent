# Convergent

**Multi-agent coherence through ambient intent awareness.**

Convergent solves the fundamental problem of parallel AI agent coordination: multiple agents generating code simultaneously will produce incompatible outputs because they diverge from a shared starting point without shared understanding of where they're going.

Existing approaches treat this as a communication problem (message passing, blackboards) or a merge problem (reconciliation, test-gating). Both are reactive — they address divergence after it happens.

Convergent prevents divergence from occurring. Agents don't communicate with each other. They observe a shared **intent graph** — a structured representation of decisions and interfaces — and independently adjust their work to be compatible. Coherence emerges from ambient awareness, not coordination.

## How It Works

```
Agents don't talk to each other.
They observe the same evolving landscape
and independently converge.
```

### The Intent Graph

A shared, append-only data structure where agents publish their architectural decisions as **IntentNodes**:

- What they decided to build
- What interfaces they provide
- What interfaces they require
- What constraints their decisions impose on other scopes

### The Stability Gradient

Each intent has a stability score (0.0–1.0) based on evidence:

- Low stability (exploring) → other agents treat as soft suggestions
- High stability (code committed, tests passing) → treated as hard constraints

Early decisions with high evidence become **attractors** that pull later decisions toward compatibility.

### The Intent Resolver

Before each major decision point, an agent's resolver reads the intent graph and adjusts plans to be compatible with high-stability decisions from other agents. No supervisor. No messages. Just independent agents observing the same landscape.

### Convergent Generation

The result: agents that started from the same codebase snapshot independently arrive at compatible outputs — not because they coordinated, but because the intent graph made divergence structurally unlikely.

## Architecture

```
┌─────────────────────────────────────────────────┐
│                  Python Layer                     │
│                                                   │
│  Agent Harness ─── Intent Publisher               │
│       │              │                            │
│       │              ▼                            │
│       │         Intent Resolver ◄── Semantic      │
│       │              │              Matcher       │
│       │              ▼                            │
│  ┌─────────────────────────────────────────┐     │
│  │           Rust Core (PyO3)               │     │
│  │                                          │     │
│  │  IntentGraph ── StabilityScorer          │     │
│  │       │              │                   │     │
│  │       ▼              ▼                   │     │
│  │  SQLite Store   Evidence Tracker         │     │
│  │       │                                  │     │
│  │       ▼                                  │     │
│  │  Query Engine (overlap, conflict detect) │     │
│  └─────────────────────────────────────────┘     │
└─────────────────────────────────────────────────┘
```

**Rust Core** (performance-critical):
- Intent graph storage and querying
- Stability score computation
- Overlap and conflict detection between interface specs
- SQLite-backed persistence

**Python Layer** (iteration-friendly):
- Agent harness and simulation
- Intent resolver logic
- Semantic matching (LLM-powered, future)
- Orchestration and demo workflows

## Quick Start

```bash
# Clone
git clone https://github.com/AreteDriver/convergent.git
cd convergent

# Install (requires Rust toolchain + Python 3.10+)
pip install maturin
maturin develop --release

# Run the convergence demo
python -m convergent.demo

# Run tests
pytest tests/ -v
cargo test
```

## Demo: Three Agents Building a Recipe App

The included demo simulates three agents building different modules of a recipe application:

- **Agent A**: Authentication module (User model, AuthService)
- **Agent B**: Recipe module (Recipe model, RecipeService)
- **Agent C**: Meal planning module (MealPlan model, MealPlanService)

Without Convergent, these agents would independently create incompatible User models, conflicting database schemas, and mismatched interfaces.

With Convergent, each agent publishes intents as it works. Agent C observes Agent A's committed User model and adopts it. Agent B's Recipe references Agent A's User type. Agent C's MealPlan consumes Agent B's Recipe interface. All three converge on a compatible design — without any direct communication.

```
T=0  All agents start from same codebase snapshot
T=1  Agent A: "AuthService with JWT" (stability: 0.3)
T=2  Agent A commits User model (stability: 0.7)
     Agent C resolves: adopts Agent A's User type
T=3  Agent B commits RecipeService (stability: 0.8)
     Agent C resolves: uses Recipe FK pattern from Agent B
T=4  All agents complete. Intent graph shows no conflicts.
     Merge succeeds. Integration tests pass.
```

## Project Status

**Phase 1: Core Library**
- [x] IntentGraph (Rust + SQLite)
- [x] IntentNode schema
- [x] StabilityScorer
- [x] IntentResolver
- [x] Simulated agent harness
- [x] Convergence test suite
- [x] Semantic matching (structural, non-LLM)

**Phase 2: Intelligence** ← Current
- [x] LLM-powered semantic overlap detection
- [x] Predictive convergence (anticipate other agents' trajectories)
- [x] Confidence-scored auto-resolution

**Phase 3: Gorgon Integration**
- [ ] Import as dependency in Gorgon orchestrator
- [ ] Wire to parallel execution patterns
- [ ] Real Claude Code agent harness

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Intent** | A structured decision an agent has made (what it builds, provides, requires) |
| **Stability** | Confidence score (0.0–1.0) based on evidence (tests, commits, dependents) |
| **Resolution** | An agent reading the intent graph and adjusting for compatibility |
| **Convergence** | Multiple agents independently arriving at compatible outputs |
| **Ambient awareness** | Agents observe a shared landscape, not each other |

## Why This Matters

Every multi-agent coding framework (Devin, Factory, OpenClaw, Blitzy) struggles with parallel agent coordination. They all use some form of message passing or supervisor coordination. Convergent introduces a new primitive: the **semantic intent layer** between isolated execution and explicit communication.

This is how flocking works in nature. Birds don't send messages to coordinate formation. They each follow simple rules relative to their neighbors and coherent behavior emerges.

## License

MIT

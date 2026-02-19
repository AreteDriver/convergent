window.BENCHMARK_DATA = {
  "lastUpdate": 1771496248627,
  "repoUrl": "https://github.com/AreteDriver/convergent",
  "entries": {
    "Rust Benchmarks": [
      {
        "commit": {
          "author": {
            "email": "AreteDriver@users.noreply.github.com",
            "name": "AreteDriver",
            "username": "AreteDriver"
          },
          "committer": {
            "email": "AreteDriver@users.noreply.github.com",
            "name": "AreteDriver",
            "username": "AreteDriver"
          },
          "distinct": true,
          "id": "6a37f73ed2d0d3a9f1907bad026a0e17137aff99",
          "message": "style(bench): run cargo fmt on intent_graph.rs\n\nCo-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>",
          "timestamp": "2026-02-15T03:00:49-08:00",
          "tree_id": "a5d4ea0476a64c6a37c0ed925d22e4dbcdf6a9c2",
          "url": "https://github.com/AreteDriver/convergent/commit/6a37f73ed2d0d3a9f1907bad026a0e17137aff99"
        },
        "date": 1771153524997,
        "tool": "cargo",
        "benches": [
          {
            "name": "publish_single_intent",
            "value": 231713,
            "range": "± 5193",
            "unit": "ns/iter"
          },
          {
            "name": "publish_100_intents",
            "value": 2873124,
            "range": "± 13367",
            "unit": "ns/iter"
          },
          {
            "name": "query_all_100_intents",
            "value": 197848,
            "range": "± 994",
            "unit": "ns/iter"
          },
          {
            "name": "resolve_with_50_existing",
            "value": 742448,
            "range": "± 17017",
            "unit": "ns/iter"
          },
          {
            "name": "find_overlapping_100_intents",
            "value": 614132,
            "range": "± 4616",
            "unit": "ns/iter"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "AreteDriver",
            "username": "AreteDriver"
          },
          "committer": {
            "name": "AreteDriver",
            "username": "AreteDriver"
          },
          "id": "ddfa0b91b4cc6b36fed96641a035a695b8f35c3e",
          "message": "fix(tests): skip tests gracefully when optional deps or root perms",
          "timestamp": "2026-02-15T11:00:56Z",
          "url": "https://github.com/AreteDriver/convergent/pull/16/commits/ddfa0b91b4cc6b36fed96641a035a695b8f35c3e"
        },
        "date": 1771386634953,
        "tool": "cargo",
        "benches": [
          {
            "name": "publish_single_intent",
            "value": 226204,
            "range": "± 2015",
            "unit": "ns/iter"
          },
          {
            "name": "publish_100_intents",
            "value": 2899733,
            "range": "± 16986",
            "unit": "ns/iter"
          },
          {
            "name": "query_all_100_intents",
            "value": 194557,
            "range": "± 1479",
            "unit": "ns/iter"
          },
          {
            "name": "resolve_with_50_existing",
            "value": 747850,
            "range": "± 9434",
            "unit": "ns/iter"
          },
          {
            "name": "find_overlapping_100_intents",
            "value": 612640,
            "range": "± 5079",
            "unit": "ns/iter"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "AreteDriver",
            "username": "AreteDriver"
          },
          "committer": {
            "name": "AreteDriver",
            "username": "AreteDriver"
          },
          "id": "03b1ab549f56ec7c2f2a089ffbdfca5436a3e729",
          "message": "fix(tests): skip tests gracefully when optional deps or root perms",
          "timestamp": "2026-02-15T11:00:56Z",
          "url": "https://github.com/AreteDriver/convergent/pull/16/commits/03b1ab549f56ec7c2f2a089ffbdfca5436a3e729"
        },
        "date": 1771387352973,
        "tool": "cargo",
        "benches": [
          {
            "name": "publish_single_intent",
            "value": 190070,
            "range": "± 1773",
            "unit": "ns/iter"
          },
          {
            "name": "publish_100_intents",
            "value": 2653133,
            "range": "± 19042",
            "unit": "ns/iter"
          },
          {
            "name": "query_all_100_intents",
            "value": 186856,
            "range": "± 3305",
            "unit": "ns/iter"
          },
          {
            "name": "resolve_with_50_existing",
            "value": 682438,
            "range": "± 7533",
            "unit": "ns/iter"
          },
          {
            "name": "find_overlapping_100_intents",
            "value": 556699,
            "range": "± 19645",
            "unit": "ns/iter"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "AreteDriver@gmail.com",
            "name": "James C. Young",
            "username": "AreteDriver"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "0094c737ce833547425a0092105343ef4ffe56d2",
          "message": "Merge pull request #16 from AreteDriver/claude/general-improvements-TDGXq\n\nfix(tests): skip tests gracefully when optional deps or root perms",
          "timestamp": "2026-02-18T02:33:14-08:00",
          "tree_id": "f72aecde00f03e2bfe79207e5298016c2324c5c0",
          "url": "https://github.com/AreteDriver/convergent/commit/0094c737ce833547425a0092105343ef4ffe56d2"
        },
        "date": 1771411022423,
        "tool": "cargo",
        "benches": [
          {
            "name": "publish_single_intent",
            "value": 225003,
            "range": "± 2639",
            "unit": "ns/iter"
          },
          {
            "name": "publish_100_intents",
            "value": 2875326,
            "range": "± 28313",
            "unit": "ns/iter"
          },
          {
            "name": "query_all_100_intents",
            "value": 195882,
            "range": "± 4855",
            "unit": "ns/iter"
          },
          {
            "name": "resolve_with_50_existing",
            "value": 744849,
            "range": "± 5832",
            "unit": "ns/iter"
          },
          {
            "name": "find_overlapping_100_intents",
            "value": 613221,
            "range": "± 4397",
            "unit": "ns/iter"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "AreteDriver@users.noreply.github.com",
            "name": "AreteDriver",
            "username": "AreteDriver"
          },
          "committer": {
            "email": "AreteDriver@users.noreply.github.com",
            "name": "AreteDriver",
            "username": "AreteDriver"
          },
          "distinct": true,
          "id": "2680abec5690eed42c153e14c8c9f9f7921ae6a0",
          "message": "ci: add CodeQL security scan workflow\n\nWeekly schedule + push/PR triggers on main. Python security-and-quality queries.\n\nCo-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>",
          "timestamp": "2026-02-18T04:53:05-08:00",
          "tree_id": "0263252c4bfc69317ec01871dc1a76e094fc4cbe",
          "url": "https://github.com/AreteDriver/convergent/commit/2680abec5690eed42c153e14c8c9f9f7921ae6a0"
        },
        "date": 1771419411779,
        "tool": "cargo",
        "benches": [
          {
            "name": "publish_single_intent",
            "value": 190874,
            "range": "± 2469",
            "unit": "ns/iter"
          },
          {
            "name": "publish_100_intents",
            "value": 2664769,
            "range": "± 8208",
            "unit": "ns/iter"
          },
          {
            "name": "query_all_100_intents",
            "value": 185414,
            "range": "± 3044",
            "unit": "ns/iter"
          },
          {
            "name": "resolve_with_50_existing",
            "value": 679703,
            "range": "± 7480",
            "unit": "ns/iter"
          },
          {
            "name": "find_overlapping_100_intents",
            "value": 555620,
            "range": "± 4805",
            "unit": "ns/iter"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "AreteDriver@users.noreply.github.com",
            "name": "AreteDriver",
            "username": "AreteDriver"
          },
          "committer": {
            "email": "AreteDriver@users.noreply.github.com",
            "name": "AreteDriver",
            "username": "AreteDriver"
          },
          "distinct": true,
          "id": "312738983506d4f63b12880fa742713617301eff",
          "message": "fix: resolve 3 CodeQL alerts (empty-except, string-concat, unused-global)\n\n- Add explanatory comment to ImportError catch in __init__.py\n- Wrap implicit string concatenation in visualization.py with parens\n- Remove unused _core variable in test_rust_backend.py (importorskip\n  side effect still triggers module skip)\n\nCo-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>",
          "timestamp": "2026-02-18T12:07:25-08:00",
          "tree_id": "60bbd43b5431d5e38a65f7e8112a0bae3ba07edd",
          "url": "https://github.com/AreteDriver/convergent/commit/312738983506d4f63b12880fa742713617301eff"
        },
        "date": 1771445489323,
        "tool": "cargo",
        "benches": [
          {
            "name": "publish_single_intent",
            "value": 188298,
            "range": "± 4514",
            "unit": "ns/iter"
          },
          {
            "name": "publish_100_intents",
            "value": 2804764,
            "range": "± 18282",
            "unit": "ns/iter"
          },
          {
            "name": "query_all_100_intents",
            "value": 192320,
            "range": "± 1465",
            "unit": "ns/iter"
          },
          {
            "name": "resolve_with_50_existing",
            "value": 708247,
            "range": "± 5771",
            "unit": "ns/iter"
          },
          {
            "name": "find_overlapping_100_intents",
            "value": 584605,
            "range": "± 6645",
            "unit": "ns/iter"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "AreteDriver@users.noreply.github.com",
            "name": "AreteDriver",
            "username": "AreteDriver"
          },
          "committer": {
            "email": "AreteDriver@users.noreply.github.com",
            "name": "AreteDriver",
            "username": "AreteDriver"
          },
          "distinct": true,
          "id": "58792b68b37331cd57e96ce4f188078a57d4496e",
          "message": "fix: use sys.executable for PytestGate subprocess\n\nPytestGate was running bare `pytest` which resolves to the system PATH\nrather than the current Python environment. This caused failures when\nthe system pytest couldn't find packages installed in the venv.\n\nUsing `sys.executable -m pytest` ensures the gate runs within the same\nenvironment as the caller.\n\nCo-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>",
          "timestamp": "2026-02-18T12:12:46-08:00",
          "tree_id": "6864faf01b800f439cfbb724179fed40ebf14049",
          "url": "https://github.com/AreteDriver/convergent/commit/58792b68b37331cd57e96ce4f188078a57d4496e"
        },
        "date": 1771445807865,
        "tool": "cargo",
        "benches": [
          {
            "name": "publish_single_intent",
            "value": 188350,
            "range": "± 1414",
            "unit": "ns/iter"
          },
          {
            "name": "publish_100_intents",
            "value": 2661648,
            "range": "± 64284",
            "unit": "ns/iter"
          },
          {
            "name": "query_all_100_intents",
            "value": 191061,
            "range": "± 1544",
            "unit": "ns/iter"
          },
          {
            "name": "resolve_with_50_existing",
            "value": 683764,
            "range": "± 4627",
            "unit": "ns/iter"
          },
          {
            "name": "find_overlapping_100_intents",
            "value": 559032,
            "range": "± 5103",
            "unit": "ns/iter"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "AreteDriver@users.noreply.github.com",
            "name": "AreteDriver",
            "username": "AreteDriver"
          },
          "committer": {
            "email": "AreteDriver@users.noreply.github.com",
            "name": "AreteDriver",
            "username": "AreteDriver"
          },
          "distinct": true,
          "id": "6ed6ab21229e65e9a63e7ebe75da845257d7ff71",
          "message": "chore: rename PyPI package to convergentAI\n\nThe name \"convergent\" was already taken on PyPI. Package installs as\n`pip install convergentAI` but import name remains `import convergent`.\n\nCo-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>",
          "timestamp": "2026-02-18T12:24:50-08:00",
          "tree_id": "f0211cb25e82c620befd291de068828103d69bbe",
          "url": "https://github.com/AreteDriver/convergent/commit/6ed6ab21229e65e9a63e7ebe75da845257d7ff71"
        },
        "date": 1771446541838,
        "tool": "cargo",
        "benches": [
          {
            "name": "publish_single_intent",
            "value": 227616,
            "range": "± 1409",
            "unit": "ns/iter"
          },
          {
            "name": "publish_100_intents",
            "value": 2882900,
            "range": "± 28671",
            "unit": "ns/iter"
          },
          {
            "name": "query_all_100_intents",
            "value": 194544,
            "range": "± 1258",
            "unit": "ns/iter"
          },
          {
            "name": "resolve_with_50_existing",
            "value": 749604,
            "range": "± 5194",
            "unit": "ns/iter"
          },
          {
            "name": "find_overlapping_100_intents",
            "value": 620570,
            "range": "± 4506",
            "unit": "ns/iter"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "AreteDriver@users.noreply.github.com",
            "name": "AreteDriver",
            "username": "AreteDriver"
          },
          "committer": {
            "email": "AreteDriver@users.noreply.github.com",
            "name": "AreteDriver",
            "username": "AreteDriver"
          },
          "distinct": true,
          "id": "efb695ed60586fd6a0002e77908669f78f31710b",
          "message": "feat: add health dashboard, cycle detection, and event log\n\nThree new observability modules for Phase 4:\n\n1. health.py — CoordinationHealth aggregates metrics from all subsystems\n   (intent graph, stigmergy, phi scores, voting). HealthChecker with\n   configurable grading (A-F). CLI: `convergent health <db_path>`\n\n2. cycles.py — DependencyGraph from provides/requires edges with\n   DFS-based cycle detection and Kahn's topological sort for safe\n   execution ordering. CLI: `convergent cycles <db_path>`\n\n3. event_log.py — Append-only SQLite event log for all coordination\n   events. 10 event types, correlation IDs for tracing, timeline\n   renderer. CLI: `convergent events <db_path>`\n\n60 new tests, all 887 tests passing.\n\nCo-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>",
          "timestamp": "2026-02-18T12:36:52-08:00",
          "tree_id": "f4b1180ad817df1175625ba55860381f4ebd601f",
          "url": "https://github.com/AreteDriver/convergent/commit/efb695ed60586fd6a0002e77908669f78f31710b"
        },
        "date": 1771447234980,
        "tool": "cargo",
        "benches": [
          {
            "name": "publish_single_intent",
            "value": 189723,
            "range": "± 3289",
            "unit": "ns/iter"
          },
          {
            "name": "publish_100_intents",
            "value": 2678493,
            "range": "± 10619",
            "unit": "ns/iter"
          },
          {
            "name": "query_all_100_intents",
            "value": 186223,
            "range": "± 1291",
            "unit": "ns/iter"
          },
          {
            "name": "resolve_with_50_existing",
            "value": 683825,
            "range": "± 8663",
            "unit": "ns/iter"
          },
          {
            "name": "find_overlapping_100_intents",
            "value": 560999,
            "range": "± 5424",
            "unit": "ns/iter"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "AreteDriver@users.noreply.github.com",
            "name": "AreteDriver",
            "username": "AreteDriver"
          },
          "committer": {
            "email": "AreteDriver@users.noreply.github.com",
            "name": "AreteDriver",
            "username": "AreteDriver"
          },
          "distinct": true,
          "id": "ee20372eeabc715ee522c568da50085279106379",
          "message": "chore: bump version to 1.1.0 for Phase 4 release\n\nPhase 4 modules (health dashboard, cycle detection, event log) were\nadded after v1.0.0 PyPI release. This version includes all Phase 4\nexports needed by Gorgon.\n\nCo-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>",
          "timestamp": "2026-02-18T14:32:49-08:00",
          "tree_id": "bf8a37c245a7416957ca0d81f5bdc864263a4e92",
          "url": "https://github.com/AreteDriver/convergent/commit/ee20372eeabc715ee522c568da50085279106379"
        },
        "date": 1771454199005,
        "tool": "cargo",
        "benches": [
          {
            "name": "publish_single_intent",
            "value": 230471,
            "range": "± 2261",
            "unit": "ns/iter"
          },
          {
            "name": "publish_100_intents",
            "value": 2918762,
            "range": "± 31942",
            "unit": "ns/iter"
          },
          {
            "name": "query_all_100_intents",
            "value": 195455,
            "range": "± 5741",
            "unit": "ns/iter"
          },
          {
            "name": "resolve_with_50_existing",
            "value": 743631,
            "range": "± 5631",
            "unit": "ns/iter"
          },
          {
            "name": "find_overlapping_100_intents",
            "value": 612602,
            "range": "± 4350",
            "unit": "ns/iter"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "AreteDriver",
            "username": "AreteDriver"
          },
          "committer": {
            "name": "AreteDriver",
            "username": "AreteDriver"
          },
          "id": "adbdf5028c4f8dd645c2e1a87dfa17d024dbccde",
          "message": "chore(deps): bump actions/setup-python from 5 to 6",
          "timestamp": "2026-02-18T22:33:01Z",
          "url": "https://github.com/AreteDriver/convergent/pull/17/commits/adbdf5028c4f8dd645c2e1a87dfa17d024dbccde"
        },
        "date": 1771496233595,
        "tool": "cargo",
        "benches": [
          {
            "name": "publish_single_intent",
            "value": 223111,
            "range": "± 1448",
            "unit": "ns/iter"
          },
          {
            "name": "publish_100_intents",
            "value": 2848122,
            "range": "± 15655",
            "unit": "ns/iter"
          },
          {
            "name": "query_all_100_intents",
            "value": 194422,
            "range": "± 3491",
            "unit": "ns/iter"
          },
          {
            "name": "resolve_with_50_existing",
            "value": 743688,
            "range": "± 6670",
            "unit": "ns/iter"
          },
          {
            "name": "find_overlapping_100_intents",
            "value": 615261,
            "range": "± 4801",
            "unit": "ns/iter"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "AreteDriver",
            "username": "AreteDriver"
          },
          "committer": {
            "name": "AreteDriver",
            "username": "AreteDriver"
          },
          "id": "ecfefd64594549892b08f50a317d43f02ba1f5d0",
          "message": "chore(deps): update criterion requirement from 0.5 to 0.8",
          "timestamp": "2026-02-18T22:33:01Z",
          "url": "https://github.com/AreteDriver/convergent/pull/18/commits/ecfefd64594549892b08f50a317d43f02ba1f5d0"
        },
        "date": 1771496248195,
        "tool": "cargo",
        "benches": [
          {
            "name": "publish_single_intent",
            "value": 229472,
            "range": "± 2683",
            "unit": "ns/iter"
          },
          {
            "name": "publish_100_intents",
            "value": 2915048,
            "range": "± 20621",
            "unit": "ns/iter"
          },
          {
            "name": "query_all_100_intents",
            "value": 195176,
            "range": "± 3948",
            "unit": "ns/iter"
          },
          {
            "name": "resolve_with_50_existing",
            "value": 744215,
            "range": "± 7280",
            "unit": "ns/iter"
          },
          {
            "name": "find_overlapping_100_intents",
            "value": 613831,
            "range": "± 5522",
            "unit": "ns/iter"
          }
        ]
      }
    ]
  }
}
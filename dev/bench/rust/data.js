window.BENCHMARK_DATA = {
  "lastUpdate": 1771445489694,
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
      }
    ]
  }
}
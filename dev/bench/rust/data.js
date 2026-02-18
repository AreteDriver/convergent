window.BENCHMARK_DATA = {
  "lastUpdate": 1771411022646,
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
      }
    ]
  }
}
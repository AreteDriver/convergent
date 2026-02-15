window.BENCHMARK_DATA = {
  "lastUpdate": 1771153525428,
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
      }
    ]
  }
}
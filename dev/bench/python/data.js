window.BENCHMARK_DATA = {
  "lastUpdate": 1771387352083,
  "repoUrl": "https://github.com/AreteDriver/convergent",
  "entries": {
    "Python Benchmarks": [
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
        "date": 1771153523785,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::TestResolverBenchmark::test_resolve_50_intents",
            "value": 698.578656639649,
            "unit": "iter/sec",
            "range": "stddev: 0.00003873117349186626",
            "extra": "mean: 1.431478031135776 msec\nrounds: 546"
          },
          {
            "name": "tests/test_benchmarks.py::TestStructuralOverlapBenchmark::test_structural_overlaps_1000",
            "value": 294.131595110745,
            "unit": "iter/sec",
            "range": "stddev: 0.000034737589939749534",
            "extra": "mean: 3.399838768165945 msec\nrounds: 289"
          },
          {
            "name": "tests/test_benchmarks.py::TestConstraintBenchmark::test_validate_20_constraints",
            "value": 181648.98179041554,
            "unit": "iter/sec",
            "range": "stddev: 7.408721760283672e-7",
            "extra": "mean: 5.505123068368136 usec\nrounds: 59341"
          },
          {
            "name": "tests/test_benchmarks.py::TestPhiScoringBenchmark::test_phi_score_100_outcomes",
            "value": 85015.90310372187,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014270166261356388",
            "extra": "mean: 11.762505172473096 usec\nrounds: 46883"
          },
          {
            "name": "tests/test_benchmarks.py::TestRealisticScenarioBenchmark::test_realistic_25_agents",
            "value": 200.01983863434577,
            "unit": "iter/sec",
            "range": "stddev: 0.00010623327629948574",
            "extra": "mean: 4.999504083332902 msec\nrounds: 144"
          },
          {
            "name": "tests/test_benchmarks.py::TestPublishThroughputBenchmark::test_publish_100_intents",
            "value": 773.7689409931015,
            "unit": "iter/sec",
            "range": "stddev: 0.0006233565004004226",
            "extra": "mean: 1.2923754715671838 msec\nrounds: 721"
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
        "date": 1771386633280,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::TestResolverBenchmark::test_resolve_50_intents",
            "value": 692.3910460216171,
            "unit": "iter/sec",
            "range": "stddev: 0.00003132495568336801",
            "extra": "mean: 1.4442705545455294 msec\nrounds: 550"
          },
          {
            "name": "tests/test_benchmarks.py::TestStructuralOverlapBenchmark::test_structural_overlaps_1000",
            "value": 284.5672774769823,
            "unit": "iter/sec",
            "range": "stddev: 0.00003066544671312139",
            "extra": "mean: 3.514107485815499 msec\nrounds: 282"
          },
          {
            "name": "tests/test_benchmarks.py::TestConstraintBenchmark::test_validate_20_constraints",
            "value": 184562.62493040887,
            "unit": "iter/sec",
            "range": "stddev: 7.27484945249753e-7",
            "extra": "mean: 5.418215092991117 usec\nrounds: 58133"
          },
          {
            "name": "tests/test_benchmarks.py::TestPhiScoringBenchmark::test_phi_score_100_outcomes",
            "value": 86557.91249651561,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012648451664017845",
            "extra": "mean: 11.552958835973028 usec\nrounds: 46424"
          },
          {
            "name": "tests/test_benchmarks.py::TestRealisticScenarioBenchmark::test_realistic_25_agents",
            "value": 196.6032124321631,
            "unit": "iter/sec",
            "range": "stddev: 0.0001723655077838174",
            "extra": "mean: 5.086386878571706 msec\nrounds: 140"
          },
          {
            "name": "tests/test_benchmarks.py::TestPublishThroughputBenchmark::test_publish_100_intents",
            "value": 771.1334423413986,
            "unit": "iter/sec",
            "range": "stddev: 0.000493311643725946",
            "extra": "mean: 1.2967924163212168 msec\nrounds: 723"
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
        "date": 1771387351292,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::TestResolverBenchmark::test_resolve_50_intents",
            "value": 716.8252377664127,
            "unit": "iter/sec",
            "range": "stddev: 0.000018066559773977764",
            "extra": "mean: 1.3950401678321818 msec\nrounds: 572"
          },
          {
            "name": "tests/test_benchmarks.py::TestStructuralOverlapBenchmark::test_structural_overlaps_1000",
            "value": 285.7742169385381,
            "unit": "iter/sec",
            "range": "stddev: 0.000019984213514050977",
            "extra": "mean: 3.499265996466965 msec\nrounds: 283"
          },
          {
            "name": "tests/test_benchmarks.py::TestConstraintBenchmark::test_validate_20_constraints",
            "value": 203764.15324518672,
            "unit": "iter/sec",
            "range": "stddev: 4.946138520985728e-7",
            "extra": "mean: 4.90763455727521 usec\nrounds: 64467"
          },
          {
            "name": "tests/test_benchmarks.py::TestPhiScoringBenchmark::test_phi_score_100_outcomes",
            "value": 108877.70929781235,
            "unit": "iter/sec",
            "range": "stddev: 7.386730592592461e-7",
            "extra": "mean: 9.184616451331722 usec\nrounds: 52713"
          },
          {
            "name": "tests/test_benchmarks.py::TestRealisticScenarioBenchmark::test_realistic_25_agents",
            "value": 216.35092969260694,
            "unit": "iter/sec",
            "range": "stddev: 0.000040347275775036276",
            "extra": "mean: 4.622120188809947 msec\nrounds: 143"
          },
          {
            "name": "tests/test_benchmarks.py::TestPublishThroughputBenchmark::test_publish_100_intents",
            "value": 863.8944969580501,
            "unit": "iter/sec",
            "range": "stddev: 0.000860817259005264",
            "extra": "mean: 1.1575487556885768 msec\nrounds: 835"
          }
        ]
      }
    ]
  }
}
window.BENCHMARK_DATA = {
  "lastUpdate": 1771445806739,
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
        "date": 1771411020675,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::TestResolverBenchmark::test_resolve_50_intents",
            "value": 693.6406729640898,
            "unit": "iter/sec",
            "range": "stddev: 0.000026280379327719",
            "extra": "mean: 1.441668631867801 msec\nrounds: 546"
          },
          {
            "name": "tests/test_benchmarks.py::TestStructuralOverlapBenchmark::test_structural_overlaps_1000",
            "value": 292.1337430025628,
            "unit": "iter/sec",
            "range": "stddev: 0.00005004370319494656",
            "extra": "mean: 3.4230896770840578 msec\nrounds: 288"
          },
          {
            "name": "tests/test_benchmarks.py::TestConstraintBenchmark::test_validate_20_constraints",
            "value": 185809.29705200644,
            "unit": "iter/sec",
            "range": "stddev: 7.547838758558861e-7",
            "extra": "mean: 5.381862026635344 usec\nrounds: 56105"
          },
          {
            "name": "tests/test_benchmarks.py::TestPhiScoringBenchmark::test_phi_score_100_outcomes",
            "value": 86912.15321168404,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010656041701074397",
            "extra": "mean: 11.505870733226352 usec\nrounds: 43739"
          },
          {
            "name": "tests/test_benchmarks.py::TestRealisticScenarioBenchmark::test_realistic_25_agents",
            "value": 199.38273278510394,
            "unit": "iter/sec",
            "range": "stddev: 0.000041665744905762495",
            "extra": "mean: 5.015479455173316 msec\nrounds: 145"
          },
          {
            "name": "tests/test_benchmarks.py::TestPublishThroughputBenchmark::test_publish_100_intents",
            "value": 747.8509185526583,
            "unit": "iter/sec",
            "range": "stddev: 0.0007104754567489636",
            "extra": "mean: 1.3371649017097345 msec\nrounds: 702"
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
        "date": 1771419410146,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::TestResolverBenchmark::test_resolve_50_intents",
            "value": 714.1125276110146,
            "unit": "iter/sec",
            "range": "stddev: 0.000012688692399760322",
            "extra": "mean: 1.4003395282048765 msec\nrounds: 585"
          },
          {
            "name": "tests/test_benchmarks.py::TestStructuralOverlapBenchmark::test_structural_overlaps_1000",
            "value": 285.44391266801887,
            "unit": "iter/sec",
            "range": "stddev: 0.00005470201908203388",
            "extra": "mean: 3.5033152070159383 msec\nrounds: 285"
          },
          {
            "name": "tests/test_benchmarks.py::TestConstraintBenchmark::test_validate_20_constraints",
            "value": 201373.17705924556,
            "unit": "iter/sec",
            "range": "stddev: 6.577300767782243e-7",
            "extra": "mean: 4.965904668156436 usec\nrounds: 58354"
          },
          {
            "name": "tests/test_benchmarks.py::TestPhiScoringBenchmark::test_phi_score_100_outcomes",
            "value": 109340.65344582143,
            "unit": "iter/sec",
            "range": "stddev: 6.560436362542127e-7",
            "extra": "mean: 9.145729136286006 usec\nrounds: 53226"
          },
          {
            "name": "tests/test_benchmarks.py::TestRealisticScenarioBenchmark::test_realistic_25_agents",
            "value": 216.44633372797486,
            "unit": "iter/sec",
            "range": "stddev: 0.00003957335926727695",
            "extra": "mean: 4.620082875863256 msec\nrounds: 145"
          },
          {
            "name": "tests/test_benchmarks.py::TestPublishThroughputBenchmark::test_publish_100_intents",
            "value": 868.1612995371156,
            "unit": "iter/sec",
            "range": "stddev: 0.0007555154391481057",
            "extra": "mean: 1.1518596838319997 msec\nrounds: 835"
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
        "date": 1771445487457,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::TestResolverBenchmark::test_resolve_50_intents",
            "value": 725.0017119719123,
            "unit": "iter/sec",
            "range": "stddev: 0.000017635979423876467",
            "extra": "mean: 1.3793070878138032 msec\nrounds: 558"
          },
          {
            "name": "tests/test_benchmarks.py::TestStructuralOverlapBenchmark::test_structural_overlaps_1000",
            "value": 294.4117272466849,
            "unit": "iter/sec",
            "range": "stddev: 0.00006567930944369878",
            "extra": "mean: 3.396603828767015 msec\nrounds: 292"
          },
          {
            "name": "tests/test_benchmarks.py::TestConstraintBenchmark::test_validate_20_constraints",
            "value": 185413.22409391913,
            "unit": "iter/sec",
            "range": "stddev: 7.796216009574289e-7",
            "extra": "mean: 5.393358563753039 usec\nrounds: 54894"
          },
          {
            "name": "tests/test_benchmarks.py::TestPhiScoringBenchmark::test_phi_score_100_outcomes",
            "value": 86639.20613619265,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012172446552035745",
            "extra": "mean: 11.542118685021748 usec\nrounds: 44319"
          },
          {
            "name": "tests/test_benchmarks.py::TestRealisticScenarioBenchmark::test_realistic_25_agents",
            "value": 213.75779014280127,
            "unit": "iter/sec",
            "range": "stddev: 0.000043606931872120324",
            "extra": "mean: 4.678192075862818 msec\nrounds: 145"
          },
          {
            "name": "tests/test_benchmarks.py::TestPublishThroughputBenchmark::test_publish_100_intents",
            "value": 775.4362065361179,
            "unit": "iter/sec",
            "range": "stddev: 0.0007134213127240967",
            "extra": "mean: 1.2895967348068658 msec\nrounds: 724"
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
        "date": 1771445805931,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::TestResolverBenchmark::test_resolve_50_intents",
            "value": 709.4616486889983,
            "unit": "iter/sec",
            "range": "stddev: 0.00005200619468759187",
            "extra": "mean: 1.4095194600693108 msec\nrounds: 576"
          },
          {
            "name": "tests/test_benchmarks.py::TestStructuralOverlapBenchmark::test_structural_overlaps_1000",
            "value": 283.18934265903437,
            "unit": "iter/sec",
            "range": "stddev: 0.000024504668387848643",
            "extra": "mean: 3.531206332167733 msec\nrounds: 286"
          },
          {
            "name": "tests/test_benchmarks.py::TestConstraintBenchmark::test_validate_20_constraints",
            "value": 192686.87011819854,
            "unit": "iter/sec",
            "range": "stddev: 4.552206806782281e-7",
            "extra": "mean: 5.189767208251278 usec\nrounds: 64809"
          },
          {
            "name": "tests/test_benchmarks.py::TestPhiScoringBenchmark::test_phi_score_100_outcomes",
            "value": 107393.85096208635,
            "unit": "iter/sec",
            "range": "stddev: 8.041017788295653e-7",
            "extra": "mean: 9.311520082774885 usec\nrounds: 52184"
          },
          {
            "name": "tests/test_benchmarks.py::TestRealisticScenarioBenchmark::test_realistic_25_agents",
            "value": 215.35736232455807,
            "unit": "iter/sec",
            "range": "stddev: 0.00024177661905041596",
            "extra": "mean: 4.643444687500085 msec\nrounds: 144"
          },
          {
            "name": "tests/test_benchmarks.py::TestPublishThroughputBenchmark::test_publish_100_intents",
            "value": 867.1071904991239,
            "unit": "iter/sec",
            "range": "stddev: 0.0007872157247968101",
            "extra": "mean: 1.1532599555821703 msec\nrounds: 833"
          }
        ]
      }
    ]
  }
}
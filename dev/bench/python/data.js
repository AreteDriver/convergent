window.BENCHMARK_DATA = {
  "lastUpdate": 1771496824319,
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
        "date": 1771446539116,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::TestResolverBenchmark::test_resolve_50_intents",
            "value": 686.3318744716147,
            "unit": "iter/sec",
            "range": "stddev: 0.000023198915834386603",
            "extra": "mean: 1.4570210669144115 msec\nrounds: 538"
          },
          {
            "name": "tests/test_benchmarks.py::TestStructuralOverlapBenchmark::test_structural_overlaps_1000",
            "value": 283.1169468254031,
            "unit": "iter/sec",
            "range": "stddev: 0.000030441612659551457",
            "extra": "mean: 3.5321092969284367 msec\nrounds: 293"
          },
          {
            "name": "tests/test_benchmarks.py::TestConstraintBenchmark::test_validate_20_constraints",
            "value": 184966.56172930263,
            "unit": "iter/sec",
            "range": "stddev: 9.649372192317212e-7",
            "extra": "mean: 5.40638259505247 usec\nrounds: 55513"
          },
          {
            "name": "tests/test_benchmarks.py::TestPhiScoringBenchmark::test_phi_score_100_outcomes",
            "value": 86266.93311204808,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010153199642717193",
            "extra": "mean: 11.591927102603112 usec\nrounds: 44981"
          },
          {
            "name": "tests/test_benchmarks.py::TestRealisticScenarioBenchmark::test_realistic_25_agents",
            "value": 198.0500120140362,
            "unit": "iter/sec",
            "range": "stddev: 0.00006303551188893797",
            "extra": "mean: 5.049229686131643 msec\nrounds: 137"
          },
          {
            "name": "tests/test_benchmarks.py::TestPublishThroughputBenchmark::test_publish_100_intents",
            "value": 761.8028845818483,
            "unit": "iter/sec",
            "range": "stddev: 0.0008858255023475879",
            "extra": "mean: 1.3126755230769407 msec\nrounds: 715"
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
        "date": 1771447232595,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::TestResolverBenchmark::test_resolve_50_intents",
            "value": 717.5380464992984,
            "unit": "iter/sec",
            "range": "stddev: 0.00005946551765636279",
            "extra": "mean: 1.3936543224136588 msec\nrounds: 580"
          },
          {
            "name": "tests/test_benchmarks.py::TestStructuralOverlapBenchmark::test_structural_overlaps_1000",
            "value": 284.4959228054823,
            "unit": "iter/sec",
            "range": "stddev: 0.00031833139063418053",
            "extra": "mean: 3.514988862190927 msec\nrounds: 283"
          },
          {
            "name": "tests/test_benchmarks.py::TestConstraintBenchmark::test_validate_20_constraints",
            "value": 204446.49553877857,
            "unit": "iter/sec",
            "range": "stddev: 4.900252125945747e-7",
            "extra": "mean: 4.891255276177253 usec\nrounds: 66904"
          },
          {
            "name": "tests/test_benchmarks.py::TestPhiScoringBenchmark::test_phi_score_100_outcomes",
            "value": 106910.65493178295,
            "unit": "iter/sec",
            "range": "stddev: 7.949305254265662e-7",
            "extra": "mean: 9.35360465837643 usec\nrounds: 51563"
          },
          {
            "name": "tests/test_benchmarks.py::TestRealisticScenarioBenchmark::test_realistic_25_agents",
            "value": 218.3674080337407,
            "unit": "iter/sec",
            "range": "stddev: 0.000035408427040012344",
            "extra": "mean: 4.579437971098171 msec\nrounds: 173"
          },
          {
            "name": "tests/test_benchmarks.py::TestPublishThroughputBenchmark::test_publish_100_intents",
            "value": 870.5739716571129,
            "unit": "iter/sec",
            "range": "stddev: 0.0008342045263569248",
            "extra": "mean: 1.1486674683100486 msec\nrounds: 852"
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
        "date": 1771454197536,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::TestResolverBenchmark::test_resolve_50_intents",
            "value": 678.0886466430062,
            "unit": "iter/sec",
            "range": "stddev: 0.00015305800054439124",
            "extra": "mean: 1.4747334363297055 msec\nrounds: 534"
          },
          {
            "name": "tests/test_benchmarks.py::TestStructuralOverlapBenchmark::test_structural_overlaps_1000",
            "value": 290.2268219085776,
            "unit": "iter/sec",
            "range": "stddev: 0.00008352935778060222",
            "extra": "mean: 3.4455809198606846 msec\nrounds: 287"
          },
          {
            "name": "tests/test_benchmarks.py::TestConstraintBenchmark::test_validate_20_constraints",
            "value": 182060.85014130766,
            "unit": "iter/sec",
            "range": "stddev: 7.516129784403301e-7",
            "extra": "mean: 5.492669067643284 usec\nrounds: 54422"
          },
          {
            "name": "tests/test_benchmarks.py::TestPhiScoringBenchmark::test_phi_score_100_outcomes",
            "value": 80425.5885303748,
            "unit": "iter/sec",
            "range": "stddev: 0.000002861123781370302",
            "extra": "mean: 12.43385368106227 usec\nrounds: 37924"
          },
          {
            "name": "tests/test_benchmarks.py::TestRealisticScenarioBenchmark::test_realistic_25_agents",
            "value": 200.13510414522335,
            "unit": "iter/sec",
            "range": "stddev: 0.00005732604578794336",
            "extra": "mean: 4.996624676470418 msec\nrounds: 170"
          },
          {
            "name": "tests/test_benchmarks.py::TestPublishThroughputBenchmark::test_publish_100_intents",
            "value": 742.2405811778331,
            "unit": "iter/sec",
            "range": "stddev: 0.0008152645280544588",
            "extra": "mean: 1.3472720642855964 msec\nrounds: 700"
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
        "date": 1771496231623,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::TestResolverBenchmark::test_resolve_50_intents",
            "value": 713.8560835479981,
            "unit": "iter/sec",
            "range": "stddev: 0.000021253332060601416",
            "extra": "mean: 1.4008425830453293 msec\nrounds: 578"
          },
          {
            "name": "tests/test_benchmarks.py::TestStructuralOverlapBenchmark::test_structural_overlaps_1000",
            "value": 298.20199510057915,
            "unit": "iter/sec",
            "range": "stddev: 0.00003967346024424858",
            "extra": "mean: 3.353431621618476 msec\nrounds: 296"
          },
          {
            "name": "tests/test_benchmarks.py::TestConstraintBenchmark::test_validate_20_constraints",
            "value": 183424.54356474717,
            "unit": "iter/sec",
            "range": "stddev: 7.61946077237772e-7",
            "extra": "mean: 5.451833111128933 usec\nrounds: 63012"
          },
          {
            "name": "tests/test_benchmarks.py::TestPhiScoringBenchmark::test_phi_score_100_outcomes",
            "value": 86970.52340059265,
            "unit": "iter/sec",
            "range": "stddev: 9.926809001579043e-7",
            "extra": "mean: 11.498148578385877 usec\nrounds: 47941"
          },
          {
            "name": "tests/test_benchmarks.py::TestRealisticScenarioBenchmark::test_realistic_25_agents",
            "value": 202.12476894515152,
            "unit": "iter/sec",
            "range": "stddev: 0.00011586927227079629",
            "extra": "mean: 4.947439174420823 msec\nrounds: 172"
          },
          {
            "name": "tests/test_benchmarks.py::TestPublishThroughputBenchmark::test_publish_100_intents",
            "value": 777.764068279721,
            "unit": "iter/sec",
            "range": "stddev: 0.00046935488211779966",
            "extra": "mean: 1.2857369487534007 msec\nrounds: 722"
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
        "date": 1771496246809,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::TestResolverBenchmark::test_resolve_50_intents",
            "value": 682.3550442277856,
            "unit": "iter/sec",
            "range": "stddev: 0.00016293599549666252",
            "extra": "mean: 1.4655127245841495 msec\nrounds: 541"
          },
          {
            "name": "tests/test_benchmarks.py::TestStructuralOverlapBenchmark::test_structural_overlaps_1000",
            "value": 280.3248379259911,
            "unit": "iter/sec",
            "range": "stddev: 0.0003106639011603401",
            "extra": "mean: 3.5672900318023593 msec\nrounds: 283"
          },
          {
            "name": "tests/test_benchmarks.py::TestConstraintBenchmark::test_validate_20_constraints",
            "value": 181096.66675703684,
            "unit": "iter/sec",
            "range": "stddev: 6.767310087327178e-7",
            "extra": "mean: 5.521912787835137 usec\nrounds: 55451"
          },
          {
            "name": "tests/test_benchmarks.py::TestPhiScoringBenchmark::test_phi_score_100_outcomes",
            "value": 86100.93257712279,
            "unit": "iter/sec",
            "range": "stddev: 0.000001010417888804579",
            "extra": "mean: 11.614276060300213 usec\nrounds: 45577"
          },
          {
            "name": "tests/test_benchmarks.py::TestRealisticScenarioBenchmark::test_realistic_25_agents",
            "value": 200.37135162407458,
            "unit": "iter/sec",
            "range": "stddev: 0.00008616092915681991",
            "extra": "mean: 4.990733415204702 msec\nrounds: 171"
          },
          {
            "name": "tests/test_benchmarks.py::TestPublishThroughputBenchmark::test_publish_100_intents",
            "value": 758.9423993045624,
            "unit": "iter/sec",
            "range": "stddev: 0.000737965397727109",
            "extra": "mean: 1.3176230513887808 msec\nrounds: 720"
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
          "id": "936184220292d08fe4a501a31ac542ab615bbc21",
          "message": "chore(deps): bump actions/checkout from 4 to 6",
          "timestamp": "2026-02-18T22:33:01Z",
          "url": "https://github.com/AreteDriver/convergent/pull/19/commits/936184220292d08fe4a501a31ac542ab615bbc21"
        },
        "date": 1771496249407,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::TestResolverBenchmark::test_resolve_50_intents",
            "value": 690.7862108519791,
            "unit": "iter/sec",
            "range": "stddev: 0.00015357738993023747",
            "extra": "mean: 1.4476258852455277 msec\nrounds: 549"
          },
          {
            "name": "tests/test_benchmarks.py::TestStructuralOverlapBenchmark::test_structural_overlaps_1000",
            "value": 287.9187100226192,
            "unit": "iter/sec",
            "range": "stddev: 0.000038864850988340606",
            "extra": "mean: 3.473202557490755 msec\nrounds: 287"
          },
          {
            "name": "tests/test_benchmarks.py::TestConstraintBenchmark::test_validate_20_constraints",
            "value": 179928.514307102,
            "unit": "iter/sec",
            "range": "stddev: 7.187267815569928e-7",
            "extra": "mean: 5.557762780685223 usec\nrounds: 55885"
          },
          {
            "name": "tests/test_benchmarks.py::TestPhiScoringBenchmark::test_phi_score_100_outcomes",
            "value": 79383.88898853445,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010988057720230153",
            "extra": "mean: 12.597014491749473 usec\nrounds: 43473"
          },
          {
            "name": "tests/test_benchmarks.py::TestRealisticScenarioBenchmark::test_realistic_25_agents",
            "value": 201.68125409094586,
            "unit": "iter/sec",
            "range": "stddev: 0.000041047486250654665",
            "extra": "mean: 4.958319029239384 msec\nrounds: 171"
          },
          {
            "name": "tests/test_benchmarks.py::TestPublishThroughputBenchmark::test_publish_100_intents",
            "value": 766.031513283985,
            "unit": "iter/sec",
            "range": "stddev: 0.0006732895046046035",
            "extra": "mean: 1.305429323283307 msec\nrounds: 597"
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
          "id": "a51d0eb160eacdbbdfb6defe2eca02d201cf93c0",
          "message": "chore(deps): bump actions/setup-python from 5 to 6",
          "timestamp": "2026-02-19T10:16:47Z",
          "url": "https://github.com/AreteDriver/convergent/pull/17/commits/a51d0eb160eacdbbdfb6defe2eca02d201cf93c0"
        },
        "date": 1771496483026,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::TestResolverBenchmark::test_resolve_50_intents",
            "value": 706.0695464303462,
            "unit": "iter/sec",
            "range": "stddev: 0.000024228210181918442",
            "extra": "mean: 1.416291079335837 msec\nrounds: 542"
          },
          {
            "name": "tests/test_benchmarks.py::TestStructuralOverlapBenchmark::test_structural_overlaps_1000",
            "value": 298.042055787677,
            "unit": "iter/sec",
            "range": "stddev: 0.0002673619687924261",
            "extra": "mean: 3.35523118493181 msec\nrounds: 292"
          },
          {
            "name": "tests/test_benchmarks.py::TestConstraintBenchmark::test_validate_20_constraints",
            "value": 180217.61340668207,
            "unit": "iter/sec",
            "range": "stddev: 7.803683686642275e-7",
            "extra": "mean: 5.548847202539428 usec\nrounds: 53548"
          },
          {
            "name": "tests/test_benchmarks.py::TestPhiScoringBenchmark::test_phi_score_100_outcomes",
            "value": 85538.70945306234,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012745904946448732",
            "extra": "mean: 11.690613599317043 usec\nrounds: 44679"
          },
          {
            "name": "tests/test_benchmarks.py::TestRealisticScenarioBenchmark::test_realistic_25_agents",
            "value": 198.72339640659592,
            "unit": "iter/sec",
            "range": "stddev: 0.0000630859646357813",
            "extra": "mean: 5.032120113094083 msec\nrounds: 168"
          },
          {
            "name": "tests/test_benchmarks.py::TestPublishThroughputBenchmark::test_publish_100_intents",
            "value": 733.2711430280538,
            "unit": "iter/sec",
            "range": "stddev: 0.0009020550131041566",
            "extra": "mean: 1.3637520165739587 msec\nrounds: 724"
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
          "id": "cfc1e28cf0be24b7cf9180aa0d80b34b1752cc32",
          "message": "test: push coverage 97% → 98% with 19 targeted tests\n\nCover previously-uncovered edge cases:\n- resolver.py: low-stability skip, semantic conflicts, structural/semantic\n  constraint conflicts (lines 74, 273, 309-310, 355-356)\n- health.py: same-agent skip, low stability, low marker strength, high\n  escalation rate issues (lines 163, 173, 212, 295)\n- governor.py: HARD_FAIL in evaluate_publish (lines 195-196)\n- scoring.py: naive datetime UTC normalization (line 180)\n- signal_backend.py: path traversal guard (line 131)\n- stigmergy.py: naive datetime UTC normalization (line 213)\n- intent.py: Evidence.to_dict() (line 134)\n- constraints.py: TypedConstraint.to_base, GateResult properties (84, 122, 126)\n- economics.py: non-zero rate/cost, AUTO_RESOLVE savings (145, 305, 313)\n\nAlso add poetry.lock to .gitignore (library shouldn't commit lock files).\n\n27/36 modules now at 100% coverage. Remaining gaps:\n- rust_backend.py (89%): PyO3 import guards require compiled Rust\n- flocking.py (99%): unreachable defensive guard (union==0 after empty check)\n\n906 tests, 98% coverage, all passing.\n\nCo-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>",
          "timestamp": "2026-02-19T02:23:12-08:00",
          "tree_id": "172b6a69671d5a7c599bd0a4744acf80fa1f1b09",
          "url": "https://github.com/AreteDriver/convergent/commit/cfc1e28cf0be24b7cf9180aa0d80b34b1752cc32"
        },
        "date": 1771496823850,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_benchmarks.py::TestResolverBenchmark::test_resolve_50_intents",
            "value": 672.7490145795553,
            "unit": "iter/sec",
            "range": "stddev: 0.00019216243695496018",
            "extra": "mean: 1.486438446327514 msec\nrounds: 531"
          },
          {
            "name": "tests/test_benchmarks.py::TestStructuralOverlapBenchmark::test_structural_overlaps_1000",
            "value": 285.87638507709056,
            "unit": "iter/sec",
            "range": "stddev: 0.000051908231415921634",
            "extra": "mean: 3.498015408759055 msec\nrounds: 274"
          },
          {
            "name": "tests/test_benchmarks.py::TestConstraintBenchmark::test_validate_20_constraints",
            "value": 182057.30099473064,
            "unit": "iter/sec",
            "range": "stddev: 7.49938434266945e-7",
            "extra": "mean: 5.4927761454012956 usec\nrounds: 56358"
          },
          {
            "name": "tests/test_benchmarks.py::TestPhiScoringBenchmark::test_phi_score_100_outcomes",
            "value": 86247.13298319974,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011786533442679233",
            "extra": "mean: 11.594588311646163 usec\nrounds: 43171"
          },
          {
            "name": "tests/test_benchmarks.py::TestRealisticScenarioBenchmark::test_realistic_25_agents",
            "value": 194.9152448055643,
            "unit": "iter/sec",
            "range": "stddev: 0.000580754179008558",
            "extra": "mean: 5.130435030864517 msec\nrounds: 162"
          },
          {
            "name": "tests/test_benchmarks.py::TestPublishThroughputBenchmark::test_publish_100_intents",
            "value": 748.4980793475669,
            "unit": "iter/sec",
            "range": "stddev: 0.0010780381360457197",
            "extra": "mean: 1.3360087722224436 msec\nrounds: 720"
          }
        ]
      }
    ]
  }
}
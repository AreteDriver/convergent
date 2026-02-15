use criterion::{black_box, criterion_group, criterion_main, Criterion};

use convergent_core::graph::IntentGraph;
use convergent_core::models::{IntentNode, InterfaceKind, InterfaceSpec};

fn make_intent(agent_id: &str, name: &str, provides: Vec<&str>, requires: Vec<&str>) -> IntentNode {
    IntentNode::new(agent_id, &format!("Implement {}", name))
        .with_provides(
            provides
                .into_iter()
                .map(|n| {
                    InterfaceSpec::new(n, InterfaceKind::Function, "(x: str) -> str")
                        .with_tags(vec!["api", "benchmark"])
                })
                .collect(),
        )
        .with_requires(
            requires
                .into_iter()
                .map(|n| {
                    InterfaceSpec::new(n, InterfaceKind::Function, "(x: str) -> str")
                        .with_tags(vec!["api", "benchmark"])
                })
                .collect(),
        )
        .with_stability(0.7)
}

fn bench_publish(c: &mut Criterion) {
    c.bench_function("publish_single_intent", |b| {
        b.iter(|| {
            let graph = IntentGraph::in_memory().unwrap();
            let intent = make_intent("agent_1", "service_a", vec!["output_a"], vec!["input_a"]);
            graph.publish(black_box(&intent)).unwrap()
        });
    });

    c.bench_function("publish_100_intents", |b| {
        b.iter(|| {
            let graph = IntentGraph::in_memory().unwrap();
            for i in 0..100 {
                let intent = make_intent(
                    &format!("agent_{}", i),
                    &format!("service_{}", i),
                    vec![Box::leak(format!("provide_{}", i).into_boxed_str())],
                    vec![Box::leak(format!("require_{}", i % 5).into_boxed_str())],
                );
                graph.publish(&intent).unwrap();
            }
        });
    });
}

fn bench_query_all(c: &mut Criterion) {
    c.bench_function("query_all_100_intents", |b| {
        let graph = IntentGraph::in_memory().unwrap();
        for i in 0..100 {
            let intent = make_intent(
                &format!("agent_{}", i),
                &format!("service_{}", i),
                vec![Box::leak(format!("provide_{}", i).into_boxed_str())],
                vec![Box::leak(format!("require_{}", i % 5).into_boxed_str())],
            );
            graph.publish(&intent).unwrap();
        }

        b.iter(|| graph.query_all(black_box(None)).unwrap());
    });
}

fn bench_resolve(c: &mut Criterion) {
    c.bench_function("resolve_with_50_existing", |b| {
        let graph = IntentGraph::in_memory().unwrap();
        for i in 0..50 {
            let intent = make_intent(
                &format!("agent_{}", i),
                &format!("service_{}", i),
                vec![Box::leak(format!("provide_{}", i).into_boxed_str())],
                vec![Box::leak(format!("require_{}", i % 5).into_boxed_str())],
            );
            graph.publish(&intent).unwrap();
        }

        let new_intent = make_intent(
            "agent_new",
            "new_service",
            vec!["provide_0"],
            vec!["require_99"],
        );

        b.iter(|| {
            graph
                .resolve(black_box(&new_intent), black_box(0.0))
                .unwrap()
        });
    });
}

fn bench_find_overlapping(c: &mut Criterion) {
    c.bench_function("find_overlapping_100_intents", |b| {
        let graph = IntentGraph::in_memory().unwrap();
        for i in 0..100 {
            let intent = make_intent(
                &format!("agent_{}", i),
                &format!("service_{}", i),
                vec![Box::leak(format!("provide_{}", i % 10).into_boxed_str())],
                vec![Box::leak(format!("require_{}", i % 5).into_boxed_str())],
            );
            graph.publish(&intent).unwrap();
        }

        let specs =
            vec![
                InterfaceSpec::new("provide_0", InterfaceKind::Function, "(x: str) -> str")
                    .with_tags(vec!["api", "benchmark"]),
            ];

        b.iter(|| {
            graph
                .find_overlapping(black_box(&specs), black_box("agent_new"), black_box(0.0))
                .unwrap()
        });
    });
}

criterion_group!(
    benches,
    bench_publish,
    bench_query_all,
    bench_resolve,
    bench_find_overlapping
);
criterion_main!(benches);

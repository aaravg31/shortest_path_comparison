"""
Runtime Benchmark: Dijkstra's Algorithm with Different Heaps

Compares performance of BinaryHeap, PairingHeap, and FibonacciHeap
on randomly generated sparse graphs of increasing size.

Outputs
-------
- Console table of runtimes (seconds)
- Matplotlib line chart (runtime vs number of nodes)
- Saved PNG plot ("runtime_comparison.png")

Notes
-----
- Uses tqdm (from util.generate_graph) for progress tracking.
- Graphs are directed with random positive weights.
"""

import time
import matplotlib.pyplot as plt
from src.algorithms.dijkstra import dijkstra
from src.utils.graph_generator import generate_graph


def benchmark_dijkstra():
    """Run Dijkstra on multiple graph sizes and heap types, record runtimes."""
    heap_types = ["binary", "radix", "fibonacci"]

    # Graph sizes: (num_nodes, avg_edges_per_node)
    
    # For peer review testing:
    # Use smaller graphs first if runtime or memory is limited (uncomment and comment sizes accordingly):
    graph_sizes = [
        (10_000, 8),
        (50_000, 10),
        #(100_000, 12),
        #(500_000, 15),
        #(1_000_000, 20),
        #(2_000_000, 25),
    ]

    results = {heap: [] for heap in heap_types}

    for num_nodes, avg_edges in graph_sizes:
        num_edges = avg_edges * num_nodes
        print(f"\n🔹 Benchmarking graph with {num_nodes} nodes and ~{num_edges} edges")

        # Generate graph (progress shown via tqdm)
        graph = generate_graph(num_nodes, num_edges, seed=42, show_progress=True)

        # Run Dijkstra for each heap type
        for heap_type in heap_types:
            print(f"   ▶ Running Dijkstra with {heap_type.title()} Heap...", end=" ", flush=True)
            start = time.perf_counter()
            dijkstra(graph, source=0, heap_type=heap_type)
            end = time.perf_counter()

            runtime = end - start
            results[heap_type].append(runtime)
            print(f"done in {runtime:.2f}s")

    return graph_sizes, results


def plot_results(graph_sizes, results):
    """Plot runtime vs graph size for each heap with custom colors."""
    plt.figure(figsize=(8, 5))
    x = [n for n, _ in graph_sizes]

    colors = {
        "binary": "#1f77b4",
        "radix": "#e377c2",
        "fibonacci": "#9467bd"
    }

    for heap_type, runtimes in results.items():
        plt.plot(
            x, runtimes, marker='o', label=f"{heap_type.title()} Heap",
            color=colors.get(heap_type, None), linewidth=2
        )

    plt.xlabel("Number of Nodes")
    plt.ylabel("Runtime (seconds)")
    plt.title("Dijkstra Runtime Comparison: Different Heaps")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig("latex/plots/runtime_comparison.png", dpi=300)
    plt.show()



if __name__ == "__main__":
    sizes, results = benchmark_dijkstra()
    plot_results(sizes, results)

"""
Runtime Benchmark: Dijkstra's Algorithm with Different Heaps

Compares performance of BinaryHeap, RadixHeap, and FibonacciHeap
on randomly generated sparse graphs of increasing size.

Outputs
-------
- Console table of runtimes (seconds) and peak memory (MiB)
- Matplotlib line chart: runtime vs number of nodes
- Matplotlib line chart: peak memory vs number of nodes
- Saved PNG plots:
    - "latex/plots/runtime_comparison.png"
    - "latex/plots/memory_comparison.png"

Notes
-----
- Uses tqdm (from util.graph_generator) for progress tracking.
- Graphs are directed with random positive weights.
- Memory usage is measured with tracemalloc, which works on macOS.
"""

import time
import tracemalloc
import matplotlib.pyplot as plt

from src.algorithms.dijkstra import dijkstra
from src.utils.graph_generator import generate_er_graph, generate_ba_graph


def benchmark_dijkstra():
    """Run Dijkstra on multiple graph sizes and heap types, record runtimes and peak memory."""
    heap_types = ["binary", "radix", "fibonacci"]

    # Graph sizes: (num_nodes, avg_edges_per_node)
    # For peer review testing:
    # Use smaller graphs first if runtime or memory is limited (uncomment and comment sizes accordingly):
    graph_sizes = [
        (10_000, 8),
        (50_000, 10),
        (100_000, 12),
        (500_000, 15),
        (1_000_000, 20),
        (2_000_000, 25),
    ]

    # Store results per heap type
    time_results = {heap: [] for heap in heap_types}
    mem_results = {heap: [] for heap in heap_types}

    for num_nodes, avg_edges in graph_sizes:
        approx_edges = avg_edges * num_nodes
        print(f"\n🔹 Benchmarking graph with {num_nodes} nodes and ~{approx_edges} edges")

        # ----- Choose graph generator here -----
        # Option 1: Erdos–Rényi style random graph
        graph = generate_er_graph(num_nodes, approx_edges, seed=42, show_progress=True)

        # Option 2: Barabási–Albert preferential attachment graph
        # To use BA instead, comment out the line above and uncomment this:
        # graph = generate_ba_graph(num_nodes, m=avg_edges, seed=42, show_progress=True)

        # Run Dijkstra for each heap type
        for heap_type in heap_types:
            print(f"   ▶ Running Dijkstra with {heap_type.title()} Heap...", end=" ", flush=True)

            # Start memory tracking
            tracemalloc.start()

            start = time.perf_counter()
            dijkstra(graph, source=0, heap_type=heap_type)
            end = time.perf_counter()

            # Capture memory usage (current, peak) in bytes
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            runtime = end - start
            peak_mib = peak / (1024 * 1024)  # convert to MiB

            time_results[heap_type].append(runtime)
            mem_results[heap_type].append(peak_mib)

            print(f"done in {runtime:.2f}s (peak ~{peak_mib:.2f} MiB)")

    return graph_sizes, time_results, mem_results


def plot_results(graph_sizes, time_results, mem_results):
    """Plot runtime and peak memory vs graph size for each heap with custom colors."""
    x = [n for n, _ in graph_sizes]

    colors = {
        "binary": "#1f77b4",
        "radix": "#e377c2",
        "fibonacci": "#9467bd",
    }
    
    colors_2 = {
        "binary": "#800000",
        "radix":  "#CC3333", 
        "fibonacci": "#FF8C00",
    }

    # --- Runtime (linear) ---
    plt.figure(figsize=(8, 5))
    for heap_type, runtimes in time_results.items():
        plt.plot(
            x,
            runtimes,
            marker="o",
            label=f"{heap_type.title()} Heap",
            color=colors.get(heap_type, None),
            linewidth=2,
        )

    plt.xlabel("Number of Nodes")
    plt.ylabel("Runtime (seconds)")
    plt.title("Dijkstra Runtime Comparison: Different Heaps (Linear Scale)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig("latex/plots/runtime_comparison.png", dpi=300)
    plt.show()
    
     # --- Runtime (log scale) ---
    plt.figure(figsize=(8, 5))
    for heap_type, runtimes in time_results.items():
        plt.plot(
            x,
            runtimes,
            marker="o",
            label=f"{heap_type.title()} Heap",
            color=colors.get(heap_type, None),
            linewidth=2,
        )

    plt.yscale("log")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Runtime (seconds, log scale)")
    plt.title("Dijkstra Runtime Comparison: Different Heaps (Log Scale)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig("latex/plots/runtime_comparison_log.png", dpi=300)
    plt.show()

    # --- Memory plot ---
    plt.figure(figsize=(8, 5))
    for heap_type, peaks in mem_results.items():
        plt.plot(
            x,
            peaks,
            marker="o",
            label=f"{heap_type.title()} Heap",
            color=colors_2.get(heap_type, None),
            linewidth=2,
        )

    plt.xlabel("Number of Nodes")
    plt.ylabel("Peak Memory (MiB)")
    plt.title("Dijkstra Peak Memory Comparison: Different Heaps")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig("latex/plots/memory_comparison.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    sizes, time_results, mem_results = benchmark_dijkstra()
    plot_results(sizes, time_results, mem_results)

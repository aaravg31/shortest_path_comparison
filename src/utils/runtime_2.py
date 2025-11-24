"""
Runtime Benchmark: Dijkstra Variants with Different Heaps

Compares performance (runtime + peak memory) of:
- Standard Dijkstra
- Bidirectional Dijkstra with skewness
- Contraction Hierarchies

Each variant is tested with three heap implementations:
- BinaryHeap
- RadixHeap
- FibonacciHeap

Outputs
-------
- Console timings + peak memory
- Matplotlib line charts (runtime, log-runtime, memory) per algorithm type
- Saved PNG plots under latex/plots/

Notes
-----
- Uses tqdm progress bars from graph_generator.
- Graphs are directed with random positive weights.
"""

import time
import tracemalloc
import matplotlib.pyplot as plt

from src.algorithms.dijkstra import dijkstra
from src.algorithms.bidirectional_skewed import BidirectionalDijkstra
from src.algorithms.contraction_hierarchy import ContractionHierarchy
from src.utils.graph_generator import generate_er_graph, generate_ba_graph


ALGORITHMS = ["dijkstra", "bidirectional"]
HEAP_TYPES = ["binary", "radix", "fibonacci"]


def _run_algorithm(alg: str, heap_type: str, graph, source: int, target: int):
    """
    Run one algorithm/heap combo with tracemalloc.
    Returns (runtime_seconds, peak_memory_MiB).
    """
    tracemalloc.start()
    start = time.perf_counter()

    if alg == "dijkstra":
        dijkstra(graph, source, heap_type=heap_type)

    elif alg == "bidirectional":
        bd = BidirectionalDijkstra(graph, heap_type=heap_type, skew=0.5)
        bd.find_shortest_path(source, target)

    elif alg == "contraction":
        # Assumes ContractionHierarchy can be configured per heap type.
        # If your current CH only uses BinaryHeap internally, you can
        # extend it to accept `heap_type` or temporarily ignore this arg.
        ch = ContractionHierarchy(graph, heap_type=heap_type)  # adjust if needed
        ch.preprocess()
        ch.query(source, target)

    else:
        raise ValueError(f"Unknown algorithm: {alg}")

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    runtime = end - start
    peak_mib = peak / (1024 * 1024)
    return runtime, peak_mib


def benchmark_all():
    """
    Run all algorithms (Dijkstra, Bidirectional, Contraction Hierarchy)
    with all heap types on multiple graph sizes.

    Returns
    -------
    graph_sizes : list[(num_nodes, avg_edges)]
    time_results : dict[alg][heap] -> [runtimes...]
    mem_results  : dict[alg][heap] -> [peak MiB...]
    """
    # Graph sizes: (num_nodes, avg_edges_per_node)
    graph_sizes = [
        (10_000, 8),
        (50_000, 10),
        (100_000, 12),
        (500_000, 15),
        (1_000_000, 20),
        (2_000_000, 25),
    ]

    time_results = {
        alg: {heap: [] for heap in HEAP_TYPES} for alg in ALGORITHMS
    }
    mem_results = {
        alg: {heap: [] for heap in HEAP_TYPES} for alg in ALGORITHMS
    }

    alg_labels = {
        "dijkstra": "Dijkstra",
        "bidirectional": "Bidirectional Dijkstra",
        "contraction": "Contraction Hierarchy",
    }

    for num_nodes, avg_edges in graph_sizes:
        approx_edges = avg_edges * num_nodes
        print(f"\n🔹 Benchmarking graph with {num_nodes} nodes and ~{approx_edges} edges")

        # ----- Choose graph generator here -----
        # Option 1: Erdos–Rényi style random graph (used in final experiments)
        graph = generate_er_graph(num_nodes, approx_edges, seed=42, show_progress=True)

        # Option 2: Barabási–Albert preferential attachment graph
        # graph = generate_ba_graph(num_nodes, m=avg_edges, seed=42, show_progress=True)

        source = 0
        target = num_nodes - 1

        for alg in ALGORITHMS:
            print(f"\n   ▶ {alg_labels[alg]} variant:")
            for heap_type in HEAP_TYPES:
                print(
                    f"      - {heap_type.title()} Heap...",
                    end=" ",
                    flush=True,
                )
                runtime, peak_mib = _run_algorithm(alg, heap_type, graph, source, target)
                time_results[alg][heap_type].append(runtime)
                mem_results[alg][heap_type].append(peak_mib)
                print(f"done in {runtime:.2f}s (peak ~{peak_mib:.2f} MiB)")

    return graph_sizes, time_results, mem_results


def _plot_for_algorithm(alg: str, graph_sizes, time_results_alg, mem_results_alg):
    """
    Create three plots for a single algorithm:
    - Runtime vs nodes (linear scale)
    - Runtime vs nodes (log scale)
    - Peak memory vs nodes
    """
    x = [n for n, _ in graph_sizes]

    # Runtime color palette
    colors = {
        "binary": "#1f77b4",   # blue
        "radix": "#e377c2",    # magenta
        "fibonacci": "#9467bd" # purple
    }

    # Memory color palette (warm tones)
    mem_colors = {
        "binary": "#800000",   # maroon
        "radix": "#d62728",    # red
        "fibonacci": "#ff8c00" # dark orange
    }

    alg_prefix = {
        "dijkstra": "dijkstra",
        "bidirectional": "bidijkstra",
        "contraction": "contraction",
    }[alg]

    alg_title = {
        "dijkstra": "Dijkstra",
        "bidirectional": "Bidirectional Dijkstra (Skewed Search)",
        "contraction": "Contraction Hierarchies",
    }[alg]

    # --- Runtime (linear) ---
    plt.figure(figsize=(8, 5))
    for heap_type, runtimes in time_results_alg.items():
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
    plt.title(f"{alg_title}: Runtime Comparison (Linear Scale)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"latex/plots/{alg_prefix}_runtime_linear.png", dpi=300)
    plt.show()

    # --- Runtime (log scale) ---
    plt.figure(figsize=(8, 5))
    for heap_type, runtimes in time_results_alg.items():
        plt.plot(
            x,
            runtimes,
            marker="o",
            label=f"{heap_type.title()} Heap",
            color=colors.get(heap_type, None),
            linewidth=2,
        )

    plt.xlabel("Number of Nodes")
    plt.ylabel("Runtime (seconds, log scale)")
    plt.title(f"{alg_title}: Runtime Comparison (Log Scale)")
    plt.yscale("log")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"latex/plots/{alg_prefix}_runtime_log.png", dpi=300)
    plt.show()

    # --- Memory (linear) ---
    plt.figure(figsize=(8, 5))
    for heap_type, peaks in mem_results_alg.items():
        plt.plot(
            x,
            peaks,
            marker="o",
            label=f"{heap_type.title()} Heap",
            color=mem_colors.get(heap_type, None),
            linewidth=2,
        )

    plt.xlabel("Number of Nodes")
    plt.ylabel("Peak Memory (MiB)")
    plt.title(f"{alg_title}: Peak Memory Comparison")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"latex/plots/{alg_prefix}_memory.png", dpi=300)
    plt.show()


def plot_all(graph_sizes, time_results, mem_results):
    """
    Generate plots for each algorithm:
    - 3 plots per algorithm (runtime linear, runtime log, memory)
    """
    for alg in ALGORITHMS:
        _plot_for_algorithm(
            alg,
            graph_sizes,
            time_results[alg],
            mem_results[alg],
        )


if __name__ == "__main__":
    sizes, time_res, mem_res = benchmark_all()
    plot_all(sizes, time_res, mem_res)
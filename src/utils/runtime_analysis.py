"""
Runtime Benchmark: Dijkstra vs Bidirectional Dijkstra with Different Heaps

Compares performance (runtime + peak memory) of:
- Standard Dijkstra
- Bidirectional Dijkstra with skewness

Each variant is tested with three heap implementations:
- BinaryHeap
- RadixHeap
- FibonacciHeap

Outputs
-------
- Console timings + peak memory
- Matplotlib line charts (runtime, log-runtime, memory),
  each containing ALL curves (Dijkstra + Bidirectional).

Notes
-----
- Uses tqdm progress bars from graph_generator.
- Graphs are directed with random positive weights.
- For graphs up to 500,000 nodes: each (algorithm, heap) combo is run 3 times
  and averaged.
- For larger graphs: each combo is run once (to keep total runtime manageable).
"""

import time
import tracemalloc
import matplotlib.pyplot as plt

from src.algorithms.dijkstra import dijkstra
from src.algorithms.bidirectional_skewed import BidirectionalDijkstra
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
    Run Dijkstra and Bidirectional Dijkstra with all heap types on multiple
    graph sizes.

    For num_nodes <= 500,000: run each combo 3 times and average.
    For num_nodes > 500,000: run once.

    Returns
    -------
    graph_sizes : list[(num_nodes, avg_edges)]
    time_results : dict[alg][heap] -> [avg runtimes...]
    mem_results  : dict[alg][heap] -> [avg peak MiB...]
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
        "bidirectional": "Bidirectional Dijkstra (Skewed Search)",
    }

    for num_nodes, avg_edges in graph_sizes:
        approx_edges = avg_edges * num_nodes
        repeats = 3 if num_nodes <= 500_000 else 1

        print(
            f"\n🔹 Benchmarking graph with {num_nodes} nodes and "
            f"~{approx_edges} edges ({repeats} run(s) per configuration)"
        )

        # ----- Choose graph generator here -----
        # Option 1: Erdos–Rényi style random graph (used in final experiments)
        graph = generate_er_graph(
            num_nodes, approx_edges, seed=42, show_progress=True
        )

        # Option 2: Barabási–Albert preferential attachment graph
        # graph = generate_ba_graph(
        #     num_nodes, m=avg_edges, seed=42, show_progress=True
        # )

        source = 0
        target = num_nodes - 1

        for alg in ALGORITHMS:
            print(f"\n   ▶ {alg_labels[alg]} variant:")
            for heap_type in HEAP_TYPES:
                total_time = 0.0
                total_peak = 0.0

                for r in range(repeats):
                    print(
                        f"      - {heap_type.title()} Heap "
                        f"(run {r+1}/{repeats})...",
                        end=" ",
                        flush=True,
                    )
                    runtime, peak_mib = _run_algorithm(
                        alg, heap_type, graph, source, target
                    )
                    total_time += runtime
                    total_peak += peak_mib
                    print(f"done in {runtime:.2f}s (peak ~{peak_mib:.2f} MiB)")

                avg_time = total_time / repeats
                avg_peak = total_peak / repeats

                time_results[alg][heap_type].append(avg_time)
                mem_results[alg][heap_type].append(avg_peak)

                if repeats > 1:
                    print(
                        f"        ↳ Avg over {repeats} runs: "
                        f"{avg_time:.2f}s, peak ~{avg_peak:.2f} MiB"
                    )

    return graph_sizes, time_results, mem_results


def plot_all(graph_sizes, time_results, mem_results):
    """
    Generate 3 plots, each containing all curves:
    - Runtime vs nodes (linear) for Dijkstra + Bidirectional
    - Runtime vs nodes (log scale) for Dijkstra + Bidirectional
    - Peak memory vs nodes for Dijkstra + Bidirectional

    Dijkstra curves use cool color tones; Bidirectional curves use warm tones.
    """
    x = [n for n, _ in graph_sizes]

    # Cool color palette (for Dijkstra)
    cool_colors = {
        "binary": "#1f77b4",   # blue
        "radix": "#e377c2",    # magenta
        "fibonacci": "#9467bd" # purple
    }

    # Warm color palette (for Bidirectional)
    warm_colors = {
        "binary": "#ff7f0e",   # orange
        "radix": "#d62728",    # red
        "fibonacci": "#ff8c00" # dark orange
    }

    # ---------- Runtime (linear) ----------
    plt.figure(figsize=(8, 5))
    for heap_type in HEAP_TYPES:
        # Dijkstra
        plt.plot(
            x,
            time_results["dijkstra"][heap_type],
            marker="o",
            label=f"Dijkstra - {heap_type.title()} Heap",
            color=cool_colors.get(heap_type),
            linewidth=2,
        )
        # Bidirectional
        plt.plot(
            x,
            time_results["bidirectional"][heap_type],
            marker="s",
            linestyle="--",
            label=f"Bidirectional - {heap_type.title()} Heap",
            color=warm_colors.get(heap_type),
            linewidth=2,
        )

    plt.xlabel("Number of Nodes")
    plt.ylabel("Runtime (seconds)")
    plt.title("Runtime Comparison: Dijkstra vs Bidirectional Dijkstra (Linear Scale)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig("latex/plots/dijkstra_vs_bidijkstra_runtime_linear.png", dpi=300)
    plt.show()

    # ---------- Runtime (log scale) ----------
    plt.figure(figsize=(8, 5))
    for heap_type in HEAP_TYPES:
        # Dijkstra
        plt.plot(
            x,
            time_results["dijkstra"][heap_type],
            marker="o",
            label=f"Dijkstra - {heap_type.title()} Heap",
            color=cool_colors.get(heap_type),
            linewidth=2,
        )
        # Bidirectional
        plt.plot(
            x,
            time_results["bidirectional"][heap_type],
            marker="s",
            linestyle="--",
            label=f"Bidirectional - {heap_type.title()} Heap",
            color=warm_colors.get(heap_type),
            linewidth=2,
        )

    plt.xlabel("Number of Nodes")
    plt.ylabel("Runtime (seconds, log scale)")
    plt.title("Runtime Comparison: Dijkstra vs Bidirectional Dijkstra (Log Scale)")
    plt.yscale("log")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig("latex/plots/dijkstra_vs_bidijkstra_runtime_log.png", dpi=300)
    plt.show()

    # ---------- Memory (linear) ----------
    plt.figure(figsize=(8, 5))
    for heap_type in HEAP_TYPES:
        # Dijkstra
        plt.plot(
            x,
            mem_results["dijkstra"][heap_type],
            marker="o",
            label=f"Dijkstra - {heap_type.title()} Heap",
            color=cool_colors.get(heap_type),
            linewidth=2,
        )
        # Bidirectional
        plt.plot(
            x,
            mem_results["bidirectional"][heap_type],
            marker="s",
            linestyle="--",
            label=f"Bidirectional - {heap_type.title()} Heap",
            color=warm_colors.get(heap_type),
            linewidth=2,
        )

    plt.xlabel("Number of Nodes")
    plt.ylabel("Peak Memory (MiB)")
    plt.title("Peak Memory Comparison: Dijkstra vs Bidirectional Dijkstra")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig("latex/plots/dijkstra_vs_bidijkstra_memory.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    sizes, time_res, mem_res = benchmark_all()
    plot_all(sizes, time_res, mem_res)

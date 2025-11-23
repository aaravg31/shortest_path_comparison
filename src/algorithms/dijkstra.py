"""
Dijkstra's Shortest Path Algorithm

Implements:
- dijkstra(graph, source, heap_type="binary")

Parameters
----------
graph : dict
    Adjacency list {u: [(v, weight), ...]}.
source : Any
    Starting node.
heap_type : str
    One of {"binary", "radix", "fibonacci"}.

Returns
-------
dict
    Mapping of node -> shortest distance from source.
"""

import math
from src.data_structures.binary_heap import BinaryHeap
from src.data_structures.fibonacci_heap import FibonacciHeap
from src.data_structures.radix_heap import RadixHeap


def dijkstra(graph, source, heap_type: str = "binary"):
    # --- choose heap implementation ---
    if heap_type == "binary":
        heap = BinaryHeap()
    elif heap_type == "fibonacci":
        heap = FibonacciHeap()
    elif heap_type == "radix":
        # use an upper bound on distances: max_weight * (num_nodes - 1)
        max_w = 0
        for u, nbrs in graph.items():
            for _, w in nbrs:
                if w > max_w:
                    max_w = w
        if max_w == 0:
            max_w = 1
        max_key = max_w * max(len(graph) - 1, 1)
        heap = RadixHeap(max_key=max_key)
    else:
        raise ValueError("heap_type must be one of {'binary', 'radix', 'fibonacci'}")

    # --- initialize distances ---
    dist = {v: math.inf for v in graph}
    dist[source] = 0

    # push source
    heap.insert(source, 0)

    while not heap.is_empty():
        u, d = heap.extract_min()
        if u is None:
            continue
        if d > dist[u]:
            continue  # stale entry

        for v, w in graph.get(u, []):
            alt = dist[u] + w
            if alt < dist[v]:
                dist[v] = alt

                #Unified membership check via __contains__
                if v in heap:
                    heap.decrease_key(v, alt)
                else:
                    heap.insert(v, alt)

    return dist
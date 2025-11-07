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


def dijkstra(graph, source, heap_type="binary"):
    # Initialize heap based on type
    if heap_type == "binary":
        heap = BinaryHeap()
    elif heap_type == "fibonacci":
        heap = FibonacciHeap()
    elif heap_type == "radix":
        max_edge = 0
        for u in graph:
            for _, w in graph[u]:
                max_edge += w  # sum upper bound
        if max_edge == 0:
            max_edge = 1

        heap = RadixHeap(max_key=max_edge)
    else:
        raise ValueError("heap_type must be one of {'binary', 'pairing', 'fibonacci'}")

    # Initialize distances
    dist = {v: math.inf for v in graph}
    dist[source] = 0

    # Insert source
    heap.insert(source, 0)

    while not heap.is_empty():
        u, d = heap.extract_min()
        if u is None:
            continue
        if d > dist[u]:
            continue  # Skip outdated entries

        for v, w in graph.get(u, []):
            alt = dist[u] + w
            if alt < dist[v]:
                dist[v] = alt

                # Check if node already exists in heap for decrease-key
                if (hasattr(heap, "nodes") and v in heap.nodes
                ) or (
                    hasattr(heap, "_pos") and v in heap._pos
                ) or (
                    isinstance(heap, RadixHeap) and v in heap._node_map
                ):
                    heap.decrease_key(v, alt)
                else:
                    heap.insert(v, alt)

    return dist

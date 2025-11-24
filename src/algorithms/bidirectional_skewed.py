"""
Bidirectional Dijkstra with Skewness

Implements:
- BidirectionalDijkstra class
"""

import math
from typing import Any, Dict, List, Optional, Tuple

from src.data_structures.binary_heap import BinaryHeap
from src.data_structures.fibonacci_heap import FibonacciHeap
from src.data_structures.radix_heap import RadixHeap


class BidirectionalDijkstra:
    # Initialize Bidirectional Dijkstra
    def __init__(self, graph: Dict[Any, List[Tuple[Any, float]]], heap_type: str = "binary", skew: float = 0.5):
        """
        Params:
            graph : dict
                Adjacency list {u: [(v, weight), ...]}.
            heap_type : str
                One of {"binary", "radix", "fibonacci"}.
            skew : float
                Parameter to control search balance.
                0.5 = balanced.

        Logic:
            if len(f_heap) * (1 - skew) < len(b_heap) * skew: expand forward
            If skew is 0.5: len(f) * 0.5 < len(b) * 0.5 => len(f) < len(b). Expand smaller
            If skew is 0.1: len(f) * 0.9 < len(b) * 0.1 => len(f) < len(b) * 1/9.
            This means we expand forward unless forward is MUCH larger than backward
            So small skew => prefer backward expansion
        """
        self.graph = graph
        self.reverse_graph = self._build_reverse_graph(graph)
        self.heap_type = heap_type
        self.skew = skew
        
        # Precompute max_key for RadixHeap if needed
        self.max_key = 0
        if heap_type == "radix":
            max_w = 0
            for u, nbrs in graph.items():
                for _, w in nbrs:
                    if w > max_w:
                        max_w = w
            if max_w == 0:
                max_w = 1
            # Upper bound for bidirectional might be smaller, but safe to use same bound
            self.max_key = int(max_w * max(len(graph) - 1, 1))

    def _build_reverse_graph(self, graph: Dict[Any, List[Tuple[Any, float]]]) -> Dict[Any, List[Tuple[Any, float]]]:
        rev = {u: [] for u in graph}
        for u, neighbors in graph.items():
            for v, w in neighbors:
                if v not in rev:
                    rev[v] = []
                rev[v].append((u, w))
        return rev

    def _init_heap(self):
        if self.heap_type == "binary":
            return BinaryHeap()
        elif self.heap_type == "fibonacci":
            return FibonacciHeap()
        elif self.heap_type == "radix":
            return RadixHeap(max_key=self.max_key)
        else:
            raise ValueError("heap_type must be one of {'binary', 'radix', 'fibonacci'}")

    def find_shortest_path(self, source: Any, target: Any) -> float:
        if source == target:
            return 0.0
        
        # If source or target not in graph, return infinity
        if source not in self.graph or target not in self.graph:
            return math.inf

        f_heap = self._init_heap()
        b_heap = self._init_heap()

        f_dist = {source: 0.0}
        b_dist = {target: 0.0}

        f_heap.insert(source, 0.0)
        b_heap.insert(target, 0.0)

        mu = math.inf # Best path found so far

        while not f_heap.is_empty() and not b_heap.is_empty():
            # Termination check
            f_min_node, f_min_dist = f_heap.peek()
            b_min_node, b_min_dist = b_heap.peek()
            
            # Should not happen if heaps are not empty
            if f_min_dist is None or b_min_dist is None:
                break
                
            if f_min_dist + b_min_dist >= mu:
                return mu

            # Decide direction
            # Avoid division by zero or weirdness if heaps are empty (checked above)
            # Logic: len(f_heap) * (1 - skew) < len(b_heap) * skew
            
            if len(f_heap) * (1 - self.skew) <= len(b_heap) * self.skew:
                # Expand forward
                u, d = f_heap.extract_min()
                if u is None: continue 
                
                if d > f_dist[u]:
                    continue

                for v, w in self.graph.get(u, []):
                    alt = d + w
                    if alt < f_dist.get(v, math.inf):
                        f_dist[v] = alt
                        if v in f_heap:
                            f_heap.decrease_key(v, alt)
                        else:
                            f_heap.insert(v, alt)
                        
                        # Update mu if v is visited by backward search
                        if v in b_dist:
                            new_path_len = alt + b_dist[v]
                            if new_path_len < mu:
                                mu = new_path_len
            else:
                # Expand backward
                u, d = b_heap.extract_min()
                if u is None: continue
                
                if d > b_dist[u]:
                    continue

                for v, w in self.reverse_graph.get(u, []):
                    alt = d + w
                    if alt < b_dist.get(v, math.inf):
                        b_dist[v] = alt
                        if v in b_heap:
                            b_heap.decrease_key(v, alt)
                        else:
                            b_heap.insert(v, alt)
                        
                        # Update mu if v is visited by forward search
                        if v in f_dist:
                            new_path_len = alt + f_dist[v]
                            if new_path_len < mu:
                                mu = new_path_len
                                
        return mu

"""
Contraction Hierarchies Algorithm

Implements:
- ContractionHierarchy class

Based on work in:
Geisberger, R., Sanders, P., Schultes, D., & Delling, D. (2008). \
    Contraction Hierarchies: Faster and Simpler Hierarchical Routing in Road Networks.
"""

import math
import copy
from typing import Any, Dict, List, Tuple, Set

# Import all heap types
from src.data_structures.binary_heap import BinaryHeap
from src.data_structures.fibonacci_heap import FibonacciHeap
from src.data_structures.radix_heap import RadixHeap


class ContractionHierarchy:
    PRIORITY_OFFSET = 1_000_000
    def __init__(self, graph: Dict[Any, List[Tuple[Any, float]]], heap_type: str = "binary"):
        """
        Initialize Contraction Hierarchy
        
        Params:
            graph: Adjacency list {u: [(v, weight), ...]}
            heap_type: one of {"binary", "fibonacci", "radix"}
        """
        self.heap_type = heap_type

        # Work on a copy of the graph since shortcuts will be added
        self.original_graph = graph
        self.graph = copy.deepcopy(graph)
        
        # Ensure all nodes are present in the graph keys
        all_nodes = set(self.graph.keys())
        for u, neighbors in self.graph.items():
            for v, w in neighbors:
                all_nodes.add(v)
                
        for node in all_nodes:
            if node not in self.graph:
                self.graph[node] = []

        self.nodes = list(self.graph.keys())
        self.node_order = []  
        self.rank = {}
        self.is_contracted = {node: False for node in self.nodes}
        
        # Reverse graph for backward search and preprocessing
        self.reverse_graph = self._build_reverse_graph(self.graph)

        # For RadixHeap, compute upper-bound key
        if heap_type == "radix":
            max_w = 0
            for u, nbrs in graph.items():
                for _, w in nbrs:
                    if w > max_w:
                        max_w = w
            if max_w == 0:  
                max_w = 1
            # Max possible path length ~ weight * number of edges
            self.max_key = int(max_w * max(len(graph) - 1, 1))
        else:
            self.max_key = None

    # ------------------------------------------------------------
    # Internal Heap Factory
    # ------------------------------------------------------------
    def _init_heap(self):
        if self.heap_type == "binary":
            return BinaryHeap()
        elif self.heap_type == "fibonacci":
            return FibonacciHeap()
        elif self.heap_type == "radix":
            return RadixHeap(max_key=self.max_key)
        else:
            raise ValueError("heap_type must be one of {'binary','fibonacci','radix'}")

    # ------------------------------------------------------------
    # Build Reverse Graph
    # ------------------------------------------------------------
    def _build_reverse_graph(self, graph):
        rev = {u: [] for u in graph}
        for u, neighbors in graph.items():
            for v, w in neighbors:
                if v not in rev:
                    rev[v] = []
                rev[v].append((u, w))
        return rev

    # ------------------------------------------------------------
    # Preprocessing
    # ------------------------------------------------------------
    def preprocess(self):
        """
        Execute the contraction phase: orders nodes by importance
        and contracts them one by one.
        """

        pq = self._init_heap()

        for node in self.nodes:
            imp = self._compute_importance(node)
            pq.insert(node, imp + self.PRIORITY_OFFSET)
            
        rank_counter = 0
        
        while not pq.is_empty():
            u, imp = pq.extract_min()
            
            current_imp = self._compute_importance(u)
            if not pq.is_empty():
                next_u, next_imp = pq.peek()
                if current_imp > next_imp:
                    pq.insert(u, current_imp + self.PRIORITY_OFFSET)
                    continue

            # Contract u
            self.rank[u] = rank_counter
            self.node_order.append(u)
            rank_counter += 1
            
            self._contract_node(u)
            self.is_contracted[u] = True

    # ------------------------------------------------------------
    # Compute Node Importance
    # ------------------------------------------------------------
    def _compute_importance(self, u):
        if self.is_contracted[u]:
            return math.inf

        incoming = [v for v, w in self.reverse_graph.get(u, []) if not self.is_contracted[v]]
        outgoing = [v for v, w in self.graph.get(u, []) if not self.is_contracted[v]]
        
        edges_removed = len(incoming) + len(outgoing)
        
        shortcuts = 0

        for iv in incoming:
            for ov in outgoing:
                if iv == ov:
                    continue
                
                w_iu = self._get_weight(iv, u)
                w_uo = self._get_weight(u, ov)
                target_dist = w_iu + w_uo
                
                witness_dist = self._local_dijkstra(iv, ov, limit=target_dist, exclude=u)
                if witness_dist > target_dist:
                    shortcuts += 1
                    
        return shortcuts - edges_removed

    # ------------------------------------------------------------
    # Node Contraction (adding shortcuts)
    # ------------------------------------------------------------
    def _contract_node(self, u):
        incoming = [v for v, w in self.reverse_graph.get(u, []) if not self.is_contracted[v]]
        outgoing = [v for v, w in self.graph.get(u, []) if not self.is_contracted[v]]

        for iv in incoming:
            for ov in outgoing:
                if iv == ov:
                    continue
                
                w_iu = self._get_weight(iv, u)
                w_uo = self._get_weight(u, ov)
                target_dist = w_iu + w_uo
                
                witness_dist = self._local_dijkstra(iv, ov, limit=target_dist, exclude=u)
                
                if witness_dist > target_dist:
                    self._add_edge(iv, ov, target_dist)

    # ------------------------------------------------------------
    # Local Dijkstra (small-radius search)
    # ------------------------------------------------------------
    def _local_dijkstra(self, source, target, limit, exclude):
        heap = self._init_heap()
        dist = {source: 0}
        heap.insert(source, 0)

        while not heap.is_empty():
            u, d = heap.extract_min()
            
            if d > limit:
                return math.inf
            if u == target:
                return d
            if d > dist[u]:
                continue
                
            for v, w in self.graph.get(u, []):
                if v == exclude or self.is_contracted[v]:
                    continue
                    
                new_dist = d + w
                if new_dist < dist.get(v, math.inf):
                    dist[v] = new_dist
                    if v in heap:
                        heap.decrease_key(v, new_dist)
                    else:
                        heap.insert(v, new_dist)
                        
        return dist.get(target, math.inf)

    # ------------------------------------------------------------
    # Graph Helpers
    # ------------------------------------------------------------
    def _get_weight(self, u, v):
        min_w = math.inf
        for node, w in self.graph.get(u, []):
            if node == v and w < min_w:
                min_w = w
        return min_w

    def _add_edge(self, u, v, w):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append((v, w))
        
        if v not in self.reverse_graph:
            self.reverse_graph[v] = []
        self.reverse_graph[v].append((u, w))

    # ------------------------------------------------------------
    # Query Phase (Bidirectional Dijkstra on CH graph)
    # ------------------------------------------------------------
    def query(self, source: Any, target: Any) -> float:
        if source not in self.graph or target not in self.graph:
            return math.inf
        if source == target:
            return 0.0
            
        f_heap = self._init_heap()
        b_heap = self._init_heap()
        
        f_dist = {source: 0.0}
        b_dist = {target: 0.0}
        
        f_heap.insert(source, 0.0)
        b_heap.insert(target, 0.0)
        
        mu = math.inf
        
        while not f_heap.is_empty() or not b_heap.is_empty():
            # Forward Expansion
            if not f_heap.is_empty():
                u, d = f_heap.extract_min()
                if d <= mu and d <= f_dist[u]:
                    for v, w in self.graph.get(u, []):
                        if self.rank[u] < self.rank[v]:
                            alt = d + w
                            if alt < f_dist.get(v, math.inf):
                                f_dist[v] = alt
                                if v in f_heap:
                                    f_heap.decrease_key(v, alt)
                                else:
                                    f_heap.insert(v, alt)

                                if v in b_dist:
                                    mu = min(mu, alt + b_dist[v])

            # Backward Expansion
            if not b_heap.is_empty():
                u, d = b_heap.extract_min()
                if d <= mu and d <= b_dist[u]:
                    for v, w in self.reverse_graph.get(u, []):
                        if self.rank[u] < self.rank[v]:
                            alt = d + w
                            if alt < b_dist.get(v, math.inf):
                                b_dist[v] = alt
                                if v in b_heap:
                                    b_heap.decrease_key(v, alt)
                                else:
                                    b_heap.insert(v, alt)

                                if v in f_dist:
                                    mu = min(mu, alt + f_dist[v])
                                            
        return mu

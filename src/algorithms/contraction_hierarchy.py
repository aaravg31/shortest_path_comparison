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
from src.data_structures.binary_heap import BinaryHeap

class ContractionHierarchy:
    def __init__(self, graph: Dict[Any, List[Tuple[Any, float]]]):
        """
        Initialize Contraction Hierarchy
        
        Params:
            graph: Adjacency list {u: [(v, weight), ...]}
        """
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
        self.node_order = []  # Stores nodes in contraction order
        self.rank = {}        # node -> rank (0 to N-1)
        self.is_contracted = {node: False for node in self.nodes}
        self.shortcuts = {}   # (u, v) -> middle_node
        
        # Reverse graph for backward search and preprocessing
        self.reverse_graph = self._build_reverse_graph(self.graph)

    def _build_reverse_graph(self, graph: Dict[Any, List[Tuple[Any, float]]]) -> Dict[Any, List[Tuple[Any, float]]]:
        rev = {u: [] for u in graph}
        for u, neighbors in graph.items():
            for v, w in neighbors:
                if v not in rev:
                    rev[v] = []
                rev[v].append((u, w))
        return rev

    def preprocess(self):
        """
        Execute the contraction phase: orders nodes by importance and contracts them one by one
        """
        # Compute initial importance for all nodes
        # Heuristic: Edge Difference = (shortcuts_needed) - (edges_removed)
        
        pq = BinaryHeap()
        for node in self.nodes:
            imp = self._compute_importance(node)
            pq.insert(node, imp)
            
        rank_counter = 0
        
        while not pq.is_empty():
            u, imp = pq.extract_min()
            
            current_imp = self._compute_importance(u)
            if not pq.is_empty():
                next_u, next_imp = pq.peek()
                if current_imp > next_imp:
                    pq.insert(u, current_imp)
                    continue

            # Contract u
            self.rank[u] = rank_counter
            self.node_order.append(u)
            rank_counter += 1
            
            self._contract_node(u)
            self.is_contracted[u] = True

    def _compute_importance(self, u: Any) -> int:
        """
        Compute importance of node u
        Importance = (Shortcuts added) - (Incoming edges + Outgoing edges) + (Contracted neighbors)
        """
        # If already contracted, infinite importance (shouldn't happen if logic is correct)
        if self.is_contracted[u]:
            return math.inf

        # Edges removed
        # Incoming: edges in reverse_graph from non-contracted nodes
        # Outgoing: edges in graph to non-contracted nodes
        incoming = [v for v, w in self.reverse_graph.get(u, []) if not self.is_contracted[v]]
        outgoing = [v for v, w in self.graph.get(u, []) if not self.is_contracted[v]]
        
        edges_removed = len(incoming) + len(outgoing)
        
        # Shortcuts needed
        shortcuts = 0
        # Need to simulate contraction to count shortcuts
        # For exact CH, run a local Dijkstra
        max_w = 0
        for iv in incoming:
            w_iu = self._get_weight(iv, u)
            for ov in outgoing:
                w_uo = self._get_weight(u, ov)
                path_len = w_iu + w_uo
                if path_len > max_w:
                    max_w = path_len
                    
        # Just count how many shortcuts WOULD be added
        for iv in incoming:
            for ov in outgoing:
                if iv == ov: continue
                
                w_iu = self._get_weight(iv, u)
                w_uo = self._get_weight(u, ov)
                target_dist = w_iu + w_uo
                
                # Check if there is a witness path shorter or equal to target_dist
                # Witness search: Dijkstra from iv to ov, excluding u, with limit target_dist
                witness_dist = self._local_dijkstra(iv, ov, limit=target_dist, exclude=u)
                
                if witness_dist > target_dist:
                    shortcuts += 1

        contracted_neighbors = 0 # Simplified for now
        
        return shortcuts - edges_removed + contracted_neighbors

    def _contract_node(self, u: Any):
        """
        Contract node u: add shortcuts between neighbors if u is on the shortest path
        """
        incoming = [v for v, w in self.reverse_graph.get(u, []) if not self.is_contracted[v]]
        outgoing = [v for v, w in self.graph.get(u, []) if not self.is_contracted[v]]

        for iv in incoming:
            for ov in outgoing:
                if iv == ov: continue
                
                w_iu = self._get_weight(iv, u)
                w_uo = self._get_weight(u, ov)
                target_dist = w_iu + w_uo
                
                witness_dist = self._local_dijkstra(iv, ov, limit=target_dist, exclude=u)
                
                if witness_dist > target_dist:
                    # Add shortcut iv -> ov
                    self._add_edge(iv, ov, target_dist, middle_node=u)

    def _local_dijkstra(self, source, target, limit, exclude):
        """
        Local Dijkstra search to find if a path exists from source to target 
        shorter than or equal to limit, avoiding 'exclude' node and contracted nodes
        """
        heap = BinaryHeap()
        dist = {source: 0}
        heap.insert(source, 0)
        
        # Only search on non-contracted nodes
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

    def _get_weight(self, u, v):
        # Helper to get weight u->v
        # Returns min weight if multiple edges exist
        min_w = math.inf
        found = False
        for node, w in self.graph.get(u, []):
            if node == v:
                if w < min_w:
                    min_w = w
                found = True
        return min_w if found else math.inf

    def _add_edge(self, u, v, w, middle_node=None):
        # Uncomment for debugging 
        # if middle_node is not None:
            #  print(f"Shortcut {u} -> {v} via {middle_node}")
             
        # Add to graph
        if u not in self.graph: self.graph[u] = []
        self.graph[u].append((v, w))
        
        # Add to reverse graph
        if v not in self.reverse_graph: self.reverse_graph[v] = []
        self.reverse_graph[v].append((u, w))
        
        if middle_node is not None:
            self.shortcuts[(u, v)] = middle_node

    def query(self, source: Any, target: Any) -> float:
        """
        Bidirectional Dijkstra Query on the CH graph.
        Forward search: u -> v only if rank[u] < rank[v]
        Backward search: u -> v only if rank[u] < rank[v] (in reverse graph)
        """
        if source not in self.graph or target not in self.graph:
            return math.inf
        if source == target:
            return 0.0
            
        f_heap = BinaryHeap()
        b_heap = BinaryHeap()
        
        f_dist = {source: 0.0}
        b_dist = {target: 0.0}
        
        f_heap.insert(source, 0.0)
        b_heap.insert(target, 0.0)
        
        mu = math.inf
        
        while not f_heap.is_empty() or not b_heap.is_empty():
            # Forward Step
            if not f_heap.is_empty():
                u, d = f_heap.extract_min()
                if d <= mu: # Prune if already worse than best path
                    if d <= f_dist[u]:
                        # Relax edges u -> v where rank[u] < rank[v]
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
                                        if alt + b_dist[v] < mu:
                                            mu = alt + b_dist[v]

            # Backward Step
            if not b_heap.is_empty():
                u, d = b_heap.extract_min()
                if d <= mu:
                    if d <= b_dist[u]:
                        # Relax edges u -> v in reverse graph where rank[u] < rank[v]
                        # u is the current node in backward search (moving away from target)
                        # v is a predecessor in original graph (successor in reverse graph)
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
                                        if alt + f_dist[v] < mu:
                                            mu = alt + f_dist[v]
                                            
        return mu

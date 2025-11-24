import math
from src.data_structures.binary_heap import BinaryHeap
from src.algorithms.contraction_hierarchy import ContractionHierarchy
def dijkstra_visual(graph, start, end):
    """
    Yields (visited_nodes, frontier_nodes, path_nodes)
    visited_nodes: list of nodes that have been extracted from heap
    frontier_nodes: list of nodes currently in heap (or just added)
    """
    heap = BinaryHeap()
    dist = {v: math.inf for v in graph}
    dist[start] = 0
    parent = {start: None}
    
    heap.insert(start, 0)
    
    visited = []
    
    while not heap.is_empty():
        u, d = heap.extract_min()
        visited.append(u)
        
        if u == end:
            break
            
        if d > dist[u]:
            continue
            
        yield (visited, list(heap._pos.keys()), [])

        for v, w in graph.get(u, []):
            alt = dist[u] + w
            if alt < dist[v]:
                dist[v] = alt
                parent[v] = u
                if v in heap:
                    heap.decrease_key(v, alt)
                else:
                    heap.insert(v, alt)
    
    # Reconstruct path
    path = []
    curr = end
    if dist[end] != math.inf:
        while curr is not None:
            path.append(curr)
            curr = parent.get(curr)
    
    yield (visited, [], path)

def bidirectional_dijkstra_visual(graph, start, end):
    f_heap = BinaryHeap()
    b_heap = BinaryHeap()
    
    f_dist = {v: math.inf for v in graph}
    b_dist = {v: math.inf for v in graph}
    
    f_dist[start] = 0
    b_dist[end] = 0
    
    f_parent = {start: None}
    b_parent = {end: None}
    
    f_heap.insert(start, 0)
    b_heap.insert(end, 0)
    
    f_visited = []
    b_visited = []
    
    mu = math.inf
    meet_node = None
    
    while not f_heap.is_empty() and not b_heap.is_empty():
        # Forward Step
        u, d = f_heap.extract_min()
        f_visited.append(u)
        
        if d + b_dist[u] < mu:
            mu = d + b_dist[u]
            meet_node = u
            
        # if d > mu, it can stop
        # For visualization, show it until heaps are empty
        if d > mu and not b_heap.is_empty() and b_heap.peek()[1] > mu:
             break

        yield (f_visited + b_visited, list(f_heap._pos.keys()) + list(b_heap._pos.keys()), [])

        for v, w in graph.get(u, []):
            alt = d + w
            if alt < f_dist[v]:
                f_dist[v] = alt
                f_parent[v] = u
                if v in f_heap:
                    f_heap.decrease_key(v, alt)
                else:
                    f_heap.insert(v, alt)
                
                if alt + b_dist[v] < mu:
                    mu = alt + b_dist[v]
                    meet_node = v

        # Backward Step
        u_b, d_b = b_heap.extract_min()
        b_visited.append(u_b)
        
        if d_b + f_dist[u_b] < mu:
            mu = d_b + f_dist[u_b]
            meet_node = u_b
            
        yield (f_visited + b_visited, list(f_heap._pos.keys()) + list(b_heap._pos.keys()), [])

        for v, w in graph.get(u_b, []): # In undirected grid, reverse graph is same
            alt = d_b + w
            if alt < b_dist[v]:
                b_dist[v] = alt
                b_parent[v] = u_b
                if v in b_heap:
                    b_heap.decrease_key(v, alt)
                else:
                    b_heap.insert(v, alt)
                    
                if alt + f_dist[v] < mu:
                    mu = alt + f_dist[v]
                    meet_node = v
                    
        if mu != math.inf and f_heap.peek()[1] + b_heap.peek()[1] >= mu:
            break

    # Reconstruct path
    path = []
    if meet_node and mu != math.inf:
        # From start to meet_node
        curr = meet_node
        while curr is not None:
            path.append(curr)
            curr = f_parent.get(curr)
        path.reverse()
        
        # From meet_node to end
        curr = b_parent.get(meet_node)
        while curr is not None:
            path.append(curr)
            curr = b_parent.get(curr)
            
    yield (f_visited + b_visited, [], path)

def contraction_hierarchy_visual(graph, start, end):
    # Preprocess (not visualized for now, just done instantly)
    ch = ContractionHierarchy(graph)
    ch.preprocess()
    
    # Query Visualization
    if start not in ch.graph or end not in ch.graph:
        return
    if start == end:
        yield ([], [], [start])
        return

    f_heap = BinaryHeap()
    b_heap = BinaryHeap()
    
    f_dist = {start: 0.0}
    b_dist = {end: 0.0}
    
    f_parent = {start: None}
    b_parent = {end: None}
    
    f_heap.insert(start, 0.0)
    b_heap.insert(end, 0.0)
    
    f_visited = []
    b_visited = []
    
    mu = math.inf
    meet_node = None
    
    while not f_heap.is_empty() or not b_heap.is_empty():
        # Forward Step
        if not f_heap.is_empty():
            u, d = f_heap.extract_min()
            f_visited.append(u)
            
            if d <= mu:
                if d <= f_dist[u]:
                    for v, w in ch.graph.get(u, []):
                        if ch.rank[u] < ch.rank[v]:
                            alt = d + w
                            if alt < f_dist.get(v, math.inf):
                                f_dist[v] = alt
                                f_parent[v] = u
                                if v in f_heap:
                                    f_heap.decrease_key(v, alt)
                                else:
                                    f_heap.insert(v, alt)
                                
                                if v in b_dist:
                                    if alt + b_dist[v] < mu:
                                        mu = alt + b_dist[v]
                                        meet_node = v
            
            yield (f_visited + b_visited, list(f_heap._pos.keys()) + list(b_heap._pos.keys()), [])

        # Backward Step
        if not b_heap.is_empty():
            u, d = b_heap.extract_min()
            b_visited.append(u)
            
            if d <= mu:
                if d <= b_dist[u]:
                    for v, w in ch.reverse_graph.get(u, []):
                        if ch.rank[u] < ch.rank[v]:
                            alt = d + w
                            if alt < b_dist.get(v, math.inf):
                                b_dist[v] = alt
                                b_parent[v] = u
                                if v in b_heap:
                                    b_heap.decrease_key(v, alt)
                                else:
                                    b_heap.insert(v, alt)
                                    
                                if v in f_dist:
                                    if alt + f_dist[v] < mu:
                                        mu = alt + f_dist[v]
                                        meet_node = v
            
            yield (f_visited + b_visited, list(f_heap._pos.keys()) + list(b_heap._pos.keys()), [])

    # Reconstruct path with shortcut unpacking
    shortcuts_used = []  # Track shortcuts used during unpacking
    
    def unpack_path(u, v):
        if (u, v) in ch.shortcuts:
            shortcuts_used.append((u, v))  # Record this shortcut
            mid = ch.shortcuts[(u, v)]
            return unpack_path(u, mid) + [mid] + unpack_path(mid, v)
        return []
    
    def bfs_path(start, end, graph):
        # Simple BFS to find path between two nodes in original graph
        from collections import deque
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            node, path = queue.popleft()
            if node == end:
                return path[1:-1]  # Exclude start and end
            
            for neighbor, _ in graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return []  # No path found

    full_path = []
    if meet_node and mu != math.inf:
        # Trace up from start
        curr = meet_node
        start_path = []
        while curr is not None:
            start_path.append(curr)
            curr = f_parent.get(curr)
        start_path.reverse()
        
        # Trace up from end
        curr = b_parent.get(meet_node)
        end_path = []
        while curr is not None:
            end_path.append(curr)
            curr = b_parent.get(curr)
            
        raw_path = start_path + end_path[1:]
        
        if raw_path:
            full_path.append(raw_path[0])
            for i in range(len(raw_path) - 1):
                u = raw_path[i]
                v = raw_path[i+1]
                
                # Try to unpack as shortcut
                unpacked = unpack_path(u, v)
                full_path.extend(unpacked)
                
                # If no shortcut but nodes are not adjacent, use BFS on original graph
                if not unpacked:
                    dr = abs(u[0] - v[0])
                    dc = abs(u[1] - v[1])
                    if dr + dc > 1:
                        # Need to fill the gap using original graph
                        gap_path = bfs_path(u, v, ch.original_graph)
                        full_path.extend(gap_path)
                
                full_path.append(v)
            
    yield (f_visited + b_visited, [], full_path, shortcuts_used)

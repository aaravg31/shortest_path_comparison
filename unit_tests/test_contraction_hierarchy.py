"""
Unit tests for Contraction Hierarchies
"""

import pytest
import math
from src.algorithms.contraction_hierarchy import ContractionHierarchy

def test_simple_contraction():
    # A -> B -> C, weights 1, 1
    # Contracting B should add shortcut A -> C with weight 2
    graph = {
        'A': [('B', 1)],
        'B': [('C', 1)],
        'C': []
    }
    
    ch = ContractionHierarchy(graph)
    ch.preprocess()
    
    assert ch.query('A', 'C') == 2
    assert ch.query('A', 'B') == 1
    assert ch.query('B', 'C') == 1

def test_diamond_graph():
    # A->B=1, B->D=1 (path 2)
    # A->C=2, C->D=2 (path 4)
    graph = {
        'A': [('B', 1), ('C', 2)],
        'B': [('D', 1)],
        'C': [('D', 2)],
        'D': []
    }
    
    ch = ContractionHierarchy(graph)
    ch.preprocess()
    
    assert ch.query('A', 'D') == 2
    assert ch.query('A', 'B') == 1
    assert ch.query('A', 'C') == 2

def test_disconnected():
    graph = {
        'A': [('B', 1)],
        'C': [('D', 1)]
    }
    ch = ContractionHierarchy(graph)
    ch.preprocess()
    
    assert ch.query('A', 'C') == math.inf
    assert ch.query('A', 'D') == math.inf
    assert ch.query('A', 'B') == 1

def test_cycle():
    # A -> B -> C -> A
    graph = {
        'A': [('B', 1)],
        'B': [('C', 1)],
        'C': [('A', 1)]
    }
    ch = ContractionHierarchy(graph)
    ch.preprocess()
    
    assert ch.query('A', 'C') == 2
    assert ch.query('A', 'B') == 1
    assert ch.query('A', 'A') == 0

def test_random_correctness():
    # Compare against standard Dijkstra on a small random graph
    import random
    from src.algorithms.dijkstra import dijkstra
    
    nodes = range(20)
    graph = {u: [] for u in nodes}
    
    # Create random edges
    for _ in range(50):
        u = random.choice(nodes)
        v = random.choice(nodes)
        if u != v:
            w = random.randint(1, 10)
            graph[u].append((v, w))
            
    ch = ContractionHierarchy(graph)
    ch.preprocess()
    
    for _ in range(20):
        u = random.choice(nodes)
        v = random.choice(nodes)
        
        ch_dist = ch.query(u, v)
        
        # Standard Dijkstra
        dists = dijkstra(graph, u)
        std_dist = dists.get(v, math.inf)
        
        assert ch_dist == std_dist, f"Mismatch for {u}->{v}: CH={ch_dist}, Std={std_dist}"

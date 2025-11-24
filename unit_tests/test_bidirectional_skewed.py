import pytest
import math
from src.algorithms.bidirectional_skewed import BidirectionalDijkstra

# Sample Graphs
@pytest.fixture
def simple_graph():
    """
    A -> B -> C -> D
    Weights: 1, 1, 1
    Shortest path A->D is 3
    """
    return {
        'A': [('B', 1)],
        'B': [('C', 1)],
        'C': [('D', 1)],
        'D': []
    }

@pytest.fixture
def complex_graph():
    """
    A -> B (1)
    A -> C (4)
    B -> C (2)
    B -> D (5)
    C -> D (1)
    
    Path A->B->C->D: 1 + 2 + 1 = 4
    Path A->C->D: 4 + 1 = 5
    Path A->B->D: 1 + 5 = 6
    
    Shortest A->D is 4
    """
    return {
        'A': [('B', 1), ('C', 4)],
        'B': [('C', 2), ('D', 5)],
        'C': [('D', 1)],
        'D': []
    }

@pytest.fixture
def disconnected_graph():
    return {
        'A': [('B', 1)],
        'B': [],
        'C': [('D', 1)],
        'D': []
    }

# Tests
@pytest.mark.parametrize("heap_type", ["binary", "fibonacci", "radix"])
@pytest.mark.parametrize("skew", [0.1, 0.5, 0.9])
def test_simple_graph(simple_graph, heap_type, skew):
    bd = BidirectionalDijkstra(simple_graph, heap_type=heap_type, skew=skew)
    dist = bd.find_shortest_path('A', 'D')
    assert dist == 3

@pytest.mark.parametrize("heap_type", ["binary", "fibonacci", "radix"])
@pytest.mark.parametrize("skew", [0.1, 0.5, 0.9])
def test_complex_graph(complex_graph, heap_type, skew):
    bd = BidirectionalDijkstra(complex_graph, heap_type=heap_type, skew=skew)
    dist = bd.find_shortest_path('A', 'D')
    assert dist == 4

@pytest.mark.parametrize("heap_type", ["binary", "fibonacci", "radix"])
def test_disconnected_graph(disconnected_graph, heap_type):
    bd = BidirectionalDijkstra(disconnected_graph, heap_type=heap_type)
    dist = bd.find_shortest_path('A', 'C')
    assert dist == math.inf

def test_same_node(simple_graph):
    bd = BidirectionalDijkstra(simple_graph)
    dist = bd.find_shortest_path('A', 'A')
    assert dist == 0

def test_invalid_heap_type(simple_graph):
    bd = BidirectionalDijkstra(simple_graph, heap_type="invalid")
    with pytest.raises(ValueError):
        bd.find_shortest_path('A', 'D')

def test_large_skew_forward(simple_graph):
    # Skew 1.0 means (1-1) = 0 on LHS. 0 <= len(b) * 1
    # If skew=1.0, LHS=0. RHS=len(b). 0 <= len(b) is always true
    # So it should behave like forward Dijkstra (mostly)
    bd = BidirectionalDijkstra(simple_graph, skew=1.0)
    dist = bd.find_shortest_path('A', 'D')
    assert dist == 3

def test_small_skew_backward(simple_graph):
    # Skew 0.0 means LHS=len(f). RHS=0
    # len(f) <= 0 is only true if len(f)=0
    # So it should expand backward mostly
    bd = BidirectionalDijkstra(simple_graph, skew=0.0)
    dist = bd.find_shortest_path('A', 'D')
    assert dist == 3

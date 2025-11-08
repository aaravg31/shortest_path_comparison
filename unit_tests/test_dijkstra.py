import unittest
from src.algorithms.dijkstra import dijkstra

class TestDijkstra(unittest.TestCase):
    def setUp(self):
        # Simple weighted directed graph
        self.graph = {
            'A': [('B', 1), ('C', 4)],
            'B': [('C', 2), ('D', 5)],
            'C': [('D', 1)],
            'D': []
        }
        self.expected = {'A': 0, 'B': 1, 'C': 3, 'D': 4}

    def test_binary_heap(self):
        result = dijkstra(self.graph, 'A', heap_type="binary")
        self.assertEqual(result, self.expected)

    def test_fibonacci_heap(self):
        result = dijkstra(self.graph, 'A', heap_type="fibonacci")
        self.assertEqual(result, self.expected)

    def test_radix_heap(self):
        result = dijkstra(self.graph, 'A', heap_type="radix")
        self.assertEqual(result, self.expected)

if __name__ == "__main__":
    unittest.main()

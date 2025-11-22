import unittest
from src.utils.graph_generator import generate_er_graph, generate_ba_graph

class TestERGraphGenerator(unittest.TestCase):

    def test_er_graph_node_count(self):
        g = generate_er_graph(5, 10, seed=123, show_progress=False)
        self.assertEqual(len(g), 5)

    def test_er_no_self_loops(self):
        g = generate_er_graph(20, 100, seed=123, show_progress=False)
        for u, neighbors in g.items():
            for v, _ in neighbors:
                self.assertNotEqual(u, v)

    def test_er_weight_range(self):
        g = generate_er_graph(10, 40, weight_range=(5, 10), seed=123, show_progress=False)
        for _, neighbors in g.items():
            for _, w in neighbors:
                self.assertTrue(5 <= w <= 10)

    def test_er_reproducibility(self):
        g1 = generate_er_graph(10, 30, seed=123, show_progress=False)
        g2 = generate_er_graph(10, 30, seed=123, show_progress=False)
        self.assertEqual(g1, g2)

    def test_er_edges_not_more_than_requested(self):
        num_nodes = 10
        num_edges = 50
        g = generate_er_graph(num_nodes, num_edges, seed=123, show_progress=False)
        total_edges = sum(len(neigh) for neigh in g.values())
        # We skip self-loops, so total_edges can be <= num_edges
        self.assertLessEqual(total_edges, num_edges)


class TestBAGraphGenerator(unittest.TestCase):

    def test_ba_graph_node_count(self):
        g = generate_ba_graph(10, m=3, seed=123, show_progress=False)
        self.assertEqual(len(g), 10)
        # Ensure all node IDs from 0..9 exist
        self.assertEqual(set(g.keys()), set(range(10)))

    def test_ba_no_self_loops(self):
        g = generate_ba_graph(30, m=3, seed=123, show_progress=False)
        for u, neighbors in g.items():
            for v, _ in neighbors:
                self.assertNotEqual(u, v)

    def test_ba_weight_range(self):
        g = generate_ba_graph(20, m=2, weight_range=(5, 10), seed=42, show_progress=False)
        for _, neighbors in g.items():
            for _, w in neighbors:
                self.assertTrue(5 <= w <= 10)

    def test_ba_reproducibility(self):
        g1 = generate_ba_graph(25, m=3, seed=99, show_progress=False)
        g2 = generate_ba_graph(25, m=3, seed=99, show_progress=False)
        self.assertEqual(g1, g2)

    def test_ba_initial_chain_exists(self):
        """
        For m=3, we start with a chain 0->1, 1->2, 2->3.
        Check that these edges exist.
        """
        m = 3
        g = generate_ba_graph(10, m=m, seed=1, show_progress=False)

        def has_edge(u, v):
            return any(neigh == v for neigh, _ in g[u])

        for u in range(m):
            v = u + 1
            self.assertTrue(
                has_edge(u, v),
                msg=f"Expected initial chain edge {u}->{v} to exist in BA seed graph",
            )

    def test_ba_out_degree_of_new_nodes(self):
        """
        Every new node (from m+1 to num_nodes-1) should create exactly m outgoing edges.
        """
        num_nodes = 15
        m = 3
        g = generate_ba_graph(num_nodes, m=m, seed=123, show_progress=False)

        for new_node in range(m + 1, num_nodes):
            self.assertEqual(
                len(g[new_node]),
                m,
                msg=f"Node {new_node} should have exactly {m} outgoing edges",
            )

    def test_ba_invalid_parameters(self):
        # m must be at least 1
        with self.assertRaises(ValueError):
            generate_ba_graph(num_nodes=10, m=0, seed=1, show_progress=False)

        # num_nodes must be > m
        with self.assertRaises(ValueError):
            generate_ba_graph(num_nodes=3, m=3, seed=1, show_progress=False)


if __name__ == "__main__":
    unittest.main()
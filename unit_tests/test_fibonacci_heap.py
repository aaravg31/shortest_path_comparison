import unittest
from data_structures.fibonacci_heap import FibonacciHeap

class TestFibonacciHeap(unittest.TestCase):

    def test_insert_and_extract_min(self):
        fh = FibonacciHeap()
        fh.insert('A', 10)
        fh.insert('B', 3)
        fh.insert('C', 5)

        node, key = fh.extract_min()
        self.assertEqual((node, key), ('B', 3))

        node, key = fh.extract_min()
        self.assertIn(node, ['A', 'C'])
        self.assertTrue(key in [5, 10])
        
    def test_duplicate_insert(self):
        fh = FibonacciHeap()
        fh.insert('A', 5)
        with self.assertRaises(ValueError):
            fh.insert('A', 1)

    def test_decrease_key(self):
        fh = FibonacciHeap()
        fh.insert('X', 10)
        fh.insert('Y', 5)
        fh.decrease_key('X', 2)
        node, key = fh.extract_min()
        self.assertEqual((node, key), ('X', 2))

    def test_decrease_key_missing(self):
        fh = FibonacciHeap()
        fh.insert('A', 3)
        with self.assertRaises(KeyError):
            fh.decrease_key('B', 1)

    def test_is_empty_and_len(self):
        fh = FibonacciHeap()
        self.assertTrue(fh.is_empty())
        fh.insert('N1', 4)
        self.assertFalse(fh.is_empty())
        self.assertEqual(len(fh), 1)
        fh.extract_min()
        self.assertTrue(fh.is_empty())

if __name__ == "__main__":
    unittest.main()
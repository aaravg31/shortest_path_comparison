import unittest
from src.data_structures.binary_heap import BinaryHeap

class TestBinaryHeap(unittest.TestCase):

    def test_insert_and_extract_min(self):
        pq = BinaryHeap()
        pq.insert('A', 5)
        pq.insert('B', 2)
        pq.insert('C', 7)

        node, pr = pq.extract_min()
        self.assertEqual((node, pr), ('B', 2))

        node, pr = pq.extract_min()
        self.assertEqual((node, pr), ('A', 5))

        node, pr = pq.extract_min()
        self.assertEqual((node, pr), ('C', 7))

        node, pr = pq.extract_min()
        self.assertEqual((node, pr), (None, None))  # empty now

    def test_duplicate_insert(self):
        pq = BinaryHeap()
        pq.insert('A', 3)
        with self.assertRaises(ValueError):
            pq.insert('A', 1)

    def test_decrease_key(self):
        pq = BinaryHeap()
        pq.insert('X', 10)
        pq.insert('Y', 8)
        pq.insert('Z', 12)

        pq.decrease_key('Z', 1)  # Z becomes smallest
        node, pr = pq.extract_min()
        self.assertEqual((node, pr), ('Z', 1))

        # Decreasing to a higher value should be ignored (no error)
        pq.decrease_key('X', 15)
        node, pr = pq.extract_min()
        self.assertEqual((node, pr), ('Y', 8))

        node, pr = pq.extract_min()
        self.assertEqual((node, pr), ('X', 10))

    def test_decrease_key_missing(self):
        pq = BinaryHeap()
        pq.insert('A', 3)
        with self.assertRaises(KeyError):
            pq.decrease_key('B', 1)
            
    def test_is_empty_and_len(self):
        pq = BinaryHeap()
        self.assertTrue(pq.is_empty())
        self.assertEqual(len(pq), 0)
        pq.insert(1, 3.0)
        self.assertFalse(pq.is_empty())
        self.assertEqual(len(pq), 1)

if __name__ == "__main__":
    unittest.main()
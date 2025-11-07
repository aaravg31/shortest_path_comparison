import unittest
from src.data_structures.radix_heap import RadixHeap


class TestRadixHeap(unittest.TestCase):

    def setUp(self):
        # choose a safe upper bound for priorities in tests
        self.max_key = 100

    def test_insert_and_extract_min(self):
        pq = RadixHeap(max_key=self.max_key)
        pq.insert('A', 20)
        pq.insert('B', 5)
        pq.insert('C', 12)

        node, pr = pq.extract_min()
        self.assertEqual((node, pr), ('B', 5))

        node, pr = pq.extract_min()
        self.assertEqual((node, pr), ('C', 12))

        node, pr = pq.extract_min()
        self.assertEqual((node, pr), ('A', 20))

        node, pr = pq.extract_min()
        self.assertEqual((node, pr), (None, None))

    def test_duplicate_insert(self):
        pq = RadixHeap(max_key=self.max_key)
        pq.insert('A', 30)
        with self.assertRaises(ValueError):
            pq.insert('A', 10)

    def test_decrease_key(self):
        pq = RadixHeap(max_key=self.max_key)
        pq.insert('X', 50)
        pq.insert('Y', 40)
        pq.insert('Z', 90)

        # Z becomes smallest
        pq.decrease_key('Z', 10)
        node, pr = pq.extract_min()
        self.assertEqual((node, pr), ('Z', 10))

        # decreasing to a higher value should be ignored
        pq.decrease_key('X', 60)
        # next smallest should be Y
        node, pr = pq.extract_min()
        self.assertEqual((node, pr), ('Y', 40))

        node, pr = pq.extract_min()
        self.assertEqual((node, pr), ('X', 50))

    def test_decrease_key_missing(self):
        pq = RadixHeap(max_key=self.max_key)
        pq.insert('A', 3)
        with self.assertRaises(KeyError):
            pq.decrease_key('B', 1)

    def test_monotonicity_violation(self):
        pq = RadixHeap(max_key=self.max_key)
        pq.insert('A', 10)
        pq.extract_min()  # last_extracted = 10

        # inserting smaller key should throw
        with self.assertRaises(ValueError):
            pq.insert('B', 5)

        pq.insert('C', 12)  # valid

        with self.assertRaises(ValueError):
            pq.decrease_key('C', 9)  # also violates monotonicity

    def test_is_empty_and_len(self):
        pq = RadixHeap(max_key=self.max_key)
        self.assertTrue(pq.is_empty())
        self.assertEqual(len(pq), 0)

        pq.insert('N1', 7)
        pq.insert('N2', 4)
        self.assertFalse(pq.is_empty())
        self.assertEqual(len(pq), 2)

        pq.extract_min()
        pq.extract_min()
        self.assertTrue(pq.is_empty())


if __name__ == "__main__":
    unittest.main()

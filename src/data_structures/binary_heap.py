"""
Binary Min Heap

Implements:
- insert(node, priority)
- extract_min() -> (node, priority) or (None, None) if empty
- decrease_key(node, new_priority)
- is_empty() -> bool
- __len__() -> number of items

Notes
-----
- Each `node` must be unique in the heap at any time.
- `decrease_key` only lowers priority; higher values are ignored.
- Internally stores items in an array and keeps a node->index map
  so we can do O(log n) sifts for both insert and decrease-key.
  """

from typing import Any, List, Tuple, Dict, Optional

class BinaryHeap:
    def __init__(self) -> None:
        # Array of (node, priority)
        self._heap: List[Tuple[Any, float]] = []
        # Position map: node -> index in _heap
        self._pos: Dict[Any, int] = {}

    # INSERT
    def insert(self, node: Any, priority: float) -> None:
        """Insert a new (node, priority). Node must not already be present."""
        if node in self._pos:
            raise ValueError(f"Node {node!r} already present; use decrease_key if needed.")
        self._heap.append((node, priority))
        idx = len(self._heap) - 1
        self._pos[node] = idx
        self._sift_up(idx)

    # EXTRACT MIN
    def extract_min(self) -> Tuple[Optional[Any], Optional[float]]:
        """Remove and return the (node, priority) with smallest priority."""
        if not self._heap:
            return None, None

        # Swap root with last, pop last, then sift-down the new root
        self._swap(0, len(self._heap) - 1)
        node, priority = self._heap.pop()
        del self._pos[node]

        if self._heap:
            self._sift_down(0)

        return node, priority

    # DECREASE KEY
    def decrease_key(self, node: Any, new_priority: float) -> None:
        """
        Decrease the priority of an existing node.
        If new_priority >= current, no change.
        """
        idx = self._pos.get(node)
        if idx is None:
            raise KeyError(f"Node {node!r} not found in heap.")

        cur_node, cur_priority = self._heap[idx]
        if new_priority >= cur_priority:
            return  # no-op

        # Update and sift up
        self._heap[idx] = (cur_node, new_priority)
        self._sift_up(idx)

    # IS EMPTY
    def is_empty(self) -> bool:
        return len(self._heap) == 0

    # LEN
    def __len__(self) -> int:
        return len(self._heap)
    
    # CONTAINS
    def __contains__(self, node: Any) -> bool:
        return node in self._pos

    # INTERNAL UTILITIES
    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left(self, i: int) -> int:
        return 2 * i + 1

    def _right(self, i: int) -> int:
        return 2 * i + 2

    def _sift_up(self, i: int) -> None:
        while i > 0:
            p = self._parent(i)
            if self._heap[i][1] < self._heap[p][1]:
                self._swap(i, p)
                i = p
            else:
                break

    def _sift_down(self, i: int) -> None:
        n = len(self._heap)
        while True:
            l, r = self._left(i), self._right(i)
            smallest = i

            if l < n and self._heap[l][1] < self._heap[smallest][1]:
                smallest = l
            if r < n and self._heap[r][1] < self._heap[smallest][1]:
                smallest = r

            if smallest != i:
                self._swap(i, smallest)
                i = smallest
            else:
                break

    def _swap(self, i: int, j: int) -> None:
        """Swap positions i and j in the heap array and update the position map."""
        if i == j:
            return
        (node_i, pri_i), (node_j, pri_j) = self._heap[i], self._heap[j]
        self._heap[i], self._heap[j] = (node_j, pri_j), (node_i, pri_i)
        self._pos[node_i] = j
        self._pos[node_j] = i
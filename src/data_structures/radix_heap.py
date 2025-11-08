"""
Radix heap (monotone priority queue) for non-negative integer keys.

Implements:
- insert(node, priority)
- extract_min() -> (node, priority) or (None, None) if empty
- decrease_key(node, new_priority)
- is_empty() -> bool
- __len__() -> number of items

Notes
-----
- Assumes that extracted keys never decrease (monotonicity holds).
- max_key: an upper bound on the maximum key that will ever be inserted.
"""

from typing import Any, List, Tuple, Dict, Optional
import math


class RadixHeap:

    def __init__(self, max_key: int):
        self._last_extracted = 0
        self._size = 0
        self._node_map: Dict[Any, Tuple[int, int]] = {}  # node → (priority, bucket_index)

        # number of buckets (standard: floor(log2(max)) + 2)
        self._B = math.floor(math.log2(max_key)) + 2 if max_key > 0 else 2
        self._buckets: List[List[Tuple[Any, int]]] = [[] for _ in range(self._B)]

        # bucket bounds u[i]
        self._u: List[int] = [0] * self._B
        self._recompute_bounds()

    # INSERT
    def insert(self, node: Any, priority: int) -> None:
        if priority < self._last_extracted:
            raise ValueError(
                f"Cannot insert priority {priority} < last extracted {self._last_extracted}"
            )
        if node in self._node_map:
            raise ValueError(f"Node {node!r} already present; use decrease_key.")

        b = self._bucket_index(priority)
        self._buckets[b].append((node, priority))
        self._node_map[node] = (priority, b)
        self._size += 1

    # EXTRACT MIN
    def extract_min(self) -> Tuple[Optional[Any], Optional[int]]:
        if self._size == 0:
            return None, None

        # ensure bucket 0 has something valid
        if not self._buckets[0]:
            self._refill_bucket_0()

        # now bucket 0 must contain reachable elements
        min_node = None
        min_prio = None

        for (node, prio) in self._buckets[0]:
            cur_prio, _ = self._node_map.get(node, (None, None))
            if cur_prio == prio:
                if min_prio is None or prio < min_prio:
                    min_prio = prio
                    min_node = node

        if min_node is None:
            # all were stale; clear and try again
            self._buckets[0].clear()
            return self.extract_min()

        # remove winner
        del self._node_map[min_node]
        self._size -= 1

        # update monotonic boundary
        self._last_extracted = min_prio
        self._recompute_bounds()

        return min_node, min_prio

    # DECREASE KEY
    def decrease_key(self, node: Any, new_priority: int) -> None:
        if node not in self._node_map:
            raise KeyError(f"Node {node!r} not found in heap.")

        old_priority, old_bucket = self._node_map[node]

        if new_priority >= old_priority:
            return

        if new_priority < self._last_extracted:
            raise ValueError(
                f"new_priority {new_priority} < last extracted {self._last_extracted}"
            )

        # lazy delete: just insert new entry
        b = self._bucket_index(new_priority)
        self._buckets[b].append((node, new_priority))
        self._node_map[node] = (new_priority, b)

    # IS EMPTY
    def is_empty(self) -> bool:
        return self._size == 0

    # LEN
    def __len__(self) -> int:
        return self._size

    # INTERNAL UTILITIES 
    
    def _recompute_bounds(self):
        """Recompute bucket boundaries based on last_extracted."""
        self._u[0] = self._last_extracted
        for i in range(1, self._B):
            self._u[i] = self._last_extracted + (1 << (i - 1)) 

    def _bucket_index(self, prio: int) -> int:
        # find smallest b such that prio < u[b+1]
        for b in range(self._B - 1):
            if prio < self._u[b + 1]:
                return b
        return self._B - 1

    def _refill_bucket_0(self) -> None:
        """Move next valid min element(s) down to bucket 0."""

        # find next nonempty bucket
        i = 1
        while i < self._B and not self._buckets[i]:
            i += 1

        if i == self._B:
            raise RuntimeError(
                "RadixHeap: internal error, no buckets have elements but size>0"
            )

        # find minimum priority in bucket i
        items = self._buckets[i]
        min_prio = min(
            prio
            for node, prio in items
            if self._node_map.get(node, (None, None))[0] == prio
        )

        # update last_extracted and bounds
        self._last_extracted = min_prio
        self._recompute_bounds()

        # redistribute bucket i
        self._buckets[i] = []
        for (node, prio) in items:
            cur_prio, _ = self._node_map.get(node, (None, None))
            if cur_prio != prio:
                continue
            b = self._bucket_index(prio)
            self._buckets[b].append((node, prio))
            self._node_map[node] = (prio, b)

        # NO RECURSION. If bucket 0 still empty, something else will fill it
        # on the next extract_min call. No infinite loop.

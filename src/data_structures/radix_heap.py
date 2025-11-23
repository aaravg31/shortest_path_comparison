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

        # node -> (priority, bucket_index)
        self._node_map: Dict[Any, Tuple[int, int]] = {}

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

        # ensure bucket 0 has candidates
        if not self._buckets[0]:
            self._refill_bucket_0()

        # bucket 0 contains keys == current minimal key;
        # just pop until we find a live entry
        while self._buckets[0]:
            node, prio = self._buckets[0].pop()
            cur_prio, _ = self._node_map.get(node, (None, None))
            if cur_prio == prio:
                # this is the current best entry for this node
                del self._node_map[node]
                self._size -= 1

                # NOTE: we do NOT recompute bounds here.
                # Bounds only change when we refill from a higher bucket.
                self._last_extracted = prio
                return node, prio

        # If we drained bucket 0 but only saw stale entries,
        # try refilling again (rare, but possible with many lazy decreases).
        if self._size == 0:
            return None, None

        # After refill, try once more; if it still fails, something is wrong.
        self._refill_bucket_0()
        while self._buckets[0]:
            node, prio = self._buckets[0].pop()
            cur_prio, _ = self._node_map.get(node, (None, None))
            if cur_prio == prio:
                del self._node_map[node]
                self._size -= 1
                self._last_extracted = prio
                return node, prio

        # Should not reach here if invariants hold.
        raise RuntimeError("RadixHeap: no valid minimum found despite size > 0")

    # DECREASE KEY
    def decrease_key(self, node: Any, new_priority: int) -> None:
        if node not in self._node_map:
            raise KeyError(f"Node {node!r} not found in heap.")

        old_priority, _ = self._node_map[node]

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
    
    # CONTAINS
    def __contains__(self, node: Any) -> bool:
        return node in self._node_map

    # INTERNAL UTILITIES

    def _recompute_bounds(self) -> None:
        """Recompute bucket boundaries based on last_extracted."""
        base = self._last_extracted
        self._u[0] = base
        for i in range(1, self._B):
            self._u[i] = base + (1 << (i - 1))

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
            # no buckets have elements, so heap should be empty
            if self._size == 0:
                return
            raise RuntimeError(
                "RadixHeap: internal error, no buckets have elements but size>0"
            )

        items = self._buckets[i]

        # find minimum priority in bucket i among live entries
        min_prio = None
        for node, prio in items:
            cur_prio, _ = self._node_map.get(node, (None, None))
            if cur_prio == prio:
                if min_prio is None or prio < min_prio:
                    min_prio = prio

        if min_prio is None:
            # bucket i had only stale entries; clear and try again
            self._buckets[i] = []
            self._refill_bucket_0()
            return

        # update last_extracted and bounds
        self._last_extracted = min_prio
        self._recompute_bounds()

        # redistribute bucket i
        self._buckets[i] = []
        for node, prio in items:
            cur_prio, _ = self._node_map.get(node, (None, None))
            if cur_prio != prio:
                continue
            b = self._bucket_index(prio)
            self._buckets[b].append((node, prio))
            self._node_map[node] = (prio, b)

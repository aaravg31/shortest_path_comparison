"""
Fibonacci Min Heap

Implements:
- insert(node, priority)
- extract_min() -> (node, priority) or (None, None) if empty
- decrease_key(node, new_priority)
- is_empty() -> bool
- __len__() -> number of items

Notes
-----
- Stores a collection of heap-ordered trees linked in a circular list.
- Optimized for amortized performance:
  * Insert and Decrease-Key: O(1) amortized
  * Extract-Min: O(log n) amortized
- Each node is represented by a FibNode with parent/child pointers.
"""

import math
from typing import Any, Optional


class FibNode:
    def __init__(self, node: Any, key: float):
        self.node = node
        self.key = key
        self.parent: Optional["FibNode"] = None
        self.child: Optional["FibNode"] = None
        self.left: "FibNode" = self
        self.right: "FibNode" = self
        self.degree = 0
        self.mark = False


class FibonacciHeap:
    def __init__(self):
        self.min: Optional[FibNode] = None
        self.count = 0
        self.nodes = {}

    # INSERT
    def insert(self, node: Any, priority: float) -> None:
        if node in self.nodes:
            raise ValueError(f"Node {node!r} already present in heap.")
        new_node = FibNode(node, priority)
        self._merge_with_root_list(new_node)
        if self.min is None or new_node.key < self.min.key:
            self.min = new_node
        self.nodes[node] = new_node
        self.count += 1

    # EXTRACT MIN
    def extract_min(self):
        z = self.min
        if z is None:
            return None, None

        if z.child is not None:
            for x in list(self._iterate(z.child)):
                self._merge_with_root_list(x)
                x.parent = None

        self._remove_from_list(z)
        del self.nodes[z.node]
        self.count -= 1

        if z == z.right:
            self.min = None
        else:
            self.min = z.right
            self._consolidate()

        return z.node, z.key

    # DECREASE KEY
    def decrease_key(self, node: Any, new_key: float) -> None:
        x = self.nodes.get(node)
        if x is None:
            raise KeyError(f"Node {node!r} not found.")
        if new_key >= x.key:
            return

        x.key = new_key
        y = x.parent
        if y and x.key < y.key:
            self._cut(x, y)
            self._cascading_cut(y)
        if x.key < self.min.key:
            self.min = x

    # IS EMPTY
    def is_empty(self) -> bool:
        return self.min is None

    # LEN
    def __len__(self) -> int:
        return self.count
    
    # CONTAINS
    def __contains__(self, node: Any) -> bool:
        return node in self.nodes

    # INTERNAL UTILITIES
    def _merge_with_root_list(self, node: FibNode) -> None:
        if self.min is None:
            node.left = node.right = node
            self.min = node
        else:
            node.left = self.min
            node.right = self.min.right
            self.min.right.left = node
            self.min.right = node

    def _remove_from_list(self, node: FibNode) -> None:
        node.left.right = node.right
        node.right.left = node.left

    def _iterate(self, head: FibNode):
        node = head
        flag = False
        while True:
            if node == head and flag:
                break
            flag = True
            yield node
            node = node.right

    def _link(self, y: FibNode, x: FibNode) -> None:
        self._remove_from_list(y)
        y.parent = x
        if x.child is None:
            x.child = y
            y.left = y.right = y
        else:
            y.left = x.child
            y.right = x.child.right
            x.child.right.left = y
            x.child.right = y
        x.degree += 1
        y.mark = False

    def _consolidate(self) -> None:
        max_degree = int(math.log(self.count, 2)) + 2
        A = [None] * max_degree

        for w in list(self._iterate(self.min)):
            x = w
            d = x.degree
            while A[d] is not None:
                y = A[d]
                if x.key > y.key:
                    x, y = y, x
                self._link(y, x)
                A[d] = None
                d += 1
            A[d] = x

        self.min = None
        for i in range(max_degree):
            if A[i] is not None:
                if self.min is None:
                    self.min = A[i]
                    A[i].left = A[i].right = A[i]
                else:
                    self._merge_with_root_list(A[i])
                    if A[i].key < self.min.key:
                        self.min = A[i]

    def _cut(self, x: FibNode, y: FibNode) -> None:
        if y.child == x:
            if x.right != x:
                y.child = x.right
            else:
                y.child = None
        self._remove_from_list(x)
        y.degree -= 1
        self._merge_with_root_list(x)
        x.parent = None
        x.mark = False

    def _cascading_cut(self, y: FibNode) -> None:
        z = y.parent
        if z:
            if not y.mark:
                y.mark = True
            else:
                self._cut(y, z)
                self._cascading_cut(z)

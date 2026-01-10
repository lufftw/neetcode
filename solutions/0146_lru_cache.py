# solutions/0146_lru_cache.py
"""
Problem: LRU Cache
https://leetcode.com/problems/lru-cache/

Design a data structure that follows the constraints of a Least Recently
Used (LRU) cache.

Implement the LRUCache class:
- LRUCache(int capacity) Initialize the cache with positive capacity
- int get(int key) Return the value if key exists, otherwise return -1
- void put(int key, int value) Update or insert the value. If capacity
  exceeded, evict the least recently used key.

Both get and put must run in O(1) average time complexity.

Constraints:
- 1 <= capacity <= 3000
- 0 <= key <= 10^4
- 0 <= value <= 10^5
- At most 2 * 10^5 calls to get and put
"""
from typing import List, Optional
from collections import OrderedDict

SOLUTIONS = {
    "default": {
        "class": "LRUCacheOrderedDict",
        "method": "_run_operations",
        "complexity": "O(1) per operation",
        "description": "OrderedDict with move_to_end for recency tracking",
    },
    "manual": {
        "class": "LRUCacheManual",
        "method": "_run_operations",
        "complexity": "O(1) per operation",
        "description": "HashMap + Doubly linked list implementation",
    },
}


class LRUCacheOrderedDict:
    """
    OrderedDict-based implementation leveraging Python's built-in.

    OrderedDict maintains insertion order and provides O(1) move_to_end
    operation. When accessing a key, we move it to the end (most recent).
    When evicting, we remove from the front (least recent).

    This is the idiomatic Python solution, hiding complexity behind
    a well-optimized standard library data structure.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: OrderedDict = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        # Move to end to mark as most recently used
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update existing and move to end
            self.cache.move_to_end(key)
        self.cache[key] = value

        # Evict least recently used if over capacity
        if len(self.cache) > self.capacity:
            # popitem(last=False) removes from front (oldest)
            self.cache.popitem(last=False)

    def _run_operations(
        self, operations: List[str], arguments: List[List]
    ) -> List[Optional[int]]:
        """Execute operations and return results."""
        results: List[Optional[int]] = [None]  # Constructor returns null

        for op, args in zip(operations[1:], arguments[1:]):
            if op == "get":
                results.append(self.get(args[0]))
            elif op == "put":
                self.put(args[0], args[1])
                results.append(None)

        return results


class DLLNode:
    """Doubly linked list node for manual LRU implementation."""

    def __init__(self, key: int = 0, val: int = 0):
        self.key = key
        self.val = val
        self.prev: Optional[DLLNode] = None
        self.next: Optional[DLLNode] = None


class LRUCacheManual:
    """
    Manual implementation with HashMap and Doubly Linked List.

    The hash map provides O(1) key lookup. The doubly linked list
    maintains access order with O(1) insertion, deletion, and move
    operations. Dummy head/tail nodes simplify edge case handling.

    This demonstrates the underlying mechanism that OrderedDict
    abstracts away, useful for interviews and language-agnostic contexts.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: dict = {}  # key -> DLLNode

        # Dummy head and tail for easier list manipulation
        self.head = DLLNode()  # LRU end (oldest)
        self.tail = DLLNode()  # MRU end (newest)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: DLLNode) -> None:
        """Remove node from its current position in the list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_tail(self, node: DLLNode) -> None:
        """Add node right before tail (most recently used position)."""
        prev_node = self.tail.prev
        prev_node.next = node
        node.prev = prev_node
        node.next = self.tail
        self.tail.prev = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        node = self.cache[key]
        # Move to tail (most recently used)
        self._remove(node)
        self._add_to_tail(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update existing node
            node = self.cache[key]
            node.val = value
            self._remove(node)
            self._add_to_tail(node)
        else:
            # Create new node
            node = DLLNode(key, value)
            self.cache[key] = node
            self._add_to_tail(node)

            # Evict LRU if over capacity
            if len(self.cache) > self.capacity:
                lru = self.head.next
                self._remove(lru)
                del self.cache[lru.key]

    def _run_operations(
        self, operations: List[str], arguments: List[List]
    ) -> List[Optional[int]]:
        """Execute operations and return results."""
        results: List[Optional[int]] = [None]  # Constructor returns null

        for op, args in zip(operations[1:], arguments[1:]):
            if op == "get":
                results.append(self.get(args[0]))
            elif op == "put":
                self.put(args[0], args[1])
                results.append(None)

        return results


def judge(actual, expected, input_data: str) -> bool:
    """
    Validate LRU cache operations using OrderedDict reference.
    """
    import json

    # Parse actual if string
    if isinstance(actual, str):
        actual = json.loads(actual)

    lines = input_data.strip().split("\n")
    operations = json.loads(lines[0])
    arguments = json.loads(lines[1])

    # Simulate with OrderedDict
    capacity = arguments[0][0]
    cache = OrderedDict()
    expected_results = [None]

    for op, args in zip(operations[1:], arguments[1:]):
        if op == "get":
            if args[0] not in cache:
                expected_results.append(-1)
            else:
                cache.move_to_end(args[0])
                expected_results.append(cache[args[0]])
        elif op == "put":
            if args[0] in cache:
                cache.move_to_end(args[0])
            cache[args[0]] = args[1]
            if len(cache) > capacity:
                cache.popitem(last=False)
            expected_results.append(None)

    return actual == expected_results


JUDGE_FUNC = judge


def solve():
    import sys
    import json

    lines = sys.stdin.read().strip().split("\n")

    # Parse input: operations and arguments
    operations = json.loads(lines[0])
    arguments = json.loads(lines[1])

    # Get the solution class and instantiate with capacity
    import os

    method = os.environ.get("METHOD", "default")
    solution_info = SOLUTIONS.get(method, SOLUTIONS["default"])
    cls = globals()[solution_info["class"]]

    # First argument is [capacity]
    capacity = arguments[0][0]
    instance = cls(capacity)
    result = instance._run_operations(operations, arguments)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()

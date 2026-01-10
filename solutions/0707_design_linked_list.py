"""
Problem: Design Linked List
Link: https://leetcode.com/problems/design-linked-list/

Design a singly or doubly linked list with standard operations.

Constraints:
- 0 <= index, val <= 1000
- At most 2000 calls to get, addAtHead, addAtTail, addAtIndex, deleteAtIndex

Topics: Linked List, Design
"""
from typing import List, Optional
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "execute",
        "complexity": "O(n) per operation, O(n) space",
        "description": "Singly linked list with dummy head for uniform edge handling",
    },
}


# JUDGE_FUNC for generated tests
def _reference(operations: List[str], args: List[List]) -> List[Optional[int]]:
    """Reference implementation."""
    results = []
    ll = None  # linked list as Python list for simplicity
    for op, arg in zip(operations, args):
        if op == "MyLinkedList":
            ll = []
            results.append(None)
        elif op == "get":
            idx = arg[0]
            results.append(ll[idx] if 0 <= idx < len(ll) else -1)
        elif op == "addAtHead":
            ll.insert(0, arg[0])
            results.append(None)
        elif op == "addAtTail":
            ll.append(arg[0])
            results.append(None)
        elif op == "addAtIndex":
            idx, val = arg[0], arg[1]
            if 0 <= idx <= len(ll):
                ll.insert(idx, val)
            results.append(None)
        elif op == "deleteAtIndex":
            idx = arg[0]
            if 0 <= idx < len(ll):
                ll.pop(idx)
            results.append(None)
    return results


def judge(actual, expected, input_data: str) -> bool:
    lines = input_data.strip().split('\n')
    operations = json.loads(lines[0])
    args = json.loads(lines[1])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(operations, args)


JUDGE_FUNC = judge


class ListNode:
    """Node for singly linked list."""
    __slots__ = ['val', 'next']

    def __init__(self, val: int = 0, next: 'ListNode' = None):
        self.val = val
        self.next = next


# ============================================================================
# MyLinkedList: Singly Linked List with Dummy Head
# ============================================================================
class MyLinkedList:
    # Dummy head simplifies edge cases for addAtHead and deleteAtIndex(0).
    # Track size for O(1) bounds checking.

    def __init__(self):
        self.dummy = ListNode()  # dummy.next is actual head
        self.size = 0

    def get(self, index: int) -> int:
        """Get value at index, or -1 if invalid."""
        if index < 0 or index >= self.size:
            return -1
        curr = self.dummy.next
        for _ in range(index):
            curr = curr.next
        return curr.val

    def addAtHead(self, val: int) -> None:
        """Insert node at the beginning."""
        self.addAtIndex(0, val)

    def addAtTail(self, val: int) -> None:
        """Append node at the end."""
        self.addAtIndex(self.size, val)

    def addAtIndex(self, index: int, val: int) -> None:
        """Insert node before index. No-op if index > size."""
        if index < 0 or index > self.size:
            return
        prev = self.dummy
        for _ in range(index):
            prev = prev.next
        new_node = ListNode(val, prev.next)
        prev.next = new_node
        self.size += 1

    def deleteAtIndex(self, index: int) -> None:
        """Delete node at index if valid."""
        if index < 0 or index >= self.size:
            return
        prev = self.dummy
        for _ in range(index):
            prev = prev.next
        prev.next = prev.next.next
        self.size -= 1


# ============================================================================
# Solution wrapper for test runner
# ============================================================================
class Solution:
    def execute(self, operations: List[str], args: List[List]) -> List[Optional[int]]:
        """Execute sequence of operations on MyLinkedList."""
        results = []
        obj = None

        for op, arg in zip(operations, args):
            if op == "MyLinkedList":
                obj = MyLinkedList()
                results.append(None)
            elif op == "get":
                results.append(obj.get(arg[0]))
            elif op == "addAtHead":
                obj.addAtHead(arg[0])
                results.append(None)
            elif op == "addAtTail":
                obj.addAtTail(arg[0])
                results.append(None)
            elif op == "addAtIndex":
                obj.addAtIndex(arg[0], arg[1])
                results.append(None)
            elif op == "deleteAtIndex":
                obj.deleteAtIndex(arg[0])
                results.append(None)

        return results


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: operations (JSON array of strings)
        Line 2: arguments (JSON 2D array)

    Example:
        ["MyLinkedList","addAtHead","addAtTail","addAtIndex","get","deleteAtIndex","get"]
        [[],[1],[3],[1,2],[1],[1],[1]]
        -> [null,null,null,null,2,null,3]
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    operations = json.loads(lines[0])
    args = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.execute(operations, args)

    # Format output: null for None, compact JSON
    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

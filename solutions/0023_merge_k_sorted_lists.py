# solutions/0023_merge_k_sorted_lists.py
"""
Problem: Merge k Sorted Lists
Link: https://leetcode.com/problems/merge-k-sorted-lists/

You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.
Merge all the linked-lists into one sorted linked-list and return it.

Example 1:
    Input: lists = [[1,4,5],[1,3,4],[2,6]]
    Output: [1,1,2,3,4,4,5,6]
    Explanation: The linked-lists are:
                 [
                 1->4->5,
                 1->3->4,
                 2->6
                 ]
                 merging them into one sorted list:
                 1->1->2->3->4->4->5->6

Example 2:
    Input: lists = []
    Output: []

Example 3:
    Input: lists = [[]]
    Output: []

Constraints:
- k == lists.length
- 0 <= k <= 10^4
- 0 <= lists[i].length <= 500
- -10^4 <= lists[i][j] <= 10^4
- lists[i] is sorted in ascending order.
- The sum of lists[i].length will not exceed 10^4.

Topics: Linked List, Divide And Conquer, Heap Priority Queue, Merge Sort
"""
import ast
import json
from typing import List, Optional
from _runner import get_solver


# ============================================
# SOLUTIONS definition - tells test_runner which solutions are available
# Polymorphic pattern: each entry specifies class + method
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionHeap",
        "method": "mergeKLists",
        "complexity": "O(N log k)",
        "description": "Priority Queue (Min Heap) approach"
    },
    "heap": {
        "class": "SolutionHeap",
        "method": "mergeKLists",
        "complexity": "O(N log k)",
        "description": "Priority Queue (Min Heap) approach"
    },
    "divide": {
        "class": "SolutionDivideConquer",
        "method": "mergeKLists",
        "complexity": "O(N log k)",
        "description": "Divide and Conquer approach"
    },
    "greedy": {
        "class": "SolutionGreedy",
        "method": "mergeKLists",
        "complexity": "O(kN)",
        "description": "Greedy comparison - compare all k heads each time"
    },
}


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result by computing the expected merged sorted list.
    
    Args:
        actual: Program output (may be list or string)
        expected: Expected output (None if from generator)
        input_data: Raw input string
    
    Returns:
        bool: True if correct
    """
    # Parse input to get all values
    lines = _coerce_input_lines(input_data)
    if not lines:
        return False
    try:
        k = int(lines[0])
    except ValueError:
        return False
    
    all_values = []
    for i in range(1, k + 1):
        if i < len(lines):
            raw_line = lines[i].strip()
            if not raw_line or raw_line == 'empty':
                continue
            values = _parse_values_from_line(raw_line)
            all_values.extend(values)
    
    # Expected result: sorted merge of all lists
    correct = sorted(all_values)
    
    # Parse actual output (may be list, ListNode, or string)
    try:
        if isinstance(actual, list):
            actual_list = actual
        elif isinstance(actual, ListNode):
            actual_list = linkedlist_to_list(actual)
        else:
            actual_list = ast.literal_eval(str(actual).strip())
        return actual_list == correct
    except (ValueError, SyntaxError):
        return False


JUDGE_FUNC = judge


class ListNode:
    def __init__(self, val: int = 0, next: 'ListNode' = None):
        self.val = val
        self.next = next


import heapq


# ============================================
# Solution 1: Min Heap (Priority Queue)
# Time: O(N log k), Space: O(k)
# ============================================
class SolutionHeap:
    """
    Merge k sorted lists using a min-heap (priority queue).
    
    Each list head is pushed to the heap. We repeatedly pop the smallest,
    attach it to the result, and push its successor.
    """
    
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        # Edge case: empty input
        if not lists:
            return None

        # Min-heap: each entry is a tuple (value, list_index, node)
        # list_index is used to break ties when node values are equal
        min_heap = []

        for i, node in enumerate(lists):
            if node:
                # Push tuple (value, index, node) into heap
                # value → primary sort key
                # index → tie-breaker (avoids comparing ListNode objects)
                # node → the actual node reference
                heapq.heappush(min_heap, (node.val, i, node))

        dummy = ListNode()
        tail = dummy

        while min_heap:
            # Pop the smallest node among all current list heads
            val, i, node = heapq.heappop(min_heap)

            # Attach the node to the merged list
            tail.next = node
            tail = tail.next

            # Push the next node from the same list if available
            if node.next:
                heapq.heappush(min_heap, (node.next.val, i, node.next))

        return dummy.next


# ============================================
# Solution 2: Divide and Conquer (merge lists in pairs)
# Time: O(N log k), Space: O(1)
# ============================================
class SolutionDivideConquer:
    """
    Merge k sorted lists by repeatedly merging pairs.
    
    In each round, we merge adjacent pairs of lists, halving the count.
    After log(k) rounds, only one list remains.
    """
    
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        # Base case
        if not lists:
            return None

        while len(lists) > 1:
            k = len(lists)
            merged = []

            # Merge lists in pairs
            for i in range(0, k, 2):
                list1 = lists[i]
                list2 = lists[i + 1] if i + 1 < k else None
                merged.append(self._mergeTwoLists(list1, list2))

            lists = merged

        return lists[0]

    def _mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        """Merge two sorted linked lists."""
        dummy = ListNode()
        tail = dummy

        # Standard merge two sorted lists
        while list1 and list2:
            if list1.val <= list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next

        # Attach the remaining nodes
        tail.next = list1 if list1 else list2

        return dummy.next


# ============================================
# Solution 3: Greedy (compare all k heads each round)
# Time: O(kN), Space: O(1)
# ============================================
class SolutionGreedy:
    """
    Merge k sorted lists by comparing all k heads each time.
    
    Simple but O(kN) time - not optimal for large k.
    """
    
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        k = len(lists)

        # Base case
        if k == 0:
            return None

        dummy = ListNode()
        tail = dummy

        while True:
            # Find the smallest head among the k lists
            small = float("Inf")
            choice = -1

            for i in range(k):
                if lists[i] is None:
                    continue
                if lists[i].val < small:
                    small = lists[i].val
                    choice = i

            # No available nodes → merge complete
            if choice == -1:
                break

            # Attach the node to the result
            tail.next = lists[choice]
            tail = tail.next

            # Move the chosen list forward
            lists[choice] = lists[choice].next

        return dummy.next


def _coerce_input_lines(input_data: str) -> list[str]:
    """Normalize raw input into a list of lines."""
    raw = input_data.strip()
    if not raw:
        return []

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return raw.splitlines()

    if isinstance(parsed, list):
        return [str(item) for item in parsed]
    if isinstance(parsed, str):
        return parsed.splitlines()

    return [str(parsed)]


def _parse_values_from_line(line: str) -> list[int]:
    """Normalize a single input line into a list of integers."""
    line = line.strip()
    if not line:
        return []

    if line.startswith('[') and line.endswith(']'):
        parsed = ast.literal_eval(line)
        if isinstance(parsed, list):
            return [int(v) for v in parsed]
        raise ValueError("expected list representation")

    return [int(component.strip()) for component in line.split(',') if component.strip()]


def list_to_linkedlist(lst: List[int]) -> Optional[ListNode]:
    """Convert Python list to LinkedList."""
    if not lst:
        return None
    dummy = ListNode(0)
    current = dummy
    for val in lst:
        current.next = ListNode(val)
        current = current.next
    return dummy.next


def linkedlist_to_list(node: Optional[ListNode]) -> List[int]:
    """Convert LinkedList to Python list."""
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result


def solve():
    """
    Input format:
    First line: k (number of linked lists)
    Next k lines: values of each linked list (comma-separated; empty line = empty list)

    Example:
    3
    1,4,5
    1,3,4
    2,6
    """
    import sys

    # Parse input
    lines = _coerce_input_lines(sys.stdin.read())
    if not lines:
        print([])
        return
    k = int(lines[0])

    # Keep raw lists for shape detection, then convert to LinkedList
    raw_lists = []
    for i in range(1, k + 1):
        raw_values = []
        if i < len(lines):
            raw_line = lines[i].strip()
            if raw_line and raw_line != 'empty':
                raw_values = _parse_values_from_line(raw_line)
        raw_lists.append(raw_values)

    # Variable 'lists' holds raw data for shape inference by get_solver()
    lists = raw_lists

    # Convert to LinkedList for the actual method call
    linked_lists = [list_to_linkedlist(lst) if lst else None for lst in raw_lists]

    # Get solver - auto-reports shape of 'lists' (the raw List[List[int]])
    solver = get_solver(SOLUTIONS)
    result = solver.mergeKLists(linked_lists)

    # Output result as list
    print(linkedlist_to_list(result))


if __name__ == "__main__":
    solve()


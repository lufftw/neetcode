# solutions/0023_merge_k_sorted_lists.py
"""
Problem: Merge k Sorted Lists
Link: https://leetcode.com/problems/merge-k-sorted-lists/

You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.
Merge all the linked-lists into one sorted linked-list and return it.
"""
from typing import List, Optional
import os


# ============================================
# SOLUTIONS definition - tells test_runner which solutions are available
# ============================================
SOLUTIONS = {
    "default": {
        "method": "mergeKListsPriorityQueue",
        "complexity": "O(N log k)",
        "description": "Priority Queue (Min Heap) approach"
    },
    "heap": {
        "method": "mergeKListsPriorityQueue",
        "complexity": "O(N log k)",
        "description": "Priority Queue (Min Heap) approach"
    },
    "divide": {
        "method": "mergeKListsDivideAndConquer",
        "complexity": "O(N log k)",
        "description": "Divide and Conquer approach"
    },
    "greedy": {
        "method": "mergeKListsGreedy",
        "complexity": "O(kN)",
        "description": "Greedy comparison - compare all k heads each time"
    },
}

class ListNode:
    def __init__(self, val: int = 0, next: 'ListNode' = None):
        self.val = val
        self.next = next

import heapq
class Solution:
    # ============================================
    # Solution 1: Min Heap (Priority Queue)
    # Time: O(N log k), Space: O(k)
    # ============================================
    def mergeKListsPriorityQueue(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
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
    def mergeKListsDivideAndConquer(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
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
                merged.append(self.mergeTwoLists(list1, list2))

            lists = merged
 
        return lists[0]


    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
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
    def mergeKListsGreedy(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
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

    # Read environment variable to select which solution method to use
    method_name = os.environ.get('SOLUTION_METHOD', 'default')
    method_info = SOLUTIONS.get(method_name, SOLUTIONS['default'])
    method_func_name = method_info['method']
    
    # Parse input
    lines = sys.stdin.read().strip().split('\n')
    k = int(lines[0])

    lists = []
    for i in range(1, k + 1):
        if i < len(lines) and lines[i] and lines[i] != 'empty':
            values = list(map(int, lines[i].split(',')))
            lists.append(list_to_linkedlist(values))
        else:
            lists.append(None)

    sol = Solution()
    
    # Dynamically call the selected solution method
    method_func = getattr(sol, method_func_name)
    result = method_func(lists)

    # Output result as list
    print(linkedlist_to_list(result))


if __name__ == "__main__":
    solve()


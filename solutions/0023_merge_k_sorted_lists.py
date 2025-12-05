# solutions/0023_merge_k_sorted_lists.py
"""
題目: Merge k Sorted Lists
連結: https://leetcode.com/problems/merge-k-sorted-lists/

You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.
Merge all the linked-lists into one sorted linked-list and return it.
"""
from typing import List, Optional
import os


# ============================================
# SOLUTIONS 定義 - 告訴 test_runner 有哪些解法
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
    # 解法一：Min Heap (Priority Queue)
    # Time: O(N log k), Space: O(k)
    # ============================================
    def mergeKListsPriorityQueue(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        # Edge case: empty input list
        if not lists:
            return None
        # Min-heap: each entry is a tuple (value, list_index, node)
        # list index is used to break ties when node values are equal
        min_heap = []

        for i, node in enumerate(lists):
            if node:
                # Push tuple (value, index, node) into heap
                # value → primary sort key
                # index → tie-breaker (prevents comparing ListNode objects)
                # node → the actual node to attach
                heapq.heappush(min_heap, (node.val, i, node))

        dummy = ListNode()
        tail = dummy

        while min_heap:
            # Pop the smallest node among all current heads of the lists.
            val, i, node = heapq.heappop(min_heap)

            # Attach this node to the result list
            tail.next = node
            tail = tail.next

            # Move forward in the same list, and push the new head into heap if it exists.
            if node.next:
                heapq.heappush(min_heap, (node.next.val, i, node.next))

        return dummy.next


    # ============================================
    # 解法二：Greedy (每次比較所有 k 個頭)
    # Time: O(kN), Space: O(1)
    # ============================================
    def mergeKListsGreedy(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        k = len(lists)

        # base case
        if k == 0:
            return None
        dummy = ListNode()
        tail = dummy

        while True:
            # 找出最小, 鏈結串列往下走
            small = float("Inf")
            choice = -1
            for i in range(k):
                if lists[i] is None:
                    continue
                if lists[i].val < small:
                    small = lists[i].val
                    choice = i

            if choice == -1:
                break

            tail.next = lists[choice]
            tail = tail.next
            lists[choice] = lists[choice].next

        return dummy.next


def list_to_linkedlist(lst: List[int]) -> Optional[ListNode]:
    """將 Python list 轉換為 LinkedList"""
    if not lst:
        return None
    dummy = ListNode(0)
    current = dummy
    for val in lst:
        current.next = ListNode(val)
        current = current.next
    return dummy.next


def linkedlist_to_list(node: Optional[ListNode]) -> List[int]:
    """將 LinkedList 轉換為 Python list"""
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result


def solve():
    """
    輸入格式:
    第一行: k (linked lists 數量)
    接下來 k 行: 每個 linked list 的值 (逗號分隔，空行代表空 list)

    Example:
    3
    1,4,5
    1,3,4
    2,6
    """
    import sys

    # 讀取環境變數，決定要用哪個解法
    method_name = os.environ.get('SOLUTION_METHOD', 'default')
    method_info = SOLUTIONS.get(method_name, SOLUTIONS['default'])
    method_func_name = method_info['method']
    
    # 解析輸入
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
    
    # 動態呼叫對應的解法
    method_func = getattr(sol, method_func_name)
    result = method_func(lists)

    # 輸出格式
    print(linkedlist_to_list(result))


if __name__ == "__main__":
    solve()


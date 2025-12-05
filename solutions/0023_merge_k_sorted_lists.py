# solutions/0023_merge_k_sorted_lists.py
"""
題目: Merge k Sorted Lists
連結: https://leetcode.com/problems/merge-k-sorted-lists/

You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.
Merge all the linked-lists into one sorted linked-list and return it.
"""
from typing import Optional, List


class ListNode:
    def __init__(self, val: int = 0, next: 'ListNode' = None):
        self.val = val
        self.next = next

import heapq
class Solution:
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


def copy_linkedlist(node: Optional[ListNode]) -> Optional[ListNode]:
    """深拷貝 LinkedList"""
    if not node:
        return None
    dummy = ListNode(0)
    current = dummy
    while node:
        current.next = ListNode(node.val)
        current = current.next
        node = node.next
    return dummy.next


def copy_lists(lists: List[Optional[ListNode]]) -> List[Optional[ListNode]]:
    """深拷貝整個 linked list 陣列"""
    return [copy_linkedlist(node) for node in lists]


def solve():
    """
    輸入格式:
    第一行: k (linked list 的數量)
    接下來 k 行: 每個 linked list 的值 (逗號分隔，空串列用 empty 表示)

    Example:
    3
    1,4,5
    1,3,4
    2,6
    """
    import sys
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

    # 根據參數選擇解法
    import sys
    method = sys.argv[1] if len(sys.argv) > 1 else 'heap'

    if method == 'greedy':
        # 解法二: Greedy (O(kN))
        result = sol.mergeKListsGreedy(copy_lists(lists))
    else:
        # 解法一: Priority Queue (O(N log k)) - 預設
        result = sol.mergeKListsPriorityQueue(copy_lists(lists))

    print(linkedlist_to_list(result))


if __name__ == "__main__":
    solve()


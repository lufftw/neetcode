# solutions/0023_merge_k_sorted_lists.py
"""
題目: Merge k Sorted Lists
連結: https://leetcode.com/problems/merge-k-sorted-lists/

You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.
Merge all the linked-lists into one sorted linked-list and return it.
"""
from typing import List, Optional
import heapq
import os


# ============================================
# SOLUTIONS 定義 - 告訴 test_runner 有哪些解法
# ============================================
SOLUTIONS = {
    "default": {
        "method": "mergeKLists_heap",
        "complexity": "O(N log k)",
        "description": "Priority Queue (Min Heap) approach"
    },
    "heap": {
        "method": "mergeKLists_heap",
        "complexity": "O(N log k)",
        "description": "Priority Queue (Min Heap) approach"
    },
    "greedy": {
        "method": "mergeKLists_greedy",
        "complexity": "O(kN)",
        "description": "Greedy comparison - compare all k heads each time"
    },
    "divide": {
        "method": "mergeKLists_divide_conquer",
        "complexity": "O(N log k)",
        "description": "Divide and Conquer - merge pairs recursively"
    },
}


class ListNode:
    def __init__(self, val: int = 0, next: 'ListNode' = None):
        self.val = val
        self.next = next
    
    # 讓 heapq 可以比較 ListNode
    def __lt__(self, other):
        return self.val < other.val


class Solution:
    # ============================================
    # 解法一：Min Heap (Priority Queue)
    # Time: O(N log k), Space: O(k)
    # ============================================
    def mergeKLists_heap(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        dummy = ListNode(0)
        current = dummy
        
        # 建立 min heap，存入 (val, index, node) 避免比較問題
        heap = []
        for i, node in enumerate(lists):
            if node:
                heapq.heappush(heap, (node.val, i, node))
        
        while heap:
            val, i, node = heapq.heappop(heap)
            current.next = node
            current = current.next
            
            if node.next:
                heapq.heappush(heap, (node.next.val, i, node.next))
        
        return dummy.next
    
    # ============================================
    # 解法二：Greedy (每次比較所有 k 個頭)
    # Time: O(kN), Space: O(1)
    # ============================================
    def mergeKLists_greedy(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        dummy = ListNode(0)
        current = dummy
        
        while True:
            min_idx = -1
            min_val = float('inf')
            
            # 找出最小的頭
            for i, node in enumerate(lists):
                if node and node.val < min_val:
                    min_val = node.val
                    min_idx = i
            
            if min_idx == -1:
                break
            
            current.next = lists[min_idx]
            current = current.next
            lists[min_idx] = lists[min_idx].next
        
        return dummy.next
    
    # ============================================
    # 解法三：Divide and Conquer
    # Time: O(N log k), Space: O(log k) for recursion
    # ============================================
    def mergeKLists_divide_conquer(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists:
            return None
        if len(lists) == 1:
            return lists[0]
        
        mid = len(lists) // 2
        left = self.mergeKLists_divide_conquer(lists[:mid])
        right = self.mergeKLists_divide_conquer(lists[mid:])
        
        return self._merge_two(left, right)
    
    def _merge_two(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        current = dummy
        
        while l1 and l2:
            if l1.val <= l2.val:
                current.next = l1
                l1 = l1.next
            else:
                current.next = l2
                l2 = l2.next
            current = current.next
        
        current.next = l1 or l2
        return dummy.next


# ============================================
# 輔助函式
# ============================================
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
        if i < len(lines) and lines[i].strip():
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


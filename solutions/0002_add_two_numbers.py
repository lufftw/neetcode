# solutions/0002_add_two_numbers.py
"""
題目: Add Two Numbers
連結: https://leetcode.com/problems/add-two-numbers/

You are given two non-empty linked lists representing two non-negative integers.
The digits are stored in reverse order, and each of their nodes contains a single digit.
Add the two numbers and return the sum as a linked list.
"""
from typing import Optional, List


class ListNode:
    def __init__(self, val: int = 0, next: 'ListNode' = None):
        self.val = val
        self.next = next


class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = tail = ListNode(0)
        temp = 0

        while l1 is not None or l2 is not None or temp > 0:
            if l1 is not None:
                temp += l1.val
                l1 = l1.next
            if l2 is not None:
                temp += l2.val
                l2 = l2.next
            tail.next = ListNode(temp % 10)
            tail = tail.next
            temp = temp // 10
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
    第一行: l1 的值 (逗號分隔)
    第二行: l2 的值 (逗號分隔)

    Example:
    2,4,3
    5,6,4
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')

    # 解析 l1
    l1_values = list(map(int, lines[0].split(',')))
    # 解析 l2
    l2_values = list(map(int, lines[1].split(',')))

    # 轉換為 LinkedList
    l1 = list_to_linkedlist(l1_values)
    l2 = list_to_linkedlist(l2_values)

    sol = Solution()
    result = sol.addTwoNumbers(l1, l2)

    # 輸出格式: [7, 0, 8]
    print(linkedlist_to_list(result))


if __name__ == "__main__":
    solve()


# solutions/0002_add_two_numbers.py
"""
Problem: Add Two Numbers
Link: https://leetcode.com/problems/add-two-numbers/

You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.
You may assume the two numbers do not contain any leading zero, except the number 0 itself.

Example 1:
    <img alt="" src="https://assets.leetcode.com/uploads/2020/10/02/addtwonumber1.jpg" style="width: 483px; height: 342px;" />
    Input: l1 = [2,4,3], l2 = [5,6,4]
    Output: [7,0,8]
    Explanation: 342 + 465 = 807.

Example 2:
    Input: l1 = [0], l2 = [0]
    Output: [0]

Example 3:
    Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
    Output: [8,9,9,9,0,0,0,1]

Constraints:
- The number of nodes in each linked list is in the range [1, 100].
- 0 <= Node.val <= 9
- It is guaranteed that the list represents a number that does not have leading zeros.

Topics: Linked List, Math, Recursion
"""
from typing import Optional, List
from _runner import get_solver


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# Polymorphic pattern: each entry specifies class + method
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "addTwoNumbers",
        "complexity": "O(max(m,n)) time, O(max(m,n)) space",
        "description": "Single pass with carry handling",
    },
}


class ListNode:
    def __init__(self, val: int = 0, next: 'ListNode' = None):
        self.val = val
        self.next = next


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result by computing the expected sum.
    
    Args:
        actual: Program output (may be list or string)
        expected: Expected output (None if from generator)
        input_data: Raw input string
    
    Returns:
        bool: True if correct
    """
    import ast
    
    # Parse input
    lines = input_data.strip().split('\n')
    l1_digits = json.loads(lines[0])
    l2_digits = json.loads(lines[1])
    
    # Convert digits (reverse order) to numbers
    num1 = _digits_to_number(l1_digits)
    num2 = _digits_to_number(l2_digits)
    
    # Compute expected result
    result_sum = num1 + num2
    correct = _number_to_digits(result_sum)
    
    # Parse actual output
    try:
        if isinstance(actual, list):
            actual_list = actual
        else:
            actual_list = ast.literal_eval(str(actual).strip())
        return actual_list == correct
    except (ValueError, SyntaxError):
        return False


def _digits_to_number(digits: List[int]) -> int:
    """Convert reversed digits to number. [2,4,3] -> 342"""
    result = 0
    for i, d in enumerate(digits):
        result += d * (10 ** i)
    return result


def _number_to_digits(num: int) -> List[int]:
    """Convert number to reversed digits. 807 -> [7,0,8]"""
    if num == 0:
        return [0]
    digits = []
    while num > 0:
        digits.append(num % 10)
        num //= 10
    return digits


JUDGE_FUNC = judge


# ============================================
# Solution 1: Single Pass
# Time: O(max(m,n)), Space: O(max(m,n))
#   - Single pass through both lists
#   - Result list has at most max(m,n) + 1 nodes
# ============================================
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = tail = ListNode(0)
        carry = 0

        while l1 is not None or l2 is not None or carry > 0:
            if l1 is not None:
                carry += l1.val
                l1 = l1.next
            if l2 is not None:
                carry += l2.val
                l2 = l2.next
            tail.next = ListNode(carry % 10)
            tail = tail.next
            carry = carry // 10
        return dummy.next


# ============================================
# Helper functions for LinkedList conversion
# ============================================
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
    import json
    """
    Input format:
    Line 1: l1 values (comma-separated digits, reverse order)
    Line 2: l2 values (comma-separated digits, reverse order)

    Example:
    2,4,3
    5,6,4
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    # Parse l1
    l1_values = json.loads(lines[0])
    # Parse l2
    l2_values = json.loads(lines[1])

    # Convert to LinkedList
    l1 = list_to_linkedlist(l1_values)
    l2 = list_to_linkedlist(l2_values)

    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.addTwoNumbers(l1, l2)

    # Output format: [7, 0, 8]
    print(linkedlist_to_list(result))


if __name__ == "__main__":
    solve()

# solutions/0021_merge_two_sorted_lists.py
"""
Problem: Merge Two Sorted Lists
Link: https://leetcode.com/problems/merge-two-sorted-lists/

You are given the heads of two sorted linked lists list1 and list2.
Merge the two lists into one sorted list by splicing together the nodes
of the first two lists. Return the head of the merged linked list.

Constraints:
- The number of nodes in both lists is in the range [0, 50].
- -100 <= Node.val <= 100
- Both list1 and list2 are sorted in non-decreasing order.
"""
from typing import Optional
from _runner import get_solver


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionIterative",
        "method": "mergeTwoLists",
        "complexity": "O(m+n) time, O(1) space",
        "description": "Iterative merge using dummy head",
    },
    "iterative": {
        "class": "SolutionIterative",
        "method": "mergeTwoLists",
        "complexity": "O(m+n) time, O(1) space",
        "description": "Iterative merge using dummy head",
    },
    "recursive": {
        "class": "SolutionRecursive",
        "method": "mergeTwoLists",
        "complexity": "O(m+n) time, O(m+n) space for recursion stack",
        "description": "Recursive merge choosing smaller head",
    },
}


# ============================================================================
# Definition for singly-linked list (provided by LeetCode)
# ============================================================================

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output is correctly merged sorted list.
    
    Args:
        actual: Program output (space-separated integers as string, list, or single int)
        expected: Expected output (None if from generator)
        input_data: Raw input string (Line 1: list1, Line 2: list2)
    
    Returns:
        bool: True if correctly merged
    """
    # Parse input - preserve empty lines by splitting before strip
    lines = input_data.split('\n')
    # Handle trailing newline by removing empty last element if present
    if lines and lines[-1] == '':
        lines = lines[:-1]
    
    list1_vals = list(map(int, lines[0].split())) if lines[0].strip() else []
    list2_vals = list(map(int, lines[1].split())) if len(lines) > 1 and lines[1].strip() else []
    
    # Compute correct answer
    correct = sorted(list1_vals + list2_vals)
    
    # Parse actual output - handle int (from ast.literal_eval), str, or list
    if isinstance(actual, int):
        actual_vals = [actual]
    elif isinstance(actual, str):
        actual_vals = list(map(int, actual.strip().split())) if actual.strip() else []
    elif isinstance(actual, list):
        actual_vals = actual
    else:
        return False
    
    return actual_vals == correct


JUDGE_FUNC = judge


# ============================================
# Solution 1: Iterative Merge
# Time: O(m+n), Space: O(1)
#   - Each node visited once
#   - Only pointer references needed
#   - Optimal space complexity
# ============================================
class SolutionIterative:
    """
    Optimal iterative solution using dummy head pattern.
    
    Builds the merged list by always appending the smaller of the two
    current heads, then advancing that pointer.
    """
    
    def mergeTwoLists(self, list1: Optional[ListNode], 
                       list2: Optional[ListNode]) -> Optional[ListNode]:
        """
        Merge two sorted linked lists into one sorted list.
        
        Args:
            list1: Head of first sorted list
            list2: Head of second sorted list
            
        Returns:
            Head of merged sorted list
        """
        # DUMMY HEAD: Simplifies building the result list
        dummy: ListNode = ListNode(0)
        current: ListNode = dummy
        
        # MERGE: Compare heads and append smaller one
        while list1 and list2:
            if list1.val <= list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next
            
            current = current.next
        
        # APPEND REMAINING: One list might still have nodes
        # Since it's already sorted, just append the rest
        current.next = list1 if list1 else list2
        
        return dummy.next


# ============================================
# Solution 2: Recursive Merge
# Time: O(m+n), Space: O(m+n) recursion stack
#   - Conceptually elegant recursive structure
#   - O(m+n) stack space due to recursion depth
#   - Useful for understanding the problem
# ============================================
class SolutionRecursive:
    """
    Recursive solution.
    
    Conceptually elegant: the merged list is the smaller head followed by
    the merge of the remaining lists.
    
    Note: Uses O(m + n) stack space due to recursion depth.
    """
    
    def mergeTwoLists(self, list1: Optional[ListNode], 
                       list2: Optional[ListNode]) -> Optional[ListNode]:
        # Base cases
        if not list1:
            return list2
        if not list2:
            return list1
        
        # Recursive case: choose smaller head
        if list1.val <= list2.val:
            list1.next = self.mergeTwoLists(list1.next, list2)
            return list1
        else:
            list2.next = self.mergeTwoLists(list1, list2.next)
            return list2


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: Space-separated integers (first list)
        Line 2: Space-separated integers (second list)
    
    Output format:
        Merged sorted list (space-separated)
    
    Example:
        Input:
        1 2 4
        1 3 4
        Output: 1 1 2 3 4 4
    """
    import sys
    
    lines = sys.stdin.read().strip().split('\n')
    
    def build_list(values):
        if not values:
            return None
        nodes = [ListNode(v) for v in values]
        for i in range(len(nodes) - 1):
            nodes[i].next = nodes[i + 1]
        return nodes[0]
    
    values1 = list(map(int, lines[0].split())) if lines[0].strip() else []
    values2 = list(map(int, lines[1].split())) if len(lines) > 1 and lines[1].strip() else []
    
    list1 = build_list(values1)
    list2 = build_list(values2)
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.mergeTwoLists(list1, list2)
    
    # Output merged list
    output = []
    while result:
        output.append(str(result.val))
        result = result.next
    
    print(' '.join(output) if output else '')


if __name__ == "__main__":
    solve()

# solutions/0141_linked_list_cycle.py
"""
Problem: Linked List Cycle
Link: https://leetcode.com/problems/linked-list-cycle/

Given head, the head of a linked list, determine if the linked list has a cycle
in it. A cycle exists if some node can be reached again by continuously
following the next pointer.

Constraints:
- The number of the nodes in the list is in the range [0, 10^4]
- -10^5 <= Node.val <= 10^5
- pos is -1 or a valid index in the linked-list
"""
from typing import Optional
from _runner import get_solver


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# Polymorphic pattern: each entry specifies class + method
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionFloyd",
        "method": "hasCycle",
        "complexity": "O(n) time, O(1) space",
        "description": "Floyd's cycle detection (fast-slow pointers)",
    },
    "floyd": {
        "class": "SolutionFloyd",
        "method": "hasCycle",
        "complexity": "O(n) time, O(1) space",
        "description": "Floyd's cycle detection (fast-slow pointers)",
    },
    "hashset": {
        "class": "SolutionHashSet",
        "method": "hasCycle",
        "complexity": "O(n) time, O(n) space",
        "description": "Hash set to track visited nodes",
    },
}


# ============================================================================
# Definition for singly-linked list (provided by LeetCode)
# ============================================================================

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output correctly detects cycle.
    
    Args:
        actual: Program output ("true" or "false" as string)
        expected: Expected output (None if from generator)
        input_data: Raw input string (Line 1: node values, Line 2: cycle position)
    
    Returns:
        bool: True if correct cycle detection
    """
    lines = input_data.strip().split('\n')
    values = list(map(int, lines[0].split())) if lines[0] else []
    pos = int(lines[1]) if len(lines) > 1 else -1
    
    # Build linked list
    if not values:
        has_cycle = False
    else:
        nodes = [ListNode(v) for v in values]
        for i in range(len(nodes) - 1):
            nodes[i].next = nodes[i + 1]
        if pos >= 0 and pos < len(nodes):
            nodes[-1].next = nodes[pos]
            has_cycle = True
        else:
            has_cycle = False
    
    # Parse actual output
    actual_str = str(actual).strip().lower()
    actual_bool = actual_str == "true"
    
    return actual_bool == has_cycle


JUDGE_FUNC = judge


# ============================================
# Solution 1: Floyd's Cycle Detection
# Time: O(n), Space: O(1)
#   - Fast pointer traverses at most 2n nodes
#   - Only two pointer references needed
#   - Optimal space complexity
# ============================================
class SolutionFloyd:
    """
    Optimal solution using Floyd's Tortoise and Hare algorithm.
    
    This is the standard O(1) space solution for cycle detection.
    Alternative approaches using a hash set would require O(n) space.
    """
    
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        """
        Detect if linked list contains a cycle.
        
        Args:
            head: Head of the linked list
            
        Returns:
            True if the list has a cycle
        """
        # Handle empty list and single node without cycle
        if not head or not head.next:
            return False
        
        # INITIALIZE: Both pointers start at head
        slow: Optional[ListNode] = head
        fast: Optional[ListNode] = head
        
        # TRAVERSE: Fast moves 2x speed of slow
        while fast and fast.next:
            slow = slow.next           # Move slow by 1
            fast = fast.next.next      # Move fast by 2
            
            # CHECK: If they meet, cycle exists
            if slow == fast:
                return True
        
        # TERMINATION: Fast reached end → no cycle
        return False


# ============================================
# Solution 2: HashSet Approach
# Time: O(n), Space: O(n)
#   - Tracks all visited nodes in a set
#   - Simpler logic but uses O(n) extra space
#   - Useful for understanding the problem
# ============================================
class SolutionHashSet:
    """
    Alternative using a hash set to track visited nodes.
    
    Simpler logic but uses O(n) extra space.
    Useful for understanding the problem or when modifying nodes is allowed.
    """
    
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        visited: set = set()
        current: Optional[ListNode] = head
        
        while current:
            if current in visited:
                return True
            visited.add(current)
            current = current.next
        
        return False


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: Space-separated integers (node values)
        Line 2: Position where cycle begins (-1 if no cycle)
    
    Output format:
        "true" or "false"
    
    Example:
        Input:
        3 2 0 -4
        1
        Output: true
    """
    import sys
    
    lines = sys.stdin.read().strip().split('\n')
    values = list(map(int, lines[0].split())) if lines[0] else []
    pos = int(lines[1]) if len(lines) > 1 else -1
    
    # Build linked list
    if not values:
        print("false")
        return
    
    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    
    # Create cycle if pos >= 0
    if pos >= 0 and pos < len(nodes):
        nodes[-1].next = nodes[pos]
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.hasCycle(nodes[0])
    
    print("true" if result else "false")


if __name__ == "__main__":
    solve()

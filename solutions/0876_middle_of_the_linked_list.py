# solutions/0876_middle_of_the_linked_list.py
"""
================================================================================
LeetCode 876: Middle of the Linked List
================================================================================

Problem: Given the head of a singly linked list, return the middle node.
         If there are two middle nodes, return the second middle node.

API Kernel: TwoPointersTraversal
Pattern: fast_slow_midpoint
Family: linked_list_traversal

--------------------------------------------------------------------------------
TWO POINTERS PATTERN: FAST–SLOW (MIDPOINT FINDING)
--------------------------------------------------------------------------------

This is a classic application of fast-slow pointers for finding the midpoint.

Key Insight:
    When fast reaches the end, slow is at the middle.
    - Fast moves 2× speed of slow
    - When fast travels n nodes, slow travels n/2 nodes
    - So when fast reaches end, slow is at midpoint

For Even-Length Lists:
    The problem asks for the SECOND middle node.
    With our termination condition (while fast and fast.next), we get:
    - List [1,2,3,4]: slow stops at node 3 (second middle)
    - List [1,2,3,4,5]: slow stops at node 3 (exact middle)

INVARIANT: slow is always at the midpoint of the traversed portion.

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(n) - Single pass with fast moving 2× speed
Space: O(1) - Only two pointer references

================================================================================
"""
from typing import Optional
from _runner import get_solver


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# Polymorphic pattern: each entry specifies class + method
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionFastSlow",
        "method": "middleNode",
        "complexity": "O(n) time, O(1) space",
        "description": "Fast-slow pointers for midpoint finding",
    },
    "fast_slow": {
        "class": "SolutionFastSlow",
        "method": "middleNode",
        "complexity": "O(n) time, O(1) space",
        "description": "Fast-slow pointers for midpoint finding",
    },
    "two_pass": {
        "class": "SolutionTwoPass",
        "method": "middleNode",
        "complexity": "O(n) time, O(1) space",
        "description": "Two-pass: count nodes then find middle",
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
    Validate result: check if actual output is the middle node values.
    
    Args:
        actual: Program output (space-separated integers as string)
        expected: Expected output (None if from generator)
        input_data: Raw input string (space-separated node values)
    
    Returns:
        bool: True if correct middle node values
    """
    line = input_data.strip()
    values = list(map(int, line.split())) if line else []
    
    if not values:
        correct = []
    else:
        # Middle index for even length: second middle (len//2)
        mid_idx = len(values) // 2
        correct = values[mid_idx:]
    
    # Parse actual output
    if isinstance(actual, str):
        actual_vals = list(map(int, actual.strip().split())) if actual.strip() else []
    elif isinstance(actual, list):
        actual_vals = actual
    else:
        return False
    
    return actual_vals == correct


JUDGE_FUNC = judge


# ============================================
# Solution 1: Fast-Slow Pointers
# Time: O(n), Space: O(1)
#   - Single pass with fast moving 2× speed
#   - When fast reaches end, slow is at middle
#   - Optimal single-pass approach
# ============================================
class SolutionFastSlow:
    """
    Optimal solution using fast-slow pointers for midpoint finding.
    
    The fast pointer travels twice as fast as slow. When fast reaches
    the end, slow is at the middle (or second middle for even length).
    """
    
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Find the middle node of the linked list.
        
        Args:
            head: Head of the linked list
            
        Returns:
            Middle node (second middle if two middle nodes)
        """
        # INITIALIZE: Both pointers start at head
        slow: Optional[ListNode] = head
        fast: Optional[ListNode] = head
        
        # TRAVERSE: Fast moves 2 steps, slow moves 1 step
        while fast and fast.next:
            slow = slow.next           # Move slow by 1
            fast = fast.next.next      # Move fast by 2
        
        # When fast reaches end, slow is at middle
        return slow


# ============================================
# Solution 2: Two-Pass Approach
# Time: O(n), Space: O(1)
#   - First pass: count nodes O(n)
#   - Second pass: find middle O(n)
#   - More straightforward but requires two traversals
# ============================================
class SolutionTwoPass:
    """
    Alternative using two passes: count nodes, then find middle.
    
    More straightforward but requires two traversals.
    """
    
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # First pass: count nodes
        count = 0
        current = head
        while current:
            count += 1
            current = current.next
        
        # Second pass: find middle
        middle_index = count // 2
        current = head
        for _ in range(middle_index):
            current = current.next
        
        return current


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: Space-separated integers (node values)
    
    Output format:
        Values from middle node to end (space-separated)
    
    Example:
        Input:  1 2 3 4 5
        Output: 3 4 5
    """
    import sys
    
    line = sys.stdin.read().strip()
    values = list(map(int, line.split())) if line else []
    
    if not values:
        return
    
    # Build linked list
    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.middleNode(nodes[0])
    
    # Output remaining values from middle to end
    output = []
    while result:
        output.append(str(result.val))
        result = result.next
    
    print(' '.join(output))


if __name__ == "__main__":
    solve()

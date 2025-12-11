# solutions/0141_linked_list_cycle.py
"""
================================================================================
LeetCode 141: Linked List Cycle
================================================================================

Problem: Given head, the head of a linked list, determine if the linked list
         has a cycle in it. A cycle exists if some node can be reached again
         by continuously following the next pointer.

API Kernel: TwoPointersTraversal
Pattern: fast_slow_cycle_detection
Family: linked_list_cycle

--------------------------------------------------------------------------------
TWO POINTERS PATTERN: FAST–SLOW (FLOYD'S CYCLE DETECTION)
--------------------------------------------------------------------------------

This is the canonical fast-slow pointer pattern for cycle detection,
also known as Floyd's Tortoise and Hare algorithm.

Pointer Movement:
- SLOW: Moves 1 node per iteration
- FAST: Moves 2 nodes per iteration

INVARIANT: If no cycle, fast reaches null. If cycle exists, fast eventually
           catches slow inside the cycle.

Why This Works:
    If there's a cycle of length C, once both pointers enter the cycle:
    - The gap between fast and slow decreases by 1 each step
    - They must meet within C steps
    
    If there's no cycle:
    - Fast reaches the end (null) before they can meet

Mathematical Proof:
    Let the cycle length be C. When slow enters the cycle, fast is already
    inside at some position. The distance between them (measured in the
    direction of travel) decreases by 1 each step, so they meet in ≤C steps.

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(n) - Fast traverses at most 2n nodes
Space: O(1) - Only two pointer references

================================================================================
"""
from typing import Optional


# ============================================================================
# Definition for singly-linked list (provided by LeetCode)
# ============================================================================

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


# ============================================================================
# Solution - O(n) Floyd's Cycle Detection
# ============================================================================

class Solution:
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


# ============================================================================
# Alternative: Using Hash Set (O(n) Space)
# ============================================================================

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
# Alternative: Destructive Marking (Not Recommended)
# ============================================================================

class SolutionDestructive:
    """
    Alternative that marks visited nodes by modifying them.
    
    Warning: This modifies the original list, which may not be acceptable.
    Shown for educational purposes only.
    """
    
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        VISITED_MARKER = float('inf')
        current = head
        
        while current:
            if current.val == VISITED_MARKER:
                return True
            current.val = VISITED_MARKER
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
    
    solution = Solution()
    result = solution.hasCycle(nodes[0])
    
    print("true" if result else "false")


if __name__ == "__main__":
    solve()


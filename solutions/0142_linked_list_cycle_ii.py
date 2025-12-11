# solutions/0142_linked_list_cycle_ii.py
"""
================================================================================
LeetCode 142: Linked List Cycle II
================================================================================

Problem: Given the head of a linked list, return the node where the cycle begins.
         If there is no cycle, return null.

API Kernel: TwoPointersTraversal
Pattern: fast_slow_cycle_start
Family: linked_list_cycle

--------------------------------------------------------------------------------
TWO POINTERS PATTERN: FAST–SLOW (FLOYD'S ALGORITHM - PHASE 2)
--------------------------------------------------------------------------------

This problem extends basic cycle detection to find the cycle's starting node.

DELTA from Linked List Cycle (LeetCode 141):
- Phase 1 (same): Detect if cycle exists by finding meeting point
- Phase 2 (new): Find the cycle start using mathematical properties

INVARIANT: If cycle exists, meeting point is a fixed distance from cycle start.

Why Phase 2 Works (Mathematical Proof):
    Let:
    - F = distance from head to cycle start
    - C = cycle length
    - a = distance from cycle start to meeting point
    
    When they meet:
    - Slow traveled: F + a
    - Fast traveled: F + a + kC (for some integer k ≥ 1)
    - Fast traveled 2× slow: 2(F + a) = F + a + kC
    - Therefore: F + a = kC, which means F = kC - a = (k-1)C + (C - a)
    
    This means: starting from head and from meeting point, if both move at
    speed 1, they will meet at the cycle start after F steps.

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(n) - Phase 1: O(n), Phase 2: O(n)
Space: O(1) - Only pointer references

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
# Solution - O(n) Floyd's Algorithm (Two Phases)
# ============================================================================

class Solution:
    """
    Optimal solution using Floyd's algorithm with two phases.
    
    Phase 1: Detect if cycle exists and find meeting point
    Phase 2: Find cycle start using the mathematical property
    """
    
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Find the node where the cycle begins, or None if no cycle.
        
        Args:
            head: Head of the linked list
            
        Returns:
            The node where cycle begins, or None
        """
        # ==== PHASE 1: Detect cycle and find meeting point ====
        slow: Optional[ListNode] = head
        fast: Optional[ListNode] = head
        
        # Find meeting point (if cycle exists)
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            
            if slow == fast:
                # Cycle detected, proceed to phase 2
                break
        else:
            # No cycle (fast reached end)
            return None
        
        # ==== PHASE 2: Find cycle start ====
        # Reset one pointer to head, keep other at meeting point
        # Move both at same speed - they meet at cycle start
        finder: Optional[ListNode] = head
        
        while finder != slow:
            finder = finder.next
            slow = slow.next
        
        return finder


# ============================================================================
# Alternative: Using Hash Set (O(n) Space)
# ============================================================================

class SolutionHashSet:
    """
    Alternative using a hash set to track visited nodes.
    
    Returns the first node seen twice (cycle start).
    Simpler but uses O(n) extra space.
    """
    
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        visited: set = set()
        current: Optional[ListNode] = head
        
        while current:
            if current in visited:
                return current  # First revisited node is cycle start
            visited.add(current)
            current = current.next
        
        return None


# ============================================================================
# Alternative: Detailed Phase 1 with Early Exit
# ============================================================================

class SolutionDetailed:
    """
    More explicit version with clear phase separation.
    
    Includes early termination checks and detailed comments.
    """
    
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Edge cases
        if not head or not head.next:
            return None
        
        # Phase 1: Find meeting point
        slow, fast = head, head
        has_cycle = False
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            
            if slow == fast:
                has_cycle = True
                break
        
        if not has_cycle:
            return None
        
        # Phase 2: Find entry point
        # Key insight: distance from head to entry = distance from meeting to entry
        entry_finder = head
        
        while entry_finder != slow:
            entry_finder = entry_finder.next
            slow = slow.next
        
        return entry_finder


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: Space-separated integers (node values)
        Line 2: Position where cycle begins (-1 if no cycle)
    
    Output format:
        Index of cycle start node, or -1 if no cycle
    
    Example:
        Input:
        3 2 0 -4
        1
        Output: 1
    """
    import sys
    
    lines = sys.stdin.read().strip().split('\n')
    values = list(map(int, lines[0].split())) if lines[0] else []
    pos = int(lines[1]) if len(lines) > 1 else -1
    
    # Build linked list
    if not values:
        print(-1)
        return
    
    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    
    # Create cycle if pos >= 0
    if pos >= 0 and pos < len(nodes):
        nodes[-1].next = nodes[pos]
    
    solution = Solution()
    result = solution.detectCycle(nodes[0])
    
    # Find index of result node
    if result is None:
        print(-1)
    else:
        for i, node in enumerate(nodes):
            if node == result:
                print(i)
                break


if __name__ == "__main__":
    solve()


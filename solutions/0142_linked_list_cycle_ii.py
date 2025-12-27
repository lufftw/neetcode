# solutions/0142_linked_list_cycle_ii.py
"""
Problem: Linked List Cycle II
Link: https://leetcode.com/problems/linked-list-cycle-ii/

Given the head of a linked list, return the node where the cycle begins. If there is no cycle, return null.
There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the next pointer. Internally, pos is used to denote the index of the node that tail's next pointer is connected to (0-indexed). It is -1 if there is no cycle. Note that pos is not passed as a parameter.
Do not modify the linked list.

Example 1:
    <img alt="" src="https://assets.leetcode.com/uploads/2018/12/07/circularlinkedlist.png" style="height: 145px; width: 450px;" />
    Input: head = [3,2,0,-4], pos = 1
    Output: tail connects to node index 1
    Explanation: There is a cycle in the linked list, where tail connects to the second node.

Example 2:
    <img alt="" src="https://assets.leetcode.com/uploads/2018/12/07/circularlinkedlist_test2.png" style="height: 105px; width: 201px;" />
    Input: head = [1,2], pos = 0
    Output: tail connects to node index 0
    Explanation: There is a cycle in the linked list, where tail connects to the first node.

Example 3:
    <img alt="" src="https://assets.leetcode.com/uploads/2018/12/07/circularlinkedlist_test3.png" style="height: 65px; width: 65px;" />
    Input: head = [1], pos = -1
    Output: no cycle
    Explanation: There is no cycle in the linked list.

Constraints:
- The number of the nodes in the list is in the range [0, 10^4].
- -10^5 <= Node.val <= 10^5
- pos is -1 or a valid index in the linked-list.

Topics: Hash Table, Linked List, Two Pointers

Follow-up: Can you solve it using O(1) (i.e. constant) memory?
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
        "method": "detectCycle",
        "complexity": "O(n) time, O(1) space",
        "description": "Floyd's algorithm with two phases",
    },
    "floyd": {
        "class": "SolutionFloyd",
        "method": "detectCycle",
        "complexity": "O(n) time, O(1) space",
        "description": "Floyd's algorithm with two phases",
    },
    "hashset": {
        "class": "SolutionHashSet",
        "method": "detectCycle",
        "complexity": "O(n) time, O(n) space",
        "description": "Hash set to find first revisited node",
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
    Validate result: check if actual output is the correct cycle start index.
    
    Args:
        actual: Program output (integer as string or int, or -1 for no cycle)
        expected: Expected output (None if from generator)
        input_data: Raw input string (Line 1: node values, Line 2: cycle position)
    
    Returns:
        bool: True if correct cycle start index
    """
    lines = input_data.strip().split('\n')
    values = list(map(int, lines[0].split())) if lines[0] else []
    pos = int(lines[1]) if len(lines) > 1 else -1
    
    # Build linked list
    if not values:
        correct_pos = -1
    else:
        nodes = [ListNode(v) for v in values]
        for i in range(len(nodes) - 1):
            nodes[i].next = nodes[i + 1]
        if pos >= 0 and pos < len(nodes):
            nodes[-1].next = nodes[pos]
            correct_pos = pos
        else:
            correct_pos = -1
    
    # Parse actual output
    try:
        actual_val = int(actual) if not isinstance(actual, int) else actual
        return actual_val == correct_pos
    except (ValueError, TypeError):
        return False


JUDGE_FUNC = judge


# ============================================
# Solution 1: Floyd's Algorithm (Two Phases)
# Time: O(n), Space: O(1)
#   - Phase 1: Detect cycle and find meeting point O(n)
#   - Phase 2: Find cycle start O(n)
#   - Only pointer references needed
# ============================================
class SolutionFloyd:
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


# ============================================
# Solution 2: HashSet Approach
# Time: O(n), Space: O(n)
#   - Tracks visited nodes in a set
#   - Returns first node seen twice (cycle start)
#   - Simpler logic but uses O(n) extra space
# ============================================
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
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.detectCycle(nodes[0])
    
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

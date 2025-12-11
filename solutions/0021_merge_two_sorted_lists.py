# solutions/0021_merge_two_sorted_lists.py
"""
================================================================================
LeetCode 21: Merge Two Sorted Lists
================================================================================

Problem: You are given the heads of two sorted linked lists list1 and list2.
         Merge the two lists into one sorted list by splicing together the nodes
         of the first two lists. Return the head of the merged linked list.

API Kernel: TwoPointersTraversal
Pattern: merge_sorted_sequences
Family: merge_pattern

--------------------------------------------------------------------------------
TWO POINTERS PATTERN: MERGE SORTED SEQUENCES
--------------------------------------------------------------------------------

This is the canonical merge pattern for two sorted sequences.

Two Approaches:
1. ITERATIVE: Use a dummy head and build the merged list node by node
2. RECURSIVE: Recursively choose the smaller head and merge remaining

INVARIANT: At each step, the next node in the merged list is the smaller of
           the two current nodes being compared.

Key Insight:
    Both lists are already sorted. The smallest unprocessed element is always
    at the head of one of the two remaining lists. Compare heads, take smaller,
    and advance that list's pointer.

Why Dummy Node:
    Using a dummy node simplifies edge cases. We don't need special handling
    for initializing the merged list's head — we just return dummy.next.

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(m + n) - Each node visited once
Space: O(1) iterative, O(m + n) recursive (call stack)

================================================================================
"""
from typing import Optional


# ============================================================================
# Definition for singly-linked list (provided by LeetCode)
# ============================================================================

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ============================================================================
# Solution - O(m + n) Iterative Merge
# ============================================================================

class Solution:
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


# ============================================================================
# Alternative: Recursive Merge
# ============================================================================

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
# Alternative: In-Place Merge (Reusing Nodes)
# ============================================================================

class SolutionInPlace:
    """
    Explicit in-place merge that reuses existing nodes.
    
    Same approach as main solution but with clearer variable naming
    showing that we're splicing existing nodes.
    """
    
    def mergeTwoLists(self, list1: Optional[ListNode], 
                       list2: Optional[ListNode]) -> Optional[ListNode]:
        # Sentinel node to start the merged list
        sentinel = ListNode(-1)
        prev = sentinel
        
        # Two pointers for the input lists
        ptr1, ptr2 = list1, list2
        
        while ptr1 and ptr2:
            if ptr1.val <= ptr2.val:
                prev.next = ptr1  # Link to existing node
                ptr1 = ptr1.next
            else:
                prev.next = ptr2
                ptr2 = ptr2.next
            prev = prev.next
        
        # Attach remaining list
        prev.next = ptr1 or ptr2
        
        return sentinel.next


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
    
    solution = Solution()
    result = solution.mergeTwoLists(list1, list2)
    
    # Output merged list
    output = []
    while result:
        output.append(str(result.val))
        result = result.next
    
    print(' '.join(output) if output else '')


if __name__ == "__main__":
    solve()


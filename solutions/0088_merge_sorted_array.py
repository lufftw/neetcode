# solutions/0088_merge_sorted_array.py
"""
================================================================================
LeetCode 88: Merge Sorted Array
================================================================================

Problem: You are given two integer arrays nums1 and nums2, sorted in non-decreasing
         order, and two integers m and n, representing the number of elements in
         nums1 and nums2 respectively.
         
         Merge nums1 and nums2 into a single array sorted in non-decreasing order.
         The final sorted array should be stored inside nums1.
         
         nums1 has length m + n, where the last n elements are 0 and should be ignored.

API Kernel: TwoPointersTraversal
Pattern: merge_sorted_in_place
Family: merge_pattern

--------------------------------------------------------------------------------
TWO POINTERS PATTERN: MERGE IN-PLACE (WRITE FROM END)
--------------------------------------------------------------------------------

This problem requires in-place merging where the destination array already
contains the first input array.

Key Insight:
    If we write from the BEGINNING, we would overwrite elements of nums1
    before processing them. Instead, write from the END:
    - Compare largest elements from both arrays
    - Write the larger one to the end position
    - Move backwards

Three Pointers:
- i: Points to last element of nums1's actual elements (m-1)
- j: Points to last element of nums2 (n-1)
- write: Points to last position of nums1 (m+n-1)

INVARIANT: nums1[write+1:] is sorted and contains the largest elements from both arrays.

Why Write From End Works:
    The "empty" space in nums1 (indices m to m+n-1) is exactly where we can
    safely write. By writing largest elements first, we never overwrite
    unprocessed elements.

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(m + n) - Each element processed once
Space: O(1) - In-place modification

================================================================================
"""
from typing import List


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output is correctly merged sorted array.
    
    Args:
        actual: Program output (space-separated integers as string)
        expected: Expected output (None if from generator)
        input_data: Raw input string (Line 1: nums1, Line 2: m, Line 3: nums2, Line 4: n)
    
    Returns:
        bool: True if correctly merged
    """
    lines = input_data.strip().split('\n')
    nums1 = list(map(int, lines[0].split())) if lines[0] else []
    m = int(lines[1]) if len(lines) > 1 else 0
    nums2 = list(map(int, lines[2].split())) if len(lines) > 2 and lines[2].strip() else []
    n = int(lines[3]) if len(lines) > 3 else 0
    
    # Extract actual elements from nums1 (first m elements)
    nums1_actual = nums1[:m] if m > 0 else []
    
    # Compute correct answer
    correct = sorted(nums1_actual + nums2)
    
    # Parse actual output
    if isinstance(actual, str):
        actual_vals = list(map(int, actual.strip().split())) if actual.strip() else []
    elif isinstance(actual, list):
        actual_vals = actual
    else:
        return False
    
    return actual_vals == correct


JUDGE_FUNC = judge


# ============================================================================
# Solution - O(m + n) Merge from End
# ============================================================================

class Solution:
    """
    Optimal in-place merge by writing from the end.
    
    By processing largest elements first and writing to the back of nums1,
    we avoid overwriting unprocessed elements.
    """
    
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Merge nums2 into nums1 in-place.
        
        Args:
            nums1: First sorted array with extra space at end
            m: Number of actual elements in nums1
            nums2: Second sorted array
            n: Number of elements in nums2
        """
        # POINTERS: Start from the end of actual elements
        i: int = m - 1           # Last element in nums1's actual data
        j: int = n - 1           # Last element in nums2
        write: int = m + n - 1   # Last position in nums1
        
        # MERGE: Write largest elements from the end
        while j >= 0:
            # If nums1 has elements left and its current is larger
            if i >= 0 and nums1[i] > nums2[j]:
                nums1[write] = nums1[i]
                i -= 1
            else:
                # nums2's current is larger (or nums1 exhausted)
                nums1[write] = nums2[j]
                j -= 1
            
            write -= 1
        
        # Note: If i >= 0 after loop, remaining nums1 elements are already in place


# ============================================================================
# Alternative: Explicit While Loops
# ============================================================================

class SolutionExplicit:
    """
    Alternative with explicit handling of both exhaustion cases.
    
    More verbose but clearer about all cases.
    """
    
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        i, j, write = m - 1, n - 1, m + n - 1
        
        # Merge while both arrays have elements
        while i >= 0 and j >= 0:
            if nums1[i] > nums2[j]:
                nums1[write] = nums1[i]
                i -= 1
            else:
                nums1[write] = nums2[j]
                j -= 1
            write -= 1
        
        # Copy remaining elements from nums2 (if any)
        # No need to copy from nums1 - elements are already in place
        while j >= 0:
            nums1[write] = nums2[j]
            j -= 1
            write -= 1


# ============================================================================
# Alternative: Using Slice Assignment
# ============================================================================

class SolutionSlice:
    """
    Pythonic solution using slicing.
    
    Less efficient due to sorting, but very concise.
    """
    
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        # Copy nums2 to the empty space in nums1
        nums1[m:m + n] = nums2
        # Sort the entire array
        nums1.sort()


# ============================================================================
# Alternative: Two-Pointer Forward (Requires Extra Space)
# ============================================================================

class SolutionForward:
    """
    Forward merge requiring extra space.
    
    Standard merge like merge sort, but needs to copy nums1 first.
    Shown for comparison with the optimal backward approach.
    """
    
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        # Copy nums1's actual elements
        nums1_copy = nums1[:m]
        
        # Merge forward
        i, j, write = 0, 0, 0
        
        while i < m and j < n:
            if nums1_copy[i] <= nums2[j]:
                nums1[write] = nums1_copy[i]
                i += 1
            else:
                nums1[write] = nums2[j]
                j += 1
            write += 1
        
        # Copy remaining
        while i < m:
            nums1[write] = nums1_copy[i]
            i += 1
            write += 1
        
        while j < n:
            nums1[write] = nums2[j]
            j += 1
            write += 1


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: Space-separated integers (nums1 with trailing zeros)
        Line 2: Integer m (actual elements in nums1)
        Line 3: Space-separated integers (nums2)
        Line 4: Integer n (elements in nums2)
    
    Output format:
        Merged sorted array
    
    Example:
        Input:
        1 2 3 0 0 0
        3
        2 5 6
        3
        Output: 1 2 2 3 5 6
    """
    import sys
    
    lines = sys.stdin.read().strip().split('\n')
    nums1 = list(map(int, lines[0].split()))
    m = int(lines[1])
    nums2 = list(map(int, lines[2].split())) if lines[2].strip() else []
    n = int(lines[3])
    
    solution = Solution()
    solution.merge(nums1, m, nums2, n)
    
    print(' '.join(map(str, nums1)))


if __name__ == "__main__":
    solve()


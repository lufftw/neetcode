# solutions/0088_merge_sorted_array.py
"""
Problem: Merge Sorted Array
Link: https://leetcode.com/problems/merge-sorted-array/

You are given two integer arrays nums1 and nums2, sorted in non-decreasing order, and two integers m and n, representing the number of elements in nums1 and nums2 respectively.
Merge nums1 and nums2 into a single array sorted in non-decreasing order.
The final sorted array should not be returned by the function, but instead be stored inside the array nums1. To accommodate this, nums1 has a length of m + n, where the first m elements denote the elements that should be merged, and the last n elements are set to 0 and should be ignored. nums2 has a length of n.

Example 1:
    Input: nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
    Output: [1,2,2,3,5,6]
    Explanation: The arrays we are merging are [1,2,3] and [2,5,6].
                 The result of the merge is [1,2,2,3,5,6] with the underlined elements coming from nums1.

Example 2:
    Input: nums1 = [1], m = 1, nums2 = [], n = 0
    Output: [1]
    Explanation: The arrays we are merging are [1] and [].
                 The result of the merge is [1].

Example 3:
    Input: nums1 = [0], m = 0, nums2 = [1], n = 1
    Output: [1]
    Explanation: The arrays we are merging are [] and [1].
                 The result of the merge is [1].
                 Note that because m = 0, there are no elements in nums1. The 0 is only there to ensure the merge result can fit in nums1.

Constraints:
- nums1.length == m + n
- nums2.length == n
- 0 <= m, n <= 200
- 1 <= m + n <= 200
- -10^9 <= nums1[i], nums2[j] <= 10^9

Topics: Array, Two Pointers, Sorting

Hint 1: You can easily solve this problem if you simply think about two elements at a time rather than two arrays. We know that each of the individual arrays is sorted. What we don't know is how they will intertwine. Can we take a local decision and arrive at an optimal solution?

Hint 2: If you simply consider one element each at a time from the two arrays and make a decision and proceed accordingly, you will arrive at the optimal solution.

Follow-up: Can you come up with an algorithm that runs in O(m + n) time?
"""
from typing import List
from _runner import get_solver


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionBackward",
        "method": "merge",
        "complexity": "O(m+n) time, O(1) space",
        "description": "Merge from end to avoid overwriting unprocessed elements",
        "api_kernels": ["MergeSortedSequences"],
        "patterns": ["merge_sorted_from_ends"],
    },
    "backward": {
        "class": "SolutionBackward",
        "method": "merge",
        "complexity": "O(m+n) time, O(1) space",
        "description": "Merge from end to avoid overwriting unprocessed elements",
        "api_kernels": ["MergeSortedSequences"],
        "patterns": ["merge_sorted_from_ends"],
    },
    "forward": {
        "class": "SolutionForward",
        "method": "merge",
        "complexity": "O(m+n) time, O(m) space",
        "description": "Forward merge requiring extra space for nums1 copy",
        "api_kernels": ["MergeSortedSequences"],
        "patterns": ["merge_two_sorted_arrays"],
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output is correctly merged sorted array.
    
    Args:
        actual: Program output (space-separated integers as string, list, or single int)
        expected: Expected output (None if from generator)
        input_data: Raw input string (Line 1: nums1, Line 2: m, Line 3: nums2, Line 4: n)
    
    Returns:
        bool: True if correctly merged
    """
    import json
    # Parse input - preserve empty lines by splitting before strip
    lines = input_data.split('\n')
    # Handle trailing newline by removing empty last element if present
    while lines and lines[-1] == '':
        lines.pop()
    
    nums1 = json.loads(lines[0]) if lines[0].strip() else []
    m = int(lines[1]) if len(lines) > 1 and lines[1].strip() else 0
    nums2 = json.loads(lines[2]) if len(lines) > 2 and lines[2].strip() else []
    n = int(lines[3]) if len(lines) > 3 and lines[3].strip() else 0
    
    # Extract actual elements from nums1 (first m elements)
    nums1_actual = nums1[:m] if m > 0 else []
    
    # Compute correct answer
    correct = sorted(nums1_actual + nums2)
    
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
# Solution 1: Merge from End
# Time: O(m+n), Space: O(1)
#   - Write largest elements first from the end
#   - Never overwrites unprocessed elements
#   - Optimal space complexity
# ============================================
class SolutionBackward:
    """
    Optimal in-place merge by writing from the end.
    
    By processing largest elements first and writing to the back of nums1,
    we avoid overwriting unprocessed elements.
    """
    
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Merge nums2 into nums1 in-place.

        Core insight: Write from end to avoid overwriting unprocessed elements.
        Place largest elements first; remaining nums1 elements are already in place.

        Invariant: nums1[write+1:] contains the largest elements in sorted order.

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


# ============================================
# Solution 2: Forward Merge with Extra Space
# Time: O(m+n), Space: O(m)
#   - Requires copy of nums1's actual elements
#   - Standard forward merge like merge sort
#   - Simpler logic but uses extra space
# ============================================
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
    import json
    
    lines = sys.stdin.read().strip().split('\n')
    nums1 = json.loads(lines[0])
    m = int(lines[1])
    nums2 = json.loads(lines[2]) if lines[2].strip() else []
    n = int(lines[3])
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    solver.merge(nums1, m, nums2, n)
    
    print(json.dumps(nums1, separators=(',', ':')))


if __name__ == "__main__":
    solve()

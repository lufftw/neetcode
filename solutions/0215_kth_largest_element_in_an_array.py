# solutions/0215_kth_largest_element_in_an_array.py
"""
Problem: Kth Largest Element in an Array
Link: https://leetcode.com/problems/kth-largest-element-in-an-array/

Given an integer array nums and an integer k, return the kth largest element in the array.
Note that it is the kth largest element in the sorted order, not the kth distinct element.
Can you solve it without sorting?

Example 1:
    Input: nums = [3,2,1,5,6,4], k = 2
    Output: 5

Example 2:
    Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
    Output: 4

Constraints:
- 1 <= k <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4

Topics: Array, Divide And Conquer, Sorting, Heap Priority Queue, Quickselect
"""
from typing import List
import random
from _runner import get_solver


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# Polymorphic pattern: each entry specifies class + method
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionQuickselect",
        "method": "findKthLargest",
        "complexity": "O(n) average time, O(1) space",
        "description": "Quickselect algorithm with random pivot",
    },
    "quickselect": {
        "class": "SolutionQuickselect",
        "method": "findKthLargest",
        "complexity": "O(n) average time, O(1) space",
        "description": "Quickselect algorithm with random pivot",
    },
    "heap": {
        "class": "SolutionHeap",
        "method": "findKthLargest",
        "complexity": "O(n log k) time, O(k) space",
        "description": "Min-heap of size k to maintain k largest elements",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output is the kth largest element.
    
    Args:
        actual: Program output (integer as string or int)
        expected: Expected output (None if from generator)
        input_data: Raw input string (Line 1: nums, Line 2: k)
    
    Returns:
        bool: True if correct kth largest element
    """
    lines = input_data.strip().split('\n')
    nums = list(map(int, lines[0].split())) if lines[0] else []
    k = int(lines[1]) if len(lines) > 1 else 1
    
    # Compute correct answer
    correct = _brute_force_kth_largest(nums, k)
    
    try:
        actual_val = int(actual) if not isinstance(actual, int) else actual
        return actual_val == correct
    except (ValueError, TypeError):
        return False


def _brute_force_kth_largest(nums: List[int], k: int) -> int:
    """O(n log n) brute force solution for verification."""
    sorted_nums = sorted(nums, reverse=True)
    return sorted_nums[k - 1]


JUDGE_FUNC = judge


# ============================================
# Solution 1: Quickselect Algorithm
# Time: O(n) average, O(n²) worst, Space: O(1)
#   - Uses partition scheme from quicksort
#   - Random pivot selection for expected O(n) performance
#   - In-place partitioning
# ============================================
class SolutionQuickselect:
    """
    Optimal solution using Quickselect algorithm.
    
    Uses random pivot selection to achieve expected O(n) time complexity.
    """
    
    def findKthLargest(self, nums: List[int], k: int) -> int:
        """
        Find the kth largest element in the array.
        
        Args:
            nums: Array of integers
            k: Position (1-indexed) of element to find when sorted descending
            
        Returns:
            The kth largest element
        """
        
        def partition(left: int, right: int) -> int:
            """
            Partition array around a random pivot (descending order).
            
            Returns the final position of the pivot.
            """
            # Random pivot selection for expected O(n) performance
            pivot_idx = random.randint(left, right)
            pivot_value = nums[pivot_idx]
            
            # Move pivot to end
            nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]
            
            # Partition: elements >= pivot go to the left
            store_idx = left
            for i in range(left, right):
                if nums[i] >= pivot_value:  # >= for descending order
                    nums[store_idx], nums[i] = nums[i], nums[store_idx]
                    store_idx += 1
            
            # Move pivot to final position
            nums[store_idx], nums[right] = nums[right], nums[store_idx]
            
            return store_idx
        
        # Convert k to 0-indexed position for kth largest
        target_idx = k - 1
        left, right = 0, len(nums) - 1
        
        while left <= right:
            pivot_idx = partition(left, right)
            
            if pivot_idx == target_idx:
                return nums[pivot_idx]
            elif pivot_idx < target_idx:
                left = pivot_idx + 1
            else:
                right = pivot_idx - 1
        
        return nums[left]  # Should never reach here


# ============================================
# Solution 2: Heap-Based Solution
# Time: O(n log k), Space: O(k)
#   - Maintains min-heap of size k
#   - Root is the kth largest element
#   - Better when k is small relative to n
# ============================================
class SolutionHeap:
    """
    Alternative using a min-heap of size k.
    
    Maintains the k largest elements seen so far in a min-heap.
    The root of the heap is the kth largest element.
    
    Time: O(n log k)
    Space: O(k)
    """
    
    def findKthLargest(self, nums: List[int], k: int) -> int:
        import heapq
        
        # Use negative values for max-heap behavior (or use min-heap of size k)
        min_heap = []
        
        for num in nums:
            if len(min_heap) < k:
                heapq.heappush(min_heap, num)
            elif num > min_heap[0]:
                heapq.heapreplace(min_heap, num)
        
        return min_heap[0]


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: Space-separated integers (array)
        Line 2: Integer k
    
    Output format:
        The kth largest element
    
    Example:
        Input:
        3 2 1 5 6 4
        2
        Output: 5
    """
    import sys
    
    lines = sys.stdin.read().strip().split('\n')
    nums = list(map(int, lines[0].split()))
    k = int(lines[1])
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.findKthLargest(nums, k)
    
    print(result)


if __name__ == "__main__":
    solve()

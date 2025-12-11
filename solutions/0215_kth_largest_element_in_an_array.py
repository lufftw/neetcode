# solutions/0215_kth_largest_element_in_an_array.py
"""
================================================================================
LeetCode 215: Kth Largest Element in an Array
================================================================================

Problem: Given an integer array nums and an integer k, return the kth largest
         element in the array. Note that it is the kth largest element in the
         sorted order, not the kth distinct element.

API Kernel: TwoPointersTraversal
Pattern: quickselect_partition
Family: selection_algorithms

--------------------------------------------------------------------------------
TWO POINTERS PATTERN: QUICKSELECT (PARTITION-BASED SELECTION)
--------------------------------------------------------------------------------

This problem demonstrates the Quickselect algorithm, which uses the partition
scheme from Quicksort to find the kth element in expected O(n) time.

Core Idea:
    The partition operation places the pivot in its final sorted position.
    After partitioning:
    - If pivot position == k-1: pivot is the kth largest
    - If pivot position < k-1: search right side
    - If pivot position > k-1: search left side

Partition Invariant:
    After partition around pivot:
    - Elements in [low, pivot_idx) are ≥ pivot
    - Elements in (pivot_idx, high] are < pivot
    (For kth largest, we use descending order logic)

Why This Works:
    Each partition eliminates roughly half the candidates on average,
    leading to expected O(n) time: n + n/2 + n/4 + ... = O(2n) = O(n).

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(n) average, O(n²) worst case
Space: O(1) - In-place partitioning

To guarantee O(n) worst case: use median-of-medians for pivot selection.

================================================================================
"""
from typing import List
import random


# ============================================================================
# Solution - O(n) Average Quickselect
# ============================================================================

class Solution:
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


# ============================================================================
# Alternative: Heap-Based Solution
# ============================================================================

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
# Alternative: Sort-Based Solution
# ============================================================================

class SolutionSort:
    """
    Simple sorting approach.
    
    Sort the array and return the kth element from the end.
    
    Time: O(n log n)
    Space: O(1) or O(n) depending on sort implementation
    """
    
    def findKthLargest(self, nums: List[int], k: int) -> int:
        nums.sort(reverse=True)
        return nums[k - 1]


# ============================================================================
# Alternative: Counting Sort (When Values Bounded)
# ============================================================================

class SolutionCounting:
    """
    Counting approach for bounded value ranges.
    
    If values are bounded (e.g., -10^4 to 10^4), count occurrences
    and find kth element by counting down from max.
    
    Time: O(n + range)
    Space: O(range)
    """
    
    def findKthLargest(self, nums: List[int], k: int) -> int:
        min_val = min(nums)
        max_val = max(nums)
        
        # Shift values to be non-negative
        offset = -min_val
        count = [0] * (max_val - min_val + 1)
        
        for num in nums:
            count[num + offset] += 1
        
        # Count from largest to find kth
        remaining = k
        for val in range(max_val, min_val - 1, -1):
            remaining -= count[val + offset]
            if remaining <= 0:
                return val
        
        return min_val


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
    
    solution = Solution()
    result = solution.findKthLargest(nums, k)
    
    print(result)


if __name__ == "__main__":
    solve()


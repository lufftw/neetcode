# solutions/0015_3sum.py
"""
Problem: 3Sum
Link: https://leetcode.com/problems/3sum/

Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.
Notice that the solution set must not contain duplicate triplets.

Example 1:
    Input: nums = [-1,0,1,2,-1,-4]
    Output: [[-1,-1,2],[-1,0,1]]
    Explanation: nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
                 nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
                 nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
                 The distinct triplets are [-1,0,1] and [-1,-1,2].
                 Notice that the order of the output and the order of the triplets does not matter.

Example 2:
    Input: nums = [0,1,1]
    Output: []
    Explanation: The only possible triplet does not sum up to 0.

Example 3:
    Input: nums = [0,0,0]
    Output: [[0,0,0]]
    Explanation: The only possible triplet sums up to 0.

Constraints:
- 3 <= nums.length <= 3000
- -10^5 <= nums[i] <= 10^5

Topics: Array, Two Pointers, Sorting

Hint 1: So, we essentially need to find three numbers x, y, and z such that they add up to the given value. If we fix one of the numbers say x, we are left with the two-sum problem at hand!

Hint 2: For the two-sum problem, if we fix one of the numbers, say x, we have to scan the entire array to find the next number y, which is value - x where value is the input parameter. Can we change our array somehow so that this search becomes faster?

Hint 3: The second train of thought for two-sum is, without changing the array, can we use additional space somehow? Like maybe a hash map to speed up the search?
"""
from typing import List
from _runner import get_solver


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# Polymorphic pattern: each entry specifies class + method
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionTwoPointers",
        "method": "threeSum",
        "complexity": "O(n²) time, O(1) extra space",
        "description": "Sort + two pointers with duplicate skipping",
    },
    "two_pointers": {
        "class": "SolutionTwoPointers",
        "method": "threeSum",
        "complexity": "O(n²) time, O(1) extra space",
        "description": "Sort + two pointers with duplicate skipping",
    },
    "hashset": {
        "class": "SolutionHashSet",
        "method": "threeSum",
        "complexity": "O(n²) time, O(n) space for set",
        "description": "Sort + two pointers using set for deduplication",
    },
    "hash": {
        "class": "SolutionHash",
        "method": "threeSum",
        "complexity": "O(n²) time, O(n) space",
        "description": "Hash-based two-sum for each element, no two-pointer",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output contains all unique triplets summing to 0.
    
    Args:
        actual: Program output (may be string with newlines or list)
        expected: Expected output (None if from generator)
        input_data: Raw input string (canonical JSON format)
    
    Returns:
        bool: True if all triplets are valid and complete
    """
    import json
    
    line = input_data.strip()
    # Parse input: support both canonical JSON and legacy space-separated
    if line.startswith('['):
        nums = json.loads(line)
    else:
        nums = json.loads(line) if line else []
    
    # Parse actual output
    if isinstance(actual, str):
        actual = actual.strip()
        # Try JSON parse first
        if actual.startswith('['):
            try:
                parsed = json.loads(actual)
                if isinstance(parsed, list) and all(isinstance(t, list) for t in parsed):
                    actual_triplets = [tuple(sorted(t)) for t in parsed if len(t) == 3]
                else:
                    actual_triplets = []
            except json.JSONDecodeError:
                actual_triplets = []
        else:
            # Legacy format: space-separated lines
            lines = actual.split('\n')
            actual_triplets = []
            for l in lines:
                if l.strip():
                    triplet = list(map(int, l.strip().split()))
                    if len(triplet) == 3:
                        actual_triplets.append(tuple(sorted(triplet)))
    elif isinstance(actual, list):
        actual_triplets = [tuple(sorted(t)) for t in actual if len(t) == 3]
    else:
        return False
    
    # Compute correct answer
    correct_triplets = _brute_force_3sum(nums)
    correct_set = set(tuple(sorted(t)) for t in correct_triplets)
    actual_set = set(actual_triplets)
    
    # Check if sets match
    return actual_set == correct_set and len(actual_triplets) == len(actual_set)


def _brute_force_3sum(nums: List[int]) -> List[List[int]]:
    """O(n³) brute force solution for verification."""
    n = len(nums)
    if n < 3:
        return []
    
    result_set = set()
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    triplet = tuple(sorted([nums[i], nums[j], nums[k]]))
                    result_set.add(triplet)
    
    return [list(t) for t in result_set]


JUDGE_FUNC = judge


# ============================================
# Solution 1: Sort + Two Pointers with Deduplication
# Time: O(n²), Space: O(1) extra
#   - O(n log n) sorting + O(n²) nested iteration
#   - In-place duplicate skipping without extra space
#   - Most efficient space usage
# ============================================
class SolutionTwoPointers:
    """
    Optimal solution using sorting and two-pointer technique.
    
    The key insight is that sorting enables both efficient pair search
    and systematic duplicate avoidance.
    """
    
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """
        Find all unique triplets that sum to zero.

        Core insight: Sorting enables both efficient two-pointer pair search
        and systematic duplicate avoidance via skip logic.

        Invariant: All unique triplets with first element < nums[i] have been found.

        Args:
            nums: List of integers

        Returns:
            List of triplets [a, b, c] where a + b + c = 0
        """
        n: int = len(nums)
        if n < 3:
            return []
        
        # SORT: Enable two-pointer search and deduplication
        nums.sort()
        
        result: List[List[int]] = []
        
        # OUTER LOOP: Fix the first element
        for i in range(n - 2):
            # DEDUP: Skip duplicate first elements
            # Must check i > 0 to avoid index out of bounds
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            
            # PRUNING: Early termination if smallest sum > 0
            # nums[i] is smallest in remaining array; if nums[i] > 0,
            # no triplet starting here can sum to 0
            if nums[i] > 0:
                break
            
            # PRUNING: Skip if largest possible sum < 0
            if nums[i] + nums[n - 2] + nums[n - 1] < 0:
                continue
            
            # TWO POINTERS: Find pairs summing to -nums[i]
            target: int = -nums[i]
            left: int = i + 1
            right: int = n - 1
            
            while left < right:
                current_sum: int = nums[left] + nums[right]
                
                if current_sum == target:
                    # FOUND: Record triplet
                    result.append([nums[i], nums[left], nums[right]])
                    
                    # DEDUP: Skip duplicate second elements
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    # DEDUP: Skip duplicate third elements
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    
                    # Move both pointers after recording
                    left += 1
                    right -= 1
                    
                elif current_sum < target:
                    # Sum too small: need larger values
                    left += 1
                else:
                    # Sum too large: need smaller values
                    right -= 1
        
        return result


# ============================================
# Solution 2: Sort + Two Pointers with HashSet Deduplication
# Time: O(n²), Space: O(n) for set
#   - Uses set to handle deduplication automatically
#   - Simpler logic but higher space usage
#   - Useful when duplicate-skipping logic is error-prone
# ============================================
class SolutionHashSet:
    """
    Alternative using a set to handle deduplication.
    
    Simpler logic but slightly higher space usage due to set overhead.
    Useful when the duplicate-skipping logic is error-prone.
    """
    
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        n: int = len(nums)
        result_set: set = set()
        
        for i in range(n - 2):
            if nums[i] > 0:
                break
            
            target: int = -nums[i]
            left, right = i + 1, n - 1
            
            while left < right:
                current_sum = nums[left] + nums[right]
                
                if current_sum == target:
                    # Use tuple for hashability
                    result_set.add((nums[i], nums[left], nums[right]))
                    left += 1
                    right -= 1
                elif current_sum < target:
                    left += 1
                else:
                    right -= 1
        
        return [list(triplet) for triplet in result_set]


# ============================================
# Solution 3: Hash-based Two-Sum Approach
# Time: O(n²), Space: O(n)
#   - For each element, solve two-sum using hash set
#   - No two-pointer technique, pure hash lookup
#   - Alternative paradigm: extends Two-Sum pattern
# ============================================
class SolutionHash:
    """
    Hash-based approach: reduce to Two-Sum for each fixed element.

    Key insight: For each nums[i], find pairs (nums[j], nums[k]) where
    j > i and nums[j] + nums[k] = -nums[i]. Use hash set for O(1) lookup.

    Trade-off: Same O(n²) time but different paradigm than two-pointer.
    Useful when array is not sorted or sorting is undesirable.
    """

    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """
        Find all unique triplets using hash-based two-sum.

        Core insight: Fix first element, then solve two-sum on remaining
        elements using a hash set for complement lookup.

        Args:
            nums: List of integers

        Returns:
            List of triplets [a, b, c] where a + b + c = 0
        """
        n = len(nums)
        if n < 3:
            return []

        # Sort for consistent triplet ordering and deduplication
        nums.sort()
        result: List[List[int]] = []

        for i in range(n - 2):
            # Skip duplicate first elements
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            # Early termination: smallest element > 0
            if nums[i] > 0:
                break

            # Two-Sum using hash set
            target = -nums[i]
            seen = set()

            j = i + 1
            while j < n:
                complement = target - nums[j]

                if complement in seen:
                    result.append([nums[i], complement, nums[j]])
                    # Skip duplicates for third element
                    while j + 1 < n and nums[j] == nums[j + 1]:
                        j += 1

                seen.add(nums[j])
                j += 1

        return result


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format (canonical JSON):
        Line 1: nums as JSON array
    
    Output format:
        JSON array of triplets
    
    Example:
        Input:  [-1,0,1,2,-1,-4]
        Output: [[-1,-1,2],[-1,0,1]]
    """
    import sys
    import json
    
    line = sys.stdin.read().strip()
    nums = json.loads(line)
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.threeSum(nums)
    
    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

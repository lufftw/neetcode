# solutions/0202_happy_number.py
"""
Problem: Happy Number
Link: https://leetcode.com/problems/happy-number/

Write an algorithm to determine if a number n is happy.
A happy number is a number defined by the following process:
- Starting with any positive integer, replace the number by the sum of the squares of its digits.
- Repeat the process until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1.
- Those numbers for which this process ends in 1 are happy.
Return true if n is a happy number, and false if not.

Example 1:
    Input: n = 19
    Output: true
    Explanation: 12 + 92 = 82
                 82 + 22 = 68
                 62 + 82 = 100
                 12 + 02 + 02 = 1

Example 2:
    Input: n = 2
    Output: false

Constraints:
- 1 <= n <= 2^31 - 1

Topics: Hash Table, Math, Two Pointers
"""
from _runner import get_solver


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# Polymorphic pattern: each entry specifies class + method
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionFloyd",
        "method": "isHappy",
        "complexity": "O(log n) time, O(1) space",
        "description": "Floyd's cycle detection on number sequence",
    },
    "floyd": {
        "class": "SolutionFloyd",
        "method": "isHappy",
        "complexity": "O(log n) time, O(1) space",
        "description": "Floyd's cycle detection on number sequence",
    },
    "hashset": {
        "class": "SolutionHashSet",
        "method": "isHappy",
        "complexity": "O(log n) time, O(log n) space",
        "description": "Hash set to detect cycles in sequence",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output correctly identifies happy number.
    
    Args:
        actual: Program output ("true" or "false" as string)
        expected: Expected output (None if from generator)
        input_data: Raw input string (integer n)
    
    Returns:
        bool: True if correct happy number check
    """
    n = int(input_data.strip())
    
    # Compute correct answer using set to detect cycles
    correct = _brute_force_happy(n)
    
    # Parse actual output
    actual_str = str(actual).strip().lower()
    actual_bool = actual_str == "true"
    
    return actual_bool == correct


def _brute_force_happy(n: int) -> bool:
    """Check if n is happy using set to detect cycles."""
    seen = set()
    
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(int(d) ** 2 for d in str(n))
    
    return n == 1


JUDGE_FUNC = judge


# ============================================
# Solution 1: Floyd's Cycle Detection
# Time: O(log n), Space: O(1)
#   - Treats number sequence as implicit linked list
#   - Fast pointer moves 2 steps, slow moves 1 step
#   - Only two number values stored
# ============================================
class SolutionFloyd:
    """
    Optimal solution using fast-slow pointers on the implicit sequence.
    
    Treats the number sequence as a linked list and applies Floyd's
    cycle detection algorithm.
    """
    
    def isHappy(self, n: int) -> bool:
        """
        Determine if n is a happy number.
        
        Args:
            n: Positive integer to check
            
        Returns:
            True if n is happy (sequence reaches 1)
        """
        
        def get_next(num: int) -> int:
            """Compute sum of squares of digits (the 'next' function)."""
            total: int = 0
            while num > 0:
                digit = num % 10
                total += digit * digit
                num //= 10
            return total
        
        # FAST-SLOW: Apply cycle detection to number sequence
        slow: int = n
        fast: int = get_next(n)
        
        # Continue until they meet (cycle found) or fast reaches 1
        while fast != 1 and slow != fast:
            slow = get_next(slow)           # Move slow by 1
            fast = get_next(get_next(fast)) # Move fast by 2
        
        # If fast reached 1, n is happy
        return fast == 1


# ============================================
# Solution 2: HashSet Approach
# Time: O(log n), Space: O(log n)
#   - Stores all visited numbers in a set
#   - If we see a repeat, there's a cycle
#   - If we reach 1 first, n is happy
# ============================================
class SolutionHashSet:
    """
    Alternative using a hash set to detect cycles.
    
    Store all visited numbers; if we see a repeat, there's a cycle.
    If we reach 1 first, n is happy.
    """
    
    def isHappy(self, n: int) -> bool:
        def sum_of_squares(num: int) -> int:
            total = 0
            while num > 0:
                digit = num % 10
                total += digit * digit
                num //= 10
            return total
        
        seen: set = set()
        current: int = n
        
        while current != 1 and current not in seen:
            seen.add(current)
            current = sum_of_squares(current)
        
        return current == 1


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: Integer n
    
    Output format:
        "true" or "false"
    
    Example:
        Input:  19
        Output: true
    """
    import sys
    
    n = int(sys.stdin.read().strip())
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.isHappy(n)
    
    print("true" if result else "false")


if __name__ == "__main__":
    solve()

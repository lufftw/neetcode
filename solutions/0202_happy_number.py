# solutions/0202_happy_number.py
"""
================================================================================
LeetCode 202: Happy Number
================================================================================

Problem: Write an algorithm to determine if a number n is happy.
         A happy number is defined by the following process:
         - Starting with any positive integer, replace the number by the sum
           of the squares of its digits.
         - Repeat the process until the number equals 1 (happy), or it loops
           endlessly in a cycle (not happy).

API Kernel: TwoPointersTraversal
Pattern: fast_slow_implicit_cycle
Family: number_sequence_cycle

--------------------------------------------------------------------------------
TWO POINTERS PATTERN: FAST–SLOW ON IMPLICIT LINKED LIST
--------------------------------------------------------------------------------

This problem applies the fast-slow cycle detection pattern to a number sequence.

Key Insight:
    The sequence of "sum of squares of digits" forms an implicit linked list:
    - Each number is a "node"
    - The "next" function is sum_of_squares(n)
    - If we reach 1, the sequence stays at 1 (1 → 1 → 1...)
    - If we don't reach 1, we must eventually enter a cycle

INVARIANT: The sequence either reaches 1 or enters a cycle.

Why We Can Use Fast-Slow:
    The sequence is deterministic: each number has exactly one successor.
    This is exactly the structure of a linked list with possible cycles.
    If we detect a cycle at 1, n is happy; otherwise, n is not happy.

Mathematical Note:
    For any number with d digits, the maximum sum of squares is d × 81.
    For d ≥ 4, this is less than the original number, so the sequence
    eventually stays below 243 (for any starting number).

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(log n) iterations, each O(log n) to compute sum of squares
Space: O(1) - Only two number values stored

================================================================================
"""


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


# ============================================================================
# Solution - O(log n) Fast-Slow Pointers
# ============================================================================

class Solution:
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


# ============================================================================
# Alternative: Using Hash Set (O(log n) Space)
# ============================================================================

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
# Alternative: Hardcoded Cycle Detection
# ============================================================================

class SolutionHardcoded:
    """
    Alternative using known mathematical property.
    
    For unhappy numbers, the sequence always enters a specific cycle
    containing these numbers: 4, 16, 37, 58, 89, 145, 42, 20.
    We can detect unhappiness by checking for 4.
    """
    
    def isHappy(self, n: int) -> bool:
        def sum_of_squares(num: int) -> int:
            total = 0
            while num > 0:
                digit = num % 10
                total += digit * digit
                num //= 10
            return total
        
        current = n
        
        # All unhappy sequences eventually reach 4
        while current != 1 and current != 4:
            current = sum_of_squares(current)
        
        return current == 1


# ============================================================================
# Alternative: Using String Conversion
# ============================================================================

class SolutionString:
    """
    Alternative using string conversion for digit extraction.
    
    Slightly slower due to string operations but more readable.
    """
    
    def isHappy(self, n: int) -> bool:
        def sum_of_squares(num: int) -> int:
            return sum(int(d) ** 2 for d in str(num))
        
        slow = n
        fast = sum_of_squares(n)
        
        while fast != 1 and slow != fast:
            slow = sum_of_squares(slow)
            fast = sum_of_squares(sum_of_squares(fast))
        
        return fast == 1


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
    
    solution = Solution()
    result = solution.isHappy(n)
    
    print("true" if result else "false")


if __name__ == "__main__":
    solve()


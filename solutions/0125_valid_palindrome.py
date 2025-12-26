# solutions/0125_valid_palindrome.py
"""
Problem: Valid Palindrome
Link: https://leetcode.com/problems/valid-palindrome/

A phrase is a palindrome if, after converting all uppercase letters into
lowercase letters and removing all non-alphanumeric characters, it reads the
same forward and backward.

Given a string s, return true if it is a palindrome, or false otherwise.

Sub-Pattern: Opposite pointers (symmetric check)
Key Insight: Use two pointers from both ends, skip non-alphanumeric characters,
and compare case-insensitively.

Constraints:
- 1 <= s.length <= 2 * 10^5
- s consists only of printable ASCII characters
"""
from _runner import get_solver


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# Polymorphic pattern: each entry specifies class + method
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionTwoPointers",
        "method": "isPalindrome",
        "complexity": "O(n) time, O(1) space",
        "description": "Two pointers from both ends with inline filtering",
    },
    "two_pointers": {
        "class": "SolutionTwoPointers",
        "method": "isPalindrome",
        "complexity": "O(n) time, O(1) space",
        "description": "Two pointers from both ends with inline filtering",
    },
    "filtered": {
        "class": "SolutionFiltered",
        "method": "isPalindrome",
        "complexity": "O(n) time, O(n) space",
        "description": "Pre-filter string then check palindrome",
    },
    "filtered_pointers": {
        "class": "SolutionFilteredPointers",
        "method": "isPalindrome",
        "complexity": "O(n) time, O(n) space",
        "description": "Filter first, then use two pointers on filtered string",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output correctly identifies palindrome.
    
    Args:
        actual: Program output ("true" or "false" as string)
        expected: Expected output (None if from generator)
        input_data: Raw input string
    
    Returns:
        bool: True if correct palindrome check
    """
    s = input_data.strip()
    
    # Compute correct answer
    correct = _brute_force_palindrome(s)
    
    # Parse actual output
    actual_str = str(actual).strip().lower()
    actual_bool = actual_str == "true"
    
    return actual_bool == correct


def _brute_force_palindrome(s: str) -> bool:
    """Brute force palindrome check."""
    # Filter to alphanumeric only
    filtered = ''.join(c.lower() for c in s if c.isalnum())
    return filtered == filtered[::-1]


JUDGE_FUNC = judge


# ============================================
# Solution 1: Two Pointers with Inline Filtering
# Time: O(n), Space: O(1)
#   - Each character visited at most once
#   - No extra space for filtered string
#   - Most space-efficient approach
# ============================================
class SolutionTwoPointers:
    """
    Optimal solution using opposite pointers for palindrome verification.
    
    Handles the character filtering inline without creating a cleaned string,
    which saves O(n) space.
    """
    
    def isPalindrome(self, s: str) -> bool:
        """
        Check if the string is a palindrome (alphanumeric only, case-insensitive).
        
        Args:
            s: Input string
            
        Returns:
            True if s is a valid palindrome
        """
        left: int = 0
        right: int = len(s) - 1
        
        while left < right:
            # SKIP: Advance left pointer past non-alphanumeric characters
            while left < right and not s[left].isalnum():
                left += 1
            
            # SKIP: Advance right pointer past non-alphanumeric characters
            while left < right and not s[right].isalnum():
                right -= 1
            
            # COMPARE: Check if characters match (case-insensitive)
            if s[left].lower() != s[right].lower():
                return False
            
            # MOVE: Advance both pointers toward center
            left += 1
            right -= 1
        
        return True


# ============================================
# Solution 2: Pre-Filter Approach
# Time: O(n), Space: O(n)
#   - Two passes: filter then check
#   - Uses O(n) space for filtered string
#   - Clearer logic but less space-efficient
# ============================================
class SolutionFiltered:
    """
    Alternative that first filters the string, then checks palindrome.
    
    Clearer logic but uses O(n) extra space for the filtered string.
    Useful when readability is prioritized over space efficiency.
    """
    
    def isPalindrome(self, s: str) -> bool:
        # FILTER: Create cleaned string with only alphanumeric, lowercase
        filtered: str = ''.join(c.lower() for c in s if c.isalnum())
        
        # CHECK: Compare with reverse
        return filtered == filtered[::-1]


# ============================================
# Solution 3: Filtered String with Two Pointers
# Time: O(n), Space: O(n)
#   - Filter first, then use two pointers
#   - Demonstrates separation of concerns
#   - Same space as SolutionFiltered but different approach
# ============================================
class SolutionFilteredPointers:
    """
    Hybrid approach: filter first, then use two pointers.
    
    Demonstrates separation of concerns between filtering and validation.
    """
    
    def isPalindrome(self, s: str) -> bool:
        # FILTER: Create cleaned string
        filtered: str = ''.join(c.lower() for c in s if c.isalnum())
        
        # TWO POINTERS: Check palindrome property
        left: int = 0
        right: int = len(filtered) - 1
        
        while left < right:
            if filtered[left] != filtered[right]:
                return False
            left += 1
            right -= 1
        
        return True


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: The input string
    
    Output format:
        "true" or "false"
    
    Example:
        Input:  A man, a plan, a canal: Panama
        Output: true
    """
    import sys
    
    s = sys.stdin.read().strip()
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.isPalindrome(s)
    
    print("true" if result else "false")


if __name__ == "__main__":
    solve()

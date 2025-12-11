# solutions/0680_valid_palindrome_ii.py
"""
================================================================================
LeetCode 680: Valid Palindrome II
================================================================================

Problem: Given a string s, return true if s can be a palindrome after deleting
         at most one character from it.

API Kernel: TwoPointersTraversal
Pattern: opposite_pointers_with_skip
Family: string_validation

--------------------------------------------------------------------------------
TWO POINTERS PATTERN: OPPOSITE POINTERS WITH ONE SKIP
--------------------------------------------------------------------------------

This problem extends the basic palindrome check by allowing one character removal.

DELTA from Valid Palindrome (LeetCode 125):
- When a mismatch is found, we have TWO choices: skip left or skip right
- If EITHER choice results in a valid palindrome, answer is True
- We get ONE "skip allowance" to use

Algorithm:
1. Use opposite pointers moving toward center
2. On mismatch: check if s[left+1:right+1] OR s[left:right] is a palindrome
3. If either is valid, return True; otherwise return False

INVARIANT: We have used at most one skip, and s[0:left] matches s[right+1:n]
           with the appropriate reversal.

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(n) - Main pass O(n) + at most one helper check O(n)
Space: O(1) - Only pointer indices used

================================================================================
"""


# ============================================================================
# Solution - O(n) Opposite Pointers with Skip
# ============================================================================

class Solution:
    """
    Optimal solution using opposite pointers with one allowed skip.
    
    When a mismatch is found, we branch into two possibilities and
    check if either results in a valid palindrome.
    """
    
    def validPalindrome(self, s: str) -> bool:
        """
        Check if s can become a palindrome by removing at most one character.
        
        Args:
            s: Input string (lowercase letters only)
            
        Returns:
            True if s can be a palindrome with at most one deletion
        """
        
        def is_palindrome_range(left: int, right: int) -> bool:
            """Check if s[left:right+1] is a palindrome."""
            while left < right:
                if s[left] != s[right]:
                    return False
                left += 1
                right -= 1
            return True
        
        left: int = 0
        right: int = len(s) - 1
        
        while left < right:
            if s[left] != s[right]:
                # MISMATCH FOUND: Try skipping either character
                # Option 1: Skip the left character → check s[left+1:right+1]
                # Option 2: Skip the right character → check s[left:right]
                return (is_palindrome_range(left + 1, right) or 
                        is_palindrome_range(left, right - 1))
            
            left += 1
            right -= 1
        
        # No mismatch found: already a palindrome
        return True


# ============================================================================
# Alternative: Generalized K-Skip Solution
# ============================================================================

class SolutionKSkips:
    """
    Generalized solution that can handle up to k character removals.
    
    For this problem k=1, but the structure supports arbitrary k.
    Note: For large k, this approach becomes exponential; DP would be needed.
    """
    
    def validPalindrome(self, s: str, k: int = 1) -> bool:
        """
        Check if s can become a palindrome by removing at most k characters.
        """
        
        def check(left: int, right: int, remaining_skips: int) -> bool:
            while left < right:
                if s[left] != s[right]:
                    if remaining_skips == 0:
                        return False
                    # Try both skip options
                    return (check(left + 1, right, remaining_skips - 1) or
                            check(left, right - 1, remaining_skips - 1))
                left += 1
                right -= 1
            return True
        
        return check(0, len(s) - 1, k)


# ============================================================================
# Alternative: Iterative with Explicit State
# ============================================================================

class SolutionIterative:
    """
    Fully iterative solution avoiding recursion.
    
    Uses explicit tracking of whether a skip has been used.
    """
    
    def validPalindrome(self, s: str) -> bool:
        left, right = 0, len(s) - 1
        
        while left < right:
            if s[left] != s[right]:
                # Check both skip options iteratively
                # Option 1: Skip left
                l1, r1 = left + 1, right
                valid1 = True
                while l1 < r1:
                    if s[l1] != s[r1]:
                        valid1 = False
                        break
                    l1 += 1
                    r1 -= 1
                
                if valid1:
                    return True
                
                # Option 2: Skip right
                l2, r2 = left, right - 1
                while l2 < r2:
                    if s[l2] != s[r2]:
                        return False
                    l2 += 1
                    r2 -= 1
                
                return True
            
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
        Input:  abca
        Output: true
    """
    import sys
    
    s = sys.stdin.read().strip()
    
    solution = Solution()
    result = solution.validPalindrome(s)
    
    print("true" if result else "false")


if __name__ == "__main__":
    solve()


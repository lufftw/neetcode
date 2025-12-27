# solutions/0340_longest_substring_with_at_most_k_distinct.py
"""
Problem: Longest Substring with At Most K Distinct Characters
Link: https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/

Given a string s and an integer k, return the length of the longest substring of s that contains at most k distinct characters.

Example 1:
    Input: s = "eceba", k = 2
    Output: 3
    Explanation: The substring is "ece" with length 3.

Example 2:
    Input: s = "aa", k = 1
    Output: 2
    Explanation: The substring is "aa" with length 2.

Constraints:
- 1 <= s.length <= 5 * 10^4
- 0 <= k <= 50

Topics: Hash Table, String, Sliding Window
"""
from typing import Dict
from _runner import get_solver


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# Polymorphic pattern: each entry specifies class + method
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "lengthOfLongestSubstringKDistinct",
        "complexity": "O(n) time, O(k) space",
        "description": "Sliding window with frequency tracking",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result using reference implementation.
    """
    lines = input_data.strip().split('\n')
    s = lines[0]
    k = int(lines[1]) if len(lines) > 1 else 0
    
    correct = _find_longest_k_distinct(s, k)
    
    try:
        actual_val = int(actual) if not isinstance(actual, int) else actual
        return actual_val == correct
    except (ValueError, TypeError):
        return False


def _find_longest_k_distinct(s: str, k: int) -> int:
    """Reference implementation for verification."""
    if k == 0:
        return 0
    
    char_freq: Dict[str, int] = {}
    left = 0
    max_length = 0
    
    for right, char in enumerate(s):
        char_freq[char] = char_freq.get(char, 0) + 1
        
        while len(char_freq) > k:
            left_char = s[left]
            char_freq[left_char] -= 1
            if char_freq[left_char] == 0:
                del char_freq[left_char]
            left += 1
        
        max_length = max(max_length, right - left + 1)
    
    return max_length


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Sliding Window
# Time: O(n), Space: O(k)
#   - Each character visited at most twice
#   - Frequency map bounded by k distinct characters
# ============================================================================

class Solution:
    def lengthOfLongestSubstringKDistinct(self, s: str, k: int) -> int:
        """
        Find the length of the longest substring with at most K distinct characters.
        
        Args:
            s: Input string
            k: Maximum number of distinct characters allowed
            
        Returns:
            Length of the longest valid substring
        """
        if k == 0:
            return 0
        
        # STATE: Frequency map tracking count of each character in window
        char_frequency: Dict[str, int] = {}
        
        # WINDOW boundaries
        left: int = 0
        max_length: int = 0
        
        for right, char in enumerate(s):
            # EXPAND: Add character to window
            char_frequency[char] = char_frequency.get(char, 0) + 1
            
            # CONTRACT: Shrink while we have more than K distinct characters
            while len(char_frequency) > k:
                left_char = s[left]
                char_frequency[left_char] -= 1
                
                # Remove from map when count reaches zero
                if char_frequency[left_char] == 0:
                    del char_frequency[left_char]
                
                left += 1
            
            # UPDATE ANSWER
            max_length = max(max_length, right - left + 1)
        
        return max_length


# ============================================================================
# Solution 2: LeetCode 159: At Most Two Distinct (K=2 specialization)
# Time: O(n), Space: O(1)
#   - Direct specialization of K-distinct pattern with K=2
#   - Same sliding window approach with fixed K=2
# ============================================================================

class SolutionTwoDistinct:
    """
    LeetCode 159: Longest Substring with At Most Two Distinct Characters.
    Direct specialization of K-distinct pattern with K=2.
    """
    
    def lengthOfLongestSubstringTwoDistinct(self, s: str) -> int:
        if not s:
            return 0
        
        char_frequency: Dict[str, int] = {}
        left: int = 0
        max_length: int = 0
        
        for right, char in enumerate(s):
            char_frequency[char] = char_frequency.get(char, 0) + 1
            
            while len(char_frequency) > 2:
                left_char = s[left]
                char_frequency[left_char] -= 1
                if char_frequency[left_char] == 0:
                    del char_frequency[left_char]
                left += 1
            
            max_length = max(max_length, right - left + 1)
        
        return max_length


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: s (the input string)
        Line 2: k (maximum distinct characters)
    
    Output format:
        Single integer: length of longest valid substring
    """
    import sys
    
    lines = sys.stdin.read().strip().split('\n')
    s = lines[0]
    k = int(lines[1]) if len(lines) > 1 else 0
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.lengthOfLongestSubstringKDistinct(s, k)
    
    print(result)


if __name__ == "__main__":
    solve()


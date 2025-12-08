# solutions/0003_longest_substring_without_repeating_characters.py
"""
Problem: Longest Substring Without Repeating Characters
Link: https://leetcode.com/problems/longest-substring-without-repeating-characters/

Given a string s, find the length of the longest substring without repeating characters.

Time Complexity: O(n) - sliding window with hash table
Space Complexity: O(min(m, n)) - where m is the charset size
"""


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result using brute force verification.
    
    Args:
        actual: Program output (may be int or string)
        expected: Expected output (None if from generator)
        input_data: Raw input string
    
    Returns:
        bool: True if correct
    """
    s = input_data.strip()
    correct = _brute_force(s)
    
    try:
        # Handle both int and string input
        actual_val = int(actual) if not isinstance(actual, int) else actual
        return actual_val == correct
    except (ValueError, TypeError):
        return False


def _brute_force(s: str) -> int:
    """O(n²) brute force solution for verification."""
    n = len(s)
    if n == 0:
        return 0
    
    max_len = 0
    for i in range(n):
        seen = set()
        for j in range(i, n):
            if s[j] in seen:
                break
            seen.add(s[j])
            max_len = max(max_len, j - i + 1)
    
    return max_len


JUDGE_FUNC = judge


# ============================================
# Solution - O(n) Sliding Window
# ============================================
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # Track last seen position of each character (ASCII)
        last = [-1] * 128
        ans = 0
        start = 0
        
        for i, ch in enumerate(s):
            # If character was seen within current window, move start
            if last[ord(ch)] != -1:
                start = max(start, last[ord(ch)] + 1)
            # Update answer
            ans = max(ans, i - start + 1)
            # Record position
            last[ord(ch)] = i

        return ans


def solve():
    """
    Input format:
    Line 1: s (string)
    
    Example:
    abcabcbb
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')
    
    # Parse s
    s = lines[0] if lines else ""
    
    sol = Solution()
    result = sol.lengthOfLongestSubstring(s)
    
    # Output format: integer
    print(result)


if __name__ == "__main__":
    solve()

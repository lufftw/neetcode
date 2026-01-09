# solutions/0076_minimum_window_substring.py
"""
Problem: Minimum Window Substring
Link: https://leetcode.com/problems/minimum-window-substring/

Given two strings s and t of lengths m and n respectively, return the minimum window substring of s such that every character in t (including duplicates) is included in the window. If there is no such substring, return the empty string "".
The testcases will be generated such that the answer is unique.

Example 1:
    Input: s = "ADOBECODEBANC", t = "ABC"
    Output: "BANC"
    Explanation: The minimum window substring "BANC" includes 'A', 'B', and 'C' from string t.

Example 2:
    Input: s = "a", t = "a"
    Output: "a"
    Explanation: The entire string s is the minimum window.

Example 3:
    Input: s = "a", t = "aa"
    Output: ""
    Explanation: Both 'a's from t must be included in the window.
                 Since the largest window of s only has one 'a', return empty string.

Constraints:
- m == s.length
- n == t.length
- 1 <= m, n <= 10^5
- s and t consist of uppercase and lowercase English letters.

Topics: Hash Table, String, Sliding Window

Hint 1: Use two pointers to create a window of letters in s, which would have all the characters from t.

Hint 2: Expand the right pointer until all the characters of t are covered.

Hint 3: Once all the characters are covered, move the left pointer and ensure that all the characters are still covered to minimize the subarray size.

Hint 4: Continue expanding the right and left pointers until you reach the end of s.

Follow-up: Could you find an algorithm that runs in O(m + n) time?
"""
from typing import Dict
from collections import Counter
from _runner import get_solver


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# Polymorphic pattern: each entry specifies class + method
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "minWindow",
        "complexity": "O(|s| + |t|) time, O(|t|) space",
        "description": "Sliding window with frequency tracking",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output is a valid minimum window.
    
    A valid answer must:
    1. Be a substring of s
    2. Contain all characters of t with required frequencies
    3. Have minimal length among all valid windows
    """
    import json
    lines = input_data.strip().split('\n')
    s = json.loads(lines[0])
    t = json.loads(lines[1]) if len(lines) > 1 else ""
    
    actual_str = str(actual).strip()
    
    # Compute correct answer
    correct = _find_min_window(s, t)
    
    # Both empty means no valid window
    if correct == "" and actual_str == "":
        return True
    
    # Check length match (minimum window property)
    if len(actual_str) != len(correct):
        return False
    
    # Verify actual is a valid window (contains all chars of t)
    if not _is_valid_window(actual_str, t):
        return False
    
    # Verify actual is a substring of s
    if actual_str not in s:
        return False
    
    return True


def _find_min_window(s: str, t: str) -> str:
    """Reference implementation for verification."""
    if not t or not s or len(t) > len(s):
        return ""
    
    need = Counter(t)
    have: Dict[str, int] = {}
    satisfied = 0
    required = len(need)
    
    min_len = float('inf')
    min_start = 0
    left = 0
    
    for right, char in enumerate(s):
        have[char] = have.get(char, 0) + 1
        if char in need and have[char] == need[char]:
            satisfied += 1
        
        while satisfied == required:
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_start = left
            
            left_char = s[left]
            have[left_char] -= 1
            if left_char in need and have[left_char] < need[left_char]:
                satisfied -= 1
            left += 1
    
    return "" if min_len == float('inf') else s[min_start:min_start + min_len]


def _is_valid_window(window: str, t: str) -> bool:
    """Check if window contains all characters of t."""
    need = Counter(t)
    have = Counter(window)
    for char, count in need.items():
        if have.get(char, 0) < count:
            return False
    return True


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Sliding Window
# Time: O(|s| + |t|), Space: O(|t|)
#   - Linear scan through s with sliding window
#   - Frequency maps bounded by t's unique characters
#   - Uses satisfied counter for efficient validity check
# ============================================================================

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        """
        Find the minimum window substring of s that contains all characters of t.

        Core insight: Expand until all requirements satisfied, then contract
        aggressively while still valid. The "satisfied counter" optimization
        reduces validity check from O(|t|) to O(1).

        Invariant: When chars_satisfied == chars_required, window contains all of t.

        Args:
            s: Source string to search in
            t: Target string containing required characters

        Returns:
            Minimum window substring, or "" if no valid window exists
        """
        if not t or not s or len(t) > len(s):
            return ""
        
        # STATE: Required character frequencies (what we NEED)
        need_frequency: Dict[str, int] = Counter(t)
        
        # STATE: Current window character frequencies (what we HAVE)
        have_frequency: Dict[str, int] = {}
        
        # OPTIMIZATION: Track how many unique characters have met their requirement
        chars_satisfied: int = 0
        chars_required: int = len(need_frequency)
        
        # ANSWER tracking
        min_length: float = float('inf')
        min_window_start: int = 0
        
        # WINDOW boundaries
        left: int = 0
        
        for right, char in enumerate(s):
            # EXPAND: Add character to window
            have_frequency[char] = have_frequency.get(char, 0) + 1
            
            # Check if this character just satisfied its requirement
            if char in need_frequency and have_frequency[char] == need_frequency[char]:
                chars_satisfied += 1
            
            # CONTRACT: Once all requirements satisfied, try to MINIMIZE window
            while chars_satisfied == chars_required:
                window_length = right - left + 1
                if window_length < min_length:
                    min_length = window_length
                    min_window_start = left
                
                # Remove leftmost character
                left_char = s[left]
                have_frequency[left_char] -= 1
                
                if left_char in need_frequency and have_frequency[left_char] < need_frequency[left_char]:
                    chars_satisfied -= 1
                
                left += 1
        
        if min_length == float('inf'):
            return ""
        
        return s[min_window_start : min_window_start + min_length]


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format (canonical JSON):
        Line 1: s (JSON string, e.g. "ADOBECODEBANC")
        Line 2: t (JSON string, e.g. "ABC")
    
    Output format:
        JSON string: minimum window substring, or "" if none exists
    """
    import sys
    import json
    
    lines = sys.stdin.read().strip().split('\n')
    s = json.loads(lines[0])
    t = json.loads(lines[1]) if len(lines) > 1 else ""
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.minWindow(s, t)
    
    print(json.dumps(result))


if __name__ == "__main__":
    solve()


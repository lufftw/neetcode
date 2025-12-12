# solutions/0076_minimum_window_substring.py
"""
================================================================================
LeetCode 76: Minimum Window Substring
================================================================================

Problem: Given two strings s and t, find the minimum window in s which contains
         all characters of t (including duplicates).

API Kernel: SubstringSlidingWindow
Pattern: sliding_window_freq_cover
Family: substring_window

--------------------------------------------------------------------------------
RELATIONSHIP TO BASE KERNEL (LeetCode 3)
--------------------------------------------------------------------------------

Base (LeetCode 3):
    INVARIANT: All characters in window are unique
    GOAL: Maximize window size

This Variant (LeetCode 76):
    INVARIANT: Window contains all required characters with sufficient frequency
    GOAL: Minimize window size (reverse optimization direction!)

Delta from Base:
    - Track "need" (required) and "have" (current) frequencies separately
    - Use a "satisfied counter" to efficiently check if all requirements are met
    - Contract WHILE valid (to minimize), not UNTIL valid (to maximize)

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(|s| + |t|) - Linear in both string lengths
Space: O(|t|) - Frequency maps bounded by t's unique characters

================================================================================
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
    lines = input_data.strip().split('\n')
    s = lines[0]
    t = lines[1] if len(lines) > 1 else ""
    
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
    Input format:
        Line 1: s (source string)
        Line 2: t (target string)
    
    Output format:
        The minimum window substring, or empty string if none exists
    """
    import sys
    
    lines = sys.stdin.read().strip().split('\n')
    s = lines[0]
    t = lines[1] if len(lines) > 1 else ""
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.minWindow(s, t)
    
    print(result)


if __name__ == "__main__":
    solve()


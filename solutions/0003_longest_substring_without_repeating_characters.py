# solutions/0003_longest_substring_without_repeating_characters.py
"""
================================================================================
LeetCode 3: Longest Substring Without Repeating Characters
================================================================================

Problem: Given a string s, find the length of the longest substring without
         repeating characters.

API Kernel: SubstringSlidingWindow (BASE TEMPLATE)
Pattern: sliding_window_unique
Family: substring_window

This is the canonical sliding window kernel. All other sliding window variations
build upon the principles established here.

--------------------------------------------------------------------------------
SLIDING WINDOW CORE CONCEPT
--------------------------------------------------------------------------------

The sliding window technique maintains a dynamic window [left, right] over a
sequence while preserving an INVARIANT - a condition that must always hold.

For this problem:
    INVARIANT: All characters in window [left, right] are unique.

Window Operations:
    1. EXPAND: Always move right pointer forward, adding elements
    2. CONTRACT: Move left pointer to restore invariant when violated
    3. UPDATE: Record answer when window is valid

Key Insight (Jump Optimization):
    Instead of incrementally shrinking with a while-loop, we directly jump
    `left` to `last_seen[char] + 1`. This works because:
    - Any position before last_seen[char] would still include the duplicate
    - Position last_seen[char] + 1 is the first that excludes the duplicate

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(n) - Each character is visited at most twice
Space: O(min(n, σ)) - Where σ is the alphabet size (128 for ASCII)

================================================================================
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
        "method": "lengthOfLongestSubstring",
        "complexity": "O(n) time, O(min(n,σ)) space",
        "description": "Sliding window with jump optimization",
    },
    "dict": {
        "class": "SolutionDict",
        "method": "lengthOfLongestSubstring",
        "complexity": "O(n) time, O(min(n,σ)) space",
        "description": "Sliding window using dictionary for Unicode support",
    },
    "set": {
        "class": "SolutionWithSet",
        "method": "lengthOfLongestSubstring",
        "complexity": "O(n) time, O(min(n,σ)) space",
        "description": "Sliding window using set with while-loop contraction",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

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


# ============================================================================
# Solution 1: Sliding Window (Optimized with Jump)
# Time: O(n), Space: O(min(n, σ))
#   - Each character visited at most twice
#   - Uses last-seen-index array for O(1) duplicate detection
#   - Direct position jumping instead of incremental contraction
# ============================================================================

class Solution:
    """
    Optimal solution using sliding window with jump optimization.
    
    Uses a last-seen-index array for O(1) duplicate detection and
    direct position jumping instead of incremental contraction.
    """
    
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        Find the length of the longest substring without repeating characters.
        
        Args:
            s: Input string
            
        Returns:
            Length of the longest substring with all unique characters
        """
        # STATE: Track last seen position of each character (ASCII)
        # Using array for O(1) access, -1 means not seen
        last_seen: list = [-1] * 128
        
        # WINDOW: left boundary (right boundary is the loop variable)
        left: int = 0
        
        # ANSWER: Track the maximum window size seen
        max_length: int = 0
        
        for right, char in enumerate(s):
            char_code = ord(char)
            
            # CHECK INVARIANT: Is this character already in our window?
            if last_seen[char_code] >= left:
                # CONTRACT (Jump): Move left pointer past the previous occurrence
                left = last_seen[char_code] + 1
            
            # UPDATE STATE: Record character's position
            last_seen[char_code] = right
            
            # UPDATE ANSWER: Current window [left, right] is valid
            max_length = max(max_length, right - left + 1)
        
        return max_length


# ============================================================================
# Alternative: Using Dictionary (More Flexible for Unicode)
# ============================================================================

class SolutionDict:
    """
    Alternative implementation using dictionary for last-seen index.
    
    More flexible for Unicode strings but slightly slower due to
    hash table overhead.
    """
    
    def lengthOfLongestSubstring(self, s: str) -> int:
        last_seen_index: Dict[str, int] = {}
        left: int = 0
        max_length: int = 0
        
        for right, char in enumerate(s):
            if char in last_seen_index and last_seen_index[char] >= left:
                left = last_seen_index[char] + 1
            
            last_seen_index[char] = right
            max_length = max(max_length, right - left + 1)
        
        return max_length


# ============================================================================
# Alternative: Using Set (Standard While-Loop Pattern)
# ============================================================================

class SolutionWithSet:
    """
    Alternative implementation using a set for the current window.
    
    This version demonstrates the standard while-loop contraction pattern,
    which is more intuitive but slightly less efficient than the jump
    optimization used in the main Solution class.
    """
    
    def lengthOfLongestSubstring(self, s: str) -> int:
        window_chars: set = set()
        left: int = 0
        max_length: int = 0
        
        for right, char in enumerate(s):
            # CONTRACT: Shrink window until we can add the new character
            while char in window_chars:
                window_chars.remove(s[left])
                left += 1
            
            # EXPAND: Add the new character
            window_chars.add(char)
            
            # UPDATE ANSWER
            max_length = max(max_length, right - left + 1)
        
        return max_length


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: s (the input string)
    
    Output format:
        Single integer: length of longest substring without repeating characters
    
    Example:
        Input:  abcabcbb
        Output: 3
    """
    import sys
    
    lines = sys.stdin.read().strip().split('\n')
    s = lines[0] if lines else ""
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.lengthOfLongestSubstring(s)
    
    print(result)


if __name__ == "__main__":
    solve()

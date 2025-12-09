# solutions/0567_permutation_in_string.py
"""
================================================================================
LeetCode 567: Permutation in String
================================================================================

Problem: Given two strings s1 and s2, return true if s2 contains a permutation
         of s1. In other words, return true if one of s1's permutations is a
         substring of s2.

API Kernel: SubstringSlidingWindow
Pattern: sliding_window_freq_cover (fixed-size variant)
Family: substring_window

--------------------------------------------------------------------------------
RELATIONSHIP TO BASE KERNEL AND OTHER VARIANTS
--------------------------------------------------------------------------------

Base (LeetCode 3):
    - Variable window size
    - Maximize window

LeetCode 76 (Minimum Window):
    - Variable window size
    - Minimize window that covers requirements

This Variant (LeetCode 567):
    - FIXED window size = len(s1)
    - Check for EXACT frequency match (permutation = same chars, same counts)
    - Return boolean (existence check)

Key Insight:
    A permutation of s1 has:
    1. Exactly the same length as s1
    2. Exactly the same character frequencies as s1

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(|s1| + |s2|) - Build pattern frequency + single pass over s2
Space: O(1) - At most 26 lowercase letters in frequency maps

================================================================================
"""
from typing import Dict
from collections import Counter


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result using reference implementation.
    """
    lines = input_data.strip().split('\n')
    s1 = lines[0]
    s2 = lines[1] if len(lines) > 1 else ""
    
    correct = _check_inclusion(s1, s2)
    
    # Parse actual result
    actual_str = str(actual).strip().lower()
    actual_bool = actual_str in ("true", "1", "yes")
    
    return actual_bool == correct


def _check_inclusion(s1: str, s2: str) -> bool:
    """Reference implementation for verification."""
    if len(s1) > len(s2):
        return False
    
    pattern_freq = Counter(s1)
    window_freq: Dict[str, int] = {}
    matched = 0
    required = len(pattern_freq)
    pattern_len = len(s1)
    
    for i, char in enumerate(s2):
        window_freq[char] = window_freq.get(char, 0) + 1
        if char in pattern_freq:
            if window_freq[char] == pattern_freq[char]:
                matched += 1
            elif window_freq[char] == pattern_freq[char] + 1:
                matched -= 1
        
        if i >= pattern_len:
            old_char = s2[i - pattern_len]
            if old_char in pattern_freq:
                if window_freq[old_char] == pattern_freq[old_char]:
                    matched -= 1
                elif window_freq[old_char] == pattern_freq[old_char] + 1:
                    matched += 1
            window_freq[old_char] -= 1
            if window_freq[old_char] == 0:
                del window_freq[old_char]
        
        if matched == required:
            return True
    
    return False


JUDGE_FUNC = judge


# ============================================================================
# Solution - O(|s1| + |s2|) Sliding Window
# ============================================================================

class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        """
        Check if s2 contains any permutation of s1.
        
        Args:
            s1: Pattern string (looking for its permutation)
            s2: Source string to search in
            
        Returns:
            True if s2 contains a permutation of s1
        """
        pattern_length = len(s1)
        source_length = len(s2)
        
        if pattern_length > source_length:
            return False
        
        # STATE: Build pattern frequency map
        pattern_frequency: Dict[str, int] = Counter(s1)
        
        # STATE: Window frequency map
        window_frequency: Dict[str, int] = {}
        
        # OPTIMIZATION: Track matching character counts
        chars_matched: int = 0
        chars_to_match: int = len(pattern_frequency)
        
        for i, char in enumerate(s2):
            # EXPAND: Add character to window
            window_frequency[char] = window_frequency.get(char, 0) + 1
            
            if char in pattern_frequency:
                if window_frequency[char] == pattern_frequency[char]:
                    chars_matched += 1
                elif window_frequency[char] == pattern_frequency[char] + 1:
                    chars_matched -= 1
            
            # CONTRACT: Remove character that falls out of window
            if i >= pattern_length:
                old_char = s2[i - pattern_length]
                if old_char in pattern_frequency:
                    if window_frequency[old_char] == pattern_frequency[old_char]:
                        chars_matched -= 1
                    elif window_frequency[old_char] == pattern_frequency[old_char] + 1:
                        chars_matched += 1
                window_frequency[old_char] -= 1
                if window_frequency[old_char] == 0:
                    del window_frequency[old_char]
            
            # CHECK: Did we find a permutation?
            if chars_matched == chars_to_match:
                return True
        
        return False


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: s1 (pattern string)
        Line 2: s2 (source string)
    
    Output format:
        "true" or "false"
    """
    import sys
    
    lines = sys.stdin.read().strip().split('\n')
    s1 = lines[0]
    s2 = lines[1] if len(lines) > 1 else ""
    
    solution = Solution()
    result = solution.checkInclusion(s1, s2)
    
    print("true" if result else "false")


if __name__ == "__main__":
    solve()


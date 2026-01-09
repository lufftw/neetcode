# solutions/0567_permutation_in_string.py
"""
Problem: Permutation in String
Link: https://leetcode.com/problems/permutation-in-string/

Given two strings s1 and s2, return true if s2 contains a permutation of s1, or false otherwise.
In other words, return true if one of s1's permutations is the substring of s2.

Example 1:
    Input: s1 = "ab", s2 = "eidbaooo"
    Output: true
    Explanation: s2 contains one permutation of s1 ("ba").

Example 2:
    Input: s1 = "ab", s2 = "eidboaoo"
    Output: false

Constraints:
- 1 <= s1.length, s2.length <= 10^4
- s1 and s2 consist of lowercase English letters.

Topics: Hash Table, Two Pointers, String, Sliding Window

Hint 1: Obviously, brute force will result in TLE. Think of something else.

Hint 2: How will you check whether one string is a permutation of another string?

Hint 3: One way is to sort the string and then compare. But, Is there a better way?

Hint 4: If one string is a permutation of another string then they must one common metric. What is that?

Hint 5: Both strings must have same character frequencies, if  one is permutation of another. Which data structure should be used to store frequencies?

Hint 6: What about hash table?  An array of size 26?
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
        "method": "checkInclusion",
        "complexity": "O(|s1| + |s2|) time, O(|s1|) space",
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
    import json
    lines = input_data.strip().split('\n')
    s1 = json.loads(lines[0])
    s2 = json.loads(lines[1]) if len(lines) > 1 else ""
    
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
# Solution 1: Sliding Window
# Time: O(|s1| + |s2|), Space: O(|s1|)
#   - Build pattern frequency + single pass over s2
#   - Fixed window size = len(s1)
#   - Frequency maps bounded by s1's unique characters
# ============================================================================

class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        """
        Check if s2 contains any permutation of s1.

        Core insight: Permutation = same character frequencies. Use fixed window
        of size len(s1) and track how many characters have matching frequencies.

        Invariant: Window size is always exactly len(s1) after initial fill.

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
    Input format (canonical JSON):
        Line 1: s1 (JSON string, e.g. "ab")
        Line 2: s2 (JSON string, e.g. "eidbaooo")
    
    Output format:
        JSON boolean: true or false
    """
    import sys
    import json
    
    lines = sys.stdin.read().strip().split('\n')
    s1 = json.loads(lines[0])
    s2 = json.loads(lines[1]) if len(lines) > 1 else ""
    
    # Get solver and call method naturally (like LeetCode)
    solver = get_solver(SOLUTIONS)
    result = solver.checkInclusion(s1, s2)
    
    print("true" if result else "false")


if __name__ == "__main__":
    solve()


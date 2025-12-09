# solutions/0438_find_all_anagrams_in_a_string.py
"""
================================================================================
LeetCode 438: Find All Anagrams in a String
================================================================================

Problem: Given two strings s and p, return an array of all the start indices
         of p's anagrams in s. An anagram is a permutation of a string.

API Kernel: SubstringSlidingWindow
Pattern: sliding_window_freq_cover (fixed-size, collect all)
Family: substring_window

--------------------------------------------------------------------------------
RELATIONSHIP TO BASE KERNEL AND OTHER VARIANTS
--------------------------------------------------------------------------------

LeetCode 567 (Permutation in String):
    - Return boolean (exists or not)
    - Stop on first match

This Variant (LeetCode 438):
    - Return list of ALL starting indices
    - Continue searching after each match

Delta from LeetCode 567:
    - Instead of `return True` on match, append index to result list
    - Continue processing after finding a match

--------------------------------------------------------------------------------
COMPLEXITY ANALYSIS
--------------------------------------------------------------------------------

Time:  O(|s| + |p|) - Build pattern frequency + single pass over s
Space: O(1) for frequency maps (bounded by alphabet size)
       O(k) for output where k = number of anagrams found

================================================================================
"""
from typing import List, Dict
from collections import Counter


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================

def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result using reference implementation.
    """
    lines = input_data.strip().split('\n')
    s = lines[0]
    p = lines[1] if len(lines) > 1 else ""
    
    correct = _find_anagrams(s, p)
    
    # Parse actual result
    try:
        if isinstance(actual, list):
            actual_list = actual
        else:
            actual_str = str(actual).strip()
            if actual_str == "[]":
                actual_list = []
            else:
                # Handle "[0, 6]" format
                actual_str = actual_str.strip("[]")
                if not actual_str:
                    actual_list = []
                else:
                    actual_list = [int(x.strip()) for x in actual_str.split(",")]
        
        return sorted(actual_list) == sorted(correct)
    except (ValueError, TypeError):
        return False


def _find_anagrams(s: str, p: str) -> List[int]:
    """Reference implementation for verification."""
    result: List[int] = []
    
    if len(p) > len(s):
        return result
    
    pattern_freq = Counter(p)
    window_freq: Dict[str, int] = {}
    matched = 0
    required = len(pattern_freq)
    pattern_len = len(p)
    
    for i, char in enumerate(s):
        window_freq[char] = window_freq.get(char, 0) + 1
        if char in pattern_freq and window_freq[char] == pattern_freq[char]:
            matched += 1
        elif char in pattern_freq and window_freq[char] == pattern_freq[char] + 1:
            matched -= 1
        
        if i >= pattern_len:
            old_char = s[i - pattern_len]
            if old_char in pattern_freq and window_freq[old_char] == pattern_freq[old_char]:
                matched -= 1
            elif old_char in pattern_freq and window_freq[old_char] == pattern_freq[old_char] + 1:
                matched += 1
            window_freq[old_char] -= 1
            if window_freq[old_char] == 0:
                del window_freq[old_char]
        
        if matched == required:
            result.append(i - pattern_len + 1)
    
    return result


JUDGE_FUNC = judge


# ============================================================================
# Solution - O(|s| + |p|) Sliding Window
# ============================================================================

class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        """
        Find all start indices of p's anagrams in s.
        
        Args:
            s: Source string to search in
            p: Pattern string (looking for its anagrams)
            
        Returns:
            List of starting indices where anagrams of p begin in s
        """
        result: List[int] = []
        
        pattern_length = len(p)
        source_length = len(s)
        
        if pattern_length > source_length:
            return result
        
        # STATE: Build pattern frequency map
        pattern_frequency: Dict[str, int] = Counter(p)
        
        # STATE: Window frequency map
        window_frequency: Dict[str, int] = {}
        
        # OPTIMIZATION: Track matching character counts
        chars_matched: int = 0
        chars_to_match: int = len(pattern_frequency)
        
        for i, char in enumerate(s):
            # EXPAND: Add character to window
            window_frequency[char] = window_frequency.get(char, 0) + 1
            
            if char in pattern_frequency:
                if window_frequency[char] == pattern_frequency[char]:
                    chars_matched += 1
                elif window_frequency[char] == pattern_frequency[char] + 1:
                    chars_matched -= 1
            
            # CONTRACT: Remove character that falls out of window
            if i >= pattern_length:
                old_char = s[i - pattern_length]
                if old_char in pattern_frequency:
                    if window_frequency[old_char] == pattern_frequency[old_char]:
                        chars_matched -= 1
                    elif window_frequency[old_char] == pattern_frequency[old_char] + 1:
                        chars_matched += 1
                window_frequency[old_char] -= 1
                if window_frequency[old_char] == 0:
                    del window_frequency[old_char]
            
            # COLLECT: Record if anagram found
            if chars_matched == chars_to_match:
                result.append(i - pattern_length + 1)
        
        return result


# ============================================================================
# STDIN/STDOUT Interface for Testing Framework
# ============================================================================

def solve():
    """
    Input format:
        Line 1: s (source string)
        Line 2: p (pattern string)
    
    Output format:
        List of starting indices
    """
    import sys
    
    lines = sys.stdin.read().strip().split('\n')
    s = lines[0]
    p = lines[1] if len(lines) > 1 else ""
    
    solution = Solution()
    result = solution.findAnagrams(s, p)
    
    print(result)


if __name__ == "__main__":
    solve()


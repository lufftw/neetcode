# solutions/0003_longest_substring_without_repeating_characters.py
"""
題目: Longest Substring Without Repeating Characters
連結: https://leetcode.com/problems/longest-substring-without-repeating-characters/

Given a string s, find the length of the longest substring without repeating characters.
"""


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last = [-1] * 128
        ans = 0
        start = 0
        for i, ch in enumerate(s):
            if last[ord(ch)] != -1:
                start = max(start, last[ord(ch)] + 1)
            ans = max(ans, i - start + 1)
            last[ord(ch)] = i

        return ans


def solve():
    """
    輸入格式:
    第一行: s (字串)
    
    Example:
    abcabcbb
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')
    
    # 解析 s
    s = lines[0] if lines[0] else ""
    
    sol = Solution()
    result = sol.lengthOfLongestSubstring(s)
    
    # 輸出格式: 整數
    print(result)


if __name__ == "__main__":
    solve()


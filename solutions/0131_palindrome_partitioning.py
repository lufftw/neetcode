# solutions/0131_palindrome_partitioning.py
"""
Problem: Palindrome Partitioning
Link: https://leetcode.com/problems/palindrome-partitioning/

Given a string s, partition s such that every substring of the partition
is a palindrome. Return all possible palindrome partitioning of s.
The decision tree is: at each position, where do we make the next cut?
Only valid (palindrome) prefixes lead to recursive calls.

Constraints:
- 1 <= s.length <= 16
- s contains only lowercase English letters
"""
from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionDP",
        "method": "partition",
        "complexity": "O(n × 2^n) time, O(n^2) space",
        "description": "Backtracking with DP-precomputed palindrome table",
    },
    "naive": {
        "class": "SolutionNaive",
        "method": "partition",
        "complexity": "O(n × 2^n × n) time, O(n) space",
        "description": "Backtracking with on-the-fly palindrome checking",
    },
}


# ============================================================================
# JUDGE_FUNC - Validate palindrome partitions
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Palindrome Partitioning results."""
    s = input_data.strip()
    
    def is_palindrome(t: str) -> bool:
        return t == t[::-1]
    
    for partition in actual:
        # Check partition reconstructs original string
        if ''.join(partition) != s:
            return False
        # Check each part is a palindrome
        for part in partition:
            if not is_palindrome(part):
                return False
    
    # Check no duplicate partitions
    partition_tuples = [tuple(p) for p in actual]
    if len(set(partition_tuples)) != len(actual):
        return False
    
    if expected is not None:
        return len(actual) == len(expected)
    
    return True


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Backtracking with DP-Precomputed Palindrome Table
# Time: O(n × 2^n), Space: O(n^2)
#   - Precompute is_palindrome[i][j] for O(1) checks
#   - At each position, try all valid (palindrome) prefixes
#   - O(n^2) preprocessing dominated by O(n × 2^n) backtracking
# ============================================================================
class SolutionDP:
    def partition(self, s: str) -> List[List[str]]:
        """
        Find all palindrome partitionings with DP-precomputed palindrome table.
        
        Algorithm:
        - Precompute is_palindrome[i][j] for all substrings
        - Backtrack: at each position, try all valid (palindrome) prefixes
        - When start reaches end of string, we have a valid partition
        
        DP Table Construction:
        - is_palindrome[i][j] = True if s[i:j+1] is a palindrome
        - Base: single chars and pairs
        - Transition: s[i]==s[j] and is_palindrome[i+1][j-1]
        
        Why Precompute?
        - Without precompute: O(n) per palindrome check → O(n^3) total checks
        - With precompute: O(n^2) preprocessing, O(1) per check
        
        Time Complexity: O(n × 2^n)
            - 2^(n-1) possible partitions (n-1 cut positions, each on/off)
            - O(n) to copy each partition
            - Preprocessing is O(n^2), dominated by above
        
        Space Complexity: O(n^2) for DP table
        """
        results: List[List[str]] = []
        path: List[str] = []
        n = len(s)
        
        # === PRECOMPUTE: Build palindrome lookup table ===
        # is_palindrome[i][j] = True if s[i:j+1] is a palindrome
        is_palindrome = [[False] * n for _ in range(n)]
        
        # Fill table in reverse order (bottom-up)
        # We need is_palindrome[i+1][j-1] before is_palindrome[i][j]
        for i in range(n - 1, -1, -1):
            for j in range(i, n):
                if s[i] == s[j]:
                    # Length 1 or 2, or inner substring is palindrome
                    if j - i <= 2:
                        is_palindrome[i][j] = True
                    else:
                        is_palindrome[i][j] = is_palindrome[i + 1][j - 1]
        
        def backtrack(start: int) -> None:
            # BASE CASE: Reached end of string, partition complete
            if start == n:
                results.append(path[:])
                return
            
            # Try each possible end position for the current segment
            for end in range(start, n):
                # === VALIDITY CHECK ===
                # Only proceed if prefix s[start:end+1] is a palindrome
                if not is_palindrome[start][end]:
                    continue
                
                # === CHOOSE: Add this palindrome segment ===
                path.append(s[start:end + 1])
                
                # === EXPLORE: Recurse on remainder ===
                backtrack(end + 1)
                
                # === UNCHOOSE ===
                path.pop()
        
        backtrack(0)
        return results


# ============================================================================
# Solution 2: Backtracking with On-the-Fly Checking
# Time: O(n × 2^n × n), Space: O(n)
#   - Check palindrome during backtracking (no preprocessing)
#   - Simpler code but slower for repeated checks
# ============================================================================
class SolutionNaive:
    def partition(self, s: str) -> List[List[str]]:
        """
        Find all palindrome partitionings with on-the-fly checking.
        
        Same algorithm but checks palindrome status during backtracking.
        Simpler code but slightly slower for repeated checks.
        """
        results: List[List[str]] = []
        path: List[str] = []
        n = len(s)
        
        def is_palindrome(start: int, end: int) -> bool:
            """Check if s[start:end+1] is a palindrome."""
            while start < end:
                if s[start] != s[end]:
                    return False
                start += 1
                end -= 1
            return True
        
        def backtrack(start: int) -> None:
            if start == n:
                results.append(path[:])
                return
            
            for end in range(start, n):
                if is_palindrome(start, end):
                    path.append(s[start:end + 1])
                    backtrack(end + 1)
                    path.pop()
        
        backtrack(0)
        return results


def solve():
    """
    Input format:
    Line 1: s (string to partition)
    
    Example:
    aab
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')
    
    s = lines[0]
    
    solver = get_solver(SOLUTIONS)
    result = solver.partition(s)
    
    print(result)


if __name__ == "__main__":
    solve()


# solutions/0093_restore_ip_addresses.py
"""
Problem: Restore IP Addresses
Link: https://leetcode.com/problems/restore-ip-addresses/

Given a string s containing only digits, return all possible valid IP addresses
that can be formed by inserting dots into s.

Sub-Pattern: String segmentation with multi-constraint validity
Key Insight: IP address has exactly 4 segments (octets), each with constraints:
- Length: 1-3 characters
- Value: 0-255
- No leading zeros (except "0" itself)

Prune aggressively based on remaining length bounds.
"""
from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "restoreIpAddresses",
        "complexity": "O(3^4 × n) = O(n) time, O(1) space",
        "description": "Backtracking with segment validation and length pruning",
    },
}


# ============================================================================
# JUDGE_FUNC - Validate IP addresses
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Restore IP Addresses results."""
    s = input_data.strip()
    
    def is_valid_ip(ip: str) -> bool:
        """Check if ip is valid and uses all characters from s."""
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        reconstructed = ''.join(parts)
        if reconstructed != s:
            return False
        for part in parts:
            if not part:
                return False
            if len(part) > 1 and part[0] == '0':
                return False
            if int(part) > 255:
                return False
        return True
    
    for ip in actual:
        if not is_valid_ip(ip):
            return False
    
    # Check no duplicates
    if len(set(actual)) != len(actual):
        return False
    
    if expected is not None:
        return len(actual) == len(expected)
    
    return True


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Backtracking with Segment Validation
# Time: O(3^4 × n) = O(n), Space: O(1)
#   - Exactly 4 segments; try 1, 2, or 3 chars per segment
#   - Validate: no leading zeros, value 0-255
#   - Prune based on remaining length bounds
# ============================================================================
class Solution:
    def restoreIpAddresses(self, s: str) -> List[str]:
        """
        Generate all valid IP addresses from a digit string.
        
        IP Address Constraints:
        - Exactly 4 segments (octets)
        - Each segment: 1-3 digits
        - Each segment value: 0-255
        - No leading zeros (except "0" itself)
        
        Algorithm:
        - Exactly 4 segments required, track segment count
        - For each segment, try 1, 2, or 3 characters
        - Validate each segment before proceeding
        - Prune based on remaining length bounds
        
        Length Bounds Pruning:
        - Minimum remaining = remaining_segments × 1
        - Maximum remaining = remaining_segments × 3
        - If remaining chars outside [min, max], prune
        
        Time Complexity: O(3^4 × n) = O(81 × n) = O(n)
            - At most 3 choices per segment, 4 segments
            - O(n) to validate and build result
        
        Space Complexity: O(4) = O(1) for segment storage
            - Not counting output
        """
        results: List[str] = []
        segments: List[str] = []
        n = len(s)
        
        def is_valid_segment(segment: str) -> bool:
            """
            Check if segment is a valid IP octet.
            
            Valid if:
            - Not empty
            - No leading zeros (unless segment is "0")
            - Numeric value between 0 and 255
            """
            if not segment:
                return False
            # Leading zero check: invalid if length > 1 and starts with '0'
            if len(segment) > 1 and segment[0] == '0':
                return False
            # Value range check
            value = int(segment)
            if value > 255:
                return False
            return True
        
        def backtrack(start: int, segment_count: int) -> None:
            # === LENGTH BOUNDS PRUNING ===
            remaining_chars = n - start
            remaining_segments = 4 - segment_count
            
            # Too few characters to fill remaining segments
            if remaining_chars < remaining_segments:
                return
            # Too many characters for remaining segments
            if remaining_chars > remaining_segments * 3:
                return
            
            # BASE CASE: 4 segments formed
            if segment_count == 4:
                # All characters must be used
                if start == n:
                    results.append('.'.join(segments))
                return
            
            # Try segment lengths 1, 2, 3
            for length in range(1, 4):
                # Don't exceed string bounds
                if start + length > n:
                    break
                
                segment = s[start:start + length]
                
                # === VALIDITY CHECK ===
                if not is_valid_segment(segment):
                    # For length 2 or 3 with leading zero, longer won't help
                    # But value > 255 only happens at length 3, so continue
                    continue
                
                # === CHOOSE ===
                segments.append(segment)
                
                # === EXPLORE ===
                backtrack(start + length, segment_count + 1)
                
                # === UNCHOOSE ===
                segments.pop()
        
        backtrack(0, 0)
        return results


def solve():
    """
    Input format:
    Line 1: s (digit string)
    
    Example:
    25525511135
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')
    
    s = lines[0]
    
    solver = get_solver(SOLUTIONS)
    result = solver.restoreIpAddresses(s)
    
    print(result)


if __name__ == "__main__":
    solve()


"""
Problem: Validate IP Address
Link: https://leetcode.com/problems/validate-ip-address/

Return "IPv4", "IPv6", or "Neither" based on IP address validity.

IPv4: x1.x2.x3.x4 where 0 <= xi <= 255, no leading zeros
IPv6: x1:x2:...:x8 where 1 <= len(xi) <= 4, hex chars only

Constraints:
- queryIP consists of letters, digits, '.', and ':'

Topics: String
"""
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "validIPAddress",
        "complexity": "O(n) time, O(1) space",
        "description": "String parsing with validation rules",
    },
}


# JUDGE_FUNC for generated tests
def _reference(queryIP: str) -> str:
    """Reference implementation."""
    def is_ipv4(ip):
        parts = ip.split(".")
        if len(parts) != 4:
            return False
        for p in parts:
            if not p or not p.isdigit():
                return False
            if len(p) > 1 and p[0] == '0':
                return False
            if int(p) > 255:
                return False
        return True

    def is_ipv6(ip):
        parts = ip.split(":")
        if len(parts) != 8:
            return False
        hex_chars = set("0123456789abcdefABCDEF")
        for p in parts:
            if not p or len(p) > 4:
                return False
            if not all(c in hex_chars for c in p):
                return False
        return True

    if '.' in queryIP:
        return "IPv4" if is_ipv4(queryIP) else "Neither"
    if ':' in queryIP:
        return "IPv6" if is_ipv6(queryIP) else "Neither"
    return "Neither"


def judge(actual, expected, input_data: str) -> bool:
    queryIP = json.loads(input_data.strip())
    if isinstance(actual, str) and actual.startswith('"'):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str) and expected.startswith('"'):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(queryIP)


JUDGE_FUNC = judge


# ============================================================================
# Solution: String Parsing
# Time: O(n), Space: O(1)
# ============================================================================
class Solution:
    # IPv4 validation rules:
    #   - Exactly 4 parts separated by '.'
    #   - Each part: all digits, 0-255, no leading zeros (except "0")
    #
    # IPv6 validation rules:
    #   - Exactly 8 parts separated by ':'
    #   - Each part: 1-4 hex characters (0-9, a-f, A-F)
    #   - Leading zeros ARE allowed

    def validIPAddress(self, queryIP: str) -> str:
        def is_valid_ipv4(ip: str) -> bool:
            parts = ip.split(".")
            if len(parts) != 4:
                return False
            for part in parts:
                if not part:  # empty
                    return False
                if not part.isdigit():  # non-digit chars
                    return False
                if len(part) > 1 and part[0] == '0':  # leading zero
                    return False
                if int(part) > 255:  # out of range
                    return False
            return True

        def is_valid_ipv6(ip: str) -> bool:
            parts = ip.split(":")
            if len(parts) != 8:
                return False
            hex_chars = set("0123456789abcdefABCDEF")
            for part in parts:
                if not part or len(part) > 4:
                    return False
                if not all(c in hex_chars for c in part):
                    return False
            return True

        if '.' in queryIP:
            return "IPv4" if is_valid_ipv4(queryIP) else "Neither"
        if ':' in queryIP:
            return "IPv6" if is_valid_ipv6(queryIP) else "Neither"
        return "Neither"


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: queryIP (JSON string)

    Example:
        "172.16.254.1"
        -> "IPv4"
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    queryIP = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.validIPAddress(queryIP)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

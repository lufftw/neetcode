# solutions/0271_encode_and_decode_strings.py
"""
Problem: Encode and Decode Strings
https://leetcode.com/problems/encode-and-decode-strings/

Design an algorithm to encode a list of strings to a single string.
The encoded string is sent over the network and decoded back to the
original list of strings.

Key insight: Use length prefix (with delimiter) to unambiguously mark
where each string starts and ends. Simple delimiters fail because they
could appear in the strings themselves.

Constraints:
- Strings may contain any ASCII character
- Algorithm must be stateless
- Cannot use serialization methods (like eval)
"""
import json
import sys
from typing import List

from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "Codec",
        "method": "encode",
        "complexity": "O(n) time, O(n) space",
        "description": "Length prefix with delimiter",
    },
}


class Codec:
    """
    Length prefix encoding.

    WHY: Simple delimiters (like comma or newline) could appear inside
    strings, making decoding ambiguous. By prefixing each string with its
    length and a delimiter, we know exactly how many characters to read.

    HOW:
    - Encode: For each string, output "len#string" where len is the length
    - Decode: Read digits until #, parse as length, read that many chars
    """

    def encode(self, strs: List[str]) -> str:
        """Encodes a list of strings to a single string."""
        result = []
        for s in strs:
            result.append(f"{len(s)}#{s}")
        return "".join(result)

    def decode(self, s: str) -> List[str]:
        """Decodes a single string to a list of strings."""
        result = []
        i = 0

        while i < len(s):
            # Find the delimiter
            j = i
            while s[j] != "#":
                j += 1

            # Parse length
            length = int(s[i:j])

            # Extract string
            result.append(s[j + 1 : j + 1 + length])

            # Move to next encoded string
            i = j + 1 + length

        return result


def judge(actual, expected, input_data: str) -> bool:
    """
    Validate encode/decode roundtrip.
    The actual output should match the original input.
    """
    if isinstance(actual, str):
        actual = json.loads(actual)

    # Parse original input
    original = json.loads(input_data.strip())

    # Actual is the result after encode->decode roundtrip
    return actual == original


JUDGE_FUNC = judge


def solve():
    lines = sys.stdin.read().strip().split("\n")
    strs = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)

    # Encode then decode (roundtrip test)
    encoded = solver.encode(strs)
    result = solver.decode(encoded)

    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    solve()

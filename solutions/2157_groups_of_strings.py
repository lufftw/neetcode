"""
Problem: Groups of Strings
Link: https://leetcode.com/problems/groups-of-strings/

Two strings are connected if one can be obtained from the other by adding,
deleting, or replacing exactly one letter. Find max groups and largest group size.

Constraints:
- 1 <= words.length <= 2 * 10^4
- 1 <= words[i].length <= 26
- No letter occurs more than once in words[i]

Topics: String, Bit Manipulation, Union Find
"""
from typing import List
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "groupStrings",
        "complexity": "O(n * 26) time, O(n * 26) space",
        "description": "Union-Find with bitmask representation and delete-mask trick",
    },
}


# JUDGE_FUNC for generated tests
def _reference(words: List[str]) -> List[int]:
    """Reference implementation using Union-Find."""
    n = len(words)
    parent = list(range(n))
    size = [1] * n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[py] = px
            size[px] += size[py]

    masks = [sum(1 << (ord(c) - ord('a')) for c in w) for w in words]
    mask_to_idx = {}
    delete_to_idx = {}

    for i, mask in enumerate(masks):
        if mask in mask_to_idx:
            union(i, mask_to_idx[mask])
        else:
            mask_to_idx[mask] = i

        for b in range(26):
            if mask & (1 << b):
                del_mask = mask ^ (1 << b)
                if del_mask in mask_to_idx:
                    union(i, mask_to_idx[del_mask])
                if del_mask in delete_to_idx:
                    union(i, delete_to_idx[del_mask])
                else:
                    delete_to_idx[del_mask] = i

    num_groups = sum(1 for i in range(n) if find(i) == i)
    max_size = max((size[i] for i in range(n) if find(i) == i), default=0)
    return [num_groups, max_size]


def judge(actual, expected, input_data: str) -> bool:
    words = json.loads(input_data.strip().split('\n')[0])
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    return actual == _reference(words)


JUDGE_FUNC = judge


# ============================================================================
# Solution: Union-Find with Bitmask
# Time: O(n * 26 * α(n)), Space: O(n * 26)
# ============================================================================
class Solution:
    # Key insight:
    #   - Represent each word as 26-bit bitmask (bit i = 1 if letter i present)
    #   - Add/Delete: masks differ by exactly one bit
    #   - Replace: masks have same popcount and differ by one bit each way
    #
    # Efficient connection detection:
    #   - For each word, try all "delete" masks (remove one bit)
    #   - If delete_mask is an actual word → Add/Delete connection
    #   - If two words share same delete_mask → Replace connection
    #     (both can delete to same intermediate, so they differ by one char)
    #
    # Union-Find tracks connected components efficiently.

    def groupStrings(self, words: List[str]) -> List[int]:
        n = len(words)

        # Union-Find with path compression and union by rank
        parent = list(range(n))
        rank = [0] * n
        size = [1] * n

        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x: int, y: int) -> None:
            px, py = find(x), find(y)
            if px == py:
                return
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            size[px] += size[py]
            if rank[px] == rank[py]:
                rank[px] += 1

        # Convert each word to bitmask
        masks = []
        for word in words:
            mask = 0
            for c in word:
                mask |= (1 << (ord(c) - ord('a')))
            masks.append(mask)

        # mask_to_idx: bitmask -> first word index with this exact mask
        # delete_to_idx: delete_mask -> first word index that generated it
        mask_to_idx = {}
        delete_to_idx = {}

        for i, mask in enumerate(masks):
            # Duplicate masks: union with first occurrence
            if mask in mask_to_idx:
                union(i, mask_to_idx[mask])
            else:
                mask_to_idx[mask] = i

            # Try removing each bit that's set
            for b in range(26):
                if mask & (1 << b):
                    del_mask = mask ^ (1 << b)

                    # If del_mask is an actual word: Add/Delete connection
                    if del_mask in mask_to_idx:
                        union(i, mask_to_idx[del_mask])

                    # If another word shares this delete_mask: Replace connection
                    if del_mask in delete_to_idx:
                        union(i, delete_to_idx[del_mask])
                    else:
                        delete_to_idx[del_mask] = i

        # Count components and find max size
        num_groups = 0
        max_size = 0
        for i in range(n):
            if find(i) == i:
                num_groups += 1
                max_size = max(max_size, size[i])

        return [num_groups, max_size]


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: words (JSON array)

    Example:
        ["a","b","ab","cde"]
        -> [2,3]
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    words = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.groupStrings(words)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

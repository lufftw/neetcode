"""
Problem: Hand of Straights
Link: https://leetcode.com/problems/hand-of-straights/

Alice has some number of cards and she wants to rearrange the cards into groups so
that each group is of size groupSize, and consists of groupSize consecutive cards.

Given an integer array hand where hand[i] is the value written on the ith card and
an integer groupSize, return true if she can rearrange the cards, or false otherwise.

Example 1:
    Input: hand = [1,2,3,6,2,3,4,7,8], groupSize = 3
    Output: true
    Explanation: Alice's hand can be rearranged as [1,2,3],[2,3,4],[6,7,8]

Example 2:
    Input: hand = [1,2,3,4,5], groupSize = 4
    Output: false
    Explanation: Alice's hand can not be rearranged into groups of 4.

Constraints:
- 1 <= hand.length <= 10^4
- 0 <= hand[i] <= 10^9
- 1 <= groupSize <= hand.length

Note: This problem is the same as LeetCode 1296 "Divide Array in Sets of Consecutive
Numbers".

Topics: Array, Hash Table, Greedy, Sorting
"""

import json
from typing import List, Dict
from collections import Counter
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionGreedy",
        "method": "isNStraightHand",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Greedy: always start group from smallest available card",
    },
    "ordered_dict": {
        "class": "SolutionSortedCounter",
        "method": "isNStraightHand",
        "complexity": "O(n log n) time, O(n) space",
        "description": "Process unique values in sorted order, track deficits",
    },
}


# ============================================================================
# Solution 1: Greedy with Counter
# Time: O(n log n) for sorting + O(n * groupSize) for group formation
# Space: O(n) for counter
#
# Key Insight:
#   The greedy choice is always correct: start each group with the smallest
#   available card. This works because:
#   - The smallest card MUST be the start of some group (it can't be middle/end)
#   - Once we know the start, the rest of the group is determined
#   - If we can't complete a group starting from the smallest, it's impossible
#
# Algorithm:
#   1. Count occurrences of each card value
#   2. Sort unique values
#   3. For each unique value (in sorted order):
#      - If count > 0, start groups using this value
#      - For each group, decrement counts of consecutive values
#      - If any consecutive value unavailable, return False
#   4. Return True if all cards used
#
# Why Greedy Works:
#   The smallest card has no choice - it must start a group. Once we commit to
#   that, we must include the next groupSize-1 consecutive cards. Any other
#   assignment would leave the smallest card orphaned.
# ============================================================================
class SolutionGreedy:
    """
    Greedy approach starting groups from smallest available card.

    The key observation is that the minimum card must be the start of a group
    (it cannot be in the middle or end). This gives us a deterministic greedy
    strategy: always start from the smallest and build consecutive groups.
    """

    def isNStraightHand(self, hand: List[int], groupSize: int) -> bool:
        # Quick check: total cards must be divisible by groupSize
        if len(hand) % groupSize != 0:
            return False

        # groupSize of 1 means any arrangement works
        if groupSize == 1:
            return True

        # Count occurrences of each card
        count = Counter(hand)

        # Process cards in sorted order
        for card in sorted(count.keys()):
            # How many groups must start with this card?
            num_groups = count[card]

            if num_groups > 0:
                # Form num_groups groups starting with this card
                for next_card in range(card, card + groupSize):
                    if count[next_card] < num_groups:
                        # Not enough cards to complete all groups
                        return False
                    count[next_card] -= num_groups

        return True


# ============================================================================
# Solution 2: Min-Heap Approach
# Time: O(n log n) for sorting/heap operations
# Space: O(n)
#
# Key Insight:
#   Use a min-heap to always process the smallest card. For each card, try
#   to form a complete group starting from it. This is essentially the same
#   greedy logic but implemented with explicit heap operations.
#
# Algorithm:
#   - Build a min-heap of all cards
#   - While heap is not empty:
#     - Pop the minimum card as group start
#     - Try to find next groupSize-1 consecutive cards
#     - Remove used cards from the data structure
#
# This approach is more intuitive: we literally pick the smallest card and
# try to build a group, just like the problem description suggests.
# ============================================================================
class SolutionSortedCounter:
    """
    Min-heap based approach processing cards in sorted order.

    We maintain a counter and process unique values. For each value,
    we must use all cards of that value to start groups (they can't be
    in the middle of groups since they're the smallest remaining).
    """

    def isNStraightHand(self, hand: List[int], groupSize: int) -> bool:
        if len(hand) % groupSize != 0:
            return False

        if groupSize == 1:
            return True

        count = Counter(hand)
        # Use a sorted list (or sortedcontainers.SortedDict in production)
        min_heap = sorted(count.keys())

        i = 0
        while i < len(min_heap):
            start = min_heap[i]

            # Skip if this value is exhausted
            if count[start] == 0:
                i += 1
                continue

            # Try to form groups starting with 'start'
            for card in range(start, start + groupSize):
                if count[card] <= 0:
                    return False
                count[card] -= 1

        return True


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: hand as JSON array
        Line 2: groupSize as integer

    Example:
        [1,2,3,6,2,3,4,7,8]
        3
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")

    hand = json.loads(lines[0])
    groupSize = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.isNStraightHand(hand, groupSize)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

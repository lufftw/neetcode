"""
Problem: Best Time to Buy and Sell Stock with Cooldown
Link: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/

You are given an array prices where prices[i] is the price of a given stock on
the ith day.

Find the maximum profit you can achieve. You may complete as many transactions
as you like (i.e., buy one and sell one share of the stock multiple times) with
the following restrictions:
- After you sell your stock, you cannot buy stock on the next day (i.e., cooldown one day).

Note: You may not engage in multiple transactions simultaneously (i.e., you must
sell the stock before you buy again).

Example 1:
    Input: prices = [1,2,3,0,2]
    Output: 3
    Explanation: transactions = [buy, sell, cooldown, buy, sell]

Example 2:
    Input: prices = [1]
    Output: 0

Constraints:
- 1 <= prices.length <= 5000
- 0 <= prices[i] <= 1000

Topics: Array, Dynamic Programming
"""

import json
from typing import List
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionStateMachine",
        "method": "maxProfit",
        "complexity": "O(n) time, O(1) space",
        "description": "State machine with 3 states: hold, sold, rest",
    },
    "dp_2d": {
        "class": "SolutionDP2D",
        "method": "maxProfit",
        "complexity": "O(n) time, O(n) space",
        "description": "2D DP with hold/not-hold states, explicit transitions",
    },
}


# ============================================================================
# Solution 1: State Machine (Optimal)
# Time: O(n), Space: O(1)
#
# Key Insight:
#   Model the problem as a finite state machine with 3 states:
#   - HOLD: Currently holding a stock
#   - SOLD: Just sold (must cooldown next day)
#   - REST: Not holding, free to buy
#
#   Transitions:
#   - hold[i] = max(hold[i-1], rest[i-1] - prices[i])
#     (keep holding, or buy from rest state)
#   - sold[i] = hold[i-1] + prices[i]
#     (sell what we're holding)
#   - rest[i] = max(rest[i-1], sold[i-1])
#     (keep resting, or transition from cooldown)
#
# Why State Machine:
#   The cooldown constraint creates dependencies between states. A state
#   machine makes these dependencies explicit and naturally handles the
#   "you must wait one day after selling before buying" constraint.
#
# Space Optimization:
#   Since each state only depends on the previous day, we need only O(1)
#   space by maintaining three variables instead of arrays.
# ============================================================================
class SolutionStateMachine:
    """
    Finite state machine approach with hold/sold/rest states.

    The state machine elegantly captures the cooldown constraint:
    - From HOLD: can stay or SELL → SOLD
    - From SOLD: must go to REST (cooldown)
    - From REST: can stay or BUY → HOLD

    This makes the transition rules crystal clear and the code concise.
    """

    def maxProfit(self, prices: List[int]) -> int:
        if not prices:
            return 0

        n = len(prices)

        # Initial states on day 0
        hold = -prices[0]  # Bought on day 0
        sold = 0  # Can't have sold anything yet (but set to 0 for transition)
        rest = 0  # Haven't done anything

        for i in range(1, n):
            # Save previous values (order matters due to dependencies)
            prev_hold = hold
            prev_sold = sold
            prev_rest = rest

            # Update states
            hold = max(prev_hold, prev_rest - prices[i])  # Keep or buy
            sold = prev_hold + prices[i]  # Sell
            rest = max(prev_rest, prev_sold)  # Rest or was cooling down

        # Final answer: max of sold (just sold) or rest (not holding)
        # hold state means we're still holding, which isn't useful at the end
        return max(sold, rest)


# ============================================================================
# Solution 2: 2D DP with Hold/Not-Hold States
# Time: O(n), Space: O(n)
#
# Key Insight:
#   Classic DP formulation with two primary states at each day:
#   - dp[i][0]: Max profit on day i when NOT holding stock
#   - dp[i][1]: Max profit on day i when HOLDING stock
#
#   The cooldown is handled by looking back 2 days when buying:
#   - dp[i][1] = max(dp[i-1][1], dp[i-2][0] - prices[i])
#     (keep holding, or buy after cooldown from selling 2+ days ago)
#   - dp[i][0] = max(dp[i-1][0], dp[i-1][1] + prices[i])
#     (keep not-holding, or sell today)
#
# Why Look Back 2 Days:
#   If we sold on day i-1, we're in cooldown on day i, so we can't buy.
#   To buy on day i, we must have been NOT holding on day i-2 (sold on
#   day i-2 or earlier). This is why dp[i-2][0] is used for buying.
# ============================================================================
class SolutionDP2D:
    """
    2D DP tracking hold/not-hold states with explicit cooldown handling.

    The key insight is that buying on day i requires looking at dp[i-2][0]
    (not-holding state from 2 days ago) due to the cooldown restriction.
    This makes the cooldown constraint explicit in the recurrence.
    """

    def maxProfit(self, prices: List[int]) -> int:
        if not prices:
            return 0

        n = len(prices)
        if n == 1:
            return 0

        # dp[i][0] = max profit on day i, not holding
        # dp[i][1] = max profit on day i, holding
        dp = [[0, 0] for _ in range(n)]

        # Base cases
        dp[0][0] = 0  # Not holding on day 0
        dp[0][1] = -prices[0]  # Bought on day 0

        # Day 1 special case (can buy on day 1 without cooldown issue)
        dp[1][0] = max(dp[0][0], dp[0][1] + prices[1])  # Keep or sell
        dp[1][1] = max(dp[0][1], -prices[1])  # Keep or buy (no previous sell)

        for i in range(2, n):
            # Not holding: either keep not-holding or sell today
            dp[i][0] = max(dp[i - 1][0], dp[i - 1][1] + prices[i])

            # Holding: either keep holding or buy today
            # To buy today, must look at dp[i-2][0] (cooldown from any sell)
            dp[i][1] = max(dp[i - 1][1], dp[i - 2][0] - prices[i])

        # Answer: max profit when not holding at the end
        return dp[n - 1][0]


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: prices as JSON array

    Example:
        [1,2,3,0,2]
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")

    prices = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.maxProfit(prices)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

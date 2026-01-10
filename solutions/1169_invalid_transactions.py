"""
Problem: Invalid Transactions
Link: https://leetcode.com/problems/invalid-transactions/

A transaction is possibly invalid if:
1. The amount exceeds $1000, OR
2. If it occurs within (and including) 60 minutes of another transaction
   with the same name in a different city.

You are given an array of strings transaction where transactions[i] consists
of comma-separated values: name, time (in minutes), amount, and city.

Return a list of transactions that are possibly invalid. Answer can be in any order.

Example 1:
    Input: transactions = ["alice,20,800,mtv","alice,50,100,beijing"]
    Output: ["alice,20,800,mtv","alice,50,100,beijing"]
    Explanation: Both invalid due to same name, different city, within 60 min.

Example 2:
    Input: transactions = ["alice,20,800,mtv","alice,50,1200,mtv"]
    Output: ["alice,50,1200,mtv"]
    Explanation: Only second is invalid (amount > 1000).

Example 3:
    Input: transactions = ["alice,20,800,mtv","bob,50,1200,mtv"]
    Output: ["bob,50,1200,mtv"]

Constraints:
- transactions.length <= 1000
- Each transactions[i] = "{name},{time},{amount},{city}"
- 1 <= name.length, city.length <= 10
- 0 <= time <= 1000
- 0 <= amount <= 2000

Topics: Array, Hash Table, String, Sorting
"""
from typing import List
from collections import defaultdict
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "invalidTransactions",
        "complexity": "O(n^2) time, O(n) space",
        "description": "Group by name and check pairwise conflicts",
    },
}


# Custom judge because output order can vary
def judge(actual: List[str], expected: List[str], input_data: str) -> bool:
    """Accept any ordering of the invalid transactions."""
    return sorted(actual) == sorted(expected)


JUDGE_FUNC = judge
COMPARE_MODE = "set"  # Alternative: use set comparison


# ============================================================================
# Solution: Group by Name and Check Pairwise
# Time: O(n^2) worst case (all same name), Space: O(n)
#
# Two rules for invalid:
# 1. Amount > 1000 (check independently)
# 2. Same name, different city, time difference <= 60 (need pairwise check)
#
# For rule 2, group transactions by name, then for each pair check:
# - Different city?
# - abs(time1 - time2) <= 60?
# If both true, both transactions are invalid.
# ============================================================================
class Solution:
    def invalidTransactions(self, transactions: List[str]) -> List[str]:
        """
        Find all potentially invalid transactions.

        Parse each transaction, group by name, then check:
        1. Amount > 1000 -> invalid
        2. For same name: different city AND within 60 min -> both invalid

        Args:
            transactions: List of "name,time,amount,city" strings

        Returns:
            List of invalid transaction strings
        """
        n = len(transactions)

        # Parse all transactions
        parsed = []
        for t in transactions:
            parts = t.split(',')
            name = parts[0]
            time = int(parts[1])
            amount = int(parts[2])
            city = parts[3]
            parsed.append((name, time, amount, city))

        # Group by name for efficient pairwise checks
        by_name = defaultdict(list)
        for i, (name, time, amount, city) in enumerate(parsed):
            by_name[name].append(i)

        # Track which transactions are invalid
        invalid = [False] * n

        for i in range(n):
            name, time, amount, city = parsed[i]

            # Rule 1: Amount > 1000
            if amount > 1000:
                invalid[i] = True

            # Rule 2: Check against other transactions with same name
            for j in by_name[name]:
                if i == j:
                    continue

                _, other_time, _, other_city = parsed[j]

                # Same name, different city, within 60 minutes
                if other_city != city and abs(time - other_time) <= 60:
                    invalid[i] = True
                    invalid[j] = True

        # Collect invalid transactions
        return [transactions[i] for i in range(n) if invalid[i]]


def solve():
    """
    Input format:
    Line 1: transactions (JSON array of strings)
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')

    transactions = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.invalidTransactions(transactions)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

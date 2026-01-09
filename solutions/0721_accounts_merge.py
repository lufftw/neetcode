# solutions/0721_accounts_merge.py
"""
Problem: Accounts Merge
Link: https://leetcode.com/problems/accounts-merge/

Given a list of accounts where each element accounts[i] is a list of strings, where the first
element accounts[i][0] is a name, and the rest of the elements are emails representing emails
of the account.

Now, we would like to merge these accounts. Two accounts definitely belong to the same person
if there is some common email to both accounts. Note that even if two accounts have the same
name, they may belong to different people as people could have the same name. A person can
have any number of accounts initially, but all of their accounts definitely have the same name.

After merging the accounts, return the accounts in the following format: the first element of
each account is the name, and the rest of the elements are emails in sorted order. The accounts
themselves can be returned in any order.

Example 1:
    Input: accounts = [["John","johnsmith@mail.com","john_newyork@mail.com"],
                       ["John","johnsmith@mail.com","john00@mail.com"],
                       ["Mary","mary@mail.com"],
                       ["John","johnnybravo@mail.com"]]
    Output: [["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],
             ["Mary","mary@mail.com"],
             ["John","johnnybravo@mail.com"]]

Constraints:
- 1 <= accounts.length <= 1000
- 2 <= accounts[i].length <= 10
- 1 <= accounts[i][j].length <= 30
- accounts[i][0] consists of English letters.
- accounts[i][j] (for j > 0) is a valid email.

Topics: Array, String, DFS, BFS, Union Find, Sorting
"""
from typing import List
from collections import defaultdict
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Accounts Merge solution."""
    import json

    # Parse input
    accounts = json.loads(input_data.strip())

    # Normalize: sort emails within each account, then sort all accounts
    def normalize(result):
        return sorted([acc[0]] + sorted(acc[1:]) for acc in result)

    # If expected is available, compare directly
    if expected is not None:
        return normalize(actual) == normalize(expected)

    # Judge-only mode: compute expected
    expected_result = _accounts_merge(accounts)
    return normalize(actual) == normalize(expected_result)


def _accounts_merge(accounts):
    """Reference solution for validation."""
    from collections import defaultdict

    n = len(accounts)
    parent = list(range(n))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[py] = px

    email_to_account = {}
    for i, account in enumerate(accounts):
        for email in account[1:]:
            if email in email_to_account:
                union(i, email_to_account[email])
            else:
                email_to_account[email] = i

    root_to_emails = defaultdict(set)
    for email, acc_idx in email_to_account.items():
        root = find(acc_idx)
        root_to_emails[root].add(email)

    result = []
    for root, emails in root_to_emails.items():
        name = accounts[root][0]
        result.append([name] + sorted(emails))

    return result


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "accountsMerge",
        "complexity": "O(n × k × α(n)) time, O(n × k) space",
        "description": "Union-Find for equivalence grouping",
        "api_kernels": ["UnionFindConnectivity"],
        "patterns": ["union_find_equivalence_grouping"],
    },
    "union_find": {
        "class": "Solution",
        "method": "accountsMerge",
        "complexity": "O(n × k × α(n)) time, O(n × k) space",
        "description": "Union-Find grouping accounts by shared emails",
    },
    "dfs": {
        "class": "SolutionDFS",
        "method": "accountsMerge",
        "complexity": "O(n × k) time, O(n × k) space",
        "description": "DFS graph traversal - emails as nodes",
    },
}


# ============================================
# Solution 1: Union-Find Equivalence Grouping
# Time: O(n × k × α(n)), Space: O(n × k)
# ============================================
class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        """
        Merge accounts that share at least one common email.

        Core insight: Emails define equivalence between accounts. If account A
        and B share an email, they're the same person. Union-Find groups accounts
        transitively. Map each email to its first account, union when email is seen
        again. Finally, collect all emails by component root.

        Invariant: email_to_account maps each unique email to an account index;
        accounts in the same Union-Find component belong to the same person.

        Args:
            accounts: List of [name, email1, email2, ...] entries

        Returns:
            Merged accounts with [name, sorted_emails...]
        """
        n = len(accounts)
        parent = list(range(n))
        rank = [0] * n

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
            if rank[px] == rank[py]:
                rank[px] += 1

        # Map email to first account index
        email_to_account: dict[str, int] = {}

        for i, account in enumerate(accounts):
            for email in account[1:]:
                if email in email_to_account:
                    union(i, email_to_account[email])
                else:
                    email_to_account[email] = i

        # Collect emails by root
        root_to_emails: dict[int, set[str]] = defaultdict(set)
        for email, account_idx in email_to_account.items():
            root = find(account_idx)
            root_to_emails[root].add(email)

        # Build result
        result: list[list[str]] = []
        for root, emails in root_to_emails.items():
            name = accounts[root][0]
            result.append([name] + sorted(emails))

        return result


# ============================================
# Solution 2: DFS Graph Traversal
# Time: O(n × k), Space: O(n × k)
# ============================================
class SolutionDFS:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        """
        Merge accounts using DFS on email graph.

        Core insight: Build a graph where emails are nodes, and edges connect
        emails that appear in the same account. DFS from any unvisited email
        finds all emails belonging to the same person (connected component).

        This is a graph-based alternative to Union-Find, treating the problem
        as finding connected components in an email graph.

        Args:
            accounts: List of [name, email1, email2, ...] entries

        Returns:
            Merged accounts with [name, sorted_emails...]
        """
        # Build email graph and track email->name mapping
        email_graph: dict[str, set[str]] = defaultdict(set)
        email_to_name: dict[str, str] = {}

        for account in accounts:
            name = account[0]
            first_email = account[1]

            for email in account[1:]:
                email_graph[first_email].add(email)
                email_graph[email].add(first_email)
                email_to_name[email] = name

        # DFS to find connected components
        visited: set[str] = set()
        result: list[list[str]] = []

        def dfs(email: str, component: list[str]) -> None:
            visited.add(email)
            component.append(email)
            for neighbor in email_graph[email]:
                if neighbor not in visited:
                    dfs(neighbor, component)

        for email in email_graph:
            if email not in visited:
                component: list[str] = []
                dfs(email, component)
                name = email_to_name[email]
                result.append([name] + sorted(component))

        return result


def solve():
    """
    Input format (canonical JSON):
    Line 1: 2D array accounts

    Output format:
    2D array of merged accounts
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    accounts = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.accountsMerge(accounts)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

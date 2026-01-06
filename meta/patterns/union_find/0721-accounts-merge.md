## Accounts Merge (LeetCode 721)

> **Problem**: Merge accounts that share common emails.
> **Invariant**: Same email in different accounts = same person.
> **Role**: VARIANT applying Union-Find to string grouping.

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "merge by common element" | → Union-Find with element mapping |
| "group equivalent items" | → Map items to indices |
| "transitive equivalence" | → If A~B and B~C, then A~C |

### Implementation

```python
# Pattern: union_find_equivalence_grouping
# See: docs/patterns/union_find/templates.md Section 3

class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        """
        Merge accounts sharing common emails.

        Key Insight:
        - Map each email to first account index that has it
        - If email seen before, union current account with previous account
        - Collect emails by component root

        Why Union-Find?
        - Handles transitive relationships naturally
        - A shares email with B, B shares with C → A, B, C all merge
        """
        from collections import defaultdict

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
            for email in account[1:]:  # Skip name
                if email in email_to_account:
                    # Union this account with account that has same email
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
```

### Trace Example

```
Input: accounts = [
    ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
    ["John", "johnsmith@mail.com", "john00@mail.com"],
    ["Mary", "mary@mail.com"],
    ["John", "johnnybravo@mail.com"]
]

Process:
Account 0: emails = {johnsmith@mail.com, john_newyork@mail.com}
  email_to_account = {johnsmith: 0, john_newyork: 0}

Account 1: emails = {johnsmith@mail.com, john00@mail.com}
  johnsmith seen! union(1, 0)
  email_to_account = {..., john00: 1}

Account 2: emails = {mary@mail.com}
  email_to_account = {..., mary: 2}

Account 3: emails = {johnnybravo@mail.com}
  email_to_account = {..., johnnybravo: 3}

Roots: 0→{johnsmith, john_newyork, john00}, 2→{mary}, 3→{johnnybravo}

Output: [
    ["John", "john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"],
    ["Mary", "mary@mail.com"],
    ["John", "johnnybravo@mail.com"]
]
```

### Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n × k × α(n)) where k = avg emails per account |
| Space | O(n × k) for email mapping |

### Related Problems

| Problem | Variation |
|---------|-----------|
| LC 990: Equation Satisfaction | Group by character equality |
| LC 839: Similar String Groups | Group by string similarity |
| LC 1202: Smallest String With Swaps | Group by swap indices |



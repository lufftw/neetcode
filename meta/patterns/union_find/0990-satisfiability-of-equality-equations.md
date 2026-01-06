## Satisfiability of Equality Equations (LeetCode 990)

> **Problem**: Check if equality/inequality equations are satisfiable.
> **Invariant**: Equal variables must be in same component; unequal must be in different.
> **Role**: VARIANT applying Union-Find to constraint satisfaction.

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "equality constraints" | → Union-Find: union equal variables |
| "inequality constraints" | → Check: must be in different components |
| "satisfiable" | → Process equalities first, then check inequalities |

### Implementation

```python
# Pattern: union_find_constraint_satisfaction
# See: docs/patterns/union_find/templates.md Section 5

class Solution:
    def equationsPossible(self, equations: List[str]) -> bool:
        """
        Check if all equations can be satisfied.

        Key Insight:
        - Process '==' first: union all equal variables
        - Then check '!=': must be in different components
        - If any '!=' has variables in same component → unsatisfiable

        Why two passes?
        - Equality is transitive (a==b, b==c → a==c)
        - Must build all equality relationships before checking inequality
        """
        parent = list(range(26))  # 26 lowercase letters
        rank = [0] * 26

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

        # Pass 1: Process all equalities
        for eq in equations:
            if eq[1] == '=':  # "a==b"
                x = ord(eq[0]) - ord('a')
                y = ord(eq[3]) - ord('a')
                union(x, y)

        # Pass 2: Check all inequalities
        for eq in equations:
            if eq[1] == '!':  # "a!=b"
                x = ord(eq[0]) - ord('a')
                y = ord(eq[3]) - ord('a')
                if find(x) == find(y):
                    return False  # Contradiction!

        return True
```

### Trace Example

```
Input: equations = ["a==b", "b!=c", "c==a"]

Pass 1 (equalities):
- "a==b": union(0, 1) → parent[1] = 0
- "c==a": union(2, 0) → parent[2] = 0

Components: {a, b, c} all in same component

Pass 2 (inequalities):
- "b!=c": find(b)=0, find(c)=0, SAME! → return False

Output: False
```

### Another Example

```
Input: equations = ["a==b", "b==c", "a==c"]

Pass 1:
- union(a, b): {a, b}
- union(b, c): {a, b, c}
- union(a, c): already same component

Pass 2: No inequalities

Output: True
```

### Edge Cases

```python
# Self-inequality
equations = ["a!=a"]
# Pass 1: nothing
# Pass 2: find(a) == find(a) → False

# Self-equality (trivially true)
equations = ["a==a"]
# Pass 1: union(a, a) → no-op
# Pass 2: nothing
# Output: True

# Disjoint groups with inequality
equations = ["a==b", "c==d", "a!=d"]
# Pass 1: {a,b}, {c,d}
# Pass 2: find(a)≠find(d) → True
```

### Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n × α(26)) ≈ O(n) |
| Space | O(1) (fixed 26 characters) |

### Related Problems

| Problem | Variation |
|---------|-----------|
| LC 721: Accounts Merge | Group by common elements |
| LC 399: Evaluate Division | Weighted Union-Find |
| LC 1061: Lexicographically Smallest Equivalent String | Find smallest in component |



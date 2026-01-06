# solutions/0990_satisfiability_of_equality_equations.py
"""
Problem: Satisfiability of Equality Equations
Link: https://leetcode.com/problems/satisfiability-of-equality-equations/

You are given an array of strings equations that represent relationships between variables where
each string equations[i] is of length 4 and takes one of two different forms: "xi==yi" or "xi!=yi".
Here, xi and yi are lowercase letters (not necessarily different) that represent one-letter
variable names.

Return true if it is possible to assign integers to variable names so as to satisfy all the
given equations, or false otherwise.

Example 1:
    Input: equations = ["a==b","b!=a"]
    Output: false
    Explanation: If we assign say, a = 1 and b = 1, then the first equation is satisfied,
    but not the second. There is no way to assign the variables to satisfy both equations.

Example 2:
    Input: equations = ["b==a","a==b"]
    Output: true
    Explanation: We could assign a = 1 and b = 1 to satisfy both equations.

Constraints:
- 1 <= equations.length <= 500
- equations[i].length == 4
- equations[i][0] is a lowercase letter.
- equations[i][1] is either '=' or '!'.
- equations[i][2] is '='.
- equations[i][3] is a lowercase letter.

Topics: Array, String, Union Find, Graph
"""
from typing import List
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Equality Equations solution."""
    import json

    # Parse input
    equations = json.loads(input_data.strip())

    # Normalize actual to boolean
    if isinstance(actual, str):
        actual = actual.lower() == 'true'

    # If expected is available, compare directly
    if expected is not None:
        if isinstance(expected, str):
            expected = expected.lower() == 'true'
        return actual == expected

    # Judge-only mode: compute expected
    expected_result = _equations_possible(equations)
    return actual == expected_result


def _equations_possible(equations):
    """Reference solution for validation."""
    parent = list(range(26))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    # Pass 1: Union equalities
    for eq in equations:
        if eq[1] == '=':
            x = ord(eq[0]) - ord('a')
            y = ord(eq[3]) - ord('a')
            parent[find(y)] = find(x)

    # Pass 2: Check inequalities
    for eq in equations:
        if eq[1] == '!':
            x = ord(eq[0]) - ord('a')
            y = ord(eq[3]) - ord('a')
            if find(x) == find(y):
                return False

    return True


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "equationsPossible",
        "complexity": "O(n × α(26)) time, O(1) space",
        "description": "Union-Find constraint satisfaction",
        "api_kernels": ["UnionFindConnectivity"],
        "patterns": ["union_find_constraint_satisfaction"],
    },
}


# ============================================
# Solution 1: Union-Find Constraint Satisfaction
# Time: O(n × α(26)), Space: O(1)
# ============================================
class Solution:
    def equationsPossible(self, equations: List[str]) -> bool:
        """
        Check if all equations can be satisfied.

        Key Insight:
        - Process '==' first: union all equal variables
        - Then check '!=': must be in different components
        - Two passes ensure transitive equalities are captured
        """
        parent = list(range(26))
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
            if eq[1] == '=':
                x = ord(eq[0]) - ord('a')
                y = ord(eq[3]) - ord('a')
                union(x, y)

        # Pass 2: Check all inequalities
        for eq in equations:
            if eq[1] == '!':
                x = ord(eq[0]) - ord('a')
                y = ord(eq[3]) - ord('a')
                if find(x) == find(y):
                    return False

        return True


def solve():
    """
    Input format (canonical JSON):
    Line 1: Array of equation strings

    Output format:
    Boolean: true/false
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    equations = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.equationsPossible(equations)

    print(str(result).lower())


if __name__ == "__main__":
    solve()

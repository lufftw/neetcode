# solutions/1203_sort_items_by_groups.py
"""
Problem: Sort Items by Groups Respecting Dependencies
Link: https://leetcode.com/problems/sort-items-by-groups-respecting-dependencies/

There are n items each belonging to zero or one of m groups where group[i] is the
group that the i-th item belongs to and it's equal to -1 if the i-th item belongs
to no group. The items and the groups are zero indexed.

You are given beforeItems[i] which is a list of all the items that must come before
the i-th item in the sorted array (to the left of the i-th item).

Return any sorted array of the items such that:
- The items that belong to the same group are next to each other in the sorted array.
- For each pair (j, i) in beforeItems[i], item j appears before item i.

If there is no solution return an empty array.

Example 1:
    Input: n = 8, m = 2, group = [-1,-1,1,0,0,1,0,-1],
           beforeItems = [[],[6],[5],[6],[3,6],[],[],[]]
    Output: [6,3,4,1,5,2,0,7]

Example 2:
    Input: n = 8, m = 2, group = [-1,-1,1,0,0,1,0,-1],
           beforeItems = [[],[6],[5],[6],[3],[],[4],[]]
    Output: []
    Explanation: Item 4 must be before item 6, but item 6 must be before item 4.

Constraints:
- 1 <= m <= n <= 3 * 10^4
- group.length == beforeItems.length == n
- -1 <= group[i] <= m - 1
- 0 <= beforeItems[i].length <= n - 1
- 0 <= beforeItems[i][j] <= n - 1
- i != beforeItems[i][j]
- beforeItems[i] does not contain duplicates elements.

Topics: Depth-First Search, Breadth-First Search, Graph, Topological Sort
"""
from typing import List, Set
from collections import deque
from _runner import get_solver


# ============================================
# JUDGE_FUNC - Required for generator support
# ============================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate Sort Items by Groups solution."""
    import json

    lines = input_data.strip().split('\n')
    n = int(lines[0])
    m = int(lines[1])
    group = json.loads(lines[2])
    before_items = json.loads(lines[3])

    # Parse actual result
    if isinstance(actual, str):
        actual = json.loads(actual)

    # Check if no valid solution exists
    valid_exists = _has_valid_solution(n, m, group, before_items)

    if not valid_exists:
        return actual == []

    if len(actual) != n:
        return False

    # Check all items present
    if set(actual) != set(range(n)):
        return False

    # Assign unique group IDs to ungrouped items
    group = group.copy()
    group_id = m
    for i in range(n):
        if group[i] == -1:
            group[i] = group_id
            group_id += 1

    # Verify group contiguity
    position = {item: i for i, item in enumerate(actual)}
    group_ranges = {}
    for item in actual:
        g = group[item]
        pos = position[item]
        if g not in group_ranges:
            group_ranges[g] = [pos, pos]
        else:
            group_ranges[g][0] = min(group_ranges[g][0], pos)
            group_ranges[g][1] = max(group_ranges[g][1], pos)

    # Check no gaps in group ranges
    for g, (start, end) in group_ranges.items():
        for pos in range(start, end + 1):
            if group[actual[pos]] != g:
                return False

    # Verify before constraints
    for item in range(n):
        for before in before_items[item]:
            if position[before] >= position[item]:
                return False

    return True


def _has_valid_solution(n: int, m: int, group: List[int], before_items: List[List[int]]) -> bool:
    """Check if a valid solution exists using reference implementation."""
    result = _sort_items(n, m, group.copy(), before_items)
    return len(result) > 0


def _sort_items(n: int, m: int, group: List[int], before_items: List[List[int]]) -> List[int]:
    """Reference solution for validation."""
    # Assign unique group IDs to ungrouped items
    group_id = m
    for i in range(n):
        if group[i] == -1:
            group[i] = group_id
            group_id += 1

    num_groups = group_id

    # Build graphs
    group_graph: List[Set[int]] = [set() for _ in range(num_groups)]
    group_in_degree: List[int] = [0] * num_groups

    item_graph: List[List[int]] = [[] for _ in range(n)]

    for item in range(n):
        for before in before_items[item]:
            item_graph[before].append(item)

            if group[before] != group[item]:
                if group[item] not in group_graph[group[before]]:
                    group_graph[group[before]].add(group[item])
                    group_in_degree[group[item]] += 1

    def topo_sort(nodes: List[int], graph, in_degree: List[int]) -> List[int]:
        in_deg = {node: in_degree[node] for node in nodes}
        queue = deque([node for node in nodes if in_deg[node] == 0])
        result = []

        while queue:
            node = queue.popleft()
            result.append(node)
            neighbors = graph[node] if isinstance(graph[node], list) else list(graph[node])
            for neighbor in neighbors:
                if neighbor in in_deg:
                    in_deg[neighbor] -= 1
                    if in_deg[neighbor] == 0:
                        queue.append(neighbor)

        return result if len(result) == len(nodes) else []

    # Sort groups
    group_order = topo_sort(list(range(num_groups)), group_graph, group_in_degree)
    if not group_order:
        return []

    # Group items
    group_items: List[List[int]] = [[] for _ in range(num_groups)]
    for item in range(n):
        group_items[group[item]].append(item)

    # Sort items within groups and build result
    result: List[int] = []
    for g in group_order:
        items = group_items[g]
        if not items:
            continue

        # Compute within-group in-degrees
        items_set = set(items)
        local_in_degree = [0] * n
        for item in items:
            for before in before_items[item]:
                if before in items_set:
                    local_in_degree[item] += 1

        sorted_items = topo_sort(items, item_graph, local_in_degree)
        if len(sorted_items) != len(items):
            return []
        result.extend(sorted_items)

    return result


JUDGE_FUNC = judge


# ============================================
# SOLUTIONS metadata
# ============================================
SOLUTIONS = {
    "default": {
        "class": "SolutionTwoLevel",
        "method": "sortItems",
        "complexity": "O(V+E) time, O(V+E) space",
        "description": "Two-level topological sort",
        "api_kernels": ["TopologicalSort"],
        "patterns": ["topological_sort_two_level"],
    },
}


# ============================================
# Solution: Two-Level Topological Sort
# Time: O(V + E), Space: O(V + E)
#   - First sort groups topologically
#   - Then sort items within each group
# ============================================
class SolutionTwoLevel:
    def sortItems(self, n: int, m: int, group: List[int], beforeItems: List[List[int]]) -> List[int]:
        # Assign unique group IDs to ungrouped items (-1)
        group_id = m
        for i in range(n):
            if group[i] == -1:
                group[i] = group_id
                group_id += 1

        num_groups = group_id

        # Build graphs for groups and items
        group_graph: List[Set[int]] = [set() for _ in range(num_groups)]
        group_in_degree: List[int] = [0] * num_groups

        item_graph: List[List[int]] = [[] for _ in range(n)]
        item_in_degree: List[int] = [0] * n

        for item in range(n):
            for before in beforeItems[item]:
                # Item dependency
                item_graph[before].append(item)
                item_in_degree[item] += 1

                # Group dependency (if different groups)
                if group[before] != group[item]:
                    if group[item] not in group_graph[group[before]]:
                        group_graph[group[before]].add(group[item])
                        group_in_degree[group[item]] += 1

        def topo_sort(nodes: List[int], graph, in_degree: List[int]) -> List[int]:
            """Generic topological sort using Kahn's algorithm."""
            # Create local copy of in-degrees for the subset of nodes
            in_deg = {node: in_degree[node] for node in nodes}
            queue: deque[int] = deque([node for node in nodes if in_deg[node] == 0])
            result: List[int] = []

            while queue:
                node = queue.popleft()
                result.append(node)

                neighbors = graph[node] if isinstance(graph[node], list) else list(graph[node])
                for neighbor in neighbors:
                    if neighbor in in_deg:
                        in_deg[neighbor] -= 1
                        if in_deg[neighbor] == 0:
                            queue.append(neighbor)

            return result if len(result) == len(nodes) else []

        # Sort groups topologically
        group_order = topo_sort(list(range(num_groups)), group_graph, group_in_degree)
        if not group_order:
            return []

        # Group items by their group
        group_items: List[List[int]] = [[] for _ in range(num_groups)]
        for item in range(n):
            group_items[group[item]].append(item)

        # Sort items within each group and build result
        result: List[int] = []
        for g in group_order:
            items = group_items[g]
            if not items:
                continue

            # Compute within-group in-degrees (ignore cross-group dependencies)
            items_set = set(items)
            local_in_degree: List[int] = [0] * n
            for item in items:
                for before in beforeItems[item]:
                    if before in items_set:
                        local_in_degree[item] += 1

            # Topological sort items in this group
            sorted_items = topo_sort(items, item_graph, local_in_degree)
            if len(sorted_items) != len(items):
                return []

            result.extend(sorted_items)

        return result


def solve():
    """
    Input format (canonical JSON):
    Line 1: Integer n (number of items)
    Line 2: Integer m (number of groups)
    Line 3: Array group
    Line 4: 2D array beforeItems

    Output format:
    Array of item indices in valid order, or empty array
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    n = int(lines[0])
    m = int(lines[1])
    group = json.loads(lines[2])
    before_items = json.loads(lines[3])

    solver = get_solver(SOLUTIONS)
    result = solver.sortItems(n, m, group, before_items)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()

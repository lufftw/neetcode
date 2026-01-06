## Universal Templates

### Template 1: Subset Enumeration

```python
def enumerate_subsets(nums):
    """Generate all 2^n subsets using bitmask."""
    n = len(nums)
    result = []

    for mask in range(1 << n):
        # Decode bitmask to subset
        subset = [nums[i] for i in range(n) if mask & (1 << i)]
        result.append(subset)

    return result
```

**Use for**: LC 78, 90, 784, 1286

---

### Template 2: BFS + Bitmask State

```python
from collections import deque

def bfs_bitmask(graph):
    """BFS with (node, visited_mask) state."""
    n = len(graph)
    full_mask = (1 << n) - 1

    # Initialize: start from every node
    queue = deque()
    visited = set()

    for i in range(n):
        state = (i, 1 << i)
        queue.append((i, 1 << i, 0))  # (node, mask, dist)
        visited.add(state)

    while queue:
        node, mask, dist = queue.popleft()

        for neighbor in graph[node]:
            new_mask = mask | (1 << neighbor)

            # Early termination
            if new_mask == full_mask:
                return dist + 1

            state = (neighbor, new_mask)
            if state not in visited:
                visited.add(state)
                queue.append((neighbor, new_mask, dist + 1))

    return -1
```

**Use for**: LC 847, 943, 1494

---

### Template 3: Set Cover DP

```python
def set_cover_dp(required_mask, item_masks):
    """
    Find minimum items to cover all requirements.

    Args:
        required_mask: Target mask to achieve
        item_masks: List of (item_id, mask) tuples

    Returns:
        List of item indices forming minimum cover
    """
    # dp[mask] = smallest set of items to achieve mask
    dp = {0: []}

    for item_id, item_mask in item_masks:
        # Iterate over copy of current states
        for mask, items in list(dp.items()):
            new_mask = mask | item_mask

            # Only update if strictly better
            if new_mask not in dp or len(dp[new_mask]) > len(items) + 1:
                dp[new_mask] = items + [item_id]

    return dp.get(required_mask, [])
```

**Use for**: LC 1125, 1723, 1986

---

### Template 4: TSP-style DP

```python
def tsp_dp(dist):
    """
    Classic TSP: minimum cost to visit all nodes.

    Args:
        dist: n×n distance matrix

    Returns:
        Minimum cost to visit all nodes starting from node 0
    """
    n = len(dist)
    INF = float('inf')

    # dp[mask][last] = min cost to visit nodes in mask, ending at last
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # Start at node 0

    for mask in range(1, 1 << n):
        for last in range(n):
            if not (mask & (1 << last)):
                continue
            if dp[mask][last] == INF:
                continue

            for next_node in range(n):
                if mask & (1 << next_node):
                    continue

                new_mask = mask | (1 << next_node)
                dp[new_mask][next_node] = min(
                    dp[new_mask][next_node],
                    dp[mask][last] + dist[last][next_node]
                )

    full_mask = (1 << n) - 1
    return min(dp[full_mask])
```

**Use for**: TSP variants, Hamiltonian path problems

---

## Bit Manipulation Utilities

```python
# Essential bit operations

def set_bit(mask, i):
    """Add element i to set."""
    return mask | (1 << i)

def clear_bit(mask, i):
    """Remove element i from set."""
    return mask & ~(1 << i)

def has_bit(mask, i):
    """Check if element i is in set."""
    return (mask >> i) & 1

def toggle_bit(mask, i):
    """Toggle element i membership."""
    return mask ^ (1 << i)

def count_bits(mask):
    """Count elements in set."""
    return bin(mask).count('1')

def full_mask(n):
    """Create mask with all n bits set."""
    return (1 << n) - 1

def iterate_bits(mask, n):
    """Yield indices of set bits."""
    for i in range(n):
        if mask & (1 << i):
            yield i

def submasks(mask):
    """Iterate all submasks of mask (excluding 0)."""
    sub = mask
    while sub:
        yield sub
        sub = (sub - 1) & mask
```

---

## Complexity Reference

| Pattern | Time | Space | Practical n |
|---------|------|-------|-------------|
| Subset Enum | O(n × 2^n) | O(n × 2^n) | n ≤ 15 |
| BFS + Bitmask | O(n × 2^n) | O(n × 2^n) | n ≤ 12 |
| Set Cover DP | O(m × 2^m) | O(2^m) | m ≤ 16 |
| TSP DP | O(n^2 × 2^n) | O(n × 2^n) | n ≤ 18 |

## Variant: Two City Scheduling (LeetCode 1029)

> **Problem**: Send n people to city A and n to city B, minimizing total cost.
> **Invariant**: Sort by cost difference (A cost - B cost); send first half to A.
> **Delta from Base**: Sort by "relative advantage" metric.

### Implementation

```python
class Solution:
    """
    Greedy by Cost Difference: Sort by savings from choosing A over B.

    Key Insight:
    - cost[i] = [cost_A, cost_B]
    - diff = cost_A - cost_B measures "how much cheaper A is"
    - Negative diff: A is cheaper, send to A
    - Positive diff: B is cheaper, send to B
    - Sort by diff, send first n (lowest diff) to A, rest to B

    Greedy Choice: Maximize total savings by prioritizing largest
    cost differences.

    Time: O(n log n) | Space: O(1) excluding sort
    """
    def twoCitySchedCost(self, costs: List[List[int]]) -> int:
        # Sort by (cost_A - cost_B)
        # People with most "savings from A" come first
        costs.sort(key=lambda x: x[0] - x[1])

        total_cost = 0
        n = len(costs) // 2

        # First n people go to city A (they benefit most from A)
        for i in range(n):
            total_cost += costs[i][0]

        # Remaining n people go to city B
        for i in range(n, 2 * n):
            total_cost += costs[i][1]

        return total_cost
```

### Why Sorting by Difference Works

Consider swapping assignments for two people:
- Person X at A, Person Y at B → cost = X_A + Y_B
- Swap: X at B, Y at A → cost = X_B + Y_A
- Difference: (X_A + Y_B) - (X_B + Y_A) = (X_A - X_B) - (Y_A - Y_B)

If X's diff < Y's diff, keeping X at A is optimal.

### Trace Example

```
costs: [[10,20], [30,200], [400,50], [30,20]]

Calculate diffs:
  [10,20]  → diff = -10 (A much cheaper)
  [30,200] → diff = -170 (A much cheaper)
  [400,50] → diff = 350 (B much cheaper)
  [30,20]  → diff = 10 (B slightly cheaper)

Sort by diff: [[30,200], [10,20], [30,20], [400,50]]
              diff: -170,   -10,    10,     350

First n=2 to A: 30 + 10 = 40
Last n=2 to B: 20 + 50 = 70
Total: 110
```

### Generalization: Relative Advantage Sorting

This pattern applies when:
1. Each item has multiple options with different costs
2. Must distribute items across options
3. Sort by "relative advantage" of one option over another

The "advantage" metric captures opportunity cost.



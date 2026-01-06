## Variant: Gas Station (LeetCode 134)

> **Problem**: Find the starting gas station index to complete a circular route, or -1 if impossible.
> **Invariant**: Track running surplus; reset start when deficit occurs.
> **Delta from Base**: Prefix sum with reset + total feasibility check.

### Implementation

```python
class Solution:
    """
    Greedy Reset: Track local surplus, reset start on deficit.

    Key Insights:
    1. If total_gas >= total_cost, a valid start exists (pigeonhole principle)
    2. If we can't reach station j from station i, we also can't reach j
       from any station between i and j (they have less accumulated gas)
    3. When surplus goes negative, the next station is a candidate start

    Invariant: current_surplus tracks gas balance since last reset point.

    Time: O(n) | Space: O(1)
    """
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        total_surplus = 0      # Total gas - total cost (feasibility check)
        current_surplus = 0    # Surplus since candidate start
        candidate_start = 0    # Current best starting station

        for station in range(len(gas)):
            net_gain = gas[station] - cost[station]
            total_surplus += net_gain
            current_surplus += net_gain

            # Can't reach next station from candidate_start
            # Reset: next station becomes new candidate
            if current_surplus < 0:
                candidate_start = station + 1
                current_surplus = 0

        # If total is non-negative, candidate_start is valid
        return candidate_start if total_surplus >= 0 else -1
```

### Why Reset Works

**Key Lemma**: If we can't complete [i, j] (surplus goes negative at j), then no station in [i, j] can be a valid start.

Proof: Any station k in [i, j] would have even less accumulated gas when reaching j, since it misses the non-negative contributions from [i, k-1].

**Greedy Choice**: When we fail, skip all stations in the failing segment and try the next one.

### Trace Example

```
gas:  [1, 2, 3, 4, 5]
cost: [3, 4, 5, 1, 2]
net:  [-2,-2,-2, 3, 3]   (gas - cost at each station)

station=0: current=-2 < 0 → reset, candidate=1
station=1: current=-2 < 0 → reset, candidate=2
station=2: current=-2 < 0 → reset, candidate=3
station=3: current=3
station=4: current=6

total_surplus = -2-2-2+3+3 = 0 >= 0
Result: candidate_start = 3
```

### Why Total Check is Sufficient

If `total_surplus >= 0`, there must exist a valid start:
- Total gas >= total cost
- The "lowest point" in the prefix sum defines the optimal start
- Starting after the lowest point ensures we never dip below zero



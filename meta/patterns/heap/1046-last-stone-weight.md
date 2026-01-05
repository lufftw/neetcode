## Last Stone Weight (LeetCode 1046)

> **Problem**: Smash two heaviest stones repeatedly, return weight of last stone (or 0).
> **Pattern**: Greedy simulation with max-heap
> **Variant**: Simple heap operations for repeated selection

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "repeatedly pick largest/smallest" | → Max/min-heap |
| "simulation" | → Heap for efficient selection |
| "until one/none left" | → Process until heap size ≤ 1 |

### Implementation

```python
# Pattern: heap_greedy_simulation
# See: docs/patterns/heap/templates.md Section 7

import heapq

class SolutionHeap:
    def lastStoneWeight(self, stones: List[int]) -> int:
        """
        Simulate stone smashing using max-heap.

        Game Rules:
        1. Pick two heaviest stones x, y (x <= y)
        2. If x == y: both destroyed
        3. If x != y: stone of weight y - x remains

        Why max-heap?
        - Need repeated access to two largest elements
        - Python heapq is min-heap, so negate values
        - O(log n) per operation vs O(n) for linear search
        """
        # Convert to max-heap (negate all values)
        max_heap = [-stone for stone in stones]
        heapq.heapify(max_heap)  # O(n) heapify

        # Simulate until 0 or 1 stone remains
        while len(max_heap) > 1:
            # Pop two largest (remember to negate)
            largest = -heapq.heappop(max_heap)
            second = -heapq.heappop(max_heap)

            # If different weights, push the difference
            if largest != second:
                heapq.heappush(max_heap, -(largest - second))

        # Return last stone weight (or 0 if no stones left)
        return -max_heap[0] if max_heap else 0
```

### Trace Example

```
Input: stones = [2, 7, 4, 1, 8, 1]

Initial max-heap: [-8, -7, -4, -1, -2, -1]
Displayed as max-heap: [8, 7, 4, 1, 2, 1]

Round 1: Pop 8, 7; difference = 1
  heap: [4, 2, 1, 1, 1]

Round 2: Pop 4, 2; difference = 2
  heap: [2, 1, 1, 1]

Round 3: Pop 2, 1; difference = 1
  heap: [1, 1, 1]

Round 4: Pop 1, 1; equal, both destroyed
  heap: [1]

Result: 1
```

### Complexity Analysis

| Aspect | Complexity |
|--------|------------|
| Time | O(n log n) |
| Space | O(n) for heap |

**Time breakdown**:
- Heapify: O(n)
- Each smash: 2 pops + 0-1 push = O(log n)
- Total smashes: at most n-1 (each reduces count by at least 1)
- Total: O(n) + O(n log n) = O(n log n)

### Related Problems

| Problem | Variation |
|---------|-----------|
| LC 1167: Min Cost to Connect Sticks | Sum instead of difference |
| LC 973: K Closest Points | Top-k by distance |
| LC 703: Kth Largest Element in Stream | Maintain kth largest online |



## Pattern Comparison Table

| Pattern | Search Space | Predicate | Loop Condition | Result |
|---------|-------------|-----------|----------------|--------|
| Exact Match | Array indices | `arr[mid] == target` | `left <= right` | Index or -1 |
| Lower Bound | Array indices | `arr[mid] >= target` | `left < right` | First >= |
| Upper Bound | Array indices | `arr[mid] > target` | `left < right` | First > |
| Rotated Search | Array indices | Sorted-half check | `left <= right` | Index or -1 |
| Answer Space | Value range | Feasibility check | `left < right` | Min feasible |
| Peak Finding | Array indices | Slope comparison | `left < right` | Peak index |



## Pattern Comparison Table

| Pattern | Pointer Init | Movement | Termination | Time | Space | Key Use Case |
|---------|--------------|----------|-------------|------|-------|--------------|
| Opposite | `0, n-1` | Toward center | `left >= right` | O(n) | O(1) | Sorted array pairs |
| Same-Direction | `0, 0` | Both forward | `read >= n` | O(n) | O(1) | In-place modification |
| Fast–Slow | `head, head` | Slow 1×, Fast 2× | Meet or null | O(n) | O(1) | Cycle detection |
| Partitioning | `0, 0, n-1` | By element value | `mid > high` | O(n) | O(1) | Dutch flag, sorting |
| Dedup Enum | `i, i+1, n-1` | Nested + opposite | All `i` processed | O(n²) | O(1) | Multi-sum problems |
| Merge | `0, 0` | Advance smaller | Both exhausted | O(m+n) | O(1) | Merging sorted sequences |


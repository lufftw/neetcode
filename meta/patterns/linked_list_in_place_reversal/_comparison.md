## Comparison Table

| Problem | Scope | Key Challenge | Critical Step | Complexity |
|---------|-------|---------------|---------------|------------|
| **206. Reverse Linked List** | Entire list | Basic three-pointer reversal | Save `curr.next` before overwriting | O(N), O(1) |
| **92. Reverse Linked List II** | Segment [left, right] | Find boundaries, reconnect after | Track `before_segment` and reconnect both ends | O(N), O(1) |
| **25. Reverse Nodes in k-Group** | Every k nodes | Check availability, group management | Initialize `prev` to `group_next` for auto-connection | O(N), O(1) |

### What Changes Between Variants

| Aspect | 206 (Full) | 92 (Segment) | 25 (K-Group) |
|--------|------------|--------------|--------------|
| **Pre-processing** | None | Navigate to before_segment | Find kth_node, check availability |
| **Nodes reversed** | All N | right - left + 1 | k per group |
| **Prev initialization** | None | None | group_next (trick) |
| **Post-processing** | None | Reconnect both ends | Move group_prev to new tail |
| **Dummy node needed** | Optional | Required (left=1) | Required (first group) |
| **Loop condition** | `while curr` | Fixed count | `while kth_node exists` |

### Memory Model

```
Full Reversal (206):
Before: None  1 -> 2 -> 3 -> 4 -> 5 -> None
After:  None <- 1 <- 2 <- 3 <- 4 <- 5

Segment Reversal (92) [left=2, right=4]:
Before: 1 -> 2 -> 3 -> 4 -> 5
After:  1 -> 4 -> 3 -> 2 -> 5
        ^    ^---------^    ^
     anchor  reversed    reconnect

K-Group Reversal (25) [k=2]:
Before: 1 -> 2 -> 3 -> 4 -> 5
After:  2 -> 1 -> 4 -> 3 -> 5
        ^----^    ^----^    ^
        group1    group2   leftover
```



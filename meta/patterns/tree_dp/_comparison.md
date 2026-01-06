## Pattern Comparison

| Problem | States Per Node | Return Value | Global Tracking |
|---------|-----------------|--------------|-----------------|
| **House Robber III** | 2 (include, exclude) | Both states | No |
| **Max Path Sum** | 1 (contribution) | Max branch contribution | Yes (max path) |
| **Binary Tree Cameras** | 3 (coverage states) | Coverage state | Yes (camera count) |

## State Design Summary

| Pattern Type | When to Use | State Example |
|--------------|-------------|---------------|
| **Include/Exclude** | Binary choice per node | `(with_node, without_node)` |
| **Path Contribution** | Optimize paths | `max_contribution_upward` |
| **Multi-State** | Complex constraints | `(not_covered, covered, has_camera)` |

## Complexity Comparison

| Problem | Time | Space | Key Operation |
|---------|------|-------|---------------|
| House Robber III | O(n) | O(h) | Max of combinations |
| Max Path Sum | O(n) | O(h) | Sum with clamping |
| Binary Tree Cameras | O(n) | O(h) | State transition |

## Return Value vs Global State

| Problem | Return to Parent | Global Update |
|---------|------------------|---------------|
| House Robber | Both states for parent's choice | None |
| Max Path | Single branch (path constraint) | Max of all paths |
| Cameras | Coverage state | Camera count |

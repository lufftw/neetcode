---

## Problem Mapping

### By Kernel Type

| Kernel | Problems | Key Technique |
|--------|----------|---------------|
| **Reachability** | LC 55, 45, 1024 | Track farthest reachable, level boundaries |
| **Prefix Min/Reset** | LC 134 | Running balance, reset on deficit |
| **Sort + Match** | LC 455, 1029, 870, 2285 | Sort, two-pointer matching |
| **Two-Pass** | LC 135, 42 (variant) | Forward + backward scan |

### By Difficulty Progression

| Level | Problem | Why Here |
|-------|---------|----------|
| **Beginner** | LC 455 (Assign Cookies) | Pure sort + match |
| **Beginner** | LC 55 (Jump Game) | Single invariant tracking |
| **Intermediate** | LC 45 (Jump Game II) | Two variables, level counting |
| **Intermediate** | LC 1029 (Two City) | Sort by derived metric |
| **Intermediate** | LC 134 (Gas Station) | Reset logic, total check |
| **Advanced** | LC 135 (Candy) | Two-pass with max merge |

### Related Non-Core Greedy

These problems use greedy but belong to other categories:

| Problem | Category | Why Not Core |
|---------|----------|--------------|
| LC 56 (Merge Intervals) | Interval Greedy | Sort by start, merge logic |
| LC 435 (Non-overlapping Intervals) | Interval Greedy | Sort by end, conflict counting |
| LC 253 (Meeting Rooms II) | Heap Greedy | Dynamic room assignment |
| LC 621 (Task Scheduler) | Heap Greedy | Priority-based selection |



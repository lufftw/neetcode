## Task Scheduler (LeetCode 621)

> **Problem**: Schedule tasks with cooldown constraint n between same tasks. Return minimum time units.
> **Pattern**: Greedy scheduling with max-heap
> **Variant**: Heap + greedy for optimal ordering

### Pattern Recognition

| Signal | Indicator |
|--------|-----------|
| "minimum time to complete" | → Greedy scheduling |
| "cooldown period" | → Track availability |
| "most frequent first" | → Max-heap by count |

### The Greedy Insight

```
Tasks: A A A B B B, n = 2

Greedy: Always schedule most frequent available task

Optimal schedule:
A B _ A B _ A B
1 2 3 4 5 6 7 8

Total time = 8 units

Why most frequent first?
- Reduces idle time by distributing high-frequency tasks
- Idle slots appear when no task is available (all in cooldown)
```

### Implementation

```python
# Pattern: heap_task_scheduler
# See: docs/patterns/heap/templates.md Section 6

import heapq
from collections import Counter, deque

class SolutionHeap:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        """
        Schedule tasks with cooldown using max-heap.

        Strategy:
        1. Greedily pick most frequent available task
        2. Track cooldown using a queue (task becomes available at time t)
        3. If no task available, idle (time still advances)

        Why max-heap?
        - We want to process high-frequency tasks first
        - This minimizes idle time at the end
        - Max-heap gives O(log k) access to most frequent
        """
        # Count task frequencies
        task_counts = Counter(tasks)

        # Max-heap of remaining counts (negate for max-heap)
        max_heap = [-count for count in task_counts.values()]
        heapq.heapify(max_heap)

        # Queue of (available_time, remaining_count) for tasks in cooldown
        cooldown_queue: deque[tuple[int, int]] = deque()

        time = 0

        while max_heap or cooldown_queue:
            time += 1

            # Check if any task exits cooldown
            if cooldown_queue and cooldown_queue[0][0] == time:
                available_time, remaining = cooldown_queue.popleft()
                heapq.heappush(max_heap, -remaining)

            if max_heap:
                # Execute most frequent available task
                count = -heapq.heappop(max_heap)
                count -= 1

                if count > 0:
                    # Task has more instances, put in cooldown
                    cooldown_queue.append((time + n + 1, count))
            # else: idle (no task available)

        return time
```

### Trace Example

```
Input: tasks = ['A','A','A','B','B','B'], n = 2

Initial:
  Counts: A=3, B=3
  max_heap: [-3, -3]
  cooldown_queue: []

Time 1: Pop A (count=3→2), cooldown until time=4
  heap: [-3], queue: [(4, 2)]

Time 2: Pop B (count=3→2), cooldown until time=5
  heap: [], queue: [(4, 2), (5, 2)]

Time 3: Idle (heap empty, queue not ready)
  heap: [], queue: [(4, 2), (5, 2)]

Time 4: A exits cooldown, pop A (count=2→1)
  heap: [-2], queue: [(5, 2), (7, 1)]
  Actually: A exits, push to heap, then pop

... continue ...

Final time = 8
```

### Alternative: Math Formula

```python
class SolutionMath:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        """
        Mathematical approach based on most frequent task.

        Observation:
        - Most frequent task determines the "frame"
        - Frame: chunks of size (n+1) with one instance of max-freq task

        Formula:
        - frames = (max_freq - 1)
        - frame_size = n + 1
        - base_time = frames * frame_size
        - Add tasks with max_freq (they fill the last partial frame)

        Edge case:
        - If total tasks > formula result, no idle needed
        """
        task_counts = Counter(tasks)
        max_freq = max(task_counts.values())
        max_freq_count = sum(1 for count in task_counts.values() if count == max_freq)

        # Formula: (max_freq - 1) frames × (n + 1) slots + max_freq_count final slots
        formula_time = (max_freq - 1) * (n + 1) + max_freq_count

        # Actual time is max of formula and total tasks
        return max(formula_time, len(tasks))
```

### Visual Explanation of Formula

```
tasks = [A,A,A,A,B,B,B,C,C], n = 2, max_freq = 4 (task A)

Formula visualization:
Frame 1: A _ _
Frame 2: A _ _
Frame 3: A _ _
Frame 4: A

Slots per frame = n + 1 = 3
Frames (excluding last) = max_freq - 1 = 3
Base slots = 3 × 3 = 9
Plus final A = 1

Total slots = 10 (minimum, may need more if many tasks)
```

### Complexity Comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Max-heap | O(n × m) | O(k) | n=cooldown, m=total tasks, k=unique |
| Math formula | O(n) | O(k) | Count frequencies only |

### Related Problems

| Problem | Variation |
|---------|-----------|
| LC 767: Reorganize String | No same adjacent chars |
| LC 358: Rearrange String k Distance | k-distance apart |
| LC 1834: Single-Threaded CPU | Task scheduling with priority |



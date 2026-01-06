# Line Sweep Pattern

## API Kernel: `LineSweep`

> **Core Mechanism**: Transform intervals/rectangles into discrete events (start/end points), sort by position, and sweep through maintaining state with a data structure.

## Why Line Sweep?

Line sweep solves problems where:
- You have multiple overlapping intervals, rectangles, or ranges
- You need to track aggregate state (count, max height, capacity) at any point
- Processing all pairs would be O(n²) but events can be processed in O(n log n)

## Core Insight

**Every interval creates two events**: a start event and an end event. By processing events in sorted order, we convert a 2D overlap problem into a 1D scan.

```
Intervals:  [1,4] [2,5] [3,6]

Events:     1:+1  2:+1  3:+1  4:-1  5:-1  6:-1
            ↓     ↓     ↓     ↓     ↓     ↓
Count:      1     2     3     2     1     0
Max = 3 (at position 3)
```

## Universal Template Structure

```python
def line_sweep(intervals):
    # Step 1: Create events
    events = []
    for start, end in intervals:
        events.append((start, +1))  # Start event
        events.append((end, -1))    # End event

    # Step 2: Sort events
    # Tie-breaking rule depends on problem:
    # - For counting overlap: end before start at same position
    # - For skyline: start before end at same position
    events.sort()

    # Step 3: Sweep and maintain state
    current_state = 0
    result = initial_value

    for position, delta in events:
        current_state += delta
        result = update(result, current_state)

    return result
```

## Event Encoding Strategies

| Problem Type | Start Event | End Event | Sort Key | Tie-breaking |
|-------------|-------------|-----------|----------|--------------|
| **Count Overlap** | (pos, +1) | (pos, -1) | position | end before start |
| **Skyline** | (pos, -height) | (pos, height) | position | start before end |
| **Capacity Check** | (pos, +load) | (pos, -load) | position | depends on semantics |

## State Management Data Structures

| Complexity | Data Structure | Use Case |
|------------|----------------|----------|
| Simple counting | Integer counter | Meeting rooms, car pooling |
| Max tracking | Heap or Sorted Container | Skyline problem |
| Complex queries | Segment Tree | Range-based queries |

## Pattern Variants

1. **Event Counting** (Base): Count active intervals at each point
2. **Capacity Tracking**: Track cumulative load/capacity
3. **Height Tracking**: Maintain max height with multiset/heap
4. **Difference Array**: Offline version using prefix sums

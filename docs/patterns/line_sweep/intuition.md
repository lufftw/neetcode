# Line Sweep - Intuition Guide

## The Mental Model: A Security Guard's Timeline

Imagine you're a security guard monitoring a building entrance. Throughout the day, people enter and leave. Your job is to count how many people are inside at any moment.

**The naive approach**: Check every second of the day. But that's 86,400 checks!

**The smart approach**: Only check when something happens (someone enters or leaves).

```
Timeline:
  9:00 - Alice enters     → 1 person inside
  9:30 - Bob enters       → 2 people
  10:00 - Alice leaves    → 1 person
  10:15 - Carol enters    → 2 people
  11:00 - Bob leaves      → 1 person
  11:30 - Carol leaves    → 0 people

Max at any point: 2 people
```

This is **line sweep**: convert continuous time into discrete events, then process in order.

## Visual: Scanning Left to Right

```
Buildings (Skyline Problem):
                    ___
      ___          |   |
     |   |___      |   |___
     |       |     |       |
   __|       |_____|       |___
     ^   ^   ^     ^   ^   ^
     |   |   |     |   |   |
  Events (vertical lines where something changes)
```

As we sweep a vertical line from left to right:
1. Building starts → add its height to active set
2. Building ends → remove its height from active set
3. Max height changes → record a skyline point

## The Three Key Questions

When you see an interval problem, ask:

### 1. What creates events?
- Meeting starts/ends → position, ±1
- Passenger pickup/dropoff → position, ±count
- Building start/end → position, add/remove height

### 2. What order to process?
- Sort by position
- At same position, what comes first?
  - Ends before starts (reuse resources)
  - Starts before ends (see new max first)

### 3. What state to maintain?
- Simple count → integer
- Capacity check → integer with threshold
- Max height → heap or sorted container

## Pattern 1: Event Counting

**Scenario**: Conference room scheduling

```
Meetings: [[0,30], [5,10], [15,20]]

Step 1: Create events
  (0, +1), (30, -1)  ← meeting 1
  (5, +1), (10, -1)  ← meeting 2
  (15, +1), (20, -1) ← meeting 3

Step 2: Sort (by time, ends before starts)
  (0,+1), (5,+1), (10,-1), (15,+1), (20,-1), (30,-1)

Step 3: Sweep and count
  0: 0+1=1  (max=1)
  5: 1+1=2  (max=2)  ← need 2 rooms!
  10: 2-1=1
  15: 1+1=2 (max=2)
  20: 2-1=1
  30: 1-1=0

Answer: 2 rooms
```

## Pattern 2: Capacity Tracking

**Scenario**: Carpooling with limited seats

```
trips: [[2,1,5], [3,3,7]], capacity = 4

Events:
  (1, +2), (5, -2)  ← 2 passengers from 1 to 5
  (3, +3), (7, -3)  ← 3 passengers from 3 to 7

Sorted: (1,+2), (3,+3), (5,-2), (7,-3)

Sweep:
  1: 0+2=2 ≤ 4 ✓
  3: 2+3=5 > 4 ✗  ← Over capacity!

Answer: False
```

## Pattern 3: Height Tracking

**Scenario**: City skyline silhouette

```
Buildings: [[2,9,10], [3,7,15], [5,12,12]]
           (left, right, height)

Events:
  x=2: add 10    x=3: add 15    x=5: add 12
  x=7: del 15    x=9: del 10    x=12: del 12

Active heights at each x:
  x=2: {10}         → max=10, output [2,10]
  x=3: {10,15}      → max=15, output [3,15]
  x=5: {10,15,12}   → max=15, no change
  x=7: {10,12}      → max=12, output [7,12]
  x=9: {12}         → max=12, no change
  x=12: {}          → max=0, output [12,0]

Skyline: [[2,10], [3,15], [7,12], [12,0]]
```

## The Tie-Breaking Intuition

### For Meeting Rooms (ends before starts)
At time 10, one meeting ends and another starts. Can we reuse the room?

```
Wrong order (start before end):
  10: start → need 3 rooms
  10: end → only 2 rooms now
  Counted max = 3 (too many!)

Right order (end before start):
  10: end → 2 rooms → 1 room
  10: start → 1 room → 2 rooms
  Counted max = 2 (correct!)
```

### For Skyline (starts before ends)
At position 5, building A starts and building B ends. Which height do we see?

```
Wrong order (end before start):
  5: remove B's height → max drops
  5: add A's height → max increases
  Two outputs at same x!

Right order (start before end):
  5: add A's height → max might increase
  5: remove B's height → max might decrease
  Only one output if max changed
```

## From Intervals to Events: The Transformation

```
Intervals:      Events:
   [1, 4]       (1, +1), (4, -1)
   [2, 5]   →   (2, +1), (5, -1)
   [3, 6]       (3, +1), (6, -1)

Visual:
  1   2   3   4   5   6
  [---+---+---]
      [---+---+---]
          [---+---+---]
  ↑   ↑   ↑   ↑   ↑   ↑
  +1  +1  +1  -1  -1  -1
```

## Common Mistakes and Fixes

### Mistake 1: Wrong interval boundaries
```python
# Half-open [start, end): end event at end
events.append((end, -1))

# Closed [start, end]: end event at end+1
events.append((end + 1, -1))
```

### Mistake 2: Forgetting ground level
```python
# Skyline needs a baseline
heights = SortedList([0])  # Include 0!
```

### Mistake 3: Duplicate outputs
```python
# Check if height actually changed
if not result or result[-1][1] != current_max:
    result.append([x, current_max])
```

## When Line Sweep Clicks

You'll know to use line sweep when:
1. The problem mentions intervals, time ranges, or spatial extents
2. You need to track something "at any point" or "at all times"
3. The naive O(n²) pairwise comparison feels wasteful
4. Sorting by start/end time is a natural first step

## Summary

| Pattern | State | Key Operation | Tie-break |
|---------|-------|---------------|-----------|
| **Event Counting** | Integer | max(count) | end before start |
| **Capacity** | Integer | check threshold | end before start |
| **Height** | Sorted set | max of active | start before end |

The line sweep transforms a 2D overlap problem into a 1D scan by converting intervals into discrete events. Process events in order, maintain state, and you'll find the answer efficiently in O(n log n).

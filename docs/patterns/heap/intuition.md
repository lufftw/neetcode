# Heap / Priority Queue: Intuition Guide

## The Mental Model

Imagine you're a hospital triage nurse. Patients arrive continuously, but you don't treat them in arrival order—you treat the most critical patient first. You need a system that:

1. Quickly identifies the most critical patient (O(1) peek)
2. Efficiently adds new patients (O(log n) insert)
3. Efficiently removes the treated patient and finds the next most critical (O(log n) extract)

This is exactly what a **heap** provides: efficient access to the "extreme" element (min or max) while supporting fast insertions and removals.

---

## Pattern Recognition Signals

### Signal: "Find kth largest/smallest"

**Trigger phrases**: "kth largest", "kth smallest", "kth element"

**Mental model**: You need a "bouncer at a VIP club" that only lets in the top k.

```
Elements: [3, 1, 4, 1, 5, 9, 2, 6]
k = 3

Min-heap of size 3 (the VIP list):
Process 3: heap = [3]          (room for more)
Process 1: heap = [1, 3]       (room for more)
Process 4: heap = [1, 3, 4]    (full)
Process 1: 1 < 1? No, rejected (not VIP enough)
Process 5: 5 > 1? Yes! heap = [3, 4, 5]
Process 9: 9 > 3? Yes! heap = [4, 5, 9]
...

Answer: heap[0] = 3rd largest
```

**Why min-heap for max problem?** The heap root is the "bouncer"—the weakest VIP. Anyone stronger replaces them.

### Signal: "Top k frequent/closest/largest"

**Trigger phrases**: "most frequent", "k closest", "k largest"

**Mental model**: Same as kth element, but return all k elements.

```python
# Pattern: min-heap of size k
for element in elements:
    if len(heap) < k:
        push(element)
    elif element > heap[0]:  # Better than worst VIP
        replace(element)
return heap  # All k elements
```

### Signal: "Streaming median" or "running median"

**Trigger phrases**: "median of stream", "running median", "middle value"

**Mental model**: Split numbers into "small team" and "big team". Team captains (heap roots) are always adjacent to the median.

```
Numbers seen: [1, 5, 2, 8, 3]

After each number:
     lower (max-heap)  |  upper (min-heap)
[1]       [1]          |       []           median = 1
[5]       [1]          |       [5]          median = 3
[2]       [2, 1]       |       [5]          median = 2
[8]       [2, 1]       |       [5, 8]       median = 3.5
[3]       [3, 2, 1]    |       [5, 8]       median = 3

Invariant: All in lower ≤ All in upper
```

### Signal: "Merge k sorted"

**Trigger phrases**: "merge k lists", "k sorted arrays", "external sort"

**Mental model**: You have k lines of people (sorted by height), and you need to merge them into one line while maintaining order.

```
Line 0: Alice(5) → Bob(7) → Carol(9)
Line 1: Dan(4) → Eve(6) → Frank(8)
Line 2: Grace(3) → Henry(10)

Heap of front people: [(Grace, 2), (Dan, 1), (Alice, 0)]

Pop Grace → Push Henry → Heap: [(Dan, 1), (Alice, 0), (Henry, 2)]
Pop Dan → Push Eve → ...

Result: Grace, Dan, Alice, Eve, Bob, Frank, Carol, Henry, ...
```

### Signal: "Minimum resources for scheduling"

**Trigger phrases**: "minimum rooms", "minimum servers", "overlapping intervals"

**Mental model**: Resources become available at certain times. Track when each resource frees up.

```
Meetings: [0,30], [5,10], [15,20]

Timeline:    0    5    10   15   20   30
Meeting 0:   |========================|
Meeting 1:        |-----|
Meeting 2:                  |-----|

Heap of end times (when rooms free):
t=0:  Room 1 takes [0,30], heap = [30]
t=5:  30 > 5, need new room, heap = [10, 30]
t=15: 10 ≤ 15, reuse Room 2!, heap = [20, 30]

Answer: 2 rooms (max heap size)
```

### Signal: "Schedule with cooldown"

**Trigger phrases**: "cooldown period", "same task interval", "CPU scheduling"

**Mental model**: Greedily do the most frequent task that's not on cooldown.

```
Tasks: A A A B B B, n = 2

Time:  1  2  3  4  5  6  7  8
Task:  A  B  _  A  B  _  A  B
       ↑        ↑        ↑
       A done   A ready  A done again

Max-heap by frequency ensures we always pick the most urgent task.
```

---

## Common Pitfalls

### Pitfall 1: Forgetting Python heapq is min-heap only

```python
# WRONG: Trying to use heapq as max-heap directly
max_heap = [3, 1, 4]
heapq.heapify(max_heap)
print(heapq.heappop(max_heap))  # Returns 1, not 4!

# CORRECT: Negate values for max-heap behavior
max_heap = [-3, -1, -4]
heapq.heapify(max_heap)
print(-heapq.heappop(max_heap))  # Returns 4 ✓
```

### Pitfall 2: Using wrong heap type for top-k

```python
# WRONG: Max-heap for k largest
# This keeps k smallest, not k largest!

# CORRECT: Min-heap of size k for k largest
# Root = smallest of k largest = kth largest
```

**Memory trick**: "Min-heap is the bouncer for the VIP section. The bouncer (root) is the weakest VIP."

### Pitfall 3: Off-by-one in kth element

```python
# "kth largest" means:
# - 1st largest = max element
# - 2nd largest = second from top when sorted descending

nums = [3, 2, 1, 5, 6, 4]
# Sorted descending: [6, 5, 4, 3, 2, 1]
#                     1  2  3  4  5  6  (k values)
# 2nd largest = 5 (not 6!)
```

### Pitfall 4: Comparing non-comparable objects

```python
# WRONG: ListNode objects can't be compared
heapq.heappush(heap, (node.val, node))  # Error if vals equal!

# CORRECT: Add unique tie-breaker
heapq.heappush(heap, (node.val, idx, node))  # idx breaks ties
```

### Pitfall 5: Modifying heap elements in place

```python
# WRONG: Changing element value without re-heapifying
heap[2] = new_value  # Heap property violated!

# CORRECT: Remove and re-insert, or rebuild heap
```

---

## Practice Progression

### Level 1: Basic Heap Operations (Master First!)
1. **LC 1046 - Last Stone Weight**: Simple max-heap simulation
2. **LC 215 - Kth Largest Element**: Classic min-heap of size k

### Level 2: Top-K Variations
3. **LC 347 - Top K Frequent Elements**: Frequency + heap
4. **LC 703 - Kth Largest Element in Stream**: Online top-k

### Level 3: Two-Heap Pattern
5. **LC 295 - Find Median from Data Stream**: Two-heap median

### Level 4: K-Way Merge
6. **LC 23 - Merge K Sorted Lists**: Classic k-way merge
7. **LC 373 - Find K Pairs with Smallest Sums**: Virtual k-way merge

### Level 5: Interval/Scheduling
8. **LC 253 - Meeting Rooms II**: Resource scheduling
9. **LC 621 - Task Scheduler**: Greedy scheduling with cooldown

---

## Quick Decision Tree

```
Problem mentions...
├── "kth largest/smallest" → Min/max-heap of size k (LC 215)
├── "top k" + "frequent" → Count + heap (LC 347)
├── "median" + "stream" → Two heaps (LC 295)
├── "merge k sorted" → Min-heap of heads (LC 23)
├── "minimum rooms/resources" → Heap of end times (LC 253)
├── "schedule with cooldown" → Max-heap + queue (LC 621)
└── "repeatedly pick max/min" → Simple heap simulation (LC 1046)
```

---

## Related Patterns

| If you see... | Consider also... |
|--------------|------------------|
| Kth element | Quickselect (O(n) average) |
| Top-k frequent | Bucket sort (O(n) when bounded) |
| Merge k sorted | Divide and conquer |
| Interval scheduling | Sweep line |
| Running median | Balanced BST (SortedList) |

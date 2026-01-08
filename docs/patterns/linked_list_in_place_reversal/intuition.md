# Linked List In-Place Reversal: Building Intuition

> **API Kernel**: `LinkedListInPlaceReversal`
> **Core Insight**: Reverse direction by changing where arrows point, not by moving data.

---

## The Mental Model: Flipping Train Cars

Imagine a train where each car has a coupler pointing to the next car:

```
Engine → Car1 → Car2 → Car3 → Caboose → (nothing)
```

To reverse the train, you don't physically move the cars. Instead, you **flip the direction of each coupler**:

```
(nothing) ← Engine ← Car1 ← Car2 ← Car3 ← Caboose
```

The Caboose becomes the new Engine (new head), and the original Engine points to nothing (new tail).

### The Three-Pointer Dance

At each step, you work with three positions:

```
             prev    curr    next_node
               ↓       ↓       ↓
(reversed) ← [ A ] <- [ B ] -> [ C ] -> (to process)

Action:
1. Save next_node = curr.next (or we lose C forever!)
2. Flip: curr.next = prev (B now points backward to A)
3. Advance prev = curr (prev moves to B)
4. Advance curr = next_node (curr moves to C)
```

It's like a caterpillar inching forward while flipping tracks behind it.

---

## Visual Intuition: The Domino Effect

### Full List Reversal (LC 206)

Think of dominoes standing in a row. To reverse them, you tip each one backward instead of forward:

```
Step 0: Stand behind first domino
        ●→●→●→●→●→ (all pointing right)

Step 1: Tip first one left (into empty space)
        ←● ●→●→●→●→

Step 2: Tip second one into first
        ←●←● ●→●→●→

Step 3: Continue...
        ←●←●←● ●→●→

Step 4: ...until done
        ←●←●←●←●←●
```

The last domino becomes the "head" of the reversed sequence.

### Segment Reversal (LC 92)

Same idea, but you only flip dominoes in a specific range:

```
Original:    ●→●→●→●→●→● (positions 1-6)
Reverse 2-4: ●→ ←●←●←● →●→●

You need to:
1. Walk to position 1 (before the segment)
2. Remember this anchor point
3. Flip dominoes 2,3,4
4. Reconnect: anchor→4, and 2→5
```

### K-Group Reversal (LC 25)

Like reversing sections of a marching band, k musicians at a time:

```
Original (k=2):  [1,2] [3,4] [5]
After groups:    [2,1] [4,3] [5]

For each group:
1. Check: are there k musicians available?
2. If yes: flip their order
3. If no: leave them (the lonely 5 stays)
4. Move to next group
```

---

## Why Three Pointers?

Consider reversing just one link without helpers:

```python
# WRONG - we lose access to the rest!
curr.next = prev   # Oops, where's the next node?
```

The moment you flip `curr.next`, you've severed the connection to everything after `curr`. That's why you MUST save `curr.next` first:

```python
# CORRECT
next_node = curr.next   # Save the bridge before burning it
curr.next = prev        # Now safe to flip
```

This is the most common bug in reversal problems!

---

## The Dummy Node Trick

When you might change the first node, anchor to a fake "pre-head":

```
Without dummy (dangerous when left=1):
    head → [ ] → [ ] → [ ]
    What do we return if head changes?

With dummy (safe):
    dummy → head → [ ] → [ ]
    dummy.next is always the true head, even after changes!
```

Rule of thumb: **If the head might move, use a dummy.**

---

## Segment Reversal: The Bookmark Pattern

For reversing a middle portion, think of bookmarking a book:

```
Book (list):    [ Cover | Pages 1-5 | Pages 6-10 | Pages 11-15 | Back ]

To reverse pages 6-10:
1. Put bookmark BEFORE page 6 (after page 5)
2. Take out pages 6-10
3. Reverse them: 10-9-8-7-6
4. Reinsert: bookmark → page 10, and page 6 → page 11
```

In code:
- `before_segment` = the bookmark (node before left)
- `segment_start` = first page to reverse (becomes tail after)
- `prev` after reversal = last page reversed (becomes head)
- `curr` after reversal = first page NOT reversed (page 11)

---

## K-Group: The Assembly Line

Imagine a factory assembly line with stations processing k items at a time:

```
Conveyor belt:  [1][2][3][4][5][6][7]

Station 1 (k=3): Take [1][2][3], reverse to [3][2][1], pass on
Conveyor belt:  [3][2][1][4][5][6][7]

Station 2 (k=3): Take [4][5][6], reverse to [6][5][4], pass on
Conveyor belt:  [3][2][1][6][5][4][7]

Station 3 (k=3): Only [7] left (< 3), leave as-is
Final:          [3][2][1][6][5][4][7]
```

The key insight: **check availability BEFORE processing each group**.

---

## Common Pitfalls & Fixes

### Pitfall 1: Losing the Next Node
```python
# WRONG
curr.next = prev
curr = curr.next  # Oops, curr.next is now prev!

# FIXED
next_node = curr.next
curr.next = prev
curr = next_node
```

### Pitfall 2: Returning Wrong Head
```python
# WRONG
return head  # head is still the original first node (now tail)

# FIXED
return prev  # prev is the new head after loop ends
```

### Pitfall 3: Off-By-One in Segment
```python
# WRONG: Starting from head when left=2
for _ in range(left):  # Goes one too far!
    before = before.next

# FIXED: Navigate left-1 times from dummy
for _ in range(left - 1):
    before = before.next
```

### Pitfall 4: Forgetting Reconnection
```python
# WRONG: Reversed segment is now floating!
# ... reversal code ...
return dummy.next  # Lost connection!

# FIXED: Reconnect both ends
segment_start.next = curr       # old head → after segment
before_segment.next = prev      # before → new head
```

---

## Complexity Guarantees

| Variant | Time | Space | Key Factor |
|---------|------|-------|------------|
| Full Reversal | O(N) | O(1) | Visit each node once |
| Segment Reversal | O(N) | O(1) | Navigate + reverse subset |
| K-Group Reversal | O(N) | O(1) | Each node: 1 count + 1 reverse |
| Recursive Variants | O(N) | O(N) or O(N/k) | Call stack depth |

The iterative versions are strictly O(1) space because we only use a fixed number of pointer variables, regardless of input size.

---

## Pattern Recognition Checklist

When you see a linked list problem, ask:

1. **Does it mention "reverse"?** → This pattern
2. **"Without extra space"?** → Must be in-place (not array copy)
3. **"Swap adjacent pairs"?** → K-group with k=2
4. **"Reverse between positions"?** → Segment reversal
5. **"Reverse every k nodes"?** → K-group reversal

If yes to any, reach for the three-pointer technique!



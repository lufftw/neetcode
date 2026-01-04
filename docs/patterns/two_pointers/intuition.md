# Two Pointers: Pattern Intuition Guide

> *"Two points of attention, moving in coordinated rhythm — each step permanently narrows the world of possibilities."*

---

## The Situation That Calls for Two Pointers

Imagine you're standing at the edge of a long corridor with doors on both sides. You know the answer lies somewhere in this corridor, but checking every possible pair of doors would take forever.

Then you realize: you don't need to check everything. You can place one hand on the leftmost door and one on the rightmost door. Based on what you find, you know which hand to move. With each movement, doors behind you become irrelevant — forever excluded from consideration.

**This is the essence of Two Pointers.**

You encounter this pattern whenever:
- You're working with a **sorted** or **ordered** sequence
- You need to find **pairs, tuples, or regions** with certain properties
- The relationship between elements is **monotonic** — changing one pointer predictably affects the outcome
- You can **eliminate possibilities** based on the current state

The key insight: *You're not searching — you're eliminating. Every pointer movement permanently shrinks the problem.*

---

## The Invariant: The Space Between

Every two pointers algorithm maintains a **sacred region** — the space where the answer must exist.

```
┌───────────────────────────────────────────────────────────────────────────┐
│                                                                           │
│   [excluded]  ←  left  ═══════ answer space ═══════  right → [excluded]   │
│                                                                           │
│   Once excluded, never reconsidered.                                      │
│   The region between pointers is the ONLY remaining hope.                 │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

The invariant says: *If a valid answer exists, it lies within the current boundaries.* Moving a pointer is a declaration: "I've proven that nothing behind this pointer can be part of the answer."

**This is what makes two pointers work**: each movement is a proof of exclusion. You're not guessing — you're eliminating with certainty.

---

## The Irreversible Decision

Here's the crucial insight that separates two pointers from brute force:

> **Once a pointer moves, it never moves back.**

When you advance `left` from position 3 to position 4, you've permanently decided: "No valid answer involves position 3 as the left element." This decision is irreversible.

This one-directional march is what transforms O(n²) into O(n). Instead of checking all n² pairs, each of the 2n pointer positions is visited at most once.

The irreversibility creates efficiency: *you burn bridges as you cross them.*

---

## The Six Shapes of Two Pointers

Two pointer problems come in six distinct flavors. Recognizing the shape tells you exactly how to position and move the pointers.

---

### Shape 1: Opposite Approach — "Closing the Gap"

**The situation**: Two sentinels stand at opposite ends of a corridor. They walk toward each other, meeting somewhere in the middle.

**What it feels like**: You're squeezing from both ends. The search space shrinks from the outside in.

**The mental model**:
```
Initial:    L ═══════════════════════════════════ R
            ↓                                     ↓
Step 1:       L ═════════════════════════════ R
                                              ↓
Step 2:       L ═════════════════════════ R
              ↓
Step 3:         L ═══════════════════ R
                         ...
Final:                   L R  (or L crosses R)
```

**The decision rule**: Based on the current pair's property:
- If the combined value is **too small** → move `left` right (seek larger)
- If the combined value is **too large** → move `right` left (seek smaller)
- If it matches → record and continue (or return immediately)

**Why it works**: Sorted order creates monotonicity. Moving `left` right can only *increase* its contribution. Moving `right` left can only *decrease* its contribution. This gives you precise control.

**Classic problems**: Two Sum II, Container With Most Water, 3Sum

---

### Shape 2: Same Direction — "The Writer Following the Reader"

**The situation**: Two people walk the same corridor. One is a **Reader** who examines every door. The other is a **Writer** who only records the doors worth keeping.

**What it feels like**: You're filtering in-place. The Reader advances relentlessly; the Writer only moves when something passes the test.

**The mental model**:
```
Initial:    [a] [b] [c] [d] [e] [f]
             W   R
             ↓
             Reader examines 'a'
             'a' passes → Writer takes it, both advance

Step 2:     [a] [b] [c] [d] [e] [f]
                 W   R
                 ↓
                 Reader examines 'b'
                 'b' fails → only Reader advances

Step 3:     [a] [b] [c] [d] [e] [f]
                 W       R
                         ↓
                         Reader examines 'c'
                         'c' passes → Writer takes it, both advance

Final:      [a] [c] [x] [x] [x] [x]
                     ↑
                     New logical end (write position)
```

**The decision rule**: 
- Reader always advances
- Writer only advances when the current element should be kept
- Elements are copied from Reader position to Writer position

**Why it works**: The Writer index marks the boundary of "good" elements. Everything before Writer is the output; everything at or after is either unprocessed or discarded.

**The invariant**: `arr[0:write]` contains exactly the valid elements seen so far, in their original order.

**Classic problems**: Remove Duplicates, Remove Element, Move Zeroes

---

### Shape 3: Fast and Slow — "The Tortoise and the Hare"

**The situation**: Two runners on a track. One runs twice as fast as the other. If the track is a loop, the fast runner will eventually lap the slow one.

**What it feels like**: You're detecting a cycle by observing when speeds converge.

**The mental model**:
```
Linear track (no cycle):
    Slow: 1 step per turn
    Fast: 2 steps per turn

    Fast reaches the end first → No cycle


Circular track (cycle exists):
    ┌───────────────────────────┐
    │                           │
    ↓                           │
   [A] → [B] → [C] → [D] → [E] ─┘
    S          F

    Fast enters cycle first
    Slow eventually enters
    Fast "chases" slow from behind
    Gap closes by 1 each step
    They MUST meet inside the cycle
```

**The decision rule**:
- Slow moves 1 step
- Fast moves 2 steps
- If they meet → cycle exists
- If Fast reaches null → no cycle

**Why it works**: If there's a cycle, once both pointers are inside, the relative distance changes by 1 each iteration. Since the cycle length is finite, they must eventually collide.

**Finding the cycle start** (Phase 2):
- When they meet, reset Slow to head
- Move both at speed 1
- They meet again at the cycle start

This works because of the mathematical relationship between the meeting point and the cycle entry.

**Classic problems**: Linked List Cycle, Happy Number, Find Duplicate Number

---

### Shape 4: Partitioning — "The Bouncer Sorting the Queue"

**The situation**: A bouncer at a club entrance directs each person to one of three sections: left, middle, or right. Each person is examined once and placed in their final position.

**What it feels like**: You're sorting without sorting — classifying elements into regions in a single pass.

**The mental model** (Dutch National Flag):
```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   [  < pivot  ]  [  = pivot  ]  [  unclassified  ]  [ > pivot ] │
│   └───────────┘  └───────────┘  └────────────────┘  └─────────┘ │
│    0      low-1   low    mid-1   mid         high   high+1   n-1│
│                          ↑                                      │
│                      examine this                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Three pointers, three regions**:
- `low`: boundary between "less than" and "equal to"
- `mid`: the examiner, scanning the unclassified region
- `high`: boundary between "unclassified" and "greater than"

**The decision rule**:
- If `arr[mid] < pivot`: swap with `low`, advance both `low` and `mid`
- If `arr[mid] > pivot`: swap with `high`, retreat `high` only (the swapped element needs examination)
- If `arr[mid] == pivot`: advance `mid` only

**Why it works**: Each element is placed in its final region. The `mid` pointer only advances when we're certain the element at `mid` belongs to the middle or has been swapped from a known region.

**Classic problems**: Sort Colors, Partition Array, Sort By Parity

---

### Shape 5: Dedup Enumeration — "Pinning Down the Triangle"

**The situation**: You need to find all unique triplets (or quadruplets) with a target property. You've seen Two Sum with a hash map — now imagine finding *all* Two Sum pairs, without duplicates, inside a loop.

**What it feels like**: You pin down one corner, then use opposite pointers to sweep the remaining candidates.

**The mental model**:
```
Find all triplets summing to 0:

For each i (the anchor):
    ┌─────────────────────────────────────────────────┐
    │   nums[i] is FIXED for this iteration           │
    │                                                 │
    │   [anchor]  [left ═══════════════════ right]    │
    │      i        i+1                      n-1      │
    │                                                 │
    │   Use opposite pointers to find pairs           │
    │   that complete the triplet                     │
    │                                                 │
    └─────────────────────────────────────────────────┘
```

**The deduplication insight**: After sorting:
- Skip `i` if `nums[i] == nums[i-1]` (don't anchor at duplicate)
- After finding a triplet, skip `left` forward while `nums[left] == nums[left+1]`
- After finding a triplet, skip `right` backward while `nums[right] == nums[right-1]`

**Why it works**: Sorting enables two things:
1. The opposite-pointer technique for finding pairs in O(n)
2. Adjacent duplicates can be skipped to avoid duplicate triplets

**The irreversible truth**: Once anchor `i` is processed, all triplets starting with `nums[i]` are found. Moving to `i+1` permanently excludes `nums[i]` from being an anchor again.

**Classic problems**: 3Sum, 4Sum, 3Sum Closest

---

### Shape 6: Merge — "Two Rivers Joining"

**The situation**: Two sorted streams need to become one. You hold a cup at the head of each stream. You pour from whichever cup has the smaller value.

**What it feels like**: You're interleaving two sorted sequences into a single sorted sequence.

**The mental model**:
```
Stream 1:  [1] [3] [5] [7]
            ↑
            i

Stream 2:  [2] [4] [6]
            ↑
            j

Output:    [1]
            └── smaller of arr1[i] and arr2[j]

After pouring 1:
Stream 1:  [1] [3] [5] [7]
                ↑
                i

Output:    [1] [2]
                └── now arr2[j] is smaller
```

**The decision rule**:
- Compare `arr1[i]` and `arr2[j]`
- Take the smaller one, advance that pointer
- When one stream empties, pour the remainder of the other

**Why it works**: Both streams are sorted. The smallest unpoured element must be at one of the two heads. By always taking the smaller head, we maintain sorted order in the output.

**In-place variant** (LeetCode 88): Write from the end to avoid overwriting unprocessed elements.

**Classic problems**: Merge Sorted Array, Merge Two Sorted Lists, Squares of Sorted Array

---

## Pattern Recognition: "Is This a Two Pointers Problem?"

Ask yourself these questions:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  1. Is the sequence SORTED (or can I sort it)?              │
│     └── No? → Two pointers unlikely (consider hash map)     │
│                                                             │
│  2. Am I looking for PAIRS or TUPLES with a property?       │
│     └── Yes? → Opposite pointers or dedup enumeration       │
│                                                             │
│  3. Do I need to modify the array IN-PLACE?                 │
│     └── Yes? → Same-direction (writer pattern)              │
│                                                             │
│  4. Am I detecting a CYCLE in a sequence?                   │
│     └── Yes? → Fast-slow pointers                           │
│                                                             │
│  5. Am I PARTITIONING by some property?                     │
│     └── Yes? → Dutch flag pattern                           │
│                                                             │
│  6. Am I MERGING two sorted sequences?                      │
│     └── Yes? → Merge pattern                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## The Moment of Recognition

You're reading a problem. You notice:

- *"Given a **sorted** array..."* — Sorting enables deterministic pointer movement
- *"Find **two elements** that sum to..."* — Pair search screams opposite pointers
- *"Remove ... **in-place** with O(1) extra space"* — Same-direction writer
- *"Detect if there's a **cycle**..."* — Fast-slow pointers
- *"**Sort** the array so that all X come before Y..."* — Partitioning
- *"**Merge** two sorted..."* — Merge pattern

And you feel it: *This is a two pointers problem. I know exactly which shape.*

That's the goal. Instant recognition. No hesitation.

---

## Why O(n)? The Amortized Argument

Every two pointers algorithm achieves O(n) through the same principle:

> **Each pointer only moves forward.**

Consider opposite pointers:
- `left` starts at 0, can only increase, ends at most at n-1: **at most n moves**
- `right` starts at n-1, can only decrease, ends at most at 0: **at most n moves**
- Total moves: **at most 2n = O(n)**

Consider same-direction:
- `read` visits each position exactly once: **n moves**
- `write` moves at most once per `read` move: **at most n moves**
- Total moves: **at most 2n = O(n)**

The magic: *No element is ever reconsidered.* This is the irreversibility that transforms quadratic brute force into linear elegance.

---

## Visual Intuition: The Six Shapes Side by Side

```
┌─────────────────────────────────────────────────────────────────────────┐
│  OPPOSITE POINTERS                                                      │
│  L → → → → → → → → → → → ← ← ← ← ← ← ← ← ← ← ← R                        │
│  Closing in from both ends                                              │
├─────────────────────────────────────────────────────────────────────────┤
│  SAME DIRECTION (WRITER)                                                │
│  W → → → → →           (selective)                                      │
│  R → → → → → → → → → → (relentless)                                     │
│  Writer follows reader, keeping only what passes                        │
├─────────────────────────────────────────────────────────────────────────┤
│  FAST-SLOW                                                              │
│  S → → → → → → →                                                        │
│  F → → → → → → → → → → → → → →                                          │
│  If they meet, there's a cycle                                          │
├─────────────────────────────────────────────────────────────────────────┤
│  PARTITIONING (DUTCH FLAG)                                              │
│  [  <  ] [  =  ] [  ?  ] [  >  ]                                        │
│       low    mid      high                                              │
│  Three regions, one-pass classification                                 │
├─────────────────────────────────────────────────────────────────────────┤
│  DEDUP ENUMERATION                                                      │
│  [anchor]  L → → → → → → → → → ← ← ← ← ← ← R                            │
│      i         opposite pointers in subarray                            │
│  Fix one, sweep the rest                                                │
├─────────────────────────────────────────────────────────────────────────┤
│  MERGE                                                                  │
│  [1] [3] [5] →                                                          │
│  [2] [4] [6] →        ══>  [1] [2] [3] [4] [5] [6]                      │
│  Two sorted streams becoming one                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Detailed Traces: Seeing the Pattern in Motion

### Trace 1: Opposite Pointers — Two Sum II

**Problem**: Find two numbers in sorted array that sum to target.  
**Input**: `nums = [2, 7, 11, 15]`, `target = 9`

```
┌────────────────────────────────────────────────────────────────────────┐
│  Step 0:  [2]  [7]  [11]  [15]     target = 9                          │
│            L              R        sum = 2 + 15 = 17                   │
│                                    17 > 9 → move R left                │
├────────────────────────────────────────────────────────────────────────┤
│  Step 1:  [2]  [7]  [11]  [15]                                         │
│            L         R             sum = 2 + 11 = 13                   │
│                                    13 > 9 → move R left                │
├────────────────────────────────────────────────────────────────────────┤
│  Step 2:  [2]  [7]  [11]  [15]                                         │
│            L    R                  sum = 2 + 7 = 9                     │
│                                    9 == 9 → FOUND! Return [1, 2]       │
└────────────────────────────────────────────────────────────────────────┘

Key observations:
• We never examined (2,11) or (7,11) or (7,15) — they were eliminated!
• Each step provably excluded possibilities based on monotonicity.
```

---

### Trace 2: Same-Direction — Remove Duplicates

**Problem**: Remove duplicates from sorted array in-place.  
**Input**: `nums = [1, 1, 2, 2, 2, 3]`

```
┌────────────────────────────────────────────────────────────────────────┐
│  Initial: [1]  [1]  [2]  [2]  [2]  [3]                                 │
│            W    R                                                      │
│                                                                        │
│  Step 0:  nums[R]=1, nums[W-1]=undefined → KEEP                        │
│           write_index becomes 1                                        │
│           [1]  [1]  [2]  [2]  [2]  [3]                                 │
│                 W    R                                                 │
│                                                                        │
│  Step 1:  nums[R]=1 == nums[W-1]=1 → SKIP                              │
│           [1]  [1]  [2]  [2]  [2]  [3]                                 │
│                 W         R                                            │
│                                                                        │
│  Step 2:  nums[R]=2 != nums[W-1]=1 → KEEP                              │
│           [1]  [2]  [2]  [2]  [2]  [3]                                 │
│                      W         R                                       │
│                                                                        │
│  Step 3:  nums[R]=2 == nums[W-1]=2 → SKIP                              │
│           [1]  [2]  [2]  [2]  [2]  [3]                                 │
│                      W              R                                  │
│                                                                        │
│  Step 4:  nums[R]=2 == nums[W-1]=2 → SKIP                              │
│           [1]  [2]  [2]  [2]  [2]  [3]                                 │
│                      W                   R                             │
│                                                                        │
│  Step 5:  nums[R]=3 != nums[W-1]=2 → KEEP                              │
│           [1]  [2]  [3]  [2]  [2]  [3]                                 │
│                           W                   R (done)                 │
│                                                                        │
│  Result:  First 3 elements [1, 2, 3] are the unique values             │
└────────────────────────────────────────────────────────────────────────┘

Invariant maintained throughout:
• nums[0:W] contains exactly the unique elements seen so far
• Elements are in their original sorted order
```

---

### Trace 3: Fast-Slow — Cycle Detection

**Problem**: Detect if linked list has a cycle.  
**Input**: `1 → 2 → 3 → 4 → 5 → 3` (cycle back to node 3)

```
┌────────────────────────────────────────────────────────────────────────┐
│  The linked list:                                                      │
│                                                                        │
│      1 → 2 → 3 → 4 → 5                                                 │
│              ↑       │                                                 │
│              └───────┘                                                 │
│                                                                        │
├────────────────────────────────────────────────────────────────────────┤
│  Step 0:  S=1, F=1 (start)                                             │
│                                                                        │
│  Step 1:  S=2 (moved 1)                                                │
│           F=3 (moved 2)                                                │
│                                                                        │
│  Step 2:  S=3 (moved 1)                                                │
│           F=5 (moved 2)                                                │
│                                                                        │
│  Step 3:  S=4 (moved 1)                                                │
│           F=4 (moved 2: 5→3→4)  ← F wrapped around the cycle!          │
│                                                                        │
│  Step 4:  S=5 (moved 1)                                                │
│           F=3 (moved 2: 4→5→3)                                         │
│                                                                        │
│  Step 5:  S=3 (moved 1: 5→3)                                           │
│           F=5 (moved 2: 3→4→5)                                         │
│                                                                        │
│  Step 6:  S=4 (moved 1)                                                │
│           F=4 (moved 2: 5→3→4)                                         │
│                                                                        │
│           S == F → CYCLE DETECTED!                                     │
└────────────────────────────────────────────────────────────────────────┘

Why they MUST meet:
• Once both are in the cycle, Fast "chases" Slow
• The gap closes by 1 each step (Fast gains 1 on Slow)
• Maximum steps until collision = cycle length
```

---

### Trace 4: Dutch National Flag — Sort Colors

**Problem**: Sort array containing only 0s, 1s, and 2s.  
**Input**: `nums = [2, 0, 2, 1, 1, 0]`

```
┌────────────────────────────────────────────────────────────────────────┐
│  Legend: low (L), mid (M), high (H)                                    │
│  Regions: [0..L) = 0s, [L..M) = 1s, [M..H] = unclassified, (H..] = 2s  │
├────────────────────────────────────────────────────────────────────────┤
│  Initial: [2]  [0]  [2]  [1]  [1]  [0]                                 │
│            L,M                      H                                  │
│            ↑ examine 2: >1 → swap with H, H--                          │
│                                                                        │
│  Step 1:  [0]  [0]  [2]  [1]  [1]  [2]                                 │
│            L,M                 H                                       │
│            ↑ examine 0: <1 → swap with L, L++, M++                     │
│                                                                        │
│  Step 2:  [0]  [0]  [2]  [1]  [1]  [2]                                 │
│                 L,M            H                                       │
│                 ↑ examine 0: <1 → swap with L (self), L++, M++         │
│                                                                        │
│  Step 3:  [0]  [0]  [2]  [1]  [1]  [2]                                 │
│                      L,M       H                                       │
│                      ↑ examine 2: >1 → swap with H, H--                │
│                                                                        │
│  Step 4:  [0]  [0]  [1]  [1]  [2]  [2]                                 │
│                      L,M  H                                            │
│                      ↑ examine 1: =1 → M++                             │
│                                                                        │
│  Step 5:  [0]  [0]  [1]  [1]  [2]  [2]                                 │
│                      L        M,H                                      │
│                           ↑ examine 1: =1 → M++                        │
│                                                                        │
│  Step 6:  [0]  [0]  [1]  [1]  [2]  [2]                                 │
│                      L            M (M > H, done!)                     │
│                               H                                        │
│                                                                        │
│  Result: [0, 0, 1, 1, 2, 2] — sorted in single pass!                   │
└────────────────────────────────────────────────────────────────────────┘

Key insight:
• When swapping with high, we DON'T advance mid — the swapped element is unclassified
• When swapping with low, we DO advance mid — the swapped element is known to be 0 or 1
```

---

## From Intuition to Implementation

Only now — after the patterns feel inevitable — does code become useful.

### Opposite Pointers Template

```python
def opposite_pointers(arr):
    """
    Two pointers approaching from opposite ends.
    Use when: sorted array, finding pairs with target property.
    """
    left, right = 0, len(arr) - 1
    
    while left < right:
        current = evaluate(arr, left, right)
        
        if current == target:
            return record_answer(left, right)
        elif current < target:
            left += 1   # Need larger: move left forward
        else:
            right -= 1  # Need smaller: move right backward
    
    return no_answer_found
```

### Same-Direction (Writer) Template

```python
def same_direction(arr):
    """
    Writer follows reader, keeping valid elements.
    Use when: in-place modification, filtering, deduplication.
    """
    write = 0
    
    for read in range(len(arr)):
        if should_keep(arr, read, write):
            arr[write] = arr[read]
            write += 1
    
    return write  # New logical length
```

### Fast-Slow Template

```python
def fast_slow(head):
    """
    Detect cycle using speed differential.
    Use when: cycle detection, finding midpoint.
    """
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            return True  # Cycle detected
    
    return False  # No cycle
```

### Dutch National Flag Template

```python
def partition_three_way(arr, pivot=1):
    """
    Partition into three regions in single pass.
    Use when: sorting by category, three-way partition.
    """
    low, mid, high = 0, 0, len(arr) - 1
    
    while mid <= high:
        if arr[mid] < pivot:
            arr[low], arr[mid] = arr[mid], arr[low]
            low += 1
            mid += 1
        elif arr[mid] > pivot:
            arr[mid], arr[high] = arr[high], arr[mid]
            high -= 1  # Don't advance mid — swapped element is unknown
        else:
            mid += 1
```

### Merge Template

```python
def merge_sorted(arr1, arr2):
    """
    Merge two sorted arrays into one.
    Use when: combining sorted sequences.
    """
    i, j = 0, 0
    result = []
    
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1
    
    result.extend(arr1[i:])
    result.extend(arr2[j:])
    return result
```

---

## Quick Reference: Shape Selection Guide

| When You See... | Think... | Shape |
|----------------|----------|-------|
| "Sorted array, find pair with sum X" | Closing the gap | Opposite |
| "Remove/modify in-place with O(1) space" | Writer follows reader | Same-Direction |
| "Detect cycle in linked list" | Tortoise and hare | Fast-Slow |
| "Sort array with only 2-3 distinct values" | Bouncer sorting queue | Partitioning |
| "Find all unique triplets summing to X" | Pin one, sweep the rest | Dedup Enumeration |
| "Merge two sorted arrays" | Two rivers joining | Merge |

---

## Common Pitfalls

### Pitfall 1: Forgetting the Sorted Prerequisite

Two pointers works because sorting creates monotonicity. If you need two pointers but the array isn't sorted, sort it first (if allowed).

### Pitfall 2: Off-by-One in Termination

- Opposite: `while left < right` (not `<=`) for pair problems
- Same-direction: `for read in range(len(arr))` visits all elements
- Fast-slow: check `fast and fast.next` before advancing

### Pitfall 3: Not Handling Duplicates in Enumeration

For 3Sum and similar, always skip duplicates at both the anchor level and the pointer level:
```python
if i > 0 and nums[i] == nums[i-1]:
    continue  # Skip duplicate anchor
```

### Pitfall 4: Advancing Mid in Dutch Flag After High Swap

When you swap `arr[mid]` with `arr[high]`, the new value at `mid` is unclassified. Don't advance `mid` — examine it in the next iteration.

---

## The Two Pointers Mantra

> **One invariant: the answer lies between.**  
> **One rule: once passed, never reconsidered.**  
> **One result: O(n) elegance from O(n²) brute force.**

When you see sorted sequences and pair-finding, think of the sentinels. When you see in-place modification, think of the writer following the reader. When you see cycles, think of the tortoise and hare.

The pattern is always the same: *coordinated movement, irreversible exclusion, linear time.*

---

*For implementation templates and problem mappings, see [templates.md](./templates.md).*


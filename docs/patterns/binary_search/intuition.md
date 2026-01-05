# Binary Search: Pattern Intuition Guide

> *"The answer hides in a shrinking world. With each question, half the universe becomes impossible."*

---

## The Situation That Calls for Binary Search

Imagine a library with a million books arranged by author name. You're looking for "Kafka." You could start at the first shelf and walk forward — that would take forever. Or you could go to the middle, see "Miller," realize Kafka comes before Miller, and instantly know: the entire right half of the library is irrelevant. You'll never look there again.

**This is the essence of Binary Search.**

You encounter this pattern whenever:
- The search space has an **ordering** or **monotonic property**
- You can ask a **yes/no question** that eliminates half the candidates
- The answer to that question tells you which half to keep
- Once you eliminate a half, it's **gone forever**

The key insight: *You're not searching — you're eliminating. Each question cuts the world in half.*

---

## The Invariant: The Shrinking Promise

Every binary search algorithm maintains one sacred promise:

> **If the answer exists, it lies within `[left, right]`.**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   [eliminated]  ←  left  ═══════ answer must be here ═══════  right →  [eliminated]
│                                                                             │
│   Everything before 'left' has been proven wrong.                           │
│   Everything after 'right' has been proven wrong.                           │
│   The answer, if it exists, is trapped between them.                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

The invariant is your compass. Every decision must preserve it. When `left` and `right` converge, you've cornered the answer.

---

## The Irreversible Decision

Here's what gives binary search its power:

> **Once you eliminate a half, you never look back.**

When you discover that the middle element is too small, you declare: *"Everything to the left of mid, including mid itself, is forever excluded."* You set `left = mid + 1` and move on.

This is not a guess. This is a proof. The monotonic property guarantees that if `arr[mid]` is too small, then `arr[0], arr[1], ..., arr[mid]` are all too small. You've eliminated half the universe with a single comparison.

This one-directional march — always shrinking, never expanding — is what transforms O(n) linear search into O(log n) binary search. Each step doesn't just make progress; it *halves* the remaining work.

---

## The Predicate: The Question That Divides

At the heart of every binary search is a **predicate** — a yes/no question you ask about the middle element.

```
The search space, viewed through the predicate:

┌───────────────────────────────────────────────────────────────┐
│  [F, F, F, F, F, F, T, T, T, T, T, T, T]                       │
│                    ↑                                           │
│               The Boundary                                     │
│                                                                │
│  Predicate is False here  │  Predicate is True here            │
│  ─────────────────────────┼────────────────────────────────    │
│                           │                                    │
│  "Find the FIRST position where predicate becomes True"        │
└───────────────────────────────────────────────────────────────┘
```

**The unifying insight**: Almost every binary search problem can be reframed as:
- *"Find the first position where some condition becomes true"*
- Or equivalently: *"Find the boundary between false and true"*

| Problem Type | The Predicate |
|--------------|---------------|
| Find target | `arr[mid] >= target` (first position ≥ target) |
| First occurrence | `arr[mid] >= target` |
| Last occurrence | `arr[mid] > target` (then subtract 1) |
| Minimum speed to finish | `can_finish(speed)` |
| Minimum capacity to ship | `can_ship(capacity)` |
| Find peak | `arr[mid] > arr[mid+1]` (descending = peak nearby) |

Once you see the predicate, the algorithm writes itself.

---

## The Two Forces at Play

Every binary search is a dialogue between two boundaries:

### The Left Sentinel
- Guards the lower boundary
- Advances when the predicate is false at mid
- Says: *"The answer is not here or before. Move forward."*
- Updates: `left = mid + 1`

### The Right Sentinel
- Guards the upper boundary
- Retreats when the predicate is true at mid
- Says: *"The answer might be here or earlier. Hold this ground."*
- Updates: `right = mid`

They march toward each other. When they meet, the search is over. The meeting point is the boundary.

```
Initial:    L ════════════════════════════════════════════ R
                              mid
                               ↓
Step 1:                    predicate(mid) = False
            ─────────────────→ L ═══════════════════════════ R
                              (left jumps past mid)

                                        mid
                                         ↓
Step 2:                              predicate(mid) = True
            ════════════════════ L ═════ R ←─────────────────
                                        (right shrinks to mid)

                                   mid
                                    ↓
Step 3:                         predicate(mid) = True
            ════════════════════ L R ←──
                                (right shrinks to mid)

Final:      ════════════════════ L=R
                                 ↑
                            The Boundary
```

---

## The Five Shapes of Binary Search

Binary search problems come in five distinct shapes. Recognizing the shape tells you exactly how to frame the predicate and where to find the answer.

---

### Shape 1: Boundary Search — "Find the First True"

**The situation**: You have a sorted array and want to find where a property first becomes true.

**What it feels like**: Walking through a threshold. Before: no. After: yes. You want to find the exact moment of transition.

**The mental model**:
```
Looking for first occurrence of 5:
arr = [1, 2, 3, 5, 5, 5, 7, 8]
       F  F  F  T  T  T  T  T    ← predicate: arr[mid] >= 5
                ↑
          First True = Answer

Looking for insertion point of 4:
arr = [1, 2, 3, 5, 5, 5, 7, 8]
       F  F  F  T  T  T  T  T    ← predicate: arr[mid] >= 4
                ↑
          First True = Insertion Point
```

**The key insight**: Lower bound and upper bound are just different predicates:
- **Lower bound**: First `i` where `arr[i] >= target`
- **Upper bound**: First `i` where `arr[i] > target`

**Classic problems**: Search Insert Position, First and Last Position, Find Smallest Letter Greater Than Target

---

### Shape 2: Exact Match — "Is It Here?"

**The situation**: You want to find a specific value, returning its index or -1.

**What it feels like**: Looking for a friend in a crowd. You scan to the middle, ask if they're left or right, and keep narrowing.

**The subtle truth**: Exact match is just boundary search with verification:
1. Find the boundary (first position where `arr[i] >= target`)
2. Check if `arr[boundary] == target`
3. If yes, return boundary. If no, return -1.

Or use the classic three-way split:
- `arr[mid] == target`: Found it!
- `arr[mid] < target`: Go right
- `arr[mid] > target`: Go left

**Classic problems**: Binary Search, Search a 2D Matrix

---

### Shape 3: Rotated Array — "Two Sorted Halves"

**The situation**: A sorted array was rotated at an unknown pivot. The order is broken, but not gone — it's hidden in two pieces.

**What it feels like**: A ring that was cut and unfolded. The elements are still sorted, just wrapped around.

```
Original: [0, 1, 2, 3, 4, 5, 6, 7]
Rotated:  [4, 5, 6, 7, 0, 1, 2, 3]
                    ↑
               The Pivot (minimum element)

The key observation:
┌──────────────────────────────────────────────────────────────┐
│  [4, 5, 6, 7, 0, 1, 2, 3]                                    │
│   ↑           ↑        ↑                                     │
│  left        mid     right                                   │
│                                                              │
│  At any mid, ONE HALF is guaranteed to be sorted:            │
│  - If arr[left] <= arr[mid]: left half is sorted             │
│  - Otherwise: right half is sorted                           │
│                                                              │
│  The sorted half gives you exact bounds to check.            │
└──────────────────────────────────────────────────────────────┘
```

**The decision rule**:
1. Determine which half is sorted
2. Check if target is in the sorted half (using exact bounds)
3. If yes, search that half. If no, search the other half.

**The invariant**: If target exists, it's still in `[left, right]`. You eliminate the half where target provably cannot exist.

**With duplicates**: When `arr[left] == arr[mid] == arr[right]`, you can't determine which half is sorted. Shrink linearly: `left++, right--`. This is the price of duplicates — worst case becomes O(n).

**Classic problems**: Search in Rotated Sorted Array I/II, Find Minimum in Rotated Sorted Array

---

### Shape 4: Answer Space Search — "Search Over Possibilities"

**The situation**: You're not searching an array — you're searching over all possible answers to find the optimal one.

**What it feels like**: You're a quality inspector. You test if a proposed answer works. If it does, you try something more ambitious. If it fails, you try something more conservative.

```
Problem: What's the minimum eating speed to finish in time?

Answer Space: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
               ↓  ↓  ↓  ↓  ↓  ↓  ↓  ↓  ↓  ↓
Feasibility:   F  F  F  F  T  T  T  T  T  T  ...
                          ↑
                   First feasible = optimal answer

The predicate: can_finish_in_time(speed) returns True/False
Binary search finds the minimum speed where predicate is True.
```

**The pattern**:
1. Define the answer space: `[lo, hi]` where lo is the minimum possible answer and hi is the maximum
2. Define the feasibility predicate: does this answer work?
3. Binary search for the first (or last) feasible answer

**The monotonicity requirement**: If answer `x` works, then `x+1` must also work (for minimization) or `x-1` must also work (for maximization). This is what makes binary search valid.

**Classic problems**:
- Koko Eating Bananas (minimize speed)
- Capacity To Ship Packages (minimize capacity)
- Split Array Largest Sum (minimize maximum)
- Magnetic Force Between Two Balls (maximize minimum)

---

### Shape 5: Peak Finding — "Follow the Slope"

**The situation**: Find a peak (local maximum) in an array where neighbors are never equal.

**What it feels like**: You're hiking in fog. You can only see your immediate surroundings. But you know: if you keep walking uphill, you'll eventually reach a peak.

```
The Mountain:
                    ╱╲
                   ╱  ╲
                  ╱    ╲
            ╱╲  ╱        ╲
           ╱  ╲╱          ╲
          ╱                 ╲
         ╱
        ╱

Observation at mid:
- If arr[mid] < arr[mid+1]: You're on an ascending slope → peak is to the RIGHT
- If arr[mid] > arr[mid+1]: You're on a descending slope → peak is to the LEFT (or here!)

Boundary condition: arr[-1] = arr[n] = -∞
This guarantees at least one peak exists.
```

**The key insight**: Unlike exact match, you're not looking for a specific value — you're following a direction. The ascending slope *pulls* you toward a peak. Once you're on a slope, you know a peak exists in that direction.

**The invariant**: There is always a peak within `[left, right]`. Moving toward "uphill" preserves this invariant.

**Classic problems**: Find Peak Element, Peak Index in Mountain Array

---

## Pattern Recognition: "Is This a Binary Search Problem?"

Ask yourself these questions:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  1. Is the data SORTED or does it have a MONOTONIC property?    │
│     └── No? → Binary search unlikely (consider hash map)        │
│                                                                 │
│  2. Can I define a YES/NO predicate that divides the space?     │
│     └── No? → Binary search won't help                          │
│                                                                 │
│  3. Does the predicate have a TRANSITION point?                 │
│     (All False, then all True — or vice versa)                  │
│     └── No? → Binary search won't work                          │
│                                                                 │
│  4. Once I know the answer at mid, can I ELIMINATE half?        │
│     └── No? → You need the whole space, use linear scan         │
│                                                                 │
│  5. Am I looking for "minimum X such that..." or                │
│     "maximum X such that..."?                                   │
│     └── Yes? → Binary search on answer space!                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## The Moment of Recognition

You're reading a problem. You see phrases like:
- *"sorted array"*
- *"find the first..."* / *"find the last..."*
- *"minimum speed/capacity/time such that..."*
- *"maximum distance/value such that..."*
- *"O(log n) required"*

And you feel it: *This is a boundary I need to find. I can ask a yes/no question. Half the world will vanish.*

That's your cue. The sentinels are ready. The space wants to shrink.

---

## Visualizing the Dance

### Trace 1: Lower Bound Search

**Problem**: Find first position where `arr[i] >= 5`
**Input**: `arr = [1, 2, 4, 5, 5, 5, 8, 9]`

```
┌────────────────────────────────────────────────────────────────────────┐
│  Initial:  [1]  [2]  [4]  [5]  [5]  [5]  [8]  [9]                      │
│             L                                   R        (L=0, R=8)    │
│                         mid=4                                          │
│                          ↓                                             │
│             arr[4]=5 >= 5 → True                                       │
│             Answer might be here or earlier → R = mid                  │
├────────────────────────────────────────────────────────────────────────┤
│  Step 1:   [1]  [2]  [4]  [5]  [5]  [5]  [8]  [9]                      │
│             L              R                        (L=0, R=4)         │
│                  mid=2                                                 │
│                   ↓                                                    │
│             arr[2]=4 >= 5 → False                                      │
│             Answer must be after mid → L = mid + 1                     │
├────────────────────────────────────────────────────────────────────────┤
│  Step 2:   [1]  [2]  [4]  [5]  [5]  [5]  [8]  [9]                      │
│                         L    R                      (L=3, R=4)         │
│                         mid=3                                          │
│                          ↓                                             │
│             arr[3]=5 >= 5 → True                                       │
│             Answer might be here or earlier → R = mid                  │
├────────────────────────────────────────────────────────────────────────┤
│  Step 3:   [1]  [2]  [4]  [5]  [5]  [5]  [8]  [9]                      │
│                         L=R                         (L=3, R=3)         │
│                          ↑                                             │
│             CONVERGED! First position >= 5 is index 3                  │
└────────────────────────────────────────────────────────────────────────┘

Result: 3 (arr[3] = 5, the first occurrence)
```

---

### Trace 2: Rotated Array Search

**Problem**: Find target = 0 in rotated sorted array
**Input**: `arr = [4, 5, 6, 7, 0, 1, 2]`

```
┌────────────────────────────────────────────────────────────────────────┐
│  Initial:  [4]  [5]  [6]  [7]  [0]  [1]  [2]                           │
│             L              mid              R        (L=0, R=6)        │
│                             ↓                                          │
│             arr[mid]=7 ≠ 0                                             │
│             Is left half sorted? arr[0]=4 <= arr[3]=7 → YES            │
│             Is 0 in [4, 7)? → NO                                       │
│             Search right half → L = mid + 1                            │
├────────────────────────────────────────────────────────────────────────┤
│  Step 1:   [4]  [5]  [6]  [7]  [0]  [1]  [2]                           │
│                              L   mid    R            (L=4, R=6)        │
│                                   ↓                                    │
│             arr[mid]=1 ≠ 0                                             │
│             Is left half sorted? arr[4]=0 <= arr[5]=1 → YES            │
│             Is 0 in [0, 1)? → YES!                                     │
│             Search left half → R = mid - 1                             │
├────────────────────────────────────────────────────────────────────────┤
│  Step 2:   [4]  [5]  [6]  [7]  [0]  [1]  [2]                           │
│                              L=R                     (L=4, R=4)        │
│                               ↓                                        │
│             arr[mid]=0 = 0 → FOUND!                                    │
└────────────────────────────────────────────────────────────────────────┘

Result: 4 (arr[4] = 0)
```

---

### Trace 3: Binary Search on Answer Space

**Problem**: Minimum eating speed to finish 4 piles in 8 hours
**Input**: `piles = [3, 6, 7, 11]`, `h = 8`

```
┌────────────────────────────────────────────────────────────────────────┐
│  Answer space: [1, 11]  (minimum 1, maximum = max pile)                │
│                                                                        │
│  Feasibility predicate:                                                │
│  can_finish(speed) = sum(ceil(pile/speed)) <= h                        │
├────────────────────────────────────────────────────────────────────────┤
│  Step 1:   lo=1, hi=11, mid=6                                          │
│            Hours at speed 6: ceil(3/6)+ceil(6/6)+ceil(7/6)+ceil(11/6)  │
│                             = 1 + 1 + 2 + 2 = 6                        │
│            6 <= 8 → Feasible! Try smaller → hi = 6                     │
├────────────────────────────────────────────────────────────────────────┤
│  Step 2:   lo=1, hi=6, mid=3                                           │
│            Hours at speed 3: ceil(3/3)+ceil(6/3)+ceil(7/3)+ceil(11/3)  │
│                             = 1 + 2 + 3 + 4 = 10                       │
│            10 > 8 → NOT feasible! Need faster → lo = 4                 │
├────────────────────────────────────────────────────────────────────────┤
│  Step 3:   lo=4, hi=6, mid=5                                           │
│            Hours at speed 5: ceil(3/5)+ceil(6/5)+ceil(7/5)+ceil(11/5)  │
│                             = 1 + 2 + 2 + 3 = 8                        │
│            8 <= 8 → Feasible! Try smaller → hi = 5                     │
├────────────────────────────────────────────────────────────────────────┤
│  Step 4:   lo=4, hi=5, mid=4                                           │
│            Hours at speed 4: ceil(3/4)+ceil(6/4)+ceil(7/4)+ceil(11/4)  │
│                             = 1 + 2 + 2 + 3 = 8                        │
│            8 <= 8 → Feasible! Try smaller → hi = 4                     │
├────────────────────────────────────────────────────────────────────────┤
│  Step 5:   lo=4, hi=4 → CONVERGED!                                     │
└────────────────────────────────────────────────────────────────────────┘

Result: Minimum speed = 4 bananas per hour
```

---

## The Off-by-One Trap

Binary search is famous for off-by-one errors. Here's how to avoid them:

### The Two Schools

| Style | Loop Condition | Right Init | On True | On False |
|-------|---------------|-----------|---------|----------|
| `[left, right)` | `left < right` | `n` | `right = mid` | `left = mid + 1` |
| `[left, right]` | `left <= right` | `n - 1` | `right = mid - 1` | `left = mid + 1` |

**The `[left, right)` style** is recommended for boundary search because:
- The loop terminates with `left == right`, giving you exactly one candidate
- `right = mid` (not `mid - 1`) keeps the true candidate in range
- The final `left` is directly the answer — no adjustment needed

### The Mid Calculation

Always use:
```
mid = left + (right - left) // 2
```

Never use:
```
mid = (left + right) // 2  # Can overflow!
```

### The Termination Guarantee

For `left < right` with `right = mid` and `left = mid + 1`:
- If predicate is True: range becomes `[left, mid]` — shrinks by at least 1
- If predicate is False: range becomes `[mid+1, right]` — shrinks by at least 1
- Range always shrinks → loop always terminates

---

## Why O(log n)? The Halving Argument

```
Start:     n candidates
Step 1:    n/2 candidates
Step 2:    n/4 candidates
Step 3:    n/8 candidates
...
Step k:    n/2^k candidates

When n/2^k = 1:
    2^k = n
    k = log₂(n)

Total steps: O(log n)
```

Each step does O(1) work (one comparison, maybe some arithmetic). Total: O(log n).

This is the magic of elimination. Linear search asks: "Is it here? Is it here? Is it here?" — O(n) questions. Binary search asks: "Is it in this half?" — O(log n) questions. At n = 1 million, that's 1,000,000 vs 20.

---

## From Intuition to Implementation

Only now — after the dance feels inevitable — does code become useful.

### The Universal Template: First True

```python
def binary_search_first_true(left, right, predicate):
    """
    Find the first position where predicate(x) is True.

    Invariant: If answer exists, it's in [left, right].
    Termination: left == right, single candidate remains.

    Returns: First index where predicate is True, or 'right' if never True.
    """
    while left < right:
        mid = left + (right - left) // 2

        if predicate(mid):
            # True at mid — answer might be here or earlier
            right = mid
        else:
            # False at mid — answer must be after mid
            left = mid + 1

    return left  # The boundary between False and True
```

This single template handles:
- Lower bound: `predicate = lambda i: arr[i] >= target`
- Upper bound: `predicate = lambda i: arr[i] > target`
- First occurrence: lower bound + verify equality
- Minimum feasible: `predicate = lambda x: is_feasible(x)`
- Peak finding: `predicate = lambda i: arr[i] > arr[i+1]`

The variations come from:
1. **What is the predicate?**
2. **What is the search space?**
3. **Do you need to verify the answer?**

---

## Quick Reference: Shape → Template

| Shape | Predicate | Search Space | Answer |
|-------|-----------|--------------|--------|
| Lower bound | `arr[mid] >= target` | `[0, n)` | `left` |
| Upper bound | `arr[mid] > target` | `[0, n)` | `left` |
| Exact match | Three-way comparison | `[0, n-1]` | `mid` or `-1` |
| Rotated search | Sorted-half check | `[0, n-1]` | `mid` or `-1` |
| Min feasible | `can_do(mid)` | `[lo, hi]` | `left` |
| Max feasible | `can_do(mid)` | `[lo, hi]` | `right` or `left-1` |
| Peak finding | `arr[mid] > arr[mid+1]` | `[0, n-1]` | `left` |

---

## Common Pitfalls

### Pitfall 1: Wrong Loop Condition

For boundary search (`right = mid`), use `left < right`.
For exact match (`right = mid - 1`), use `left <= right`.

Mixing them causes infinite loops or missed answers.

### Pitfall 2: Forgetting to Verify

Lower bound finds the first position `>= target`, not the target itself. Always check:
```python
if left < n and arr[left] == target:
    return left
return -1
```

### Pitfall 3: Wrong Monotonicity Direction

For "minimum X such that feasible(X)":
- Predicate should be `feasible(X)` → first True
- Search finds **minimum** feasible

For "maximum X such that feasible(X)":
- Predicate should be `NOT feasible(X)` → first True gives you one-past-max
- Or use: `feasible(X)` → last True = first False - 1

### Pitfall 4: Integer Overflow in Mid

In languages with fixed-size integers:
```
mid = left + (right - left) / 2  # Safe
mid = (left + right) / 2          # Can overflow if left + right > MAX_INT
```

Python has arbitrary precision integers, so this isn't an issue, but it's a critical habit for other languages.

---

## The Binary Search Mantra

> **One invariant: the answer lies within.**
> **One question: which half to eliminate?**
> **One step: half the world vanishes forever.**

When you see sorted data or monotonic predicates, think of the shrinking universe. Ask your question. Watch half the candidates disappear. Repeat until only the answer remains.

The power of binary search isn't finding — it's eliminating.

---

*For implementation templates and problem mappings, see [templates.md](./templates.md).*

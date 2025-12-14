# Sliding Window: Pattern Intuition Guide

> *"The window is a moving lens of attention — it forgets the past to focus on what matters now."*

---

## The Situation That Calls for a Window

Imagine you're walking through a long corridor, and you can only see through a rectangular frame you carry with you. As you move forward, new things enter your view on the right, and old things disappear on the left.

**This is the essence of Sliding Window.**

You encounter this pattern whenever:
- You're scanning through a sequence (string, array, stream)
- You care about a **contiguous portion** of that sequence
- The answer depends on properties of that portion
- Those properties can be **updated incrementally** as the portion shifts

The key insight: *You don't need to remember everything — only what's currently in view.*

---

## The Two Forces at Play

Every sliding window algorithm is a dance between two opposing forces:

### The Explorer (Right Boundary) $R$
- Always moves forward, never backward
- Discovers new territory
- Adds new elements to consideration
- Asks: *"What happens if I include this?"*

### The Gatekeeper (Left Boundary) $L$
- Follows behind, cleaning up
- Removes elements that no longer serve the goal
- Enforces the rules of what's allowed
- Asks: *"Must I let go of something to stay valid?"*

The Explorer is eager and expansive. The Gatekeeper is disciplined and selective. Together, they maintain a **window of validity** that slides through the sequence.

---

## The Invariant: The Window's Promise

At every moment, the window makes a promise — an **invariant** that must always be true:

| Problem Type | The Promise |
|--------------|-------------|
| Longest unique substring | *"Every character in my view appears exactly once"* |
| At most K distinct | *"I contain no more than K different characters"* |
| Minimum covering substring | *"I contain everything required"* |
| Sum at least target | *"My total meets or exceeds the goal"* |

**This promise is sacred.** The moment it's broken, the Gatekeeper must act — shrinking the window until the promise is restored.

---

## The Irreversible Truth

Here's what makes sliding window work: **the Explorer never retreats.**

Once the right boundary passes an element, that element has been "seen." We may include it or exclude it from our current window, but we never go back to re-examine it as a potential starting point... unless the Gatekeeper releases it.

This one-directional march is what gives us O(n) time complexity. Each element enters the window at most once and exits at most once. No element is visited more than twice across the entire algorithm.

The irreversibility creates efficiency: *past decisions don't haunt us.*

---

## The Two Modes of Seeking

Depending on what you're optimizing, the dance changes:

### Mode 1: Maximize the Window
*"How large can my view become while staying valid?"*

```
Process:
1. Explorer advances, adding new element
2. If promise breaks → Gatekeeper advances until promise restored
3. Record the current window size (this is a candidate answer)
4. Repeat

The window EXPANDS freely, CONTRACTS only when forced.
```

**Mental image**: Stretching a rubber band until it's about to snap, then easing off just enough.

#### Flowchart: Maximize Window

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Example: Longest Substring Without Repeating Characters                    │
│  Sequence: [ a  b  c  a  b ]    Promise: "All chars unique"                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────┐                                                                    │
│  │START│                                                                    │
│  └──┬──┘                                                                    │
│     ▼                                                                       │
│  ╔══════════════════════════════╗                                           │
│  ║  🟢 R advances (Explorer)    ║  ◀─────────────────────────┐              │
│  ║     Add element to state     ║                            │              │
│  ╚═══════════════╤══════════════╝                            │              │
│                  ▼                                           │              │
│        ┌─────────────────────┐                               │              │
│        │ Promise broken?     │                               │              │
│        │ (duplicate found?)  │                               │              │
│        └────────┬────────────┘                               │              │
│           Yes   │   No                                       │              │
│      ┌──────────┴──────────┐                                 │              │
│      ▼                     ▼                                 │              │
│  ╔═══════════════════╗  ┌─────────────────────┐              │              │
│  ║ 🔴 L advances     ║  │ ✅ Update answer:   │              │              │
│  ║   (Gatekeeper)    ║  │    max(ans, R-L+1)  │              │              │
│  ║ Remove from state ║  └──────────┬──────────┘              │              │
│  ╚═════════╤═════════╝             │                         │              │
│            │                       │                         │              │
│            ▼                       │                         │              │
│   ┌────────────────┐               │                         │              │
│   │Promise restored?│              │                         │              │
│   └───────┬────────┘               │                         │              │
│      No   │   Yes                  │                         │              │
│   ┌───────┴───────┐                │                         │              │
│   │               ▼                ▼                         │              │
│   │         ┌──────────────────────────────┐                 │              │
│   │         │  More elements?              │                 │              │
│   │         └─────────────┬────────────────┘                 │              │
│   │               Yes     │    No                            │              │
│   │           ┌───────────┴───────────┐                      │              │
│   ▼           │                       ▼                      │              │
│  🔴 L++       │                  ┌─────────┐                 │              │
│  (repeat)     └──────────────────┤  DONE   │                 │              │
│                                  └─────────┘                 │              │
│                                                              │              │
└──────────────────────────────────────────────────────────────┴──────────────┘

Visual Trace:
═══════════════════════════════════════════════════════════════════════════════

  Sequence:   a    b    c    a    b
             [0]  [1]  [2]  [3]  [4]

  Step 1:   🟢R→
            [ a ]                        max = 1
              L,R

  Step 2:        🟢R→
            [ a    b ]                   max = 2
              L        R

  Step 3:             🟢R→
            [ a    b    c ]              max = 3
              L              R

  Step 4:                  🟢R→
            [ a    b    c    a ]         ❌ 'a' duplicate!
              L                  R
                         │
            🔴L→ 🔴L→    ▼
                 [ b    c    a ]         max = 3 (restored)
                   L              R

  Step 5:                       🟢R→
                 [ b    c    a    b ]    ❌ 'b' duplicate!
                   L                  R
                         │
            🔴L→ 🔴L→    ▼
                      [ c    a    b ]    max = 3 (final)
                        L              R

Legend: 🟢 = R expands (green)  🔴 = L contracts (red)  ❌ = promise broken
```

---

### Mode 2: Minimize the Window
*"How small can my view become while still being valid?"*

```
Process:
1. Explorer advances until promise becomes TRUE
2. While promise holds → Gatekeeper advances, shrinking window
3. Record the window size just before promise breaks
4. Repeat

The window EXPANDS until valid, then CONTRACTS aggressively.
```

**Mental image**: Tightening a noose around the minimal solution.

#### Flowchart: Minimize Window

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Example: Minimum Size Subarray Sum ≥ 7                                     │
│  Sequence: [ 2  3  1  2  4  3 ]    Promise: "Sum ≥ target"                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────┐                                                                    │
│  │START│                                                                    │
│  └──┬──┘                                                                    │
│     ▼                                                                       │
│  ╔══════════════════════════════╗                                           │
│  ║  🟢 R advances (Explorer)    ║  ◀─────────────────────────┐              │
│  ║     Add to sum               ║                            │              │
│  ╚═══════════════╤══════════════╝                            │              │
│                  ▼                                           │              │
│        ┌─────────────────────┐                               │              │
│        │ Promise satisfied?  │                               │              │
│        │   (sum ≥ target?)   │                               │              │
│        └────────┬────────────┘                               │              │
│            No   │   Yes                                      │              │
│      ┌──────────┴──────────────────────┐                     │              │
│      │                                 ▼                     │              │
│      │  ┌────────────────────────────────────────────────┐   │              │
│      │  │  WHILE promise still holds:                    │   │              │
│      │  │  ┌──────────────────────────────────────────┐  │   │              │
│      │  │  │ ✅ Update answer: min(ans, R-L+1)        │  │   │              │
│      │  │  │ 🔴 L advances (Gatekeeper)               │  │   │              │
│      │  │  │    Subtract from sum                     │  │   │              │
│      │  │  └──────────────────────────────────────────┘  │   │              │
│      │  └────────────────────────────────────────────────┘   │              │
│      │                                 │                     │              │
│      │                                 ▼                     │              │
│      │         ┌──────────────────────────────┐              │              │
│      └────────►│  More elements?              │              │              │
│                └─────────────┬────────────────┘              │              │
│                        Yes   │    No                         │              │
│                    ┌─────────┴─────────┐                     │              │
│                    │                   ▼                     │              │
│                    │              ┌─────────┐                │              │
│                    └──────────────┤  DONE   │                │              │
│                                   └─────────┘                │              │
│                                                              │              │
└──────────────────────────────────────────────────────────────┴──────────────┘

Visual Trace:
═══════════════════════════════════════════════════════════════════════════════

  Sequence:   2    3    1    2    4    3      target = 7
             [0]  [1]  [2]  [3]  [4]  [5]

  Step 1:   🟢R→
            [ 2 ]                sum=2 < 7   min = ∞
              L,R                (keep expanding)

  Step 2:        🟢R→
            [ 2    3 ]           sum=5 < 7   min = ∞
              L        R         (keep expanding)

  Step 3:             🟢R→
            [ 2    3    1 ]      sum=6 < 7   min = ∞
              L              R   (keep expanding)

  Step 4:                  🟢R→
            [ 2    3    1    2 ] sum=8 ≥ 7  ✅ VALID!
              L                  R
                     │
            🔴L→     ▼           Record: min = 4
                 [ 3    1    2 ] sum=6 < 7  (stop contracting)
                   L              R

  Step 5:                       🟢R→
                 [ 3    1    2    4 ]  sum=10 ≥ 7  ✅
                   L                   R
                     │
            🔴L→     ▼           Record: min = 4
                      [ 1    2    4 ]  sum=7 ≥ 7  ✅
                        L              R
                     │
            🔴L→     ▼           Record: min = 3
                           [ 2    4 ]  sum=6 < 7  (stop)
                             L         R

  Step 6:                              🟢R→
                           [ 2    4    3 ]  sum=9 ≥ 7  ✅
                             L              R
                     │
            🔴L→     ▼           Record: min = 3
                                [ 4    3 ]  sum=7 ≥ 7  ✅
                                  L         R
                     │
            🔴L→     ▼           Record: min = 2 ✨ FINAL
                                     [ 3 ]  sum=3 < 7  (stop)
                                       L,R

Legend: 🟢 = R expands  🔴 = L contracts  ✅ = promise satisfied
```

---

## Pattern Recognition: "Is This a Sliding Window Problem?"

Ask yourself these questions:

```
┌─────────────────────────────────────────────────────────────┐
│  1. Am I looking for a CONTIGUOUS subarray or substring?   │
│     └── No? → Not sliding window                           │
│                                                             │
│  2. Can I describe a PROPERTY that makes a window valid?   │
│     └── No? → Probably not sliding window                  │
│                                                             │
│  3. Can I UPDATE that property in O(1) when I add/remove   │
│     a single element?                                       │
│     └── No? → Sliding window won't give O(n)               │
│                                                             │
│  4. Is the answer about OPTIMIZING that window             │
│     (longest, shortest, exists)?                            │
│     └── Yes to all? → SLIDING WINDOW.                      │
└─────────────────────────────────────────────────────────────┘
```

---

## The Three Window Shapes

### Shape 1: Variable Window, Maximize
**Story**: *"I want the biggest room that still follows the rules."*

- Invariant: Some constraint must not be violated
- Strategy: Grow greedily, shrink reluctantly
- Answer: Largest valid window seen

**Classic problems**: Longest substring without repeating characters, longest with at most K distinct

### Shape 2: Variable Window, Minimize  
**Story**: *"I want the smallest container that still holds everything I need."*

- Invariant: Some requirement must be satisfied
- Strategy: Grow until valid, shrink aggressively
- Answer: Smallest valid window seen

**Classic problems**: Minimum window substring, minimum size subarray sum

### Shape 3: Fixed Window
**Story**: *"I'm looking through a frame of exact size — does it ever show what I'm looking for?"*

- Invariant: Window size exactly K
- Strategy: Add one, remove one, check condition
- Answer: Whether/where condition is met

**Classic problems**: Find all anagrams, check permutation inclusion

#### Fixed Window Example Trace (K=3)

```
Problem: Find maximum sum of any subarray of size K=3
Sequence: [ 1  4  2  10  2  3  1  0  20 ]

┌──────┬───────┬─────────┬──────────────────┬───────────────┬────────────────┐
│ Step │ R→    │ sum     │ L action         │ Window [L,R]  │ Max Sum        │
├──────┼───────┼─────────┼──────────────────┼───────────────┼────────────────┤
│  0   │ 1     │ 1       │ —                │ [1]           │ (building...)  │
│  1   │ 4     │ 5       │ —                │ [1,4]         │ (building...)  │
│  2   │ 2     │ 7       │ —                │ [1,4,2]       │ 7 ✨           │
│  3   │ 10    │ 7+10=17 │ 🔴 remove 1 → 16 │ [4,2,10]      │ 16             │
│  4   │ 2     │ 16+2=18 │ 🔴 remove 4 → 14 │ [2,10,2]      │ 16             │
│  5   │ 3     │ 14+3=17 │ 🔴 remove 2 → 15 │ [10,2,3]      │ 16             │
│  6   │ 1     │ 15+1=16 │ 🔴 remove 10→ 6  │ [2,3,1]       │ 16             │
│  7   │ 0     │ 6+0=6   │ 🔴 remove 2 → 4  │ [3,1,0]       │ 16             │
│  8   │ 20    │ 4+20=24 │ 🔴 remove 3 → 21 │ [1,0,20]      │ 21 ✨          │
└──────┴───────┴─────────┴──────────────────┴───────────────┴────────────────┘

Key insight: Once R reaches index 2 (K-1), every subsequent step:
  1. 🟢 R advances → add new element
  2. 🔴 L advances → remove oldest element (exactly K steps behind)
  3. Window size stays constant at K=3

Answer: Maximum sum = 21 (subarray [1, 0, 20])
```

---

## The State: What the Window Remembers

The window isn't just boundaries — it carries **state** about its contents:

| What You're Tracking | State Structure | Update Cost |
|---------------------|-----------------|-------------|
| Character uniqueness | Last-seen index map | O(1) |
| Character frequencies | Count map | O(1) |
| Distinct count | Map + size | O(1) |
| Running sum | Single integer | O(1) |
| Requirement satisfaction | "Have" vs "Need" counters | O(1) |

The magic of sliding window is that these states are **incrementally maintainable**. Adding an element updates the state. Removing an element reverses that update. No full recomputation needed.

---

## Visualizing the Dance

**Problem**: Longest substring without repeating characters  
**Input**: `"abcabcbb"` — Find the longest window where all characters are unique.

| Step | $R$ (char) | State: `last_seen` | $L$ move? | Window `[L, R]` | Max Length |
|:----:|:----------:|:-------------------|:---------:|:---------------:|:----------:|
| 0 | `a` | `{a:0}` | — | `[0,0]` = "a" | 1 |
| 1 | `b` | `{a:0, b:1}` | — | `[0,1]` = "ab" | 2 |
| 2 | `c` | `{a:0, b:1, c:2}` | — | `[0,2]` = "abc" | 3 |
| 3 | `a` | `{a:3, b:1, c:2}` | 🔴 `L→1` (skip past old 'a') | `[1,3]` = "bca" | 3 |
| 4 | `b` | `{a:3, b:4, c:2}` | 🔴 `L→2` (skip past old 'b') | `[2,4]` = "cab" | 3 |
| 5 | `c` | `{a:3, b:4, c:5}` | 🔴 `L→3` (skip past old 'c') | `[3,5]` = "abc" | 3 |
| 6 | `b` | `{a:3, b:6, c:5}` | 🔴 `L→5` (skip past old 'b') | `[5,6]` = "cb" | 3 |
| 7 | `b` | `{a:3, b:7, c:5}` | 🔴 `L→7` (skip past old 'b') | `[7,7]` = "b" | 3 |

**Answer**: 3 (substring `"abc"`)

**Key observations**:
- $R$ (Explorer) advances every single step — never skips, never retreats
- $L$ (Gatekeeper) only moves when a duplicate is found in the current window
- The jump optimization: $L$ jumps directly to `last_seen[char] + 1` instead of incrementing one by one
- Window length = `R - L + 1`

---

## The Moment of Recognition

You're reading a problem. You see phrases like:
- *"contiguous subarray"*
- *"substring"*  
- *"longest/shortest"*
- *"at most K"*
- *"containing all of"*

And you feel it: *This is about maintaining something over a moving portion.*

That's your cue. The Explorer and Gatekeeper are ready. The window wants to slide.

---

## From Intuition to Implementation

Only now — after the dance is clear — does code become useful.

The template is always the same skeleton:

```python
def sliding_window(sequence):
    state = initial_state()
    left = 0
    answer = initial_answer()
    
    ## 1. Explorer (R) always advances
    for right, element in enumerate(sequence):
        # Explorer: include new element
        update_state_add(state, element)
        
        ## 2. Gatekeeper (L) acts to restore invariant
        while promise_is_broken(state):
            update_state_remove(state, sequence[left])
            left += 1
        
        # Record: this window is valid
        answer = consider(answer, left, right)
    
    return answer
```

The variations come from:
1. **What is the promise?** (determines the while condition)
2. **What state do we track?** (determines the data structure)
3. **What are we optimizing?** (determines how we update the answer)

---

## Quick Reference: Problem → Pattern Mapping

| When You See... | Think... | Window Type |
|----------------|----------|-------------|
| "Longest substring with unique chars" | Uniqueness promise | Maximize |
| "Longest with at most K distinct" | Count limit promise | Maximize |
| "Minimum window containing all of T" | Coverage promise | Minimize |
| "Subarray sum ≥ target" | Threshold promise | Minimize |
| "Contains permutation" | Exact match promise | Fixed |
| "Find all anagrams" | Exact match, collect all | Fixed |

---

## The Pattern in One Sentence

> *Sliding Window is the art of maintaining a valid contiguous view by advancing eagerly and retreating only when necessary.*

When you see a problem about optimizing over contiguous sequences with incrementally checkable properties — you've found your window.

Let it slide.

---

*For detailed implementations and code examples, see [templates.md](./templates.md).*

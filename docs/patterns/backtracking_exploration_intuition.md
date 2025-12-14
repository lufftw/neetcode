# Backtracking: The Art of Reversible Exploration

> **Core Intuition**: You're exploring a maze of choices. You walk forward, leaving footprints. When you hit a dead end, you walk backward—erasing each footprint—until you find an untried path.

---

## Table of Contents

1. [The Feeling of Backtracking](#1-the-feeling-of-backtracking)
2. [The Three Forces: Choose, Explore, Unchoose](#2-the-three-forces-choose-explore-unchoose)
3. [The Invariant That Makes It Work](#3-the-invariant-that-makes-it-work)
4. [When the Pattern Appears](#4-when-the-pattern-appears)
5. [The Five Shapes of the Decision Tree](#5-the-five-shapes-of-the-decision-tree)
6. [Pruning: Seeing Dead Ends Early](#6-pruning-seeing-dead-ends-early)
7. [Deduplication: One Path to Each Treasure](#7-deduplication-one-path-to-each-treasure)
8. [From Intuition to Code](#8-from-intuition-to-code)
9. [Problem Gallery](#9-problem-gallery)
10. [Quick Reference Templates](#10-quick-reference-templates)

---

## 1. The Feeling of Backtracking

### What the Situation Feels Like

Imagine standing at the entrance of a cave with many branching tunnels. You need to find *all* chambers containing treasure. You have:
- A ball of thread (your *path*)
- Chalk to mark visited junctions (your *state*)

You unroll thread as you walk deeper. When a tunnel ends (dead end) or you find treasure (valid solution), you *rewind* the thread and *erase* your chalk marks—returning to the last junction to try a different tunnel.

**This is backtracking**: systematic exploration where every choice is reversible, every path is fully explored, and the explorer always returns to a clean state before trying alternatives.

### The Three Key Observations

1. **The world is a tree of choices**: From any point, you have several options. Each option leads to more options. This creates a decision tree.

2. **You must try everything**: Unlike optimization problems where you seek *one* best answer, here you want *all* valid configurations.

3. **Choices are reversible**: Unlike a one-way door, you can step back. But stepping back must *completely* undo what stepping forward did.

### What Changes Over Time

As you explore:
- Your **path grows** (you add choices)
- Your **path shrinks** (you remove choices when backtracking)
- **Branches get exhausted** (once fully explored, they're never revisited)

What remains constant:
- The **problem structure** (the cave's layout)
- The **invariant**: *at any moment, your state perfectly reflects your current path*

---

## 2. The Three Forces: Choose, Explore, Unchoose

Every backtracking algorithm is a rhythm of three actions:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   CHOOSE  →  Make a decision, modify state                  │
│      ↓                                                      │
│   EXPLORE →  Recurse into the world where that choice holds │
│      ↓                                                      │
│   UNCHOOSE → Undo the decision, restore state exactly       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Choose**: You pick one of the available options. You mark it as taken. Your path grows by one.

**Explore**: You commit to that choice and see what's possible in the world where it holds. You recurse.

**Unchoose**: When you return from exploration, you *must* undo the choice. The state returns to exactly what it was before. Your path shrinks by one.

### The Moment of Permanence

Here's the subtle truth: backtracking *feels* reversible, but something *is* permanent:

> Once you've explored a branch completely, that branch is **forever finished**.

You've extracted every treasure from that path. When you backtrack past a junction, you're not erasing the treasures you found—you're just erasing your footprints so you can walk a different path.

---

## 3. The Invariant That Makes It Work

### The State Consistency Invariant

> **At every moment, the current state reflects exactly the path taken to reach this point—nothing more, nothing less.**

If your path is `[A, B, C]`, then:
- `A` is marked as used
- `B` is marked as used
- `C` is marked as used
- Nothing else is marked

When you backtrack from `C`, your path becomes `[A, B]`, and `C` *must* be unmarked. If you forget to unmark `C`, you'll think it's still used when you try other paths, and you'll miss solutions.

### Why This Invariant Matters

The invariant guarantees:

1. **No missed solutions**: Every valid configuration is reachable through some path.
2. **No duplicates**: Each configuration is visited exactly once.
3. **Correct pruning**: When you prune, you're pruning based on true state.

**The most common bug**: Forgetting to undo state changes. The explorer walks backward but leaves chalk marks on the wall. Future paths see phantom constraints.

---

## 4. When the Pattern Appears

### Instant Recognition Signals

You're facing a backtracking problem when:

| Signal | What It Means |
|--------|---------------|
| "Find **all** valid configurations" | You need exhaustive enumeration, not just one |
| "Generate all permutations/subsets/combinations" | Classic decision tree over choices |
| "Partition such that every part satisfies..." | Try all cut positions |
| "Place pieces so no conflicts..." | Constraint satisfaction over positions |
| "Find all paths through a grid" | DFS with visited tracking |

### The Decision Tree Mental Model

Every backtracking problem has a hidden tree:

```
                     []                    ← Root: empty state
            ┌────────┼────────┐
          [A]       [B]       [C]          ← First choice: 3 options
        ┌──┴──┐   ┌──┴──┐   ┌──┴──┐
      [AB] [AC] [BA] [BC] [CA] [CB]        ← Second choice
        │    │    │    │    │    │
      ...  ...  ...  ...  ...  ...         ← Continue until complete
```

You're walking this tree. At each node, you:
1. Check if you've found treasure (base case)
2. If not, try each child (recursive case)
3. Return to parent when all children exhausted

---

## 5. The Five Shapes of the Decision Tree

Backtracking problems fall into five distinct shapes. Recognizing the shape tells you exactly what to track and how to recurse.

### Shape 1: Permutation — "Arrange All, Order Matters"

**The situation**: You have n distinct items. You want every possible ordering.

**The constraint**: Each item appears exactly once per arrangement.

**What to track**: Which items have been used (`used[]` array).

**The tree shape**: 
- Level 0: n choices (pick first item)
- Level 1: n-1 choices (pick from unused)
- Level k: n-k choices
- **Leaves**: n! arrangements

```
Who goes first?  → [1] or [2] or [3]
Who goes second? → [1,2] or [1,3] (not [1,1])
...
```

### Shape 2: Subset — "Include or Exclude, Order Doesn't Matter"

**The situation**: You have n items. You want every possible subset.

**The constraint**: Items appear in canonical order (no `{2,1}`, only `{1,2}`).

**What to track**: Start index (only consider items from here onward).

**The tree shape**:
- At each item: include it or skip it
- **Leaves**: 2^n subsets

```
Item 1: [include] → [1]    or [skip] → []
Item 2: [1,2] or [1] or [2] or []
...
```

**Key insight**: Using a start index automatically enforces canonical order. You never look backward.

### Shape 3: Target Sum — "Reach a Goal"

**The situation**: Find combinations that add up to a target.

**The constraint**: Sum must equal target exactly.

**What to track**: Remaining target (what's left to fill).

**The pruning**: If remaining goes negative, stop. If sorted and current element exceeds remaining, stop entirely.

```
Target: 7
Pick 2 → remaining: 5
Pick 3 → remaining: 2
Pick 2 → remaining: 0 ← FOUND!
```

### Shape 4: Constraint Satisfaction — "Place Without Conflict"

**The situation**: Place items (queens, numbers) so no two conflict.

**The constraint**: Each placement must satisfy rules with all previous placements.

**What to track**: Sets of forbidden values (columns, diagonals, etc.).

**The pruning**: If no valid position exists at current row/cell, backtrack immediately.

```
N-Queens:
Row 0: Place queen → column 2 now forbidden, diagonals forbidden
Row 1: Only columns not forbidden are valid
...
```

### Shape 5: Segmentation — "Cut Into Valid Pieces"

**The situation**: Partition a sequence into parts where each part is valid.

**The constraint**: Each segment must pass a validity check.

**What to track**: Current position (where next cut starts).

**The pruning**: If segment fails validity, don't recurse.

```
"aab" palindrome partition:
Cut after 'a': "a" is palindrome → recurse on "ab"
Cut after 'aa': "aa" is palindrome → recurse on "b"
...
```

---

## 6. Pruning: Seeing Dead Ends Early

### The Insight

Not all paths lead to treasure. Some lead to dead ends. The earlier you recognize a dead end, the less time you waste walking toward it.

**Pruning** is recognizing impossibility *before* you reach it.

### Four Pruning Strategies

#### 1. Feasibility Bound — "Not Enough Left"

*"I need 3 more items, but only 2 remain. No point continuing."*

```
Combinations of k elements:
If remaining_elements < elements_needed:
    stop exploring
```

#### 2. Target Bound — "Already Too Much"

*"I'm looking for sum 10, but I'm already at 12. Going deeper only adds more."*

```
Combination Sum:
If current_sum > target:
    stop exploring
```

#### 3. Sorted Early Exit — "Everything After Is Worse"

*"Items are sorted. If this one is too big, all following are too big."*

```
If candidates are sorted and candidates[i] > remaining:
    break (not just continue)
```

#### 4. Constraint Propagation — "No Valid Move Exists"

*"Every column is attacked by existing queens. No legal placement at this row."*

```
N-Queens:
If no column is valid at this row:
    backtrack
```

### The Pruning Principle

> The best path not taken is the path you never started.

Every pruned branch saves exponential work. A single check that prevents going down a branch of depth d saves O(branching_factor^d) operations.

---

## 7. Deduplication: One Path to Each Treasure

### The Problem of Duplicates

When input has repeated elements, different paths can lead to the same treasure:

```
Input: [1, 1, 2]
Path via index 0 → index 1: [1, 1]
Path via index 1 → index 0: [1, 1]  ← Same treasure, different path!
```

### The Two Deduplication Strategies

#### Strategy 1: Canonical Order (for subsets/combinations)

**Rule**: Only pick element at index `i` if you haven't skipped it earlier in this level.

```
Sort first.
At each level, skip nums[i] if:
    i > start_index AND nums[i] == nums[i-1]
```

**Intuition**: At each level, among identical items, always pick the leftmost one first. Never pick the second `1` if you didn't pick the first `1`.

#### Strategy 2: Used-Based Skip (for permutations)

**Rule**: Among identical items, only use the k-th one if the (k-1)-th is already in the path.

```
Sort first.
Skip nums[i] if:
    i > 0 AND nums[i] == nums[i-1] AND NOT used[i-1]
```

**Intuition**: Identical items must be used in their natural left-to-right order. This ensures only one permutation of identical items is generated.

### Why Sorting Is Essential

Deduplication requires identical items to be adjacent. Sorting brings them together. Without sorting, you can't compare with the previous item.

---

## 8. From Intuition to Code

Now that the intuition is established, code becomes a natural transcription of the process.

### The Universal Template

```python
def backtrack(state, choices):
    # BASE CASE: Is this a complete solution?
    if is_complete(state):
        collect(state)
        return
    
    # RECURSIVE CASE: Try each available choice
    for choice in available_choices(state, choices):
        # CHOOSE: Make this choice
        apply(state, choice)
        
        # EXPLORE: Recurse
        backtrack(state, next_choices(choices, choice))
        
        # UNCHOOSE: Undo this choice
        undo(state, choice)
```

The template maps exactly to the three forces:
- `apply()` is Choose
- `backtrack()` is Explore  
- `undo()` is Unchoose

---

## 9. Problem Gallery

Each problem below shows the shape recognition and implementation.

### 9.1 Permutations (LeetCode 46)

**Shape**: Permutation — arrange all, order matters.

**Recognition**: "Return all possible permutations" + all elements must appear once.

**What to track**: `used[]` array marking which elements are in current path.

**Time**: O(n! × n) — n! permutations, O(n) to copy each.

```python
def permute(nums: list[int]) -> list[list[int]]:
    results: list[list[int]] = []
    n = len(nums)
    path: list[int] = []
    used: list[bool] = [False] * n
    
    def backtrack() -> None:
        if len(path) == n:
            results.append(path[:])
            return
        
        for i in range(n):
            if used[i]:
                continue
            
            # Choose
            path.append(nums[i])
            used[i] = True
            
            # Explore
            backtrack()
            
            # Unchoose
            path.pop()
            used[i] = False
    
    backtrack()
    return results
```

### 9.2 Permutations II — With Duplicates (LeetCode 47)

**Shape**: Permutation with deduplication.

**Delta**: Sort + skip duplicates at same level.

```python
def permute_unique(nums: list[int]) -> list[list[int]]:
    results: list[list[int]] = []
    n = len(nums)
    nums.sort()  # Critical: bring duplicates together
    path: list[int] = []
    used: list[bool] = [False] * n
    
    def backtrack() -> None:
        if len(path) == n:
            results.append(path[:])
            return
        
        for i in range(n):
            if used[i]:
                continue
            # Skip duplicate at same level
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
            
            path.append(nums[i])
            used[i] = True
            backtrack()
            path.pop()
            used[i] = False
    
    backtrack()
    return results
```

### 9.3 Subsets (LeetCode 78)

**Shape**: Subset — include or exclude, canonical order.

**Recognition**: "Return all possible subsets (the power set)."

**What to track**: Start index to enforce forward-only selection.

**Time**: O(2^n × n) — 2^n subsets, O(n) to copy each.

```python
def subsets(nums: list[int]) -> list[list[int]]:
    results: list[list[int]] = []
    path: list[int] = []
    n = len(nums)
    
    def backtrack(start: int) -> None:
        # Every path is a valid subset
        results.append(path[:])
        
        for i in range(start, n):
            path.append(nums[i])
            backtrack(i + 1)  # Move forward only
            path.pop()
    
    backtrack(0)
    return results
```

### 9.4 Subsets II — With Duplicates (LeetCode 90)

**Shape**: Subset with deduplication.

**Delta**: Sort + skip duplicates at same level.

```python
def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    results: list[list[int]] = []
    nums.sort()  # Critical for deduplication
    path: list[int] = []
    n = len(nums)
    
    def backtrack(start: int) -> None:
        results.append(path[:])
        
        for i in range(start, n):
            # Skip duplicate at same level
            if i > start and nums[i] == nums[i - 1]:
                continue
            
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()
    
    backtrack(0)
    return results
```

### 9.5 Combinations (LeetCode 77)

**Shape**: Subset with fixed size k.

**Recognition**: "Return all combinations of k numbers from [1..n]."

**Delta from subsets**: Only collect when path length equals k.

**Pruning**: Stop early if not enough elements remain.

```python
def combine(n: int, k: int) -> list[list[int]]:
    results: list[list[int]] = []
    path: list[int] = []
    
    def backtrack(start: int) -> None:
        if len(path) == k:
            results.append(path[:])
            return
        
        # Pruning: need (k - len(path)) more, have (n - start + 1) available
        need = k - len(path)
        for i in range(start, n - need + 2):
            path.append(i)
            backtrack(i + 1)
            path.pop()
    
    backtrack(1)
    return results
```

### 9.6 Combination Sum (LeetCode 39)

**Shape**: Target sum with element reuse allowed.

**Recognition**: "Find all combinations that sum to target. Each number may be used unlimited times."

**Key difference**: Recurse with same index (reuse allowed).

```python
def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    results: list[list[int]] = []
    candidates.sort()  # For pruning
    path: list[int] = []
    
    def backtrack(start: int, remaining: int) -> None:
        if remaining == 0:
            results.append(path[:])
            return
        
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break  # Pruning: sorted, all after are larger
            
            path.append(candidates[i])
            backtrack(i, remaining - candidates[i])  # Same index: reuse
            path.pop()
    
    backtrack(0, target)
    return results
```

### 9.7 Combination Sum II (LeetCode 40)

**Shape**: Target sum, no reuse, with duplicates.

**Delta**: Use i+1 (no reuse) + deduplicate.

```python
def combination_sum2(candidates: list[int], target: int) -> list[list[int]]:
    results: list[list[int]] = []
    candidates.sort()
    path: list[int] = []
    
    def backtrack(start: int, remaining: int) -> None:
        if remaining == 0:
            results.append(path[:])
            return
        
        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i - 1]:
                continue  # Skip duplicate at same level
            if candidates[i] > remaining:
                break
            
            path.append(candidates[i])
            backtrack(i + 1, remaining - candidates[i])  # i+1: no reuse
            path.pop()
    
    backtrack(0, target)
    return results
```

### 9.8 Combination Sum III (LeetCode 216)

**Shape**: Target sum with fixed count, bounded range [1-9].

**Dual constraint**: Exactly k numbers that sum to n.

```python
def combination_sum3(k: int, n: int) -> list[list[int]]:
    results: list[list[int]] = []
    path: list[int] = []
    
    def backtrack(start: int, remaining: int) -> None:
        if len(path) == k:
            if remaining == 0:
                results.append(path[:])
            return
        
        # Pruning: not enough numbers left
        if 9 - start + 1 < k - len(path):
            return
        
        for i in range(start, 10):
            if i > remaining:
                break
            
            path.append(i)
            backtrack(i + 1, remaining - i)
            path.pop()
    
    backtrack(1, n)
    return results
```

### 9.9 N-Queens (LeetCode 51/52)

**Shape**: Constraint satisfaction — place without conflict.

**Recognition**: "Place n queens on n×n board with no attacks."

**What to track**: Sets of forbidden columns and diagonals.

**Key insight**: Row-by-row placement eliminates row conflicts by design.

```python
def solve_n_queens(n: int) -> list[list[str]]:
    results: list[list[str]] = []
    queen_cols: list[int] = [-1] * n
    
    used_cols: set[int] = set()
    used_diag_main: set[int] = set()   # row - col is constant
    used_diag_anti: set[int] = set()   # row + col is constant
    
    def backtrack(row: int) -> None:
        if row == n:
            results.append(build_board(queen_cols, n))
            return
        
        for col in range(n):
            d_main, d_anti = row - col, row + col
            
            if col in used_cols or d_main in used_diag_main or d_anti in used_diag_anti:
                continue
            
            # Choose
            queen_cols[row] = col
            used_cols.add(col)
            used_diag_main.add(d_main)
            used_diag_anti.add(d_anti)
            
            # Explore
            backtrack(row + 1)
            
            # Unchoose
            used_cols.discard(col)
            used_diag_main.discard(d_main)
            used_diag_anti.discard(d_anti)
    
    backtrack(0)
    return results


def build_board(queen_cols: list[int], n: int) -> list[str]:
    return ['.' * c + 'Q' + '.' * (n - c - 1) for c in queen_cols]


def total_n_queens(n: int) -> int:
    """Count solutions without building boards."""
    count = 0
    cols, d_main, d_anti = set(), set(), set()
    
    def backtrack(row: int) -> None:
        nonlocal count
        if row == n:
            count += 1
            return
        for col in range(n):
            dm, da = row - col, row + col
            if col in cols or dm in d_main or da in d_anti:
                continue
            cols.add(col); d_main.add(dm); d_anti.add(da)
            backtrack(row + 1)
            cols.discard(col); d_main.discard(dm); d_anti.discard(da)
    
    backtrack(0)
    return count
```

### 9.10 Palindrome Partitioning (LeetCode 131)

**Shape**: Segmentation — cut into valid pieces.

**Recognition**: "Partition such that every substring is a palindrome."

**What to track**: Start position of next cut.

**Optimization**: Precompute palindrome status.

```python
def partition(s: str) -> list[list[str]]:
    results: list[list[str]] = []
    path: list[str] = []
    n = len(s)
    
    # Precompute: is_pal[i][j] = True if s[i:j+1] is palindrome
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i <= 2 or is_pal[i + 1][j - 1]):
                is_pal[i][j] = True
    
    def backtrack(start: int) -> None:
        if start == n:
            results.append(path[:])
            return
        
        for end in range(start, n):
            if not is_pal[start][end]:
                continue
            
            path.append(s[start:end + 1])
            backtrack(end + 1)
            path.pop()
    
    backtrack(0)
    return results
```

### 9.11 Restore IP Addresses (LeetCode 93)

**Shape**: Segmentation with multiple constraints.

**Recognition**: "Return all valid IP addresses from digit string."

**Constraints**: Exactly 4 segments, each 1-3 digits, value 0-255, no leading zeros.

```python
def restore_ip_addresses(s: str) -> list[str]:
    results: list[str] = []
    segments: list[str] = []
    n = len(s)
    
    def is_valid(seg: str) -> bool:
        if not seg or (len(seg) > 1 and seg[0] == '0'):
            return False
        return int(seg) <= 255
    
    def backtrack(start: int, count: int) -> None:
        remaining = n - start
        remaining_segs = 4 - count
        
        # Pruning: too few or too many characters left
        if remaining < remaining_segs or remaining > remaining_segs * 3:
            return
        
        if count == 4:
            if start == n:
                results.append('.'.join(segments))
            return
        
        for length in range(1, 4):
            if start + length > n:
                break
            seg = s[start:start + length]
            if not is_valid(seg):
                continue
            
            segments.append(seg)
            backtrack(start + length, count + 1)
            segments.pop()
    
    backtrack(0, 0)
    return results
```

### 9.12 Word Search (LeetCode 79)

**Shape**: Grid path with visited tracking.

**Recognition**: "Find if word exists by traversing adjacent cells."

**What to track**: Visited cells (in-place marking).

```python
def exist(board: list[list[str]], word: str) -> bool:
    if not board or not board[0]:
        return False
    
    rows, cols = len(board), len(board[0])
    
    def backtrack(r: int, c: int, idx: int) -> bool:
        if idx == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if board[r][c] != word[idx]:
            return False
        
        # Choose: mark as visited
        original = board[r][c]
        board[r][c] = '#'
        
        # Explore: try all 4 directions
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if backtrack(r + dr, c + dc, idx + 1):
                board[r][c] = original  # Restore before returning
                return True
        
        # Unchoose: unmark
        board[r][c] = original
        return False
    
    for r in range(rows):
        for c in range(cols):
            if backtrack(r, c, 0):
                return True
    return False
```

---

## 10. Quick Reference Templates

### Permutation Template

```python
def permutation_template(items):
    results, path, used = [], [], [False] * len(items)
    
    def backtrack():
        if len(path) == len(items):
            results.append(path[:])
            return
        for i in range(len(items)):
            if used[i]:
                continue
            used[i] = True
            path.append(items[i])
            backtrack()
            path.pop()
            used[i] = False
    
    backtrack()
    return results
```

### Subset/Combination Template

```python
def subset_template(items):
    results, path = [], []
    
    def backtrack(start):
        results.append(path[:])
        for i in range(start, len(items)):
            path.append(items[i])
            backtrack(i + 1)
            path.pop()
    
    backtrack(0)
    return results
```

### Target Sum Template

```python
def target_sum_template(candidates, target, allow_reuse=True):
    results, path = [], []
    candidates.sort()
    
    def backtrack(start, remaining):
        if remaining == 0:
            results.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break
            path.append(candidates[i])
            next_start = i if allow_reuse else i + 1
            backtrack(next_start, remaining - candidates[i])
            path.pop()
    
    backtrack(0, target)
    return results
```

### Grid Search Template

```python
def grid_search_template(grid, target):
    rows, cols = len(grid), len(grid[0])
    
    def backtrack(r, c, idx):
        if idx == len(target):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != target[idx]:
            return False
        
        temp, grid[r][c] = grid[r][c], '#'
        found = any(backtrack(r + dr, c + dc, idx + 1) 
                    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)])
        grid[r][c] = temp
        return found
    
    return any(backtrack(r, c, 0) for r in range(rows) for c in range(cols))
```

---

## Pattern Summary

| Shape | What to Track | How to Advance | Deduplication |
|-------|---------------|----------------|---------------|
| **Permutation** | `used[]` array | Try all unused | Sort + same-level skip |
| **Subset** | Start index | `i + 1` (forward only) | Sort + same-level skip |
| **Combination** | Start index + count | `i + 1` until count reached | Same as subset |
| **Target Sum** | Start index + remaining | `i` (reuse) or `i + 1` (no reuse) | Sort + same-level skip |
| **Constraint** | Forbidden sets | Row-by-row with checks | Built-in via constraints |
| **Segmentation** | Start position | Next segment start | Usually none needed |
| **Grid Path** | Visited marks | 4 directions | In-place marking |

---

## The Backtracking Mantra

> **Choose, Explore, Unchoose.**
> 
> Mark your path as you go.
> When you've gone as far as you can, walk back and erase your marks.
> The cave remains clean for the next path.

When you see a problem asking for *all* configurations, think of the cave.
Unroll the thread. Mark the junctions. Collect the treasures. Rewind. Repeat.

---

*Document generated for NeetCode Practice Framework — Pattern: BacktrackingExploration*

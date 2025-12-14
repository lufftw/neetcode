# Backtracking Exploration Patterns: Complete Reference

> **API Kernel**: `BacktrackingExploration`  
> **Core Mechanism**: Systematically explore all candidate solutions by building them incrementally, abandoning paths that violate constraints (pruning), and undoing choices to try alternatives.

This document presents the **canonical backtracking template** and all its major variations. Each implementation follows consistent naming conventions and includes detailed algorithmic explanations.

---

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Base Template: Permutations (LeetCode 46)](#2-base-template-permutations-leetcode-46)
3. [Variation: Permutations with Duplicates (LeetCode 47)](#3-variation-permutations-with-duplicates-leetcode-47)
4. [Variation: Subsets (LeetCode 78)](#4-variation-subsets-leetcode-78)
5. [Variation: Subsets with Duplicates (LeetCode 90)](#5-variation-subsets-with-duplicates-leetcode-90)
6. [Variation: Combinations (LeetCode 77)](#6-variation-combinations-leetcode-77)
7. [Variation: Combination Sum (LeetCode 39)](#7-variation-combination-sum-leetcode-39)
8. [Variation: Combination Sum II (LeetCode 40)](#8-variation-combination-sum-ii-leetcode-40)
9. [Variation: Combination Sum III (LeetCode 216)](#9-variation-combination-sum-iii-leetcode-216)
10. [Variation: N-Queens (LeetCode 51/52)](#10-variation-n-queens-leetcode-5152)
11. [Variation: Palindrome Partitioning (LeetCode 131)](#11-variation-palindrome-partitioning-leetcode-131)
12. [Variation: Restore IP Addresses (LeetCode 93)](#12-variation-restore-ip-addresses-leetcode-93)
13. [Variation: Word Search (LeetCode 79)](#13-variation-word-search-leetcode-79)
14. [Deduplication Strategies](#14-deduplication-strategies)
15. [Pruning Techniques](#15-pruning-techniques)
16. [Pattern Comparison Table](#16-pattern-comparison-table)
17. [When to Use Backtracking](#17-when-to-use-backtracking)
18. [Template Quick Reference](#18-template-quick-reference)

---

## 1. Core Concepts

### 1.1 What is Backtracking?

Backtracking is a **systematic trial-and-error** approach that incrementally builds candidates to the solutions and abandons a candidate ("backtracks") as soon as it determines that the candidate cannot lead to a valid solution.

```
Decision Tree Visualization:

                    []
           ┌────────┼────────┐
          [1]      [2]      [3]
        ┌──┴──┐   ┌──┴──┐   ┌──┴──┐
      [1,2] [1,3] [2,1] [2,3] [3,1] [3,2]
        │     │     │     │     │     │
     [1,2,3] ... (continue building)
        ↓
    SOLUTION FOUND → collect and backtrack
```

### 1.2 The Three-Step Pattern: Choose → Explore → Unchoose

Every backtracking algorithm follows this fundamental pattern:

```python
def backtrack(state, choices):
    """
    Core backtracking template.
    
    1. BASE CASE: Check if current state is a complete solution
    2. RECURSIVE CASE: For each available choice:
       a) CHOOSE: Make a choice and update state
       b) EXPLORE: Recursively explore with updated state
       c) UNCHOOSE: Undo the choice (backtrack)
    """
    # BASE CASE: Is this a complete solution?
    if is_solution(state):
        collect_solution(state)
        return
    
    # RECURSIVE CASE: Try each choice
    for choice in get_available_choices(state, choices):
        # CHOOSE: Make this choice
        apply_choice(state, choice)
        
        # EXPLORE: Recurse with updated state
        backtrack(state, remaining_choices(choices, choice))
        
        # UNCHOOSE: Undo the choice (restore state)
        undo_choice(state, choice)
```

### 1.3 Key Invariants

| Invariant | Description |
|-----------|-------------|
| **State Consistency** | After backtracking, state must be exactly as before the choice was made |
| **Exhaustive Exploration** | Every valid solution must be reachable through some path |
| **Pruning Soundness** | Pruned branches must not contain any valid solutions |
| **No Duplicates** | Each unique solution must be generated exactly once |

### 1.4 Time Complexity Discussion

Backtracking algorithms typically have exponential or factorial complexity because they explore the entire solution space:

| Problem Type | Typical Complexity | Output Size |
|--------------|-------------------|-------------|
| Permutations | O(n! × n) | n! |
| Subsets | O(2^n × n) | 2^n |
| Combinations C(n,k) | O(C(n,k) × k) | C(n,k) |
| N-Queens | O(n!) | variable |

**Important**: The complexity is often **output-sensitive** — if there are many solutions, generating them all is inherently expensive.

### 1.5 Sub-Pattern Classification

| Sub-Pattern | Key Characteristic | Examples |
|-------------|-------------------|----------|
| **Permutation** | Used/visited tracking | LeetCode 46, 47 |
| **Subset/Combination** | Start-index canonicalization | LeetCode 78, 90, 77 |
| **Target Search** | Remaining/target pruning | LeetCode 39, 40, 216 |
| **Constraint Satisfaction** | Row-by-row with constraint sets | LeetCode 51, 52 |
| **String Partitioning** | Cut positions with validity | LeetCode 131, 93 |
| **Grid/Path Search** | Visited marking and undo | LeetCode 79 |

---

## 2. Base Template: Permutations (LeetCode 46)

> **Problem**: Given an array of distinct integers, return all possible permutations.  
> **Sub-Pattern**: Permutation Enumeration with used tracking.  
> **Key Insight**: At each position, try all unused elements.

### 2.1 Implementation

```python
def permute(nums: list[int]) -> list[list[int]]:
    """
    Generate all permutations of distinct integers.
    
    Algorithm:
    - Build permutation position by position
    - Track which elements have been used with a boolean array
    - At each position, try every unused element
    - When path length equals nums length, we have a complete permutation
    
    Time Complexity: O(n! × n)
        - n! permutations to generate
        - O(n) to copy each permutation
    
    Space Complexity: O(n)
        - Recursion depth is n
        - Used array is O(n)
        - Output space not counted
    
    Args:
        nums: Array of distinct integers
        
    Returns:
        All possible permutations
    """
    results: list[list[int]] = []
    n = len(nums)
    
    # State: Current permutation being built
    path: list[int] = []
    
    # Tracking: Which elements are already used in current path
    used: list[bool] = [False] * n
    
    def backtrack() -> None:
        # BASE CASE: Permutation is complete
        if len(path) == n:
            results.append(path[:])  # Append a copy
            return
        
        # RECURSIVE CASE: Try each unused element
        for i in range(n):
            if used[i]:
                continue  # Skip already used elements
            
            # CHOOSE: Add element to permutation
            path.append(nums[i])
            used[i] = True
            
            # EXPLORE: Recurse to fill next position
            backtrack()
            
            # UNCHOOSE: Remove element (backtrack)
            path.pop()
            used[i] = False
    
    backtrack()
    return results
```

### 2.2 Why This Works

The `used` array ensures each element appears exactly once in each permutation. The decision tree has:
- Level 0: n choices
- Level 1: n-1 choices  
- Level k: n-k choices
- Total leaves: n!

### 2.3 Trace Example

```
Input: [1, 2, 3]

backtrack(path=[], used=[F,F,F])
├─ CHOOSE 1 → backtrack(path=[1], used=[T,F,F])
│  ├─ CHOOSE 2 → backtrack(path=[1,2], used=[T,T,F])
│  │  └─ CHOOSE 3 → backtrack(path=[1,2,3], used=[T,T,T])
│  │                 → SOLUTION: [1,2,3]
│  └─ CHOOSE 3 → backtrack(path=[1,3], used=[T,F,T])
│     └─ CHOOSE 2 → backtrack(path=[1,3,2], used=[T,T,T])
│                    → SOLUTION: [1,3,2]
├─ CHOOSE 2 → ... → [2,1,3], [2,3,1]
└─ CHOOSE 3 → ... → [3,1,2], [3,2,1]

Output: [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
```

### 2.4 Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Forgetting to copy | All results point to same list | Use `path[:]` or `list(path)` |
| Not unmarking used | Elements appear multiple times | Always set `used[i] = False` after recursion |
| Modifying during iteration | Concurrent modification errors | Iterate over indices, not elements |

---

## 3. Variation: Permutations with Duplicates (LeetCode 47)

> **Problem**: Given an array with duplicate integers, return all unique permutations.  
> **Delta from Base**: Add same-level deduplication after sorting.  
> **Key Insight**: Skip duplicate elements at the same tree level.

### 3.1 Implementation

```python
def permute_unique(nums: list[int]) -> list[list[int]]:
    """
    Generate all unique permutations of integers that may contain duplicates.
    
    Algorithm:
    - Sort the array to bring duplicates together
    - Use same-level deduplication: skip a duplicate if its previous
      occurrence wasn't used (meaning we're at the same decision level)
    
    Deduplication Rule:
    - If nums[i] == nums[i-1] and used[i-1] == False, skip nums[i]
    - This ensures we only use the first occurrence of a duplicate
      at each level of the decision tree
    
    Time Complexity: O(n! × n) in worst case (all unique)
    Space Complexity: O(n)
    
    Args:
        nums: Array of integers (may contain duplicates)
        
    Returns:
        All unique permutations
    """
    results: list[list[int]] = []
    n = len(nums)
    
    # CRITICAL: Sort to bring duplicates together
    nums.sort()
    
    path: list[int] = []
    used: list[bool] = [False] * n
    
    def backtrack() -> None:
        if len(path) == n:
            results.append(path[:])
            return
        
        for i in range(n):
            if used[i]:
                continue
            
            # DEDUPLICATION: Skip duplicates at the same tree level
            # Condition: Current equals previous AND previous is unused
            # (unused previous means we're trying duplicate at same level)
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

### 3.2 Deduplication Logic Explained

```
Input: [1, 1, 2] (sorted)
Indices: [0, 1, 2]

Without deduplication, we'd get:
- Path using indices [0,1,2] → [1,1,2]
- Path using indices [1,0,2] → [1,1,2]  ← DUPLICATE!

With deduplication (skip if nums[i]==nums[i-1] and !used[i-1]):
- When i=1 and used[0]=False: skip (same level, use i=0 first)
- When i=1 and used[0]=True: proceed (different subtree)

This ensures we always pick the leftmost duplicate first at each level.
```

---

## 4. Variation: Subsets (LeetCode 78)

> **Problem**: Given an array of distinct integers, return all possible subsets.  
> **Sub-Pattern**: Subset enumeration with start-index canonicalization.  
> **Key Insight**: Use a start index to avoid revisiting previous elements.

### 4.1 Implementation

```python
def subsets(nums: list[int]) -> list[list[int]]:
    """
    Generate all subsets (power set) of distinct integers.
    
    Algorithm:
    - Each subset is a collection of elements with no ordering
    - To avoid duplicates like {1,2} and {2,1}, enforce canonical ordering
    - Use start_index to only consider elements at or after current position
    - Every intermediate path is a valid subset (collect at every node)
    
    Key Insight:
    - Unlike permutations, subsets don't need a "used" array
    - The start_index inherently prevents revisiting previous elements
    
    Time Complexity: O(n × 2^n)
        - 2^n subsets to generate
        - O(n) to copy each subset
    
    Space Complexity: O(n) for recursion depth
    
    Args:
        nums: Array of distinct integers
        
    Returns:
        All possible subsets
    """
    results: list[list[int]] = []
    n = len(nums)
    path: list[int] = []
    
    def backtrack(start_index: int) -> None:
        # COLLECT: Every path (including empty) is a valid subset
        results.append(path[:])
        
        # EXPLORE: Only consider elements from start_index onwards
        for i in range(start_index, n):
            # CHOOSE
            path.append(nums[i])
            
            # EXPLORE: Move start_index forward to enforce ordering
            backtrack(i + 1)
            
            # UNCHOOSE
            path.pop()
    
    backtrack(0)
    return results
```

### 4.2 Why Start Index Works

```
Input: [1, 2, 3]

Decision tree with start_index:
[]                         ← start=0, collect []
├─ [1]                     ← start=1, collect [1]
│  ├─ [1,2]                ← start=2, collect [1,2]
│  │  └─ [1,2,3]           ← start=3, collect [1,2,3]
│  └─ [1,3]                ← start=3, collect [1,3]
├─ [2]                     ← start=2, collect [2]
│  └─ [2,3]                ← start=3, collect [2,3]
└─ [3]                     ← start=3, collect [3]

Total: 8 subsets = 2^3 ✓
```

The start_index ensures:
- We never pick element i after already having an element j > i
- This enforces a canonical ordering (ascending by index)
- Each subset is generated exactly once

---

## 5. Variation: Subsets with Duplicates (LeetCode 90)

> **Problem**: Given an array with duplicates, return all unique subsets.  
> **Delta from Subsets**: Sort + same-level deduplication.  
> **Key Insight**: Skip duplicate values at the same recursion level.

### 5.1 Implementation

```python
def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    """
    Generate all unique subsets from integers that may contain duplicates.
    
    Algorithm:
    - Sort to bring duplicates together
    - Use same-level deduplication: skip if current equals previous
      in the same iteration loop
    
    Deduplication Condition:
    - Skip nums[i] if i > start_index AND nums[i] == nums[i-1]
    - This prevents choosing the same value twice at the same tree level
    
    Time Complexity: O(n × 2^n) worst case
    Space Complexity: O(n)
    
    Args:
        nums: Array of integers (may contain duplicates)
        
    Returns:
        All unique subsets
    """
    results: list[list[int]] = []
    n = len(nums)
    
    # CRITICAL: Sort to bring duplicates together
    nums.sort()
    
    path: list[int] = []
    
    def backtrack(start_index: int) -> None:
        results.append(path[:])
        
        for i in range(start_index, n):
            # DEDUPLICATION: Skip duplicates at same level
            # i > start_index ensures we're not skipping the first occurrence
            if i > start_index and nums[i] == nums[i - 1]:
                continue
            
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()
    
    backtrack(0)
    return results
```

### 5.2 Deduplication Visualization

```
Input: [1, 2, 2] (sorted)

Without deduplication:
[]
├─ [1] → [1,2] → [1,2,2]
│      → [1,2]  ← choosing second 2
├─ [2] → [2,2]
└─ [2]  ← DUPLICATE of above!

With deduplication (skip if i > start and nums[i] == nums[i-1]):
[]
├─ [1] → [1,2] → [1,2,2]
│                        ↑ i=2, start=2, 2==2 but i==start, proceed
│      → [1,2]  skipped (i=2 > start=1, 2==2)
├─ [2] → [2,2]
└─ skip (i=2 > start=0, 2==2)

Result: [[], [1], [1,2], [1,2,2], [2], [2,2]]
```

---

## 6. Variation: Combinations (LeetCode 77)

> **Problem**: Given n and k, return all combinations of k numbers from [1..n].  
> **Sub-Pattern**: Fixed-size subset enumeration.  
> **Delta from Subsets**: Only collect when path length equals k.

### 6.1 Implementation

```python
def combine(n: int, k: int) -> list[list[int]]:
    """
    Generate all combinations of k numbers from range [1, n].
    
    Algorithm:
    - Similar to subsets, but only collect when path has exactly k elements
    - Use start_index to enforce canonical ordering
    - Add pruning: stop early if remaining elements can't fill path to k
    
    Pruning Optimization:
    - If we need (k - len(path)) more elements, we need at least that many
      elements remaining in [i, n]
    - Elements remaining = n - i + 1
    - Prune when: n - i + 1 < k - len(path)
    - Equivalently: stop loop when i > n - (k - len(path)) + 1
    
    Time Complexity: O(k × C(n,k))
    Space Complexity: O(k)
    
    Args:
        n: Range upper bound [1..n]
        k: Size of each combination
        
    Returns:
        All combinations of k numbers from [1..n]
    """
    results: list[list[int]] = []
    path: list[int] = []
    
    def backtrack(start: int) -> None:
        # BASE CASE: Combination is complete
        if len(path) == k:
            results.append(path[:])
            return
        
        # PRUNING: Calculate upper bound for current loop
        # We need (k - len(path)) more elements
        # Available elements from start to n is (n - start + 1)
        # Stop when available < needed
        need = k - len(path)
        
        for i in range(start, n - need + 2):  # n - need + 1 + 1 for range
            path.append(i)
            backtrack(i + 1)
            path.pop()
    
    backtrack(1)
    return results
```

### 6.2 Pruning Analysis

```
n=4, k=2

Without pruning:
start=1: try 1,2,3,4
  start=2: try 2,3,4
  start=3: try 3,4
  start=4: try 4     ← only 1 element left, need 1 more → works
  start=5: empty     ← wasted call

With pruning (need=2, loop until n-need+2=4):
start=1: try 1,2,3 (not 4, because 4→[] would fail)
  ...

This eliminates branches that can't possibly lead to valid combinations.
```

---

## 7. Variation: Combination Sum (LeetCode 39)

> **Problem**: Find combinations that sum to target. Elements can be reused.  
> **Sub-Pattern**: Target search with element reuse.  
> **Key Insight**: Don't increment start_index when allowing reuse.

### 7.1 Implementation

```python
def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    """
    Find all combinations that sum to target. Each number can be used unlimited times.
    
    Algorithm:
    - Track remaining target (target - current sum)
    - When remaining = 0, found a valid combination
    - Allow reuse by NOT incrementing start_index when recursing
    - Prune when remaining < 0 (overshot target)
    
    Key Difference from Combinations:
    - Reuse allowed: recurse with same index i, not i+1
    - This means we can pick the same element multiple times
    
    Time Complexity: O(n^(t/m)) where t=target, m=min(candidates)
        - Branching factor up to n at each level
        - Depth up to t/m (using smallest element repeatedly)
    
    Space Complexity: O(t/m) for recursion depth
    
    Args:
        candidates: Array of distinct positive integers
        target: Target sum
        
    Returns:
        All unique combinations that sum to target
    """
    results: list[list[int]] = []
    path: list[int] = []
    
    # Optional: Sort for consistent output order
    candidates.sort()
    
    def backtrack(start_index: int, remaining: int) -> None:
        # BASE CASE: Found valid combination
        if remaining == 0:
            results.append(path[:])
            return
        
        # PRUNING: Overshot target
        if remaining < 0:
            return
        
        for i in range(start_index, len(candidates)):
            # PRUNING: If current candidate exceeds remaining, 
            # all subsequent (if sorted) will too
            if candidates[i] > remaining:
                break
            
            path.append(candidates[i])
            
            # REUSE ALLOWED: Recurse with same index i
            backtrack(i, remaining - candidates[i])
            
            path.pop()
    
    backtrack(0, target)
    return results
```

### 7.2 Reuse vs No-Reuse Comparison

| Aspect | With Reuse (LC 39) | Without Reuse (LC 40) |
|--------|-------------------|----------------------|
| Recurse with | `backtrack(i, ...)` | `backtrack(i+1, ...)` |
| Same element | Can appear multiple times | Can appear at most once |
| Deduplication | Not needed (distinct) | Needed (may have duplicates) |

---

## 8. Variation: Combination Sum II (LeetCode 40)

> **Problem**: Find combinations that sum to target. Each element used at most once. Input may have duplicates.  
> **Delta from Combination Sum**: No reuse + duplicate handling.  
> **Key Insight**: Sort + same-level skip for duplicates.

### 8.1 Implementation

```python
def combination_sum2(candidates: list[int], target: int) -> list[list[int]]:
    """
    Find all unique combinations that sum to target. Each number used at most once.
    Input may contain duplicates.
    
    Algorithm:
    - Sort to bring duplicates together
    - Use start_index to prevent reuse (i+1 when recursing)
    - Same-level deduplication: skip if current == previous at same level
    
    Deduplication Rule:
    - Skip candidates[i] if i > start_index AND candidates[i] == candidates[i-1]
    - This prevents generating duplicate combinations
    
    Time Complexity: O(2^n) worst case
    Space Complexity: O(n)
    
    Args:
        candidates: Array of positive integers (may have duplicates)
        target: Target sum
        
    Returns:
        All unique combinations summing to target
    """
    results: list[list[int]] = []
    path: list[int] = []
    
    # CRITICAL: Sort for deduplication
    candidates.sort()
    
    def backtrack(start_index: int, remaining: int) -> None:
        if remaining == 0:
            results.append(path[:])
            return
        
        if remaining < 0:
            return
        
        for i in range(start_index, len(candidates)):
            # DEDUPLICATION: Skip same value at same level
            if i > start_index and candidates[i] == candidates[i - 1]:
                continue
            
            # PRUNING: Current exceeds remaining (sorted, so break)
            if candidates[i] > remaining:
                break
            
            path.append(candidates[i])
            
            # NO REUSE: Recurse with i+1
            backtrack(i + 1, remaining - candidates[i])
            
            path.pop()
    
    backtrack(0, target)
    return results
```

---

## 9. Variation: Combination Sum III (LeetCode 216)

> **Problem**: Find k numbers from [1-9] that sum to n. Each number used at most once.  
> **Delta from Combination Sum II**: Fixed count k + bounded range [1-9].  
> **Key Insight**: Dual constraint — both count and sum must be satisfied.

### 9.1 Implementation

```python
def combination_sum3(k: int, n: int) -> list[list[int]]:
    """
    Find all combinations of k numbers from [1-9] that sum to n.
    
    Algorithm:
    - Fixed size k (must have exactly k numbers)
    - Fixed sum n (must sum to exactly n)
    - Range is [1-9], all distinct, no reuse
    
    Pruning Strategies:
    1. If current sum exceeds n, stop
    2. If path length exceeds k, stop
    3. If remaining numbers can't fill to k, stop
    
    Time Complexity: O(C(9,k) × k)
    Space Complexity: O(k)
    
    Args:
        k: Number of elements required
        n: Target sum
        
    Returns:
        All valid combinations
    """
    results: list[list[int]] = []
    path: list[int] = []
    
    def backtrack(start: int, remaining: int) -> None:
        # BASE CASE: Have k numbers
        if len(path) == k:
            if remaining == 0:
                results.append(path[:])
            return
        
        # PRUNING: Not enough numbers left to fill path
        if 9 - start + 1 < k - len(path):
            return
        
        for i in range(start, 10):
            # PRUNING: Current number too large
            if i > remaining:
                break
            
            path.append(i)
            backtrack(i + 1, remaining - i)
            path.pop()
    
    backtrack(1, n)
    return results
```

---

## 10. Variation: N-Queens (LeetCode 51/52)

> **Problem**: Place n queens on an n×n board so no two queens attack each other.  
> **Sub-Pattern**: Constraint satisfaction with row-by-row placement.  
> **Key Insight**: Track columns and diagonals as constraint sets.

### 10.1 Implementation

```python
def solve_n_queens(n: int) -> list[list[str]]:
    """
    Find all solutions to the N-Queens puzzle.
    
    Algorithm:
    - Place queens row by row (one queen per row guaranteed)
    - Track three constraints:
      1. Columns: No two queens in same column
      2. Main diagonals (↘): row - col is constant
      3. Anti-diagonals (↙): row + col is constant
    - Use hash sets for O(1) constraint checking
    
    Key Insight:
    - Row-by-row placement eliminates row conflicts by construction
    - Only need to check column and diagonal conflicts
    
    Time Complexity: O(n!)
        - At row 0: n choices
        - At row 1: at most n-1 choices
        - ... and so on
    
    Space Complexity: O(n) for constraint sets and recursion
    
    Args:
        n: Board size
        
    Returns:
        All valid board configurations as string arrays
    """
    results: list[list[str]] = []
    
    # State: queen_cols[row] = column where queen is placed
    queen_cols: list[int] = [-1] * n
    
    # Constraint sets for O(1) conflict checking
    used_cols: set[int] = set()
    used_diag_main: set[int] = set()   # row - col
    used_diag_anti: set[int] = set()   # row + col
    
    def backtrack(row: int) -> None:
        # BASE CASE: All queens placed
        if row == n:
            results.append(build_board(queen_cols, n))
            return
        
        # Try each column in current row
        for col in range(n):
            # Calculate diagonal identifiers
            diag_main = row - col
            diag_anti = row + col
            
            # CONSTRAINT CHECK (pruning)
            if col in used_cols:
                continue
            if diag_main in used_diag_main:
                continue
            if diag_anti in used_diag_anti:
                continue
            
            # CHOOSE: Place queen
            queen_cols[row] = col
            used_cols.add(col)
            used_diag_main.add(diag_main)
            used_diag_anti.add(diag_anti)
            
            # EXPLORE: Move to next row
            backtrack(row + 1)
            
            # UNCHOOSE: Remove queen
            queen_cols[row] = -1
            used_cols.discard(col)
            used_diag_main.discard(diag_main)
            used_diag_anti.discard(diag_anti)
    
    backtrack(0)
    return results


def build_board(queen_cols: list[int], n: int) -> list[str]:
    """Convert queen positions to board representation."""
    board = []
    for col in queen_cols:
        row = '.' * col + 'Q' + '.' * (n - col - 1)
        board.append(row)
    return board
```

### 10.2 Diagonal Identification

```
Main diagonal (↘): cells where row - col is constant
    (0,0) (1,1) (2,2) → row - col = 0
    (0,1) (1,2) (2,3) → row - col = -1
    (1,0) (2,1) (3,2) → row - col = 1

Anti-diagonal (↙): cells where row + col is constant
    (0,2) (1,1) (2,0) → row + col = 2
    (0,3) (1,2) (2,1) (3,0) → row + col = 3
```

### 10.3 N-Queens II (Count Only)

```python
def total_n_queens(n: int) -> int:
    """Count solutions without building boards."""
    count = 0
    
    used_cols: set[int] = set()
    used_diag_main: set[int] = set()
    used_diag_anti: set[int] = set()
    
    def backtrack(row: int) -> None:
        nonlocal count
        if row == n:
            count += 1
            return
        
        for col in range(n):
            dm, da = row - col, row + col
            if col in used_cols or dm in used_diag_main or da in used_diag_anti:
                continue
            
            used_cols.add(col)
            used_diag_main.add(dm)
            used_diag_anti.add(da)
            
            backtrack(row + 1)
            
            used_cols.discard(col)
            used_diag_main.discard(dm)
            used_diag_anti.discard(da)
    
    backtrack(0)
    return count
```

---

## 11. Variation: Palindrome Partitioning (LeetCode 131)

> **Problem**: Partition a string such that every substring is a palindrome.  
> **Sub-Pattern**: String segmentation with validity check.  
> **Key Insight**: Try all cut positions, validate each segment.

### 11.1 Implementation

```python
def partition(s: str) -> list[list[str]]:
    """
    Partition string so every part is a palindrome.
    
    Algorithm:
    - Try cutting at each position from current start
    - Check if prefix is palindrome; if yes, recurse on suffix
    - When start reaches end of string, we have a valid partition
    
    Key Insight:
    - Each "choice" is where to cut the string
    - Only proceed if the cut-off prefix is a palindrome
    
    Optimization:
    - Precompute palindrome status with DP for O(1) checks
    - Without precompute: O(n) per check, O(n^3) total
    - With precompute: O(n^2) preprocessing, O(1) per check
    
    Time Complexity: O(n × 2^n) worst case
        - 2^(n-1) possible partitions (n-1 cut positions)
        - O(n) to copy each partition
    
    Space Complexity: O(n) for recursion
    
    Args:
        s: Input string
        
    Returns:
        All palindrome partitionings
    """
    results: list[list[str]] = []
    path: list[str] = []
    n = len(s)
    
    # Precompute: is_palindrome[i][j] = True if s[i:j+1] is palindrome
    is_palindrome = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j]:
                if j - i <= 2:
                    is_palindrome[i][j] = True
                else:
                    is_palindrome[i][j] = is_palindrome[i + 1][j - 1]
    
    def backtrack(start: int) -> None:
        # BASE CASE: Reached end of string
        if start == n:
            results.append(path[:])
            return
        
        # Try each end position for current segment
        for end in range(start, n):
            # VALIDITY CHECK: Only proceed if palindrome
            if not is_palindrome[start][end]:
                continue
            
            path.append(s[start:end + 1])
            backtrack(end + 1)
            path.pop()
    
    backtrack(0)
    return results
```

---

## 12. Variation: Restore IP Addresses (LeetCode 93)

> **Problem**: Return all valid IP addresses that can be formed from a digit string.  
> **Sub-Pattern**: String segmentation with multi-constraint validity.  
> **Key Insight**: Fixed 4 segments, each 1-3 digits, value 0-255, no leading zeros.

### 12.1 Implementation

```python
def restore_ip_addresses(s: str) -> list[str]:
    """
    Generate all valid IP addresses from a digit string.
    
    Constraints per segment:
    1. Length: 1-3 characters
    2. Value: 0-255
    3. No leading zeros (except "0" itself)
    
    Algorithm:
    - Exactly 4 segments required
    - Try 1, 2, or 3 characters for each segment
    - Validate each segment before proceeding
    
    Pruning:
    - Early termination if remaining chars can't form remaining segments
    - Min remaining = segments_left × 1
    - Max remaining = segments_left × 3
    
    Time Complexity: O(3^4 × n) = O(81 × n) = O(n)
        - At most 3 choices per segment, 4 segments
        - O(n) to validate/copy
    
    Space Complexity: O(4) = O(1) for path
    
    Args:
        s: String of digits
        
    Returns:
        All valid IP addresses
    """
    results: list[str] = []
    segments: list[str] = []
    n = len(s)
    
    def is_valid_segment(segment: str) -> bool:
        """Check if segment is a valid IP octet."""
        if not segment:
            return False
        if len(segment) > 1 and segment[0] == '0':
            return False  # No leading zeros
        if int(segment) > 255:
            return False
        return True
    
    def backtrack(start: int, segment_count: int) -> None:
        # PRUNING: Check remaining length bounds
        remaining = n - start
        remaining_segments = 4 - segment_count
        
        if remaining < remaining_segments:  # Too few chars
            return
        if remaining > remaining_segments * 3:  # Too many chars
            return
        
        # BASE CASE: 4 segments formed
        if segment_count == 4:
            if start == n:  # Used all characters
                results.append('.'.join(segments))
            return
        
        # Try 1, 2, or 3 character segments
        for length in range(1, 4):
            if start + length > n:
                break
            
            segment = s[start:start + length]
            
            if not is_valid_segment(segment):
                continue
            
            segments.append(segment)
            backtrack(start + length, segment_count + 1)
            segments.pop()
    
    backtrack(0, 0)
    return results
```

---

## 13. Variation: Word Search (LeetCode 79)

> **Problem**: Find if a word exists in a grid by traversing adjacent cells.  
> **Sub-Pattern**: Grid/Path DFS with visited marking.  
> **Key Insight**: Mark visited, explore neighbors, unmark on backtrack.

### 13.1 Implementation

```python
def exist(board: list[list[str]], word: str) -> bool:
    """
    Check if word exists in grid by traversing adjacent cells.
    
    Algorithm:
    - Start DFS from each cell that matches word[0]
    - Mark current cell as visited (modify in-place or use set)
    - Try all 4 directions for next character
    - Unmark on backtrack
    
    Key Insight:
    - Each cell can be used at most once per path
    - In-place marking (temporary modification) is efficient
    
    Pruning:
    - Early return on mismatch
    - Can add frequency check: if board doesn't have enough of each char
    
    Time Complexity: O(m × n × 4^L) where L = len(word)
        - m×n starting positions
        - 4 choices at each step, depth L
    
    Space Complexity: O(L) for recursion depth
    
    Args:
        board: 2D character grid
        word: Target word to find
        
    Returns:
        True if word can be formed
    """
    if not board or not board[0]:
        return False
    
    rows, cols = len(board), len(board[0])
    word_len = len(word)
    
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    def backtrack(row: int, col: int, index: int) -> bool:
        # BASE CASE: All characters matched
        if index == word_len:
            return True
        
        # BOUNDARY CHECK
        if row < 0 or row >= rows or col < 0 or col >= cols:
            return False
        
        # CHARACTER CHECK
        if board[row][col] != word[index]:
            return False
        
        # MARK AS VISITED (in-place modification)
        original = board[row][col]
        board[row][col] = '#'  # Temporary marker
        
        # EXPLORE: Try all 4 directions
        for dr, dc in directions:
            if backtrack(row + dr, col + dc, index + 1):
                # Found! Restore and return
                board[row][col] = original
                return True
        
        # UNMARK (backtrack)
        board[row][col] = original
        return False
    
    # Try starting from each cell
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == word[0]:
                if backtrack(r, c, 0):
                    return True
    
    return False
```

### 13.2 In-Place Marking vs Visited Set

| Approach | Pros | Cons |
|----------|------|------|
| In-place (`#`) | O(1) space, fast | Modifies input temporarily |
| Visited set | Clean, no mutation | O(L) space for coordinates |

---

## 14. Deduplication Strategies

### 14.1 Strategy Comparison

| Strategy | When to Use | Example |
|----------|-------------|---------|
| **Sorting + Same-Level Skip** | Input has duplicates | Permutations II, Subsets II |
| **Start Index** | Subsets/Combinations (order doesn't matter) | Subsets, Combinations |
| **Used Array** | Permutations (all elements, order matters) | Permutations |
| **Canonical Ordering** | Implicit via index ordering | All subset-like problems |

### 14.2 Same-Level Skip Pattern

```python
# Sort first, then skip duplicates at same level
nums.sort()

for i in range(start, n):
    # Skip if current equals previous at same tree level
    if i > start and nums[i] == nums[i - 1]:
        continue
    # ... process nums[i]
```

### 14.3 Used Array Pattern

```python
# For permutations with duplicates
if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
    continue
# This ensures we use duplicates in order (leftmost first)
```

---

## 15. Pruning Techniques

### 15.1 Pruning Categories

| Category | Description | Example |
|----------|-------------|---------|
| **Feasibility Bound** | Remaining elements can't satisfy constraints | Combinations: not enough elements left |
| **Target Bound** | Current path already exceeds target | Combination Sum: sum > target |
| **Constraint Propagation** | Future choices are forced/impossible | N-Queens: no valid columns left |
| **Sorted Early Exit** | If sorted, larger elements also fail | Combination Sum with sorted candidates |

### 15.2 Pruning Patterns

```python
# 1. Not enough elements left (Combinations)
if remaining_elements < elements_needed:
    return

# 2. Exceeded target (Combination Sum)
if current_sum > target:
    return

# 3. Sorted early break (when candidates sorted)
if candidates[i] > remaining:
    break  # All subsequent are larger

# 4. Length/count bound
if len(path) > max_allowed:
    return
```

---

## 16. Pattern Comparison Table

| Problem | Sub-Pattern | State | Dedup Strategy | Pruning |
|---------|-------------|-------|----------------|---------|
| Permutations (46) | Permutation | used[] | None (distinct) | None |
| Permutations II (47) | Permutation | used[] | Sort + level skip | Same-level |
| Subsets (78) | Subset | start_idx | Index ordering | None |
| Subsets II (90) | Subset | start_idx | Sort + level skip | Same-level |
| Combinations (77) | Combination | start_idx | Index ordering | Count bound |
| Combination Sum (39) | Target Search | start_idx | None (distinct) | Target bound |
| Combination Sum II (40) | Target Search | start_idx | Sort + level skip | Target + level |
| Combination Sum III (216) | Target Search | start_idx | None (1-9 distinct) | Count + target |
| N-Queens (51) | Constraint | constraint sets | Row-by-row | Constraints |
| Palindrome Part. (131) | Segmentation | start_idx | None | Validity check |
| IP Addresses (93) | Segmentation | start_idx, count | None | Length bounds |
| Word Search (79) | Grid Path | visited | Path uniqueness | Boundary + char |

---

## 17. When to Use Backtracking

### 17.1 Problem Indicators

✅ **Use backtracking when:**
- Need to enumerate all solutions (permutations, combinations, etc.)
- Decision tree structure (sequence of choices)
- Constraints can be checked incrementally
- Solution can be built piece by piece

❌ **Consider alternatives when:**
- Only need count (use DP with counting)
- Only need one solution (may use greedy or simple DFS)
- Optimization problem (consider DP or greedy)
- State space is too large even with pruning

### 17.2 Decision Guide

```
Is the problem asking for ALL solutions?
├── Yes → Does solution have natural ordering/structure?
│         ├── Permutation → Use used[] array
│         ├── Subset/Combination → Use start_index
│         ├── Grid path → Use visited marking
│         └── Constraint satisfaction → Use constraint sets
└── No → Need single solution or count?
         ├── Single solution → Simple DFS may suffice
         └── Count → Consider DP
```

---

## 18. Template Quick Reference

### 18.1 Permutation Template

```python
def permute(nums):
    results = []
    used = [False] * len(nums)
    
    def backtrack(path):
        if len(path) == len(nums):
            results.append(path[:])
            return
        
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            used[i] = False
    
    backtrack([])
    return results
```

### 18.2 Subset/Combination Template

```python
def subsets(nums):
    results = []
    
    def backtrack(start, path):
        results.append(path[:])  # Collect at every node
        
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)  # i+1 for no reuse
            path.pop()
    
    backtrack(0, [])
    return results
```

### 18.3 Target Sum Template

```python
def combination_sum(candidates, target):
    results = []
    
    def backtrack(start, path, remaining):
        if remaining == 0:
            results.append(path[:])
            return
        if remaining < 0:
            return
        
        for i in range(start, len(candidates)):
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])  # i for reuse
            path.pop()
    
    backtrack(0, [], target)
    return results
```

### 18.4 Grid Search Template

```python
def grid_search(grid, word):
    rows, cols = len(grid), len(grid[0])
    
    def backtrack(r, c, index):
        if index == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if grid[r][c] != word[index]:
            return False
        
        temp = grid[r][c]
        grid[r][c] = '#'
        
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            if backtrack(r + dr, c + dc, index + 1):
                grid[r][c] = temp
                return True
        
        grid[r][c] = temp
        return False
    
    for r in range(rows):
        for c in range(cols):
            if backtrack(r, c, 0):
                return True
    return False
```

---

## LeetCode Problem Mapping

| Sub-Pattern | Problems |
|-------------|----------|
| **Permutation Enumeration** | 46. Permutations, 47. Permutations II |
| **Subset/Combination** | 78. Subsets, 90. Subsets II, 77. Combinations |
| **Target Search** | 39. Combination Sum, 40. Combination Sum II, 216. Combination Sum III |
| **Constraint Satisfaction** | 51. N-Queens, 52. N-Queens II, 37. Sudoku Solver |
| **String Partitioning** | 131. Palindrome Partitioning, 93. Restore IP Addresses, 140. Word Break II |
| **Grid/Path Search** | 79. Word Search, 212. Word Search II |

---

*Document generated for NeetCode Practice Framework — API Kernel: BacktrackingExploration*


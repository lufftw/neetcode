# Backtracking Exploration Patterns: Complete Reference

> **API Kernel**: `BacktrackingExploration`  
> **Core Mechanism**: Systematically explore all candidate solutions by building them incrementally, abandoning paths that violate constraints (pruning), and undoing choices to try alternatives.

This document presents the **canonical backtracking template** and all its major variations. Each implementation follows consistent naming conventions and includes detailed algorithmic explanations.

---

## Table of Contents

1. [Core Concepts](#1-core-concepts)
2. [Template Quick Reference](#2-template-quick-reference)

---

## 1. Core Concepts

### 1.1 The Backtracking Process

Backtracking is a systematic search technique that builds solutions incrementally and abandons partial solutions that cannot lead to valid complete solutions.

```
Backtracking State:
┌─────────────────────────────────────────────────────────┐
│  [choice₁] → [choice₂] → [choice₃] → ... → [choiceₙ]  │
│     │           │           │              │            │
│     └───────────┴───────────┴──────────────┘            │
│              Path (current partial solution)            │
│                                                          │
│  When constraint violated:                               │
│     Backtrack: undo last choice, try next alternative   │
└─────────────────────────────────────────────────────────┘
```

### 1.2 Universal Template Structure

```python
def backtracking_template(problem_state):
    """
    Generic backtracking template.
    
    Key components:
    1. Base Case: Check if current path is a complete solution
    2. Pruning: Abandon paths that violate constraints
    3. Choices: Generate all valid choices at current state
    4. Make Choice: Add choice to path, update state
    5. Recurse: Explore further with updated state
    6. Backtrack: Undo choice, restore state
    """
    results = []
    
    def backtrack(path, state):
        # BASE CASE: Check if solution is complete
        if is_complete(path, state):
            results.append(path[:])  # Copy path
            return
        
        # PRUNING: Abandon invalid paths early
        if violates_constraints(path, state):
            return
        
        # CHOICES: Generate all valid choices
        for choice in generate_choices(path, state):
            # MAKE CHOICE: Add to path, update state
            path.append(choice)
            update_state(state, choice)
            
            # RECURSE: Explore further
            backtrack(path, state)
            
            # BACKTRACK: Undo choice, restore state
            path.pop()
            restore_state(state, choice)
    
    backtrack([], initial_state)
    return results
```

### 1.3 Backtracking Family Overview

| Sub-Pattern | Key Characteristic | Primary Use Case |
|-------------|-------------------|------------------|
| **Permutation** | All elements used, order matters | Generate all arrangements |
| **Subset/Combination** | Select subset, order doesn't matter | Generate all subsets/combinations |
| **Target Sum** | Constraint on sum/value | Find combinations meeting target |
| **Grid Search** | 2D space exploration | Path finding, word search |
| **Constraint Satisfaction** | Multiple constraints | N-Queens, Sudoku |

### 1.4 When to Use Backtracking

- **Exhaustive Search**: Need to explore all possible solutions
- **Constraint Satisfaction**: Multiple constraints must be satisfied simultaneously
- **Decision Problem**: Need to find ANY valid solution (can optimize with early return)
- **Enumeration**: Need to list ALL valid solutions
- **Pruning Opportunity**: Can eliminate large portions of search space early

### 1.5 Why It Works

Backtracking systematically explores the solution space by:
1. **Building incrementally**: Each recursive call extends the current partial solution
2. **Pruning early**: Invalid paths are abandoned immediately, saving computation
3. **Exploring exhaustively**: All valid paths are explored through recursion
4. **Undoing choices**: Backtracking allows exploring alternative paths from the same state

The key insight is that by maintaining state and undoing choices, we can explore all possibilities without storing all partial solutions explicitly.

---

---

## 2. Template Quick Reference

### 2.1 Permutation Template

> **Strategy**: Generate all arrangements where all elements are used and order matters.  
> **Key Insight**: Use a `used` array to track which elements are already in the current path.  
> **Time Complexity**: O(n! × n) — n! permutations, each takes O(n) to copy.

#### When to Use

- Generate all **arrangements** of elements
- Order matters (e.g., [1,2,3] ≠ [2,1,3])
- All elements must be used exactly once
- No duplicates in input (or handle duplicates with sorting + skipping)

#### Template

```python
def permute(nums):
    """
    Generate all permutations of nums.
    
    Time Complexity: O(n! × n) - n! permutations, O(n) to copy each
    Space Complexity: O(n) - recursion depth + path storage
    """
    results = []
    used = [False] * len(nums)
    
    def backtrack(path):
        # BASE CASE: Complete permutation found
        if len(path) == len(nums):
            results.append(path[:])  # Copy path
            return
        
        # CHOICES: Try all unused elements
        for i in range(len(nums)):
            if used[i]:
                continue  # Skip already used elements
            
            # MAKE CHOICE
            used[i] = True
            path.append(nums[i])
            
            # RECURSE
            backtrack(path)
            
            # BACKTRACK
            path.pop()
            used[i] = False
    
    backtrack([])
    return results
```

#### Handling Duplicates

```python
def permute_unique(nums):
    """Handle duplicates by sorting and skipping same values."""
    nums.sort()
    results = []
    used = [False] * len(nums)
    
    def backtrack(path):
        if len(path) == len(nums):
            results.append(path[:])
            return
        
        for i in range(len(nums)):
            if used[i]:
                continue
            # Skip duplicates: if same as previous and previous not used
            if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
                continue
            
            used[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            used[i] = False
    
    backtrack([])
    return results
```

#### Complexity Notes

| Aspect | Analysis |
|--------|----------|
| Time | O(n! × n) — n! permutations, O(n) to copy each |
| Space | O(n) — recursion depth + path storage |
| Pruning | Early termination possible if only need existence check |

#### LeetCode Problems

| ID | Problem | Variation |
|----|---------|-----------|
| 46 | Permutations | Basic permutation |
| 47 | Permutations II | Handle duplicates |
| 60 | Permutation Sequence | Find k-th permutation (math) |

---

### 2.2 Subset/Combination Template

> **Strategy**: Generate all subsets/combinations where order doesn't matter.  
> **Key Insight**: Use `start` index to avoid duplicates and ensure order.  
> **Time Complexity**: O(2ⁿ × n) — 2ⁿ subsets, each takes O(n) to copy.

#### When to Use

- Generate all **subsets** or **combinations**
- Order doesn't matter (e.g., [1,2] = [2,1])
- Elements can be skipped
- Often combined with constraints (size limit, sum, etc.)

#### Template

```python
def subsets(nums):
    """
    Generate all subsets of nums.
    
    Time Complexity: O(2ⁿ × n) - 2ⁿ subsets, O(n) to copy each
    Space Complexity: O(n) - recursion depth + path storage
    """
    results = []
    
    def backtrack(start, path):
        # COLLECT: Add current path (every node is a valid subset)
        results.append(path[:])
        
        # CHOICES: Try elements starting from 'start'
        for i in range(start, len(nums)):
            # MAKE CHOICE
            path.append(nums[i])
            
            # RECURSE: Next start is i+1 (no reuse)
            backtrack(i + 1, path)
            
            # BACKTRACK
            path.pop()
    
    backtrack(0, [])
    return results
```

#### Combination with Size Constraint

```python
def combine(n, k):
    """Generate all combinations of k numbers from [1..n]."""
    results = []
    
    def backtrack(start, path):
        # BASE CASE: Reached desired size
        if len(path) == k:
            results.append(path[:])
            return
        
        # PRUNING: Not enough elements remaining
        if len(path) + (n - start + 1) < k:
            return
        
        for i in range(start, n + 1):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()
    
    backtrack(1, [])
    return results
```

#### Complexity Notes

| Aspect | Analysis |
|--------|----------|
| Time | O(2ⁿ × n) — 2ⁿ subsets, O(n) to copy each |
| Space | O(n) — recursion depth + path storage |
| Optimization | Can prune early if size constraint exists |

#### LeetCode Problems

| ID | Problem | Variation |
|----|---------|-----------|
| 78 | Subsets | All subsets |
| 90 | Subsets II | Handle duplicates |
| 77 | Combinations | Size-k combinations |
| 39 | Combination Sum | With target sum |

---

### 2.3 Target Sum Template

> **Strategy**: Find combinations that sum to a target value.  
> **Key Insight**: Track remaining sum and prune negative paths early.  
> **Time Complexity**: O(2ⁿ) worst case, often much better with pruning.

#### When to Use

- Find combinations meeting a **target sum**
- Elements can be reused (or not, depending on problem)
- Early pruning possible when sum exceeds target
- Often combined with sorting for better pruning

#### Template (With Reuse)

```python
def combination_sum(candidates, target):
    """
    Find all combinations that sum to target.
    Elements can be reused.
    
    Time Complexity: O(2ⁿ) worst case, better with pruning
    Space Complexity: O(target) - recursion depth
    """
    results = []
    
    def backtrack(start, path, remaining):
        # BASE CASE: Found valid combination
        if remaining == 0:
            results.append(path[:])
            return
        
        # PRUNING: Sum exceeds target
        if remaining < 0:
            return
        
        for i in range(start, len(candidates)):
            # MAKE CHOICE
            path.append(candidates[i])
            
            # RECURSE: Start from i (allow reuse)
            backtrack(i, path, remaining - candidates[i])
            
            # BACKTRACK
            path.pop()
    
    backtrack(0, [], target)
    return results
```

#### Template (No Reuse)

```python
def combination_sum2(candidates, target):
    """Elements cannot be reused. Handle duplicates."""
    candidates.sort()
    results = []
    
    def backtrack(start, path, remaining):
        if remaining == 0:
            results.append(path[:])
            return
        if remaining < 0:
            return
        
        for i in range(start, len(candidates)):
            # Skip duplicates
            if i > start and candidates[i] == candidates[i-1]:
                continue
            
            path.append(candidates[i])
            backtrack(i + 1, path, remaining - candidates[i])  # i+1: no reuse
            path.pop()
    
    backtrack(0, [], target)
    return results
```

#### Complexity Notes

| Aspect | Analysis |
|--------|----------|
| Time | O(2ⁿ) worst case, often O(2^(target/min)) with pruning |
| Space | O(target/min) — recursion depth |
| Pruning | Very effective when sorted + early termination |

#### LeetCode Problems

| ID | Problem | Variation |
|----|---------|-----------|
| 39 | Combination Sum | Allow reuse |
| 40 | Combination Sum II | No reuse, handle duplicates |
| 216 | Combination Sum III | Size-k constraint |
| 377 | Combination Sum IV | Count ways (DP better) |

---

### 2.4 Grid Search Template

> **Strategy**: Explore 2D grid to find paths matching a pattern.  
> **Key Insight**: Mark visited cells temporarily, restore after backtracking.  
> **Time Complexity**: O(m × n × 4^L) where L is pattern length.

#### When to Use

- **2D grid exploration** problems
- **Path finding** with constraints
- **Word search** in grid
- Need to avoid revisiting same cell in current path
- Often combined with early return for existence check

#### Template

```python
def exist(grid, word):
    """
    Check if word exists in grid (can move 4-directionally).
    
    Time Complexity: O(m × n × 4^L) - L is word length
    Space Complexity: O(L) - recursion depth
    """
    rows, cols = len(grid), len(grid[0])
    
    def backtrack(r, c, index):
        # BASE CASE: Found complete word
        if index == len(word):
            return True
        
        # BOUNDARY CHECK
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        
        # CONSTRAINT CHECK: Character doesn't match
        if grid[r][c] != word[index]:
            return False
        
        # MARK VISITED: Temporarily mark to avoid reuse in current path
        temp = grid[r][c]
        grid[r][c] = '#'
        
        # EXPLORE: Try all 4 directions
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            if backtrack(r + dr, c + dc, index + 1):
                # Found solution, restore and return
                grid[r][c] = temp
                return True
        
        # BACKTRACK: Restore cell
        grid[r][c] = temp
        return False
    
    # Try starting from each cell
    for r in range(rows):
        for c in range(cols):
            if backtrack(r, c, 0):
                return True
    return False
```

#### Alternative: Using Visited Set

```python
def exist_with_set(grid, word):
    """Alternative using visited set (more memory but clearer)."""
    rows, cols = len(grid), len(grid[0])
    
    def backtrack(r, c, index, visited):
        if index == len(word):
            return True
        if (r < 0 or r >= rows or c < 0 or c >= cols or 
            (r, c) in visited or grid[r][c] != word[index]):
            return False
        
        visited.add((r, c))
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            if backtrack(r + dr, c + dc, index + 1, visited):
                return True
        visited.remove((r, c))
        return False
    
    for r in range(rows):
        for c in range(cols):
            if backtrack(r, c, 0, set()):
                return True
    return False
```

#### Complexity Notes

| Aspect | Analysis |
|--------|----------|
| Time | O(m × n × 4^L) — L is pattern length, 4 directions |
| Space | O(L) — recursion depth (or O(m×n) with visited set) |
| Optimization | Early return when existence check only |

#### LeetCode Problems

| ID | Problem | Variation |
|----|---------|-----------|
| 79 | Word Search | Basic grid search |
| 212 | Word Search II | Multiple words (Trie + backtrack) |
| 130 | Surrounded Regions | Flood fill variant |
| 200 | Number of Islands | DFS on grid |

---

### 2.5 Constraint Satisfaction Template

> **Strategy**: Solve problems with multiple constraints (N-Queens, Sudoku).  
> **Key Insight**: Check constraints before making choice, prune aggressively.  
> **Time Complexity**: Varies, often exponential but heavily pruned.

#### When to Use

- **Multiple constraints** must be satisfied simultaneously
- **Placement problems** (N-Queens, Sudoku)
- Can check validity before making choice
- Often benefits from constraint propagation

#### Template (N-Queens)

```python
def solve_n_queens(n):
    """
    Place n queens on n×n board so none attack each other.
    
    Time Complexity: O(n!) worst case, much better with pruning
    Space Complexity: O(n) - recursion depth + board storage
    """
    results = []
    board = [['.' for _ in range(n)] for _ in range(n)]
    
    def is_valid(row, col):
        """Check if placing queen at (row, col) is valid."""
        # Check column
        for i in range(row):
            if board[i][col] == 'Q':
                return False
        
        # Check diagonal: top-left to bottom-right
        i, j = row - 1, col - 1
        while i >= 0 and j >= 0:
            if board[i][j] == 'Q':
                return False
            i -= 1
            j -= 1
        
        # Check diagonal: top-right to bottom-left
        i, j = row - 1, col + 1
        while i >= 0 and j < n:
            if board[i][j] == 'Q':
                return False
            i -= 1
            j += 1
        
        return True
    
    def backtrack(row):
        # BASE CASE: Placed all queens
        if row == n:
            results.append([''.join(row) for row in board])
            return
        
        # CHOICES: Try each column in current row
        for col in range(n):
            # PRUNING: Check validity before placing
            if not is_valid(row, col):
                continue
            
            # MAKE CHOICE
            board[row][col] = 'Q'
            
            # RECURSE
            backtrack(row + 1)
            
            # BACKTRACK
            board[row][col] = '.'
    
    backtrack(0)
    return results
```

#### Complexity Notes

| Aspect | Analysis |
|--------|----------|
| Time | O(n!) worst case, heavily pruned in practice |
| Space | O(n²) — board storage + O(n) recursion |
| Optimization | Constraint checking before placement is crucial |

#### LeetCode Problems

| ID | Problem | Variation |
|----|---------|-----------|
| 51 | N-Queens | Basic constraint satisfaction |
| 52 | N-Queens II | Count solutions only |
| 37 | Sudoku Solver | 9×9 grid with 3×3 boxes |



---



*Document generated for NeetCode Practice Framework — API Kernel: BacktrackingExploration*
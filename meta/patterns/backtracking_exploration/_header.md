# Backtracking Exploration Patterns: Complete Reference

> **API Kernel**: `BacktrackingExploration`  
> **Core Mechanism**: Systematically explore all candidate solutions by building them incrementally, abandoning paths that violate constraints (pruning), and undoing choices to try alternatives.

This document presents the **canonical backtracking template** and all its major variations. Each implementation follows consistent naming conventions and includes detailed algorithmic explanations.

---

## Core Concepts

### What is Backtracking?

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

### The Three-Step Pattern: Choose → Explore → Unchoose

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

### Key Invariants

| Invariant | Description |
|-----------|-------------|
| **State Consistency** | After backtracking, state must be exactly as before the choice was made |
| **Exhaustive Exploration** | Every valid solution must be reachable through some path |
| **Pruning Soundness** | Pruned branches must not contain any valid solutions |
| **No Duplicates** | Each unique solution must be generated exactly once |

### Time Complexity Discussion

Backtracking algorithms typically have exponential or factorial complexity because they explore the entire solution space:

| Problem Type | Typical Complexity | Output Size |
|--------------|-------------------|-------------|
| Permutations | O(n! × n) | n! |
| Subsets | O(2^n × n) | 2^n |
| Combinations C(n,k) | O(C(n,k) × k) | C(n,k) |
| N-Queens | O(n!) | variable |

**Important**: The complexity is often **output-sensitive** — if there are many solutions, generating them all is inherently expensive.

### Sub-Pattern Classification

| Sub-Pattern | Key Characteristic | Examples |
|-------------|-------------------|----------|
| **Permutation** | Used/visited tracking | LeetCode 46, 47 |
| **Subset/Combination** | Start-index canonicalization | LeetCode 78, 90, 77 |
| **Target Search** | Remaining/target pruning | LeetCode 39, 40, 216 |
| **Constraint Satisfaction** | Row-by-row with constraint sets | LeetCode 51, 52 |
| **String Partitioning** | Cut positions with validity | LeetCode 131, 93 |
| **Grid/Path Search** | Visited marking and undo | LeetCode 79 |

---

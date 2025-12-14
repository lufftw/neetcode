# Backtracking Exploration Patterns: Complete Reference

> **API Kernel**: `BacktrackingExploration`  
> **Core Mechanism**: Systematically explore all candidate solutions by building them incrementally, abandoning paths that violate constraints (pruning), and undoing choices to try alternatives.

This document presents the **canonical backtracking template** and all its major variations. Each implementation follows consistent naming conventions and includes detailed algorithmic explanations.

---

## Core Concepts

### The Backtracking Process

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

### Universal Template Structure

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

### Backtracking Family Overview

| Sub-Pattern | Key Characteristic | Primary Use Case |
|-------------|-------------------|------------------|
| **Permutation** | All elements used, order matters | Generate all arrangements |
| **Subset/Combination** | Select subset, order doesn't matter | Generate all subsets/combinations |
| **Target Sum** | Constraint on sum/value | Find combinations meeting target |
| **Grid Search** | 2D space exploration | Path finding, word search |
| **Constraint Satisfaction** | Multiple constraints | N-Queens, Sudoku |

### When to Use Backtracking

- **Exhaustive Search**: Need to explore all possible solutions
- **Constraint Satisfaction**: Multiple constraints must be satisfied simultaneously
- **Decision Problem**: Need to find ANY valid solution (can optimize with early return)
- **Enumeration**: Need to list ALL valid solutions
- **Pruning Opportunity**: Can eliminate large portions of search space early

### Why It Works

Backtracking systematically explores the solution space by:
1. **Building incrementally**: Each recursive call extends the current partial solution
2. **Pruning early**: Invalid paths are abandoned immediately, saving computation
3. **Exploring exhaustively**: All valid paths are explored through recursion
4. **Undoing choices**: Backtracking allows exploring alternative paths from the same state

The key insight is that by maintaining state and undoing choices, we can explore all possibilities without storing all partial solutions explicitly.

---

## Variation: Word Search (LeetCode 79)

> **Problem**: Find if a word exists in a grid by traversing adjacent cells.  
> **Sub-Pattern**: Grid/Path DFS with visited marking.  
> **Key Insight**: Mark visited, explore neighbors, unmark on backtrack.

### Implementation

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

### In-Place Marking vs Visited Set

| Approach | Pros | Cons |
|----------|------|------|
| In-place (`#`) | O(1) space, fast | Modifies input temporarily |
| Visited set | Clean, no mutation | O(L) space for coordinates |


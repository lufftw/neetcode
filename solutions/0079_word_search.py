# solutions/0079_word_search.py
"""
Problem: Word Search
Link: https://leetcode.com/problems/word-search/

Given an m x n grid of characters board and a string word, return true if word exists in the grid.
The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.

Example 1:
    <img alt="" src="https://assets.leetcode.com/uploads/2020/11/04/word2.jpg" style="width: 322px; height: 242px;" />
    Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
    Output: true

Example 2:
    <img alt="" src="https://assets.leetcode.com/uploads/2020/11/04/word-1.jpg" style="width: 322px; height: 242px;" />
    Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "SEE"
    Output: true

Example 3:
    <img alt="" src="https://assets.leetcode.com/uploads/2020/10/15/word3.jpg" style="width: 322px; height: 242px;" />
    Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCB"
    Output: false

Constraints:
- m == board.length
- n = board[i].length
- 1 <= m, n <= 6
- 1 <= word.length <= 15
- board and word consists of only lowercase and uppercase English letters.

Topics: Array, Backtracking, Matrix

Follow-up: Could you use search pruning to make your solution faster with a larger board?
"""
from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "exist",
        "complexity": "O(m × n × 4^L) time, O(L) space",
        "description": "DFS backtracking with in-place visited marking",
    },
}


# ============================================================================
# Solution 1: DFS Backtracking with In-Place Visited Marking
# Time: O(m × n × 4^L), Space: O(L)
#   - Start DFS from each cell matching word[0]
#   - Mark visited cells in-place (temporarily change to '#')
#   - Try all 4 directions; unmark on backtrack
# ============================================================================
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        """
        Check if word exists in grid by traversing adjacent cells.
        
        Algorithm:
        - Start DFS from each cell that matches word[0]
        - At each step, try all 4 directions (up, down, left, right)
        - Mark current cell as visited before exploring
        - Unmark on backtrack to allow other paths to use this cell
        
        Visited Marking Strategy:
        - In-place modification: temporarily change cell to '#'
        - Pros: O(1) space, no separate data structure
        - Cons: Modifies input temporarily (restored after)
        - Alternative: Use set of (row, col) tuples (O(L) space)
        
        Pruning:
        - Early return on character mismatch
        - Early return on boundary violation
        - Optional: Check if board has enough of each character
        
        Time Complexity: O(m × n × 4^L)
            - m×n possible starting positions
            - 4 choices at each step, up to L steps deep
            - L = len(word)
            - In practice, much faster due to pruning and mismatches
        
        Space Complexity: O(L) for recursion depth
        """
        if not board or not board[0]:
            return False
        
        rows, cols = len(board), len(board[0])
        word_len = len(word)
        
        # Four directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        def backtrack(row: int, col: int, index: int) -> bool:
            """
            DFS from (row, col) trying to match word[index:].
            
            Returns True if we can complete the word from here.
            """
            # BASE CASE: All characters matched
            if index == word_len:
                return True
            
            # === BOUNDARY CHECK ===
            if row < 0 or row >= rows or col < 0 or col >= cols:
                return False
            
            # === CHARACTER MATCH CHECK ===
            if board[row][col] != word[index]:
                return False
            
            # === CHOOSE: Mark as visited ===
            # Store original character and replace with marker
            # This prevents revisiting this cell in the current path
            original = board[row][col]
            board[row][col] = '#'  # Marker for "visited"
            
            # === EXPLORE: Try all 4 directions ===
            for dr, dc in directions:
                next_row, next_col = row + dr, col + dc
                if backtrack(next_row, next_col, index + 1):
                    # Found complete word! Restore and return True
                    board[row][col] = original
                    return True
            
            # === UNCHOOSE: Unmark (backtrack) ===
            board[row][col] = original
            
            # No direction led to a complete word
            return False
        
        # Try starting from each cell
        for r in range(rows):
            for c in range(cols):
                # Only start from cells that match first character
                if board[r][c] == word[0]:
                    if backtrack(r, c, 0):
                        return True
        
        return False


def solve():
    """
    Input format (canonical JSON):
    Line 1: [m,n] dimensions as JSON array
    Lines 2 to m+1: grid rows as JSON arrays
    Last line: word as string
    
    Example:
    [3,4]
    ["A","B","C","E"]
    ["S","F","C","S"]
    ["A","D","E","E"]
    ABCCED
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')
    
    dims = json.loads(lines[0])
    m, n = dims[0], dims[1]
    board = []
    for i in range(1, m + 1):
        row = json.loads(lines[i])
        board.append(row)
    word = lines[m + 1]
    
    solver = get_solver(SOLUTIONS)
    result = solver.exist(board, word)
    
    # Output canonical boolean
    print('true' if result else 'false')


if __name__ == "__main__":
    solve()


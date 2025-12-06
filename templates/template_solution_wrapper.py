# solutions/xxxx_problem_name.py
"""
Problem: [Problem Name]
Link: https://leetcode.com/problems/xxx/

Wrapper-based template - Multiple Solution classes with wrapper functions
Use this when you want to:
- Keep each solution in its own class
- Preserve original LeetCode method names (e.g., reverseKGroup, mergeKLists)
- Avoid method name conflicts
"""
from typing import List, Optional
import os


# ============================================
# Solution 1: Approach A (e.g., Recursive)
# Time: O(?), Space: O(?)
# ============================================
class SolutionA:
    def solve(self, *args):
        """
        TODO: Implement solution A
        Keep the original LeetCode method name if applicable.
        """
        pass


# ============================================
# Solution 2: Approach B (e.g., Iterative)
# Time: O(?), Space: O(?)
# ============================================
class SolutionB:
    def solve(self, *args):
        """
        TODO: Implement solution B
        Keep the original LeetCode method name if applicable.
        """
        pass


# ============================================
# Wrapper functions for test_runner integration
# These connect your Solution classes to the runner
# ============================================
def solve_a(*args):
    """Wrapper for SolutionA."""
    return SolutionA().solve(*args)


def solve_b(*args):
    """Wrapper for SolutionB."""
    return SolutionB().solve(*args)


# ============================================
# SOLUTIONS metadata - tells test_runner which solutions are available
# ============================================
SOLUTIONS = {
    "default": {
        "method": "solve_a",               # Default wrapper function
        "complexity": "O(?)",              # Time/Space complexity
        "description": "Approach A"
    },
    "a": {
        "method": "solve_a",
        "complexity": "O(?)",
        "description": "Approach A"
    },
    "b": {
        "method": "solve_b",
        "complexity": "O(?)",
        "description": "Approach B"
    },
}


def solve():
    """
    Parse input from stdin, select solution based on SOLUTION_METHOD env var.
    """
    import sys

    # Get solution method from environment variable
    method_name = os.environ.get('SOLUTION_METHOD', 'default')
    method_info = SOLUTIONS.get(method_name, SOLUTIONS['default'])
    method_func_name = method_info['method']

    # Parse input
    lines = sys.stdin.read().strip().split('\n')
    # TODO: Parse input according to problem format
    # Example:
    # nums = list(map(int, lines[0].split(',')))

    # Call wrapper function directly using globals()
    method_func = globals()[method_func_name]
    result = method_func()  # TODO: Pass parsed parameters

    # Print result
    print(result)


if __name__ == "__main__":
    solve()


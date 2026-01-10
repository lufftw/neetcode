"""
Problem: Letter Combinations of a Phone Number
Link: https://leetcode.com/problems/letter-combinations-of-a-phone-number/

Given a string containing digits from 2-9 inclusive, return all possible letter
combinations that the number could represent. Return the answer in any order.

A mapping of digits to letters (just like on the telephone buttons):
    2 -> abc, 3 -> def, 4 -> ghi, 5 -> jkl,
    6 -> mno, 7 -> pqrs, 8 -> tuv, 9 -> wxyz

Example 1:
    Input: digits = "23"
    Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]

Example 2:
    Input: digits = ""
    Output: []

Example 3:
    Input: digits = "2"
    Output: ["a","b","c"]

Constraints:
- 0 <= digits.length <= 4
- digits[i] is a digit in the range ['2', '9'].

Topics: Hash Table, String, Backtracking
"""
import json
from typing import List
from _runner import get_solver


# Phone digit to letters mapping (classic T9 keyboard)
DIGIT_TO_LETTERS = {
    '2': 'abc',
    '3': 'def',
    '4': 'ghi',
    '5': 'jkl',
    '6': 'mno',
    '7': 'pqrs',
    '8': 'tuv',
    '9': 'wxyz',
}


# ============================================================================
# JUDGE_FUNC - Validates output for generated tests
# ============================================================================
def _get_expected_combinations(digits: str) -> set:
    """Compute expected combinations using itertools."""
    if not digits:
        return set()
    from itertools import product
    letter_groups = [DIGIT_TO_LETTERS[d] for d in digits]
    return {''.join(combo) for combo in product(*letter_groups)}


def judge(actual, expected, input_data: str) -> bool:
    """
    Custom validation for Letter Combinations.

    Validates:
    1. All returned combinations are valid
    2. No duplicates
    3. Correct total count
    """
    # Parse input
    digits = json.loads(input_data.strip())

    # Handle empty input
    if not digits:
        return actual == []

    # Convert actual to set for comparison
    if not isinstance(actual, list):
        return False

    actual_set = set(actual)

    # Check for duplicates
    if len(actual_set) != len(actual):
        return False

    # Compute expected combinations
    expected_set = _get_expected_combinations(digits)

    # Compare sets
    return actual_set == expected_set


JUDGE_FUNC = judge

# Also keep COMPARE_MODE for static tests without JUDGE_FUNC overhead
COMPARE_MODE = "sorted"


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "SolutionBacktrack",
        "method": "letterCombinations",
        "complexity": "O(4^n) time, O(n) space",
        "description": "Backtracking - build combinations character by character",
    },
    "backtrack": {
        "class": "SolutionBacktrack",
        "method": "letterCombinations",
        "complexity": "O(4^n) time, O(n) space",
        "description": "Backtracking - build combinations character by character",
    },
    "iterative": {
        "class": "SolutionIterative",
        "method": "letterCombinations",
        "complexity": "O(4^n) time, O(4^n) space",
        "description": "Iterative BFS-style expansion",
    },
    "product": {
        "class": "SolutionProduct",
        "method": "letterCombinations",
        "complexity": "O(4^n) time, O(4^n) space",
        "description": "Using itertools.product for Cartesian product",
    },
}


# ============================================================================
# Solution 1: Backtracking
# Time: O(4^n * n), Space: O(n) excluding output
#   - At most 4 choices per digit (7 and 9 have 4 letters)
#   - n levels of recursion for n digits
#   - Each combination takes O(n) to build the string
# ============================================================================
class SolutionBacktrack:
    """
    Backtracking approach - the canonical interview solution.

    Build combinations character by character using DFS. At each digit,
    try all possible letters and recurse to the next digit. When we've
    processed all digits, we have a complete combination.
    """

    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []

        results: List[str] = []
        n = len(digits)

        def backtrack(index: int, path: List[str]) -> None:
            """
            Build combinations recursively.

            Args:
                index: Current digit position being processed
                path: Letters chosen so far
            """
            # Base case: all digits processed
            if index == n:
                results.append(''.join(path))
                return

            # Get letters for current digit
            current_digit = digits[index]
            letters = DIGIT_TO_LETTERS[current_digit]

            # Try each letter for this digit
            for letter in letters:
                path.append(letter)          # Choose
                backtrack(index + 1, path)   # Explore
                path.pop()                   # Unchoose (backtrack)

        backtrack(0, [])
        return results


# ============================================================================
# Solution 2: Iterative (BFS-style)
# Time: O(4^n * n), Space: O(4^n * n) for intermediate results
#   - Builds all combinations level by level
#   - Each level multiplies the result set by up to 4x
# ============================================================================
class SolutionIterative:
    """
    Iterative BFS-style expansion.

    Start with empty string, then for each digit, extend all current
    combinations with each possible letter. This builds combinations
    "breadth-first" rather than "depth-first".
    """

    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []

        # Start with one empty combination
        combinations = ['']

        for digit in digits:
            letters = DIGIT_TO_LETTERS[digit]

            # Extend each existing combination with each letter
            new_combinations = []
            for combo in combinations:
                for letter in letters:
                    new_combinations.append(combo + letter)

            combinations = new_combinations

        return combinations


# ============================================================================
# Solution 3: Using itertools.product
# Time: O(4^n * n), Space: O(4^n * n)
#   - Cartesian product handles the combinatorics
#   - Pythonic but less educational for interviews
# ============================================================================
class SolutionProduct:
    """
    Using itertools.product for Cartesian product.

    The problem is essentially computing the Cartesian product of
    letter sets for each digit. Python's itertools makes this trivial.
    """

    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []

        from itertools import product

        # Get letter groups for each digit
        letter_groups = [DIGIT_TO_LETTERS[d] for d in digits]

        # Compute Cartesian product and join each tuple
        return [''.join(combo) for combo in product(*letter_groups)]


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: digits (JSON string with quotes)

    Example:
        "23"
    """
    import sys
    lines = sys.stdin.read().strip().split('\n')

    # Parse JSON string input
    digits = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.letterCombinations(digits)

    # Output as JSON array
    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

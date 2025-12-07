# generators/0051_n_queens.py
"""
Test Case Generator for Problem 0051 - N-Queens

This generator creates random N values to test the N-Queens solution.
Unlike 0004_median which has complex multi-line inputs, N-Queens has
a simple single-integer input, making it a good contrasting example.

=== Generator Design Philosophy ===

1. EDGE CASES FIRST
   - Always yield known edge cases before random cases
   - Edge cases help catch corner-case bugs early
   - Example: n=1 (trivial), n=4 (classic), n=9 (larger)

2. CONSTRAINTS AWARENESS
   - Define constraints as local variables at the top
   - Match LeetCode's constraints exactly
   - This problem: 1 <= n <= 9

3. PERFORMANCE CONSIDERATION
   - N-Queens has O(N!) time complexity
   - n=9 is the max because n=10+ would be too slow
   - Generator should respect these practical limits

4. INPUT FORMAT
   - Output must match .in file format exactly
   - For N-Queens: just a single integer per line
   - Always end with newline (handled by test_runner)

5. JUDGE_FUNC REQUIREMENT
   - Generator produces INPUT only, no expected output
   - Solution MUST have JUDGE_FUNC to validate results
   - See solutions/0051_n_queens.py for JUDGE_FUNC example

=== Usage ===

# Run tests/ + 5 generated cases
python runner/test_runner.py 0051_n_queens --generate 5

# Only generated cases (skip tests/)
python runner/test_runner.py 0051_n_queens --generate-only 10

# Reproducible with seed
python runner/test_runner.py 0051_n_queens --generate 5 --seed 42

LeetCode Constraints:
- 1 <= n <= 9
"""
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for N-Queens.
    
    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)
    
    Yields:
        str: Test input - a single integer n
    
    Note:
        The solution's JUDGE_FUNC will validate that:
        1. Number of solutions matches expected count
        2. Each board is a valid N-Queens configuration
        3. No duplicate solutions
    """
    # ========================================
    # Constraints from LeetCode
    # ========================================
    min_n = 1   # Minimum board size
    max_n = 9   # Maximum board size (n=10+ is too slow)
    
    # ========================================
    # Initialize random seed if provided
    # ========================================
    if seed is not None:
        random.seed(seed)
    
    # ========================================
    # Edge cases first (known important values)
    # ========================================
    # These are cases that often reveal bugs:
    # - n=1: trivial case, only one solution
    # - n=4: classic example, 2 solutions
    # - n=8: standard chess board, 92 solutions
    # - n=9: maximum allowed, 352 solutions
    edge_cases = [
        "1",  # Trivial: single cell, single solution
        "4",  # Classic: 2 solutions, good for basic testing
        "8",  # Standard chess: 92 solutions
        "9",  # Maximum: 352 solutions, stress test
    ]
    
    for edge in edge_cases:
        yield edge
        count -= 1
        if count <= 0:
            return
    
    # ========================================
    # Random cases
    # ========================================
    # Generate random n values within constraints
    # Weight towards larger values for stress testing
    for _ in range(count):
        # Option 1: Uniform random
        # n = random.randint(min_n, max_n)
        
        # Option 2: Weighted towards larger (more thorough testing)
        # Using choices with weights
        n = random.choices(
            population=range(min_n, max_n + 1),
            weights=[1, 1, 2, 3, 4, 5, 6, 7, 8],  # Higher weight for larger n
            k=1
        )[0]
        
        yield str(n)


# ========================================
# Optional: Stress test generator
# ========================================
# You can define additional generator functions for specific purposes.
# The main generate() function is what test_runner calls.

def generate_all_sizes() -> Iterator[str]:
    """
    Generate one test case for each possible n value.
    Useful for comprehensive validation.
    
    Usage (manual):
        from generators.0051_n_queens import generate_all_sizes
        for input_data in generate_all_sizes():
            print(input_data)
    """
    for n in range(1, 10):
        yield str(n)


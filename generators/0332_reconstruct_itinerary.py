# generators/0332_reconstruct_itinerary.py
"""
Test Case Generator for Problem 0332 - Reconstruct Itinerary

LeetCode Constraints:
- 1 <= tickets.length <= 300
- tickets[i].length == 2
- fromi.length == 3, toi.length == 3
- fromi and toi consist of uppercase English letters
- fromi != toi
"""
import json
import random
import string
from typing import Iterator, Optional, List, Set


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Reconstruct Itinerary.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (tickets as JSON 2D array)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # LeetCode Example 1
        [["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]],
        # LeetCode Example 2
        [["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]],
        # Single ticket
        [["JFK", "NYC"]],
        # Simple cycle
        [["JFK", "LAX"], ["LAX", "JFK"]],
        # Linear path
        [["JFK", "AAA"], ["AAA", "BBB"], ["BBB", "CCC"]],
    ]

    for tickets in edge_cases:
        yield json.dumps(tickets, separators=(",", ":"))
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random valid itinerary."""
    # Generate random airport codes
    num_airports = random.randint(3, 10)
    airports = ["JFK"]  # Must start with JFK

    for _ in range(num_airports - 1):
        code = "".join(random.choices(string.ascii_uppercase, k=3))
        if code not in airports and code != "JFK":
            airports.append(code)

    # Generate a valid Eulerian path
    # Start from JFK, randomly walk through airports
    num_tickets = random.randint(2, min(15, len(airports) * 2))
    tickets = []
    current = "JFK"

    for _ in range(num_tickets):
        # Pick a random destination
        candidates = [a for a in airports if a != current]
        if not candidates:
            candidates = airports
        dest = random.choice(candidates)
        tickets.append([current, dest])
        current = dest

    return json.dumps(tickets, separators=(",", ":"))


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Reconstruct Itinerary:
    - n is the number of tickets (edges)
    - Time complexity is O(n log n)

    Args:
        n: Number of tickets (will be clamped to [1, 300])

    Returns:
        str: Test input (tickets as JSON)
    """
    # Clamp to LeetCode constraints
    n = max(1, min(n, 300))

    # Generate airports
    num_airports = min(n // 2 + 2, 26)
    airports = ["JFK"] + [
        chr(ord("A") + i) + chr(ord("A") + j) + chr(ord("A") + k)
        for i in range(num_airports)
        for j in range(1)
        for k in range(1)
    ][:num_airports]

    # Generate tickets forming a valid path
    tickets = []
    current = "JFK"

    for _ in range(n):
        candidates = [a for a in airports if a != current]
        if not candidates:
            candidates = airports
        dest = random.choice(candidates)
        tickets.append([current, dest])
        current = dest

    return json.dumps(tickets, separators=(",", ":"))


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(5, seed=42), 1):
        tickets = json.loads(test)
        print(f"Test {i}: {len(tickets)} tickets")
        if len(tickets) <= 10:
            print(f"  tickets: {tickets}")
        print()

# generators/0981_time_based_key_value_store.py
"""
Test Case Generator for Problem 0981 - Time Based Key-Value Store

LeetCode Constraints:
- 1 <= key.length, value.length <= 100
- key and value consist of lowercase English letters and digits
- 1 <= timestamp <= 10^7
- All timestamps of set are strictly increasing
- At most 2 * 10^5 calls will be made to set and get
"""
import json
import random
import string
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Time Based Key-Value Store.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (operations and args as JSON)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # LeetCode Example 1
        (
            ["TimeMap", "set", "get", "get", "set", "get", "get"],
            [[], ["foo", "bar", 1], ["foo", 1], ["foo", 3], ["foo", "bar2", 4], ["foo", 4], ["foo", 5]],
        ),
        # Get before any set
        (
            ["TimeMap", "get"],
            [[], ["key", 1]],
        ),
        # Multiple keys
        (
            ["TimeMap", "set", "set", "get", "get"],
            [[], ["a", "v1", 1], ["b", "v2", 2], ["a", 1], ["b", 2]],
        ),
    ]

    for ops, args in edge_cases:
        yield f"{json.dumps(ops, separators=(',', ':'))}\n{json.dumps(args, separators=(',', ':'))}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random sequence of TimeMap operations."""
    num_ops = random.randint(10, 30)
    keys = ["key" + str(i) for i in range(3)]

    operations = ["TimeMap"]
    args = [[]]

    timestamp = 1
    key_timestamps = {k: [] for k in keys}

    for _ in range(num_ops):
        op = random.choice(["set", "get", "get"])  # More gets than sets

        if op == "set":
            key = random.choice(keys)
            value = "".join(random.choices(string.ascii_lowercase, k=5))
            operations.append("set")
            args.append([key, value, timestamp])
            key_timestamps[key].append(timestamp)
            timestamp += random.randint(1, 10)

        elif op == "get":
            key = random.choice(keys)
            # Query a timestamp that might or might not have a value
            query_ts = random.randint(1, timestamp + 5)
            operations.append("get")
            args.append([key, query_ts])

    return f"{json.dumps(operations, separators=(',', ':'))}\n{json.dumps(args, separators=(',', ':'))}"


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Time Based Key-Value Store:
    - n is the number of operations
    - set is O(1), get is O(log k) where k is entries per key

    Args:
        n: Number of operations (will be clamped to [2, 200000])

    Returns:
        str: Test input
    """
    # Clamp to LeetCode constraints
    n = max(2, min(n, 200000))

    operations = ["TimeMap"]
    args = [[]]

    timestamp = 1
    key = "key"

    # Half sets, half gets
    for i in range(n - 1):
        if i < n // 2:
            value = f"v{i}"
            operations.append("set")
            args.append([key, value, timestamp])
            timestamp += 1
        else:
            query_ts = random.randint(1, timestamp)
            operations.append("get")
            args.append([key, query_ts])

    return f"{json.dumps(operations, separators=(',', ':'))}\n{json.dumps(args, separators=(',', ':'))}"


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(3, seed=42), 1):
        lines = test.split("\n")
        ops = json.loads(lines[0])
        print(f"Test {i}: {len(ops)} operations")
        print(f"  Sample: {ops[:5]}...")
        print()

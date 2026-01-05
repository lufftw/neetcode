# generators/0621_task_scheduler.py
"""
Test Case Generator for Problem 621 - Task Scheduler

LeetCode Constraints:
- 1 <= tasks.length <= 10^4
- tasks[i] is an uppercase English letter
- 0 <= n <= 100
"""
import json
import random
import string
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Test input in .in file format (tasks on line 1, n on line 2)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        (["A", "A", "A", "B", "B", "B"], 2),       # Classic example, result 8
        (["A", "C", "A", "B", "D", "B"], 1),       # Result 6 (no idle)
        (["A", "A", "A", "B", "B", "B"], 3),       # More idle, result 10
        (["A"], 0),                                 # Single task
        (["A"], 100),                              # Single task, large n
        (["A", "B", "C", "D"], 2),                 # All different, no idle
        (["A", "A", "A", "A"], 3),                 # Same task repeated
    ]

    for tasks, n in edge_cases:
        yield f"{json.dumps(tasks, separators=(',', ':'))}\n{n}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single valid random test case."""
    # Random number of tasks
    num_tasks = random.randint(10, 200)

    # Use a subset of letters
    num_types = random.randint(2, 10)
    task_types = random.sample(string.ascii_uppercase, num_types)

    # Generate tasks with varying frequencies
    tasks = []
    for task_type in task_types:
        freq = random.randint(1, num_tasks // num_types + 5)
        tasks.extend([task_type] * freq)

    # Trim or pad to target size
    if len(tasks) > num_tasks:
        tasks = random.sample(tasks, num_tasks)
    elif len(tasks) < num_tasks:
        tasks.extend(random.choices(task_types, k=num_tasks - len(tasks)))

    random.shuffle(tasks)

    # Random cooldown period
    n = random.randint(0, 10)

    return f"{json.dumps(tasks, separators=(',', ':'))}\n{n}"


def generate_for_complexity(num_tasks: int) -> str:
    """Generate test case with specific number of tasks."""
    num_types = min(26, num_tasks // 10 + 2)
    task_types = list(string.ascii_uppercase[:num_types])

    tasks = []
    for task_type in task_types:
        tasks.extend([task_type] * (num_tasks // num_types))

    while len(tasks) < num_tasks:
        tasks.append(random.choice(task_types))

    random.shuffle(tasks)
    n = random.randint(0, 10)

    return f"{json.dumps(tasks, separators=(',', ':'))}\n{n}"

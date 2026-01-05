# solutions/0621_task_scheduler.py
"""
Problem: Task Scheduler
Link: https://leetcode.com/problems/task-scheduler/

You are given an array of CPU tasks, each represented by letters A to Z, and a cooling
number n. Each cycle or interval allows the completion of one task. Tasks can be
completed in any order, but there's a constraint: identical tasks must be separated
by at least n intervals due to cooling time.

Return the minimum number of intervals required to complete all tasks.

Example 1:
    Input: tasks = ["A","A","A","B","B","B"], n = 2
    Output: 8
    Explanation: A possible sequence is: A -> B -> idle -> A -> B -> idle -> A -> B.
                 After completing task A, you must wait two intervals before doing A again.
                 The same applies to task B.

Example 2:
    Input: tasks = ["A","C","A","B","D","B"], n = 1
    Output: 6
    Explanation: A possible sequence is: A -> B -> A -> C -> D -> B.

Example 3:
    Input: tasks = ["A","A","A","B","B","B"], n = 3
    Output: 10
    Explanation: A possible sequence is: A -> B -> idle -> idle -> A -> B -> idle -> idle -> A -> B.

Constraints:
- 1 <= tasks.length <= 10^4
- tasks[i] is an uppercase English letter.
- 0 <= n <= 100

Topics: Array, Hash Table, Greedy, Sorting, Heap Priority Queue, Counting
"""

import json
from collections import Counter, deque
from typing import List
import heapq

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionMath",
        "method": "leastInterval",
        "complexity": "O(n) time, O(1) space",
        "description": "Mathematical formula based on max frequency",
    },
    "math": {
        "class": "SolutionMath",
        "method": "leastInterval",
        "complexity": "O(n) time, O(1) space",
        "description": "Mathematical formula based on max frequency",
    },
    "heap": {
        "class": "SolutionHeap",
        "method": "leastInterval",
        "complexity": "O(n * m) time, O(k) space",
        "description": "Greedy scheduling with max-heap",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output is correct minimum intervals.

    Args:
        actual: Program output (integer as string or int)
        expected: Expected output (None if from generator)
        input_data: Raw input string (tasks and n on separate lines)

    Returns:
        bool: True if correct minimum intervals
    """
    lines = input_data.strip().split("\n")
    tasks = json.loads(lines[0]) if lines[0] else []
    n = int(lines[1]) if len(lines) > 1 else 0

    # Compute correct answer
    correct = _reference_least_interval(tasks, n)

    try:
        actual_val = int(actual) if not isinstance(actual, int) else actual
        return actual_val == correct
    except (ValueError, TypeError):
        return False


def _reference_least_interval(tasks: List[str], n: int) -> int:
    """Reference implementation using math formula."""
    task_counts = Counter(tasks)
    max_freq = max(task_counts.values())
    max_freq_count = sum(1 for count in task_counts.values() if count == max_freq)

    formula_time = (max_freq - 1) * (n + 1) + max_freq_count
    return max(formula_time, len(tasks))


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Mathematical Formula
# Time: O(n), Space: O(1) (26 letters max)
#
# Pattern: heap_task_scheduler (math variant)
# See: docs/patterns/heap/templates.md Section 6 (Task Scheduler)
# ============================================================================
class SolutionMath:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        """
        Calculate minimum intervals using mathematical formula.

        Key Observation:
        - Most frequent task determines the "frame" structure
        - Frame: chunks of size (n+1), each containing one instance of max-freq task

        Formula:
        - frames = (max_freq - 1)
        - frame_size = n + 1
        - base_time = frames * frame_size
        - Add tasks with max_freq (they fill the last partial frame)

        Example: tasks = [A,A,A,B,B,B], n = 2, max_freq = 3
        Frame 1: A B _
        Frame 2: A B _
        Frame 3: A B
        Total: (3-1) * 3 + 2 = 8

        Edge Case:
        - If total tasks > formula result, no idle needed
        - Just return len(tasks)
        """
        # Count task frequencies
        task_counts: dict[str, int] = Counter(tasks)

        # Find maximum frequency
        max_freq = max(task_counts.values())

        # Count how many tasks have maximum frequency
        max_freq_count = sum(1 for count in task_counts.values() if count == max_freq)

        # Formula: (max_freq - 1) frames × (n + 1) slots + max_freq_count final slots
        formula_time = (max_freq - 1) * (n + 1) + max_freq_count

        # Actual time is max of formula and total tasks
        # (when many different tasks, no idle needed)
        return max(formula_time, len(tasks))


# ============================================================================
# Solution 2: Greedy Scheduling with Max-Heap
# Time: O(n * m), Space: O(k)
#   where n = cooldown, m = total tasks, k = unique tasks
#
# Pattern: heap_task_scheduler
# See: docs/patterns/heap/templates.md Section 6 (Task Scheduler)
# ============================================================================
class SolutionHeap:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        """
        Schedule tasks using greedy max-heap approach.

        Strategy:
        1. Greedily pick most frequent available task
        2. Track cooldown using a queue (task available at time t)
        3. If no task available, idle (time still advances)

        Why max-heap?
        - Always process high-frequency tasks first
        - Minimizes idle time at the end
        - Max-heap gives O(log k) access to most frequent
        """
        # Count task frequencies
        task_counts: dict[str, int] = Counter(tasks)

        # Max-heap of remaining counts (negate for max-heap)
        max_heap = [-count for count in task_counts.values()]
        heapq.heapify(max_heap)

        # Queue of (available_time, remaining_count) for tasks in cooldown
        cooldown_queue: deque[tuple[int, int]] = deque()

        time = 0

        while max_heap or cooldown_queue:
            time += 1

            # Check if any task exits cooldown
            if cooldown_queue and cooldown_queue[0][0] == time:
                available_time, remaining = cooldown_queue.popleft()
                heapq.heappush(max_heap, -remaining)

            if max_heap:
                # Execute most frequent available task
                count = -heapq.heappop(max_heap)
                count -= 1

                if count > 0:
                    # Task has more instances, put in cooldown
                    cooldown_queue.append((time + n + 1, count))
            # else: idle (no task available)

        return time


def solve():
    """
    Input format (JSON per line):
        Line 1: tasks as JSON array of strings
        Line 2: n as integer (cooldown period)

    Output format:
        Integer - minimum number of intervals
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    tasks = json.loads(lines[0])
    n = int(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.leastInterval(tasks, n)

    print(result)


if __name__ == "__main__":
    solve()

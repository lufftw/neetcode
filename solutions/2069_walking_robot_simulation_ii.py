"""
Problem: Walking Robot Simulation II
Link: https://leetcode.com/problems/walking-robot-simulation-ii/

Implement a Robot class that simulates walking on a grid perimeter.
Robot starts at (0,0) facing East and can step forward num steps.

Constraints:
- 2 <= width, height <= 100
- 1 <= num <= 10^5
- At most 10^4 calls to step, getPos, and getDir

Topics: Design, Simulation
"""
from typing import List
from _runner import get_solver
import json


SOLUTIONS = {
    "default": {
        "class": "Robot",
        "method": "",
        "complexity": "O(1) per operation (amortized)",
        "description": "Perimeter modular arithmetic with direction lookup",
    },
}


# Reference implementation for JUDGE_FUNC (simulation-based)
class _ReferenceRobot:
    """Naive simulation for verification."""
    def __init__(self, width: int, height: int):
        self.w = width
        self.h = height
        self.x = 0
        self.y = 0
        self.direction = 0  # 0=East, 1=North, 2=West, 3=South
        self.dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.dir_names = ["East", "North", "West", "South"]

    def step(self, num: int) -> None:
        # Optimize with modulo on perimeter
        perimeter = 2 * (self.w - 1) + 2 * (self.h - 1)
        num = num % perimeter
        if num == 0:
            num = perimeter  # Must move at least once to set direction

        for _ in range(num):
            dx, dy = self.dirs[self.direction]
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < self.w and 0 <= ny < self.h:
                self.x, self.y = nx, ny
            else:
                self.direction = (self.direction + 1) % 4
                dx, dy = self.dirs[self.direction]
                self.x, self.y = self.x + dx, self.y + dy

    def getPos(self):
        return [self.x, self.y]

    def getDir(self):
        return self.dir_names[self.direction]


def judge(actual, expected, input_data: str) -> bool:
    if isinstance(actual, str):
        actual = json.loads(actual)
    if expected is not None:
        if isinstance(expected, str):
            expected = json.loads(expected)
        return actual == expected
    # Use reference implementation
    lines = input_data.strip().split('\n')
    methods = json.loads(lines[0])
    args = json.loads(lines[1])

    ref_results = []
    ref_obj = None
    for method, arg in zip(methods, args):
        if method == "Robot":
            ref_obj = _ReferenceRobot(*arg)
            ref_results.append(None)
        elif method == "step":
            ref_obj.step(*arg)
            ref_results.append(None)
        elif method == "getPos":
            ref_results.append(ref_obj.getPos())
        elif method == "getDir":
            ref_results.append(ref_obj.getDir())
    return actual == ref_results


JUDGE_FUNC = judge


# ============================================================================
# Solution: Perimeter Modular Arithmetic
# Time: O(1) per step (using modulo), O(1) for getPos/getDir
# Space: O(1)
# ============================================================================
class Robot:
    # Key insight:
    #   - Robot only moves on the perimeter (2*(w-1) + 2*(h-1) cells)
    #   - Use modular arithmetic: position = (position + num) % perimeter
    #   - Map linear position to (x, y, direction)
    #
    # Perimeter traversal order (counterclockwise when hitting bounds):
    #   Bottom edge: (0,0) to (w-1, 0) facing East
    #   Right edge: (w-1, 0) to (w-1, h-1) facing North
    #   Top edge: (w-1, h-1) to (0, h-1) facing West
    #   Left edge: (0, h-1) to (0, 0) facing South
    #
    # Special case: At origin (0,0) after moving, face South (not East)

    def __init__(self, width: int, height: int):
        self.w = width
        self.h = height
        self.perimeter = 2 * (width - 1) + 2 * (height - 1)
        self.pos = 0  # Linear position on perimeter
        self.moved = False  # Track if robot has moved (affects direction at origin)

    def step(self, num: int) -> None:
        self.moved = True
        self.pos = (self.pos + num) % self.perimeter

    def getPos(self) -> List[int]:
        pos = self.pos
        w, h = self.w, self.h

        # Bottom edge: positions [0, w-1), moving right
        if pos < w - 1:
            return [pos, 0]
        pos -= w - 1

        # Right edge: positions [0, h-1), moving up
        if pos < h - 1:
            return [w - 1, pos]
        pos -= h - 1

        # Top edge: positions [0, w-1), moving left
        if pos < w - 1:
            return [w - 1 - pos, h - 1]
        pos -= w - 1

        # Left edge: positions [0, h-1), moving down
        return [0, h - 1 - pos]

    def getDir(self) -> str:
        pos = self.pos
        w, h = self.w, self.h

        # Bottom edge (including origin)
        if pos < w - 1:
            # Special case: origin after moving faces South
            if pos == 0 and self.moved:
                return "South"
            return "East"
        pos -= w - 1

        # Right edge (including bottom-right corner)
        if pos < h - 1:
            if pos == 0:
                return "East"  # At corner, came from East direction
            return "North"
        pos -= h - 1

        # Top edge (including top-right corner)
        if pos < w - 1:
            if pos == 0:
                return "North"  # At corner, came from North direction
            return "West"
        pos -= w - 1

        # Left edge (including top-left corner, excluding origin)
        if pos == 0:
            return "West"  # At top-left corner
        return "South"


# ============================================================================
# solve() - stdin/stdout interface for OOP design problems
# ============================================================================
def solve():
    """
    Input format:
        Line 1: JSON array of method names
        Line 2: JSON array of arguments

    Example:
        ["Robot","step","step","getPos","getDir"]
        [[6,3],[2],[2],[],[]]
        -> [null,null,null,[4,0],"East"]
    """
    import sys

    lines = sys.stdin.read().strip().split('\n')
    methods = json.loads(lines[0])
    args = json.loads(lines[1])

    results = []
    obj = None

    for method, arg in zip(methods, args):
        if method == "Robot":
            obj = Robot(*arg)
            results.append(None)
        elif method == "step":
            obj.step(*arg)
            results.append(None)
        elif method == "getPos":
            results.append(obj.getPos())
        elif method == "getDir":
            results.append(obj.getDir())

    print(json.dumps(results, separators=(',', ':')))


if __name__ == "__main__":
    solve()

# New Pattern Development Guide

> **Status**: Canonical Reference
> **Scope**: End-to-end workflow for adding a new algorithm pattern
> **Last Updated**: {{ git_revision_date_localized }}
> **Created**: {{ git_creation_date_localized }}

This guide describes the complete workflow for developing a new algorithm pattern in this repository. Follow these phases sequentially to ensure all components are properly integrated.

---

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Phase 1: Solution Files](#phase-1-solution-files)
- [Phase 2: Test Infrastructure](#phase-2-test-infrastructure)
- [Phase 3: Pattern Documentation](#phase-3-pattern-documentation)
- [Phase 4: Ontology and Metadata](#phase-4-ontology-and-metadata)
- [Phase 5: Mindmap Integration](#phase-5-mindmap-integration)
- [Phase 6: Version Control](#phase-6-version-control)
- [Quick Reference Checklist](#quick-reference-checklist)
- [Example: Monotonic Stack Pattern](#example-monotonic-stack-pattern)

---

## Overview

A complete pattern implementation consists of these components:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Pattern Development Pipeline                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Phase 1: Solutions        Phase 2: Tests          Phase 3: Documentation   │
│  ┌──────────────────┐     ┌──────────────────┐    ┌──────────────────┐     │
│  │ solutions/*.py   │────▶│ generators/*.py  │───▶│ meta/patterns/   │     │
│  │ - SOLUTIONS dict │     │ tests/*.in/out   │    │ docs/patterns/   │     │
│  │ - JUDGE_FUNC     │     └──────────────────┘    └──────────────────┘     │
│  └──────────────────┘                                      │                │
│                                                            ▼                │
│  Phase 4: Ontology         Phase 5: Mindmaps      Phase 6: Version Control │
│  ┌──────────────────┐     ┌──────────────────┐    ┌──────────────────┐     │
│  │ ontology/*.toml  │────▶│ ai-markmap-agent │───▶│ git commit       │     │
│  │ roadmaps/*.toml  │     │ config.yaml      │    │ gh pr create     │     │
│  │ meta/problems/   │     └──────────────────┘    └──────────────────┘     │
│  └──────────────────┘                                                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Deliverables Summary

| Phase | Directory | Files Created |
|-------|-----------|---------------|
| 1 | `solutions/` | `{id}_{slug}.py` for each problem |
| 2 | `generators/`, `tests/` | Generator + 5-7 test cases per problem |
| 3 | `meta/patterns/`, `docs/patterns/` | Pattern snippets + intuition.md + templates.md |
| 4 | `ontology/`, `roadmaps/`, `meta/problems/` | Taxonomy + learning path + problem metadata |
| 5 | `tools/mindmaps/` | Config updates for AI mindmap generation |
| 6 | Git | Feature branch + PR |

---

## Prerequisites

Before starting, ensure you have:

1. **Problem Selection**: Identify 8-15 LeetCode problems that represent the pattern
2. **Pattern Analysis**: Understand the core algorithm and its variations
3. **Learning Order**: Determine the pedagogical progression (base → variants → advanced)

### Recommended Problem Selection

| Role | Count | Description |
|------|-------|-------------|
| Base Template | 1-2 | Canonical problem that teaches the core pattern |
| Direct Variants | 3-5 | Same pattern with minor modifications |
| Advanced Applications | 3-5 | Complex problems combining the pattern with others |
| Edge Cases | 1-2 | Problems that test edge case handling |

---

## Phase 1: Solution Files

### 1.1 Create Solution Skeleton

For each problem, create a solution file in `solutions/`:

```bash
# Option A: Use CodeGen (recommended for new problems)
python -m codegen new <leetcode_id> --with-tests

# Option B: Manual creation
# Create: solutions/{id:04d}_{slug}.py
```

### 1.2 Solution File Structure

Every solution file MUST follow this exact structure. See [Solution Contract](../contracts/solution-contract.md) for complete specification.

#### Required Elements

| Element | Required | Description |
|---------|----------|-------------|
| File-level docstring | ✅ | Problem description with Link, Examples, Constraints |
| `from _runner import get_solver` | ✅ | Required import for polymorphic dispatch |
| `SOLUTIONS` dict | ✅ | Metadata with `"default"` key required |
| Solution class(es) | ✅ | One or more classes implementing the solution |
| `JUDGE_FUNC` | ✅ | Custom validation (required for pattern problems) |
| `solve()` function | ✅ | Entry point for stdin/stdout execution |

#### Complete Solution Template

```python
# solutions/0496_next_greater_element_i.py
"""
Problem: Next Greater Element I
Link: https://leetcode.com/problems/next-greater-element-i/

The next greater element of some element x in an array is the first greater
element that is to the right of x in the same array.
You are given two distinct 0-indexed integer arrays nums1 and nums2, where
nums1 is a subset of nums2.

Example 1:
    Input: nums1 = [4,1,2], nums2 = [1,3,4,2]
    Output: [-1,3,-1]
    Explanation: The next greater element for each value of nums1 is as follows:
                 - 4 is underlined in nums2 = [1,3,4,2]. There is no next greater element, so the answer is -1.
                 - 1 is underlined in nums2 = [1,3,4,2]. The next greater element is 3.
                 - 2 is underlined in nums2 = [1,3,4,2]. There is no next greater element, so the answer is -1.

Example 2:
    Input: nums1 = [2,4], nums2 = [1,2,3,4]
    Output: [3,-1]

Constraints:
- 1 <= nums1.length <= nums2.length <= 1000
- 0 <= nums1[i], nums2[i] <= 10^4
- All integers in nums1 and nums2 are unique.
- All the integers of nums1 also appear in nums2.

Topics: Array, Hash Table, Stack, Monotonic Stack
"""

import json
from typing import List

from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "SolutionMonotonicStack",
        "method": "nextGreaterElement",
        "complexity": "O(n + m) time, O(n) space",
        "description": "Monotonic decreasing stack with hash map lookup",
    },
    "stack": {
        "class": "SolutionMonotonicStack",
        "method": "nextGreaterElement",
        "complexity": "O(n + m) time, O(n) space",
        "description": "Monotonic decreasing stack with hash map lookup",
    },
    "brute": {
        "class": "SolutionBruteForce",
        "method": "nextGreaterElement",
        "complexity": "O(m * n) time, O(1) space",
        "description": "Linear scan for each query element",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for generator support
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """
    Validate result: check if actual output is the correct NGE array.

    Args:
        actual: Program output (list as string or list)
        expected: Expected output (None if from generator)
        input_data: Raw input string (nums1 and nums2 on separate lines)

    Returns:
        bool: True if correct NGE results
    """
    lines = input_data.strip().split("\n")
    nums1 = json.loads(lines[0]) if lines[0] else []
    nums2 = json.loads(lines[1]) if len(lines) > 1 else []

    # Compute correct answer using reference solution
    correct = _reference_nge(nums1, nums2)

    # Parse actual output (may be list or string)
    if isinstance(actual, list):
        actual_list = actual
    else:
        actual_str = actual.strip()
        try:
            actual_list = json.loads(actual_str) if actual_str else []
        except (ValueError, json.JSONDecodeError):
            return False

    return actual_list == correct


def _reference_nge(nums1: List[int], nums2: List[int]) -> List[int]:
    """O(n + m) reference using monotonic stack."""
    nge_map: dict[int, int] = {}
    stack: list[int] = []

    for num in nums2:
        while stack and stack[-1] < num:
            nge_map[stack.pop()] = num
        stack.append(num)

    return [nge_map.get(x, -1) for x in nums1]


JUDGE_FUNC = judge


# ============================================================================
# Solution 1: Monotonic Decreasing Stack + Hash Map
# Time: O(n + m), Space: O(n)
#   - Precompute NGE for all elements in nums2 using monotonic stack
#   - Stack stores indices of candidates awaiting their next greater element
#   - When a larger element appears, it becomes NGE for all smaller candidates
#   - Hash map enables O(1) lookup for nums1 queries
#
# Key Insight: The stack maintains a decreasing sequence of unresolved elements.
# When we encounter a larger element, it "resolves" all smaller elements on top.
# ============================================================================
class SolutionMonotonicStack:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        next_greater_map: dict[int, int] = {}
        candidate_stack: list[int] = []  # Stores values (not indices) since unique

        # Build NGE map: process nums2 to find next greater for each element
        for current_value in nums2:
            # Resolve all candidates that found their next greater element
            while candidate_stack and candidate_stack[-1] < current_value:
                resolved_value = candidate_stack.pop()
                next_greater_map[resolved_value] = current_value

            # Current element becomes a new candidate awaiting its NGE
            candidate_stack.append(current_value)

        # Elements remaining in stack have no next greater element
        # They will return -1 via dict.get() default

        # Look up NGE for each query element
        return [next_greater_map.get(query, -1) for query in nums1]


# ============================================================================
# Solution 2: Brute Force Linear Scan
# Time: O(m * n), Space: O(1)
#   - For each element in nums1, find its position in nums2
#   - Scan right from that position to find the first greater element
#   - Simple but inefficient for large inputs
#
# Educational Value: Establishes baseline before optimization.
# ============================================================================
class SolutionBruteForce:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        result: list[int] = []
        nums2_length = len(nums2)

        for query in nums1:
            # Find position of query element in nums2
            position = nums2.index(query)

            # Scan rightward for next greater element
            next_greater = -1
            for scan_idx in range(position + 1, nums2_length):
                if nums2[scan_idx] > query:
                    next_greater = nums2[scan_idx]
                    break

            result.append(next_greater)

        return result


def solve():
    """
    Input format (JSON per line):
        Line 1: nums1 as JSON array
        Line 2: nums2 as JSON array

    Output format:
        JSON array of next greater elements
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    nums1 = json.loads(lines[0])
    nums2 = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.nextGreaterElement(nums1, nums2)

    print(json.dumps(result))


if __name__ == "__main__":
    solve()
```

### 1.3 File-Level Docstring Requirements

The docstring MUST include:

| Field | Required | Format |
|-------|----------|--------|
| `Problem:` | ✅ | Problem title |
| `Link:` | ✅ | `https://leetcode.com/problems/{slug}/` (NO `/description/` suffix) |
| Description | ✅ | Problem statement |
| `Example N:` | ✅ | At least one example with Input/Output/Explanation |
| `Constraints:` | ✅ | All LeetCode constraints |
| `Topics:` | Recommended | LeetCode topic tags |

### 1.4 SOLUTIONS Dict Requirements

| Rule | Requirement |
|------|-------------|
| `"default"` key | ✅ REQUIRED - used when no `--method` flag specified |
| `"class"` field | ✅ REQUIRED - must match actual class name in file |
| `"method"` field | ✅ REQUIRED - must match LeetCode method signature |
| `"complexity"` field | Recommended - e.g., `"O(n) time, O(n) space"` |
| `"description"` field | Recommended - brief algorithm description |

### 1.5 Solution Block Comment Format

**CRITICAL**: No blank line between comment block and class definition.

```python
# ============================================================================
# Solution N: {Approach Name}
# Time: O(?), Space: O(?)
#   - {Key insight 1}
#   - {Key insight 2}
#   - {Implementation detail}
#
# {Optional extended explanation}
# ============================================================================
class SolutionName:   # ← NO blank line here
    def methodName(self, ...):
        ...
```

### 1.6 JUDGE_FUNC Requirements

The `JUDGE_FUNC` is **mandatory** for pattern problems. Key requirements:

| Requirement | Description |
|-------------|-------------|
| Handle both types | `actual` may be `list` or `str` depending on context |
| Support `expected=None` | Generated tests have no expected output |
| Reference solution | Include `_reference_{name}()` helper to compute correct answer |
| Parse `input_data` | Use `json.loads()` to parse input |
| Return boolean | `True` for pass, `False` for fail |

#### JUDGE_FUNC Template

```python
def judge(actual, expected, input_data: str) -> bool:
    """Validate result."""
    # 1. Parse input
    lines = input_data.strip().split("\n")
    param1 = json.loads(lines[0])
    param2 = json.loads(lines[1]) if len(lines) > 1 else None

    # 2. Compute correct answer using reference
    correct = _reference_solution(param1, param2)

    # 3. Parse actual (handle both list and string)
    if isinstance(actual, list):
        actual_list = actual
    else:
        actual_str = actual.strip()
        try:
            actual_list = json.loads(actual_str) if actual_str else []
        except (ValueError, json.JSONDecodeError):
            return False

    # 4. Compare
    return actual_list == correct


def _reference_solution(param1, param2):
    """Reference implementation for validation."""
    # Implement correct algorithm here
    pass


JUDGE_FUNC = judge
```

### 1.7 solve() Function Requirements

```python
def solve():
    """
    Input format (JSON per line):
        Line 1: {param1 description}
        Line 2: {param2 description}

    Output format:
        {output description}
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")
    param1 = json.loads(lines[0])
    param2 = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.methodName(param1, param2)

    print(json.dumps(result))  # Use json.dumps for arrays


if __name__ == "__main__":
    solve()
```

> **Reference**: [Solution Contract](../contracts/solution-contract.md)

---

## Phase 2: Test Infrastructure

### 2.1 Create Test Generator

For each problem, create a generator in `generators/`:

```python
# generators/0496_next_greater_element_i.py
"""
Test Case Generator for Problem 496 - Next Greater Element I

LeetCode Constraints:
- 1 <= nums1.length <= 1000
- 1 <= nums2.length <= 1000
- 0 <= nums1[i], nums2[i] <= 10^4
- All integers in nums1 and nums2 are unique
- All integers of nums1 also appear in nums2
"""
import json
import random
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Test input in .in file format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        ([4, 1, 2], [1, 3, 4, 2]),      # Classic example
        ([2, 4], [1, 2, 3, 4]),          # All have next greater
        ([4, 3, 2, 1], [4, 3, 2, 1]),    # Decreasing - all -1
        ([1], [1]),                       # Single element
    ]

    for nums1, nums2 in edge_cases:
        yield f"{json.dumps(nums1, separators=(',', ':'))}\n{json.dumps(nums2, separators=(',', ':'))}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_case()


def _generate_case() -> str:
    """Generate a single valid random test case."""
    # Generate nums2 with unique values
    size2 = random.randint(5, 100)
    nums2 = random.sample(range(10001), size2)

    # nums1 is a subset of nums2
    size1 = random.randint(1, min(size2, 50))
    nums1 = random.sample(nums2, size1)

    return f"{json.dumps(nums1, separators=(',', ':'))}\n{json.dumps(nums2, separators=(',', ':'))}"


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size for complexity estimation."""
    nums2 = list(range(n))
    random.shuffle(nums2)
    nums1 = random.sample(nums2, min(n, n // 2 + 1))
    return f"{json.dumps(nums1, separators=(',', ':'))}\n{json.dumps(nums2, separators=(',', ':'))}"
```

> **Reference**: [Generator Contract](../contracts/generator-contract.md)

### 2.2 Generate Test Files

Use the generator to create input files, then run solutions to create output files:

```bash
# Step 1: Generate input files
cd /path/to/neetcode

# Using Python to generate inputs
python -c "
from generators.{problem} import generate
import json

for i, test_input in enumerate(generate(count=7, seed=42), 1):
    with open(f'tests/{problem}_{i}.in', 'w', newline='\n') as f:
        f.write(test_input)
    print(f'Created tests/{problem}_{i}.in')
"

# Step 2: Generate outputs by running the solution
for i in 1 2 3 4 5 6 7; do
    python solutions/{problem}.py < tests/{problem}_${i}.in > tests/{problem}_${i}.out
done
```

### 2.3 Run Tests to Verify

```bash
# Test single problem
python runner/test_runner.py {problem_id}

# Test all problems in pattern (example for monotonic stack)
python runner/test_runner.py 0042 0084 0085 0316 0321 0402 0496 0503 0739 0901 0907 2104

# Run with generated tests
python runner/test_runner.py {problem_id} --generate 10 --seed 42
```

### 2.4 Test File Format

Files must use canonical JSON format:

```
tests/{problem_id}_{slug}_{n}.in   # Input file
tests/{problem_id}_{slug}_{n}.out  # Expected output file
```

| Rule | Correct | Incorrect |
|------|---------|-----------|
| No spaces after comma | `[1,2,3]` | `[1, 2, 3]` |
| Double quotes | `"hello"` | `'hello'` |
| Lowercase booleans | `true` | `True` |
| LF line endings | `\n` | `\r\n` |

> **Reference**: [Test File Format](../contracts/test-file-format.md)

---

## Phase 3: Pattern Documentation

### 3.1 Create Meta Pattern Directory

Create pattern snippets in `meta/patterns/{pattern_name}/`:

```
meta/patterns/{pattern_name}/
├── _config.toml          # Pattern configuration
├── _header.md            # Core concepts
├── _templates.md         # Code templates
├── _comparison.md        # Comparison with similar patterns
├── _decision.md          # Decision tree for when to use
├── _mapping.md           # Maps sub-patterns to problems
├── _robustness.md        # Common pitfalls
├── _termination.md       # Loop invariants and termination
└── {problem_id}-{topic}.md  # Problem-specific snippets
```

#### _config.toml

```toml
[pattern]
id = "monotonic_stack"
name = "Monotonic Stack"
api_kernel = "MonotonicStack"

[order]
# Order of sections in generated templates.md
header = 1
templates = 2
comparison = 3
decision = 4
mapping = 5
robustness = 6
termination = 7
problems = 100  # Problem snippets come last

[problems]
# Problem snippets to include
include = [
    "0496-next-greater-element",
    "0739-span-distance",
    "0084-histogram-expansion",
    "0907-contribution-counting",
    "0042-container-valley",
    "0402-greedy-monotonic",
    "0503-circular-boundary",
]
```

#### _header.md

```markdown
# Monotonic Stack Pattern

## Core Concept

A **monotonic stack** maintains elements in sorted order (increasing or decreasing).
When a new element violates the monotonic property, we pop elements until the
property is restored.

## When to Use

- Finding next/previous greater/smaller element
- Calculating spans or distances
- Problems involving "dominated" elements
- Histogram-based area calculations

## Template Selection

| Sub-Pattern | Use When |
|-------------|----------|
| Next Greater | Find first larger element to the right |
| Span Calculation | Count consecutive dominated elements |
| Contribution | Sum contributions of each element |
| Histogram | Find maximum rectangle area |
```

### 3.2 Generate Documentation

Run the pattern documentation generator:

```bash
# Generate templates.md from meta/patterns sources
python tools/patterndocs/generate_pattern_docs.py {pattern_name}

# Example
python tools/patterndocs/generate_pattern_docs.py monotonic_stack
```

This creates `docs/patterns/{pattern_name}/templates.md`.

### 3.3 Create Intuition Guide

Manually create `docs/patterns/{pattern_name}/intuition.md`:

```markdown
# Monotonic Stack: Intuition Guide

## The Mental Model

Imagine a line of people waiting, where shorter people can't see past taller ones...

## Sub-Pattern Recognition

### Next Greater Element
**Signal**: "Find the next element that is greater/smaller"

### Span Calculation
**Signal**: "Count consecutive days/elements where condition holds"

## Common Pitfalls

1. **Duplicate handling**: Use `<=` vs `<` carefully
2. **Boundary elements**: Don't forget elements that never get popped

## Practice Progression

1. Start with 496 (basic next greater)
2. Move to 739 (span calculation)
3. Try 84 (histogram - combines concepts)
```

---

## Phase 4: Ontology and Metadata

### 4.1 Update ontology/patterns.toml

Add new patterns to the ontology:

```toml
# ontology/patterns.toml

# Add under appropriate section
[[patterns]]
id = "next_greater_element"
api_kernel = "MonotonicStack"
summary = "Find next greater element for each position."

[[patterns]]
id = "monotonic_stack_span"
api_kernel = "MonotonicStack"
summary = "Count consecutive dominated elements (span calculation)."

[[patterns]]
id = "monotonic_stack_contribution"
api_kernel = "MonotonicStack"
summary = "Sum contributions using boundary products (subarray min/max sums)."

# Add more sub-patterns as needed...
```

### 4.2 Update ontology/roadmaps.toml

Register the new roadmap:

```toml
# ontology/roadmaps.toml

[[roadmaps]]
id = "monotonic_stack_path"
name = "Monotonic Stack Mastery"
summary = "Step-by-step path to master monotonic stack patterns."
```

### 4.3 Create Roadmap File

Create `roadmaps/{pattern}_path.toml`:

```toml
# roadmaps/monotonic_stack_path.toml

# Roadmap metadata
id = "monotonic_stack_path"
name = "Monotonic Stack Mastery Path"
api_kernel = "MonotonicStack"

# Learning steps in order
[[steps]]
order = 1
problem = "0496_next_greater_element_i"
role = "base"
pattern = "next_greater_element"
prerequisite = []
delta = ""
note = "Learn the canonical monotonic stack template with next greater element."

[[steps]]
order = 2
problem = "0503_next_greater_element_ii"
role = "variant"
pattern = "monotonic_stack_circular"
prerequisite = ["0496"]
delta = "Circular array handling with 2n traversal."
note = "Extends base pattern to circular arrays using modulo indexing."

[[steps]]
order = 3
problem = "0739_daily_temperatures"
role = "variant"
pattern = "monotonic_stack_span"
prerequisite = ["0496"]
delta = "Track distance instead of value."
note = "Same pattern, different output format (distance vs value)."

# Continue with remaining problems...
```

### 4.4 Create Problem Metadata Files

For each problem, create `meta/problems/{id}_{slug}.toml`:

```toml
# meta/problems/0496_next_greater_element_i.toml

# ===== Problem Info =====
id = "0496"
slug = "0496_next_greater_element_i"
title = "Next Greater Element I"
leetcode_id = 496
url = "https://leetcode.com/problems/next-greater-element-i/"

# ===== LeetCode Official Metadata =====
difficulty = "easy"
topics = ["array", "hash_table", "stack", "monotonic_stack"]
companies = ["amazon", "google", "meta"]

# ===== Roadmaps =====
roadmaps = ["monotonic_stack_path"]

# ===== Ontology Tags (Problem Level) =====
api_kernels      = ["MonotonicStack"]
patterns         = ["next_greater_element"]
families         = ["stack_monotonic"]
data_structures  = ["array", "stack", "hash_table"]
algorithms       = ["monotonic_stack"]
related_problems = ["0503", "0739", "0901"]

# ===== File Locations =====
[files]
solution  = "solutions/0496_next_greater_element_i.py"
generator = "generators/0496_next_greater_element_i.py"
tests_dir = "tests/"

# ===== Solutions =====
[[solutions]]
key    = "default"
class  = "SolutionStack"
method = "nextGreaterElement"

api_kernels      = ["MonotonicStack"]
patterns         = ["next_greater_element"]
families         = ["stack_monotonic"]
data_structures  = ["array", "stack", "hash_table"]
algorithms       = ["monotonic_stack"]

role       = "base"
variant    = ""
based_on   = []
delta      = "Canonical next greater element with hash map lookup."
complexity = "O(n + m) time, O(n) space"
notes      = "Base template for all monotonic stack problems."
```

---

## Phase 5: Mindmap Integration

### 5.1 Update AI Markmap Agent Config

Edit `tools/mindmaps/ai-markmap-agent/config/config.yaml`:

```yaml
data_sources:
  # Add pattern directory
  patterns:
    enabled: true
    directories:
      - name: "sliding_window"
        path: "sliding_window"
        enabled: true
        config_file: "_config.toml"
      # Add new pattern
      - name: "monotonic_stack"
        path: "monotonic_stack"
        enabled: true
        config_file: "_config.toml"

  # Add roadmap file
  roadmaps:
    enabled: true
    files:
      - name: "sliding_window_path"
        path: "sliding_window_path.toml"
        enabled: true
      # Add new roadmap
      - name: "monotonic_stack_path"
        path: "monotonic_stack_path.toml"
        enabled: true
```

### 5.2 Verify Configuration

The following configs auto-include new content (no changes needed):

| Config File | Behavior |
|-------------|----------|
| `tools/mindmaps/generate_mindmaps_ai.toml` | Empty `include = []` means all files |
| `tools/mindmaps/generate_mindmaps.toml` | SEO descriptions only |

---

## Phase 6: Version Control

### 6.1 Create Feature Branch

```bash
git checkout -b feat/{pattern-name}-pattern
```

### 6.2 Commit Changes

Organize commits by phase:

```bash
# Commit solutions
git add solutions/*.py
git commit -m "feat(solutions): add {pattern} solution files with test cases"

# Commit generators and tests
git add generators/*.py tests/*.in tests/*.out
git commit -m "test: add test generators and cases for {pattern} problems"

# Commit documentation
git add meta/patterns/{pattern}/ docs/patterns/{pattern}/
git commit -m "docs({pattern}): add pattern documentation and intuition guide"

# Commit ontology and metadata
git add ontology/*.toml roadmaps/*.toml meta/problems/*.toml
git commit -m "feat(ontology): add {pattern} patterns, roadmap, and problem metadata"

# Commit mindmap config
git add tools/mindmaps/
git commit -m "chore: update mindmap configs for {pattern}"
```

### 6.3 Push and Create PR

```bash
# Push branch
git push -u origin feat/{pattern-name}-pattern

# Create PR
gh pr create --title "feat: Complete {Pattern Name} Pattern Implementation" --body "$(cat <<'EOF'
## Summary

- Implement complete {Pattern Name} pattern with N LeetCode problems
- Add comprehensive documentation, generators, and test infrastructure
- Update ontology with new patterns and learning roadmap

## Changes

### Solutions (N problems)
- Problem 1
- Problem 2
- ...

### Documentation
- `docs/patterns/{pattern}/intuition.md` - Story-based learning guide
- `docs/patterns/{pattern}/templates.md` - Generated code templates
- `meta/patterns/{pattern}/` - Source pattern snippets

### Infrastructure
- N test generators in `generators/`
- M test files in `tests/`
- JUDGE_FUNC added to all solution files

### Ontology & Metadata
- X new patterns in `ontology/patterns.toml`
- `{pattern}_path` roadmap with Y-step learning path
- N problem metadata files in `meta/problems/`
- Updated ai-markmap-agent config

## Test plan

- [ ] All solutions pass tests
- [ ] Test generators produce valid input/output pairs
- [ ] JUDGE_FUNC handles both list and string types
- [ ] Documentation builds correctly
EOF
)"
```

---

## Quick Reference Checklist

### Pre-Development

- [ ] Identify 8-15 representative problems
- [ ] Analyze pattern and variations
- [ ] Determine learning progression order

### Phase 1: Solutions

- [ ] Create `solutions/{id}_{slug}.py` for each problem
- [ ] Include `SOLUTIONS` dict with metadata
- [ ] Implement `JUDGE_FUNC` that handles both types
- [ ] Add `solve()` entry point

### Phase 2: Tests

- [ ] Create `generators/{id}_{slug}.py` for each problem
- [ ] Generate 5-7 test cases per problem
- [ ] Verify all tests pass with `python runner/test_runner.py`
- [ ] Fix any CRLF line ending issues

### Phase 3: Documentation

- [ ] Create `meta/patterns/{pattern}/_config.toml`
- [ ] Create `meta/patterns/{pattern}/_header.md`
- [ ] Create `meta/patterns/{pattern}/_templates.md`
- [ ] Create problem snippets `{id}-{topic}.md`
- [ ] Generate `docs/patterns/{pattern}/templates.md`
- [ ] Write `docs/patterns/{pattern}/intuition.md`
- [ ] Update `docs/patterns/README.md`

### Phase 4: Ontology

- [ ] Add patterns to `ontology/patterns.toml`
- [ ] Add roadmap to `ontology/roadmaps.toml`
- [ ] Create `roadmaps/{pattern}_path.toml`
- [ ] Create `meta/problems/{id}_{slug}.toml` for each problem

### Phase 5: Mindmaps

- [ ] Update `tools/mindmaps/ai-markmap-agent/config/config.yaml`

### Phase 6: Version Control

- [ ] Create feature branch
- [ ] Commit changes by phase
- [ ] Push and create PR
- [ ] Merge to main after review

---

## Example: Monotonic Stack Pattern

The Monotonic Stack pattern implementation serves as a reference:

| Component | Count | Location |
|-----------|-------|----------|
| Solutions | 12 | `solutions/0042_*.py`, `solutions/0084_*.py`, ... |
| Generators | 12 | `generators/0042_*.py`, `generators/0084_*.py`, ... |
| Test files | 84 | `tests/0042_*`, `tests/0084_*`, ... |
| Pattern snippets | 15 | `meta/patterns/monotonic_stack/*` |
| Docs | 2 | `docs/patterns/monotonic_stack/intuition.md`, `templates.md` |
| Problem metadata | 12 | `meta/problems/0042_*.toml`, ... |
| Roadmap | 1 | `roadmaps/monotonic_stack_path.toml` |
| Ontology patterns | 10 | Added to `ontology/patterns.toml` |

### Problems in Monotonic Stack Pattern

| ID | Problem | Role | Sub-Pattern |
|----|---------|------|-------------|
| 0496 | Next Greater Element I | Base | next_greater_element |
| 0503 | Next Greater Element II | Variant | circular |
| 0739 | Daily Temperatures | Variant | span |
| 0901 | Online Stock Span | Variant | span |
| 0084 | Largest Rectangle in Histogram | Advanced | histogram |
| 0085 | Maximal Rectangle | Advanced | matrix_histogram |
| 0907 | Sum of Subarray Minimums | Advanced | contribution |
| 2104 | Sum of Subarray Ranges | Advanced | contribution |
| 0042 | Trapping Rain Water | Advanced | container |
| 0402 | Remove K Digits | Advanced | greedy |
| 0316 | Remove Duplicate Letters | Advanced | lexicographic |
| 0321 | Create Maximum Number | Advanced | greedy_selection |

---

## Related Documentation

| Document | Content |
|----------|---------|
| [Solution Contract](../contracts/solution-contract.md) | Solution file requirements |
| [Generator Contract](../contracts/generator-contract.md) | Test generator requirements |
| [Test File Format](../contracts/test-file-format.md) | `.in`/`.out` file format |
| [Ontology Design](../reference/ontology-design.md) | Taxonomy structure |
| [Pattern Docs Tool](../tools/patterndocs/README.md) | Documentation generator |

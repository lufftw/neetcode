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
- [Phase 1: Pattern Documentation (templates.md)](#phase-1-pattern-documentation-templatesmd)
- [Phase 2: Solution Files](#phase-2-solution-files)
- [Phase 3: Test Infrastructure (Generators)](#phase-3-test-infrastructure-generators)
- [Phase 4: Intuition Guide](#phase-4-intuition-guide)
- [Phase 5: Problem Metadata](#phase-5-problem-metadata)
- [Phase 6: Ontology and Roadmaps](#phase-6-ontology-and-roadmaps)
- [Phase 7: Mindmap Integration](#phase-7-mindmap-integration)
- [Phase 8: Navigation and Version Control](#phase-8-navigation-and-version-control)
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
│  Phase 1: Templates        Phase 2: Solutions      Phase 3: Generators      │
│  ┌──────────────────┐     ┌──────────────────┐    ┌──────────────────┐     │
│  │ meta/patterns/   │────▶│ solutions/*.py   │───▶│ generators/*.py  │     │
│  │ docs/patterns/   │     │ - Reference      │    │ - JUDGE_FUNC     │     │
│  │   templates.md   │     │   templates.md   │    │ - Edge cases     │     │
│  └──────────────────┘     └──────────────────┘    └──────────────────┘     │
│          │                                                 │                │
│          ▼                                                 ▼                │
│  Phase 4: Intuition        Phase 5: Metadata       Phase 6: Ontology       │
│  ┌──────────────────┐     ┌──────────────────┐    ┌──────────────────┐     │
│  │ docs/patterns/   │     │ meta/problems/   │───▶│ ontology/*.toml  │     │
│  │   intuition.md   │     │ *.toml           │    │ roadmaps/*.toml  │     │
│  └──────────────────┘     └──────────────────┘    └──────────────────┘     │
│                                                            │                │
│                                                            ▼                │
│                           Phase 7: Mindmaps       Phase 8: Version Control │
│                          ┌──────────────────┐    ┌──────────────────┐     │
│                          │ ai-markmap-agent │───▶│ mkdocs.yml       │     │
│                          │ config.yaml      │    │ git + PR         │     │
│                          └──────────────────┘    └──────────────────┘     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Critical Workflow Order

**IMPORTANT**: The phases MUST be executed in this order:

1. **Templates FIRST** → Solutions reference the canonical templates
2. **Solutions SECOND** → Implement algorithms exactly as documented
3. **Generators THIRD** → Test solutions using JUDGE_FUNC
4. **Intuition FOURTH** → Written after understanding real implementation challenges

### Deliverables Summary

| Phase | Directory | Files Created |
|-------|-----------|---------------|
| 1 | `meta/patterns/`, `docs/patterns/` | Pattern snippets → `templates.md` (generated) |
| 2 | `solutions/` | `{id}_{slug}.py` for each problem (references templates) |
| 3 | `generators/` | Generator files with `generate()` function |
| 4 | `docs/patterns/` | `intuition.md` (manually written) |
| 5 | `meta/problems/` | `{id}_{slug}.toml` problem metadata |
| 6 | `ontology/`, `roadmaps/` | Taxonomy + learning path |
| 7 | `tools/mindmaps/` | Config updates for AI mindmap generation |
| 8 | `mkdocs.yml`, Git | Navigation update + feature branch + PR |

### Documentation-Only Workflow

For cases where you only need pattern documentation (no solutions, generators, or ontology updates), use this minimal workflow:

1. **Phase 1**: Create `meta/patterns/{pattern}/` source files and generate `templates.md`
2. **Phase 4**: Write `docs/patterns/{pattern}/intuition.md` manually
3. **Phase 8 (partial)**: Update indexes (`docs/patterns/README.md`, `README.md`, `README_zh-TW.md`, `mkdocs.yml`) and create PR

**Recommended commit structure for documentation-only patterns:**

```bash
# Commit 1: Scaffold pattern structure
git commit -m "docs({pattern}): scaffold {pattern} pattern"

# Commit 2: Add generated templates and intuition guide
git commit -m "docs({pattern}): add templates and intuition guide"

# Commit 3: Wire into indexes
git commit -m "docs: wire {pattern} pattern into indexes"
```

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

## Phase 1: Pattern Documentation (templates.md)

**Purpose**: Create the canonical template documentation BEFORE writing solutions. Solutions should reference and implement these templates exactly.

### 1.1 Why Templates First?

| Reason | Explanation |
|--------|-------------|
| **Consistency** | All solutions follow the same variable names and structure |
| **Documentation-Driven** | Forces clear thinking about the algorithm before coding |
| **Reviewability** | Solutions can be verified against documented templates |
| **Teaching Quality** | Templates serve as learning reference for readers |

### 1.2 Create Meta Pattern Directory

Create source files in `meta/patterns/{pattern_name}/`:

```
meta/patterns/{pattern_name}/
├── _config.toml              # File ordering and output configuration
├── _header.md                # Core concepts (REQUIRED: must include API Kernel)
├── _templates.md             # Code templates with variable naming standards
├── _comparison.md            # Comparison with similar patterns
├── _decision.md              # Decision flowchart for when to use
├── _mapping.md               # Maps sub-patterns to LeetCode problems
└── {problem_id}-{topic}.md   # Problem-specific implementation snippets
```

#### 1.2.1 _config.toml (Required)

Controls file ordering and output path:

```toml
# Pattern Documentation Configuration
header_files = ["_header.md"]

# Problem files ordered by learning progression
problem_files = [
    "0303-range-sum-base.md",
    "0560-subarray-sum-k.md",
    "0525-contiguous-array.md",
    "0304-2d-range-sum.md",
    "1094-difference-array.md"
]

footer_files = [
    "_comparison.md",
    "_decision.md",
    "_mapping.md",
    "_templates.md"
]

[output]
subdirectory = "prefix_sum"
filename = "templates.md"
```

#### 1.2.2 _header.md (Required)

**CRITICAL**: Must include `> **API Kernel**: \`KernelID\`` line.

```markdown
# Prefix Sum Patterns: Complete Reference

> **API Kernel**: `PrefixSumRangeQuery`
> **Core Mechanism**: Precompute cumulative sums for O(1) range sum queries.

## Core Concepts

### The Prefix Sum Principle

Given array `nums`, prefix sum `P[i]` = sum of `nums[0..i-1]`:
- `P[0] = 0` (empty prefix)
- `P[i] = P[i-1] + nums[i-1]`

Range sum `[i, j]` = `P[j+1] - P[i]` in O(1).
```

#### 1.2.3 Problem Snippet Files

Each problem snippet provides the canonical implementation:

```markdown
## Base Template: Range Sum Query (LeetCode 303)

> **Problem**: Handle multiple range sum queries efficiently.
> **Invariant**: `prefix[i]` = sum of all elements before index `i`.
> **Role**: BASE TEMPLATE for `PrefixSumRangeQuery` API Kernel.

### Implementation

\`\`\`python
class NumArray:
    def __init__(self, nums: List[int]):
        # Initialize with 0 for empty prefix
        self.prefix_sum: List[int] = [0]
        for num in nums:
            self.prefix_sum.append(self.prefix_sum[-1] + num)

    def sumRange(self, left: int, right: int) -> int:
        return self.prefix_sum[right + 1] - self.prefix_sum[left]
\`\`\`

### Trace Example

\`\`\`
Input: nums = [-2, 0, 3, -5, 2, -1]
Prefix:       [0, -2, -2, 1, -4, -2, -3]

Query: sumRange(0, 2) = prefix[3] - prefix[0] = 1
\`\`\`
```

### 1.3 Generate templates.md

First, create the output directory if it doesn't exist:

```bash
# Create output directory
mkdir -p docs/patterns/{pattern_name}
```

Then run the pattern documentation generator:

```bash
# Generate templates.md from meta/patterns sources
python tools/patterndocs/generate_pattern_docs.py --pattern {pattern_name}

# Example
python tools/patterndocs/generate_pattern_docs.py --pattern prefix_sum
```

This creates `docs/patterns/{pattern_name}/templates.md`.

> **Note**: The generator expects the output directory to exist. If you see a "directory not found" error, ensure you created the directory first.

> **Reference**: [Pattern Docs Generator](../tools/patterndocs/README.md)

---

## Phase 2: Solution Files

**Purpose**: Implement solutions that reference and follow `templates.md` exactly.

> **Reference**: [Solution Contract](../contracts/solution-contract.md) - Complete specification for solution file structure

### 2.1 Create Solution Skeleton

For each problem, create a solution file in `solutions/`:

```bash
# Option A: Use CodeGen (recommended for new problems)
python -m codegen new <leetcode_id> --with-tests

# Option B: Manual creation
# Create: solutions/{id:04d}_{slug}.py
```

### 2.2 Solution File Structure

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

### 1.6 Writing High-Quality Solutions (Dual Perspective)

Solutions should be written from two merged perspectives:

| Perspective | Focus | What It Provides |
|-------------|-------|------------------|
| **Algorithm Expert** | Correctness, complexity, mathematical reasoning | Why the algorithm works, invariants, edge cases |
| **Engineering Lead** | Maintainability, readability, production-quality | Clean naming, clear structure, documentation |

#### Quality Standards

**Variable Naming**:
- Use semantically clear names: `prefix_sum` not `ps`, `first_occurrence` not `fo`
- Match template names in `docs/patterns/*/templates.md` exactly
- Names should reveal intent: `char_frequency` not `freq`, `window_sum` not `ws`

**Comments**:
- Explain **WHY**, not what (the code shows what)
- Include invariants and loop reasoning
- Reference pattern documentation when applicable

**Code Structure**:
- Group related operations with blank lines
- Use type hints consistently
- Keep methods focused and single-purpose

#### Example: High-Quality Solution

```python
# ============================================================================
# Solution: Prefix Sum + Hash Map
# Time: O(n), Space: O(n)
#
# Core Insight (Algorithm Expert):
#   If prefix[j] - prefix[i] = k, then subarray (i, j] sums to k.
#   We count occurrences of (prefix_sum - k) seen so far.
#
# Why Hash Map (Algorithm Expert):
#   Instead of O(n²) brute force checking all pairs, we use a hash map to
#   answer "how many times have we seen this prefix sum?" in O(1).
#
# Why Initialize {0: 1} (Engineering Lead - Edge Case):
#   Handles subarrays starting from index 0. If prefix_sum == k at position i,
#   we need to count the "empty prefix" (sum 0 at position -1).
#
# Pattern Reference: prefix_sum_subarray_sum
# See: docs/patterns/prefix_sum/templates.md Section 2
# ============================================================================
class SolutionPrefixSum:
    def subarraySum(self, nums: List[int], k: int) -> int:
        subarray_count = 0
        prefix_sum = 0

        # Map: prefix_sum value -> count of occurrences
        # Initialize with {0: 1} for subarrays starting at index 0
        sum_frequency: dict[int, int] = {0: 1}

        for num in nums:
            # Extend prefix sum with current element
            prefix_sum += num

            # Key insight: If (prefix_sum - k) was seen before, those positions
            # mark valid subarray starts. Add their count to result.
            complement = prefix_sum - k
            subarray_count += sum_frequency.get(complement, 0)

            # Record current prefix sum for future elements
            sum_frequency[prefix_sum] = sum_frequency.get(prefix_sum, 0) + 1

        return subarray_count
```

#### Anti-Patterns to Avoid

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| `for i in range(len(nums))` + `nums[i]` | Verbose, index-focused | `for i, num in enumerate(nums)` or `for num in nums` |
| Single-letter variables | Unclear intent | Descriptive names: `n` → `array_length` |
| Magic numbers | Unexplained constants | Named constants or comments |
| Overly clever one-liners | Hard to debug/maintain | Clear multi-line with comments |
| Comments stating the obvious | Noise, not signal | Focus on WHY, not WHAT |

### 1.7 JUDGE_FUNC Requirements

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

### 1.8 solve() Function Requirements

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

## Phase 3: Test Infrastructure (Generators)

**Purpose**: Create test generators that produce valid test cases and use JUDGE_FUNC for validation.

> **Reference**: [Generator Contract](../contracts/generator-contract.md) - Complete specification for generator functions

### 3.1 Create Test Generator

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

### 3.2 Generate Test Files

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

### 3.3 Run Tests to Verify

```bash
# Test single problem
python runner/test_runner.py {problem_id}

# Test all problems in pattern (example for monotonic stack)
python runner/test_runner.py 0042 0084 0085 0316 0321 0402 0496 0503 0739 0901 0907 2104

# Run with generated tests
python runner/test_runner.py {problem_id} --generate 10 --seed 42
```

### 3.4 Test File Format

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

## Phase 4: Intuition Guide

**Purpose**: Create a narrative guide that builds intuition and helps readers recognize when to use this pattern.

> **Note**: Write `intuition.md` AFTER completing solutions and generators. Real implementation experience informs better explanations.

### 4.1 Create Intuition Guide

Create `docs/patterns/{pattern_name}/intuition.md` manually:

```markdown
# Prefix Sum: Intuition Guide

## The Mental Model

Imagine you're tracking a bank account balance over time...

## Pattern Recognition Signals

### Signal: "Sum of subarray"
When you see: "find subarray with sum = k", "count subarrays", "range sum"
Think: Prefix sum + hash map

### Signal: "Range updates"
When you see: "add value to range [i, j]", "increment interval"
Think: Difference array (inverse of prefix sum)

### Signal: "Multiple range queries"
When you see: "answer Q queries", "immutable array"
Think: Precompute prefix sum once

## Common Pitfalls

1. **Off-by-one errors**: Remember `prefix[i]` = sum of elements BEFORE index `i`
2. **Forgetting {0: 1}**: For subarray sum = k, initialize with empty prefix
3. **Integer overflow**: For large arrays, consider using `long` type

## Practice Progression

1. **LC 303** (Range Sum Query) - Build the intuition
2. **LC 560** (Subarray Sum = K) - Add hash map
3. **LC 525** (Contiguous Array) - Transform problem
4. **LC 1094** (Car Pooling) - Difference array
5. **LC 304** (2D Range Sum) - Extend to 2D
```

### 4.2 Update Pattern Indexes

Update all pattern index files to include the new pattern:

1. **`docs/patterns/README.md`** - Add to API Kernel table
2. **`README.md`** - Add to pattern documentation section
3. **`README_zh-TW.md`** - Add to pattern documentation section (Chinese labels)
4. **`mkdocs.yml`** - Add navigation entry under `📐 Patterns`

Example for `docs/patterns/README.md`:

```markdown
| `{PatternName}` | 💡 [Intuition]({pattern}/intuition.md) · 🛠️ [Templates]({pattern}/templates.md) | Description | LeetCode IDs |
```

Example for `mkdocs.yml` (add under Patterns section):

```yaml
- {Pattern Display Name}:
  - Intuition: patterns/{pattern}/intuition.md
  - Templates: patterns/{pattern}/templates.md
```

> **Important**: Both English and Chinese README files must be updated to maintain consistency.

---

## Phase 5: Problem Metadata

**Purpose**: Create metadata files that link problems to patterns, roadmaps, and learning paths.

> **Reference**: [Test File Format](../contracts/test-file-format.md) - Problem metadata structure

### 5.1 Create Problem Metadata Files

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

## Phase 6: Ontology and Roadmaps

**Purpose**: Register patterns and learning paths in the taxonomy system.

> **Reference**: [Ontology Design](../reference/ontology-design.md) - Taxonomy structure

### 6.1 Update ontology/patterns.toml

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

### 6.2 Update ontology/roadmaps.toml

Register the new roadmap:

```toml
# ontology/roadmaps.toml

[[roadmaps]]
id = "monotonic_stack_path"
name = "Monotonic Stack Mastery"
summary = "Step-by-step path to master monotonic stack patterns."
```

### 6.3 Create Roadmap File

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

---

## Phase 7: Mindmap Integration

**Purpose**: Configure AI mindmap generation for the new pattern.

### 7.1 Update AI Markmap Agent Config

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

### 7.2 Verify Configuration

The following configs auto-include new content (no changes needed):

| Config File | Behavior |
|-------------|----------|
| `tools/mindmaps/generate_mindmaps_ai.toml` | Empty `include = []` means all files |
| `tools/mindmaps/generate_mindmaps.toml` | SEO descriptions only |

---

## Phase 8: Navigation and Version Control

**Purpose**: Update navigation, create feature branch, and submit PR.

### 8.1 Update mkdocs.yml Navigation

Add the new pattern documentation to `mkdocs.yml`:

```yaml
nav:
  - Patterns:
    - patterns/index.md
    - Sliding Window:
      - patterns/sliding_window/templates.md
      - patterns/sliding_window/intuition.md
    # Add new pattern
    - Prefix Sum:
      - patterns/prefix_sum/templates.md
      - patterns/prefix_sum/intuition.md
```

### 8.2 Create Feature Branch

```bash
git checkout -b feat/{pattern-name}-pattern
```

### 8.3 Commit Changes

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

### 8.4 Push and Create PR

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

### Phase 1: Pattern Documentation (templates.md)

- [ ] Create `meta/patterns/{pattern}/_config.toml`
- [ ] Create `meta/patterns/{pattern}/_header.md` with API Kernel
- [ ] Create `meta/patterns/{pattern}/_templates.md`
- [ ] Create problem snippets `{id}-{topic}.md`
- [ ] Run `python tools/patterndocs/generate_pattern_docs.py --pattern {pattern}`
- [ ] Verify `docs/patterns/{pattern}/templates.md` generated correctly

### Phase 2: Solution Files

- [ ] Create `solutions/{id}_{slug}.py` for each problem
- [ ] Reference `templates.md` in solution comments
- [ ] Include `SOLUTIONS` dict with metadata
- [ ] Implement `JUDGE_FUNC` that handles both types
- [ ] Add `solve()` entry point

### Phase 3: Test Infrastructure (Generators)

- [ ] Create `generators/{id}_{slug}.py` for each problem
- [ ] Include edge cases as first test cases
- [ ] Generate 5-7 test cases per problem
- [ ] Verify all tests pass with `python runner/test_runner.py`
- [ ] Fix any CRLF line ending issues

### Phase 4: Intuition Guide

- [ ] Write `docs/patterns/{pattern}/intuition.md`
- [ ] Include pattern recognition signals
- [ ] Include common pitfalls
- [ ] Include practice progression
- [ ] Update `docs/patterns/README.md`

### Phase 5: Problem Metadata

- [ ] Create `meta/problems/{id}_{slug}.toml` for each problem
- [ ] Include ontology tags (api_kernels, patterns, families)
- [ ] Link to roadmaps

### Phase 6: Ontology and Roadmaps

- [ ] Add patterns to `ontology/patterns.toml`
- [ ] Add roadmap to `ontology/roadmaps.toml`
- [ ] Create `roadmaps/{pattern}_path.toml`

### Phase 7: Mindmap Integration

- [ ] Update `tools/mindmaps/ai-markmap-agent/config/config.yaml`

### Phase 8: Navigation and Version Control

- [ ] Update `mkdocs.yml` navigation
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

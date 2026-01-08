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
- [Quick Start: Existing Problems](#quick-start-existing-problems)
- [Phase 1: Meta Pattern Sources](#phase-1-meta-pattern-sources)
- [Phase 2: Templates and Intuition](#phase-2-templates-and-intuition)
- [Phase 3: Solutions](#phase-3-solutions)
- [Phase 4: Generators (Optional)](#phase-4-generators-optional)
- [Phase 5: Test Files](#phase-5-test-files)
- [Phase 6: Problem Metadata](#phase-6-problem-metadata)
- [Phase 7: Ontology and Roadmap](#phase-7-ontology-and-roadmap)
- [Phase 8: Navigation and Integration](#phase-8-navigation-and-integration)
- [Common Pitfalls](#common-pitfalls)
- [Writing Effective Intuition Guides](#writing-effective-intuition-guides)
- [Quick Reference Checklist](#quick-reference-checklist)
- [Example Patterns](#example-patterns)

---

## Overview

A complete pattern implementation consists of 8 phases:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Pattern Development Pipeline                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Phase 1: Meta Sources    Phase 2: Docs           Phase 3: Solutions        │
│  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐      │
│  │ meta/patterns/   │───▶│ docs/patterns/   │───▶│ solutions/*.py   │      │
│  │ _config.toml     │    │ templates.md     │    │ JUDGE_FUNC       │      │
│  │ _header.md       │    │ intuition.md     │    │ solve()          │      │
│  │ problem files    │    └──────────────────┘    └──────────────────┘      │
│  └──────────────────┘             │                       │                 │
│          │                        │                       │                 │
│          ▼                        │                       ▼                 │
│  Phase 4: Generators     Phase 5: Tests          Phase 6: Metadata         │
│  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐      │
│  │ generators/*.py  │───▶│ tests/*.in       │    │ meta/problems/   │      │
│  │ generate()       │    │ tests/*.out      │    │ *.toml           │      │
│  └──────────────────┘    └──────────────────┘    └──────────────────┘      │
│                                   │                       │                 │
│                                   ▼                       ▼                 │
│                          Phase 7: Ontology       Phase 8: Navigation        │
│                          ┌──────────────────┐    ┌──────────────────┐      │
│                          │ ontology/*.toml  │───▶│ mkdocs.yml       │      │
│                          │ roadmaps/*.toml  │    │ README.md        │      │
│                          └──────────────────┘    │ config.yaml      │      │
│                                                  └──────────────────┘      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Deliverables Summary

| Phase | Directory | Files Created |
|-------|-----------|---------------|
| 1 | `meta/patterns/{pattern}/` | `_config.toml`, `_header.md`, problem files, footer files |
| 2 | `docs/patterns/{pattern}/` | `templates.md` (generated), `intuition.md` (manual) |
| 3 | `solutions/` | `{id}_{slug}.py` with JUDGE_FUNC |
| 4 | `generators/` | `{id}_{slug}.py` with `generate()` |
| 5 | `tests/` | `{id}_{slug}_{n}.in/.out` files |
| 6 | `meta/problems/` | `{id}_{slug}.toml` metadata |
| 7 | `ontology/`, `roadmaps/` | API kernel, patterns, roadmap |
| 8 | Various | Navigation updates + merge to main |

### Branch Naming Convention

```bash
feat/pattern-{pattern_name}
# Examples:
# feat/pattern-bitmask-dp
# feat/pattern-tree-dp
# feat/pattern-line-sweep
```

### Recommended Commit Structure

```bash
# Each phase gets its own commit for clean history
git commit -m "meta({pattern}): Phase 1 - Add pattern source files"
git commit -m "docs({pattern}): Phase 2 - Add templates and intuition guide"
git commit -m "solutions({pattern}): Phase 3 - Add/update solutions"
git commit -m "generators({pattern}): Phase 4 - Add test generators"
git commit -m "tests({pattern}): Phase 5 - Add test files"
git commit -m "meta({pattern}): Phase 6 - Add problem metadata"
git commit -m "ontology({pattern}): Phase 7 - Add to ontology and create roadmap"
git commit -m "docs({pattern}): Phase 8 - Add navigation to mkdocs.yml"
```

---

## Prerequisites

Before starting, ensure you have:

1. **Problem Selection**: Identify 3-6 LeetCode problems that represent the pattern
2. **Pattern Analysis**: Understand the core algorithm and its variations
3. **Learning Order**: Determine the pedagogical progression (base → variants)

### Recommended Problem Selection

| Role | Count | Description |
|------|-------|-------------|
| Base Template | 1 | Canonical problem that teaches the core pattern |
| Variants | 2-4 | Same pattern with different applications |
| Advanced | 0-2 | Complex problems combining with other patterns |

### Example Problem Selections

| Pattern | Problems | Rationale |
|---------|----------|-----------|
| Bitmask DP | LC 78, 847, 1125 | Enumeration → BFS + bitmask → Set cover |
| Tree DP | LC 337, 124, 968 | Include/exclude → Path contribution → Multi-state |
| Line Sweep | LC 253, 1094, 218 | Event counting → Capacity → Height tracking |
| Multi-Source BFS | LC 994, 286, 542 | Propagation timing → Distance fill → Distance field |
| K-Way Merge | LC 23, 21, 88 | Heap-based → Two-pointer → Backward in-place |
| Linked List Reversal | LC 206, 92, 25 | Full → Segment → K-group |

---

## Quick Start: Existing Problems

When creating a pattern from **problems that already have solutions and tests**, you can skip several phases:

### Minimal Workflow (3-4 hours)

```
Phase 1: Meta Sources      ✅ Required - Create pattern documentation
Phase 2: Docs              ✅ Required - Generate templates, write intuition
Phase 3: Solutions         ⚡ Minimal  - Just add api_kernels/patterns to SOLUTIONS
Phase 4: Generators        ⏭️ Skip     - Tests already exist
Phase 5: Test Files        ⏭️ Skip     - Tests already exist
Phase 6: Problem Metadata  ⚡ Minimal  - Update roadmaps field, or create if missing
Phase 7: Ontology/Roadmap  ✅ Required - Create roadmap file
Phase 8: Navigation        ✅ Required - Update mkdocs.yml and docs/patterns/README.md
```

### Example: KWayMerge Pattern

LC 23, 21, 88 already had solutions and tests. The workflow was:

1. **Phase 1-2**: Create meta sources and docs (most time spent here)
2. **Phase 3**: Add metadata to existing SOLUTIONS dicts:
   ```python
   SOLUTIONS = {
       "default": {
           "class": "SolutionHeap",
           "method": "mergeKLists",
           "api_kernels": ["KWayMerge"],      # Added
           "patterns": ["merge_k_sorted_heap"], # Added
       },
   }
   ```
3. **Phase 6**: Add `roadmaps = ["k_way_merge_path"]` to existing problem metadata
4. **Phase 7-8**: Create roadmap and update navigation

**Total commits**: 4 (vs 8 for new problems)

---

## Phase 1: Meta Pattern Sources

**Purpose**: Create source files that will be assembled into `templates.md`.

### 1.1 Create Branch and Directory

```bash
git checkout -b feat/pattern-{pattern_name}
mkdir -p meta/patterns/{pattern_name}
```

### 1.2 Create _config.toml

Controls file ordering and output:

```toml
# meta/patterns/{pattern_name}/_config.toml

header_files = ["_header.md"]

problem_files = [
    "0078-subsets.md",
    "0847-shortest-path-visiting-all-nodes.md",
    "1125-smallest-sufficient-team.md"
]

footer_files = ["_comparison.md", "_decision.md", "_templates.md"]

[output]
subdirectory = "{pattern_name}"
filename = "templates.md"
```

### 1.3 Create _header.md

**CRITICAL**: Must include `> **API Kernel**: \`KernelID\``.

```markdown
# {Pattern Name} Pattern

## API Kernel: `{KernelID}`

> **Core Mechanism**: {One-line description of what this pattern does}.

## Why {Pattern Name}?

{Pattern Name} solves problems where:
- {Condition 1}
- {Condition 2}
- {Condition 3}

## Core Insight

{Key algorithmic insight that makes this pattern work}

## Universal Template Structure

\`\`\`python
def pattern_template(params):
    # State initialization
    # Main loop
    # Return result
\`\`\`

## Pattern Variants

| Pattern | State | Transition | Example |
|---------|-------|------------|---------|
| **Variant 1** | ... | ... | Problem name |
| **Variant 2** | ... | ... | Problem name |
```

### 1.4 Create Problem Snippet Files

Each problem gets a markdown file:

```markdown
# {ID}. {Problem Title}

## Problem Link
https://leetcode.com/problems/{slug}/

## Difficulty
{Easy|Medium|Hard}

## Tags
- {Tag1}
- {Tag2}

## Pattern
{Pattern Name} - {Sub-pattern}

## API Kernel
`{KernelID}`

## Problem Summary
{One paragraph problem description}

## Key Insight

{What makes this problem solvable with this pattern}

## Template Mapping

\`\`\`python
def solution(params):
    # Implementation following the template
    pass
\`\`\`

## Complexity
- Time: O(?)
- Space: O(?)

## Why This Problem {First|Second|Third}?

{Pedagogical reasoning for problem ordering}

## Common Mistakes

1. **Mistake 1** - {Description}
2. **Mistake 2** - {Description}

## Related Problems
- LC {id}: {title}
```

### 1.5 Create Footer Files

**_comparison.md** - Side-by-side comparison:

```markdown
## Problem Comparison

| Problem | Core Pattern | State | Transition | Output |
|---------|-------------|-------|------------|--------|
| **{Problem 1}** | ... | ... | ... | ... |
| **{Problem 2}** | ... | ... | ... | ... |

## Pattern Evolution

\`\`\`
Problem 1
    ↓
{What changes}
    ↓
Problem 2
    ↓
{What changes}
    ↓
Problem 3
\`\`\`
```

**_decision.md** - Decision flowchart:

```markdown
## Decision Tree

\`\`\`
Start: {Initial question}?
            │
            ▼
    ┌───────────────────┐
    │ {Decision point}  │
    └───────────────────┘
            │
    ┌───────┴───────┐
    ▼               ▼
{Option 1}     {Option 2}
\`\`\`

## Pattern Selection Guide

### Use {Pattern 1} when:
- ✅ {Condition}
- ✅ {Condition}

### Use {Pattern 2} when:
- ✅ {Condition}
- ✅ {Condition}
```

**_templates.md** - Copy-paste ready templates:

```markdown
## Universal Templates

### Template 1: {Name}

\`\`\`python
def template_1(params):
    """Description"""
    # Implementation
    pass
\`\`\`

**Use for**: LC {ids}

---

### Template 2: {Name}

\`\`\`python
def template_2(params):
    """Description"""
    # Implementation
    pass
\`\`\`

**Use for**: LC {ids}
```

### 1.6 Commit Phase 1

```bash
git add meta/patterns/{pattern_name}/
git commit -m "meta({pattern_name}): Phase 1 - Add pattern source files

Add {Pattern Name} pattern with {N} problems:
- {Problem 1}
- {Problem 2}
- {Problem 3}

Includes header, comparison, decision tree, and templates."
```

---

## Phase 2: Templates and Intuition

**Purpose**: Generate `templates.md` and create `intuition.md`.

### 2.1 Create Output Directory

```bash
mkdir -p docs/patterns/{pattern_name}
```

### 2.2 Generate templates.md

```bash
mkdir -p docs/patterns/{pattern_name}
python tools/patterndocs/generate_pattern_docs.py --pattern {pattern_name}
```

**Important**: The generator outputs to `docs/patterns/{pattern_name}.md` (a file), not inside a subdirectory. You need to move it:

```bash
mv docs/patterns/{pattern_name}.md docs/patterns/{pattern_name}/templates.md
```

### 2.3 Create intuition.md

Write `docs/patterns/{pattern_name}/intuition.md` manually:

```markdown
# {Pattern Name} - Intuition Guide

## The Mental Model: {Analogy}

{Relatable analogy that explains the pattern}

## Why {Pattern Name}?

{Explanation of why this approach works}

## Core Insight

{Key algorithmic insight}

## Pattern 1: {Sub-pattern Name}

**The insight**: {What makes this work}

\`\`\`
{Visual diagram or trace}
\`\`\`

The code:
\`\`\`python
# Key implementation detail
\`\`\`

## Pattern 2: {Sub-pattern Name}

{Similar structure}

## Common Mistakes

### Mistake 1: {Title}

\`\`\`python
❌ # Wrong way
✅ # Right way
\`\`\`

## Quick Pattern Recognition

| Clue | Pattern |
|------|---------|
| "{keyword}" | {Sub-pattern} |
| "{keyword}" | {Sub-pattern} |

## Visual Summary

\`\`\`
{ASCII diagram summarizing the pattern}
\`\`\`
```

### 2.4 Commit Phase 2

```bash
git add docs/patterns/{pattern_name}/
git commit -m "docs({pattern_name}): Phase 2 - Add templates and intuition guide

Generate templates.md from pattern sources.
Add intuition.md with mental models:
- {Model 1}
- {Model 2}
- {Model 3}"
```

---

## Phase 3: Solutions

**Purpose**: Create solution files that implement the patterns.

### 3.1 Check for Existing Solutions

```bash
ls solutions/{id1}_*.py solutions/{id2}_*.py solutions/{id3}_*.py 2>/dev/null
```

### 3.2 Create New Solutions

For each problem without a solution:

```python
# solutions/{id}_{slug}.py
"""
Problem: {Title}
Link: https://leetcode.com/problems/{slug}/

{Problem description}

Example 1:
    Input: ...
    Output: ...

Constraints:
- ...

Topics: {Topic1}, {Topic2}
"""
from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "{methodName}",
        "complexity": "O(?) time, O(?) space",
        "description": "{Brief description}",
    },
}


# ============================================================================
# JUDGE_FUNC - Required for problems with multiple valid answers
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate result."""
    import json
    lines = input_data.strip().split('\n')
    # Parse input
    param1 = json.loads(lines[0])

    # Compute correct answer or validate actual
    # ...

    return actual == expected  # or custom validation


JUDGE_FUNC = judge


# ============================================================================
# Solution: {Approach Name}
# Time: O(?), Space: O(?)
#   - {Key insight 1}
#   - {Key insight 2}
# ============================================================================
class Solution:
    def methodName(self, params) -> ReturnType:
        """Implementation."""
        pass


def solve():
    """
    Input format:
    Line 1: {description}
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    param1 = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.methodName(param1)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()
```

### 3.3 Update Existing Solutions

If a solution exists, add the pattern-specific approach:

```python
# Add to SOLUTIONS dict
SOLUTIONS = {
    "default": {...},
    "{new_approach}": {
        "class": "Solution{Approach}",
        "method": "{methodName}",
        "complexity": "O(?) time, O(?) space",
        "description": "{Brief description}",
    },
}

# Add new solution class
class Solution{Approach}:
    def methodName(self, params):
        pass
```

### 3.4 Verify Solutions Work

Always run tests after creating/updating solutions:

```bash
python runner/test_runner.py {id1}_{slug1} --all
python runner/test_runner.py {id2}_{slug2} --all
python runner/test_runner.py {id3}_{slug3} --all
```

### 3.5 Commit Phase 3

```bash
git add solutions/{id1}_*.py solutions/{id2}_*.py solutions/{id3}_*.py
git commit -m "solutions({pattern_name}): Phase 3 - Add/update solutions

{Add|Update} solutions for:
- {Problem 1}
- {Problem 2}
- {Problem 3}"
```

---

## Phase 4: Generators (Optional)

**Purpose**: Create test generators for each problem.

**Skip this phase if**:
- The problems already have test files in `tests/`
- You're updating an existing pattern with new documentation only

Generators are primarily useful for:
- New problems without existing tests
- Stress testing with random inputs
- Complexity estimation (`--estimate` flag)

### 4.1 Create Generator Files

```python
# generators/{id}_{slug}.py
"""
Random test generator for LC {id}: {Title}

Constraints:
- {constraint 1}
- {constraint 2}
"""
import random
import json
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test cases.

    Yields test input strings in the format expected by the solution.
    """
    if seed is not None:
        random.seed(seed)

    for _ in range(count):
        # Generate valid input according to constraints
        param1 = _generate_param1()

        yield json.dumps(param1, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific size n for complexity estimation.
    """
    # Generate input of size n
    param1 = _generate_size_n(n)

    return json.dumps(param1, separators=(',', ':'))


def _generate_param1():
    """Helper to generate valid param1."""
    pass


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(5, seed=42), 1):
        print(f"Test {i}: {test}")
```

### 4.2 Commit Phase 4

```bash
git add generators/{id1}_*.py generators/{id2}_*.py generators/{id3}_*.py
git commit -m "generators({pattern_name}): Phase 4 - Add test generators

Add generators for:
- {Problem 1}
- {Problem 2}
- {Problem 3}"
```

---

## Phase 5: Test Files

**Purpose**: Generate input and output test files.

### 5.1 Create Input Files

For each problem, create 5 test cases:

```bash
# tests/{id}_{slug}_{n}.in
# Each line is a JSON value
[1,2,3]
4
```

### 5.2 Generate Output Files

Run solutions to create outputs:

```bash
for prob in {id1}_{slug1} {id2}_{slug2} {id3}_{slug3}; do
  for i in 1 2 3 4 5; do
    PYTHONPATH=. python "solutions/${prob}.py" < "tests/${prob}_${i}.in" > "tests/${prob}_${i}.out"
    echo "Created tests/${prob}_${i}.out"
  done
done
```

### 5.3 Verify Tests Pass

```bash
PYTHONPATH=. python runner/test_runner.py {id1}_{slug1}
PYTHONPATH=. python runner/test_runner.py {id2}_{slug2}
PYTHONPATH=. python runner/test_runner.py {id3}_{slug3}
```

### 5.4 Test File Format

| Rule | Correct | Incorrect |
|------|---------|-----------|
| No spaces after comma | `[1,2,3]` | `[1, 2, 3]` |
| LF line endings | `\n` | `\r\n` |
| Single newline at end | `...\n` | `...\n\n` |

### 5.5 Commit Phase 5

```bash
git add tests/{id1}_*.in tests/{id1}_*.out tests/{id2}_*.in tests/{id2}_*.out tests/{id3}_*.in tests/{id3}_*.out
git commit -m "tests({pattern_name}): Phase 5 - Add test files

Add 5 test cases each for:
- {Problem 1}
- {Problem 2}
- {Problem 3}

All tests pass with exact/judge validation."
```

---

## Phase 6: Problem Metadata

**Purpose**: Create metadata files linking problems to patterns.

### 6.1 Create Problem Metadata

```toml
# meta/problems/{id}_{slug}.toml

# ===== Problem Info =====
id = "{id}"
slug = "{id}_{slug}"
title = "{Title}"
leetcode_id = {leetcode_id}
url = "https://leetcode.com/problems/{slug}/"

# ===== LeetCode Official Metadata =====
difficulty = "{easy|medium|hard}"
topics = ["{topic1}", "{topic2}"]
companies = ["{company1}", "{company2}"]

# ===== Roadmaps =====
roadmaps = ["{pattern_name}_path"]

# ===== Ontology Tags (Problem Level) =====
api_kernels      = ["{KernelID}"]
patterns         = ["{pattern_name}_{sub_pattern}"]
families         = ["{pattern_name}"]
data_structures  = ["{ds1}", "{ds2}"]
algorithms       = ["{algo1}", "{algo2}"]
related_problems = ["{related_id1}", "{related_id2}"]

# ===== Pattern Role =====
[pattern_role]
is_base_template = {true|false}
base_for_kernel = "{KernelID}"  # Only if is_base_template = true
derived_problems = ["{id1}", "{id2}"]

# ===== File Locations =====
[files]
solution  = "solutions/{id}_{slug}.py"
generator = "generators/{id}_{slug}.py"
tests_dir = "tests/{id}_{slug}/"

# ===== Solutions =====
[[solutions]]
key    = "default"
class  = "Solution"
method = "{methodName}"

api_kernels      = ["{KernelID}"]
patterns         = ["{pattern_name}_{sub_pattern}"]
families         = ["{pattern_name}"]
data_structures  = ["{ds1}", "{ds2}"]
algorithms       = ["{algo1}", "{algo2}"]
related_problems = ["{related_id1}", "{related_id2}"]

role       = "{base|variant}"
variant    = ""
based_on   = []
delta      = ""
complexity = "O(?) time, O(?) space"
notes      = "{Description of the approach}"
```

### 6.2 Commit Phase 6

```bash
git add meta/problems/{id1}_*.toml meta/problems/{id2}_*.toml meta/problems/{id3}_*.toml
git commit -m "meta({pattern_name}): Phase 6 - Add problem metadata

Add metadata for:
- {Problem 1}
- {Problem 2}
- {Problem 3}"
```

---

## Phase 7: Ontology and Roadmap

**Purpose**: Register pattern in taxonomy and create learning path.

### 7.1 Add API Kernel (if new)

Edit `ontology/api_kernels.toml`:

```toml
[[api_kernels]]
id = "{KernelID}"
summary = "{One-line description of the kernel}"
```

### 7.2 Add Patterns

Edit `ontology/patterns.toml`:

```toml
# ===== {Pattern Name} Patterns =====

[[patterns]]
id = "{pattern_name}_{sub_pattern1}"
api_kernel = "{KernelID}"
summary = "{Description of sub-pattern 1}"

[[patterns]]
id = "{pattern_name}_{sub_pattern2}"
api_kernel = "{KernelID}"
summary = "{Description of sub-pattern 2}"
```

### 7.3 Add Roadmap Entry

Edit `ontology/roadmaps.toml`:

```toml
[[roadmaps]]
id = "{pattern_name}_path"
name = "{Pattern Name} Mastery"
summary = "Step-by-step path to master {pattern name}: {sub-pattern1}, {sub-pattern2}."
```

### 7.4 Create Roadmap File

Create `roadmaps/{pattern_name}_path.toml`:

```toml
# {Pattern Name} Learning Path

[roadmap]
id = "{pattern_name}_path"
name = "{Pattern Name} Mastery"
description = """
Master {pattern name} for {problem type}.
Progress from {basic} to {advanced}.
"""
api_kernel = "{KernelID}"
difficulty_range = ["{min}", "{max}"]
estimated_problems = {N}

prerequisites = [
    "{Prerequisite 1}",
    "{Prerequisite 2}",
]

objectives = [
    "{Learning objective 1}",
    "{Learning objective 2}",
]

# =============================================================================
# Stage 1: {Stage Name}
# =============================================================================
[[stages]]
id = "{sub_pattern1}"
name = "{Sub-pattern 1 Name}"
description = "{What this stage teaches}"
pattern = "{pattern_name}_{sub_pattern1}"

focus_points = [
    "{Focus point 1}",
    "{Focus point 2}",
]

[[stages.problems]]
id = "{id1}"
title = "{Title}"
difficulty = "{difficulty}"
role = "base_template"
notes = "{Why this problem is first}"

# =============================================================================
# Stage 2: {Stage Name}
# =============================================================================
[[stages]]
id = "{sub_pattern2}"
name = "{Sub-pattern 2 Name}"
description = "{What this stage teaches}"
pattern = "{pattern_name}_{sub_pattern2}"

[[stages.problems]]
id = "{id2}"
title = "{Title}"
difficulty = "{difficulty}"
role = "variant"
notes = "{What this problem adds}"

# =============================================================================
# Summary
# =============================================================================
[summary]
key_insight = """
{Main takeaway from this pattern}
"""

complexity_guide = """
- {Sub-pattern 1}: O(?) time, O(?) space
- {Sub-pattern 2}: O(?) time, O(?) space
"""
```

### 7.5 Commit Phase 7

```bash
git add ontology/api_kernels.toml ontology/patterns.toml ontology/roadmaps.toml roadmaps/{pattern_name}_path.toml
git commit -m "ontology({pattern_name}): Phase 7 - Add to ontology and create roadmap

Add {KernelID} API kernel with patterns:
- {sub_pattern1}
- {sub_pattern2}

Add {pattern_name}_path roadmap with {N}-stage progression."
```

---

## Phase 8: Navigation and Integration

**Purpose**: Update all navigation files and merge to main.

### 8.1 Update mkdocs.yml

Add under `📐 Patterns`:

```yaml
    - {Pattern Display Name}:
      - Intuition: patterns/{pattern_name}/intuition.md
      - Templates: patterns/{pattern_name}/templates.md
```

### 8.2 Update Mindmap Config

Edit `tools/mindmaps/ai-markmap-agent/config/config.yaml`:

```yaml
# Under data_sources.patterns.directories:
      - name: "{pattern_name}"
        path: "{pattern_name}"
        enabled: true
        config_file: "_config.toml"

# Under data_sources.roadmaps.files:
      - name: "{pattern_name}_path"
        path: "{pattern_name}_path.toml"
        enabled: true
```

### 8.3 Update README.md

Add to Pattern Documentation table:

```markdown
| `{KernelID}` | 💡 [Intuition](docs/patterns/{pattern_name}/intuition.md) · 🛠️ [Templates](docs/patterns/{pattern_name}/templates.md) | LeetCode {ids} |
```

### 8.4 Update README_zh-TW.md

Add to Pattern Documentation table (Chinese labels):

```markdown
| `{KernelID}` | 💡 [直覺理解](docs/patterns/{pattern_name}/intuition.md) · 🛠️ [模板](docs/patterns/{pattern_name}/templates.md) | LeetCode {ids} |
```

### 8.5 Update docs/patterns/README.md

Add to Available Pattern Guides table:

```markdown
| `{KernelID}` | 💡 [Intuition]({pattern_name}/intuition.md) · 🛠️ [Templates]({pattern_name}/templates.md) | {Description} | LeetCode {ids} |
```

### 8.6 Commit Phase 8

```bash
git add mkdocs.yml tools/mindmaps/ai-markmap-agent/config/config.yaml README.md README_zh-TW.md docs/patterns/README.md
git commit -m "docs({pattern_name}): Phase 8 - Add navigation to mkdocs.yml

Add {Pattern Name} to:
- mkdocs.yml navigation
- mindmap config (patterns + roadmap)
- README.md pattern table
- README_zh-TW.md pattern table
- docs/patterns/README.md index"
```

### 8.7 Merge to Main

```bash
# Switch to main and merge
git checkout main
git pull origin main
git merge feat/pattern-{pattern_name} --no-edit

# Push to remote
git push origin main

# Delete feature branch
git branch -d feat/pattern-{pattern_name}
```

---

## Common Pitfalls

Based on experience developing patterns, avoid these common mistakes:

### 1. Generator Output Location

The pattern docs generator outputs to `docs/patterns/{pattern}.md`, not inside the subdirectory:

```bash
# Wrong assumption:
docs/patterns/my_pattern/templates.md  # NOT created automatically

# Actual output:
docs/patterns/my_pattern.md            # Created here

# Fix: Move it manually
mv docs/patterns/my_pattern.md docs/patterns/my_pattern/templates.md
```

### 2. Forgetting to Read Files Before Editing

When updating existing TOML files, always read them first to avoid "File not read" errors:

```python
# Wrong: Trying to edit without reading
Edit(file_path="meta/problems/0021.toml", old_string=..., new_string=...)

# Right: Read first, then edit
Read(file_path="meta/problems/0021.toml")
Edit(file_path="meta/problems/0021.toml", old_string=..., new_string=...)
```

### 3. Missing api_kernels/patterns in SOLUTIONS

When adding patterns to existing solutions, update ALL solution entries in SOLUTIONS dict:

```python
# Incomplete - only updated "default"
SOLUTIONS = {
    "default": {
        "api_kernels": ["MyKernel"],  # ✅ Added
        "patterns": ["my_pattern"],    # ✅ Added
    },
    "variant": {
        # ❌ Missing api_kernels and patterns!
    },
}
```

### 4. README Updates May Be Optional

If the main README uses a "View All Patterns" link to `docs/patterns/README.md`, you only need to update `docs/patterns/README.md`. The main README table shows representative examples, not exhaustive listings.

### 5. Mindmap Config Update Is Optional

Updating `tools/mindmaps/ai-markmap-agent/config/config.yaml` is only needed if you want the pattern to appear in auto-generated mindmaps. It can be deferred.

---

## Writing Effective Intuition Guides

The `intuition.md` file is the most valuable documentation you'll write. Here's how to make it effective:

### Use Relatable Analogies

Each pattern benefits from a memorable mental model:

| Pattern | Effective Analogy |
|---------|-------------------|
| Multi-Source BFS | "Flashlights in a cave" - multiple light sources spreading simultaneously |
| K-Way Merge | "Racing snails" - each sequence is a snail, heap picks the leader |
| Linked List Reversal | "Train car couplers" - flip the direction of each coupler |
| Sliding Window | "Moving spotlight" - illuminate a section, slide to reveal more |
| Monotonic Stack | "Building heights" - what can you see looking left/right? |

### Include Visual Traces

ASCII art helps readers follow the algorithm step-by-step:

```
Step 0:  prev=None, curr=1
         None <- 1    2 -> 3 -> 4 -> None

Step 1:  prev=1, curr=2
         None <- 1 <- 2    3 -> 4 -> None
```

### Highlight Common Mistakes

Show both wrong and right approaches:

```python
# ❌ WRONG - loses reference to next node
curr.next = prev
curr = curr.next  # Oops, curr.next is now prev!

# ✅ RIGHT - save next before modifying
next_node = curr.next
curr.next = prev
curr = next_node
```

### Add Pattern Recognition Signals

Help readers identify when to use the pattern:

```markdown
**Use this pattern when you see:**
- "Reverse" + "linked list" in problem statement
- "In-place" or "O(1) space" constraints
- "Swap adjacent pairs" or "reverse in groups"
```

### Structure Recommendations

1. **Mental Model** (1-2 paragraphs with analogy)
2. **Visual Walkthrough** (ASCII trace of key algorithm)
3. **Pattern Variants** (when to use each variant)
4. **Common Pitfalls** (mistakes to avoid)
5. **Pattern Recognition** (keywords and signals)
6. **Complexity Summary** (quick reference table)

---

## Quick Reference Checklist

### Phase 1: Meta Pattern Sources
- [ ] Create branch: `git checkout -b feat/pattern-{pattern_name}`
- [ ] Create directory: `mkdir -p meta/patterns/{pattern_name}`
- [ ] Create `_config.toml` with file ordering
- [ ] Create `_header.md` with `> **API Kernel**: \`...\``
- [ ] Create problem markdown files
- [ ] Create `_comparison.md`, `_decision.md`, `_templates.md`
- [ ] Commit Phase 1

### Phase 2: Templates and Intuition
- [ ] Create directory: `mkdir -p docs/patterns/{pattern_name}`
- [ ] Generate: `python tools/patterndocs/generate_pattern_docs.py --pattern {pattern_name}`
- [ ] Write `intuition.md` with mental models
- [ ] Commit Phase 2

### Phase 3: Solutions
- [ ] Check for existing solutions
- [ ] Create new solution files with JUDGE_FUNC
- [ ] Add pattern variants to existing solutions
- [ ] Commit Phase 3

### Phase 4: Generators (Skip if tests exist)
- [ ] Check if tests already exist: `ls tests/{id}_{slug}_*.in`
- [ ] Create generator files with `generate()` function
- [ ] Include edge cases
- [ ] Add `generate_for_complexity()` (optional)
- [ ] Commit Phase 4

### Phase 5: Test Files (Skip if tests exist)
- [ ] Check if tests already exist
- [ ] Create 5 input files per problem
- [ ] Generate output files by running solutions
- [ ] Verify all tests pass: `python runner/test_runner.py {problem} --all`
- [ ] Commit Phase 5

### Phase 6: Problem Metadata
- [ ] Create `meta/problems/{id}_{slug}.toml` for each problem
- [ ] Include ontology tags
- [ ] Link to roadmaps
- [ ] Commit Phase 6

### Phase 7: Ontology and Roadmap
- [ ] Add API kernel to `ontology/api_kernels.toml` (if new)
- [ ] Add patterns to `ontology/patterns.toml`
- [ ] Add roadmap entry to `ontology/roadmaps.toml`
- [ ] Create `roadmaps/{pattern_name}_path.toml`
- [ ] Commit Phase 7

### Phase 8: Navigation and Integration
- [ ] Update `mkdocs.yml` (required)
- [ ] Update `docs/patterns/README.md` (required)
- [ ] Update `tools/mindmaps/ai-markmap-agent/config/config.yaml` (optional)
- [ ] Update `README.md` (optional - only if adding to main table)
- [ ] Update `README_zh-TW.md` (optional - only if adding to main table)
- [ ] Commit Phase 8
- [ ] Merge to main: `git checkout main && git merge feat/pattern-{pattern_name}`
- [ ] Push to remote: `git push origin main`
- [ ] Delete feature branch: `git branch -d feat/pattern-{pattern_name}`

---

## Example Patterns

These patterns serve as implementation references:

| Pattern | Problems | Commits | Key Techniques |
|---------|----------|---------|----------------|
| **Bitmask DP** | LC 78, 847, 1125 | 8 | Subset enumeration, BFS + bitmask, set cover |
| **Tree DP** | LC 337, 124, 968 | 8 | Include/exclude, path contribution, multi-state |
| **Line Sweep** | LC 253, 1094, 218 | 8 | Event counting, capacity, height tracking |
| **Segment Tree/Fenwick** | LC 307, 315, 327 | 8 | Range queries with updates, inversion counting |
| **Multi-Source BFS** | LC 994, 286, 542 | 8 | Propagation timing, distance fill, distance field |
| **K-Way Merge** | LC 23, 21, 88 | 4 | Heap-based, two-pointer, backward merge |
| **Linked List Reversal** | LC 206, 92, 25 | 6 | Full reversal, segment, k-group |

**Note**: Patterns using existing solutions/tests (K-Way Merge) require fewer commits since Phases 4-5 are skipped.

### Directory Structure Example (Bitmask DP)

```
meta/patterns/bitmask_dp/
├── _config.toml
├── _header.md
├── 0078-subsets.md
├── 0847-shortest-path-visiting-all-nodes.md
├── 1125-smallest-sufficient-team.md
├── _comparison.md
├── _decision.md
└── _templates.md

docs/patterns/bitmask_dp/
├── templates.md    # Generated
└── intuition.md    # Manual

solutions/
├── 0078_subsets.py              # Existing, updated
├── 0847_shortest_path_visiting_all_nodes.py  # New
└── 1125_smallest_sufficient_team.py          # New

generators/
├── 0078_subsets.py              # Existing
├── 0847_shortest_path_visiting_all_nodes.py  # New
└── 1125_smallest_sufficient_team.py          # New

tests/
├── 0847_shortest_path_visiting_all_nodes_{1-5}.{in,out}
└── 1125_smallest_sufficient_team_{1-5}.{in,out}

meta/problems/
├── 0078_subsets.toml            # Updated
├── 0847_shortest_path_visiting_all_nodes.toml  # New
└── 1125_smallest_sufficient_team.toml          # New

roadmaps/
└── bitmask_dp_path.toml         # New
```

---

## Related Documentation

| Document | Content |
|----------|---------|
| [Solution Contract](../contracts/solution-contract.md) | Solution file requirements |
| [Generator Contract](../contracts/generator-contract.md) | Test generator requirements |
| [Test File Format](../contracts/test-file-format.md) | `.in`/`.out` file format |
| [Ontology Design](../reference/ontology-design.md) | Taxonomy structure |
| [Pattern Docs Tool](../tools/patterndocs/README.md) | Documentation generator |

# Code Review: File-Level Docstring

> **Purpose**: Standard format for solution file docstrings  
> **Scope**: All solution files in `solutions/`  
> **Last Updated**: {{ git_revision_date_localized }}

This document defines the **File-Level Docstring** format for solution files. All solution files SHOULD conform to this specification.

---

## Required Format

Every solution file SHOULD start with a docstring describing the problem using the following format:

```python
"""
Problem: {Problem Title}
Link: https://leetcode.com/problems/{slug}/

{Brief problem description}

Constraints:
- {constraint 1}
- {constraint 2}
"""
```

### Field Definitions

| Field | Required | Description |
|-------|----------|-------------|
| `Problem` | ✅ | Problem title (matches LeetCode title) |
| `Link` | ✅ | LeetCode problem URL |
| Description | Recommended | Brief problem statement explaining what the problem asks |
| `Constraints` | Recommended | Key constraints affecting algorithm choice |

### Format Rules

1. **No decorative separators**: Do NOT use `===` or `---` separators
2. **Simple structure**: Keep it concise and focused on essential information
3. **Constraints format**: Use bullet points with `-` prefix
4. **Line breaks**: Use single blank line between sections

---

## Examples

### Example 1: Basic Format

```python
# solutions/0001_two_sum.py
"""
Problem: Two Sum
Link: https://leetcode.com/problems/two-sum/

Given an array of integers nums and an integer target, 
return indices of the two numbers such that they add up to target.

Constraints:
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
- Only one valid answer exists.
"""
```

### Example 2: Multi-line Description

```python
# solutions/0025_reverse_nodes_in_k_group.py
"""
Problem: Reverse Nodes in k-Group
Link: https://leetcode.com/problems/reverse-nodes-in-k-group/

Given the head of a linked list, reverse the nodes of the list k at a time,
and return the modified list.

k is a positive integer and is less than or equal to the length of the linked list.
If the number of nodes is not a multiple of k then left-out nodes, in the end,
should remain as it is.

Constraints:
- The number of nodes in the list is n.
- 1 <= k <= n <= 5000
- 0 <= Node.val <= 1000
"""
```

### Example 3: With Optional Extension Fields

For problems that benefit from pattern classification, you MAY include optional fields:

```python
# solutions/0039_combination_sum.py
"""
Problem: Combination Sum
Link: https://leetcode.com/problems/combination-sum/

Given an array of distinct integers and a target, return all unique
combinations where the chosen numbers sum to target. Each number may
be used unlimited times.

Sub-Pattern: Target search with element reuse
Key Insight: Allow reuse by NOT incrementing start_index when recursing.
Prune branches where remaining target < 0 or current element > remaining.

Constraints:
- 1 <= candidates.length <= 30
- 2 <= candidates[i] <= 40
- All elements of candidates are distinct
- 1 <= target <= 40
"""
```

**Optional Extension Fields** (use sparingly, only when helpful):
- `Sub-Pattern`: Sub-pattern classification
- `Key Insight`: Key algorithmic insight
- `API Kernel`: API kernel used (e.g., `TwoPointersTraversal`)
- `Pattern`: Pattern name (e.g., `same_direction_writer`)
- `Family`: Problem family (e.g., `in_place_array_modification`)

---

## Anti-Patterns (DO NOT USE)

### ❌ Decorative Separators

```python
"""
================================================================================
LeetCode 26: Remove Duplicates from Sorted Array
================================================================================
...
--------------------------------------------------------------------------------
TWO POINTERS PATTERN: SAME-DIRECTION (READER/WRITER)
--------------------------------------------------------------------------------
...
================================================================================
"""
```

**Why**: Adds visual clutter without value. Keep it simple.

### ❌ Excessive Detail in Docstring

```python
"""
Problem: ...
Link: ...

Detailed algorithm explanation...
Pointer Roles:
- READ pointer (fast): ...
- WRITE pointer (slow): ...
INVARIANT: ...
Algorithm:
1. ...
2. ...
...
"""
```

**Why**: Detailed explanations belong in solution block comments, not the file-level docstring.

### ❌ Missing Required Fields

```python
"""
Given an array of integers...
"""
```

**Why**: Missing `Problem` and `Link` fields make it hard to identify the problem.

---

## Checklist

When reviewing or creating a solution file, verify:

- [ ] File starts with docstring (triple quotes)
- [ ] `Problem:` field is present and matches LeetCode title
- [ ] `Link:` field is present and points to correct LeetCode URL
- [ ] Brief problem description is included
- [ ] `Constraints:` section is included with bullet points
- [ ] No decorative separators (`===`, `---`)
- [ ] Format is concise and readable
- [ ] Optional extension fields (if used) are placed before Constraints

---

## Related Documentation

- [Solution Contract](solution-contract.md) - Complete solution file specification
- [Generator Contract](generator-contract.md) - Test generator requirements


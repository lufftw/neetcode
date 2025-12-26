# Code Review: File-Level Docstring

> **Purpose**: Standard format for solution file docstrings  
> **Scope**: All solution files in `solutions/`  
> **Last Updated**: {{ git_revision_date_localized }}

This document defines the **File-Level Docstring** format for solution files.

!!! info "Auto-Generated Docstrings"
    This specification is for **auto-generated docstrings** maintained by project tooling (e.g., `review-code` tool). The format is intentionally detailed to preserve all LeetCode problem information.
    
    **For manual contribution**, follow the simpler format in [solution-contract.md#file-level-docstring](solution-contract.md#file-level-docstring) instead.

---

## Required Format

Every solution file SHOULD start with a docstring describing the problem using the following format:

```python
"""
Problem: {Problem Title}
Link: https://leetcode.com/problems/{slug}/

{Brief problem description}

Example 1:
    <img ...>  # if present, preserve the img tag
    Input: {input}
    Output: {output}
    Explanation: {explanation line 1}
    {continuation lines...}

Example 2:
    Input: {input}
    Output: {output}

... (include ALL examples from LeetCode, Explanation may span multiple lines)

Constraints:
- {constraint 1}
- {constraint 2}

Topics: {topic1}, {topic2}, ...

Hint 1: {hint 1}

Hint 2: {hint 2}

... (include ALL hints from LeetCode)

Note: {optional additional notes}

Follow-up: {optional follow-up question 1}
Follow-up: {optional follow-up question 2}
"""
```

### Field Definitions

| Field | Required | Description |
|-------|----------|-------------|
| `Problem` | ✅ | Problem title (matches LeetCode title) |
| `Link` | ✅ | LeetCode problem URL (must include `/description/` suffix) |
| Description | Recommended | Brief problem statement explaining what the problem asks |
| `Example` | Recommended | All examples from LeetCode (Input/Output with optional Explanation). Preserve `<img>` tags if present. |
| `Constraints` | Recommended | ALL constraints from LeetCode (include as many as present). Use bullet points with `-` prefix. |
| `Topics` | Recommended | Comma-separated topic tags from LeetCode (e.g., Array, Two Pointers, Hash Table). Blank line before it. |
| `Hints` | Optional | ALL progressive hints from LeetCode (if present). Use numbered format `Hint 1:`, `Hint 2:`, etc. Each hint on its own line with blank line between. |
| `Note` | Optional | Additional notes from LeetCode (if present). Blank line before it. |
| `Follow-up` | Optional | Follow-up challenge questions from LeetCode (if present). Blank line before it. May have multiple. |

### Format Rules

1. **No decorative separators**: Do NOT use `===` or `---` separators
2. **Simple structure**: Keep it concise and focused on essential information
3. **Examples format**: Use 4-space indentation for Input/Output/Explanation lines. Explanation may span multiple lines (align continuation with first line). Include ALL examples from LeetCode. Preserve `<img>` tags for visual examples. Preserve ASCII art (trees/graphs) as-is.
4. **Constraints format**: Use bullet points with `-` prefix
5. **Line breaks**: Use single blank line between sections
6. **HTML tag handling**:
   - `<img>` → Preserve as-is
   - `<sup>` → Convert to `^` notation (e.g., `10<sup>9</sup>` → `10^9`)
   - `<strong>`, `<code>`, `<b>`, `<em>` → Strip tags, keep plain text
   - `<pre>` → Preserve code block content

---

## Examples

### Example 1: Basic Format with Topics and Hints

```python
# solutions/0001_two_sum.py
"""
Problem: Two Sum
Link: https://leetcode.com/problems/two-sum/

Given an array of integers nums and an integer target, 
return indices of the two numbers such that they add up to target.

Example 1:
    Input: nums = [2,7,11,15], target = 9
    Output: [0,1]
    Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
    Input: nums = [3,2,4], target = 6
    Output: [1,2]

Constraints:
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
- Only one valid answer exists.

Topics: Array, Hash Table

Hint 1: A really brute force way would be to search for all possible pairs of numbers but that would be too slow.

Hint 2: Try to reduce the search space by using a hash table.

Hint 3: For each element, check if the complement (target - current) exists in the hash table.

Follow-up: Can you come up with an algorithm that is less than O(n^2) time complexity?
"""
```

### Example 2: With Image in Examples

```python
# solutions/0011_container_with_most_water.py
"""
Problem: Container With Most Water
Link: https://leetcode.com/problems/container-with-most-water/

You are given an integer array height of length n. There are n vertical lines
drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container, such that the
container contains the most water.

Example 1:
    <img alt="" src="https://s3-lc-upload.s3.amazonaws.com/uploads/2018/07/17/question_11.jpg" style="width: 600px; height: 287px;">
    Input: height = [1,8,6,2,5,4,8,3,7]
    Output: 49
    Explanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7].
                 In this case, the max area of water (blue section) the container can contain is 49.

Example 2:
    Input: height = [1,1]
    Output: 1

Constraints:
- n == height.length
- 2 <= n <= 10^5
- 0 <= height[i] <= 10^4
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

Example 1:
    Input: candidates = [2,3,6,7], target = 7
    Output: [[2,2,3],[7]]

Example 2:
    Input: candidates = [2,3,5], target = 8
    Output: [[2,2,2,2],[2,3,3],[3,5]]

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

### Example 4: With ASCII Tree and Note

```python
# solutions/0104_maximum_depth_of_binary_tree.py
"""
Problem: Maximum Depth of Binary Tree
Link: https://leetcode.com/problems/maximum-depth-of-binary-tree/

Given the root of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path
from the root node down to the farthest leaf node.

Example 1:
        3
       / \
      9  20
        /  \
       15   7
    Input: root = [3,9,20,null,null,15,7]
    Output: 3

Example 2:
    Input: root = [1,null,2]
    Output: 2

Constraints:
- The number of nodes in the tree is in the range [0, 10^4].
- -100 <= Node.val <= 100

Topics: Tree, Depth-First Search, Breadth-First Search, Binary Tree

Note: The tree is represented as level-order traversal where null indicates missing nodes.

Follow-up: Can you solve it both recursively and iteratively?
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
- [ ] `Example:` section includes ALL examples (Input/Output), with `<img>` tags and ASCII art preserved
- [ ] `Constraints:` section includes ALL constraints with bullet points (use `^` for superscripts)
- [ ] `Topics:` included with comma-separated topic tags (with blank line before it)
- [ ] `Hints:` included if present in LeetCode (numbered format: `Hint 1:`, `Hint 2:`, blank line between each)
- [ ] `Note:` included if present in LeetCode (with blank line before it)
- [ ] `Follow-up:` included if present in LeetCode (with blank line before it, may have multiple)
- [ ] No decorative separators (`===`, `---`)
- [ ] Format is concise and readable
- [ ] Optional extension fields (if used) are placed before Constraints

---

## Related Documentation

- [Solution Contract § File-Level Docstring](solution-contract.md#file-level-docstring) - **Simplified format for manual contribution**
- [Solution Contract](solution-contract.md) - Complete solution file specification
- [Generator Contract](generator-contract.md) - Test generator requirements


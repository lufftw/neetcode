# Markmap Format Guide

This guide describes all formatting features available in Markmap that you can use.

## YAML Frontmatter

Always start with frontmatter:

```yaml
---
title: Your Markmap Title
markmap:
  colorFreezeLevel: 2    # Colors stay consistent from level 2
  maxWidth: 300          # Max width for text wrapping
  initialExpandLevel: 2  # Initially expand to level 2
---
```

## Headings (Tree Structure)

```markdown
# Level 1 (Root)
## Level 2
### Level 3
#### Level 4
##### Level 5
```

## Links

```markdown
- [Display Text](https://example.com)
- [LeetCode 125 Valid Palindrome](https://leetcode.com/problems/valid-palindrome/)
- [GitHub Solution](https://github.com/user/repo/blob/main/solution.py)
```

## Text Formatting

```markdown
- **bold text**
- *italic text*
- ~~strikethrough~~
- ==highlight==
- `inline code`
```

## Checkboxes (Progress Tracking)

```markdown
- [x] Completed item ✓
- [ ] Pending item ○
```

## KaTeX Math

Inline math:
```markdown
- Time: $O(n)$
- Space: $O(1)$
- Formula: $x = {-b \pm \sqrt{b^2-4ac} \over 2a}$
```

Common complexity notations:
- `$O(1)$` - Constant
- `$O(\log n)$` - Logarithmic
- `$O(n)$` - Linear
- `$O(n \log n)$` - Linearithmic
- `$O(n^2)$` - Quadratic
- `$O(2^n)$` - Exponential

## Folding (Collapse Dense Sections)

Add `<!-- markmap: fold -->` after a node to collapse it by default:

```markdown
## Large Section <!-- markmap: fold -->
- Item 1
- Item 2
- Item 3
- ... (many items)
```

## Code Blocks

```markdown
```python
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target-n], i]
        seen[n] = i
```
```

## Tables

```markdown
| Difficulty | Count | Progress |
|------------|-------|----------|
| Easy       | 50    | 80%      |
| Medium     | 75    | 45%      |
| Hard       | 25    | 20%      |
```

## Images

```markdown
![Alt Text](https://example.com/image.png)
```

## Ordered Lists

```markdown
1. First step
2. Second step
3. Third step
```

## Unordered Lists

```markdown
- Item A
- Item B
  - Nested item
  - Another nested
- Item C
```

## Combined Example

```markdown
---
title: Algorithm Patterns
markmap:
  colorFreezeLevel: 2
---

# Algorithm Patterns

## Two Pointers <!-- markmap: fold -->

### Opposite Direction
- [x] [LeetCode 125 Valid Palindrome](https://github.com/.../0125.py) ✓
  - **Easy** | $O(n)$ time | $O(1)$ space
- [ ] [LeetCode 167 Two Sum II](https://leetcode.com/problems/two-sum-ii/) ○
  - **Medium** | $O(n)$ time

### Same Direction
- [x] [LeetCode 26 Remove Duplicates](https://github.com/.../0026.py) ✓

## Sliding Window <!-- markmap: fold -->

### Fixed Size
- [ ] [LeetCode 643 Max Average Subarray](https://leetcode.com/problems/maximum-average-subarray-i/) ○

### Dynamic Size
- [x] [LeetCode 3 Longest Substring](https://github.com/.../0003.py) ✓
  - **Medium** | $O(n)$ time | $O(min(m,n))$ space

## Progress Summary

| Category | Solved | Total |
|----------|--------|-------|
| Two Pointers | 2 | 3 |
| Sliding Window | 1 | 2 |
```

## Best Practices

1. **Use folding** for sections with >8 children
2. **Keep depth to 3-5 levels** for readability
3. **Include complexity** when available
4. **Use checkboxes** for all problems
5. **Bold important items** (difficulty, key terms)
6. **Use consistent naming** throughout
7. **Add status icons** (✓ solved, ○ unsolved)


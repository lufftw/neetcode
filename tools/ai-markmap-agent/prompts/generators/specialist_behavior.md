# Behavior: The Specialist

## Task

Generate a technically precise, engineering-oriented Markmap based on the provided metadata and ontology.

---

## Input

### Problem Data (Compressed Format)
```
{metadata}
```

**Data Format Explanation:**
- Compact JSON with short keys: `i`=id, `t`=title, `d`=difficulty, `p`=patterns, `s`=has_solution, `sf`=solution_file, `tp`=topics
- Difficulty: `E`=Easy, `M`=Medium, `H`=Hard
- `s`=true means we have a solution (link to GitHub), `s`=false means no solution yet (link to LeetCode)

### Ontology
```
{ontology}
```

### Language
{language}  <!-- "en" or "zh-TW" -->

---

## Link Generation Rules

**IMPORTANT: Use correct URLs based on solution status**

1. **If problem has solution (`s: true`):**
   - Link to GitHub: `https://github.com/lufftw/neetcode/blob/main/{sf}`
   - Format: `[Problem Title](github_url)` ✓

2. **If problem has no solution (`s: false`):**
   - Link to LeetCode: `https://leetcode.com/problems/{slug}/`
   - Format: `[Problem Title](leetcode_url)` ○

**Example:**
```markdown
### Binary Search
- [Binary Search](https://github.com/lufftw/neetcode/blob/main/solutions/0704_binary_search.py) ✓
  - Time: $O(\log n)$
- [Search in Rotated Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) ○
```

---

## Markmap Format Guide

Use rich Markdown features for technical precision:

### Supported Features

| Feature | Syntax | Technical Use Case |
|---------|--------|-------------------|
| **Bold** | `**text**` | Algorithm names, key data structures |
| `Inline code` | `` `code` `` | Function names, API signatures |
| Links | `[text](url)` | LeetCode problems, documentation |
| Math (KaTeX) | `$O(n \log n)$` | Complexity analysis |
| Tables | `\| A \| B \|` | Complexity comparisons |
| Code blocks | ` ``` ` | Implementation patterns |

### Technical Annotations

```markdown
### QuickSort
- [Sort Colors](https://github.com/...) ✓
  - Time: $O(n \log n)$ avg, $O(n^2)$ worst
  - Space: $O(\log n)$
  - Stability: **Unstable**

### Binary Search
- **Prerequisite**: Sorted array
- Variants: `lower_bound`, `upper_bound`
- [Search Insert Position](https://leetcode.com/problems/...) ○
```

### Complexity Notation (KaTeX)

| Notation | Syntax |
|----------|--------|
| O(n) | `$O(n)$` |
| O(n log n) | `$O(n \log n)$` |
| O(n²) | `$O(n^2)$` |
| O(2ⁿ) | `$O(2^n)$` |
| θ notation | `$\Theta(n)$` |

---

## Generation Process

### Step 1: Technical Analysis
1. Parse the compressed problem data format
2. Identify core algorithms and data structures from patterns
3. Group by technical classification (complexity, pattern type)

### Step 2: Design Structure
1. Organize by technical classification (not learning order)
2. Group by time/space complexity patterns
3. Ensure consistent categorization criteria

### Step 3: Precise Annotation
1. Add complexity for every algorithm: `$O(n)$`
2. Include prerequisites and dependencies
3. Link to problems with correct URL (GitHub if solved, LeetCode if not)
4. Mark solved with ✓, unsolved with ○

### Step 4: Technical Validation
1. Verify complexity annotations are correct
2. Check all links use correct URL pattern
3. Confirm relationships are accurate

---

## Output Format

```markdown
# Technical Domain Name

## Module 1: Category
### Component 1.1 <!-- markmap: fold -->
- **Algorithm**: `FunctionName`
- Time: $O(n \log n)$
- Space: $O(n)$
- [LeetCode 704](https://github.com/lufftw/neetcode/blob/main/solutions/0704_binary_search.py) ✓

### Component 1.2
| Operation | Time | Space |
|-----------|------|-------|
| Insert | $O(\log n)$ | $O(1)$ |
| Delete | $O(\log n)$ | $O(1)$ |

## Module 2: Category
### Component 2.1
- **Prerequisite**: Component 1.1
- [Unsolved Problem](https://leetcode.com/problems/...) ○
```

---

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Algorithms | PascalCase | `BinarySearch`, `QuickSort` |
| Functions | snake_case or camelCase | `lower_bound`, `findMin` |
| Complexity | KaTeX math | `$O(n \log n)$` |
| Data Structures | PascalCase | `BinaryHeap`, `SegmentTree` |

---

## Quality Standards

| Dimension | Requirement |
|-----------|-------------|
| Technical Accuracy | Correct complexity, accurate relationships |
| Structural Rigor | Consistent classification logic |
| Links | Correct URL based on solution status |
| Engineering Utility | Reference value for developers |
| Rich Notation | Use KaTeX, code, tables appropriately |

---

## Output

Generate only the Markmap in Markdown format. No additional explanations needed.
Include complexity analysis, code references, and technical annotations throughout.
Ensure all problem links follow the URL selection logic based on solution status.

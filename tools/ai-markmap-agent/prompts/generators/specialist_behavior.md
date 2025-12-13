# Behavior: The Specialist

## Task

Generate a technically precise, engineering-oriented Markmap based on the provided metadata and ontology.

---

## Input

### Metadata
```
{metadata}
```

### Ontology
```
{ontology}
```

### Language
{language}  <!-- "en" or "zh-TW" -->

---

## Markmap Format Guide

Markmap supports rich Markdown features. Use them for technical precision:

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
- Time: $O(n \log n)$ avg, $O(n^2)$ worst
- Space: $O(\log n)$
- Stability: **Unstable**
- [Implementation](url)

### Binary Search
- **Prerequisite**: Sorted array
- Variants: `lower_bound`, `upper_bound`
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
1. Identify core algorithms and data structures
2. Analyze dependencies between concepts
3. Determine complexity characteristics

### Step 2: Design Structure
1. Organize by technical classification (not learning order)
2. Group by time/space complexity patterns
3. Ensure consistent categorization criteria

### Step 3: Precise Annotation
1. Add complexity for every algorithm: `$O(n)$`
2. Include prerequisites and dependencies
3. Link to canonical problems: `[LC XXX](url)`
4. Use code formatting for implementations

### Step 4: Technical Validation
1. Verify complexity annotations are correct
2. Check terminology follows conventions
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
- [LC 704](https://leetcode.com/problems/704) Binary Search

### Component 1.2
| Operation | Time | Space |
|-----------|------|-------|
| Insert | $O(\log n)$ | $O(1)$ |
| Delete | $O(\log n)$ | $O(1)$ |

## Module 2: Category
### Component 2.1
- **Prerequisite**: Component 1.1
- Implementation pattern:
  ```python
  def solve(arr):
      pass
  ```
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
| Engineering Utility | Reference value for developers |
| Completeness | Cover key algorithms and patterns |
| Rich Notation | Use KaTeX, code, tables appropriately |

---

## Output

Generate only the Markmap in Markdown format. No additional explanations needed.
Include complexity analysis, code references, and technical annotations throughout.

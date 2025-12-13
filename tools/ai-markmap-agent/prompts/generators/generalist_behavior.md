# Behavior: The Generalist

## Task

Generate a well-structured, comprehensive Markmap based on the provided metadata and ontology.

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
   - Format: `[Problem Title](github_url)`

2. **If problem has no solution (`s: false`):**
   - Link to LeetCode: `https://leetcode.com/problems/{slug}/`
   - Format: `[Problem Title](leetcode_url)`

**Example:**
```markdown
- [Two Sum](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py) ✓
- [Median of Two Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) ○
```

Use ✓ for solved, ○ for unsolved (optional visual indicator).

---

## Markmap Format Guide

Markmap supports rich Markdown features. Use them effectively:

### Supported Features

| Feature | Syntax | Use Case |
|---------|--------|----------|
| **Bold** | `**text**` | Emphasize key concepts |
| *Italic* | `*text*` | Secondary emphasis |
| ~~Strikethrough~~ | `~~text~~` | Deprecated items |
| ==Highlight== | `==text==` | Important terms |
| `Inline code` | `` `code` `` | Technical terms, API names |
| Links | `[text](url)` | References to docs/problems |
| Checkboxes | `- [x] item` | Completed items in learning paths |
| Math (KaTeX) | `$O(n)$` | Complexity notation |

### Structure Rules

1. **Hierarchy**: Use `#`, `##`, `###` for levels (max 4-5 levels)
2. **Lists**: Use `-` for unordered, `1.` for ordered
3. **Folding**: Add `<!-- markmap: fold -->` to collapse sections by default
4. **Code blocks**: Use triple backticks for code examples
5. **Tables**: Use for structured comparisons

### Example Structure

```markdown
# NeetCode Patterns

## Sliding Window
### Fixed Size
- [x] [Maximum Sum Subarray](https://github.com/...) `$O(n)$` ✓
- [ ] [Subarray Average](https://leetcode.com/problems/...) ○

### Variable Size <!-- markmap: fold -->
- [Longest Substring](https://github.com/...)
- [Minimum Window](https://leetcode.com/problems/...)
  - Complexity: $O(n)$
```

---

## Generation Process

### Step 1: Analyze Input
1. Parse the compressed problem data format
2. Identify main topics/domains from patterns and topics
3. Group problems by patterns, difficulty, or learning path

### Step 2: Design Structure
1. Determine root node (clear, descriptive title)
2. Plan 3-7 level-1 categories (most important first)
3. Design subcategories (2-3 levels deep)
4. Keep depth within 3-4 levels for readability

### Step 3: Enrich Content
1. Add links using correct URL (GitHub if solved, LeetCode if not)
2. Include complexity annotations: `$O(n)$`
3. Mark solved problems: `✓` or `[x]`
4. Add `<!-- markmap: fold -->` to dense sections
5. Use **bold** for key terms, `code` for technical names

### Step 4: Review & Optimize
1. Check if structure is balanced
2. Verify all links use correct URL pattern
3. Ensure labels are intuitive and understandable

---

## Output Format

Generate a complete Markmap in Markdown:

```markdown
# Topic Name

## Category 1
### Subcategory 1.1
- **Key Concept** - description
- [Problem Name](url) `$O(n)$` ✓
### Subcategory 1.2 <!-- markmap: fold -->
- [Unsolved Problem](leetcode_url) ○

## Category 2
### Subcategory 2.1
- [x] Completed item
- [ ] Pending item
```

---

## Quality Standards

| Dimension | Requirement |
|-----------|-------------|
| Completeness | Cover all major concepts from metadata |
| Structure | Clear hierarchy, logical classification |
| Balance | Similar depth across branches |
| Links | Correct URL based on solution status |
| Readability | Intuitive labels, no extra explanation needed |

---

## Output

Generate only the Markmap in Markdown format. No additional explanations needed.
Use the full range of Markmap features to create an informative, visually rich mindmap.
Ensure all problem links follow the URL selection logic based on solution status.

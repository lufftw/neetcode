# Behavior: The Generalist

## Task

Generate a well-structured, comprehensive Markmap based on the provided metadata and ontology.

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
- [x] Maximum Sum Subarray `O(n)`
- [x] [LC 643](https://leetcode.com/problems/643) - Subarray Average

### Variable Size <!-- markmap: fold -->
- Longest Substring Without Repeating
- Minimum Window Substring
  - Complexity: $O(n)$
```

---

## Generation Process

### Step 1: Analyze Input
1. Identify main topics/domains from metadata
2. Find core concepts and relationships from ontology
3. Determine target audience's knowledge level

### Step 2: Design Structure
1. Determine root node (clear, descriptive title)
2. Plan 3-7 level-1 categories (most important first)
3. Design subcategories under each (2-3 levels deep)
4. Keep depth within 3-4 levels for readability

### Step 3: Enrich Content
1. Add links to LeetCode problems: `[LC XXX](url)`
2. Include complexity annotations: `$O(n)$`
3. Use checkboxes for learning paths: `- [x] completed`
4. Add `<!-- markmap: fold -->` to dense sections
5. Use **bold** for key terms, `code` for technical names

### Step 4: Review & Optimize
1. Check if structure is balanced
2. Confirm no important concepts are missing
3. Verify labels are intuitive and understandable
4. Ensure rich formatting is used appropriately

---

## Output Format

Generate a complete Markmap in Markdown:

```markdown
# Topic Name

## Category 1
### Subcategory 1.1
- **Key Concept** - description
- [Problem Link](url) `O(n)`
### Subcategory 1.2 <!-- markmap: fold -->
- Detail A
- Detail B

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
| Readability | Intuitive labels, no extra explanation needed |
| Rich Formatting | Use links, code, math, emphasis appropriately |

---

## Output

Generate only the Markmap in Markdown format. No additional explanations needed.
Use the full range of Markmap features to create an informative, visually rich mindmap.

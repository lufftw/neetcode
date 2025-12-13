# Behavior: The Quality Judge

## Task

Evaluate the Markmap for quality, focusing on structure, naming, and technical accuracy.

---

## Input

### Markmap to Evaluate
```
{markmap}
```

### Evaluation Criteria
{criteria}

---

## Markmap Quality Checklist

A high-quality Markmap should:
- [ ] Use **bold**, `code`, and other formatting appropriately
- [ ] Include links to problems: `[LC XXX](url)`
- [ ] Show complexity with KaTeX: `$O(n)$`
- [ ] Have balanced depth across branches
- [ ] Use `<!-- markmap: fold -->` for dense sections
- [ ] Have clear, consistent naming

---

## Evaluation Process

### Step 1: Structure Quality (40%)

| Criterion | Score (1-10) | Evidence |
|-----------|--------------|----------|
| Hierarchy Logic | X | [Does the structure make sense?] |
| Balance | X | [Are branches roughly equal depth?] |
| Depth Appropriateness | X | [Not too shallow, not too deep?] |
| **Subtotal** | X/10 | |

**Structure Issues Found:**
1. [Issue and location]

### Step 2: Naming Consistency (30%)

| Criterion | Score (1-10) | Evidence |
|-----------|--------------|----------|
| Terminology Unity | X | [Consistent terms throughout?] |
| Naming Convention | X | [PascalCase, camelCase consistent?] |
| Label Clarity | X | [Self-explanatory names?] |
| **Subtotal** | X/10 | |

**Naming Issues Found:**
1. [Inconsistency and location]

### Step 3: Technical Accuracy (30%)

| Criterion | Score (1-10) | Evidence |
|-----------|--------------|----------|
| Content Correctness | X | [Algorithms named correctly?] |
| Complexity Accuracy | X | [Big-O notation correct?] |
| Relationship Accuracy | X | [Dependencies correct?] |
| **Subtotal** | X/10 | |

**Accuracy Issues Found:**
1. [Error and location]

### Step 4: Formatting Quality (Bonus)

| Feature | Present? | Quality |
|---------|----------|---------|
| Bold/emphasis | Yes/No | Good/Poor |
| Code formatting | Yes/No | Good/Poor |
| Links | Yes/No | Good/Poor |
| Math notation | Yes/No | Good/Poor |
| Folding | Yes/No | Good/Poor |

---

## Final Evaluation

### Overall Score

```json
{
  "score": X,
  "reasoning": "Summary of evaluation"
}
```

### Strengths
1. [Strength 1]
2. [Strength 2]

### Areas for Improvement
1. [Area 1]
2. [Area 2]

### Recommendation
[Overall assessment and recommendation]

---

## Output Format

Provide evaluation as:

```markdown
# Quality Evaluation Report

## Scores
- Structure Quality: X/10
- Naming Consistency: X/10
- Technical Accuracy: X/10
- **Overall**: X/10

## Key Findings

### Strengths
1. [Strength]

### Issues
1. [Issue]

## Final Assessment

```json
{
  "score": X,
  "reasoning": "One paragraph summary"
}
```
```

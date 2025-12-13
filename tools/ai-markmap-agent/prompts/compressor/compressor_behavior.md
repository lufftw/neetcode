# Behavior: The Compressor

## Task

When discussion records or content become too long, compress them into concise summaries while preserving key information.

---

## Trigger Conditions

Activate compression when:
- Discussion records exceed {max_tokens} tokens
- Markmap node count exceeds threshold
- Need to pass concise context to subsequent rounds

---

## Input

### Original Content
```
{original_content}
```

### Content Type
{content_type}  <!-- discussion | markmap | metadata -->

### Target Length
{target_tokens} tokens

### Priority Topics (if any)
{priority_topics}

---

## Compression Principles

### 🔴 Must Preserve (Critical)

| Type | Example |
|------|---------|
| Final decisions | "Decided to adopt Solution A" |
| Key rationales | "Because the structure is more balanced" |
| Consensus points | "All three optimizers agree that..." |
| Unresolved issues | "Naming convention to be discussed next round" |

### 🟡 Preserve If Possible (Important)

| Type | Example |
|------|---------|
| Major disagreements | "A thinks X, B thinks Y" |
| Trade-off considerations | "Sacrificed Z to gain W" |
| Key examples | "Like the handling of node ABC" |

### 🟢 Can Omit (Optional)

| Type | Example |
|------|---------|
| Lengthy explanations | Detailed reasoning process |
| Repeated statements | Multiple expressions of same point |
| Minor details | Discussion not affecting decisions |
| Polite phrases | "I think", "perhaps" |

---

## Compression Formats

### Discussion Record Compression

```markdown
## Discussion Summary

### Decisions
1. [Decision 1]: [Brief rationale]
2. [Decision 2]: [Brief rationale]

### Disagreements
- [Issue]: A proposed X / B proposed Y → Adopted [Result]

### Consensus
- [Consensus point 1]
- [Consensus point 2]

### Pending
- [Issue 1]
- [Issue 2]
```

### Markmap Compression

Preserve structural framework, omit terminal details:

```markdown
## Markmap Summary

### Structure Overview
- Root node: [Name]
- Level-1 nodes: [List]
- Total depth: [Number]
- Total node count: [Number]

### Key Areas
1. [Area 1]: [Main content overview]
2. [Area 2]: [Main content overview]

### Simplified Markmap
[Only keep up to level 2-3]
```

### Metadata Compression

Extract core information:

```markdown
## Metadata Summary

### Core Concepts
- [Concept 1]
- [Concept 2]
- [Concept 3]

### Main Relationships
- [Relationship 1]
- [Relationship 2]

### Key Constraints
- [Constraint 1]
```

---

## Output Format

```markdown
# Compression Report

## Compressed Content

[Compressed content]

---

## Compression Statistics
- Original length: ~{original_tokens} tokens
- Compressed length: ~{compressed_tokens} tokens
- Compression ratio: {ratio}%

## Omitted Content Index

The following content has been omitted. Refer to original records for details:

| Omitted Item | Reason | Original Location |
|--------------|--------|-------------------|
| [Item 1] | Repeated/Secondary/Verbose | Round X discussion |
| [Item 2] | ... | ... |

## Preservation Confirmation

✅ All decisions preserved
✅ Key rationales preserved
✅ Unresolved issues marked
⚠️ Detailed discussion process omitted
```

---

## Quality Check

Self-check after compression:

1. ✅ All final decisions documented?
2. ✅ Key rationales preserved?
3. ✅ Unresolved issues marked?
4. ✅ Compressed content within target length?
5. ✅ Omitted content indexed for reference?

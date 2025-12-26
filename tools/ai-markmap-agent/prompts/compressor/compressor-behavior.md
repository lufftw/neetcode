# Behavior: The Compressor

## Task

Compress long content while preserving essential information for context passing.

---

## Input

### Content to Compress
```
{content}
```

### Target Compression
Reduce to approximately {target_ratio}% of original length.

---

## Compression Priorities

### 🔴 Must Preserve (Critical)
| Type | Example |
|------|---------|
| Final decisions | "Adopted X structure" |
| Key rationale | "Because of Y" |
| Consensus points | "All agreed on Z" |
| Unresolved issues | "Still debating A" |

### 🟡 Preserve If Possible (Important)
| Type | Example |
|------|---------|
| Major disagreements | "A vs B on X" |
| Trade-offs made | "Chose X over Y" |
| Key examples | "Like node ABC" |

### 🟢 Can Omit (Optional)
| Type | Example |
|------|---------|
| Lengthy explanations | Detailed reasoning |
| Repeated statements | Same point multiple times |
| Minor details | Doesn't affect decisions |
| Filler phrases | "I think", "perhaps" |

---

## Compression Formats

### For Discussion Records

```markdown
## Compressed Summary

### Decisions Made
1. [Decision]: [Brief rationale]

### Key Disagreements
- [Issue]: [Resolution]

### Pending Items
- [Item 1]
```

### For Markmaps

Preserve structure, remove leaf details:

```markdown
## Structure Summary
- Root: [Name]
- L1 Branches: [List]
- Total Depth: [N]
- Key Areas: [Summary of main branches]
```

---

## Output

Provide compressed content only. No meta-commentary.

Focus on:
1. What was decided
2. Why it was decided
3. What's still unresolved

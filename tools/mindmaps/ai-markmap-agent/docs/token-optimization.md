# Token Optimization Guide

This document describes the token optimization strategies implemented in the AI Markmap Agent expert system.

## Core Principles

### What We Optimize

| Category | Strategy | Savings |
|----------|----------|---------|
| Redundant instructions | Streamline phase_instructions | ~210 tokens/run |
| Peripheral problem data | Tiered delivery | ~26% |
| Unreferenced baseline sections | Relevant extraction in Round 2 | ~46% |

### What We Protect

| Principle | Rationale |
|-----------|-----------|
| **Full baseline in Round 1** | Foundation for serendipitous discoveries |
| **Why field in suggestions** | The reasoning spine of expert discussion |
| **Cross-domain visibility** | Experts may find insights outside their focus |

### Anti-Patterns (Do NOT)

- ❌ Assume LLM remembers Round 1 content in Round 2
- ❌ Use `minimal` format for problems (loses critical context)
- ❌ Compress suggestions to lose rationale
- ❌ Optimize away the expert's ability to "see the full picture"

---

## Design Philosophy

> **Token optimization reduces "redundant & useless", not "understanding & reasoning".**
>
> If optimization makes experts "see less, think shallower", the saved tokens become quality debt.

### The Serendipity Principle

The real risk of aggressive optimization is not "seeing less data" but "thinking fewer thoughts."

Experts in this system don't just classify—they review structure and learning paths. Any strategy that limits their view of the whole picture damages **insight space**, not just information.

### The Stateless Principle

LLM calls are stateless. Round 2 does NOT remember Round 1.

Assuming the LLM "remembers" is a **system design error**, not an optimization opportunity.

---

## Implementation Details

### Phase 1: Streamline Phase Instructions

**Location:** `src/agents/expert.py` → `_get_phase_instructions()`

**Before:**
```python
return """You are conducting an **independent review** of the Markmap.

Focus on your areas of expertise and identify concrete improvements.
Do NOT consider other experts' opinions yet—this is your independent assessment.
Be thorough but practical. Prioritize high-impact improvements."""
```

**After:**
```python
return """**Independent Review** — Do NOT consider other experts' opinions.
Identify concrete improvements from your expertise. Be thorough but practical."""
```

**Rationale:** Detailed instructions exist in behavior prompts (`architect-behavior.md`, etc.). Phase instructions only need to emphasize key constraints.

---

### Phase 2: Tiered Problem Data

**Location:** `src/agents/expert.py` → `_format_problems_tiered()`

**Structure:**
```
Tier 1 — Problems in baseline (full detail)
| ID | Title | Difficulty | Patterns |
|---|---|---|---|
| 0003 | Longest Substring Without... | medium | sliding_window |

Tier 2 — Other solved problems (compact)
- EASY: 0001, 0021, 0070
- MEDIUM: 0015, 0049, 0053

Tier 3 — Unsolved (20 problems)
IDs: 0081, 0082, 0083...
```

**Why this works:**
- Tier 1 preserves full context for problems experts will actually discuss
- Tier 2 shows what's available without bloating the prompt
- Tier 3 is reference-only (experts rarely discuss unsolved problems)

---

### Phase 3: Relevant Baseline Extraction

**Location:** `src/agents/expert.py` → `_extract_relevant_baseline()`

**Algorithm:**

1. **Parse baseline** into sections by `##` headings
2. **Extract keywords** from suggestion `location` fields:
   - Quoted strings: `"Sliding Window"`
   - Kernel references: `Kernel 1`, `Kernel 2`
   - Pattern names: `sliding_window_unique`
   - Common section names: `backtracking`, `two pointer`
3. **Match sections** using multiple strategies:
   - Direct substring match
   - Normalized match (ignore spaces/special chars)
   - Word overlap (e.g., "two pointer" matches "TwoPointersTraversal")
   - Content pattern match (snake_case in section content)
4. **Safety fallback** if matching is too sparse:
   ```python
   if len(matched) < 2:           # At least 2 sections
       return full_baseline
   if match_ratio < 0.3:          # At least 30% of sections
       return full_baseline
   ```

**Output format:**
```markdown
*Showing 8/12 sections relevant to suggestions*
*Keywords matched: backtracking, heap, kernel 1, sliding window...*

--- Section: Kernel 1: SubstringSlidingWindow (lines 27-64) ---
[section content]

--- Section: Kernel 2: TwoPointersTraversal (lines 65-105) ---
[section content]
```

---

## Metrics

### Token Savings by Phase

| Phase | Target | Estimated Savings |
|-------|--------|-------------------|
| Phase 1 | Phase instructions | ~210 tokens/run |
| Phase 2 | Problem data section | ~26% of problem tokens |
| Phase 3 | Baseline in Round 2 | ~46% of baseline tokens |

### Combined Effect

Assuming typical token composition per expert call:
- Baseline: ~10,000 tokens (Round 1 + Round 2 = 20,000)
- Problems: ~2,000 tokens
- Prompts: ~2,000 tokens

```
Phase 1: -210 tokens
Phase 2: -520 tokens (2,000 × 26%)
Phase 3: -4,600 tokens (10,000 × 46%, Round 2 only)

Total: ~5,330 tokens/run (~18% overall)
```

---

## Safety Mechanisms

### Fallback Conditions

The system falls back to full baseline when:

| Condition | Threshold | Rationale |
|-----------|-----------|-----------|
| Too few matched sections | < 2 | Minimum context required |
| Low match ratio | < 30% | May miss important context |
| No keywords extracted | 0 keywords | Cannot determine relevance |

### Debugging

The `_prepare_discussion_input()` method returns `_baseline_is_full` flag for logging:

```python
return {
    "baseline_markmap": relevant_baseline,
    "_baseline_is_full": is_full,  # True if fallback was triggered
}
```

---

## Future Considerations

### Potential Optimizations (Not Yet Implemented)

| Idea | Savings | Risk | Status |
|------|---------|------|--------|
| Suggestion truncation (keep Why) | 3-5% | Low | Considered |
| Expert-specific data filtering | 10-15% | Medium | Deferred |
| Incremental baseline diff | 20-30% | High | Not recommended |

### Why We Deferred Expert-Specific Filtering

Filtering data by expert role (e.g., Architect only sees API kernels) risks:
- Losing cross-domain insights
- Reducing "accidental discovery" opportunities
- Making experts overfit to their narrow focus

The current approach preserves **conservative visibility** while optimizing **redundancy**.

---

## References

- `src/agents/expert.py` — Implementation
- `docs/design-v4.md` — V4 architecture overview
- `prompts/experts/*.md` — Expert behavior prompts

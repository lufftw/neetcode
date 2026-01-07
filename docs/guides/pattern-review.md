# Pattern Review Guide

> **Status**: Canonical Reference
> **Scope**: Review process for pattern documentation quality
> **Last Updated**: {{ git_revision_date_localized }}
> **Created**: {{ git_creation_date_localized }}

This guide defines the systematic review process for pattern documentation in the NeetCode repository. Reviews ensure consistency, quality, and ontology alignment across all pattern templates.

---

## Table of Contents

- [1. Review Philosophy](#1-review-philosophy)
- [2. Gold Standards](#2-gold-standards)
- [3. Review Scope](#3-review-scope)
- [4. Review Criteria](#4-review-criteria)
- [5. Review Process](#5-review-process)
- [6. Combined Pattern + Solutions Review Workflow](#6-combined-pattern--solutions-review-workflow)
- [7. Recording Reviews](#7-recording-reviews)
- [8. Branch and Commit Protocol](#8-branch-and-commit-protocol)
- [9. Quality Tiers](#9-quality-tiers)

---

## 1. Review Philosophy

### 1.1 Core Principles

| Principle | Description |
|-----------|-------------|
| **Ontology-First** | Pattern Kernel and API Kernel must be clearly defined and consistently applied |
| **Template Reusability** | Templates must be generalizable, not single-problem optimized |
| **Pedagogical Clarity** | Explanations must teach the "why" beyond the "what" |
| **Engineering Quality** | Code must be production-grade with semantic naming |

### 1.2 Review Goals

- **Structural Consistency**: All templates follow the Gold Standard structure
- **Semantic Accuracy**: Pattern kernels correctly describe the algorithmic mechanism
- **Teaching Effectiveness**: Concepts build progressively from base to variants
- **Maintainability**: Templates support code generation and batch refactoring

### 1.3 What Review Is NOT

- NOT about adding new content
- NOT about optimizing individual problem solutions
- NOT about personal style preferences (when both approaches are valid)
- NOT about changing ontology definitions (separate process)

---

## 2. Gold Standards

### 2.1 Reference Templates

The following templates serve as **Gold Standards** and must NOT be modified during review:

| Pattern | Template | Purpose |
|---------|----------|---------|
| **Sliding Window** | `docs/patterns/sliding_window/templates.md` | Structural reference, semantic density benchmark |
| **Two Pointers** | `docs/patterns/two_pointers/templates.md` | Multi-variant organization model |
| **Backtracking** | `docs/patterns/backtracking_exploration/templates.md` | Complex pattern decomposition example |

### 2.2 Using Gold Standards

Gold Standards define the quality ceiling. When reviewing other templates:

1. **Structural Alignment**: Does the template follow the same section organization?
2. **Depth Calibration**: Is the explanation density comparable?
3. **Code Quality**: Does the code match the engineering standards?
4. **Pedagogical Flow**: Does learning progress similarly from base to variants?

---

## 3. Review Scope

### 3.1 Must Review

| Category | Files | Priority |
|----------|-------|----------|
| **Pattern Templates** | `docs/patterns/*/templates.md` (excluding Gold Standards) | High |
| **Pattern Intuitions** | `docs/patterns/*/intuition.md` | Medium |
| **Meta Pattern Sources** | `meta/patterns/*/*.md` | Medium |
| **Solution Files** | `solutions/*.py` (pattern-related) | Medium |

### 3.2 Excluded from Review

| Category | Reason |
|----------|--------|
| Gold Standard templates | Reference only |
| Ontology definitions | Separate governance process |
| Test files | Automated validation |
| Generator files | Separate contract |

---

## 4. Review Criteria

### 4.1 Conceptual Correctness (Algorithm Layer)

| Checkpoint | Question | Red Flag |
|------------|----------|----------|
| **Pattern Kernel** | Is the core mechanism clearly stated? | Missing `> **API Kernel**: \`...\`` header |
| **Invariant Definition** | Is the invariant explicitly defined? | Implicit or missing invariant |
| **State Transition** | Are state changes documented? | Magic state modifications |
| **Complexity Analysis** | Are Time/Space complexities correct? | Missing or incorrect O() |
| **Boundary Conditions** | Are edge cases addressed? | Silent failure modes |

### 4.2 Explanation Quality (Teaching Layer)

| Checkpoint | Question | Red Flag |
|------------|----------|----------|
| **Why Not Just What** | Does it explain WHY the approach works? | Only code, no reasoning |
| **Progressive Build** | Does complexity increase gradually? | Hard problems first |
| **Delta Clarity** | Are variant differences explicit? | Copy-paste variations |
| **Visual Aids** | Are traces/diagrams provided? | Wall of text |
| **Common Pitfalls** | Are mistakes documented? | Missing pitfall section |

### 4.3 Engineering Quality (Code Layer)

| Checkpoint | Question | Red Flag |
|------------|----------|----------|
| **Variable Naming** | Are names semantic and consistent? | `i`, `j`, `temp`, `val` abuse |
| **Type Hints** | Are Python type hints present? | Missing type annotations |
| **Docstrings** | Full docstrings with Args/Returns? | Empty or minimal docstrings |
| **Comments** | Are key steps commented (CHOOSE, EXPLORE, etc.)? | Uncommented dense logic |
| **Template Portability** | Can code be copy-pasted as a template? | Problem-specific logic embedded |

### 4.4 Structural Compliance

| Checkpoint | Question | Red Flag |
|------------|----------|----------|
| **Table of Contents** | Numbered TOC present? | Missing or unlinked TOC |
| **API Kernel Header** | Present immediately after title? | Missing or buried |
| **Core Concepts First** | Section 1 covers fundamentals? | Jumping to problems |
| **Base Template Second** | Section 2 is canonical example? | No clear base template |
| **Comparison Table** | Side-by-side variant comparison? | Missing comparison |
| **Quick Reference** | Copy-paste templates at end? | No quick reference |

---

## 5. Review Process

### 5.1 Pre-Review Preparation

```
1. Read Gold Standards (first time only)
2. Read pattern's templates.md completely
3. Read corresponding intuition.md
4. Read 2-3 related solution files
5. Check ontology entries for this pattern
```

### 5.2 Review Execution

```
For each review checkpoint:
  1. Identify: What is the specific issue?
  2. Classify: Concept | Explanation | Engineering
  3. Assess: Critical | Major | Minor | Nit
  4. Decide: Fix | Accept | Defer
  5. Record: Document in pattern-review-log.md
```

### 5.3 Issue Severity

| Severity | Definition | Action |
|----------|------------|--------|
| **Critical** | Incorrect algorithm or misleading explanation | Must fix before merge |
| **Major** | Missing key section or significant quality gap | Should fix |
| **Minor** | Style inconsistency or missing nice-to-have | Fix if convenient |
| **Nit** | Preference or tiny improvement | Record, don't fix |

### 5.4 Review Decision Matrix

```
                    ┌─────────────────────────────────┐
                    │ Does it match Gold Standard?    │
                    └─────────────────────────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
              ┌─────────┐                   ┌─────────┐
              │   YES   │                   │   NO    │
              └─────────┘                   └─────────┘
                    │                             │
                    ▼                             ▼
             ACCEPT as-is              Is deviation justified?
                                              │
                               ┌──────────────┴──────────────┐
                               │                             │
                               ▼                             ▼
                         ┌─────────┐                   ┌─────────┐
                         │   YES   │                   │   NO    │
                         └─────────┘                   └─────────┘
                               │                             │
                               ▼                             ▼
                    ACCEPT with note                    FIX required
```

---

## 6. Combined Pattern + Solutions Review Workflow

### 6.1 Context-Driven Solutions Audit

When reviewing pattern templates, **simultaneously audit the corresponding solutions**. Reading `templates.md` first provides the algorithmic context needed to improve solution quality.

**Workflow:**

```
1. Read docs/patterns/{pattern}/templates.md completely
2. For each problem referenced in templates.md:
   a. Read the corresponding solutions/{problem}.py
   b. Apply dual-perspective quality criteria (see 6.2)
   c. Improve comments and naming with pattern context
3. Record both template and solution findings in pattern-review-log.md
```

**Why Context Matters:**

| Without Context | With Context |
|-----------------|--------------|
| Generic variable names like `l`, `r`, `res` | Semantic names like `left_boundary`, `right_exclusive`, `max_contribution` |
| Vague comments "loop through array" | Precise comments "extend window until constraint violated" |
| Missing invariant documentation | Explicit invariant: "dp[i] represents optimal cost to reach position i" |

### 6.2 Dual-Perspective Quality Criteria

Solutions should satisfy both **pedagogical clarity** (teaching effectiveness) and **engineering quality** (production maintainability).

| Aspect | Pedagogical (Professor) | Engineering (Tech Lead) |
|--------|------------------------|-------------------------|
| **Comments** | Explain WHY the approach works | Keep concise, avoid redundancy |
| **Naming** | Self-documenting algorithm intent | Consistent, refactorable |
| **Structure** | Progressive logic flow | Minimal coupling, clean interfaces |
| **Complexity** | Explicit analysis with reasoning | Practical performance notes |

**Quality Fusion Guidelines:**

1. **Block comments**: Concise 3-4 bullet points (see Solution Contract)
2. **Internal comments**: Document key transitions and non-obvious logic
3. **Variable naming**: Semantic names reflecting algorithmic role
4. **State documentation**: Explicit invariants where applicable

### 6.3 Solutions Audit Checklist

For each solution file touched during pattern review:

- [ ] Block comment follows concise format (3-4 bullet points)
- [ ] Variable names are semantic and consistent with pattern vocabulary
- [ ] Key algorithmic transitions are documented inline
- [ ] State/invariant is explicit where applicable
- [ ] No redundant comments that merely restate the code

---

## 7. Recording Reviews

### 7.1 Review Log Location

All review findings must be recorded in:

```
docs/reviews/pattern-review-log.md
```

### 7.2 Log Entry Format

```markdown
## [Pattern Name] Review - [Date]

### Files Reviewed
- `docs/patterns/{pattern}/templates.md`
- `docs/patterns/{pattern}/intuition.md`
- Related solutions: `solutions/{files}.py`

### Reference Standards
- Gold Standard: `{which template used for comparison}`
- Ontology: `{relevant ontology entries}`

### Findings

#### [Finding ID]: [Short Title]

| Field | Value |
|-------|-------|
| **Category** | Concept / Explanation / Engineering |
| **Severity** | Critical / Major / Minor / Nit |
| **Location** | `{file}:{line_range}` |
| **Issue** | {Specific description of the problem} |
| **Why It Matters** | {Impact on ontology/teaching/maintainability} |
| **Decision** | Fix / Accept / Defer |
| **Resolution** | {What was done, if fixed} |

### Summary

| Category | Critical | Major | Minor | Nit | Total |
|----------|----------|-------|-------|-----|-------|
| Concept | X | X | X | X | X |
| Explanation | X | X | X | X | X |
| Engineering | X | X | X | X | X |
| **Total** | X | X | X | X | **X** |

### Action Items
- [ ] {Specific fix to apply}
- [ ] {Documentation update needed}
```

### 7.3 What NOT to Record

- Changes made without issues (silent fixes)
- Personal preferences overridden
- Temporary debugging observations

---

## 8. Branch and Commit Protocol

### 8.1 Branch Naming

```
review/pattern-{pattern_name}
review/pattern-quality-audit-{date}
```

### 8.2 Commit Structure

```bash
# Review log commit
git commit -m "review({pattern}): Add review findings to log

Reviewed {pattern} pattern documentation:
- {N} critical issues identified
- {N} major issues identified
- {N} fixes applied

See docs/reviews/pattern-review-log.md"

# Fix commit
git commit -m "fix({pattern}): {Specific fix description}

Issue: {Finding ID from review log}
Impact: {What this fixes}

Refs: docs/reviews/pattern-review-log.md#{pattern}-{date}"
```

### 8.3 PR Requirements

Each review PR must include:

1. **Title**: `review({scope}): {Summary}`
2. **Body**: Link to relevant `pattern-review-log.md` section
3. **Checklist**:
   - [ ] All critical issues resolved
   - [ ] Review log updated
   - [ ] No changes to Gold Standards
   - [ ] No ontology changes (unless separate PR)

---

## 9. Quality Tiers

### 9.1 Tier Definitions

| Tier | Criteria | Examples |
|------|----------|----------|
| **Tier 1 (Gold)** | Reference quality, no issues | sliding_window, two_pointers, backtracking |
| **Tier 2 (Silver)** | Minor issues only, good structure | Most reviewed patterns |
| **Tier 3 (Bronze)** | Major issues, needs improvement | Newly generated patterns |
| **Tier 4 (Draft)** | Critical issues or incomplete | Work in progress |

### 9.2 Promotion Criteria

```
Tier 4 → Tier 3: All critical issues resolved
Tier 3 → Tier 2: All major issues resolved
Tier 2 → Tier 1: Peer-reviewed, community validated
```

### 9.3 Current Pattern Status

| Pattern | Current Tier | Last Review |
|---------|--------------|-------------|
| sliding_window | Tier 1 (Gold Standard) | N/A |
| two_pointers | Tier 1 (Gold Standard) | N/A |
| backtracking_exploration | Tier 1 (Gold Standard) | N/A |
| *Other patterns* | Tier 3-4 (Pending Review) | TBD |

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| [New Pattern Guide](new-pattern.md) | How to create patterns (separate from review) |
| [Ontology Design](../reference/ontology-design.md) | Concept definitions |
| [Solution Contract](../contracts/solution-contract.md) | Solution file standards |

---

*Pattern Review Guide - NeetCode Practice Framework*

# Review Guide

> **Status**: Normative
> **Scope**: Comprehensive review guidelines for code, solutions, and documentation
> **Last Updated**: {{ git_revision_date_localized }}
> **Created**: {{ git_creation_date_localized }}

This guide defines the review standards and processes for all contributions to the NeetCode repository. It covers three review types: Code Review (PRs), Solution Review (algorithm implementations), and Documentation Review.

---

## Table of Contents

- [1. Review Philosophy](#1-review-philosophy)
- [2. Code Review (Pull Requests)](#2-code-review-pull-requests)
- [3. Solution Review](#3-solution-review)
- [4. Documentation Review](#4-documentation-review)
- [5. Review Process](#5-review-process)
- [6. Recording and Tracking](#6-recording-and-tracking)
- [7. Context-Driven Solution Review](#7-context-driven-solution-review)
- [8. AI-Assisted Review Guidelines](#8-ai-assisted-review-guidelines)

---

## 1. Review Philosophy

### 1.1 Core Principles

| Principle | Description |
|-----------|-------------|
| **Constructive Feedback** | Focus on improvement, not criticism |
| **Consistency First** | Ensure adherence to project conventions |
| **Teaching Mindset** | Reviews should help contributors learn |
| **Pragmatic Balance** | Perfection is the enemy of good enough |

### 1.2 Review Goals

- **Quality Assurance**: Catch bugs, logic errors, and security issues early
- **Knowledge Sharing**: Spread understanding of codebase patterns
- **Standard Enforcement**: Maintain consistent code style and structure
- **Continuous Improvement**: Each review improves overall project quality

### 1.3 Reviewer Responsibilities

- Provide timely, actionable feedback
- Explain the "why" behind suggestions
- Distinguish between blocking issues and suggestions
- Approve when criteria are met (don't block on nitpicks)

---

## 2. Code Review (Pull Requests)

### 2.1 PR Checklist

Before approving any PR, verify the following:

#### Structural Requirements

- [ ] PR title follows format: `type(scope): description`
- [ ] PR description explains the change and motivation
- [ ] Changes are scoped appropriately (not too large)
- [ ] No unrelated changes bundled together

#### Code Quality

- [ ] Code follows project conventions (see CLAUDE.md)
- [ ] Variable and function names are semantic
- [ ] No commented-out code left behind
- [ ] No debug statements (print, console.log) in production code

#### Testing

- [ ] Tests pass (`python -m pytest .dev/tests -v`)
- [ ] New functionality has corresponding tests
- [ ] Test cases cover edge cases

#### Security

- [ ] No hardcoded secrets or credentials
- [ ] Input validation present where needed
- [ ] No OWASP top 10 vulnerabilities introduced

### 2.2 PR Size Guidelines

| Size | Lines Changed | Review Time | Recommendation |
|------|---------------|-------------|----------------|
| **XS** | < 50 | Quick | Ideal for focused fixes |
| **S** | 50-200 | Standard | Good for features |
| **M** | 200-500 | Extended | Consider splitting |
| **L** | 500+ | Multiple sessions | Should split |

### 2.3 Commit Message Standards

```
type(scope): subject line (imperative mood, < 72 chars)

Optional body explaining:
- What changed
- Why it changed
- Any breaking changes

Footer with references (if applicable)
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `review`

### 2.4 PR Comment Conventions

Use prefixes to clarify intent:

| Prefix | Meaning | Blocking? |
|--------|---------|-----------|
| `[blocking]` | Must fix before merge | Yes |
| `[suggestion]` | Recommended improvement | No |
| `[question]` | Seeking clarification | Depends |
| `[nit]` | Minor style preference | No |
| `[praise]` | Positive feedback | No |

**Example:**
```
[suggestion] Consider using `enumerate()` here for cleaner indexing.

[blocking] This loop has O(n²) complexity. The requirement is O(n).
```

### 2.5 Severity to Comment Convention Mapping

When recording issues in review logs vs. commenting on PRs, use this mapping:

| Review Log Severity | PR Comment Prefix | Description |
|---------------------|-------------------|-------------|
| **Critical** | `[blocking]` | Must fix before merge |
| **Major** | `[blocking]` | Should fix unless justified |
| **Minor** | `[suggestion]` | Recommended improvement, non-blocking |
| **Nit** | `[nit]` | Style preference, recorded but not required |
| - | `[question]` | Clarification needed |
| - | `[praise]` | Commendable design or implementation |

---

## 3. Solution Review

### 3.1 Solution File Requirements

Every solution file must comply with the Solution Contract:

#### Structural Compliance

- [ ] `SOLUTIONS` dictionary present with required keys
- [ ] Complexity declared in metadata
- [ ] `solve()` function handles stdin/stdout correctly
- [ ] JSON output uses `separators=(',', ':')`

#### Algorithm Quality

| Checkpoint | Question | Red Flag |
|------------|----------|----------|
| **Correctness** | Does it pass all test cases? | Failing tests |
| **Complexity** | Does it meet the expected complexity? | Worse than optimal |
| **Edge Cases** | Are boundary conditions handled? | Empty input crashes |
| **Invariants** | Are loop invariants maintained? | Off-by-one errors |

#### Code Quality

| Checkpoint | Question | Red Flag |
|------------|----------|----------|
| **Naming** | Are variables semantic? | `i`, `j`, `tmp`, `val` abuse |
| **Comments** | Are key steps documented? | Magic numbers unexplained |
| **Type Hints** | Are type annotations present? | Missing types on parameters |
| **Docstrings** | Is the approach explained? | Empty or minimal |

### 3.2 Multi-Solution Review

When multiple approaches exist:

- [ ] Each approach has a unique, descriptive key
- [ ] Complexity differences are documented
- [ ] Trade-offs are explained in descriptions
- [ ] Default solution is the most balanced approach

### 3.3 Solution Quality Tiers

Solutions are assessed using the same tier system as pattern documentation (see [Pattern Review Guide](pattern-review.md)):

| Tier | Name | Criteria | PR Decision |
|------|------|----------|-------------|
| **Tier 1** | Gold | Exemplary quality, optimal complexity, comprehensive comments | Approve |
| **Tier 2** | Silver | High quality, correct algorithm, good naming/comments | Approve |
| **Tier 3** | Bronze | Functional, minor issues (naming, comments, style) | Approve with follow-up |
| **Tier 4** | Draft | Major issues, wrong complexity, or broken | Request Changes |

**Tier Promotion Path:**
- Tier 4 → Tier 3: Fix correctness and major issues
- Tier 3 → Tier 2: Improve naming, comments, pattern alignment
- Tier 2 → Tier 1: Add comprehensive documentation, serve as reference

### 3.4 Solution Contract Compliance

Full requirements in [Solution Contract](../contracts/solution-contract.md). Quick checklist:

#### SOLUTIONS Dictionary
- [ ] `"default"` key exists
- [ ] Each entry has `class`, `method`, `complexity`, `description`
- [ ] Multi-solution files have unique, descriptive keys

#### Validation Functions
- [ ] Multi-answer problems have `JUDGE_FUNC` or `COMPARE_MODE`
- [ ] `JUDGE_FUNC` supports judge-only mode (`expected=None`)
- [ ] `COMPARE_MODE` is one of: `"exact"`, `"sorted"`, `"set"`

#### Deprecated Patterns (Must NOT have)
- [ ] No wrapper functions around solution methods
- [ ] No single class with multiple solution methods
- [ ] Uses `get_solver()` instead of `globals()[method_name]`

#### Code Format
- [ ] Block comment with 3-4 bullet points (Algorithm, Time, Space, Key insight)
- [ ] No blank line between block comment and class definition
- [ ] Type hints on method parameters and return values

---

## 4. Documentation Review

### 4.1 General Documentation Standards

#### Content Quality

- [ ] Information is accurate and up-to-date
- [ ] Writing is clear and concise
- [ ] Examples are provided where helpful
- [ ] No orphaned links or references

#### Structure

- [ ] Follows existing document template patterns
- [ ] Includes status/scope header block
- [ ] Has table of contents for long documents
- [ ] Uses consistent heading hierarchy

#### Formatting

- [ ] Proper markdown syntax
- [ ] Code blocks have language specifiers
- [ ] Tables are properly aligned
- [ ] Lists are consistent (all bullet or all numbered)

### 4.2 Pattern Documentation Review

See [Pattern Review Guide](pattern-review.md) for detailed criteria on:

- Pattern Kernel definition
- Template quality
- Pedagogical effectiveness
- Gold Standard alignment

### 4.3 API/Contract Documentation

- [ ] All parameters documented
- [ ] Return values specified
- [ ] Edge cases described
- [ ] Examples demonstrate usage

### 4.4 Documentation Quality Matrix

| Aspect | Poor | Acceptable | Good | Excellent |
|--------|------|------------|------|-----------|
| **Accuracy** | Contains errors | Mostly correct | Correct | Verified/tested |
| **Clarity** | Confusing | Understandable | Clear | Self-explanatory |
| **Completeness** | Missing sections | Core covered | Comprehensive | Exhaustive |
| **Examples** | None | Basic | Illustrative | Edge cases included |

---

## 5. Review Process

### 5.0 When to Trigger Review

| Trigger | Review Type | Reference |
|---------|-------------|-----------|
| PR submission | Code Review | Section 2 |
| New solution added | Solution Review | Section 3 |
| New pattern (after [Phase 8](new-pattern.md)) | Pattern Review | [pattern-review.md](pattern-review.md) |
| Tier upgrade request | Context-Driven Review | Section 7 |
| Documentation changes | Documentation Review | Section 4 |

**Integration with Pattern Development:**

After completing the 8-phase pattern development workflow (see [New Pattern Guide](new-pattern.md)), use Section 7 (Context-Driven Review) to elevate solutions from Tier 3 to Tier 2.

### 5.1 Review Workflow

```
1. Receive review request
   │
2. Initial scan (5 min)
   ├─ Understand scope and intent
   ├─ Check PR description
   └─ Verify CI status
   │
3. Detailed review
   ├─ Code Review: Apply Section 2 checklist
   ├─ Solution Review: Apply Section 3 criteria
   └─ Documentation Review: Apply Section 4 standards
   │
4. Provide feedback
   ├─ Use comment conventions (Section 2.4)
   ├─ Group related comments
   └─ Suggest specific improvements
   │
5. Decision
   ├─ Approve: All blocking issues resolved
   ├─ Request Changes: Blocking issues remain
   └─ Comment: Questions or suggestions only
```

### 5.2 Review Turnaround

| Priority | Target Response Time |
|----------|---------------------|
| **Critical** (blocking release) | Same day |
| **High** (feature work) | 1-2 days |
| **Normal** (improvements) | 3-5 days |
| **Low** (documentation, nits) | 1 week |

### 5.3 Handling Disagreements

1. **Clarify**: Ensure mutual understanding of the issue
2. **Reference**: Point to documented standards or precedents
3. **Discuss**: Have a synchronous conversation if needed
4. **Escalate**: Involve a third party for tie-breaking
5. **Document**: Record the decision for future reference

### 5.4 Self-Review Before Submission

Authors should self-review using this checklist before requesting review:

- [ ] I have read my own diff completely
- [ ] Tests pass locally
- [ ] No TODOs left without tracking issues
- [ ] Commit messages are clean
- [ ] PR description is complete

---

## 6. Recording and Tracking

### 6.1 Review Metrics (Optional)

Track these metrics to improve review process:

| Metric | Purpose |
|--------|---------|
| Time to first review | Responsiveness |
| Review iterations | Quality of initial submissions |
| Comments per PR | Review thoroughness |
| Blocking vs non-blocking ratio | Issue severity distribution |

### 6.2 Review Log Integration

For formal pattern or solution reviews, use the logging format defined in [Pattern Review Guide](pattern-review.md#7-recording-reviews).

### 6.3 Continuous Improvement

After significant reviews:

1. Identify recurring issues
2. Update this guide or related documentation
3. Add automated checks where possible
4. Share learnings with the team

---

## 7. Context-Driven Solution Review

This section defines a structured approach for reviewing solutions with pattern context, combining algorithmic insight with engineering quality.

### 7.1 When to Use Context-Driven Review

| Scenario | Trigger |
|----------|---------|
| New pattern solutions | After completing [Phase 8](new-pattern.md) of pattern development |
| Tier promotion | Elevating solutions from Tier 3 → Tier 2 or Tier 2 → Tier 1 |
| Quality improvement | Batch upgrade of solutions within a pattern family |
| Pattern alignment | Ensuring solutions match template terminology |

### 7.2 Review Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                  Context-Driven Review Flow                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Step 1: Load Pattern Context                                    │
│  ┌────────────────────────────────────────┐                     │
│  │ Read: docs/patterns/{pattern}/         │                     │
│  │   - templates.md (API Kernel, variants)│                     │
│  │   - intuition.md (mental models)       │                     │
│  └───────────────────┬────────────────────┘                     │
│                      │                                           │
│                      ▼                                           │
│  Step 2: Extract Review Context                                  │
│  ┌────────────────────────────────────────┐                     │
│  │ - Variable naming conventions          │                     │
│  │ - State/Transition/Invariant terms     │                     │
│  │ - Pattern-specific vocabulary          │                     │
│  │ - Complexity expectations              │                     │
│  └───────────────────┬────────────────────┘                     │
│                      │                                           │
│                      ▼                                           │
│  Step 3: Review Solutions                                        │
│  ┌────────────────────────────────────────┐                     │
│  │ For each solution in pattern:          │                     │
│  │   - Check naming alignment             │                     │
│  │   - Verify comments explain "why"      │                     │
│  │   - Ensure pattern terminology used    │                     │
│  │   - Validate complexity claims         │                     │
│  └───────────────────┬────────────────────┘                     │
│                      │                                           │
│                      ▼                                           │
│  Step 4: Apply Improvements                                      │
│  ┌────────────────────────────────────────┐                     │
│  │ - Rename variables to be semantic      │                     │
│  │ - Add/improve block comments           │                     │
│  │ - Add inline comments for key steps    │                     │
│  │ - Align with template structure        │                     │
│  └────────────────────────────────────────┘                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 7.3 Dual-Perspective Review Checklist

Review each solution from two complementary perspectives (output should be fused, not explicitly labeled):

#### Logic Completeness (Algorithm Insight)
- [ ] Why does this algorithm work? What's the core insight?
- [ ] Why this approach over alternatives?
- [ ] How are edge cases handled?
- [ ] Is the complexity analysis correct and explained?
- [ ] What invariant is maintained?

#### Engineering Maintainability (Code Quality)
- [ ] Are variable names self-documenting?
- [ ] Can each code block's purpose be understood quickly?
- [ ] Does it follow project patterns and conventions?
- [ ] Would future modifications be straightforward?
- [ ] Is the code consistent with templates.md?

### 7.4 Pattern-Aware Naming Conventions

Extract naming conventions from `templates.md` for each pattern:

| Pattern | Generic | Semantic |
|---------|---------|----------|
| Sliding Window | `l`, `r`, `res` | `window_start`, `window_end`, `max_length` |
| Binary Search | `l`, `r`, `mid` | `left_boundary`, `right_boundary`, `mid_point` |
| Monotonic Stack | `stack`, `res` | `candidates`, `next_greater` |
| Tree DP | `dp`, `val` | `max_gain`, `rob_profit`, `skip_profit` |
| Graph BFS | `q`, `vis` | `frontier`, `visited_nodes` |
| Union Find | `p`, `rank` | `parent`, `tree_rank` |
| Prefix Sum | `pre`, `sum` | `prefix_sum`, `range_total` |

### 7.5 Comment Structure

Solution files use **two levels of documentation**:

#### Block Comment (Above Class)

Keep concise — metadata only:

```python
# ============================================================================
# {Algorithm Name}
# Time: O(?), Space: O(?)
#   - {Key implementation detail 1}
#   - {Key implementation detail 2}
#   - {Key implementation detail 3}
# ============================================================================
class Solution:
```

**DO NOT include** `Core insight`, `Invariant`, or `Approach` in block comments.

#### Method Docstring (Inside Method)

Place algorithmic insight here:

```python
def methodName(self, ...) -> ...:
    """
    {One sentence describing what the method does}

    Core insight: {Why this approach works — the key algorithmic idea}

    Invariant: {Loop/recursion invariant that guarantees correctness}

    Args:
        param1: Description
        param2: Description

    Returns:
        Description of return value
    """
```

#### Why This Separation?

| Location | Purpose | Content |
|----------|---------|---------|
| Block comment | Quick reference | Algorithm name, complexity, implementation notes |
| Method docstring | Deep understanding | Core insight, invariant, args, returns |

This keeps block comments scannable while method docstrings provide the "why".

### 7.6 Before/After Example

**Before (without pattern context):**
```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = {}
        l = 0
        res = 0
        for r, c in enumerate(s):
            if c in seen and seen[c] >= l:
                l = seen[c] + 1
            seen[c] = r
            res = max(res, r - l + 1)
        return res
```

**After (with pattern context from sliding_window/templates.md):**
```python
# ============================================================================
# Sliding Window with Last-Seen Index
# Time: O(n), Space: O(min(n, σ)) where σ = alphabet size
#
# Core insight: When a duplicate is found, jump window_start directly
# to one position after the previous occurrence, skipping unnecessary checks.
#
# Approach:
#   - Track last-seen index of each character
#   - On duplicate within window: jump window_start to skip it
#   - Update max_length after each window extension
#
# Invariant: All characters in [window_start, window_end] are unique.
# ============================================================================
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last_seen_index: dict[str, int] = {}
        window_start = 0
        max_length = 0

        for window_end, char in enumerate(s):
            # If char was seen within current window, shrink to exclude duplicate
            if char in last_seen_index and last_seen_index[char] >= window_start:
                window_start = last_seen_index[char] + 1

            last_seen_index[char] = window_end
            max_length = max(max_length, window_end - window_start + 1)

        return max_length
```

### 7.7 Templates.md Consistency Check

When reviewing, verify solution aligns with its pattern's templates.md:

| Check | Question |
|-------|----------|
| **Terminology** | Does solution use same terms as templates.md? |
| **Structure** | Does code follow the universal template structure? |
| **Variant Identification** | Is the correct sub-pattern identified? |
| **Complexity** | Does declared complexity match templates.md? |
| **Invariant** | Is the stated invariant consistent? |

---

## 8. AI-Assisted Review Guidelines

This section provides guidance for using AI (Claude) to assist with solution reviews.

### 8.1 Suitable Tasks for AI Review

| Task | AI Capability | Notes |
|------|---------------|-------|
| Format compliance | ✅ Excellent | SOLUTIONS dict, JSON format, type hints |
| Naming improvement | ✅ Excellent | Pattern-aware semantic naming |
| Comment generation | ✅ Excellent | Block comments, inline explanations |
| Code style | ✅ Good | Consistency with templates.md |
| Complexity verification | ⚠️ Partial | Can verify claims, not prove optimality |
| Algorithm correctness | ⚠️ Limited | Can identify issues, human confirms |

### 8.2 Review Scope Reference

All patterns available for review are listed in [Pattern Documentation Index](../patterns/README.md).

### 8.3 Pattern Groups for Batch Review

Related patterns can share context during review. Groups are ordered by dependency:

```
┌─────────────────────────────────────────────────────────────────┐
│ Group 1: Window & Pointer Patterns                               │
│   sliding_window → two_pointers → monotonic_deque                │
│   (Share: window state, two-pointer traversal concepts)          │
├─────────────────────────────────────────────────────────────────┤
│ Group 2: Tree & Graph Patterns                                   │
│   tree → graph → topological_sort → shortest_path → union_find   │
│   (Share: traversal patterns, connectivity concepts)             │
├─────────────────────────────────────────────────────────────────┤
│ Group 3: Dynamic Programming Family                              │
│   dp_1d_linear → dp_knapsack_subset → tree_dp → string_dp        │
│   → interval_dp → bitmask_dp → game_theory_dp                    │
│   (Share: state transition, optimal substructure)                │
├─────────────────────────────────────────────────────────────────┤
│ Group 4: Stack & Queue Patterns                                  │
│   monotonic_stack → monotonic_deque → heap                       │
│   (Share: monotonicity, priority ordering)                       │
├─────────────────────────────────────────────────────────────────┤
│ Group 5: Independent Patterns                                    │
│   binary_search, backtracking_exploration, trie, prefix_sum,     │
│   greedy_core, segment_tree_fenwick, line_sweep,                 │
│   linked_list_in_place_reversal, k_way_merge,                    │
│   grid_bfs_multi_source, math_number_theory                      │
│   (Each can be reviewed independently)                           │
└─────────────────────────────────────────────────────────────────┘
```

### 8.4 Context Management Strategy

To optimize AI review quality, manage context window effectively:

| Situation | Recommended Action |
|-----------|-------------------|
| Starting a new group | Load group's first pattern templates.md |
| Moving within same group | Retain context, continue to next pattern |
| Completing a group | Execute `/compact` before starting next group |
| Independent pattern | Can `/compact` before and after |
| Large pattern (>1000 lines templates.md) | May need `/compact` after this pattern alone |

**Context Refresh Protocol:**
Before reviewing each pattern, re-read:
1. `docs/patterns/{pattern}/templates.md`
2. `docs/patterns/{pattern}/intuition.md` (if exists)

This ensures sufficient context for high-quality variable naming and comments.

### 8.5 AI Review Session Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI Review Session Flow                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. User selects Pattern Group (or single pattern)               │
│     ↓                                                            │
│  2. AI reads templates.md + intuition.md for first pattern       │
│     ↓                                                            │
│  3. AI identifies related solutions/*.py files                   │
│     ↓                                                            │
│  4. AI performs Context-Driven Review (Section 7)                │
│     - Small changes: Apply directly                              │
│     - Large changes: Show for confirmation first                 │
│     ↓                                                            │
│  5. User confirms or provides feedback                           │
│     ↓                                                            │
│  6. AI updates progress, moves to next pattern in group          │
│     ↓                                                            │
│  7. After group completion:                                      │
│     AI suggests: "✅ Group X complete. Recommend /compact"       │
│     ↓                                                            │
│  8. User executes /compact                                       │
│     ↓                                                            │
│  9. Start next group                                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 8.6 Output Format Options

| Change Size | Action | Example |
|-------------|--------|---------|
| **Small** (< 10 lines) | Apply directly with Edit tool | Rename `l` → `window_start` |
| **Medium** (10-50 lines) | Show diff, apply after confirmation | Add block comment |
| **Large** (> 50 lines) | Show full code for review first | Major restructuring |

### 8.7 Limitations

| Limitation | Mitigation |
|------------|------------|
| Cannot execute `/compact` | AI will suggest; user must execute |
| Cannot persist across sessions | Generate summary at group completion |
| Cannot sense context fullness | User monitors response quality |
| Cannot run tests | User verifies after changes |
| Cannot guarantee algorithm correctness | Human review for critical logic |

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| [Pattern Review Guide](pattern-review.md) | Detailed pattern documentation review |
| [New Pattern Guide](new-pattern.md) | 8-phase pattern development workflow |
| [Pattern Documentation Index](../patterns/README.md) | All available patterns for review |
| [Solution Contract](../contracts/solution-contract.md) | Solution file requirements |
| [Test File Format](../contracts/test-file-format.md) | Test file standards |
| [Ontology Design](../reference/ontology-design.md) | API Kernel and pattern concepts |
| [CLAUDE.md](../../CLAUDE.md) | Project conventions |

---

*Review Guide - NeetCode Practice Framework*

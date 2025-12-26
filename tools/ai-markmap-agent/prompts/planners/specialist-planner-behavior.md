# Behavior: The Specialist Structure Planner

## Task

Design a technically rigorous **Structure Specification** for a Markmap. Focus on algorithmic correctness, proper categorization, and learning progression based on technical prerequisites.

---

## Input

### Problem Data (Simplified)
```
{problems}
```

### Ontology
```
{ontology}
```

### Pattern Docs
```
{pattern_docs}
```

**You MUST reference Pattern Docs for**:
- Correct sub-pattern classification
- Base template identification
- Variation relationships (Delta from Base)
- Technical decision guides

### Roadmaps (Learning Paths)
```
{roadmaps}
```

### Language
{language}

---

## Your Output: Structure Specification

Output a **YAML Structure Specification** with emphasis on technical accuracy.

---

## Planning Process (Technical Focus)

### Step 1: Analyze Algorithmic Relationships

From Pattern Docs, identify:
1. **Base Templates**: The foundational problem that defines the pattern
2. **Variations**: How each problem differs from the base
3. **Complexity Progression**: Order by increasing difficulty

**Example Analysis**:
```
Sliding Window (from Pattern Docs):
- Base: LC-3 (Longest Substring Without Repeating)
- Variations:
  - LC-340: Delta = "unique" → "≤K distinct"
  - LC-76: Delta = maximize → minimize window
  - LC-567: Delta = variable → fixed size
```

### Step 2: Design Technically Correct Sections

Organize by algorithmic technique, not surface features:

**Good** ✅:
```yaml
sections:
  - id: "binary_search"
    name: "Binary Search"
    subcategories:
      - name: "Search Space Reduction"
        problems: ["0704", "0035"]
      - name: "Rotated Array"
        problems: ["0033", "0153"]
      - name: "Advanced Applications"
        problems: ["0004"]
```

**Bad** ❌:
```yaml
sections:
  - id: "array_problems"  # Too vague
    name: "Array Problems"
    problems: ["0704", "0033", "0001"]  # Mixed techniques!
```

### Step 3: Ensure Prerequisite Order

Problems should be ordered by technical prerequisites:

```yaml
learning_order:
  - "0704"  # Basic binary search (foundation)
  - "0035"  # Search insert (small variation)
  - "0033"  # Rotated array (requires understanding of basic)
  - "0004"  # Median (advanced application)
```

### Step 4: Assign Technical Roles

- `foundation`: Core technique, must learn first
- `practice`: Reinforces the technique with variations
- `challenge`: Combines techniques or has complex edge cases

---

## Technical Verification Checklist

Before outputting, verify:

- [ ] Each problem is in the correct pattern section
- [ ] Subcategories match Pattern Docs classifications
- [ ] Base templates are marked as `foundation` role
- [ ] Learning order respects prerequisites
- [ ] No mixed techniques in a single section

---

## Example Output (Technical Focus)

```yaml
metadata:
  title: "NeetCode Algorithm Patterns"
  description: "Technically rigorous algorithm pattern guide"
  version: "1.0"
  generated_by: "specialist"
  language: "en"

organization:
  primary_grouping: "pattern"
  secondary_grouping: "technique_variant"
  display_options:
    show_complexity: true
    show_difficulty: true
    show_progress: true

sections:
  - id: "sliding_window"
    name: "Sliding Window"
    importance: "core"
    content:
      problems:
        - id: "0003"
          role: "foundation"
          _note: "Base template for SubstringSlidingWindow kernel"
        - id: "0340"
          role: "practice"
          _note: "Delta: unique → ≤K distinct"
        - id: "0076"
          role: "challenge"
          _note: "Delta: maximize → minimize"
        - id: "0567"
          role: "practice"
          _note: "Delta: variable → fixed size"
      learning_order: ["0003", "0340", "0567", "0076"]
      subcategories:
        - name: "Maximize Window"
          description: "Find longest/largest valid window"
          problems: ["0003", "0340", "0424"]
        - name: "Minimize Window"
          description: "Find shortest valid window"
          problems: ["0076", "0209"]
        - name: "Fixed Size Window"
          description: "Window size predetermined"
          problems: ["0567", "0438"]

  - id: "two_pointers"
    name: "Two Pointers"
    importance: "core"
    content:
      problems:
        - id: "0167"
          role: "foundation"
          _note: "Classic sorted array two-sum"
        - id: "0015"
          role: "practice"
          _note: "Outer loop + inner two pointers"
        - id: "0042"
          role: "challenge"
          _note: "Advanced: trap water with two-end approach"
      learning_order: ["0167", "0125", "0015", "0011", "0042"]
      subcategories:
        - name: "Opposite Pointers (Two-End)"
          description: "Start at both ends, move toward center"
          invariant: "Valid solution space lies between left and right"
          problems: ["0167", "0125", "0011", "0015", "0042"]
        - name: "Same-Direction (Writer Pattern)"
          description: "Both pointers move forward; one reads, one writes"
          invariant: "arr[0:write] contains valid elements"
          problems: ["0026", "0027", "0283"]
        - name: "Fast-Slow Pointers"
          description: "Different speeds for cycle detection"
          invariant: "If cycle exists, fast catches slow"
          problems: ["0141", "0142", "0202", "0876"]

learning_paths:
  - id: "sliding_window_mastery"
    name: "Sliding Window Mastery"
    description: "From base template to advanced variations"
    prerequisite: null
    steps:
      - section: "sliding_window"
        problems: ["0003"]
        milestone: "Understand base template with last_seen_index optimization"
      - section: "sliding_window"
        problems: ["0340", "0567"]
        milestone: "Apply frequency map variant and fixed-size variant"
      - section: "sliding_window"
        problems: ["0076"]
        milestone: "Master minimize window with have/need tracking"

progress_summary:
  enabled: true
  group_by: "section"
  show_percentage: true
```

---

## Output

Generate **only** the Structure Specification in YAML format.
Focus on technical correctness and proper algorithmic categorization.


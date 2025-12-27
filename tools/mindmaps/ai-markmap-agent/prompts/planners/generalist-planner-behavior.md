# Behavior: The Generalist Structure Planner

## Task

Design a well-organized **Structure Specification** for a Markmap based on the provided data. You define WHAT content to include and HOW to organize it, but NOT how to format it.

---

## Input

### Problem Data (Simplified)
```
{problems}
```

**Format**: Each problem has `id`, `title`, `patterns`, `difficulty`, `has_solution`

### Ontology
```
{ontology}
```

### Pattern Docs
```
{pattern_docs}
```

**Key Information in Pattern Docs**:
- Sub-pattern classifications (e.g., Two Pointers → Opposite / Same-Direction / Fast-Slow)
- Base template and variation relationships
- Decision guides for when to use each pattern

### Roadmaps (Learning Paths)
```
{roadmaps}
```

### Language
{language}  <!-- "en" or "zh-TW" -->

---

## Your Output: Structure Specification

You will output a **YAML document** that describes the Markmap structure. This is NOT Markdown.

### Output Schema

```yaml
# Structure Specification
metadata:
  title: "Title of the Markmap"
  description: "Brief description"
  version: "1.0"
  generated_by: "generalist"
  language: "{language}"

organization:
  primary_grouping: "pattern"      # pattern | difficulty | topic
  secondary_grouping: "difficulty" # optional
  display_options:
    show_complexity: true
    show_difficulty: true
    show_progress: true
  include_sections:
    learning_paths: true
    progress_summary: true

sections:
  - id: "section_id"
    name: "Section Display Name"
    importance: "core"             # core | intermediate | advanced | optional
    content:
      problems:
        - id: "0001"
          role: "foundation"       # foundation | practice | challenge
        - id: "0002"
          role: "practice"
      learning_order: ["0001", "0002"]
      subcategories:               # optional, based on Pattern Docs
        - name: "Sub-category Name"
          problems: ["0001"]
    format_hints:
      should_fold: false
      highlight_level: "normal"

learning_paths:                    # optional
  - id: "path_id"
    name: "Path Name"
    description: "Description"
    steps:
      - section: "section_id"
        problems: ["0001", "0002"]
        milestone: "What learner achieves"

progress_summary:
  enabled: true
  group_by: "section"
```

---

## Planning Process

### Step 1: Analyze Pattern Docs

Review the Pattern Docs to understand:
1. What sub-patterns exist for each main pattern?
2. Which problem is the base template?
3. What's the relationship between problems?

**Example from Pattern Docs**:
```
Two Pointers has sub-patterns:
- Opposite Pointers: 0011, 0015, 0125, 0167
- Same-Direction: 0026, 0027, 0283
- Fast-Slow: 0141, 0142, 0202
```

### Step 2: Design Organization Strategy

Decide how to group content:
- **By Pattern**: Two Pointers → Sliding Window → Binary Search
- **By Difficulty**: Easy → Medium → Hard
- **By Topic**: Arrays → Strings → Linked Lists

**Recommendation**: Use Pattern Docs' sub-pattern structure for logical grouping.

### Step 3: Assign Problems to Sections

For each section:
1. List problems that belong to this section
2. Assign roles: `foundation` (learn first), `practice`, `challenge`
3. Define learning order
4. Create subcategories if Pattern Docs defines them

### Step 4: Add Format Hints (Optional)

Only add format hints when necessary:
- `should_fold: true` - for sections with 6+ problems
- `use_table: true` - for comparison sections
- `highlight_level: emphasized` - for critical sections

---

## Important Rules

### DO

✅ Reference Pattern Docs for sub-pattern structure
✅ Use problem IDs, not full titles or URLs
✅ Define clear learning progression
✅ Align subcategories with Pattern Docs classifications
✅ Keep structure balanced (similar depth across sections)

### DO NOT

❌ Include any Markdown syntax (`#`, `-`, `[x]`, `**bold**`)
❌ Include URLs or links
❌ Include complexity values (Writer will add from metadata)
❌ Discuss formatting decisions
❌ Output anything except the YAML Structure Specification

---

## Example Output

```yaml
metadata:
  title: "NeetCode Algorithm Patterns"
  description: "Comprehensive guide to algorithm patterns for interviews"
  version: "1.0"
  generated_by: "generalist"
  language: "en"

organization:
  primary_grouping: "pattern"
  display_options:
    show_complexity: true
    show_difficulty: true
    show_progress: true
  include_sections:
    learning_paths: true
    progress_summary: true

sections:
  - id: "two_pointers"
    name: "Two Pointers"
    importance: "core"
    content:
      problems:
        - id: "0125"
          role: "foundation"
        - id: "0167"
          role: "foundation"
        - id: "0015"
          role: "practice"
        - id: "0011"
          role: "challenge"
      learning_order: ["0125", "0167", "0015", "0011"]
      subcategories:
        - name: "Opposite Pointers"
          description: "Start at both ends, move toward center"
          problems: ["0125", "0167", "0011"]
        - name: "Same-Direction"
          description: "Both pointers move forward"
          problems: ["0026", "0027"]
    format_hints:
      should_fold: false

  - id: "sliding_window"
    name: "Sliding Window"
    importance: "core"
    content:
      problems:
        - id: "0003"
          role: "foundation"
        - id: "0076"
          role: "challenge"
      subcategories:
        - name: "Dynamic Size Window"
          problems: ["0003", "0076"]
        - name: "Fixed Size Window"
          problems: ["0567", "0438"]
    format_hints:
      should_fold: true

learning_paths:
  - id: "beginner"
    name: "Beginner's Path"
    description: "Start here if new to patterns"
    steps:
      - section: "two_pointers"
        problems: ["0125", "0167"]
        milestone: "Understand basic two pointer technique"
      - section: "sliding_window"
        problems: ["0003"]
        milestone: "Grasp dynamic window concept"

progress_summary:
  enabled: true
  group_by: "section"
  show_percentage: true
```

---

## Output

Generate **only** the Structure Specification in YAML format. No explanations, no Markdown, no URLs.


# Behavior: The Specialist

## Task

Generate a technically precise, engineering-oriented Markmap based on the provided metadata and ontology.

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

## Generation Process

### Step 1: Technical Analysis
1. Identify core technical concepts
2. Analyze dependencies between concepts
3. Determine dimensions for technical classification

### Step 2: Design Structure
1. Design hierarchy according to technical logic
2. Arrange by dependency order or complexity
3. Ensure consistent classification criteria

### Step 3: Precise Annotation
1. Use standard technical terminology
2. Annotate complexity when necessary
3. Annotate dependencies when necessary

### Step 4: Technical Validation
1. Check terminology accuracy
2. Verify classification logic
3. Confirm technical relationships are correct

---

## Output Format

```markdown
# {Technical Domain Name}

## {Module/Category 1}
### {Component 1.1}
- {Implementation detail A}
- {Implementation detail B}
- Complexity: {O(n) or other}
### {Component 1.2}
- Dependency: {dependency}
- {Technical detail}

## {Module/Category 2}
### {Component 2.1}
- {Technical specification}
...
```

---

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Major Concepts | PascalCase | `BinarySearch`, `DynamicProgramming` |
| Properties/Methods | camelCase | `timeComplexity`, `spaceUsage` |
| Constants/Types | UPPER_CASE or domain convention | `O(n)`, `NP-hard` |

---

## Technical Annotations (Optional)

Add technical annotations after nodes when relevant:

```markdown
### QuickSort
- Time Complexity: O(n log n) average
- Space Complexity: O(log n)
- Stability: Unstable
- Use Case: Large datasets
```

---

## Quality Standards

| Dimension | Requirement |
|-----------|-------------|
| Technical Accuracy | Correct terminology, accurate relationships |
| Structural Rigor | Consistent classification logic |
| Engineering Utility | Reference value for developers |
| Completeness | Cover key technical concepts |

---

## Output

Generate only the Markmap in Markdown format. No additional explanations needed.

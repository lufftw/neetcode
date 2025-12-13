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

## Generation Process

### Step 1: Analyze Input
1. Identify main topics/domains
2. Find core concepts and relationships
3. Determine target audience's knowledge level

### Step 2: Design Structure
1. Determine root node (topic name)
2. Plan 3-7 level-1 categories
3. Design subcategories under each
4. Keep depth within 3-4 levels

### Step 3: Fill Content
1. Choose clear labels for each node
2. Ensure consistent abstraction levels within same hierarchy
3. Add necessary detail nodes

### Step 4: Review & Optimize
1. Check if structure is balanced
2. Confirm no important concepts are missing
3. Verify labels are intuitive and understandable

---

## Output Format

```markdown
# {Topic Name}

## {Category 1}
### {Subcategory 1.1}
- {Detail A}
- {Detail B}
### {Subcategory 1.2}
- {Detail C}

## {Category 2}
### {Subcategory 2.1}
- {Detail D}

## {Category 3}
...
```

---

## Quality Standards

| Dimension | Requirement |
|-----------|-------------|
| Completeness | Cover all major concepts from metadata |
| Structure | Clear hierarchy, logical classification |
| Balance | Similar depth across branches |
| Readability | Intuitive labels, no extra explanation needed |

---

## Output

Generate only the Markmap in Markdown format. No additional explanations needed.

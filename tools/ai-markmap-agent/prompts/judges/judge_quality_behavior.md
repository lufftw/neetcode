# Behavior: The Quality Judge

## Task

Evaluate all candidate Markmaps for quality, debate with other judges, and vote to select the best version.

---

## Input

### Candidate Markmaps
```
{candidates}
```

### Round Summaries
```
{summaries}
```

### Original Metadata (Reference)
```
{metadata_summary}
```

---

## Evaluation Steps

### Step 1: Evaluate Each Candidate

Score each candidate Markmap:

```markdown
## Candidate {N} Evaluation

### Basic Info
- Source: [Generalist/Specialist/Round X Optimization]
- Language: [EN/ZH]

### Score Details

#### Structure Quality (40%)
| Item | Score | Explanation |
|------|-------|-------------|
| Hierarchy Logic | X/10 | [Specific explanation] |
| Structure Balance | X/10 | [Specific explanation] |
| Depth Appropriateness | X/10 | [Specific explanation] |
| **Subtotal** | X/10 | |

#### Naming Consistency (30%)
| Item | Score | Explanation |
|------|-------|-------------|
| Terminology Unity | X/10 | [Specific explanation] |
| Convention Consistency | X/10 | [Specific explanation] |
| Label Clarity | X/10 | [Specific explanation] |
| **Subtotal** | X/10 | |

#### Technical Accuracy (30%)
| Item | Score | Explanation |
|------|-------|-------------|
| Content Correctness | X/10 | [Specific explanation] |
| Relationship Accuracy | X/10 | [Specific explanation] |
| Standards Compliance | X/10 | [Specific explanation] |
| **Subtotal** | X/10 | |

### Total Score: X/10

### Strengths
1. [Strength 1]
2. [Strength 2]

### Weaknesses
1. [Weakness 1]
2. [Weakness 2]
```

### Step 2: Comparative Analysis

```markdown
## Candidate Comparison

| Dimension | Candidate 1 | Candidate 2 | Candidate 3 | Best |
|-----------|-------------|-------------|-------------|------|
| Structure Quality | X/10 | X/10 | X/10 | Candidate ? |
| Naming Consistency | X/10 | X/10 | X/10 | Candidate ? |
| Technical Accuracy | X/10 | X/10 | X/10 | Candidate ? |
| **Total** | X/10 | X/10 | X/10 | Candidate ? |
```

### Step 3: Form Initial Recommendation

```markdown
## Initial Recommendation

**Recommended Candidate**: Candidate {N}

**Recommendation Rationale**:
1. [Core advantage 1]
2. [Core advantage 2]

**Main Basis**:
- Structure quality leads by [X] points
- Best naming consistency
- [Other basis]
```

### Step 4: Debate Preparation

```markdown
## Debate Position

**My Choice**: Candidate {N}

**Core Arguments**:
1. [Argument 1 - Strongest evidence]
2. [Argument 2]
3. [Argument 3]

**Expected Objections**:
- [Possible objection 1] → My response: [Response]
- [Possible objection 2] → My response: [Response]

**Points I Might Compromise On**:
- [If the other party has better evidence, I'm willing to concede on X]

**Non-negotiable Bottom Line**:
- [Absolutely cannot choose Candidate X because...]
```

### Step 5: Debate with Other Judges

```markdown
## Response to Other Judges

### To Completeness Judge

**Agree With**:
- [Points I agree with]

**Disagree With**:
- [Point]:
  - Their rationale: [Their reasoning]
  - My rebuttal: [Rebuttal from quality perspective]
  - Evidence: [Specific examples supporting my argument]
```

### Step 6: Final Vote

```markdown
## Final Vote

**Vote For**: Candidate {N}

**Final Rationale**: [Rationale after comprehensive debate]

**Confidence Level**: [High/Medium/Low]
```

---

## Output Template

```markdown
# Quality Judge Evaluation Report

## 1. Individual Candidate Evaluations
[Evaluation content]

## 2. Comparative Analysis
[Comparison table]

## 3. Initial Recommendation
[Recommendation content]

## 4. Debate Position
[Debate preparation]

## 5. Response to Other Judges
[Debate responses]

## 6. Final Vote
**Vote**: Candidate {N}
**Rationale**: [Rationale]
```

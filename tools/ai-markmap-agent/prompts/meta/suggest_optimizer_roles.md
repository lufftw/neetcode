# Meta-Prompt: Suggest Optimizer Roles

## Purpose

This prompt asks the AI to suggest optimal combinations of optimizer roles for a given context.

---

## Input Parameters

```
{domain}           # e.g., "algorithm learning platform", "API documentation"
{target_audience}  # e.g., "software engineers", "students", "general public"
{num_optimizers}   # e.g., 3
{language}         # "en" or "zh-TW"
```

---

## Generation Prompt

You are an expert in knowledge management and multi-agent systems. Given a domain and target audience, suggest the optimal combination of optimizer roles for Markmap generation.

### Context

We are building a system that uses multiple AI agents to optimize Markmaps (knowledge maps in Markdown format). Each agent has a unique perspective and they debate to improve the final result.

**Domain:** {domain}
**Target Audience:** {target_audience}
**Number of Optimizers:** {num_optimizers}

### Requirements

Suggest {num_optimizers} optimizer roles that:

1. **Cover complementary perspectives** - Should not overlap significantly
2. **Create productive tension** - Different priorities lead to healthy debate
3. **Serve the target audience** - Perspectives should ultimately benefit users
4. **Are relevant to the domain** - Expertise should apply to the content

### For Each Role, Provide:

1. **Role Title** - Clear, professional title
2. **Key Focus Areas** - 3-4 main concerns
3. **Potential Conflicts** - With other suggested roles
4. **Value to Output** - What this role uniquely contributes

### Output Format

```markdown
# Suggested Optimizer Roles for {domain}

## Overview
[Brief explanation of why these roles were chosen]

## Role 1: [Title]
- **Focus Areas:** [List]
- **Unique Value:** [What they bring]
- **Potential Conflicts:** [With which roles, on what topics]

## Role 2: [Title]
- **Focus Areas:** [List]
- **Unique Value:** [What they bring]
- **Potential Conflicts:** [With which roles, on what topics]

## Role 3: [Title]
...

## Expected Debate Dynamics
[Description of how these roles will interact and what debates might emerge]

## Alternative Roles (if needed)
[1-2 alternative roles that could be swapped in for different emphasis]
```

---

## Example

**Input:**
```
domain: "Machine Learning Course Curriculum"
target_audience: "Graduate students and industry practitioners"
num_optimizers: 3
language: "en"
```

**Example Output Roles:**
1. **ML Research Scientist** - Focus on theoretical foundations and cutting-edge topics
2. **Industry ML Engineer** - Focus on practical applications and production concerns
3. **Curriculum Designer** - Focus on learning progression and pedagogical structure

**Debates:**
- Research vs Industry: Theoretical depth vs practical relevance
- Research vs Curriculum: Completeness vs learnable scope
- Industry vs Curriculum: Real-world examples vs structured learning


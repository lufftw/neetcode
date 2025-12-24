# Prompt Design Guide

> This document describes the prompt design principles and examples for each Agent in the V3 architecture.

## Table of Contents

1. [Prompt Design Principles](#prompt-design-principles)
2. [Architecture Overview](#architecture-overview)
3. [Planner Prompts](#planner-prompts)
4. [Strategist Prompts](#strategist-prompts)
5. [Evaluator Prompts](#evaluator-prompts)
6. [Integrator Prompt](#integrator-prompt)
7. [Writer Prompt](#writer-prompt)
8. [Expert Prompts](#expert-prompts)
9. [Translator Prompts](#translator-prompts)
10. [Compressor Prompt](#compressor-prompt)

---

## Prompt Design Principles

### 1. Structured Output
- Explicitly specify output format
- Use Markdown structure for documentation
- Provide schema when YAML/JSON is required
- Separate persona (identity) from behavior (task)

### 2. Role Definition
- Clearly define Agent identity in persona prompts
- Specify professional domain and expertise
- Set behavioral guidelines in behavior prompts
- Distinguish between planning, evaluation, and execution phases

### 3. Context Management
- Place most important information at the beginning
- Use separators to distinguish sections
- Control total length to avoid truncation
- Compress data when necessary for token efficiency

### 4. Configurability
- Use placeholders `{variable}` for dynamic content
- Support language-specific prompts
- Keep core logic stable across versions
- Allow model-specific configurations

### 5. Two-Part Prompt Structure
Each agent uses two prompt files:
- **Persona Prompt** (`*_persona.md`): Defines identity, expertise, and personality
- **Behavior Prompt** (`*_behavior.md`): Defines task, input format, and output requirements

---

## Architecture Overview

### V3 Architecture (Current)

The system uses a **two-phase approach**:

1. **Structure Planning Phase**: Generate Structure Specifications (YAML)
   - **Planners**: Design organizational structure
   - **Strategists**: Suggest improvements to structure
   - **Evaluators**: Assess structure quality
   - **Integrator**: Consolidate suggestions and update spec

2. **Content Generation Phase**: Generate Markdown from Structure Spec
   - **Writer**: Produces final Markmap from Structure Spec + improvements

### Additional Agents

- **Experts**: Review baseline Markmap and suggest improvements (separate refinement workflow)
- **Translator**: Translates Markmap content between languages
- **Compressor**: Compresses long content to fit token limits

### Prompt File Organization

```
prompts/
├── planners/          # Structure planning agents
│   ├── generalist_planner_persona.md
│   ├── generalist_planner_behavior.md
│   ├── specialist_planner_persona.md
│   └── specialist_planner_behavior.md
├── strategists/       # Content strategy agents
│   ├── architect_strategist_persona.md
│   ├── architect_strategist_behavior.md
│   ├── professor_strategist_persona.md
│   ├── professor_strategist_behavior.md
│   ├── ux_strategist_persona.md
│   └── ux_strategist_behavior.md
├── evaluators/        # Quality evaluation agents
│   ├── structure_evaluator_behavior.md
│   └── content_evaluator_behavior.md
├── integrator/        # Consensus integration agent
│   ├── integrator_persona.md
│   └── integrator_behavior.md
├── writer/            # Final markdown generation
│   ├── writer_persona.md
│   ├── writer_behavior.md
│   └── markmap_format_guide.md
├── experts/           # Baseline review agents
│   ├── architect_persona.md
│   ├── architect_behavior.md
│   ├── discussion_behavior.md
│   ├── professor_persona.md
│   ├── professor_behavior.md
│   ├── engineer_persona.md
│   └── engineer_behavior.md
├── translator/        # Translation agents
│   ├── generic_translator_behavior.md
│   └── zh_tw_translator_behavior.md
└── compressor/       # Content compression
    └── compressor_behavior.md
```

---

## Planner Prompts

### Overview

Planners design the organizational structure of the Markmap. They output **Structure Specifications** in YAML format, not Markdown.

**Key Distinction**: Planners define **WHAT** to organize and **HOW** to structure it, but **NOT** how to format it. Formatting is handled by the Writer.

### Generalist Planner

**Persona**: `prompts/planners/generalist_planner_persona.md`
- Identity: Knowledge Architecture Planner
- Expertise: Cross-domain pattern recognition, holistic organization
- Focus: Strategic planning, not implementation details

**Behavior**: `prompts/planners/generalist_planner_behavior.md`

**Input Variables**:
- `{problems}`: Simplified problem data (ID, title, patterns, difficulty, has_solution)
- `{ontology}`: Ontology reference data
- `{pattern_docs}`: Pattern documentation with sub-pattern structures
- `{roadmaps}`: Learning path definitions
- `{language}`: Target language ("en" or "zh-TW")

**Output Format**: YAML Structure Specification

```yaml
metadata:
  title: "Title"
  description: "Description"
  version: "1.0"
  generated_by: "generalist"
  language: "en"

organization:
  primary_grouping: "pattern"
  display_options:
    show_complexity: true
    show_difficulty: true

sections:
  - id: "section_id"
    name: "Section Name"
    importance: "core"
    content:
      problems:
        - id: "0001"
          role: "foundation"
      learning_order: ["0001", "0002"]
      subcategories:
        - name: "Sub-category"
          problems: ["0001"]
```

### Specialist Planner

**Persona**: `prompts/planners/specialist_planner_persona.md`
- Identity: Technical Structure Planner
- Expertise: Deep technical understanding, implementation-aware design
- Focus: Technical accuracy and pattern-specific organization

**Behavior**: `prompts/planners/specialist_planner_behavior.md`

**Input Variables**: Same as Generalist Planner

**Output Format**: Same YAML Structure Specification format, but with technical precision

---

## Strategist Prompts

### Overview

Strategists analyze Structure Specifications and suggest improvements from different perspectives. They focus on **content organization**, not formatting.

### Architecture Strategist

**Persona**: `prompts/strategists/architect_strategist_persona.md`
- Identity: Architecture Strategist
- Focus: Structure, modularity, and balance
- Expertise: Software architecture principles applied to knowledge organization

**Behavior**: `prompts/strategists/architect_strategist_behavior.md`

**Input Variables**:
- `{structure_spec}`: Current Structure Specification (YAML)
- `{pattern_docs_summary}`: Summary of pattern documentation
- `{round_number}`: Current optimization round
- `{phase}`: "divergent" or "convergent"
- `{other_suggestions}`: Other strategists' suggestions (if in debate)

**Output Format**: YAML with suggestions

```yaml
suggestions:
  - id: "S1"
    type: "split" | "merge" | "reorder" | "reclassify" | "add" | "remove"
    target: "section_id or problem_id"
    proposed: "Description of change"
    rationale: "Why this improves the structure"
    priority: "high" | "medium" | "low"
```

### Professor Strategist

**Persona**: `prompts/strategists/professor_strategist_persona.md`
- Identity: Academic Strategist
- Focus: Correctness, completeness, and learning progression
- Expertise: Pedagogical organization and concept accuracy

**Behavior**: `prompts/strategists/professor_strategist_behavior.md`

**Input Variables**: Same as Architecture Strategist

**Output Format**: Same YAML suggestion format

### UX Strategist

**Persona**: `prompts/strategists/ux_strategist_persona.md`
- Identity: UX Strategist
- Focus: User experience, discoverability, and navigation
- Expertise: Information architecture and user-centered design

**Behavior**: `prompts/strategists/ux_strategist_behavior.md`

**Input Variables**: Same as Architecture Strategist

**Output Format**: Same YAML suggestion format

---

## Evaluator Prompts

### Overview

Evaluators assess the quality of Structure Specifications. They evaluate **structure and content quality**, not formatting.

### Structure Evaluator

**Behavior**: `prompts/evaluators/structure_evaluator_behavior.md`

**Evaluation Criteria**:
- Logical organization
- Appropriate depth
- Balanced sections

**Input Variables**:
- `{structure_spec}`: Structure Specification to evaluate
- `{pattern_docs_summary}`: Pattern documentation for validation
- `{criteria}`: Evaluation criteria list
- `{integration_summary}`: Summary of integration decisions

**Output Format**: YAML evaluation result

```yaml
evaluation:
  overall_score: 8.5
  criteria_scores:
    logical_organization: 9.0
    appropriate_depth: 8.0
    balanced_sections: 8.5
  strengths:
    - "Clear hierarchy"
    - "Well-balanced depth"
  improvements:
    - "Consider adding more subcategories"
  suggestions:
    - "Split large sections into smaller groups"
  approved: true
  reasoning: "Overall structure is solid with minor improvements needed"
```

### Content Evaluator

**Behavior**: `prompts/evaluators/content_evaluator_behavior.md`

**Evaluation Criteria**:
- Coverage completeness
- Learning progression
- Practical value

**Input Variables**: Same as Structure Evaluator

**Output Format**: Same YAML evaluation format

---

## Integrator Prompt

### Overview

The Integrator consolidates strategist suggestions, resolves conflicts, and produces an updated Structure Specification.

**Persona**: `prompts/integrator/integrator_persona.md`
- Identity: Consensus Integrator
- Expertise: Conflict resolution and synthesis

**Behavior**: `prompts/integrator/integrator_behavior.md`

**Input Variables**:
- `{current_structure_spec}`: Current Structure Specification (YAML)
- `{strategist_responses}`: All strategist suggestions
- `{round_number}`: Current round number
- `{consensus_threshold}`: Agreement threshold (e.g., 0.8 = 80%)
- `{num_strategists}`: Number of strategists
- `{previous_consensus}`: Previous consensus decisions
- `{previous_conflicts}`: Previous unresolved conflicts

**Output Format**: YAML with updated spec and consensus analysis

```yaml
round_result:
  consensus:
    - topic: "Add Fast-Slow subcategory"
      decision: "Adopt"
      agreed_by: ["architect_strategist", "professor_strategist", "ux_strategist"]
      agreement_ratio: 1.0
  conflicts:
    - id: "conflict_1"
      topic: "Section ordering"
      positions:
        architect_strategist: "Keep current order"
        ux_strategist: "Reorder by difficulty"
      relevant_strategists: ["architect_strategist", "ux_strategist"]

updated_structure_spec:
  # Full updated Structure Specification
  metadata:
    ...
  sections:
    ...
```

---

## Writer Prompt

### Overview

The Writer is the **ONLY** agent that produces Markdown output. It takes a Structure Specification and generates the final Markmap.

**Persona**: `prompts/writer/writer_persona.md`
- Identity: Markmap Writer
- Expertise: Markdown formatting and link generation

**Behavior**: `prompts/writer/writer_behavior.md`

**Input Variables** (Refinement Mode):
- `{baseline_markmap}`: Existing Markmap to refine
- `{adopted_improvements}`: List of expert-approved improvements
- `{improvement_details}`: Detailed descriptions of improvements
- `{problem_data}`: Problem metadata for link generation
- `{ontology_summary}`: Ontology reference

**Input Variables** (Generation Mode):
- `{structure_spec}`: Structure Specification (YAML)
- `{problem_data}`: Problem metadata
- `{ontology_summary}`: Ontology reference

**Output Format**: Markdown Markmap

**Format Guide**: `prompts/writer/markmap_format_guide.md`
- Link generation rules (GitHub vs LeetCode)
- Markdown features (bold, italic, checkboxes, etc.)
- Structure rules (hierarchy, folding, etc.)

**Key Responsibilities**:
1. Apply improvements surgically to baseline
2. Generate correct links based on solution status
3. Preserve baseline quality and style
4. Validate output formatting

---

## Expert Prompts

### Overview

Experts review a **baseline Markmap** (not Structure Spec) and suggest improvements. This is a separate refinement workflow from the planning phase.

### Architect Expert

**Persona**: `prompts/experts/architect_persona.md`
- Identity: Top Software Architect
- Focus: API Kernel design, pattern relationships, code template reusability

**Behavior**: `prompts/experts/architect_behavior.md`

**Input Variables** (Review Phase):
- `{phase}`: "Independent Review"
- `{round_number}`: 1
- `{phase_instructions}`: Phase-specific instructions
- `{baseline_markmap}`: Markmap to review
- `{ontology_summary}`: Ontology reference
- `{problem_data}`: Problem metadata
- `{min_suggestions}`: Minimum suggestions to provide
- `{max_suggestions}`: Maximum suggestions to provide

**Input Variables** (Discussion Phase):
- `{phase}`: "Full Discussion"
- `{round_number}`: 2
- `{own_suggestions}`: This expert's suggestions
- `{architect_suggestions}`: Architect's suggestions
- `{professor_suggestions}`: Professor's suggestions
- `{engineer_suggestions}`: Engineer's suggestions
- `{baseline_markmap}`: Original Markmap
- `{expert_name}`: Expert's name
- `{expert_focus_reminder}`: Focus areas reminder

**Output Format** (Review): Structured suggestions

```markdown
### A1: [Suggestion Title]
- **Type**: add | modify | remove | reorder | clarify
- **Location**: Where in the Markmap
- **What**: What to change
- **Why**: Rationale
```

**Output Format** (Discussion): Votes and adoption list

```markdown
## Part 1: Voting on Suggestions

### A1: [Suggestion]
**Vote**: ✅ Agree | ⚠️ Modify | ❌ Disagree
**Rationale**: ...

## Part 2: Final Adoption List

I recommend adopting these suggestions:
- A1, A2, P3, E1, ...
```

**Discussion Behavior**: `prompts/experts/discussion_behavior.md`
- Used in Round 2 for group discussion
- Format: Same as behavior prompt but with discussion-specific instructions

### Professor Expert

**Persona**: `prompts/experts/professor_persona.md`
- Identity: Distinguished Algorithm Professor
- Focus: Concept accuracy, learning progression, complexity analysis

**Behavior**: `prompts/experts/professor_behavior.md`

**Input Variables**: Same as Architect Expert

**Output Format**: Same suggestion format (with prefix "P" instead of "A")

### Engineer Expert

**Persona**: `prompts/experts/engineer_persona.md`
- Identity: Senior Principal Engineer
- Focus: Interview frequency, real-world applications, trade-offs

**Behavior**: `prompts/experts/engineer_behavior.md`

**Input Variables**: Same as Architect Expert

**Output Format**: Same suggestion format (with prefix "E" instead of "A")

---

## Translator Prompts

### Overview

Translators convert Markmap content between languages while preserving structure, links, and formatting.

### Generic Translator

**Behavior**: `prompts/translator/generic_translator_behavior.md`

**Input Variables**:
- Content to translate (provided directly in prompt)
- Target language (replaced in template)

**Output Format**: Translated Markdown (same structure as input)

**Key Requirements**:
- Preserve all Markdown syntax
- Keep links unchanged
- Maintain formatting (bold, italic, code blocks)
- Translate only text content

### Traditional Chinese Translator

**Behavior**: `prompts/translator/zh_tw_translator_behavior.md`

**Input Variables**: Same as Generic Translator

**Output Format**: Traditional Chinese Markdown

**Special Considerations**:
- Use Traditional Chinese terminology
- Maintain technical terms appropriately
- Preserve code and links

---

## Compressor Prompt

### Overview

The Compressor reduces content length while preserving essential information. Used when content exceeds token limits.

**Behavior**: `prompts/compressor/compressor_behavior.md`

**Input Variables**:
- `{content}`: Content to compress
- `{target_ratio}`: Target compression ratio (e.g., 50 = 50% of original)

**Output Format**: Compressed content

**Preservation Priorities**:
1. **Critical**: Key decisions, final choices
2. **Important**: Rationale, trade-offs
3. **Optional**: Detailed debates, minor points

**Compression Guidelines**:
- Keep decision outcomes
- Summarize debate points
- Remove redundant explanations
- Maintain chronological order
- Preserve hierarchical structure when possible

---

## Prompt Version Control

### Recommended Structure

```
prompts/
├── v1/              # Legacy prompts (V2 architecture)
│   └── ...
├── v2/              # Previous version
│   └── ...
└── current/         # Current version (V3)
    ├── planners/
    ├── strategists/
    ├── evaluators/
    ├── integrator/
    ├── writer/
    ├── experts/
    ├── translator/
    └── compressor/
```

### Versioning Guidelines

1. **Major Changes**: Create new version directory
   - Architecture changes (V2 → V3)
   - Output format changes (Markdown → YAML)

2. **Minor Changes**: Update files in place
   - Clarifications
   - Example updates
   - Variable additions

3. **Documentation**: Update this guide when prompts change

---

## Configuration Reference

### Agent Configuration Pattern

Each agent is configured in `config.yaml` with:

```yaml
models:
  agent_name:
    model: "gpt-4o"
    persona_prompt: "prompts/agent/agent_persona.md"
    behavior_prompt: "prompts/agent/agent_behavior.md"
    temperature: 0.7
    max_tokens: 4096
```

### Prompt Loading

Prompts are loaded by `BaseAgent._load_prompt()`:
- Paths are relative to `tools/ai-markmap-agent/`
- UTF-8 encoding
- Cached after first load

### Variable Formatting

Variables are formatted using Python's `.format()`:
- `{variable}`: Required variable
- Missing variables: Warning logged, template returned as-is

---

*Last updated: 2025-12-22*

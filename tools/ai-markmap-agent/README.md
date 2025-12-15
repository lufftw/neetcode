# AI Markmap Agent

> A multi-expert refinement system for Markmap improvement using LangGraph.

[![LangGraph](https://img.shields.io/badge/LangGraph-v1.0.4-blue)](https://github.com/langchain-ai/langgraph)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 📋 Table of Contents

- [Overview](#overview)
- [Core Philosophy](#core-philosophy)
- [Architecture](#architecture)
- [Workflow](#workflow)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Expert Roles](#expert-roles)
- [Project Structure](#project-structure)

---

## Overview

This system refines existing high-quality Markmaps through multi-expert review and consensus-based discussion. Instead of generating from scratch, it starts with a baseline Markmap and improves it through domain-specific expert analysis.

### Key Features

| Feature | Description |
|---------|-------------|
| **Refinement Mode** | Start from a high-quality baseline, not from scratch |
| **Domain Experts** | Architect, Professor, Engineer perspectives |
| **Consensus Voting** | Programmatic majority voting (2/3 required) |
| **Natural Language** | Suggestions in natural language, not rigid formats |
| **Efficient API Calls** | Only 2N + 1 calls (N = number of experts) |

---

## Core Philosophy

### "Refinement, Not Creation"

| Old Approach | New Approach |
|--------------|--------------|
| Create structure from data | Start from high-quality baseline |
| YAML intermediate format | Work directly with Markmap |
| Generic strategist roles | Domain-specific experts |
| AI-based integration | Programmatic consensus |

### Why Refinement is Better

1. **Quality Preservation** - Don't reinvent what already works well
2. **Focused Discussion** - Experts discuss "what to improve", not "what to create"
3. **Natural Language** - AI excels at understanding and generating natural text
4. **Efficient** - Fewer API calls, faster iteration

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AI Markmap Agent                                      │
│                   Refinement Mode — 2-Round Discussion                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ════════════════════════════════════════════════════════════════════════  │
│  Phase 0: Load Baseline                                                     │
│  ════════════════════════════════════════════════════════════════════════  │
│                                                                             │
│  ┌─────────────────────────────────┐                                        │
│  │ Baseline Markmap                │                                        │
│  │ (e.g., neetcode_ontology_ai.md) │                                        │
│  └───────────┬─────────────────────┘                                        │
│              │                                                              │
│  ════════════════════════════════════════════════════════════════════════  │
│  Phase 1: Independent Review (N parallel API calls)                         │
│  ════════════════════════════════════════════════════════════════════════  │
│              │                                                              │
│   ┌──────────┴──────────┬──────────────────┐                               │
│   ▼                     ▼                  ▼                               │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                 │
│   │ 🏗️ Architect │    │ 📚 Professor │    │ ⚙️ Engineer  │                 │
│   │ 5-10 ideas   │    │ 5-10 ideas   │    │ 5-10 ideas   │                 │
│   └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                 │
│          │                   │                   │                         │
│          └───────────────────┼───────────────────┘                         │
│                              │                                             │
│  ════════════════════════════════════════════════════════════════════════  │
│  Phase 2: Full Discussion (N parallel API calls)                            │
│  ════════════════════════════════════════════════════════════════════════  │
│                              │                                             │
│   Each expert sees ALL suggestions, votes: ✅ / ⚠️ / ❌                    │
│   Each expert outputs their Final Adoption List                            │
│                              │                                             │
│  ════════════════════════════════════════════════════════════════════════  │
│  Phase 3: Consensus Calculation (Code, not AI)                              │
│  ════════════════════════════════════════════════════════════════════════  │
│                              │                                             │
│   Majority voting: 2/3 (≥67%) agreement required                           │
│   ✅ Adopted: A1, A3, P1, E1, E4                                           │
│   ❌ Rejected: A2, P2, P3, E2, E3                                          │
│                              │                                             │
│  ════════════════════════════════════════════════════════════════════════  │
│  Phase 4: Writer (1 API call)                                               │
│  ════════════════════════════════════════════════════════════════════════  │
│                              │                                             │
│   Apply adopted improvements to baseline → Refined Markmap                 │
│                              │                                             │
│  ════════════════════════════════════════════════════════════════════════  │
│  Phase 5-6: Translation & Post-Processing                                   │
│  ════════════════════════════════════════════════════════════════════════  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### API Call Efficiency

| Experts (N) | API Calls | Sequential Batches |
|-------------|-----------|-------------------|
| 3 (default) | 7         | 3 (fixed)         |
| 5           | 11        | 3 (fixed)         |
| 7           | 15        | 3 (fixed)         |

---

## Workflow

### Phase 0: Load Baseline

Load an existing high-quality Markmap as the starting point.

### Phase 1: Independent Review

Each expert independently reviews the baseline and suggests 5-10 improvements:
- No group influence
- Natural language suggestions
- Focus on their domain expertise

### Phase 2: Full Discussion

Each expert:
1. Sees all suggestions from all experts
2. Votes on each suggestion (✅ Agree / ⚠️ Modify / ❌ Disagree)
3. Outputs their final adoption list

### Phase 3: Consensus Calculation

**Programmatic, not AI:**
- Count votes for each suggestion
- Adopt if ≥67% (2/3) agreement
- Reject otherwise

### Phase 4: Writer

Apply adopted improvements surgically to the baseline:
- Minimal changes
- Preserve existing quality
- Verify links and formatting

### Phase 5-6: Post-Processing

- Translation (en → zh-TW)
- Link validation
- HTML generation

---

## Installation

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Unix/macOS)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

### Basic Usage

```bash
# Run with default baseline
python main.py

# Specify a baseline file
python main.py --baseline path/to/markmap.md

# Dry run (load data only)
python main.py --dry-run
```

### Translation Only

Translate an existing Markmap without running the full pipeline:

```bash
# Translate latest English output to zh-TW
python translate_only.py

# Translate specific file
python translate_only.py --input path/to/file_en.md

# Custom source/target languages
python translate_only.py --source en --target zh-TW

# Also generate HTML
python translate_only.py --html

### Standalone HTML Converter

For converting Markdown files to HTML without running the full pipeline:

```bash
# Basic conversion (output: input.html)
python convert_to_html.py input.md

# Specify output file
python convert_to_html.py input.md -o output.html

# Custom title
python convert_to_html.py input.md -t "My Mind Map"

# Use custom template
python convert_to_html.py input.md --template templates/custom.html
```

This tool is **completely independent** of the main pipeline and only requires:
- Python 3.10+
- `jinja2` package

It can be used to convert any Markmap Markdown file to interactive HTML.

### Integration with Pipeline

The standalone tool can be integrated with the main pipeline. To use it instead of the internal converter, set in `config/config.yaml`:

```yaml
output:
  html:
    use_standalone_tool: true  # Use convert_to_html.py instead of internal converter
```

This maintains **decoupling** (the tool can run independently) while allowing **integration** (the pipeline can call it programmatically).
```

### API Keys

API keys are entered at runtime and **never stored**:

```bash
python main.py

# You'll be prompted:
# Enter OPENAI API Key: ********
#   ✓ OPENAI API key accepted
```

Skip API key prompts:

```bash
python main.py --no-openai
python main.py --no-anthropic
```

---

## Configuration

All settings in `config/config.yaml`.

### Expert Configuration

```yaml
experts:
  enabled:
    - "architect"
    - "professor"
    - "engineer"
  
  suggestions:
    min_per_expert: 5
    max_per_expert: 10
  
  definitions:
    architect:
      name: "Top Software Architect"
      emoji: "🏗️"
      model: "gpt-4o"
      focus_areas:
        - "API Kernel abstraction"
        - "Pattern relationships"
        - "Code template reusability"
```

### Refinement Scope

Control what can be changed:

```yaml
refinement_scope:
  allowed_changes:
    structure:
      enabled: true
      max_depth_change: 1
    content:
      add_content: true
      remove_content: true
      modify_content: true
    problems:
      add_problems: true
      remove_problems: false  # Conservative
      reorder_problems: true
```

### Workflow Settings

```yaml
workflow:
  discussion_rounds: 2
  parallel_execution: true
  consensus_threshold: 0.67  # 2/3 required
```

---

## Expert Roles

### 🏗️ Top Software Architect

**Focus**: API design, modularity, system mapping

**Reviews for**:
- Clean API Kernel abstractions
- Pattern composability
- Code template reusability
- System design connections

### 📚 Distinguished Algorithm Professor

**Focus**: Correctness, pedagogy, theory

**Reviews for**:
- Concept accuracy
- Learning progression
- Complexity analysis
- Invariant descriptions

### ⚙️ Senior Principal Engineer

**Focus**: Practical value, interviews, trade-offs

**Reviews for**:
- Interview frequency
- Real-world applications
- Trade-off explanations
- Knowledge discoverability

---

## Project Structure

```
ai-markmap-agent/
├── config/
│   └── config.yaml              # Main configuration
├── prompts/
│   ├── experts/                 # Expert prompts
│   │   ├── architect_persona.md
│   │   ├── architect_behavior.md
│   │   ├── professor_persona.md
│   │   ├── professor_behavior.md
│   │   ├── engineer_persona.md
│   │   ├── engineer_behavior.md
│   │   └── discussion_behavior.md
│   └── writer/
│       ├── writer_persona.md
│       ├── writer_behavior.md
│       └── markmap_format_guide.md
├── src/
│   ├── agents/
│   │   ├── base_agent.py        # Base agent class
│   │   ├── expert.py            # Expert agents
│   │   ├── writer.py            # Writer agent
│   │   └── translator.py        # Translator agent
│   ├── consensus.py             # Consensus calculation (code)
│   ├── graph.py                 # LangGraph workflow
│   ├── config_loader.py         # Configuration loading
│   └── ...
├── main.py                      # Entry point
├── outputs/
│   ├── versions/                # Version history (v1, v2, ...)
│   ├── debug/                   # Debug logs per run
│   └── intermediate/            # Intermediate outputs
└── README.md
```

---

## Output

### Output Files

Final Markmaps are saved to:
- **Markdown**: `docs/mindmaps/`
- **HTML**: `docs/pages/mindmaps/`

Filename format: `neetcode_ontology_agent_evolved_{lang}.{ext}`

Examples:
- `neetcode_ontology_agent_evolved_en.md`
- `neetcode_ontology_agent_evolved_zh-TW.html`

### Version History

Each run saves a versioned copy to `outputs/versions/`:

```
outputs/versions/
├── v1/
│   ├── neetcode_ontology_agent_evolved_en.md
│   └── neetcode_ontology_agent_evolved_zh-TW.md
├── v2/
│   └── ...
└── v3/
    └── ...
```

Version numbers auto-increment: `v1`, `v2`, `v3`, ...

### Versioning Modes

Configure in `config/config.yaml`:

```yaml
output:
  versioning:
    enabled: true
    directory: "outputs/versions"
    mode: "continue"      # continue | reset
    prompt_on_reset: true
```

| Mode | Behavior |
|------|----------|
| `continue` | Load from latest version (vN), produce vN+1 |
| `reset` | Start fresh from `input.baseline.path`, produce v1 |

**Reset mode** prompts for confirmation. Old versions are deleted only after the pipeline completes successfully (safe: if pipeline fails, old versions are preserved).

### Resume Mode

Resume mode allows you to continue execution from a previous pipeline run, supporting:
- Reusing completed stage outputs (saves tokens and time)
- Re-running from a specific stage (debug-friendly)
- Not overwriting original run data (generates new regen run)

#### Resume vs Reset

**Important distinction:**
- **`--resume`**: Reuses debug outputs from previous runs to save API calls. This is about **pipeline execution** (whether to run new API calls or reuse existing results).
- **`versioning.mode: reset`**: Deletes old version directories and starts fresh. This is about **version management** (how to organize final output versions).

These two features are **independent**:
- You can use `--resume` even when `versioning.mode: reset` is set
- Resume mode reuses debug outputs regardless of versioning mode
- Versioning reset only affects final output directories, not debug outputs
- When resuming, versioning reset prompts are skipped (reset applies to final output only)

#### Usage

**Method 1: Interactive Resume Mode**

```bash
python main.py --resume
```

After startup, it will:
1. Scan all previous runs under `outputs/debug/`
2. Display them sorted by time (newest first)
3. Let you select the run to resume
4. Ask whether to reuse each stage's output one by one

**Method 2: Start from a Specific Stage**

```bash
python main.py --resume --from-stage writer
```

This will automatically:
- Select the latest run
- Reuse outputs from `expert_review`, `full_discussion`, `consensus`
- Re-run from the `writer` stage

**Supported stages:**
- `expert_review`
- `full_discussion`
- `consensus`
- `writer`
- `translate`
- `post_process`

#### Run Naming Rules

- **Original run**: `run_YYYYMMDD_HHMMSS/`
- **Resume from original run**: `run_YYYYMMDD_HHMMSS_regen_1/`
- **Resume again**: `run_YYYYMMDD_HHMMSS_regen_2/`

**Important**: Original run data is never overwritten, all new outputs are in regen directories.

#### State Loading

The system automatically loads:
- ✅ **Consensus data**: Loaded from JSON file (if reusing consensus stage)
- ✅ **Writer output**: Loaded from writer output file (if reusing writer stage)
- ⚠️ **Expert responses**: Currently only marked as reused, incomplete recovery (needs improvement)

#### Notes

1. **Ensure debug_output.enabled = true**: Resume mode depends on debug output
2. **API Keys**: Still need to provide API keys (even when reusing stages)
3. **Configuration consistency**: Resume uses current config, which may differ from original run
4. **Partial state recovery**: Currently only partial state recovery is supported, some stages may need to be re-run

---

## Module Responsibilities

| Module | Responsibility |
|--------|----------------|
| `expert.py` | Domain-specific expert agents |
| `consensus.py` | Programmatic majority voting |
| `writer.py` | Refinement-mode writer |
| `graph.py` | LangGraph workflow orchestration |
| `config_loader.py` | Configuration management |

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Related

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
- [Markmap](https://markmap.js.org/)

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
- Link validation and normalization
- Automatic LeetCode URL generation
- GitHub solution link addition
- Comparison file generation

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
```

#### How to Output `neetcode_ontology_agent_evolved_zh-TW.md`

The `translate_only.py` script automatically generates the translated file with the correct naming convention. Here's how to use it:

**Method 1: Translate Latest English Output (Recommended)**

If you have already generated the English version (`neetcode_ontology_agent_evolved_en.md`), the script will automatically find it and translate it:

```bash
cd tools/ai-markmap-agent

# This will:
# 1. Find the latest English output (from version history or final output)
# 2. Translate it to zh-TW using gpt-5.2
# 3. Save as neetcode_ontology_agent_evolved_zh-TW.md in the final output directory
python translate_only.py
```

The output will be saved to:
- **Markdown**: `../../docs/mindmaps/neetcode_ontology_agent_evolved_zh-TW.md`
- **HTML** (if using `--html`): `../../docs/pages/mindmaps/neetcode_ontology_agent_evolved_zh-TW.html`

**Method 2: Translate a Specific File**

If you want to translate a specific English file:

**Important**: 
- **CLI Tool**: Can be run from **any directory** - relative paths are resolved relative to the script directory
- **Default output location**: When using `--output`, files are saved to the specified path
- **Auto-detection**: Without `--output`, files are saved to `docs/mindmaps/` (configured in `config.yaml`)
- **Version history**: The main pipeline also saves to `outputs/versions/v1/` for tracking, but `translate_only.py` only saves to the final location

**Working with `docs/mindmaps/` directory:**

**Option 1: From Script Directory (Recommended)**

**Unix/macOS:**
```bash
# Navigate to the script directory
cd tools/ai-markmap-agent

# Translate a specific file (auto-detects output to docs/mindmaps/)
python translate_only.py --input ../../docs/mindmaps/neetcode_ontology_agent_evolved_en.md

# Or with explicit output path to docs/mindmaps/
python translate_only.py \
    --input ../../docs/mindmaps/neetcode_ontology_agent_evolved_en.md \
    --output ../../docs/mindmaps/neetcode_ontology_agent_evolved_zh-TW.md

# Translate and generate HTML in one step
python translate_only.py \
    --input ../../docs/mindmaps/neetcode_ontology_agent_evolved_en.md \
    --output ../../docs/mindmaps/neetcode_ontology_agent_evolved_zh-TW.md \
    --html
```

**Windows PowerShell:**
```powershell
# Navigate to the script directory
cd tools\ai-markmap-agent

# Translate a specific file (auto-detects output to docs\mindmaps\)
python translate_only.py --input ..\..\docs\mindmaps\neetcode_ontology_agent_evolved_en.md

# Or with explicit output path to docs\mindmaps\
python translate_only.py `
    --input ..\..\docs\mindmaps\neetcode_ontology_agent_evolved_en.md `
    --output ..\..\docs\mindmaps\neetcode_ontology_agent_evolved_zh-TW.md

# Translate and generate HTML in one step
python translate_only.py `
    --input ..\..\docs\mindmaps\neetcode_ontology_agent_evolved_en.md `
    --output ..\..\docs\mindmaps\neetcode_ontology_agent_evolved_zh-TW.md `
    --html
```

**Option 2: From Project Root (CLI Tool Mode)**

**Unix/macOS:**
```bash
# From project root - relative paths resolved relative to script directory
python tools/ai-markmap-agent/translate_only.py \
    --input docs/mindmaps/neetcode_ontology_agent_evolved_en.md \
    --output docs/mindmaps/neetcode_ontology_agent_evolved_zh-TW.md

# With HTML generation
python tools/ai-markmap-agent/translate_only.py \
    --input docs/mindmaps/neetcode_ontology_agent_evolved_en.md \
    --output docs/mindmaps/neetcode_ontology_agent_evolved_zh-TW.md \
    --html
```

**Windows PowerShell:**
```powershell
# From project root - relative paths resolved relative to script directory
python tools\ai-markmap-agent\translate_only.py `
    --input docs\mindmaps\neetcode_ontology_agent_evolved_en.md `
    --output docs\mindmaps\neetcode_ontology_agent_evolved_zh-TW.md

# With HTML generation
python tools\ai-markmap-agent\translate_only.py `
    --input docs\mindmaps\neetcode_ontology_agent_evolved_en.md `
    --output docs\mindmaps\neetcode_ontology_agent_evolved_zh-TW.md `
    --html
```

**Option 3: Using Absolute Paths**

**Unix/macOS:**
```bash
# From any directory using absolute paths
python /path/to/neetcode/tools/ai-markmap-agent/translate_only.py \
    --input /path/to/neetcode/docs/mindmaps/neetcode_ontology_agent_evolved_en.md \
    --output /path/to/neetcode/docs/mindmaps/neetcode_ontology_agent_evolved_zh-TW.md
```

**Windows PowerShell:**
```powershell
# From any directory using absolute paths
python C:\Developer\program\python\neetcode\tools\ai-markmap-agent\translate_only.py `
    --input C:\Developer\program\python\neetcode\docs\mindmaps\neetcode_ontology_agent_evolved_en.md `
    --output C:\Developer\program\python\neetcode\docs\mindmaps\neetcode_ontology_agent_evolved_zh-TW.md
```

**Note on Output Locations:**
- **Version History** (main pipeline only): `tools/ai-markmap-agent/outputs/versions/v1/` (for tracking changes)
- **Final Output** (translate_only.py): `docs/mindmaps/` (for actual use)
- When using `--output`, the file is saved to the specified path
- When not using `--output`, it auto-detects based on config (saves to `docs/mindmaps/`)
- **Path Resolution**: Relative paths are always resolved relative to the script directory (`tools/ai-markmap-agent/`), not the current working directory
**Method 3: Translate and Generate HTML in One Step**

```bash
# Translate and generate HTML output
python translate_only.py --html
```

This will:
1. Translate the English markdown to Traditional Chinese (Taiwan)
2. Generate the HTML file with the same name

**Configuration**

The translation uses settings from `config/config.yaml`:

- **Model**: `gpt-5.2` (configured in `output.naming.languages.zh-TW.translator_model`)
- **Source Language**: `en` (default)
- **Target Language**: `zh-TW` (default)
- **Max Tokens**: `translator_max_tokens` (configured in `output.naming.languages.zh-TW.translator_max_tokens`)
  - **gpt-5.2**: Recommended `128000` (max output capacity: 128,000 tokens, context window: 400,000 tokens)
  - **gpt-4o**: Recommended `16384` (max output typically 16,384 tokens)
  - **gpt-4**: Recommended `8192` (max output typically 8,192 tokens)
  - **Default**: `8192` if not specified
- **Prompt**: Uses `prompts/translator/zh_tw_translator_behavior.md` with comprehensive Taiwan DSA terminology rules

**Important**: Set `translator_max_tokens` appropriately for your model. If the value is too small, the API may return empty responses for large translations.

**Custom Model Override**

You can override the model for a single translation:

```bash
python translate_only.py --model gpt-4o
```

**Error Handling**

All translation errors include detailed request information for debugging:
- Model name and configuration
- Prompt size (chars and estimated tokens)
- Content size
- Max output tokens setting
- Full request/response saved to debug output files

**Notes**

- The script reads from `config/config.yaml` for output directory settings
- Translation prompt enforces Taiwan-specific terminology (not Mainland China terms)
- API keys are requested at runtime and cleared after execution
- The output filename automatically replaces the language suffix (e.g., `_en` → `_zh-TW`)
- **Always check debug output files** when errors occur - they contain the full API request/response

### Standalone HTML Converter

For converting Markdown files to HTML without running the full pipeline:

**Important**: 
- **CLI Tool**: Can be run from **any directory** - relative paths are resolved relative to the script directory
- Supports both relative and absolute paths
- Template paths are resolved relative to the script directory

**Basic Usage:**

**Option 1: From Script Directory**

**Unix/macOS:**
```bash
# Navigate to script directory
cd tools/ai-markmap-agent

# Basic conversion (output: input.html in same directory)
python convert_to_html.py input.md

# Specify output file
python convert_to_html.py input.md -o output.html

# Custom title
python convert_to_html.py input.md -t "My Mind Map"

# Use custom template
python convert_to_html.py input.md --template templates/custom.html
```

**Windows PowerShell:**
```powershell
# Navigate to script directory
cd tools\ai-markmap-agent

# Basic conversion (output: input.html in same directory)
python convert_to_html.py input.md

# Specify output file
python convert_to_html.py input.md -o output.html

# Custom title
python convert_to_html.py input.md -t "My Mind Map"

# Use custom template
python convert_to_html.py input.md --template templates\custom.html
```

**Option 2: From Project Root (CLI Tool Mode)**

**Unix/macOS:**
```bash
# From project root - relative paths resolved relative to script directory
python tools/ai-markmap-agent/convert_to_html.py \
    docs/mindmaps/neetcode_ontology_agent_evolved_en.md \
    -o docs/pages/mindmaps/neetcode_ontology_agent_evolved_en.html \
    -t "NeetCode Agent Evolved Mindmap (EN)"
```

**Windows PowerShell:**
```powershell
# From project root - relative paths resolved relative to script directory
python tools\ai-markmap-agent\convert_to_html.py `
    docs\mindmaps\neetcode_ontology_agent_evolved_en.md `
    -o docs\pages\mindmaps\neetcode_ontology_agent_evolved_en.html `
    -t "NeetCode Agent Evolved Mindmap (EN)"
```

**Working with `docs/mindmaps/` directory:**

**Option 1: From Script Directory**

**Unix/macOS:**
```bash
# Navigate to the tool directory
cd tools/ai-markmap-agent

# Convert English version
python convert_to_html.py \
    ../../docs/mindmaps/neetcode_ontology_agent_evolved_en.md \
    -o ../../docs/pages/mindmaps/neetcode_ontology_agent_evolved_en.html \
    -t "NeetCode Agent Evolved Mindmap (EN)"

# Convert Traditional Chinese version
python convert_to_html.py \
    ../../docs/mindmaps/neetcode_ontology_agent_evolved_zh-TW.md \
    -o ../../docs/pages/mindmaps/neetcode_ontology_agent_evolved_zh-TW.html \
    -t "NeetCode Agent Evolved Mindmap (繁體中文)"
```

**Windows PowerShell:**
```powershell
# Navigate to the tool directory
cd tools\ai-markmap-agent

# Convert English version
python convert_to_html.py `
    ..\..\docs\mindmaps\neetcode_ontology_agent_evolved_en.md `
    -o ..\..\docs\pages\mindmaps\neetcode_ontology_agent_evolved_en.html `
    -t "NeetCode Agent Evolved Mindmap (EN)"

# Convert Traditional Chinese version
python convert_to_html.py `
    ..\..\docs\mindmaps\neetcode_ontology_agent_evolved_zh-TW.md `
    -o ..\..\docs\pages\mindmaps\neetcode_ontology_agent_evolved_zh-TW.html `
    -t "NeetCode Agent Evolved Mindmap (繁體中文)"
```

**Option 2: From Project Root (CLI Tool Mode)**

**Unix/macOS:**
```bash
# From project root - relative paths resolved relative to script directory
python tools/ai-markmap-agent/convert_to_html.py \
    docs/mindmaps/neetcode_ontology_agent_evolved_en.md \
    -o docs/pages/mindmaps/neetcode_ontology_agent_evolved_en.html \
    -t "NeetCode Agent Evolved Mindmap (EN)"

python tools/ai-markmap-agent/convert_to_html.py \
    docs/mindmaps/neetcode_ontology_agent_evolved_zh-TW.md \
    -o docs/pages/mindmaps/neetcode_ontology_agent_evolved_zh-TW.html \
    -t "NeetCode Agent Evolved Mindmap (繁體中文)"
```

**Windows PowerShell:**
```powershell
# From project root - relative paths resolved relative to script directory
python tools\ai-markmap-agent\convert_to_html.py `
    docs\mindmaps\neetcode_ontology_agent_evolved_en.md `
    -o docs\pages\mindmaps\neetcode_ontology_agent_evolved_en.html `
    -t "NeetCode Agent Evolved Mindmap (EN)"

python tools\ai-markmap-agent\convert_to_html.py `
    docs\mindmaps\neetcode_ontology_agent_evolved_zh-TW.md `
    -o docs\pages\mindmaps\neetcode_ontology_agent_evolved_zh-TW.html `
    -t "NeetCode Agent Evolved Mindmap (繁體中文)"
```

This tool is **completely independent** of the main pipeline and only requires:
- Python 3.10+
- `jinja2` package

It can be used to convert any Markmap Markdown file to interactive HTML.

**Note on Path Resolution:**
- Relative paths are always resolved relative to the script directory (`tools/ai-markmap-agent/`), not the current working directory
- This allows the tools to work as CLI tools from any directory
- Absolute paths work as expected

**Windows PowerShell:**
```powershell
# Convert English version
python convert_to_html.py `
    ..\..\docs\mindmaps\neetcode_ontology_agent_evolved_en.md `
    -o ..\..\docs\pages\mindmaps\neetcode_ontology_agent_evolved_en.html `
    -t "NeetCode Agent Evolved Mindmap (EN)"

# Convert Traditional Chinese version
python convert_to_html.py `
    ..\..\docs\mindmaps\neetcode_ontology_agent_evolved_zh-TW.md `
    -o ..\..\docs\pages\mindmaps\neetcode_ontology_agent_evolved_zh-TW.html `
    -t "NeetCode Agent Evolved Mindmap (繁體中文)"
```

**Batch conversion script** (save as `convert_all_mindmaps.sh` or `.bat`):

**Unix/macOS:**
```bash
#!/bin/bash
cd "$(dirname "$0")"

# Ensure output directory exists
mkdir -p ../../docs/pages/mindmaps

# Convert English
python convert_to_html.py \
    ../../docs/mindmaps/neetcode_ontology_agent_evolved_en.md \
    -o ../../docs/pages/mindmaps/neetcode_ontology_agent_evolved_en.html \
    -t "NeetCode Agent Evolved Mindmap (EN)"

# Convert Traditional Chinese
python convert_to_html.py \
    ../../docs/mindmaps/neetcode_ontology_agent_evolved_zh-TW.md \
    -o ../../docs/pages/mindmaps/neetcode_ontology_agent_evolved_zh-TW.html \
    -t "NeetCode Agent Evolved Mindmap (繁體中文)"

echo "✅ All conversions complete!"
```

**Windows:**
```batch
@echo off
cd /d "%~dp0"

REM Ensure output directory exists
if not exist "..\..\docs\pages\mindmaps" mkdir "..\..\docs\pages\mindmaps"

REM Convert English
python convert_to_html.py ^
    ..\..\docs\mindmaps\neetcode_ontology_agent_evolved_en.md ^
    -o ..\..\docs\pages\mindmaps\neetcode_ontology_agent_evolved_en.html ^
    -t "NeetCode Agent Evolved Mindmap (EN)"

REM Convert Traditional Chinese
python convert_to_html.py ^
    ..\..\docs\mindmaps\neetcode_ontology_agent_evolved_zh-TW.md ^
    -o ..\..\docs\pages\mindmaps\neetcode_ontology_agent_evolved_zh-TW.html ^
    -t "NeetCode Agent Evolved Mindmap (繁體中文)"

echo ✅ All conversions complete!
```

### Integration with Pipeline

The standalone tool is **automatically used** by the main pipeline. The pipeline
calls `convert_to_html.py` programmatically to generate HTML files. This maintains
**decoupling** (the tool can run independently) while enabling **integration**
(the pipeline calls it automatically).

The HTML template is stored in `templates/markmap.html` and can be customized
without modifying code.

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

## Post-Processing Link Generation

### Link Format

Post-processing automatically converts LeetCode problem references to standardized links:

**Format:**
```
[LeetCode 11](leetcode_url) | [Solution](github_url)
```

**Features:**
- Simple format: Only problem ID, no title
- Handles multiple AI-generated formats
- Auto-generates LeetCode URLs from API cache
- Adds GitHub solution links when available

### Data Sources

1. **Local TOML files** (`meta/problems/`) - Primary source
2. **LeetCode API cache** (`tools/.cache/leetcode_problems.json`) - Auto-supplement

**Priority:** Local TOML > API cache

### Comparison Files

After each post-processing run, a comparison file is automatically generated:

**Location:** `outputs/final/post_processing_comparison_{timestamp}.md`

**Contents:**
- Before: Original AI-generated content
- After: Post-processed content with normalized links

**Usage:**
- Verify link generation correctness
- Check format compliance
- Identify improvements needed

### LeetCode API Integration

The system automatically syncs with LeetCode API:

```bash
# Sync LeetCode problem data (7-day cache)
python tools/sync_leetcode_data.py

# Check cache status
python tools/sync_leetcode_data.py --check
```

**Integration:**
- `PostProcessor` automatically loads and merges API cache data
- Missing URLs are auto-generated from API data
- No configuration required

See [Post-Processing Links Documentation](docs/POST_PROCESSING_LINKS.md) for details.

---

## Module Responsibilities

| Module | Responsibility |
|--------|----------------|
| `expert.py` | Domain-specific expert agents |
| `consensus.py` | Programmatic majority voting |
| `writer.py` | Refinement-mode writer |
| `graph.py` | LangGraph workflow orchestration |
| `post_processing.py` | Link normalization and generation |
| `leetcode_api.py` | LeetCode API data loading |
| `config_loader.py` | Configuration management |

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Related

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
- [Markmap](https://markmap.js.org/)

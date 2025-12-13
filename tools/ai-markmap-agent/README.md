# AI Markmap Agent

> A configurable, extensible multi-agent AI system for generating and optimizing Markmaps using LangGraph.

[![LangGraph](https://img.shields.io/badge/LangGraph-v1.0.4-blue)](https://github.com/langchain-ai/langgraph)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Workflow Phases](#workflow-phases)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Agent Capabilities](#agent-capabilities)
- [Memory System](#memory-system)
- [Project Structure](#project-structure)

---

## Overview

This system orchestrates multiple AI agents to collaboratively generate, optimize, debate, and select the best Markmap from metadata and ontology inputs. It leverages **LangGraph**'s State + Graph paradigm for controllable agent orchestration.

### Key Features

| Feature | Description |
|---------|-------------|
| **Multi-Model Support** | Configure different LLMs for each agent role |
| **Multi-Language** | Generate Markmaps in English and Traditional Chinese |
| **Iterative Optimization** | Configurable N-round optimization with debate |
| **Memory System** | Short-term (STM) and Long-term Memory (LTM) support |
| **Content Compression** | Auto-summarize when content exceeds thresholds |
| **Configurable Workflow** | All parameters adjustable via YAML config |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        AI Markmap Agent System                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐             │
│  │ Generalist  │    │ Specialist  │    │  Optimizer  │             │
│  │   Agents    │    │   Agents    │    │   Agents    │             │
│  │  (EN / ZH)  │    │  (EN / ZH)  │    │  (2-3 roles)│             │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘             │
│         │                  │                  │                     │
│         └──────────────────┼──────────────────┘                     │
│                            ▼                                        │
│                   ┌─────────────────┐                               │
│                   │   Summarizer    │                               │
│                   └────────┬────────┘                               │
│                            ▼                                        │
│                   ┌─────────────────┐                               │
│                   │     Judges      │                               │
│                   │   (Evaluators)  │                               │
│                   └────────┬────────┘                               │
│                            ▼                                        │
│                   ┌─────────────────┐                               │
│                   │  Final Output   │                               │
│                   │  (Markmap HTML) │                               │
│                   └─────────────────┘                               │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                     Shared Components                         │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │  │
│  │  │   STM    │  │   LTM    │  │ Compress │  │   Config     │  │  │
│  │  │ (Memory) │  │ (Vector) │  │ (Summary)│  │   Loader     │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────┘  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Workflow Phases

### Phase 1: Baseline Generation

Generate 4 initial Markmaps in parallel:

| Agent Type | Language | Model (Configurable) | Output File |
|------------|----------|---------------------|-------------|
| Generalist | English | `gpt-4-turbo` | `markmap_general_en.md` |
| Generalist | 繁體中文 | `gpt-4-turbo` | `markmap_general_zh.md` |
| Specialist | English | `gpt-4-turbo` | `markmap_specialist_en.md` |
| Specialist | 繁體中文 | `gpt-4-turbo` | `markmap_specialist_zh.md` |

- **Generalist**: Optimized for broad understanding, knowledge organization, global perspective
- **Specialist**: Optimized for engineering details, structural rigor, implementation-oriented

### Phase 2: Iterative Optimization & Debate

```
┌─────────────────────────────────────────────────────────────────┐
│                    Optimization Loop (N rounds)                 │
│                                                                 │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │ Optimizer 1 │ ←→  │ Optimizer 2 │ ←→  │ Optimizer 3 │       │
│  │ (Structure) │     │ (Semantic)  │     │(Readability)│       │
│  └──────┬──────┘     └──────┬──────┘     └──────┬──────┘       │
│         │                   │                   │               │
│         └───────────────────┼───────────────────┘               │
│                             ▼                                   │
│                    All opinions visible                         │
│                    to each other                                │
│                             │                                   │
│                             ▼                                   │
│                   ┌─────────────────┐                           │
│                   │   Summarizer    │                           │
│                   │ (Round Summary) │                           │
│                   └─────────────────┘                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Key Features:**
- 2-3 optimizer agents (configurable)
- Each agent can use a different model
- All agents can see each other's discussion
- First round receives full metadata; subsequent rounds receive only:
  - Previous round's Markmap
  - Discussion history
  - Summary

### Phase 3: Round Summarization

After each optimization round:
- **Summarizer Agent** consolidates all optimization and debate content
- Outputs:
  - Updated Markmap for that round
  - Decision summary (for next round)

### Phase 4: Final Evaluation & Selection

```
┌─────────────────────────────────────────────────────────────────┐
│                       Final Evaluation                          │
│                                                                 │
│  ┌─────────────┐              ┌─────────────┐                  │
│  │   Judge 1   │    Debate    │   Judge 2   │                  │
│  │  (Quality)  │ ←──────────→ │(Completeness│                  │
│  └──────┬──────┘              └──────┬──────┘                  │
│         │                            │                          │
│         └────────────┬───────────────┘                          │
│                      ▼                                          │
│             ┌─────────────────┐                                 │
│             │  Vote / Decide  │                                 │
│             │  Final Winner   │                                 │
│             └─────────────────┘                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Inputs:**
- All candidate Markmaps
- All round summaries

**Evaluation Criteria:**
- Structure quality
- Knowledge completeness
- Readability
- Practicality

### Phase 5: Final Output

- Convert selected Markmap to `markmap.html`
- Other versions saved as historical records (optional)

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

### Requirements

```
langgraph>=1.0.4
langchain>=0.3.0
langchain-openai>=0.2.0
langchain-anthropic>=0.2.0
langchain-community>=0.3.0
chromadb>=0.4.0
pyyaml>=6.0
tiktoken>=0.5.0
```

---

## Configuration

All settings are managed in `config/config.yaml`:

```yaml
# ===== Model Configuration =====
models:
  generalist:
    en: "gpt-4-turbo"
    zh: "gpt-4-turbo"
  specialist:
    en: "gpt-4-turbo"
    zh: "gpt-4-turbo"
  optimizer:
    - model: "gpt-4-turbo"
      prompt_path: "prompts/optimizer_structure.txt"
    - model: "claude-3-opus"
      prompt_path: "prompts/optimizer_semantic.txt"
  summarizer:
    model: "gpt-4-turbo"
    prompt_path: "prompts/summarizer.txt"
  judges:
    - model: "gpt-4-turbo"
      prompt_path: "prompts/judge_quality.txt"
    - model: "claude-3-opus"
      prompt_path: "prompts/judge_completeness.txt"
  compressor:
    model: "gpt-3.5-turbo"

# ===== Workflow Configuration =====
workflow:
  optimization_rounds: 3
  optimizer_count: 3
  judge_count: 2
  max_tokens_before_compress: 8000

# ===== Memory Configuration =====
memory:
  stm_enabled: true
  ltm_enabled: true
  ltm_vector_store: "chromadb"
  ltm_collection_name: "markmap_decisions"

# ===== Output Configuration =====
output:
  save_intermediate: true
  intermediate_dir: "outputs/intermediate"
  final_dir: "outputs/final"
```

---

## Usage

### Basic Usage

```python
from src.graph import build_markmap_graph

# Build the graph
graph = build_markmap_graph()

# Prepare initial input
initial_state = {
    "metadata": your_metadata_dict,
    "ontology": your_ontology_dict,
}

# Run the workflow
result = graph.invoke(
    initial_state,
    config={"configurable": {"thread_id": "session-1"}}
)

# Access results
print(result["final_selection"])  # Final Markmap
print(result["final_html"])       # HTML output path
```

### CLI Usage

```bash
python main.py --metadata data/metadata.json --ontology data/ontology.json
```

---

## Agent Capabilities

Each Optimizer/Debater agent implements these cognitive modules:

### 🧠 Planning
- Define optimization goals (structure, hierarchy, naming, abstraction level)

### 🧩 Subgoal & Decomposition
- Break down Markmap improvements into:
  - Node structure
  - Classification hierarchy
  - Semantic consistency
  - Engineering readability

### 🔁 Reflection & Refinement
- Evaluate previous round results
- Adjust strategies to avoid repeated mistakes

### 🧠 Memory System

| Type | Scope | Implementation |
|------|-------|----------------|
| **STM** | Current round dialogue, current Markmap state | In-memory dict |
| **LTM** | Optimization principles, historical decisions | Vector Store (ChromaDB) |

---

## Memory System

### Short-Term Memory (STM)

Maintains context within the current session:
- Current round dialogue
- Current Markmap state
- Recent decisions

### Long-Term Memory (LTM)

Persists across sessions using Vector Store:
- Optimization principles
- Historical decision summaries
- Retrieved via semantic search for relevant context

```python
# LTM Query Example
relevant_decisions = query_ltm(
    query="How to structure algorithm complexity nodes?",
    k=5
)
```

---

## Project Structure

```
ai-markmap-agent/
├── config/
│   └── config.yaml              # Global configuration
├── prompts/
│   ├── generalist_en.txt        # Generalist prompt (EN)
│   ├── generalist_zh.txt        # Generalist prompt (ZH)
│   ├── specialist_en.txt        # Specialist prompt (EN)
│   ├── specialist_zh.txt        # Specialist prompt (ZH)
│   ├── optimizer_structure.txt  # Structure optimizer prompt
│   ├── optimizer_semantic.txt   # Semantic optimizer prompt
│   ├── optimizer_readability.txt# Readability optimizer prompt
│   ├── summarizer.txt           # Summarizer prompt
│   ├── judge_quality.txt        # Quality judge prompt
│   └── judge_completeness.txt   # Completeness judge prompt
├── src/
│   ├── __init__.py
│   ├── config_loader.py         # Configuration loader
│   ├── state.py                 # State definition (TypedDict)
│   ├── graph.py                 # Main Graph construction
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py        # Base agent class
│   │   ├── generator.py         # Generalist/Specialist generators
│   │   ├── optimizer.py         # Optimizer/Debater agents
│   │   ├── summarizer.py        # Summarizer agent
│   │   └── judge.py             # Judge/Evaluator agents
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── stm.py               # Short-term memory
│   │   └── ltm.py               # Long-term memory (Vector Store)
│   ├── compression/
│   │   └── compressor.py        # Long content compression
│   └── output/
│       └── html_converter.py    # Markmap → HTML converter
├── outputs/
│   ├── intermediate/            # Intermediate artifacts
│   └── final/                   # Final output
├── tests/
│   └── ...                      # Test files
├── requirements.txt
├── main.py                      # Entry point
├── README.md                    # This file
└── README_zh-TW.md             # 繁體中文文件
```

---

## Module Responsibilities

| Module | Lines | Responsibility |
|--------|-------|----------------|
| `config_loader.py` | ~50 | Load and validate YAML configuration |
| `state.py` | ~60 | Define shared state TypedDict |
| `graph.py` | ~150 | Build LangGraph StateGraph |
| `generator.py` | ~120 | Generalist/Specialist Markmap generation |
| `optimizer.py` | ~200 | Optimization, planning, reflection |
| `summarizer.py` | ~80 | Round summarization |
| `judge.py` | ~150 | Final evaluation and voting |
| `stm.py` | ~40 | Short-term memory operations |
| `ltm.py` | ~100 | Long-term memory with Vector Store |
| `compressor.py` | ~60 | Content compression/summarization |
| `html_converter.py` | ~50 | Markmap MD → HTML conversion |

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python -m pytest tests/ -q`
5. Submit a pull request

---

## Related

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
- [Markmap](https://markmap.js.org/)


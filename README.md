# 🧩 NeetCode Practice Framework

<!-- 
SEO: leetcode, algorithm, data structure, coding interview, FAANG, competitive programming, neetcode, 
     blind 75, python, mind map, pattern, dynamic programming, interview preparation, knowledge graph
AEO/GEO: A scalable Python framework with knowledge graph-driven learning, AI-powered mind maps,
         industrial-strength testing, and pattern-based learning for algorithm mastery.
-->

[![GitHub stars](https://img.shields.io/github/stars/lufftw/neetcode?style=for-the-badge&logo=github&color=gold)](https://github.com/lufftw/neetcode/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/lufftw/neetcode?style=for-the-badge&logo=github&color=silver)](https://github.com/lufftw/neetcode/network)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](https://github.com/lufftw/neetcode/blob/main/LICENSE)

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/GPT--Powered-412991?style=flat-square&logo=openai&logoColor=white)](https://openai.com/)
[![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?style=flat-square&logo=visual-studio-code&logoColor=white)](https://code.visualstudio.com/)
[![pytest](https://img.shields.io/badge/150%2B%20Tests-0A9EDC?style=flat-square&logo=pytest&logoColor=white)](https://github.com/lufftw/neetcode/tree/main/.dev/tests)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=flat-square&logo=git&logoColor=white)](https://github.com/lufftw/neetcode/pulls)

---

**Solve. Forget. Repeat. Let’s Fix That.**

### 🎯 Build Algorithmic Intuition

**NeetCode is a scalable Python practice framework for algorithm learning and interview prep — build intuition and pattern recognition, turn ideas into clean implementations, and accumulate *verifiable evidence* (tests, stress cases, benchmarks, complexity checks) so your progress is real, repeatable, and interview-ready.**

- **Learn the transferable skills**: modeling, state/invariants, edge cases, complexity awareness, and reusable solution templates.
- **Interview-ready practice**: time-boxed workflows, explain-while-coding, fewer “small bugs”, stronger trade-off discussions.
- **Prove correctness & robustness**: static + seeded random + edge-case stress tests, custom judges, failure reproduction.
- **Measure and compare**: benchmark multiple implementations and empirically estimate complexity.
- **See the big picture**: ontology + AI mind maps reveal pattern relationships and learning paths.

[📚 Docs](https://lufftw.github.io/neetcode/) • [🧪 Testing & Validation](docs/runner/README.md) • [🤖 AI Mind Maps](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode-ontology-agent-evolved-en.html) • [🧠 Interactive Mind Maps](https://lufftw.github.io/neetcode/mindmaps/) • [🚀 Quick Start](#-quick-start) • [📐 Patterns](docs/patterns/README.md)

[English](https://lufftw.github.io/neetcode/) | [繁體中文](https://lufftw.github.io/neetcode/index_zh-TW/)

---

**Topics:** `knowledge-graph` `ai-powered` `mind-map` `pattern-recognition` `leetcode` `neetcode-150` `blind-75` `stress-testing` `algorithm-engineering` `performance-benchmarking` `data-driven-testing` `random-test-generation` `judge-function` `algorithm-debugging` `competitive-programming` `python` `vscode-integration` `test-automation` `pre-commit` `local-automation` `coding-interview`

---

## 💎 Core Philosophy

> **"Algorithm mastery is not about memorizing 300 solutions — it's about internalizing 15 fundamental patterns and knowing precisely when to apply each one."**

This framework embodies three transformative principles:

### 🧬 Knowledge Graph Architecture

Traditional LeetCode practice treats problems as isolated units. We built an **interconnected ontology system** where:

- **API Kernels** define reusable algorithmic primitives (`SubstringSlidingWindow`, `GridBFS`, `BacktrackExplore`)
- **Patterns** compose kernels into higher-level strategies
- **Problem Families** reveal structural relationships across 300+ problems
- **AI Synthesis** discovers non-obvious connections humans miss

*This is how experts think — in abstractions, not in solutions.*

### ⚙️ Production-Grade Validation

Your solution passes LeetCode's tests. But is it *correct*? Is it *optimal*? We provide **ICPC/Codeforces-caliber testing infrastructure**:

| Capability | What It Proves |
|:-----------|:---------------|
| 🎲 **Seeded Random Generation** | Your code handles cases you never imagined |
| ⚖️ **Custom Judge Functions** | Multiple valid answers are all accepted |
| 📊 **Multi-Solution Benchmarking** | Which approach is *actually* faster |
| 📈 **Empirical Complexity Estimation** | Your O(n log n) claim is verified |

*This is how Google engineers validate — through exhaustive, reproducible testing.*

### 🤖 AI-Augmented Understanding

We don't just store knowledge — we **synthesize insight**:

- AI analyzes the entire ontology to generate **creative, interconnected mind maps**
- Multi-perspective synthesis: Architect × Professor × Engineer × Competitor
- Problems link to **GitHub solutions** (when available) or **LeetCode** (fallback)

*This is how the next generation learns — with AI as a thinking partner.*

---

## 🌟 What Sets Us Apart

> 💡 **"Great algorithmic skill isn’t about finding an answer — it’s about building systems that make correctness, performance, and learning provable."**

| 📦 Other LeetCode Repos | 🚀 NeetCode |
|:------------------------|:------------|
| ❌ Binary feedback ("Accepted / Wrong") | 🧩 **Evidence-driven loop**: golden tests + seeded fuzz + edge-case stress |
| ❌ Single solution, unknown behavior | 🧩 **Multiple implementations** + side-by-side benchmarks |
| ❌ Flat, tag-only pattern labels | 🧩 **Interactive mind maps** linking problems, patterns, and kernels |
| ❌ No AI-assisted discovery | 🤖 **AI-powered connections** across related problems, patterns, and approaches |
| ❌ Patterns limited to static notes | 🧠 **Dual learning paths per pattern:** intuition-driven explanations for mental models, plus reusable templates for interviews and fast recall |
| ❌ Manual runs, inconsistent environments | ⚙️ **Deterministic CLI + VS Code tasks/debug** |
| ❌ "Accepted" without proof | 🔍 **Invariant-aware solutions** + explicit failure modes |
| ❌ Ad-hoc edge cases | 🧠 **Systematic edge-case taxonomy** |
| ❌ Solution-first memorization | 🧠 **Pattern-first transfer learning** (interview-ready) |
| ❌ Big-O as documentation only | 📊 **Measured time / space trade-offs** under identical inputs |
| ❌ Complexity claimed, not verified | 📊 **Complexity + empirical benchmarks** under identical conditions |
| ❌ Results hard to reproduce | ⚙️ **Deterministic, reproducible experiments** |
| ❌ Flat problem collection | 🧩 **Skill & pattern progression tracking** |
| ❌ Silent failures | 🔍 **Auto-captured counterexamples** for debugging |
| ❌ Human-written notes only | 🤖 **AI-augmented reasoning layer** (summaries, maps, kernels) |

<sub>

**Legend — Capability Categories**  
🧠 Learning & reasoning layer  
🧩 System architecture & structure  
⚙️ Execution & tooling infrastructure  
📊 Empirical measurement & benchmarks  
🔍 Debugging & correctness analysis  
🤖 AI-assisted augmentation  

</sub>


### 🧠 The Knowledge Graph Advantage

Most people practice algorithms in isolation. We built an **interconnected knowledge system**:

| Mind Map | Description | Link |
|:---------|:------------|:----:|
| 🤖 **AI Ontology Analysis (Evolved)** | Generated via a multi-agent pipeline | [🔗 EN](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode-ontology-agent-evolved-en.html) · [🔗 中文](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode-ontology-agent-evolved-zh-tw.html) |
| 🤖 **AI Ontology Analysis** | AI-powered deep pattern synthesis | [🔗 EN](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode-ontology-ai-en.html) · [🔗 中文](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode-ontology-ai-zh-tw.html) |
| 📐 **Pattern Hierarchy** | API kernels → patterns → solutions | [🔗](https://lufftw.github.io/neetcode/pages/mindmaps/pattern-hierarchy.html) |
| 👨‍👩‍👧‍👦 **Family Derivation** | Base templates → derived variants | [🔗](https://lufftw.github.io/neetcode/pages/mindmaps/family-derivation.html) |
| ⚡ **Algorithm Usage** | Know which algorithm applies where | [🔗](https://lufftw.github.io/neetcode/pages/mindmaps/algorithm-usage.html) |
| 🏢 **Company Coverage** | Target preparation for specific companies | [🔗](https://lufftw.github.io/neetcode/pages/mindmaps/company-coverage.html) |
| 🗺️ **Learning Roadmaps** | NeetCode 150, Blind 75, etc. | [🔗](https://lufftw.github.io/neetcode/pages/mindmaps/roadmap-paths.html) |

**[→ Explore 10+ Interactive Mind Maps](https://lufftw.github.io/neetcode/mindmaps/)**

### ⚙️ Industrial-Strength Testing

Built on principles from **Codeforces, ICPC, and Google's engineering practices**:

| Capability | What It Does | Why It Matters |
|:-----------|:-------------|:---------------|
| 🎲 **Random Test Generation** | Seeded generators for reproducibility | Find edge cases you never imagined |
| ⚖️ **Custom Judge Functions** | ICPC-style validation logic | Multiple correct answers? No problem |
| 📊 **Multi-Solution Benchmark** | Compare N approaches automatically | Know which is *actually* faster |
| 📈 **Complexity Estimation** | Empirical Big-O analysis | Verify your theoretical claims |
| 🔧 **VS Code Integration** | One-click debug, tasks, shortcuts | Debug algorithms like real software |

---

## 📑 Table of Contents

- [What Sets Us Apart](#-what-sets-us-apart)
- [Why This Framework?](#-why-this-framework)
- [Quick Start](#-quick-start)
- [Key Features](#-key-features)
- [Interactive Mind Maps](#-interactive-mind-maps)
- [AI Mind Map Generation](#-ai-mind-map-generation)
- [Pattern Documentation](#-pattern-documentation)
- [Usage Guide](#-usage-guide)
- [Advanced Features](#-advanced-features)
- [Project Architecture](#-project-architecture)
- [FAQ](#-frequently-asked-questions)
- [For Contributors](#-for-contributors)
- [License](#-license)

---

## ⭐ Why This Framework?

### The Problem with Traditional Practice

You solve a problem on LeetCode. It passes. But do you *really* know if your solution is correct? What about:

- That edge case with empty input you didn't test?
- The subtle off-by-one error that only appears with large N?
- Whether your O(n log n) claim is actually true?

**Traditional practice leaves these questions unanswered.** This framework answers them definitively.

### What Makes Us Different

| Capability | This Framework | Typical Repos |
|:-----------|:-------------:|:-------------:|
| **Reproducible Random Tests** | ✅ Seeded generators | ❌ Manual only |
| **Custom Judge Functions** | ✅ ICPC/Codeforces style | ❌ String match |
| **Multi-Solution Benchmarking** | ✅ Compare N approaches | ❌ Single solution |
| **VS Code Integration** | ✅ Tasks, Debug, Shortcuts | ❌ CLI only |
| **Stress Testing** | ✅ Generate 1000+ cases | ❌ Limited |
| **Complexity Estimation** | ✅ Automatic Big-O | ❌ None |

### Built For Excellence

| Audience | How We Help |
|:---------|:------------|
| 🏆 **Competitive Programmers** | Train like Codeforces grandmasters — stress test until you break your code, then fix it |
| 💼 **FAANG Engineers** | Build interview confidence by proving your solutions work, not just hoping they do |
| 🎓 **CS Students** | Learn algorithms the right way — through experimentation, not memorization |
| 👨‍🏫 **Educators** | Give students industrial-grade tools to validate their understanding |
| 🔬 **Researchers** | Benchmark algorithm variants at scale with reproducible methodology |

---

## 🚀 Quick Start

### 1. Setup Environment

#### Windows (PowerShell)

```powershell
# Clone and navigate to project
cd C:\path\to\neetcode

# Install Python 3.11 (if needed)
py install 3.11

# Create and activate virtual environment
py -3.11 -m venv leetcode
leetcode\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Linux / macOS

```bash
# Using pyenv (recommended)
pyenv install 3.11
pyenv local 3.11

# Create and activate virtual environment
python -m venv leetcode
source leetcode/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make scripts executable
chmod +x scripts/run_tests.sh scripts/run_case.sh scripts/new_problem.sh
```

### 2. Create Your First Problem

```bash
# Windows
scripts\new_problem.bat 1
scripts\new_problem.bat 1 --with-tests

# Linux/macOS
./scripts/new_problem.sh 1
./scripts/new_problem.sh 1 --with-tests
```

📖 **Guide**: [Create New Problem](docs/guides/new-problem.md) (wrapper + flags + tiered behavior)

This creates:
- `solutions/0001_two_sum.py` — Your solution file
- `tests/0001_two_sum_1.in/.out` — Example-based tests (when `--with-tests`)

**New options:**

```bash
# New flags
scripts\new_problem.bat 1 --solve-mode tiered  # Use tiered solve() + codec generation
scripts\new_problem.bat 1 --header-level minimal  # Shorter header (optional)
scripts\new_problem.bat 1 --codec-mode import  # Override codec mode for tiered generation
scripts\new_problem.bat 1 --codec-mode inline  # Override codec mode for tiered generation (embed codec)

# Auto-detect (no need to specify --solve-mode)
scripts\new_problem.bat 104  # Tree problems → auto tiered codec + solve()
scripts\new_problem.bat 142  # Linked list cycle problems → auto tiered codec + solve()
```

📖 **Guide**: [Create Practice File](docs/guides/new-practice.md) (generate/refresh `practices/` from reference)

**More CodeGen commands (optional):**

```bash
# Check whether your existing tests match LeetCode examples
python -m codegen check 1
python -m codegen check --all --limit 10

# Migrate tests to canonical JSON-literal format (preview first)
python -m codegen migrate 1 --dry-run
python -m codegen migrate --all --dry-run
```

> 📖 Full reference: [`docs/packages/codegen/README.md`](docs/packages/codegen/README.md)

### 3. Run Tests

```bash
# Windows
scripts\run_tests.bat 0001_two_sum

# Linux/macOS
./scripts/run_tests.sh 0001_two_sum
```

### 4. Debug in VS Code

1. Open any solution file in `solutions/`
2. Press `F5` to debug with test case #1
3. Or press `Ctrl+Shift+B` to run all tests

**That's it!** You're ready to solve problems. 🎉

---

## ✨ Key Features

| Feature | Description |
|:--------|:------------|
| 🧪 **Testing & Validation Engine** | ⭐ **Core Feature** — Automated testing, benchmarking, random test generation, complexity estimation. See [Testing & Validation Guide](docs/runner/README.md) |
| 🧰 **One-Command Scaffolding (CodeGen)** | Create a full problem scaffold from a LeetCode ID: `solutions/*.py` + optional example tests (`tests/*.in/.out`) + auto `solve()` generation. For problems with **non-trivial input/output adapters** (e.g. trees, linked lists, cycles), CodeGen can **auto-detect** and generate a tiered codec-based `solve()` (`--solve-mode tiered`). See [CodeGen Docs](docs/packages/codegen/README.md). |
| 🧾 **Canonical Test Contract + Migration** | Test files use **JSON literal, one value per line** for diff-friendly, machine-stable I/O. Includes `check` (consistency vs LeetCode examples) and `migrate` (auto-convert existing tests) workflows. See [`docs/contracts/test-file-format.md`](docs/contracts/test-file-format.md). |
| 🧠 **Memory Profiling (Optional)** | Runner can show **memory traces and rankings** across methods (`--memory-trace`, `--trace-compare`, `--memory-per-case`) when optional deps are installed. See [Runner Spec](docs/runner/README.md). |
| 🤖 **AI Ontology Analysis** | AI-powered knowledge graph synthesis — discover pattern relationships humans miss |
| 🎲 **Random Test Generation** | Seeded generators for reproducibility, stress test with 1000+ cases, auto-save failing cases |
| ⚖️ **Custom Judge Functions** | Validate multiple correct answers, ICPC-style validation, works without expected output |
| 📊 **Performance Analysis** | Benchmark multiple solutions, automatic time complexity estimation, side-by-side comparison |
| 🔧 **VS Code Integration** | One-click test execution, integrated debugging, custom tasks and shortcuts |
| 🧠 **Interactive Mind Maps** | Visualize algorithm patterns, track learning progress — [Explore →](https://lufftw.github.io/neetcode/mindmaps/) |

---

## 🧠 Interactive Mind Maps

Visualize algorithm patterns, problem relationships, and learning paths:

### 🤖 AI-Powered Ontology Analysis (NEW!)

> **"Let AI synthesize what takes humans years to internalize."**

Our **AI Ontology Analyzer** processes the entire knowledge graph — API Kernels, Patterns, Algorithms, Data Structures, Problem Families — and generates **creative, interconnected mind maps** that reveal insights human-curated lists miss.

| Language | Description | Links |
|:---------|:------------|:------|
| **English (Evolved)** | Generated via a multi-agent pipeline | [Static](docs/mindmaps/neetcode-ontology-agent-evolved-en.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode-ontology-agent-evolved-en.html) |
| **繁體中文 (Evolved)** | 由多代理（multi-agent）流程產生 | [Static](docs/mindmaps/neetcode-ontology-agent-evolved-zh-tw.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode-ontology-agent-evolved-zh-tw.html) |
| **English** | AI-synthesized pattern relationships | [Static](docs/mindmaps/neetcode-ontology-ai-en.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode-ontology-ai-en.html) |
| **繁體中文** | AI 智能分析模式關聯 | [Static](docs/mindmaps/neetcode-ontology-ai-zh-tw.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode-ontology-ai-zh-tw.html) |

**What makes it special:**
- 🧬 **Deep Pattern Synthesis** — AI identifies non-obvious connections between patterns
- 🎯 **Smart Linking** — Problems link to GitHub solutions (when available) or LeetCode
- 🌐 **Multi-language** — Generate in English and 繁體中文
- ♻️ **Regeneratable** — Run `python tools/mindmaps/generate_mindmaps_ai.py` to create fresh insights

---

### 📚 Curated Mind Maps

| Mind Map | Description | Links |
|:---------|:------------|:------|
| 📐 **Pattern Hierarchy** | API Kernels → Patterns → Problems | [Static](docs/mindmaps/pattern-hierarchy.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/pattern-hierarchy.html) |
| 👨‍👩‍👧‍👦 **Family Derivation** | Base templates → Derived variants | [Static](docs/mindmaps/family-derivation.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/family-derivation.html) |
| ⚡ **Algorithm Usage** | Problems by algorithm | [Static](docs/mindmaps/algorithm-usage.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/algorithm-usage.html) |
| 🏗️ **Data Structure Usage** | Problems by data structure | [Static](docs/mindmaps/data-structure.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/data-structure.html) |
| 🏢 **Company Coverage** | Company-specific problems | [Static](docs/mindmaps/company-coverage.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/company-coverage.html) |
| 🗺️ **Learning Roadmaps** | NeetCode 150, Blind 75, etc. | [Static](docs/mindmaps/roadmap-paths.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/roadmap-paths.html) |
| 🔗 **Problem Relations** | Related problems network | [Static](docs/mindmaps/problem-relations.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/problem-relations.html) |
| 🔀 **Solution Variants** | Multiple approaches | [Static](docs/mindmaps/solution-variants.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/solution-variants.html) |
| 📊 **Difficulty × Topics** | Topics by difficulty | [Static](docs/mindmaps/difficulty-topics.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/difficulty-topics.html) |

👉 **[View All Interactive Mind Maps](https://lufftw.github.io/neetcode/mindmaps/)**

---

## 🤖 AI Mind Map Generation

> **"Let AI synthesize what takes humans years to internalize."**

### Two Generation Modes

| Mode | Description | Quick Start |
|:-----|:------------|:------------|
| **🤖 Evolved Agent** | Multi-expert refinement with consensus voting | `cd tools/mindmaps/ai-markmap-agent && python main.py` |
| **🤖 Basic AI** | Single-pass synthesis from knowledge graph | `python tools/mindmaps/generate_mindmaps_ai.py` |

### Key Features

- 🧬 **Multi-Expert Synthesis** — Architect + Professor + Engineer perspectives
- 🎯 **Smart Linking** — GitHub solution (if exists) → LeetCode fallback
- 🌐 **Multi-language** — EN / 繁體中文
- ♻️ **Regeneratable** — Version history with auto-increment

### Output Files

| Type | Output Path |
|:-----|:------------|
| **Evolved (Markdown)** | `docs/mindmaps/neetcode-ontology-agent-evolved-{lang}.md` (`{lang}` = `en` or `zh-tw`) |
| **Basic (Markdown)** | `docs/mindmaps/neetcode-ontology-ai-{lang}.md` (`{lang}` = `en` or `zh-tw`) |
| **HTML** | `docs/pages/mindmaps/*.html` |

> 📖 **Evolved Agent**: See [`tools/mindmaps/ai-markmap-agent/README.md`](docs/tools/mindmaps/ai-markmap-agent/README.md) for architecture, expert roles, and configuration.
>
> 📖 **Basic AI**: See [`tools/README.md`](docs/tools/README.md) for configuration options.

---

## 📐 Pattern Documentation

> **"Don't memorize 200 problems. Master 10 patterns."**

Each pattern provides **two learning paths**:

| Path | Purpose | Best For |
|:-----|:--------|:---------|
| 💡 **Intuition** | Understand the "why" through stories and visual explanations | First-time learners, building mental models |
| 🛠️ **Templates** | Production-ready implementations with problem-specific variations | Interview prep, quick reference |

| API Kernel | Learning Resources | Problems |
|:-----------|:-------------------|:---------|
| `SubstringSlidingWindow` | 💡 [Intuition](docs/patterns/sliding_window/intuition.md) · 🛠️ [Templates](docs/patterns/sliding_window/templates.md) | LeetCode 3, 76, 159, 209, 340, 438, 567 |
| `TwoPointersTraversal` | 💡 [Intuition](docs/patterns/two_pointers/intuition.md) · 🛠️ [Templates](docs/patterns/two_pointers/templates.md) | LeetCode 1, 11, 15, 16, 21, 26, 27, 75, 88, 125, 141, 142, 167, 202, 283, 680, 876 |
| `BinarySearchBoundary` | 💡 [Intuition](docs/patterns/binary_search/intuition.md) · 🛠️ [Templates](docs/patterns/binary_search/templates.md) | LeetCode 33, 34, 35, 81, 162, 875, 1011 |
| `BacktrackingExploration` | 💡 [Intuition](docs/patterns/backtracking_exploration/intuition.md) · 🛠️ [Templates](docs/patterns/backtracking_exploration/templates.md) | LeetCode 39, 40, 46, 47, 51, 77, 78, 79, 90, 93, 131, 216 |
| `MonotonicStack` | 💡 [Intuition](docs/patterns/monotonic_stack/intuition.md) · 🛠️ [Templates](docs/patterns/monotonic_stack/templates.md) | LeetCode 42, 84, 85, 316, 321, 402, 496, 503, 739, 901, 907, 2104 |
| `PrefixSum` | 💡 [Intuition](docs/patterns/prefix_sum/intuition.md) · 🛠️ [Templates](docs/patterns/prefix_sum/templates.md) | LeetCode 238, 303, 304, 523, 525, 560, 1094, 1109 |
| `Heap` | 💡 [Intuition](docs/patterns/heap/intuition.md) · 🛠️ [Templates](docs/patterns/heap/templates.md) | LeetCode 23, 215, 253, 295, 347, 621, 1046 |
| `GraphTraversal` | 💡 [Intuition](docs/patterns/graph/intuition.md) · 🛠️ [Templates](docs/patterns/graph/templates.md) | LeetCode 133, 200, 417, 785, 841, 994, 1971 |
| `IntervalMerge` | 💡 [Intuition](docs/patterns/interval/intuition.md) · 🛠️ [Templates](docs/patterns/interval/templates.md) | LeetCode 56, 57, 435, 452, 986 |
| `UnionFind` | 💡 [Intuition](docs/patterns/union_find/intuition.md) · 🛠️ [Templates](docs/patterns/union_find/templates.md) | LeetCode 547, 684, 721, 990, 1319 |
| `TreeTraversal` | 💡 [Intuition](docs/patterns/tree/intuition.md) · 🛠️ [Templates](docs/patterns/tree/templates.md) | LeetCode 94, 102, 104, 110, 124, 543 |
| `TopologicalSort` | 💡 [Intuition](docs/patterns/topological_sort/intuition.md) · 🛠️ [Templates](docs/patterns/topological_sort/templates.md) | LeetCode 207, 210, 802, 1203 |
| `ShortestPath` | 💡 [Intuition](docs/patterns/shortest_path/intuition.md) · 🛠️ [Templates](docs/patterns/shortest_path/templates.md) | LeetCode 743, 787, 1368, 1631, 2290 |
| `Trie` | 💡 [Intuition](docs/patterns/trie/intuition.md) · 🛠️ [Templates](docs/patterns/trie/templates.md) | LeetCode 208, 211, 212, 648, 1268 |
| `GreedyCore` | 💡 [Intuition](docs/patterns/greedy_core/intuition.md) · 🛠️ [Templates](docs/patterns/greedy_core/templates.md) | LeetCode 55, 45, 134, 135, 455, 1029 |
| `DP1DLinear` | 💡 [Intuition](docs/patterns/dp_1d_linear/intuition.md) · 🛠️ [Templates](docs/patterns/dp_1d_linear/templates.md) | LeetCode 70, 198, 213, 121, 746 |
| `DPKnapsackSubset` | 💡 [Intuition](docs/patterns/dp_knapsack_subset/intuition.md) · 🛠️ [Templates](docs/patterns/dp_knapsack_subset/templates.md) | LeetCode 416, 494, 322, 518 |
| `MathNumberTheory` | 💡 [Intuition](docs/patterns/math_number_theory/intuition.md) · 🛠️ [Templates](docs/patterns/math_number_theory/templates.md) | LeetCode 1979, 204, 168 |
| `SegmentTreeFenwick` | 💡 [Intuition](docs/patterns/segment_tree_fenwick/intuition.md) · 🛠️ [Templates](docs/patterns/segment_tree_fenwick/templates.md) | LeetCode 307, 315, 327 |
| `LineSweep` | 💡 [Intuition](docs/patterns/line_sweep/intuition.md) · 🛠️ [Templates](docs/patterns/line_sweep/templates.md) | LeetCode 253, 1094, 218 |
| `GridBFSMultiSource` | *coming soon* | LeetCode 994, 286, 542 |
| `KWayMerge` | *coming soon* | LeetCode 23, 21, 88 |
| `LinkedListInPlaceReversal` | *coming soon* | LeetCode 25, 206, 92 |

👉 **[View All Pattern Guides →](docs/patterns/README.md)**

---

## 📖 Usage Guide

### ⌨️ VS Code Integration

**Keyboard Shortcuts:**

| Shortcut | Action |
|:---------|:-------|
| `Ctrl+Shift+B` | Run all tests for current file |
| `F5` | Debug with test case #1 |

> **Note:** Open a solution file in `solutions/` before using shortcuts.

**Common Tasks** (`Ctrl+Shift+P` → "Tasks: Run Task"):

| Task | Description |
|:-----|:------------|
| Run all tests | Execute all test cases |
| Run case #1 / #2 / #3 | Run specific test case |
| Benchmark | Show execution times |
| Run all solutions | Compare all implementations |
| Run with generated (10) | Static + 10 generated cases |

> 📖 **Complete Reference**: See [VSCode Setup Guide](docs/contributors/vscode-setup.md) for all 14 tasks, 11 debug configurations, workflow examples, and customization.

### 💻 Command Line Interface

> 📖 **Complete Reference**: See [Testing & Validation Guide](docs/runner/README.md) for full CLI options, usage examples, and advanced features. This is the **core testing engine** that powers automated testing, benchmarking, random test generation, and complexity estimation.

```bash
# Run all test cases
python runner/test_runner.py <problem_name>

# Run specific test case
python runner/case_runner.py <problem_name> <case_number>

# Run with benchmarking
python runner/test_runner.py <problem_name> --benchmark

# Run all solutions
python runner/test_runner.py <problem_name> --all

# Generate random tests
python runner/test_runner.py <problem_name> --generate 10

# Estimate time complexity
python runner/test_runner.py <problem_name> --estimate

# Memory profiling (optional)
python runner/test_runner.py <problem_name> --memory-trace
python runner/test_runner.py <problem_name> --all --trace-compare

# Save failing generated cases for reproduction
python runner/test_runner.py <problem_name> --generate 100 --seed 12345 --save-failed
```

**Optional runner dependencies (enable extra features):**

```bash
pip install big-O psutil sparklines tabulate
```

### 📝 Solution File Format

```python
# solutions/0001_two_sum.py
from typing import List
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "twoSum",
        "complexity": "O(n) time, O(n) space",
        "description": "Single pass with hash map",
    },
}

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []

def solve():
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')
    
    # Parse input
    # Canonical format: JSON literal, one value per line
    nums = json.loads(lines[0])
    target = json.loads(lines[1])
    
    # Run solution (polymorphic dispatch)
    solver = get_solver(SOLUTIONS)
    result = solver.twoSum(nums, target)
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    solve()
```

> 📖 See [`docs/contracts/solution-contract.md`](docs/contracts/solution-contract.md) for the complete specification.

### 📋 Test File Format

| Specification | Requirement |
|:--------------|:------------|
| Line Ending | **LF** (Unix format, `\n`) |
| Encoding | UTF-8 |
| File Ending | Single newline at end |
| Naming | `{number}_{name}_{case}.in/.out` |

**Input file** (`tests/0001_two_sum_1.in`):
```
[2,7,11,15]
9
```

**Output file** (`tests/0001_two_sum_1.out`):
```
[0,1]
```

> 📖 Full contract: [`docs/contracts/test-file-format.md`](docs/contracts/test-file-format.md)

---

## 🔧 Advanced Features

### 🚀 Multi-Solution Benchmarking

Compare multiple approaches for the same problem using the **polymorphic pattern**:

```python
# solutions/0215_kth_largest_element_in_an_array.py
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionQuickselect",
        "method": "findKthLargest",
        "complexity": "O(n) average time, O(1) space",
        "description": "Quickselect algorithm with random pivot",
    },
    "quickselect": {
        "class": "SolutionQuickselect",
        "method": "findKthLargest",
        "complexity": "O(n) average time, O(1) space",
        "description": "Quickselect algorithm with random pivot",
    },
    "heap": {
        "class": "SolutionHeap",
        "method": "findKthLargest",
        "complexity": "O(n log k) time, O(k) space",
        "description": "Min-heap of size k",
    },
}

class SolutionQuickselect:
    def findKthLargest(self, nums, k):
        # Quickselect implementation
        pass

class SolutionHeap:
    def findKthLargest(self, nums, k):
        # Heap implementation
        pass

def solve():
    # ... parse input ...
    solver = get_solver(SOLUTIONS)
    result = solver.findKthLargest(nums, k)
    print(result)
```

**Run commands:**

```bash
# Run specific solution
python runner/test_runner.py 0215_kth_largest_element_in_an_array --method heap

# Compare all solutions
python runner/test_runner.py 0215_kth_largest_element_in_an_array --all --benchmark
```

**Output:**

```text
   ╔════════════════════════════════════════════════════╗
   ║ 0215_kth_largest_element_in_an_array - Performance ║
   ╠════════════════════════════════════════════════════╣
   ║ default:     ████████████████░░░░  166ms           ║
   ║ quickselect: █████████████████░░░  170ms           ║
   ║ heap:        ████████████████████  224ms           ║
   ╚════════════════════════════════════════════════════╝

======================================================================
Performance Comparison (Details)
======================================================================

Method         Avg Time   Pass Rate  Complexity    Peak RSS     P95 RSS
-----------  ----------  ----------  --------------------  ----------  ----------
default        166.01ms         3/3  O(n) average time, O(1) space       4.2MB       4.2MB
quickselect    170.13ms         3/3  O(n) average time, O(1) space       4.2MB       4.2MB
heap           224.22ms         3/3  O(n log k) time, O(k) space       4.2MB       4.2MB

======================================================================
```

> **Note:** The `Complexity` column is **declared metadata** from `SOLUTIONS`. If you want empirical estimation, use `--estimate` (requires `big-O` + `generate_for_complexity(n)`).

Create with: `scripts\new_problem.bat 215` (then add more entries to `SOLUTIONS` if you want multiple approaches).

> 📖 See [`docs/contracts/solution-contract.md`](docs/contracts/solution-contract.md#solutions-metadata) for complete SOLUTIONS schema and validation rules.

### 🔀 Flexible Output Validation

For problems with multiple valid answers ("return in any order"):

**Validation Modes:**

| Mode | Description | Requires `.out` |
|:-----|:------------|:---------------:|
| `[judge]` | Custom validation with reference | ✅ |
| `[judge-only]` | Custom validation only | ❌ |
| `[exact]` | Exact string match | ✅ |
| `[sorted]` | Sort before comparison | ✅ |
| `[set]` | Set comparison | ✅ |

**JUDGE_FUNC (Recommended):**

```python
def judge(actual: list, expected, input_data: str) -> bool:
    """Validate N-Queens solution."""
    n = int(input_data.strip())
    
    # Validate each board
    for board in actual:
        if not is_valid_n_queens(board, n):
            return False
    
    # Check count if expected exists
    if expected is not None:
        return len(actual) == len(expected)
    
    return True

JUDGE_FUNC = judge
```

**COMPARE_MODE (Simple Cases):**

```python
COMPARE_MODE = "sorted"  # Options: "exact" | "sorted" | "set"
```

> 📖 See [`docs/contracts/solution-contract.md`](docs/contracts/solution-contract.md#validation-judge_func--compare_mode) for complete JUDGE_FUNC signature and validation rules.

### 🎲 Random Test Generation

Create a generator file with the same name as your solution:

```python
# generators/0004_median_of_two_sorted_arrays.py
import random
from typing import Iterator, Optional

def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases."""
    import json
    if seed is not None:
        random.seed(seed)
    
    # Edge cases first
    yield "[]\n[1]"
    yield "[1]\n[]"
    
    # Random cases
    for _ in range(count - 2):
        m = random.randint(0, 1000)
        n = random.randint(0, 1000)
        nums1 = sorted(random.randint(-10**6, 10**6) for _ in range(m))
        nums2 = sorted(random.randint(-10**6, 10**6) for _ in range(n))
        yield f"{json.dumps(nums1, separators=(',', ':'))}\n{json.dumps(nums2, separators=(',', ':'))}"
```

**Usage:**

```bash
# Run static + generated tests
python runner/test_runner.py 0004_median --generate 10

# Only generated tests
python runner/test_runner.py 0004_median --generate-only 100

# Reproducible with seed
python runner/test_runner.py 0004_median --generate 10 --seed 42

# Save failing cases
python runner/test_runner.py 0004_median --generate 10 --save-failed
```

> 📖 See [`docs/contracts/generator-contract.md`](docs/contracts/generator-contract.md) for complete generator specification and best practices.

### 📈 Time Complexity Estimation

Add a complexity generator function:

```python
# generators/0004_median_of_two_sorted_arrays.py

def generate_for_complexity(n: int) -> str:
    """Generate test case with specific size n."""
    m = random.randint(0, n)
    return _generate_case(m, n - m)
```

**Run estimation:**

```bash
python runner/test_runner.py 0004_median --estimate
```

**Output:**

```
📈 Running complexity estimation...
   Sizes: [10, 20, 50, 100, 200, 500, 1000, 2000]
   n=   10: 0.0040ms
   n=  100: 0.0082ms
   n= 1000: 0.0685ms
   n= 2000: 0.1796ms

✅ Estimated: O(n log n)
   Confidence: 1.00
```

---

## 📁 Project Architecture

```
neetcode/
│
├── solutions/                 # 📝 Your solution files
│   └── 0001_two_sum.py
│
├── practices/                 # 🧠 Practice workspace (generated practice files + history)
│   └── _history/...
│
├── tests/                     # 📋 Test cases
│   ├── 0001_two_sum_1.in      # Input file
│   ├── 0001_two_sum_1.out     # Expected output
│   └── *_failed_*.in          # Auto-saved failed cases (--save-failed)
│
├── generators/                # 🎲 Random test generators (optional)
│   └── 0001_two_sum.py        # generate(count, seed) function
│
├── src/                       # 📦 Core packages (CodeGen, datasource, practice workspace)
│   ├── codegen/               # `python -m codegen ...`
│   ├── leetcode_datasource/   # LeetCode metadata/source
│   └── practice_workspace/    # Practice history utilities
│
├── config/                    # ⚙️ Living registries / policies
│   └── problem-support.yaml   # Problem support boundary (tiers/codec hints, etc.)
│
├── runner/                    # 🧪 Core testing & validation engine
│   ├── test_runner.py         # CLI entry point & main orchestration
│   ├── case_runner.py         # Single case runner (for debugging)
│   ├── executor.py            # Test case execution (subprocess) [legacy]
│   ├── compare.py             # Output comparison (exact/sorted/set/judge) [legacy]
│   ├── reporter.py            # Result formatting & benchmark display [legacy]
│   ├── module_loader.py       # Dynamic module loading
│   ├── complexity_estimator.py # Time complexity estimation (big_O)
│   ├── paths.py               # Path utilities
│   ├── io_utils.py            # File I/O operations
│   ├── util.py                # Re-exports (backward compatible)
│   ├── solution_parser.py     # Solution file parsing
│   ├── memory_profiler.py     # Memory profiling utilities
│   ├── method_runner.py       # Method-level execution [legacy]
│   ├── analysis/              # Analysis modules
│   │   ├── complexity.py      # Complexity analysis
│   │   ├── input_scale.py     # Input scale analysis
│   │   ├── input_shape.py     # Input shape analysis
│   │   ├── memory_profiler.py # Memory profiling
│   │   ├── shape_protocol.py  # Shape protocol definitions
│   │   └── type_shape.py       # Type shape analysis
│   ├── core/                  # Core execution modules
│   │   ├── executor.py        # Test case execution (subprocess)
│   │   └── method_runner.py   # Method-level execution
│   ├── display/               # Display & reporting modules
│   │   ├── benchmark.py       # Benchmark display
│   │   ├── memory.py          # Memory display
│   │   └── reporter.py        # Result formatting & benchmark display
│   ├── utils/                 # Utility modules
│   │   ├── codec/             # Codec utilities (list_node, tree_node, etc.)
│   │   ├── compare.py         # Output comparison
│   │   ├── loader.py          # Module loading utilities
│   │   ├── parser.py          # Parsing utilities
│   │   └── paths.py           # Path utilities
│   └── README.md              # Quick reference guide
│
│   📖 See [Testing & Validation Guide](docs/runner/README.md) — Core engine for automated testing, benchmarking, random test generation, and complexity estimation
│
├── templates/                 # 📄 Problem templates
│   ├── template_solution.py       # Single solution template
│   ├── template_solution_multi.py # Multi-solution (polymorphic)
│   └── template_test.txt          # Test case template
│
├── .vscode/                   # 🔧 VS Code integration
│   ├── settings.json          # Python environment settings
│   ├── tasks.json             # Ctrl+Shift+B shortcuts (14 tasks)
│   └── launch.json            # F5 debug configurations (11 configs)
│
│   📖 See [VSCode Setup Guide](docs/contributors/vscode-setup.md) — Tasks, debug configs, workflow examples
│
├── docs/                      # 📚 Documentation (MkDocs)
│   ├── index.md               # Homepage (English)
│   ├── index_zh-TW.md         # Homepage (繁體中文)
│   ├── architecture/          # Architecture documentation
│   │   ├── README.md          # Architecture overview
│   │   ├── architecture-migration.md  # Architecture migration guide
│   │   └── packages-overview.md  # Packages overview
│   ├── contracts/             # Contract specifications
│   │   ├── codec.md          # Codec contract
│   │   ├── documentation-header-spec.md  # Documentation header spec
│   │   ├── generator-contract.md  # Generator contract
│   │   ├── problem-support-boundary.md  # Problem support boundary
│   │   ├── solution-contract.md  # Solution contract
│   │   └── test-file-format.md  # Test file format
│   ├── contributors/          # Maintainer documentation
│   │   ├── README.md          # Full maintainer guide
│   │   ├── docs-directory-organization.md  # Docs directory organization
│   │   ├── documentation-architecture.md  # Documentation structure
│   │   ├── documentation-naming.md  # Documentation naming convention
│   │   ├── package-documentation-strategy.md  # Package documentation strategy
│   │   ├── testing.md         # Complete testing documentation
│   │   ├── virtual-env-setup.md  # Virtual environment setup
│   │   └── vscode-setup.md    # VS Code tasks & debug configs
│   ├── guides/                # User guides
│   │   ├── act-local-github-actions.md  # Run GitHub Actions locally
│   │   ├── build-docs-manual.md  # Build docs manually
│   │   ├── github-pages-setup.md  # GitHub Pages setup
│   │   ├── local-docs-build.md  # Local docs build options
│   │   ├── mkdocs-content-guide.md  # MkDocs content guide
│   │   ├── new-practice.md    # Create practice file
│   │   └── new-problem.md     # Create new problem
│   ├── in-progress/           # Work in progress documentation
│   │   ├── README.md          # In-progress docs overview
│   │   ├── new-problem-tests-autogen/  # Test autogen migration
│   │   └── tiered-problem-generation/  # Tiered generation spec
│   ├── mindmaps/              # Generated mind map markdown
│   │   ├── index.md          # Mind maps overview
│   │   ├── algorithm-usage.md
│   │   ├── company-coverage.md
│   │   ├── data-structure.md
│   │   ├── difficulty-topics.md
│   │   ├── family-derivation.md
│   │   ├── neetcode-ontology-agent-evolved-en.md
│   │   ├── neetcode-ontology-agent-evolved-zh-tw.md
│   │   ├── neetcode-ontology-ai-en.md
│   │   ├── neetcode-ontology-ai-zh-tw.md
│   │   ├── pattern-hierarchy.md
│   │   ├── problem-relations.md
│   │   ├── roadmap-paths.md
│   │   └── solution-variants.md
│   ├── packages/              # Package documentation (for src/ packages)
│   │   ├── codegen/           # CodeGen package docs
│   │   ├── leetcode_datasource/  # LeetCode datasource docs
│   │   └── practice_workspace/  # Practice workspace docs
│   ├── patterns/              # Generated pattern documentation
│   │   ├── README.md          # Patterns overview
│   │   ├── backtracking_exploration/
│   │   ├── sliding_window/
│   │   └── two_pointers/
│   ├── pages/                 # Generated HTML (gitignored)
│   │   ├── assets/           # HTML assets
│   │   └── mindmaps/         # Interactive mind map HTML
│   ├── reference/             # Reference documentation
│   │   └── ontology-design.md  # Ontology design
│   ├── runner/                # Runner documentation
│   │   ├── README.md          # Runner overview
│   │   ├── cli-output-contract.md  # CLI output contract
│   │   ├── benchmarking/     # Benchmarking docs
│   │   │   └── memory-metrics.md
│   │   └── profiling/        # Profiling docs
│   │       ├── cli-output-memory.md
│   │       └── input-scale-metrics.md
│   ├── tools/                 # Tools documentation
│   │   ├── README.md          # Complete tools reference
│   │   ├── docstring/        # Docstring tools
│   │   ├── leetcode-api/     # LeetCode API tools
│   │   ├── maintenance/      # Maintenance tools
│   │   ├── mindmaps/         # Mind maps tools
│   │   │   ├── README.md     # Mind maps generator docs
│   │   └── ai-markmap-agent/  # AI Markmap Agent docs
│   │   ├── patterndocs/      # Pattern docs generator
│   │   └── review-code/      # Code review tools
│   ├── assets/                # Documentation assets (images, CSS, JS)
│   │   └── document_dates/   # Document date assets
│   ├── authors.yml            # Author information
│   └── robots.txt             # Robots.txt for SEO
│
├── tools/                     # 🛠️ Utility scripts
│   ├── mindmaps/              # 🗺️ Mind map tools (all integrated)
│   │   ├── core/              # Core modules
│   │   ├── ai-markmap-agent/  # 🤖 AI Markmap Agent (multi-agent pipeline)
│   │   ├── ai_mindmap/        # AI mind map modules
│   │   ├── hooks/             # Git hooks
│   │   ├── prompts/           # AI prompts
│   │   ├── shared/            # Shared utilities
│   │   ├── tests/             # Tests
│   │   ├── generate_mindmaps.py       # Rule-based generator (entry)
│   │   ├── generate_mindmaps_ai.py    # AI generator (entry)
│   │   ├── generate_mindmaps.toml     # Rule-based configuration
│   │   ├── generate_mindmaps_ai.toml  # AI configuration
│   │   ├── sync_mindmap_html.py       # Sync HTML
│   │   ├── text_to_mindmap.py         # Text to mindmap
│   │   └── html_meta_description_generator.py  # SEO meta descriptions
│   ├── patterndocs/           # 📚 Pattern documentation generator
│   │   └── generate_pattern_docs.py   # Entry script
│   ├── review-code/           # 🔍 Code review & validation
│   │   └── validation/        # Validation tools
│   │       ├── check_solutions.py
│   │       ├── check_test_files.py
│   │       └── run_format_tests.py
│   ├── docstring/             # 📝 Docstring tools
│   ├── leetcode-api/          # 🔗 LeetCode API
│   │   └── crawler/           # Crawler tools
│   ├── maintenance/           # 🔧 Maintenance tools
│   │   └── doc-naming/        # Documentation naming tools
│   └── _staging/              # 📦 Staging area (to be organized)
│
├── ontology/                  # 🧬 Algorithm ontology (TOML)
│   ├── api_kernels.toml       # API kernel definitions
│   ├── patterns.toml          # Pattern definitions
│   ├── algorithms.toml        # Algorithm definitions
│   ├── data_structures.toml   # Data structure definitions
│   ├── companies.toml         # Company definitions
│   ├── topics.toml            # Topic definitions
│   ├── difficulties.toml      # Difficulty levels
│   ├── families.toml          # Problem family definitions
│   └── roadmaps.toml          # Roadmap definitions
│
├── meta/                      # 📊 Problem & pattern metadata
│   ├── problems/              # Problem metadata (one TOML per problem)
│   │   └── *.toml
│   └── patterns/              # Pattern documentation sources
│       └── <pattern_name>/    # Pattern-specific markdown
│
├── roadmaps/                  # 🗺️ Learning path definitions
│   ├── neetcode_150.toml
│   ├── blind_75.toml
│   └── sliding_window_path.toml
│
├── .dev/                      # 🧪 Maintainer zone (unit tests)
│   ├── tests/                 # Unit test suite (150+ cases)
│   ├── tests_solutions/       # Solution validation tests
│   ├── scripts/run_tests.bat/.sh  # Run runner unit tests
│   ├── run_all_tests.bat/.sh  # Run all unit tests
│   ├── run_tests_solutions.bat/.sh  # Run solution tests
│   ├── testing.md             # Testing documentation
│   ├── virtual-env-setup.md   # Virtual environment guide
│   └── README.md              # Maintainer guide
│
├── .github/                   # 🚀 GitHub configuration
│   └── workflows/
│       └── deploy-pages.yml   # GitHub Pages deployment
│
├── leetcode/                  # 🐍 Python virtual environment (3.11)
│
├── scripts/                   # 🔧 Utility scripts
│   ├── new_problem.bat / .sh  # Create new problem (wrapper around codegen)
│   ├── run_tests.bat / .sh    # Run all tests for a problem
│   ├── run_case.bat / .sh     # Run single test case
│   └── build_docs.bat / .sh   # Build documentation site
│
├── mkdocs_plugins/            # 🔌 MkDocs plugins
│   └── mindmaps_lastmod.py    # Last modified date plugin
│
├── requirements.txt           # Python dependencies
├── pyproject.toml             # Project configuration
├── mkdocs.yml                 # MkDocs configuration
├── pytest.ini                 # pytest configuration
├── README.md                  # This file (English)
└── README_zh-TW.md            # 繁體中文版
```

### Directory Guide

| Directory | Purpose | Target Audience |
|:----------|:--------|:----------------|
| `solutions/` | Write your solutions here | ✅ All users |
| `practices/` | Practice workspace (generated practice files + history) | ✅ All users |
| `tests/` | Add test cases (.in/.out) | ✅ All users |
| `generators/` | Random test generators | ✅ All users |
| `runner/` | Test execution engine | 🔧 Contributors |
| `packages/` | Core packages (CodeGen, datasource, practice workspace) | 🔧 Contributors |
| `config/` | Problem support registry & policy | 🔧 Contributors |
| `templates/` | Problem templates | ✅ All users |
| `.vscode/` | VS Code configuration | ✅ All users |
| `docs/` | MkDocs documentation | 🔧 Contributors |
| `tools/` | Documentation generators | 🔧 Contributors |
| `ontology/` | Algorithm ontology data | 🔧 Contributors |
| `meta/` | Problem/pattern metadata | 🔧 Contributors |
| `.dev/` | Unit tests (150+ cases) | 🔧 Maintainers |

> **📝 Note:** Files in `docs/mindmaps/`, `docs/patterns/`, and `docs/pages/` are auto-generated. Edit the source files in `ontology/`, `meta/`, and `tools/` instead.

### Documentation Guide

Documentation is organized by **target audience**:

| Location | Purpose | Audience |
|:---------|:--------|:---------|
| `docs/` | User documentation (published to website) | ✅ Users |
| `tools/README.md` | Developer tools reference | 🔧 Contributors |
| `tools/*/README.md` | Module technical details | 🔧 Contributors |
| `.dev/` | Maintainer documentation | 🔧 Maintainers |

**Key Documentation Files:**

| Document | Description |
|:---------|:------------|
| [`docs/contracts/solution-contract.md`](docs/contracts/solution-contract.md) | Solution file specification |
| [`docs/contracts/generator-contract.md`](docs/contracts/generator-contract.md) | Generator file specification |
| [`docs/contracts/test-file-format.md`](docs/contracts/test-file-format.md) | Canonical `.in`/`.out` format (JSON literal, one value per line) |
| [`docs/contracts/codec.md`](docs/contracts/codec.md) | Codec contract (import/inline helpers, semantics) |
| [`docs/contracts/problem-support-boundary.md`](docs/contracts/problem-support-boundary.md) | Problem support boundary & hard rules |
| [`docs/packages/codegen/README.md`](docs/packages/codegen/README.md) | CodeGen reference (new/practice/check/migrate) |
| [`docs/runner/README.md`](docs/runner/README.md) | Runner spec (CLI options, memory profiling, output format) |
| [`docs/tools/README.md`](docs/tools/README.md) | Complete tools reference |
| [`docs/contributors/README.md`](docs/contributors/README.md) | Maintainer guide |
| [`docs/contributors/documentation-naming.md`](docs/contributors/documentation-naming.md) | Documentation naming convention (kebab-case) |
| [`docs/contributors/documentation-architecture.md`](docs/contributors/documentation-architecture.md) | Documentation structure |

---

## ❓ Frequently Asked Questions

**What problems does this framework solve?**

- Running multiple algorithm implementations automatically
- Generating reproducible random test data for stress testing
- Benchmarking solutions to identify performance differences
- Debugging LeetCode-style problems with VS Code integration
- Validating outputs using custom logic beyond simple file comparison

**How is this different from copying LeetCode solutions?**

This is not a solution collection — it's a **testing infrastructure**. You write solutions, and the framework:

1. Runs them against static test cases
2. Generates random test cases automatically
3. Validates correctness using custom judge functions
4. Benchmarks multiple solutions against each other
5. Estimates time complexity empirically

**Can I use this for interview preparation?**

Absolutely! The framework is perfect for interview prep:

- Practice writing solutions in **real LeetCode format**
- Find **edge cases you might miss** with random test generation
- See which approach is **actually faster** with benchmarking
- **Debug easily** with VS Code integration

**What Python version is required?**

Python 3.11 — matching the [LeetCode official environment](https://support.leetcode.com/hc/en-us/articles/360011833974-What-are-the-environments-for-the-programming-languages).

---

## 🛠️ For Contributors

### Running Unit Tests

```bash
# Activate virtual environment
leetcode\Scripts\activate  # Windows
source leetcode/bin/activate  # Linux/macOS

# Run all tests
python -m pytest .dev/tests -v

# With coverage
python -m pytest .dev/tests --cov=runner --cov-report=html
```

### Generate Mind Maps Locally

**AI-Powered (Recommended):**

```bash
# Interactive mode
python tools/mindmaps/generate_mindmaps_ai.py

# With specific goal
python tools/mindmaps/generate_mindmaps_ai.py --goal interview

# Generate multiple languages
# Edit tools/mindmaps/generate_mindmaps_ai.toml: language = ["en", "zh-TW"]
python tools/mindmaps/generate_mindmaps_ai.py
```

Configuration: `tools/mindmaps/generate_mindmaps_ai.toml`

**Rule-Based:**

```bash
# Generate Markdown mind maps
python tools/mindmaps/generate_mindmaps.py

# Generate HTML (interactive) mind maps
python tools/mindmaps/generate_mindmaps.py --html
```

Configuration: `tools/mindmaps/generate_mindmaps.toml`

### Build Documentation Locally

> ⚠️ **Optional Feature:** Building documentation locally is **completely optional**. Core LeetCode practice functionality works without any documentation build setup.

**Recommended Method (Simple):**

The easiest way to build documentation locally is using the manual scripts:

```bash
# Windows
scripts\build_docs.bat

# Linux/macOS
./scripts/build_docs.sh

# Build and preview locally
scripts\build_docs.bat --serve  # Windows
./scripts/build_docs.sh --serve  # Linux/macOS
```

📖 **See [Building Documentation Locally (Manual Method)](docs/guides/build-docs-manual.md)** for complete guide.

**Advanced Option (Optional):**

If you want to test the exact GitHub Actions workflow locally, you can use `act`:

📖 **See [Running GitHub Actions Locally with Act](docs/guides/act-local-github-actions.md)** — *Note: Requires Docker and act tool. Only needed if you want to test CI/CD workflows.*

### Documentation

**Core Documentation:**
- [`docs/contributors/README.md`](docs/contributors/README.md) — Maintainer guide
- [`docs/contributors/testing.md`](docs/contributors/testing.md) — Testing documentation
- [`docs/contributors/vscode-setup.md`](docs/contributors/vscode-setup.md) — VS Code tasks, debug configurations, workflow examples
- [`docs/contributors/documentation-naming.md`](docs/contributors/documentation-naming.md) — Docs naming convention (kebab-case)
- [`docs/contracts/solution-contract.md`](docs/contracts/solution-contract.md) — Solution file specification (SOLUTIONS dict, JUDGE_FUNC)
- [`docs/contracts/generator-contract.md`](docs/contracts/generator-contract.md) — Generator file specification (generate(), edge cases, complexity)
- [`docs/contracts/test-file-format.md`](docs/contracts/test-file-format.md) — Canonical `.in`/`.out` format (JSON literal, one value per line)
- [`docs/contracts/codec.md`](docs/contracts/codec.md) — Codec contract (import/inline helpers, semantics)
- [`docs/contracts/problem-support-boundary.md`](docs/contracts/problem-support-boundary.md) — Problem support boundary & hard rules
- [`docs/packages/codegen/README.md`](docs/packages/codegen/README.md) — CodeGen reference (new/practice/check/migrate)
- [`docs/guides/new-problem.md`](docs/guides/new-problem.md) — How to create a new problem skeleton (`new_problem`)
- [`docs/guides/new-practice.md`](docs/guides/new-practice.md) — How to generate/refresh practice files (`new_practice`)
- [`docs/runner/README.md`](docs/runner/README.md) — Test runner spec (CLI options, memory profiling, output format)
- [`docs/architecture/architecture-migration.md`](docs/architecture/architecture-migration.md) — Polymorphic architecture migration guide

**Local Documentation Build (Optional):**
- [`docs/guides/build-docs-manual.md`](docs/guides/build-docs-manual.md) — ⭐ **Recommended:** Simple manual build method
- [`docs/guides/act-local-github-actions.md`](docs/guides/act-local-github-actions.md) — Advanced: Test CI/CD workflows locally with act (requires Docker)

**Deployment:**
- [`docs/guides/github-pages-setup.md`](docs/guides/github-pages-setup.md) — Deployment guide

---

## 📜 License

**MIT License** — Free for personal learning and educational use.

---

**Built with ❤️ for the competitive programming community**

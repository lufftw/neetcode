# 🧩 NeetCode Practice Framework

<!-- 
SEO: leetcode, algorithm, data structure, coding interview, FAANG, competitive programming, neetcode, 
     blind 75, python, mind map, pattern, dynamic programming, interview preparation, knowledge graph
AEO/GEO: A scalable Python framework with knowledge graph-driven learning, AI-powered mind maps,
         industrial-strength testing, and pattern-based learning for algorithm mastery.
-->

[![GitHub stars](https://img.shields.io/github/stars/lufftw/neetcode?style=for-the-badge&logo=github&color=gold)](https://github.com/lufftw/neetcode/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/lufftw/neetcode?style=for-the-badge&logo=github&color=silver)](https://github.com/lufftw/neetcode/network)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/GPT--Powered-412991?style=flat-square&logo=openai&logoColor=white)](https://openai.com/)
[![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?style=flat-square&logo=visual-studio-code&logoColor=white)](https://code.visualstudio.com/)
[![pytest](https://img.shields.io/badge/150%2B%20Tests-0A9EDC?style=flat-square&logo=pytest&logoColor=white)](https://github.com/lufftw/neetcode/tree/main/.dev/tests)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=flat-square&logo=git&logoColor=white)](https://github.com/lufftw/neetcode/pulls)

---

### 🎯 Stop Memorizing. Start Engineering.

**A scalable Python framework that transforms LeetCode-style algorithm practice into a knowledge-graph-driven, data-driven, testable, and high-performance workflow — with AI-powered mind maps, industrial-strength testing, and pattern-based learning to help developers grow faster and understand algorithms more deeply.**

[📚 Docs](https://lufftw.github.io/neetcode/) • [🤖 AI Mind Maps](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode_ontology_ai_en.html) • [🧠 Interactive Mind Maps](https://lufftw.github.io/neetcode/mindmaps/) • [🚀 Quick Start](#-quick-start) • [📐 Patterns](docs/patterns/)

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

> 💡 **"The difference between a good programmer and a great one isn't the algorithm they choose — it's how they prove it works."**

| 📦 Other LeetCode Repos | 🚀 NeetCode |
|:------------------------|:------------|
| ❌ Copy solutions, hope they work | ✅ **Prove** your solution is correct |
| ❌ Manual test cases only | ✅ Auto-generate 1000+ test cases |
| ❌ No way to compare approaches | ✅ Benchmark N solutions side-by-side |
| ❌ Memorize patterns blindly | ✅ **Visualize** patterns with mind maps |
| ❌ No systematic learning path | ✅ Structured roadmaps (NeetCode 150, Blind 75) |

### 🧠 The Knowledge Graph Advantage

Most people practice algorithms in isolation. We built an **interconnected knowledge system**:

| Mind Map | Description | Link |
|:---------|:------------|:----:|
| 🤖 **AI Ontology Analysis** | AI-powered deep pattern synthesis | [🔗 EN](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode_ontology_ai_en.html) · [🔗 中文](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode_ontology_ai_zh-TW.html) |
| 📐 **Pattern Hierarchy** | API kernels → patterns → solutions | [🔗](https://lufftw.github.io/neetcode/pages/mindmaps/pattern_hierarchy.html) |
| 👨‍👩‍👧‍👦 **Family Derivation** | Base templates → derived variants | [🔗](https://lufftw.github.io/neetcode/pages/mindmaps/family_derivation.html) |
| ⚡ **Algorithm Usage** | Know which algorithm applies where | [🔗](https://lufftw.github.io/neetcode/pages/mindmaps/algorithm_usage.html) |
| 🏢 **Company Coverage** | Target preparation for specific companies | [🔗](https://lufftw.github.io/neetcode/pages/mindmaps/company_coverage.html) |
| 🗺️ **Learning Roadmaps** | NeetCode 150, Blind 75, etc. | [🔗](https://lufftw.github.io/neetcode/pages/mindmaps/roadmap_paths.html) |

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

<details>
<summary><strong>Windows (PowerShell)</strong></summary>

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

</details>

<details>
<summary><strong>Linux / macOS</strong></summary>

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

</details>

### 2. Create Your First Problem

```bash
# Windows
scripts\new_problem.bat 0001_two_sum

# Linux/macOS
./scripts/new_problem.sh 0001_two_sum
```

This creates:
- `solutions/0001_two_sum.py` — Your solution file
- `tests/0001_two_sum_1.in` — Test input
- `tests/0001_two_sum_1.out` — Expected output

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
| 🤖 **AI Ontology Analysis** | AI-powered knowledge graph synthesis — discover pattern relationships humans miss |
| 🧪 **Automated Testing** | Run multiple test cases automatically with clear pass/fail reporting and timing |
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
| **English** | AI-synthesized pattern relationships | [Static](docs/mindmaps/neetcode_ontology_ai_en.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode_ontology_ai_en.html) |
| **繁體中文** | AI 智能分析模式關聯 | [Static](docs/mindmaps/neetcode_ontology_ai_zh-TW.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode_ontology_ai_zh-TW.html) |

**What makes it special:**
- 🧬 **Deep Pattern Synthesis** — AI identifies non-obvious connections between patterns
- 🎯 **Smart Linking** — Problems link to GitHub solutions (when available) or LeetCode
- 🌐 **Multi-language** — Generate in English and 繁體中文
- ♻️ **Regeneratable** — Run `python tools/generate_mindmaps_ai.py` to create fresh insights

---

### 📚 Curated Mind Maps

| Mind Map | Description | Links |
|:---------|:------------|:------|
| 📐 **Pattern Hierarchy** | API Kernels → Patterns → Problems | [Static](docs/mindmaps/pattern_hierarchy.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/pattern_hierarchy.html) |
| 👨‍👩‍👧‍👦 **Family Derivation** | Base templates → Derived variants | [Static](docs/mindmaps/family_derivation.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/family_derivation.html) |
| ⚡ **Algorithm Usage** | Problems by algorithm | [Static](docs/mindmaps/algorithm_usage.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/algorithm_usage.html) |
| 🏗️ **Data Structure Usage** | Problems by data structure | [Static](docs/mindmaps/data_structure.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/data_structure.html) |
| 🏢 **Company Coverage** | Company-specific problems | [Static](docs/mindmaps/company_coverage.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/company_coverage.html) |
| 🗺️ **Learning Roadmaps** | NeetCode 150, Blind 75, etc. | [Static](docs/mindmaps/roadmap_paths.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/roadmap_paths.html) |
| 🔗 **Problem Relations** | Related problems network | [Static](docs/mindmaps/problem_relations.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/problem_relations.html) |
| 🔀 **Solution Variants** | Multiple approaches | [Static](docs/mindmaps/solution_variants.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/solution_variants.html) |
| 📊 **Difficulty × Topics** | Topics by difficulty | [Static](docs/mindmaps/difficulty_topics.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/difficulty_topics.html) |

👉 **[View All Interactive Mind Maps](https://lufftw.github.io/neetcode/mindmaps/)**

---

## 🤖 AI Mind Map Generation

> **"The synthesis of a Software Architect's system thinking, an Algorithm Professor's pedagogical wisdom, a Principal Engineer's battle-tested experience, and a Competitive Programming Champion's pattern recognition — all unified through AI."**

### The Vision

Traditional algorithm learning resources present knowledge in isolation. Our **AI Ontology Analyzer** takes a fundamentally different approach:

| Traditional Approach | Our AI Approach |
|:---------------------|:----------------|
| Static problem lists | Dynamic knowledge graph synthesis |
| Manual categorization | AI-discovered pattern relationships |
| Single perspective | Multi-perspective expert synthesis |
| Memorize solutions | Understand interconnections |

### How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    KNOWLEDGE GRAPH INPUT                        │
├─────────────────────────────────────────────────────────────────┤
│  ontology/          │  meta/problems/     │  docs/patterns/     │
│  ├── api_kernels    │  ├── 0001_*.toml    │  ├── sliding_window │
│  ├── patterns       │  ├── 0003_*.toml    │  └── ...            │
│  ├── algorithms     │  └── ...            │                     │
│  └── ...            │                     │                     │
└─────────────────────┴─────────────────────┴─────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AI SYNTHESIS ENGINE                          │
├─────────────────────────────────────────────────────────────────┤
│  🏗️ Software Architect    → System-level pattern organization   │
│  📚 Algorithm Professor   → Pedagogical structure & progression │
│  ⚙️ Principal Engineer    → Practical applicability & trade-offs│
│  🏆 Competitive Champion  → Pattern recognition shortcuts       │
│  🎨 API Designer          → Clean knowledge interfaces          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INTELLIGENT OUTPUT                           │
├─────────────────────────────────────────────────────────────────┤
│  ✅ Smart Links: GitHub solution (if exists) → LeetCode fallback│
│  ✅ Multi-language: EN / 繁體中文 / 简体中文                      │
│  ✅ Markmap format: Interactive, collapsible, beautiful         │
│  ✅ Custom goals: Interview prep / Systematic learning / Review │
└─────────────────────────────────────────────────────────────────┘
```

### Quick Start

```bash
# Interactive mode (recommended)
python tools/generate_mindmaps_ai.py

# Specific goals
python tools/generate_mindmaps_ai.py --goal interview        # Interview preparation
python tools/generate_mindmaps_ai.py --goal systematic       # Learning roadmap
python tools/generate_mindmaps_ai.py --goal pattern_mastery  # Deep pattern analysis

# Focus on specific topic
python tools/generate_mindmaps_ai.py --topic sliding_window
python tools/generate_mindmaps_ai.py --topic dynamic_programming

# Multiple languages
# Configure in tools/mindmap_ai_config.toml:
# language = ["en", "zh-TW"]
```

### 🔄 Automatic Generation (Local CI/CD)

**Auto-generate AI mind maps on commit** using pre-commit hooks:

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

When you commit changes to `ontology/`, `meta/problems/`, or `tools/generate_mindmaps.py`, the hook automatically runs AI mind map generation.

**Skip when needed:**
```bash
# Skip with commit message
git commit -m "Update ontology [skip-ai]"

# Skip with environment variable
SKIP_AI_MINDMAPS=true git commit -m "Update ontology"
```

> 📖 See [tools/README.md](tools/README.md#-local-cicd-automation) for complete setup and usage guide.

### Configuration

Edit `tools/mindmap_ai_config.toml` to customize:

| Section | What You Can Configure |
|:--------|:-----------------------|
| `[model]` | LLM model, temperature, max tokens |
| `[output]` | Directory, filename, HTML generation |
| `[ontology]` | Which knowledge graph data to include |
| `[problems]` | Problem filters (difficulty, topics, roadmaps) |
| `[generation]` | Goal, style, custom instructions |
| `[links]` | GitHub repo URL, branch, link format |
| `[advanced]` | Output language(s), complexity inclusion |

### The Intelligence Behind It

The AI doesn't just reorganize data — it **synthesizes understanding** from multiple expert perspectives:

| Perspective | Contribution to Mind Map |
|:------------|:-------------------------|
| 🏗️ **Software Architect** | Identifies abstraction layers, sees patterns as reusable components |
| 📚 **Algorithm Professor** | Structures learning progression, explains "why" not just "how" |
| ⚙️ **Principal Engineer** | Highlights production trade-offs, real-world applicability |
| 🏆 **Competitive Champion** | Surfaces pattern-matching shortcuts, time-pressure optimizations |
| 🎨 **API Designer** | Creates clean knowledge interfaces, consistent naming |
| 👥 **Open Source Advocate** | Makes knowledge discoverable, contribution-friendly |

### Output Examples

**With Solution (links to GitHub):**
```markdown
- [LeetCode 3 - Longest Substring Without Repeating](https://github.com/lufftw/neetcode/blob/main/solutions/0003_longest_substring_without_repeating_characters.py)
```

**Without Solution (links to LeetCode):**
```markdown
- [LeetCode 121 - Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)
```

### No API Key? No Problem

The generator saves the complete prompt to `tools/prompts/generated/mindmap_prompt.md`. Copy and paste it into ChatGPT, Claude, or any LLM web interface.

---

## 📐 Pattern Documentation

> **"Don't memorize 200 problems. Master 10 patterns."**

Each API Kernel has a dedicated pattern guide with **base template**, **variations**, and **copy-paste ready code**.

| API Kernel | Guide | Problems |
|:-----------|:-----:|:---------|
| `SubstringSlidingWindow` | [📖](docs/patterns/sliding_window.md) | LeetCode 3, 76, 159, 209, 340, 438, 567 |
| `TwoPointersTraversal` | [📖](docs/patterns/two_pointers.md) | LeetCode 1, 11, 15, 16, 21, 26, 27, 75, 88, 125, 141, 142, 167, 202, 283, 680, 876 |
| `GridBFSMultiSource` | *soon* | LeetCode 994, 286, 542 |
| `BacktrackingExploration` | *soon* | LeetCode 51, 52, 46, 78 |
| `KWayMerge` | *soon* | LeetCode 23, 21, 88 |
| `BinarySearchBoundary` | *soon* | LeetCode 4, 33, 34, 35 |

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

**Available Tasks** (`Ctrl+Shift+P` → "Tasks: Run Task"):

| Task | Description |
|:-----|:------------|
| Run all tests | Execute all test cases |
| Run case #1 / #2 / #3 | Run specific test case |
| Benchmark | Show execution times |
| Run all solutions | Compare all implementations |
| Run with generated (10) | Static + 10 generated cases |
| Run generated only | Skip static tests |
| Save failed cases | Auto-save failing inputs |

### 💻 Command Line Interface

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
    lines = sys.stdin.read().strip().split('\n')
    
    # Parse input
    nums = list(map(int, lines[0].split(',')))
    target = int(lines[1])
    
    # Run solution (polymorphic dispatch)
    solver = get_solver(SOLUTIONS)
    result = solver.twoSum(nums, target)
    print(result)

if __name__ == "__main__":
    solve()
```

> 📖 See [`docs/SOLUTION_CONTRACT.md`](docs/SOLUTION_CONTRACT.md) for the complete specification.

### 📋 Test File Format

| Specification | Requirement |
|:--------------|:------------|
| Line Ending | **LF** (Unix format, `\n`) |
| Encoding | UTF-8 |
| File Ending | Single newline at end |
| Naming | `{number}_{name}_{case}.in/.out` |

**Input file** (`tests/0001_two_sum_1.in`):
```
2,7,11,15
9
```

**Output file** (`tests/0001_two_sum_1.out`):
```
[0, 1]
```

---

## 🔧 Advanced Features

### 🚀 Multi-Solution Benchmarking

Compare multiple approaches for the same problem using the **polymorphic pattern**:

```python
# solutions/0023_merge_k_sorted_lists.py
from _runner import get_solver

SOLUTIONS = {
    "default": {
        "class": "SolutionHeap",
        "method": "mergeKLists",
        "complexity": "O(N log k)",
        "description": "Min Heap approach"
    },
    "divide": {
        "class": "SolutionDivideConquer",
        "method": "mergeKLists",
        "complexity": "O(N log k)",
        "description": "Divide and Conquer"
    },
    "greedy": {
        "class": "SolutionGreedy",
        "method": "mergeKLists",
        "complexity": "O(kN)",
        "description": "Greedy comparison"
    },
}

class SolutionHeap:
    def mergeKLists(self, lists):
        # Heap implementation
        pass

class SolutionDivideConquer:
    def mergeKLists(self, lists):
        # Divide & Conquer implementation
        pass

class SolutionGreedy:
    def mergeKLists(self, lists):
        # Greedy implementation
        pass

def solve():
    # ... parse input ...
    solver = get_solver(SOLUTIONS)
    result = solver.mergeKLists(lists)
    print(result)
```

**Run commands:**

```bash
# Run specific solution
python runner/test_runner.py 0023_merge_k_sorted_lists --method heap

# Compare all solutions
python runner/test_runner.py 0023_merge_k_sorted_lists --all --benchmark
```

**Output:**

```
============================================================
📊 Performance Comparison
============================================================
Method               Avg Time     Complexity      Pass Rate
------------------------------------------------------------
heap                    44.36ms   O(N log k)      3/3
divide                  44.48ms   O(N log k)      3/3
greedy                  44.82ms   O(kN)           3/3
============================================================
```

Create with template: `scripts\new_problem.bat 0023_merge_k_lists --multi`

> 📖 See [`docs/SOLUTION_CONTRACT.md` §B](docs/SOLUTION_CONTRACT.md#b-solutions-metadata-schema) for complete SOLUTIONS schema and validation rules.

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

> 📖 See [`docs/SOLUTION_CONTRACT.md` §C](docs/SOLUTION_CONTRACT.md#c-judge--validation-contract) for complete JUDGE_FUNC signature and validation rules.

### 🎲 Random Test Generation

Create a generator file with the same name as your solution:

```python
# generators/0004_median_of_two_sorted_arrays.py
import random
from typing import Iterator, Optional

def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate random test cases."""
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
        yield f"{list(nums1)}\n{list(nums2)}".replace(' ', '')
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

> 📖 See [`docs/GENERATOR_CONTRACT.md`](docs/GENERATOR_CONTRACT.md) for complete generator specification and best practices.

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
├── tests/                     # 📋 Test cases
│   ├── 0001_two_sum_1.in      # Input file
│   ├── 0001_two_sum_1.out     # Expected output
│   └── *_failed_*.in          # Auto-saved failed cases (--save-failed)
│
├── generators/                # 🎲 Random test generators (optional)
│   └── 0001_two_sum.py        # generate(count, seed) function
│
├── runner/                    # ⚙️ Test execution engine
│   ├── test_runner.py         # CLI entry point & main orchestration
│   ├── case_runner.py         # Single case runner (for debugging)
│   ├── executor.py            # Test case execution (subprocess)
│   ├── compare.py             # Output comparison (exact/sorted/set/judge)
│   ├── reporter.py            # Result formatting & benchmark display
│   ├── module_loader.py       # Dynamic module loading
│   ├── complexity_estimator.py # Time complexity estimation (big_O)
│   ├── paths.py               # Path utilities
│   ├── io_utils.py            # File I/O operations
│   └── util.py                # Re-exports (backward compatible)
│
├── templates/                 # 📄 Problem templates
│   ├── template_solution.py       # Single solution template
│   ├── template_solution_multi.py # Multi-solution (polymorphic)
│   └── template_test.txt          # Test case template
│
├── .vscode/                   # 🔧 VS Code integration
│   ├── settings.json          # Python environment settings
│   ├── tasks.json             # Ctrl+Shift+B shortcuts
│   └── launch.json            # F5 debug configurations
│
├── docs/                      # 📚 Documentation (MkDocs)
│   ├── index.md               # Homepage (English)
│   ├── index_zh-TW.md         # Homepage (繁體中文)
│   ├── mindmaps/              # Generated mind map markdown
│   ├── patterns/              # Generated pattern documentation
│   ├── pages/                 # Generated HTML (gitignored)
│   └── stylesheets/           # Custom CSS
│
├── tools/                     # 🛠️ Utility scripts
│   ├── generate_mindmaps_ai.py    # 🤖 AI mind map generator
│   ├── mindmap_ai_config.toml     # AI generation configuration
│   ├── generate_mindmaps.py       # Rule-based mind map generator
│   ├── generate_mindmaps.toml     # Rule-based configuration
│   ├── generate_pattern_docs.py   # Generate pattern docs
│   ├── generate_pattern_docs.toml # Pattern docs configuration
│   ├── check_solutions.py         # Solution validation tool
│   ├── prepare_llm_input.py       # Prepare LLM input data
│   ├── text_to_mindmap.py         # Convert text to mindmap
│   ├── mindmaps/                  # Mind map generator modules
│   ├── patterndocs/               # Pattern docs generator modules
│   ├── shared/                    # Shared utilities
│   ├── prompts/                   # AI prompt management
│   │   ├── README.md              # Prompt documentation
│   │   └── generated/             # Auto-generated prompts
│   └── tests/                     # Format validation tests
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
│   ├── TESTING.md             # Testing documentation
│   ├── VIRTUAL_ENV_SETUP.md   # Virtual environment guide
│   └── README.md              # Maintainer guide
│
├── .github/                   # 🚀 GitHub configuration
│   └── workflows/
│       └── deploy-pages.yml   # GitHub Pages deployment
│
├── leetcode/                  # 🐍 Python virtual environment (3.11)
│
├── scripts/                   # 🔧 Utility scripts
│   ├── new_problem.bat / .sh  # Create new problem from template
│   ├── run_tests.bat / .sh    # Run all tests for a problem
│   ├── run_case.bat / .sh     # Run single test case
│   └── build_docs.bat / .sh   # Build documentation site
│
├── requirements.txt           # Python dependencies
├── mkdocs.yml                 # MkDocs configuration
├── pytest.ini                 # pytest configuration
├── README.md                  # This file (English)
└── README_zh-TW.md            # 繁體中文版
```

### Directory Guide

| Directory | Purpose | Target Audience |
|:----------|:--------|:----------------|
| `solutions/` | Write your solutions here | ✅ All users |
| `tests/` | Add test cases (.in/.out) | ✅ All users |
| `generators/` | Random test generators | ✅ All users |
| `runner/` | Test execution engine | 🔧 Contributors |
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
| [`docs/SOLUTION_CONTRACT.md`](docs/SOLUTION_CONTRACT.md) | Solution file specification |
| [`docs/GENERATOR_CONTRACT.md`](docs/GENERATOR_CONTRACT.md) | Generator file specification |
| [`tools/README.md`](tools/README.md) | Complete tools reference |
| [`.dev/README.md`](.dev/README.md) | Maintainer guide |
| [`.dev/DOCUMENTATION_ARCHITECTURE.md`](.dev/DOCUMENTATION_ARCHITECTURE.md) | Documentation structure |

---

## ❓ Frequently Asked Questions

<details>
<summary><strong>What problems does this framework solve?</strong></summary>

- Running multiple algorithm implementations automatically
- Generating reproducible random test data for stress testing
- Benchmarking solutions to identify performance differences
- Debugging LeetCode-style problems with VS Code integration
- Validating outputs using custom logic beyond simple file comparison

</details>

<details>
<summary><strong>How is this different from copying LeetCode solutions?</strong></summary>

This is not a solution collection — it's a **testing infrastructure**. You write solutions, and the framework:

1. Runs them against static test cases
2. Generates random test cases automatically
3. Validates correctness using custom judge functions
4. Benchmarks multiple solutions against each other
5. Estimates time complexity empirically

</details>

<details>
<summary><strong>Can I use this for interview preparation?</strong></summary>

Absolutely! The framework is perfect for interview prep:

- Practice writing solutions in **real LeetCode format**
- Find **edge cases you might miss** with random test generation
- See which approach is **actually faster** with benchmarking
- **Debug easily** with VS Code integration

</details>

<details>
<summary><strong>What Python version is required?</strong></summary>

Python 3.11 — matching the [LeetCode official environment](https://support.leetcode.com/hc/en-us/articles/360011833974-What-are-the-environments-for-the-programming-languages).

</details>

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
python tools/generate_mindmaps_ai.py

# With specific goal
python tools/generate_mindmaps_ai.py --goal interview

# Generate multiple languages
# Edit tools/mindmap_ai_config.toml: language = ["en", "zh-TW"]
python tools/generate_mindmaps_ai.py
```

Configuration: `tools/mindmap_ai_config.toml`

**Rule-Based:**

```bash
# Generate Markdown mind maps
python tools/generate_mindmaps.py

# Generate HTML (interactive) mind maps
python tools/generate_mindmaps.py --html
```

Configuration: `tools/generate_mindmaps.toml`

### Documentation

- [`.dev/README.md`](https://github.com/lufftw/neetcode/blob/main/.dev/README.md) — Maintainer guide
- [`.dev/TESTING.md`](https://github.com/lufftw/neetcode/blob/main/.dev/TESTING.md) — Testing documentation
- [`docs/SOLUTION_CONTRACT.md`](docs/SOLUTION_CONTRACT.md) — Solution file specification (SOLUTIONS dict, JUDGE_FUNC)
- [`docs/GENERATOR_CONTRACT.md`](docs/GENERATOR_CONTRACT.md) — Generator file specification (generate(), edge cases, complexity)
- [`docs/ARCHITECTURE_MIGRATION.md`](docs/ARCHITECTURE_MIGRATION.md) — Polymorphic architecture migration guide
- [`docs/GITHUB_PAGES_SETUP.md`](docs/GITHUB_PAGES_SETUP.md) — Deployment guide

---

## 📜 License

**MIT License** — Free for personal learning and educational use.

---

**Built with ❤️ for the competitive programming community**

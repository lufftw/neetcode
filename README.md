# NeetCode Practice Framework

[![GitHub stars](https://img.shields.io/github/stars/lufftw/neetcode?style=flat-square&logo=github)](https://github.com/lufftw/neetcode/stargazers)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

**Solve. Forget. Repeat. Let's fix that.**

> *"Algorithm mastery is not about memorizing 300 solutions — it's about internalizing 15 fundamental patterns."*

---

## See the Big Picture

[![AI Mind Map](https://img.shields.io/badge/Explore-AI%20Mind%20Map-blueviolet?style=for-the-badge)](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode-ontology-agent-evolved-en.html)

Our AI-generated mind maps reveal how patterns connect — relationships that take years to internalize on your own.

[![Mind Map Preview](docs/assets/mindmap-preview.png)](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode-ontology-agent-evolved-en.html)

[English](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode-ontology-agent-evolved-en.html) · [繁體中文](https://lufftw.github.io/neetcode/pages/mindmaps/neetcode-ontology-agent-evolved-zh-tw.html) · [All Mind Maps →](https://lufftw.github.io/neetcode/mindmaps/)

---

## What Makes This Different

### 1. Pattern Learning with Two Paths

Each pattern comes with **two complementary guides**:

- **💡 Intuition** — Understand the *why* through stories and visual metaphors
- **🛠️ Templates** — Production-ready code for interviews and quick reference

Example from [Sliding Window](docs/patterns/sliding_window/):

> *"The window is a moving lens of attention — it forgets the past to focus on what matters now."*
>
> Every sliding window algorithm is a dance between two forces: **The Explorer** (right pointer) discovers new territory, while **The Gatekeeper** (left pointer) enforces validity.

This isn't just another solution collection. It's a system for building **transferable intuition**.

### 2. Production-Grade Testing

Your solution passes LeetCode. But is it *correct*? Is it *optimal*?

**Compare multiple approaches:**

```bash
python runner/test_runner.py 0215_kth_largest --all --benchmark
```

```
╔════════════════════════════════════════════════════╗
║ 0215_kth_largest_element_in_an_array - Performance ║
╠════════════════════════════════════════════════════╣
║ default:     █████████████████░░░  170ms           ║
║ quickselect: ███████████████████░  191ms           ║
║ heap:        ████████████████████  199ms           ║
╚════════════════════════════════════════════════════╝

Method       Avg Time   Complexity              Description
-----------  ---------  ----------------------  ---------------------------
default      170.01ms   O(n) avg, O(1) space    Quickselect with random pivot
quickselect  191.13ms   O(n) avg, O(1) space    Quickselect with random pivot
heap         199.22ms   O(n log k), O(k) space  Min-heap of size k
```

**Verify your Big-O claim:**

```bash
python runner/test_runner.py 0004_median --estimate
```

```
📈 Running complexity estimation...
   n=   10: 0.0040ms
   n=  100: 0.0082ms
   n= 1000: 0.0685ms

✅ Estimated: O(log n)
   Confidence: 0.98
```

**Auto-save failing cases for debugging:**

```
gen_3: ❌ FAIL [generated]
   ┌─ Input ─────────────────────────────────
   │ [1,3,5,7]
   │ [2,4,6,8]
   ├─ Actual ────────────────────────────────
   │ 4.5
   └─────────────────────────────────────────
   💾 Saved to: tests/0004_failed_1.in
```

**More capabilities:**
- Seeded random generation for reproducible stress testing
- Custom judge functions for multiple valid answers
- Memory profiling with sparkline visualization

### 3. AI-Powered Knowledge Graph

We built an interconnected ontology: **API Kernels → Patterns → Problem Families**.

AI analyzes this structure to generate insights humans miss — synthesizing perspectives from Architect, Professor, Engineer, and Competitor viewpoints.

---

## Quick Start

### 1. Setup

```bash
# Clone and setup
git clone https://github.com/lufftw/neetcode.git
cd neetcode

# Create virtual environment (Python 3.11)
python -m venv leetcode
leetcode\Scripts\activate  # Windows
source leetcode/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

### 2. Create a Problem

```bash
scripts\new_problem.bat 1 --with-tests  # Windows
./scripts/new_problem.sh 1 --with-tests  # Linux/macOS
```

### 3. Run Tests

```bash
python runner/test_runner.py 0001_two_sum
```

**That's it.** Press `F5` in VS Code to debug, or `Ctrl+Shift+B` to run all tests.

---

## Pattern Guides

Each pattern provides Intuition + Templates. Start with intuition, use templates for interviews.

| Pattern | Intuition | Templates | Example Problems |
|:--------|:---------:|:---------:|:-----------------|
| Sliding Window | [💡](docs/patterns/sliding_window/intuition.md) | [🛠️](docs/patterns/sliding_window/templates.md) | LC 3, 76, 438 |
| Two Pointers | [💡](docs/patterns/two_pointers/intuition.md) | [🛠️](docs/patterns/two_pointers/templates.md) | LC 15, 11, 142 |
| Binary Search | [💡](docs/patterns/binary_search/intuition.md) | [🛠️](docs/patterns/binary_search/templates.md) | LC 33, 34, 875 |
| Backtracking | [💡](docs/patterns/backtracking_exploration/intuition.md) | [🛠️](docs/patterns/backtracking_exploration/templates.md) | LC 46, 51, 79 |
| Monotonic Stack | [💡](docs/patterns/monotonic_stack/intuition.md) | [🛠️](docs/patterns/monotonic_stack/templates.md) | LC 84, 739, 42 |
| Dynamic Programming | [💡](docs/patterns/dp_1d_linear/intuition.md) | [🛠️](docs/patterns/dp_1d_linear/templates.md) | LC 70, 198, 322 |
| Graph Traversal | [💡](docs/patterns/graph/intuition.md) | [🛠️](docs/patterns/graph/templates.md) | LC 200, 133, 994 |
| Tree Traversal | [💡](docs/patterns/tree/intuition.md) | [🛠️](docs/patterns/tree/templates.md) | LC 104, 124, 236 |

**[View All 25+ Patterns →](docs/patterns/README.md)**

---

## Features at a Glance

| Category | Capabilities |
|:---------|:-------------|
| **Testing** | Random generation, custom judges, stress testing, complexity estimation |
| **Learning** | Pattern intuition guides, reusable templates, dual-path documentation |
| **Visualization** | AI mind maps, pattern hierarchy, problem relationships |
| **Tooling** | VS Code integration, one-command scaffolding, benchmarking |

---

## Documentation

| Document | Description |
|:---------|:------------|
| [Pattern Guides](docs/patterns/README.md) | All 25+ patterns with Intuition + Templates |
| [Testing & Validation](docs/runner/README.md) | Complete test runner reference |
| [Solution Contract](docs/contracts/solution-contract.md) | How to write solution files |
| [Mind Maps](https://lufftw.github.io/neetcode/mindmaps/) | Interactive pattern visualizations |

---

## Contributing

We welcome contributions! See our [Contributor Guide](docs/contributors/README.md).

```bash
# Run unit tests
python -m pytest .dev/tests -v
```

---

## License

MIT License — Free for personal learning and educational use.

---

<p align="center">
  <b>Built for learners who want to understand, not just memorize.</b>
</p>

[📚 Docs](https://lufftw.github.io/neetcode/) · [🧠 Mind Maps](https://lufftw.github.io/neetcode/mindmaps/) · [📐 Patterns](docs/patterns/README.md) · [🧪 Testing](docs/runner/README.md)

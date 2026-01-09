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
║ default:     ████████████████████  114ms           ║
║ quickselect: ████████████████░░░░   96ms           ║
║ heap:        ██████████████████░░  107ms           ║
╚════════════════════════════════════════════════════╝

Method         Avg Time   Pass Rate  Complexity
-----------  ----------  ----------  --------------------
default        113.51ms         3/3  O(n) average time, O(1) space
quickselect     96.06ms         3/3  O(n) average time, O(1) space
heap           107.34ms         3/3  O(n log k) time, O(k) space
```

**Why algorithm choice matters — real data from 100+ problems:**

```
Benchmark Results (n = 5,000)
┌───────────────────────┬────────────────────────┬────────────────────────┬───────────┬─────────────────────┬──────────────────────┐
│ Problem               │ Fast                   │ Slow                   │ Speedup   │ Time Complexity     │ Space Complexity     │
├───────────────────────┼────────────────────────┼────────────────────────┼───────────┼─────────────────────┼──────────────────────┤
│ 0010 Regex Matching   │ Top-down Memo 0.08ms   │ Bottom-up DP 5.3s      │ 62,000×   │ O(mn) vs O(mn)      │ O(mn) vs O(mn)       │
├───────────────────────┼────────────────────────┼────────────────────────┼───────────┼─────────────────────┼──────────────────────┤
│ 0044 Wildcard Match   │ Greedy Backtrack 1.4ms │ 2D DP Table 10.0s      │ 7,000×    │ O(mn) vs O(mn)      │ O(1) vs O(mn)        │
├───────────────────────┼────────────────────────┼────────────────────────┼───────────┼─────────────────────┼──────────────────────┤
│ 0011 Container Water  │ Two Pointers 0.75ms    │ Nested Loops 4.9s      │ 7,000×    │ O(n) vs O(n²)       │ O(1) vs O(1)         │
├───────────────────────┼────────────────────────┼────────────────────────┼───────────┼─────────────────────┼──────────────────────┤
│ 0121 Buy Sell Stock   │ Running Min 2.0ms      │ Nested Loops 3.1s      │ 2,000×    │ O(n) vs O(n²)       │ O(1) vs O(1)         │
├───────────────────────┼────────────────────────┼────────────────────────┼───────────┼─────────────────────┼──────────────────────┤
│ 0416 Partition Sum    │ 2D DP Table 0.08ms     │ 1D DP Space-Opt 96.6ms │ 1,000×    │ O(n×target) vs same │ O(n×target) vs O(t)  │
├───────────────────────┼────────────────────────┼────────────────────────┼───────────┼─────────────────────┼──────────────────────┤
│ 0016 3Sum Closest     │ Two Ptr+Prune 1.1ms    │ Two Ptr Basic 1.4s     │ 1,000×    │ O(n²) vs O(n²)      │ O(1) vs O(1)         │
├───────────────────────┼────────────────────────┼────────────────────────┼───────────┼─────────────────────┼──────────────────────┤
│ 0435 Non-Overlap Intv │ Greedy Sort 5.0ms      │ DP Array 3.1s          │ 617×      │ O(n log n) vs O(n²) │ O(1) vs O(n)         │
├───────────────────────┼────────────────────────┼────────────────────────┼───────────┼─────────────────────┼──────────────────────┤
│ 0001 Two Sum          │ Hash Map 0.66ms        │ Nested Loops 70.1ms    │ 106×      │ O(n) vs O(n²)       │ O(n) vs O(1)         │
├───────────────────────┼────────────────────────┼────────────────────────┼───────────┼─────────────────────┼──────────────────────┤
│ 0494 Target Sum       │ DP Transform 0.04ms    │ Memoization 3.2ms      │ 73×       │ O(n×sum) vs same    │ O(sum) vs O(n×sum)   │
├───────────────────────┼────────────────────────┼────────────────────────┼───────────┼─────────────────────┼──────────────────────┤
│ 0875 Koko Bananas     │ Binary Search 14.6ms   │ Linear Search 1.1s     │ 72×       │ O(n log m) vs O(nm) │ O(1) vs O(1)         │
└───────────────────────┴────────────────────────┴────────────────────────┴───────────┴─────────────────────┴──────────────────────┘
```

📊 [Full benchmark: 100+ problems, 300+ solutions →](docs/benchmarks.md)

**Try it yourself:**

```bash
python runner/test_runner.py 0011_container --all --estimate
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
| Sliding Window | [💡](docs/patterns/sliding_window/intuition.md) | [🛠️](docs/patterns/sliding_window/templates.md) | LC 3, 76, 209, 239, 340, 438, 567 |
| Two Pointers | [💡](docs/patterns/two_pointers/intuition.md) | [🛠️](docs/patterns/two_pointers/templates.md) | LC 11, 15, 16, 26, 27, 75, 80, 88, 125, 141, 142, 167, 202, 283, 287, 876, 977 |
| Binary Search | [💡](docs/patterns/binary_search/intuition.md) | [🛠️](docs/patterns/binary_search/templates.md) | LC 4, 33, 34, 35, 81, 162, 875, 1011 |
| Backtracking | [💡](docs/patterns/backtracking_exploration/intuition.md) | [🛠️](docs/patterns/backtracking_exploration/templates.md) | LC 39, 40, 46, 47, 51, 52, 77, 78, 79, 90, 93, 131, 216 |
| Monotonic Stack | [💡](docs/patterns/monotonic_stack/intuition.md) | [🛠️](docs/patterns/monotonic_stack/templates.md) | LC 42, 84, 85, 316, 402, 496, 503, 739, 901, 907 |
| Dynamic Programming | [💡](docs/patterns/dp_1d_linear/intuition.md) | [🛠️](docs/patterns/dp_1d_linear/templates.md) | LC 70, 72, 121, 198, 213, 322, 416, 494, 516, 518, 746 |
| Graph Traversal | [💡](docs/patterns/graph/intuition.md) | [🛠️](docs/patterns/graph/templates.md) | LC 133, 200, 207, 210, 286, 417, 542, 547, 743, 785, 787, 802, 841, 994, 1631 |
| Tree Traversal | [💡](docs/patterns/tree/intuition.md) | [🛠️](docs/patterns/tree/templates.md) | LC 94, 102, 104, 110, 124, 337, 543, 968 |

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

### Getting Started

| Document | Description |
|:---------|:------------|
| [Create New Problem](docs/guides/new-problem.md) | How to scaffold a new problem |
| [Solution Contract](docs/contracts/solution-contract.md) | Solution file format and requirements |
| [Test File Format](docs/contracts/test-file-format.md) | How to write `.in/.out` test files |

### Learning

| Document | Description |
|:---------|:------------|
| [Pattern Guides](docs/patterns/README.md) | All 25+ patterns with Intuition + Templates |
| [Test Runner](docs/runner/README.md) | Testing, benchmarking, and validation |
| [Benchmarks](docs/benchmarks.md) | 100+ problems compared: speedups up to 65,000x |

### Advanced

| Document | Description |
|:---------|:------------|
| [Generator Contract](docs/contracts/generator-contract.md) | Random test generation for stress testing |

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

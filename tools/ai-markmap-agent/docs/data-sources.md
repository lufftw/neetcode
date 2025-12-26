# AI Markmap Agent - Data Sources Specification

> This document describes the input data required by the AI Markmap Agent and the compression strategies used for token-efficient LLM transmission.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Data Sources](#2-data-sources)
   - [Problems](#21-problems-metaproblemstoml)
   - [Ontology](#22-ontology-ontologytoml)
   - [Patterns](#23-patterns-docspatterns-metapatterns)
   - [Roadmaps](#24-roadmaps-roadmapstoml)
3. [Compression Strategy](#3-compression-strategy)
4. [Token Efficiency Analysis](#4-token-efficiency-analysis)
5. [Implementation](#5-implementation)

---

## 1. Overview

The AI Markmap Agent requires four categories of input data to generate comprehensive Markmaps:

| Source | Location | Format | Purpose |
|--------|----------|--------|---------|
| **Problems** | `meta/problems/*.toml` | TOML | Problem metadata with solution status |
| **Ontology** | `ontology/*.toml` | TOML | Taxonomy definitions (algorithms, patterns, DS) |
| **Patterns** | `docs/patterns/*.md` | Markdown | Detailed pattern documentation |
| **Roadmaps** | `roadmaps/*.toml` | TOML | Learning paths and progression |

### Data Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Problems  │    │   Ontology  │    │  Patterns   │    │  Roadmaps   │
│  (33 files) │    │  (9 files)  │    │  (2 files)  │    │  (3 files)  │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │                  │
       └──────────────────┴──────────────────┴──────────────────┘
                                    │
                          ┌─────────▼─────────┐
                          │  DataCompressor   │
                          │  (Token-Efficient)│
                          └─────────┬─────────┘
                                    │
                          ┌─────────▼─────────┐
                          │    LLM Prompts    │
                          │ (Minimal Tokens)  │
                          └───────────────────┘
```

---

## 2. Data Sources

### 2.1 Problems (`meta/problems/*.toml`)

#### Description
Each TOML file contains metadata for a single LeetCode problem, including solution status, patterns used, and relationships to other problems.

#### Key Fields for Markmap

| Field | Type | Description | Used In Markmap |
|-------|------|-------------|-----------------|
| `id` | string | Problem ID (e.g., "0003") | ✓ Display |
| `title` | string | Problem title | ✓ Display |
| `difficulty` | string | easy/medium/hard | ✓ Grouping |
| `patterns` | array | Algorithm patterns used | ✓ Categorization |
| `topics` | array | LeetCode topics | ✓ Categorization |
| `files.solution` | string | Solution file path (if exists) | ✓ Link selection |
| `roadmaps` | array | Which roadmaps include this | ○ Optional |
| `algorithms` | array | Algorithms used | ○ Optional |
| `data_structures` | array | Data structures used | ○ Optional |

#### Solution Status Logic
```
IF files.solution is non-empty string:
    → has_solution = true
    → link = GitHub solution URL
ELSE:
    → has_solution = false  
    → link = LeetCode problem URL
```

#### Example (Full vs Compressed)

**Full TOML (~1500 chars):**
```toml
id = "0003"
slug = "0003_longest_substring_without_repeating_characters"
title = "Longest Substring Without Repeating Characters"
leetcode_id = 3
url = "https://leetcode.com/problems/longest-substring-without-repeating-characters/"
difficulty = "medium"
topics = ["string", "hash_table", "sliding_window"]
patterns = ["sliding_window_unique"]
# ... 50+ more lines ...
[files]
solution = "solutions/0003_longest_substring_without_repeating_characters.py"
```

**Compressed JSON (~100 chars):**
```json
{"i":"0003","t":"Longest Substring Without Repeating Characters","d":"M","p":["sliding_window_unique"],"s":true,"sf":"solutions/0003_longest_substring_without_repeating_characters.py"}
```

---

### 2.2 Ontology (`ontology/*.toml`)

#### Files

| File | Content | Records |
|------|---------|---------|
| `algorithms.toml` | Core algorithms, techniques, paradigms | ~50 |
| `patterns.toml` | Problem-solving patterns | ~70 |
| `data_structures.toml` | Data structure definitions | ~40 |
| `api_kernels.toml` | Reusable code templates | ~15 |
| `families.toml` | Problem family groupings | ~20 |
| `topics.toml` | LeetCode topic taxonomy | ~40 |
| `roadmaps.toml` | Roadmap definitions | ~5 |
| `companies.toml` | Company tags | ~50 |
| `difficulties.toml` | Difficulty levels | 3 |

#### Key Fields for Markmap

**algorithms.toml:**
```toml
[[algorithms]]
id = "sliding_window"
kind = "technique"      # core, technique, paradigm, category
parent = "two_pointers" # hierarchy
summary = "Maintain a dynamic window [L,R] with an invariant."
```

**patterns.toml:**
```toml
[[patterns]]
id = "sliding_window_unique"
api_kernel = "SubstringSlidingWindow"
summary = "Window where all elements are unique."
```

#### Compression Strategy
- Extract only `id` and `summary` for LLM context
- Use parent-child relationships for hierarchy
- Omit rarely-used fields (companies, difficulties)

---

### 2.3 Patterns (`docs/patterns/*.md`, `meta/patterns/`)

#### Description
Detailed markdown documentation explaining each pattern with:
- Code templates
- Variation comparisons
- Example problems
- Decision trees

#### Files

| File | Size | Purpose |
|------|------|---------|
| `docs/patterns/sliding_window.md` | 25KB | Comprehensive sliding window guide |
| `docs/patterns/two_pointers.md` | 23KB | Two pointers pattern family |
| `meta/patterns/*/` | varies | Structured pattern components |

#### Compression Strategy
**These files are TOO LARGE for LLM context.** Instead:
1. Extract section headings only
2. Summarize key patterns from ontology
3. Reference problem IDs as examples

---

### 2.4 Roadmaps (`roadmaps/*.toml`)

#### Description
Learning paths that order problems by difficulty and concept dependencies.

#### Key Fields

```toml
id = "sliding_window_path"
name = "Sliding Window Mastery Path"
api_kernel = "SubstringSlidingWindow"

[[steps]]
order = 1
problem = "0003_longest_substring_without_repeating_characters"
role = "base"           # base, variant, advanced
pattern = "sliding_window_unique"
prerequisite = []
delta = ""              # what's different from prerequisite
note = "Learn the canonical sliding window template."
```

#### Compression Strategy
- Include step order and problem IDs
- Include role and pattern
- Omit verbose notes (summarize if needed)

---

## 3. Compression Strategy

### 3.1 Format Comparison

| Format | Token Ratio | Best For |
|--------|-------------|----------|
| **Full JSON** | 1.0x (baseline) | Debugging |
| **Compact JSON** | 0.3x | Balanced readability |
| **Tabular** | 0.2x | Maximum compression |
| **Minimal** | 0.1x | Just IDs and status |

### 3.2 Compact JSON Schema

```typescript
// Short key mappings
{
  "i": string,    // id (e.g., "0003")
  "t": string,    // title
  "d": "E"|"M"|"H", // difficulty
  "p": string[],  // patterns
  "s": boolean,   // has_solution
  "sf"?: string,  // solution_file (only if s=true)
  "tp"?: string[] // topics (optional)
}
```

### 3.3 Tabular Format

```
id|title|diff|solved|patterns
0001|Two Sum|E|✓|two_pointer_opposite
0003|Longest Substring...|M|✓|sliding_window_unique
0004|Median of Two...|H|○|binary_search
```

### 3.4 Ontology Compression

**Original:**
```toml
[[algorithms]]
id = "sliding_window"
kind = "technique"
parent = "two_pointers"
summary = "Maintain a dynamic window [L,R] with an invariant."
```

**Compressed:**
```json
{"algorithms":["bfs","dfs","dijkstra","sliding_window","two_pointers",...]}
```

Or hierarchical:
```json
{"two_pointers":["sliding_window","fast_slow_pointers","opposite_pointers"]}
```

---

## 4. Token Efficiency Analysis

### 4.1 Problem Data (33 problems)

| Format | Estimated Tokens | Savings |
|--------|-----------------|---------|
| Full TOML (all fields) | ~15,000 | 0% |
| Full JSON | ~12,000 | 20% |
| Compact JSON | ~3,500 | 77% |
| Tabular | ~2,000 | 87% |
| Minimal | ~500 | 97% |

### 4.2 Ontology Data

| Category | Full Tokens | Compressed | Savings |
|----------|-------------|------------|---------|
| algorithms.toml | ~2,500 | ~400 | 84% |
| patterns.toml | ~4,000 | ~600 | 85% |
| data_structures.toml | ~1,800 | ~300 | 83% |
| **Total** | ~10,000 | ~1,500 | 85% |

### 4.3 Recommended Configuration

```yaml
data_compression:
  enabled: true
  format: "compact_json"  # Best balance of info vs tokens
  
  problem_fields:
    - "id"
    - "title" 
    - "difficulty"
    - "patterns"
    - "has_solution"
    # Omit: topics, algorithms, companies (reconstructable from ontology)
  
  ontology_summary: true  # Only include IDs and hierarchy
  exclude_patterns_md: true  # Too large for context
```

---

## 5. Implementation

### 5.1 DataCompressor Class

Location: `src/data_compressor.py`

```python
class DataCompressor:
    """Token-efficient data formatting for LLM consumption."""
    
    # Short key mappings
    KEY_MAP = {
        "id": "i",
        "title": "t", 
        "difficulty": "d",
        "patterns": "p",
        "has_solution": "s",
        "solution_file": "sf",
    }
    
    DIFF_MAP = {"easy": "E", "medium": "M", "hard": "H"}
    
    def compress_problems(self, problems: dict) -> str:
        """Compress problem data to minimal JSON."""
        ...
    
    def compress_ontology(self, ontology: dict) -> str:
        """Extract essential ontology information."""
        ...
    
    def get_problem_url(self, problem_data: dict) -> str:
        """
        Get correct URL based on solution status.
        - has_solution=true → GitHub URL
        - has_solution=false → LeetCode URL
        """
        ...
```

### 5.2 Configuration

Location: `config/config.yaml`

```yaml
urls:
  github:
    solution_template: "https://github.com/lufftw/neetcode/blob/main/{solution_file}"
  leetcode:
    problem_template: "https://leetcode.com/problems/{slug}/"

data_compression:
  enabled: true
  format: "compact_json"
  problem_fields:
    - "id"
    - "title"
    - "difficulty"
    - "patterns"
    - "has_solution"
```

### 5.3 Usage in Prompts

The compressed data is passed to generator prompts with a format explanation:

```markdown
### Problem Data (Compressed Format)
[{"i":"0003","t":"Longest...","d":"M","p":["sliding_window_unique"],"s":true,"sf":"solutions/..."}]

**Key**: i=id, t=title, d=difficulty(E/M/H), p=patterns, s=has_solution, sf=solution_file
```

---

## Appendix: Data Not Included

The following data is **NOT** passed to LLM (too large or redundant):

| Data | Reason | Alternative |
|------|--------|-------------|
| Full pattern docs (*.md) | 25KB+ each | Use ontology patterns |
| Solution code | Not needed for Markmap | Reference via URL |
| Test cases | Not relevant | Omit |
| Company tags | Optional metadata | Available in config |
| Related problems | Derived from patterns | Implicit from ontology |


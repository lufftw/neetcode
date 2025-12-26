# CLI Output: Benchmark + Memory Profiling

> **Status**: Canonical Reference  
> **Scope**: CLI reporting rules for memory summaries, traces, comparisons, and error handling

This document defines how memory-related information is presented in the CLI, including
summary benchmarks, traces, multi-method comparisons, and failure scenarios.

---

## 1. Method Scope: `active_methods`

All memory outputs strictly follow the methods executed in the current run:

- No selection flag → `active_methods = ["default"]`
- `--method NAME` → `active_methods = [NAME]`
- `--all` → `active_methods = all methods in SOLUTIONS`

No additional method filtering flag is used.

---

## 2. `--benchmark` (Time + Memory Summary)

**Decision:** `--benchmark` includes memory summary by default.

### 2.1 Table Columns (Per Method)

The table is ordered to reflect user decision flow:
**performance → correctness → theory → measured memory**.

Columns:
1. Avg Time
2. Pass Rate
3. Aux Space (declared Big-O)
4. **Peak RSS (MB)**
5. **P95 RSS (MB)**

### 2.2 Example

```

Method     Avg Time   Pass Rate  Aux Space  Peak RSS   P95 RSS
default      83.2ms     50/50     O(N)       25.4MB     23.1MB
native      120.5ms     50/50     O(1)       21.1MB     20.8MB

```

**Notes**
- Time-based visual bar charts (if enabled) remain time-only.
- Benchmark output is always **method-level summary** (never per-case).

---

## 3. `--memory-trace` (Method-level Run Trace)

### Purpose
Show how memory usage evolves during execution for each method.

### Rules
- Prints **run-level memory traces only** (one line per method).
- Does **not** print case-level traces by default.
- Applies strictly to `active_methods`.

### Example

```

Memory Trace (Run-level RSS)

default:
▁▂▃▅▇▆▅▃▂▁
Peak 25.4MB | P95 23.1MB

native:
▁▂▃▄▅▄▃▂▁
Peak 21.1MB | P95 20.8MB

```

This output is observational and does not perform ranking or judgment.

---

## 4. `--memory-per-case` (Debug: Case-level Memory)

### Purpose
Enable targeted debugging when specific test cases cause abnormal memory usage.

### Rules
- Debug-only flag.
- Prints a **compact method-level summary first** (per method).
- Separates **RSS (subprocess)** and **Alloc (in-process)** measurements.
- Then prints **Top-K cases** for each measurement type (default K = 5).
- Finally prints **Global Top-K** across all methods.

### Measurement Types

| Type | Source | Measurement | Typical Values |
|------|--------|-------------|----------------|
| **RSS** | Static tests, Generated | `psutil` (subprocess) | 4-25MB |
| **Alloc** | `--estimate` runs | `tracemalloc` (in-process) | 4KB-300KB |

> **Note:** RSS and Alloc are **not comparable** — RSS includes Python interpreter
> and OS overhead, while Alloc measures Python allocations only.

### Example

```
Case Memory Summary (default)
[RSS] cases=3 | Peak=4.6MB | P95=4.6MB | Median=4.6MB
[Alloc] cases=24 | Peak=282KB | P95=281KB | Median=30KB

Top 3 by Peak RSS (subprocess):

Rank | Case ID                     | Peak RSS | Time    | Input Scale   | Input Bytes
-----|-----------------------------| ---------|---------|---------------|-------------
1    | 0023_merge_k_sorted_lists_1 | 4.6MB    | 176.4ms | lists:[3] n=8 | 18B
2    | 0023_merge_k_sorted_lists_2 | 4.6MB    | 173.3ms | lists:[0] n=0 | 2B
3    | 0023_merge_k_sorted_lists_3 | 4.6MB    | 174.0ms | lists:[1] n=0 | 8B

Top 5 by Peak Alloc (in-process):

Rank | Case ID      | Peak Alloc | Time   | Input Scale | Input Bytes
-----|--------------|------------|--------|-------------|-------------
1    | est_n2000_22 | 282KB      | 21.4ms | n=2000      | 9KB
2    | est_n2000_23 | 281KB      | 23.3ms | n=2000      | 9KB
3    | est_n2000_24 | 281KB      | 21.1ms | n=2000      | 9KB
4    | est_n1000_19 | 143KB      | 12.0ms | n=1000      | 4KB
5    | est_n1000_20 | 142KB      | 10.5ms | n=1000      | 4KB

============================================================
Global Summary
[RSS] 12 cases | Peak=4.6MB | Median=4.6MB
[Alloc] 96 cases | Peak=282KB | Median=30KB

Top 5 by Peak RSS (subprocess, across all methods):
...

Top 5 by Peak Alloc (in-process, across all methods):
...

Input Scale Legend:
  [a]     = 1D length
  [a,b]   = 2D shape (rows×cols)
  [a,b,c] = 3D shape
  n       = total elements
```

### Notes
- `Input Scale` uses PyTorch-style shape notation derived from method signatures.
- `Input Bytes` reflects the raw input size for the individual case.
- Missing values are shown as `N/A`.
- When `--estimate` is used, Alloc measurements from complexity estimation are included.

---

## 5. `--trace-compare` (Multi-Method Memory Comparison)

### Purpose
Provide an **overall memory comparison across multiple methods**, focusing on
high-level insight rather than raw traces.

This flag is intended to answer:
> “Which method uses less memory overall, and which is more stable?”

### Applicability
- Effective when `active_methods > 1`.
- When only one method is executed, the comparison degenerates to a summary;
  users are advised to use `--memory-trace` instead.

---

### 5.1 Primary Output: Memory Ranking Table

```

Memory Comparison Summary

Rank | Method   | Peak RSS | P95 RSS | Δ Peak (vs best) | Stability              | Notes
1    | native   | 21.1MB   | 20.8MB  | +0.0MB (0%)      | stable (Δ=1.4%)        |
2    | default  | 25.4MB   | 23.1MB  | +4.3MB (+20%)    | spiky (Δ=10.2%)        | higher spikes

```

#### Definitions

- **Rank**  
  Ordered by Peak RSS (default criterion).

- **Δ Peak (vs best)**  
  Absolute and relative difference compared to the lowest Peak RSS method.

- **Stability**  
  Quantifies memory volatility using:

```

Stability (%) = (Peak RSS - P95 RSS) / P95 RSS * 100

```

Thresholds:
- `< 5%`   → **stable**
- `5–15%`  → **moderate**
- `> 15%`  → **spiky**

- **Notes**  
Auto-generated annotations (e.g., “higher spikes”) to aid interpretation.

---

### 5.2 Secondary Output: Supporting Traces

Traces are shown as **supporting evidence**, not as the primary comparison signal.

```

Memory Trace Comparison (Run-level RSS)

native  : ▁▂▃▄▅▄▃▂▁
default : ▁▂▃▅▇▆▅▃▂▁

```

---

## 6. Output Ordering (Consistent)

When multiple flags are enabled, output order is:

1. Time visual bar chart (existing, if enabled)
2. Benchmark table (`--benchmark`)
3. Run-level memory traces (`--memory-trace`)
4. Overall comparison (`--trace-compare`)
5. Case-level debug output (`--memory-per-case`)

---

## 7. Error Handling in Outputs

### 7.1 RSS Measurement Failures
If RSS measurement fails (e.g., permission denied, unsupported platform):

- Display:
```

Peak RSS: Unavailable
P95 RSS: Unavailable

```
- Log technical details to debug output or log files if enabled.

### 7.2 Undeclared Aux Space
If a solution does not declare auxiliary space complexity:

- Display:
```

Aux Space: Undeclared

```

### 7.3 Zero or Small Memory Values
Memory values are formatted dynamically:
- ≥ 1 MB → shown in MB (e.g., `2.3MB`)
- < 1 MB → shown in KB for precision (e.g., `512KB`)

This ensures consistent readability across small and large inputs.
```

---
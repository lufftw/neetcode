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
- Prints a **compact method-level summary first**.
- Then prints **Top-K cases by peak RSS** (default K = 5).
- Full per-case dumps are intentionally avoided.

### Example

```

Case Memory Summary (default)
cases=200 | Peak=25.4MB | P95=23.1MB | Median=18.2MB

Top 5 memory cases (by peak RSS):

Rank | Case ID | Case Peak RSS | Time   | Input Scale (case) | Input Bytes
-----|---------|---------------|--------|--------------------|-------------
1    | gen_137 | 25.4MB        | 2.1ms  | n=100000           | 0.9MB
2    | gen_088 | 24.9MB        | 1.9ms  | n=98000            | 0.88MB
3    | case_3  | 24.2MB        | 1.8ms  | n=100000           | 0.9MB
4    | gen_012 | 24.0MB        | 1.7ms  | n=95000            | 0.85MB
5    | case_7  | 23.9MB        | 1.6ms  | n=200              | 4KB

Notes:
- `Input Scale (case)` is derived from generator metadata or signature-based heuristics.
- `Input Bytes` reflects the raw input size for the individual case.
- Missing values are shown as `N/A`.

```

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
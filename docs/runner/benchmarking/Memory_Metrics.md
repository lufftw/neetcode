# Memory Metrics

> **Status**: Canonical Reference  
> **Scope**: Definition and semantics of memory-related metrics used in benchmarking,
> tracing, and comparison outputs.

This document defines **what memory metrics mean**, how they are computed,
and how they relate to algorithmic space complexity.  
It is intentionally decoupled from CLI flags and focuses on metric semantics.

---

## 1. Design Principles

Memory reporting in this project follows four principles:

1. **Theory ≠ Measurement**  
   Algorithmic space complexity (Big-O) must not be conflated with measured memory.

2. **Method-level by Default**  
   Default outputs summarize memory at the method level, even when many test cases exist.

3. **Explicit Debugging**  
   Case-level memory is available only via explicit debug options.

4. **Graceful Degradation**  
   Missing or failed measurements must be reported explicitly, never guessed.

---

## 2. Metrics Overview

| Metric | Layer | Meaning | Unit | Notes |
|---|---|---|---|---|
| Aux Space (Big-O) | Algorithmic | Theoretical auxiliary memory excluding input | — | Declared in solution metadata |
| Peak RSS | Execution | Maximum resident set size observed | MB / KB | Worst-case memory spike |
| P95 RSS | Execution | 95th percentile of per-case peak RSS | MB / KB | Robust worst-case indicator |
| Signature Payload | Input | Deep size of signature input objects | MB / KB | May be unavailable |
| Input Bytes | Input | Raw stdin size | MB / KB | Fallback when signature unavailable |

---

## 3. Aux Space (Algorithmic Space Complexity)

**Definition**  
Aux Space represents the asymptotic *extra* memory required by an algorithm,
excluding the memory occupied by the input itself.

**Properties**
- Expressed in Big-O notation (e.g., `O(1)`, `O(N)`).
- Language- and runtime-independent.
- Optional but recommended for all solutions.

**Display Rules**
- If declared: display the Big-O value.
- If not declared: display `Aux Space: Undeclared`.

Aux Space is **theoretical** and must never be inferred from RSS values.

---

## 4. Measured Runtime Memory (RSS)

RSS (Resident Set Size) reflects the actual physical memory footprint of the process
as observed by the operating system during execution.

### 4.1 Case-level Measurement

For each test case, the following value is recorded:

- `case_peak_rss`: maximum RSS observed during that test case.

This value is not shown by default in CLI output.

---

### 4.2 Method-level Aggregation

When multiple test cases exist, case-level values are aggregated per method:

- **Peak RSS**  
```

Peak RSS = max(case_peak_rss)

```

- **P95 RSS**  
```

P95 RSS = 95th percentile(case_peak_rss)

```

**Rationale**
- Peak RSS captures absolute worst-case memory spikes (OOM risk).
- P95 RSS reflects typical worst-case behavior and is less sensitive to single outliers.

---

## 5. Stability Metric (Derived)

Stability quantifies how volatile memory usage is across test cases.

**Definition**

```

Stability (%) = (Peak RSS - P95 RSS) / P95 RSS * 100

```

**Interpretation Thresholds**

| Stability (%) | Classification |
|---|---|
| < 5% | stable |
| 5–15% | moderate |
| > 15% | spiky |

Stability is a **derived indicator** used only in comparative views.
It is not a standalone metric.

---

## 6. Input-related Memory Context

### 6.1 Signature Payload

**Definition**  
Signature Payload estimates the deep memory footprint of method signature
input objects when they are available in-process.

**Notes**
- Provides context for interpreting RSS values.
- Is not part of algorithmic space complexity.
- May be unavailable depending on execution mode.

---

### 6.2 Input Bytes

**Definition**  
Input Bytes measure the raw size of stdin input.

**Usage**
- Acts as a fallback when signature objects are unavailable.
- Provides minimal input size context.

---

## 7. Formatting and Units

Memory values are formatted dynamically for readability:

- Values ≥ 1 MB → displayed in MB (e.g., `25.4MB`)
- Values < 1 MB → displayed in KB (e.g., `512KB`)
- Zero values → displayed as `0KB`

Unit conversion is for presentation only and does not affect calculations.

---

## 8. Error Handling and Missing Data

### 8.1 RSS Measurement Failures

If RSS measurement is unavailable (e.g., permission denied, unsupported platform):

- Display:
```

Peak RSS: Unavailable
P95 RSS: Unavailable

```
- The benchmark continues without aborting.

---

### 8.2 Missing Input Metrics

- Signature Payload unavailable → display `Signature Payload: N/A`
- Input Bytes unavailable → display `Input Bytes: N/A`

---

## 9. Relationship Between Metrics (No Inference)

The following metrics answer different questions and must not be converted:

- **Aux Space** → theoretical extra memory requirement
- **Peak / P95 RSS** → observed runtime memory usage
- **Signature Payload / Input Bytes** → input size context

All are reported side-by-side for clarity, never inferred from one another.
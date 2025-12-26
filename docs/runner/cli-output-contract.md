# CLI Output Compatibility Contract

> **Status**: Canonical Reference
> **Scope**: Stability and backward compatibility guarantees for CLI output
> **Audience**: Tool authors, contributors, parser maintainers

This document defines **hard compatibility rules** for CLI output.
Its purpose is to ensure that new metrics (e.g., memory profiling) can be added
without breaking existing user workflows, log parsers, or mental models.

---

## 1. Core Principles

1. **Backward Compatibility First**
   Existing output blocks must not change their meaning or ordering.

2. **Single Responsibility per Block**
   Each visual or tabular block serves one semantic purpose only.

3. **Append-Only Extensions**
   New information is added by extending existing tables or appending new blocks,
   never by mutating established ones.

4. **Predictable Tokens**
   Missing or failed measurements must use fixed, machine-parseable tokens.

---

## 2. Output Block Taxonomy

The CLI output is composed of the following high-level blocks, in order:

1. Execution header / test progress
2. Per-method test results (case-level PASS/FAIL lists)
3. Performance visualization (bar chart)
4. **Performance Comparison (Details)** table
5. Optional appended blocks (trace, comparison, debug)

This ordering is **stable and contractual**.

---

## 3. Performance Bar Chart (Time-Only)

### Contract

* The performance bar chart **represents execution time only**.
* Bars must not encode memory, I/O, GC, or any other metric.
* No secondary axes or mixed semantics are allowed.

### Rationale

Users have a strong, established mental model:

> **Bar length = execution time**

Violating this assumption would cause confusion and break backward compatibility.

### Consequence

All non-time metrics **must not appear** in the bar chart.

---

## 4. Performance Comparison (Details) Table

### Role

The **Details table** is the **only extensible summary surface** for structured metrics.

* Human-readable
* Machine-parseable
* Column-oriented

### Placement

* The section title **must remain unchanged**:

  ```
  Performance Comparison (Details)
  ```
* The table must appear **after** the performance bar chart.

---

## 5. Column Extension Rules

### Allowed Changes

* New metrics may be added **only as new columns**.
* Existing columns must not be reordered or removed.

### Current Canonical Column Order

Minimal-compatibility ordering (existing columns preserved, new ones appended):

```
Method | Avg Time | Pass Rate | Declared | Estimated | Peak RSS | P95 RSS
```

Notes:

* `Declared` / `Estimated` refer to existing complexity-related fields.
* `Peak RSS` and `P95 RSS` are memory summary metrics.
* Future metrics must follow the same append-only rule.

---

## 6. Missing / Failed Measurement Tokens

To ensure consistent parsing and user clarity, the following tokens are fixed:

| Scenario                     | Token         |
| ---------------------------- | ------------- |
| RSS measurement unavailable  | `Unavailable` |
| Auxiliary space not declared | `Undeclared`  |
| Metric not applicable        | `N/A`         |

Example:

```
heap   ...   Peak RSS: Unavailable   P95 RSS: Unavailable
```

Tokens must be used verbatim.

---

## 7. Units and Formatting

### Memory Units

* Values ≥ 1 MB → display in MB (e.g., `25.4MB`)
* Values < 1 MB → display in KB (e.g., `512KB`)
* Zero values → display as `0KB`

### Formatting Rules

* Unit conversion is **presentation-only**.
* Internal calculations must use raw numeric values.

---

## 8. Appended Diagnostic Blocks

The following flags introduce **additional blocks**, which must obey append-only rules:

* `--memory-trace`
* `--trace-compare`
* `--memory-per-case`

### Placement Rule

* These blocks **must appear after** the Details table.
* They must not interrupt:

  * per-case test output
  * the bar chart
  * the Details table itself

Each appended block must have:

* a clear header
* fixed separators
* no impact on preceding content

---

## 9. Parser Compatibility Guidelines

For downstream tools and scripts:

* Use the **Details table header line** to detect column layout.
* Do not assume a fixed column count.
* Skip unknown appended blocks by matching section headers.

This contract guarantees that:

* Existing parsers continue to work.
* New metrics can be introduced safely.

---

## 10. Non-Goals

This contract explicitly does **not** guarantee:

* Visual compactness when many metrics are enabled
* Automatic reflow or column wrapping
* Stability of experimental or debug-only blocks

---

## 11. Summary

This contract enforces a clear separation of concerns:

* **Bar chart** → time visualization only
* **Details table** → extensible structured summary
* **Appended blocks** → diagnostics and deep inspection

By following this contract, the CLI can evolve without breaking users,
parsers, or mental models.

---
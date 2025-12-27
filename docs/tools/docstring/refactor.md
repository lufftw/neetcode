# Docstring Domain Refactor – Design Rationale

## Background

Originally, the docstring-related logic (e.g., extracting descriptions, constraints, examples, and formatting them into a structured docstring payload) lived under the `tools/review-code/` directory.

This placement was convenient at the early stage because the first consumer of this logic was the `fix_docstring` tool. However, as the functionality evolved, it became clear that this module is **not inherently tied to code review**.

Instead, it represents a **stable domain abstraction**:

> transforming a *Question* object into a *Docstring-oriented structured specification*.

This document explains the motivation and rationale behind refactoring this logic into a dedicated `docstring` domain.

---

## Problem with the Original Structure

### 1. Domain Misplacement

Placing docstring extraction and formatting logic under `review-code` implies that:

* The logic is specific to code review workflows
* Other tools should not depend on it directly

In reality:

* The module does not perform review logic
* It does not depend on review-specific concepts
* It can be reused by other tools (e.g., generators, analyzers, metadata enrichers)

This created a **semantic mismatch** between directory structure and actual responsibility.

---

### 2. Implementation-Leaking Naming

The original filename (e.g., `leetscrape_fetcher.py`) exposed an **implementation detail**:

* It suggested direct dependence on LeetScrape
* It obscured the true responsibility of the module

However, the module’s actual role is:

* Consuming a `Question` abstraction (via a unified API)
* Extracting and normalizing docstring-relevant information
* Producing a structured, spec-aligned representation

The data source (LeetScrape, SQLite cache, future providers) is an internal concern and should not define the module’s identity.

---

### 3. Long-Term Maintainability Concerns

As the project grows, docstring-related concerns are expected to expand, such as:

* Spec validation
* Schema evolution
* Rendering or normalization rules
* Additional metadata extraction

Keeping these concepts embedded inside a review tool would make future extension awkward and misleading.

---

## Design Decision

### Introduce a Dedicated `docstring` Domain

We refactor docstring-related logic into a first-class domain under `tools/docstring/`.

```text
tools/
├── docstring/
│   ├── formatter.py
│   └── README.md
├── review-code/
│   └── fix_docstring.py
```

Key points of this decision:

* `docstring` is a **domain**, not a utility bucket
* It is **conceptually independent** from review workflows
* `review-code` becomes a **consumer**, not the owner, of docstring logic

---

## Responsibility Boundaries

### `tools/docstring/`

Responsible for:

* Extracting docstring-relevant content from a `Question` abstraction
* Normalizing and structuring data according to docstring specifications
* Remaining agnostic to:

  * How the question is fetched
  * Which tool consumes the output

Non-responsibilities:

* Code review decisions
* File I/O or patching logic
* CLI concerns

---

### `tools/review-code/`

Responsible for:

* Applying review or fix workflows
* Deciding *when* and *how* docstring data is injected or updated
* Orchestrating interactions between code files and docstring data

It **depends on** the `docstring` domain but does not define it.

---

## Benefits of This Refactor

1. **Clear Domain Semantics**
   Docstring logic is defined by *what it is*, not *who uses it*.

2. **Improved Reusability**
   Other tools can safely depend on `tools.docstring` without semantic confusion.

3. **Reduced Coupling**
   Review workflows can evolve independently from docstring specifications.

4. **Future-Proof Structure**
   New docstring-related modules (e.g., validators, schemas) have a natural home.

---

## Import Example

```python
from tools.docstring.formatter import get_full_docstring_data

docstring_data = get_full_docstring_data(question)
```

This import path explicitly communicates:

* This is docstring-domain logic
* It is not review-specific
* It is part of a stable, reusable abstraction layer

---

## Summary

This refactor is not a cosmetic rename.
It is a **domain clarification**.

By elevating `docstring` to a first-class domain, the project gains:

* Clearer architecture
* Better naming integrity
* A foundation for long-term evolution without structural debt
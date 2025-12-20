## Documentation Metadata Header Specification

> **Status**: Canonical Reference  
> **Scope**: All documentation files  
> **Last Updated**: {{ git_revision_date_localized }}  
> **Created**: {{ git_creation_date_localized }}

### Purpose

This metadata header defines the **authoritative status, applicability scope, and lifecycle timestamps** of a documentation file.
It is used to clarify whether a document is canonical or informational, what it governs, and when it was created or last updated.

All documentation files **must include this header immediately after the document title**, unless explicitly stated otherwise.

---

### Required Fields

Each documentation file **MUST** include the following fields, in the exact order shown below:

```markdown
> **Status**: <status value>  
> **Scope**: <scope description>  
> **Last Updated**: {{ git_revision_date_localized }}  
> **Created**: {{ git_creation_date_localized }}
```

---

### Field Definitions

#### **Status**

Indicates the authority level of the document.

Allowed values:

* **Canonical Reference**
  The single source of truth. Other documents must follow this specification.
* **Normative**
  Defines rules or constraints that must be followed.
* **Informational**
  Provides explanation or background; not strictly binding.
* **Draft**
  Work in progress; subject to change.

> Each document MUST have exactly one status value.

---

#### **Scope**

Defines **what files, directories, or components this document applies to**.

Guidelines:

* Be explicit and unambiguous
* Prefer directory-based scopes when possible
* Use inline code formatting for paths

Examples:

* `All generator files in generators/`
* `All solution files in solutions/`
* `Documentation under docs/architecture/`
* `Repository-wide`

---

#### **Last Updated**

```text
{{ git_revision_date_localized }}
```

* Automatically populated by the documentation build system
* Reflects the **last Git commit that modified the file**
* MUST NOT be manually edited

---

#### **Created**

```text
{{ git_creation_date_localized }}
```

* Automatically populated by the documentation build system
* Reflects the **initial Git commit that introduced the file**
* MUST NOT be manually edited

---

### Canonical Examples

#### Generator Specification Documents

```markdown
# Generator Contract Specification

> **Status**: Canonical Reference  
> **Scope**: All generator files in `generators/`  
> **Last Updated**: {{ git_revision_date_localized }}  
> **Created**: {{ git_creation_date_localized }}

This document defines the **contract** for test case generator files...
```

#### Solution Specification Documents

```markdown
# Solution Contract Specification

> **Status**: Canonical Reference  
> **Scope**: All solution files in `solutions/`  
> **Last Updated**: {{ git_revision_date_localized }}  
> **Created**: {{ git_creation_date_localized }}

This document defines the **contract** for solution files...
```

---

### Placement Rules

* The metadata header **MUST appear immediately after the document title** (the first `#` heading)
* The structure MUST follow this order:
  1. Document title (first `#` heading)
  2. Blank line
  3. Metadata header block
  4. Blank line
  5. Document body content
* A blank line MUST follow the header block before body text begins

---

### Rationale (Optional Section)

This header standard exists to:

* Clearly distinguish canonical specifications from explanatory notes
* Define enforcement boundaries for generators, solutions, and tooling
* Enable automated auditing and documentation freshness checks
* Improve long-term maintainability in large repositories

---
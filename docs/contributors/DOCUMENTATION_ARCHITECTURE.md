# Documentation Architecture

> **Status**: Informational  
> **Scope**: Documentation under `.dev/` and `docs/`  
> **Last Updated**: {{ git_revision_date_localized }}  
> **Created**: {{ git_creation_date_localized }}

This document explains the documentation structure of the NeetCode Practice Framework, following software engineering best practices.

---

## 📐 Design Principles

### Separation of Concerns

Documentation is organized by **target audience**, not by file type:

| Directory | Purpose | Target Audience | Location |
|-----------|---------|-----------------|----------|
| `docs/` | User-facing documentation | Users, learners | Website |
| `docs/tools/` | Developer tools reference (full docs) | Contributors | Website |
| `docs/contributors/` | Maintainer documentation (full docs) | Maintainers | Website |
| `tools/README.md` | Tools overview (shortened) | Contributors | GitHub only |
| `.dev/README.md` | Maintainer overview (shortened) | Maintainers | GitHub only |

### Single Source of Truth

Each topic has **one authoritative document**:

- ❌ Avoid: Same content in multiple places
- ✅ Prefer: One source, with links from other places

### Proximity Principle

Documentation follows a **migration strategy** for accessibility:

- Full documentation → `docs/tools/` and `docs/contributors/` (accessible on website)
- Shortened READMEs → Original locations (`tools/README.md`, `.dev/README.md`) with links to full docs
- Code proximity → Tool scripts remain in `tools/`, tests remain in `.dev/`

---

## 📁 Documentation Structure

```
neetcode/
│
├── README.md                    # 🏠 Project overview (users)
├── README_zh-TW.md              # 🏠 Project overview (繁體中文)
│
├── docs/                        # 📚 Documentation (MkDocs website)
│   ├── index.md                 # Homepage (includes README.md)
│   ├── index_zh-TW.md           # Homepage (繁體中文)
│   │
│   ├── SOLUTION_CONTRACT.md     # Solution file specification
│   ├── GENERATOR_CONTRACT.md    # Generator file specification
│   ├── ARCHITECTURE_MIGRATION.md # Architecture migration guide
│   ├── GITHUB_PAGES_SETUP.md    # Deployment guide
│   │
│   ├── patterns/                # Pattern documentation
│   │   ├── README.md
│   │   ├── sliding_window/
│   │   └── two_pointers/
│   │
│   ├── mindmaps/                # Mind map documentation
│   │   ├── index.md
│   │   └── *.md
│   │
│   ├── contributors/            # 👥 Maintainer documentation (website)
│   │   ├── README.md            # Full maintainer guide
│   │   ├── TESTING.md           # Complete testing documentation
│   │   ├── DOCUMENTATION_ARCHITECTURE.md  # This file
│   │   └── VIRTUAL_ENV_SETUP.md # Virtual environment setup
│   │
│   ├── tools/                   # 🛠️ Tools documentation (website)
│   │   ├── README.md            # Complete tools reference
│   │   ├── ai-markmap-agent/
│   │   │   └── README.md        # AI Markmap Agent docs
│   │   ├── mindmaps/
│   │   │   └── README.md        # Mind Maps Generator docs
│   │   └── patterndocs/
│   │       └── README.md        # Pattern Docs Generator docs
│   │
│   ├── ONTOLOGY_DESIGN.md       # Ontology design
│   └── MKDOCS_CONTENT_GUIDE.md  # Content guide
│
├── tools/                       # 🔧 Developer tools (code + scripts)
│   ├── README.md                # Shortened version (links to docs/tools/)
│   ├── *.py                     # Tool scripts
│   ├── ai-markmap-agent/        # AI Markmap Agent (code only)
│   ├── mindmaps/                # Mind Maps Generator (code only)
│   ├── patterndocs/             # Pattern Docs Generator (code only)
│   └── prompts/
│       └── README.md            # AI prompts documentation
│
└── .dev/                        # 🔒 Maintainer zone (tests + scripts)
    ├── README.md                # Shortened version (links to docs/contributors/)
    ├── tests/                   # Component tests
    └── tests_solutions/         # Solution correctness tests
```

---

## 🎯 Target Audience Guide

### 👤 Users (Learners, Practitioners)

**What they need:**
- How to use the framework
- Solution and generator specifications
- Pattern guides and mind maps

**Where to find:**
- `README.md` → Quick start
- `docs/` → Detailed documentation
- Website → `https://lufftw.github.io/neetcode/`

### 🔧 Contributors (Pull Request Authors)

**What they need:**
- Code style and architecture
- Tool usage
- Testing requirements

**Where to find:**
- `docs/tools/README.md` → Complete tools reference (website)
- `docs/SOLUTION_CONTRACT.md` → Solution format
- `docs/contributors/TESTING.md` → Complete testing documentation (website)

### 🛠️ Maintainers (Core Team)

**What they need:**
- Internal architecture
- Release process
- Module deep-dives

**Where to find:**
- `docs/contributors/README.md` → Full maintainer guide (website)
- `docs/tools/*/README.md` → Complete module documentation (website)
- `docs/contributors/DOCUMENTATION_ARCHITECTURE.md` → Documentation structure (this file)

---

## 📋 Documentation Checklist

### When Adding a New Feature

- [ ] Update `README.md` if user-facing
- [ ] Update `tools/README.md` if developer tool
- [ ] Add module README if new module
- [ ] Update relevant CONTRACT files if API change

### When Adding a New Tool

- [ ] Add to `docs/tools/README.md` quick reference table (full documentation)
- [ ] Add detailed section in `docs/tools/README.md`
- [ ] Create `docs/tools/<module>/README.md` if complex
- [ ] Update `tools/README.md` (shortened version) if needed
- [ ] Add tests to `.dev/tests/` or `tools/tests/`
- [ ] Update `mkdocs.yml` navigation if adding new documentation page

### When Modifying Documentation Structure

- [ ] Update this file (`docs/contributors/DOCUMENTATION_ARCHITECTURE.md`)
- [ ] Update `docs/MKDOCS_CONTENT_GUIDE.md`
- [ ] Update `mkdocs.yml` if adding to website
- [ ] Update README documentation section

---

## 🏗️ Industry Best Practices

This structure follows patterns from well-known open source projects:

### Flask / Django Pattern

```
project/
├── docs/           # Sphinx/MkDocs user documentation
├── scripts/        # Scripts with their own README
└── CONTRIBUTING.md # Contributor guide
```

### Kubernetes Pattern

```
project/
├── docs/           # User documentation
├── hack/           # Developer scripts and tools
└── contributor/    # Contributor documentation
```

### Our Adaptation

```
neetcode/
├── docs/           # User documentation (MkDocs)
├── tools/          # Developer tools (with README.md)
└── .dev/           # Maintainer documentation
```

---

## ❓ FAQ

### Why migrate documentation to `docs/`?

**Migration Strategy**: Full documentation has been moved to `docs/contributors/` and `docs/tools/` to make it accessible via the MkDocs website, while maintaining GitHub browsing context through shortened READMEs in original locations.

**Benefits**:
- ✅ All documentation accessible on MkDocs website
- ✅ Maintains GitHub browsing context with shortened READMEs
- ✅ Links work correctly in both GitHub and website using relative paths
- ✅ Single source of truth for full documentation content

**Structure**:
- `docs/contributors/` → Full maintainer documentation (on website)
- `docs/tools/` → Full tools documentation (on website)
- `.dev/README.md` → Shortened version (links to full docs on website)
- `tools/README.md` → Shortened version (links to full docs on website)

### Why `.dev/` for maintainer zone?

- Clearly signals "internal" directory
- Keeps root directory clean
- Groups with test files (same audience)
- Shortened README maintains GitHub browsing context

### Why separate code from documentation in `tools/`?

- `tools/` → Contains actual tool scripts (`.py` files) and shortened README
- `docs/tools/` → Contains full documentation (on website)
- Clear separation between code and documentation

### How do I know where to add new documentation?

Ask: **Who is the primary reader?**

| Reader | Location |
|--------|----------|
| User learning the framework | `docs/` (patterns, guides, contracts) |
| Contributor adding features | `docs/tools/README.md` (full reference on website) |
| Maintainer debugging issues | `docs/contributors/` (full docs on website) |

**Note**: Original locations (`.dev/README.md`, `tools/README.md`) contain shortened versions with links to full documentation on the website.

---

## 📝 Update Log

- **2025-12-24**: Migrated maintainer and tools documentation to `docs/contributors/` and `docs/tools/` for MkDocs website integration. Created shortened READMEs in original locations with links to full documentation.
- **2025-12-12**: Initial version - Documented architecture after consolidating tools documentation

---

## 🔗 Related Documents

- [Maintainer Guide](contributors/README.md)
- [Testing Documentation](contributors/TESTING.md)
- [MkDocs Content Guide](MKDOCS_CONTENT_GUIDE.md)
- [Tools Reference](tools/README.md)


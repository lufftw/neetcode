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

| Directory | Purpose | Target Audience |
|-----------|---------|-----------------|
| `docs/` | User-facing documentation | Users, learners |
| `tools/README.md` | Developer tools reference | Contributors |
| `tools/*/README.md` | Module technical details | Deep contributors |
| `.dev/` | Maintainer documentation | Maintainers |

### Single Source of Truth

Each topic has **one authoritative document**:

- ❌ Avoid: Same content in multiple places
- ✅ Prefer: One source, with links from other places

### Proximity Principle

Documentation lives **close to the code** it describes:

- Tool documentation → `tools/README.md`
- Module documentation → `tools/<module>/README.md`
- Test documentation → `.dev/TESTING.md`

---

## 📁 Documentation Structure

```
neetcode/
│
├── README.md                    # 🏠 Project overview (users)
├── README_zh-TW.md              # 🏠 Project overview (繁體中文)
│
├── docs/                        # 📚 User documentation (MkDocs website)
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
│   │   ├── sliding_window.md
│   │   └── two_pointers.md
│   │
│   ├── mindmaps/                # Mind map documentation
│   │   ├── index.md
│   │   └── *.md
│   │
│   ├── ONTOLOGY_DESIGN.md       # Ontology design (not in nav)
│   └── MKDOCS_CONTENT_GUIDE.md  # Content guide (not in nav)
│
├── tools/                       # 🔧 Developer tools
│   ├── README.md                # Tools reference (comprehensive)
│   │
│   ├── mindmaps/
│   │   └── README.md            # Mind map module technical docs
│   │
│   ├── patterndocs/
│   │   └── README.md            # Pattern docs module technical docs
│   │
│   └── prompts/
│       └── README.md            # AI prompts documentation
│
└── .dev/                        # 🔒 Maintainer documentation
    ├── README.md                # Maintainer guide
    ├── TESTING.md               # Testing documentation
    ├── VIRTUAL_ENV_SETUP.md     # Virtual environment guide
    └── DOCUMENTATION_ARCHITECTURE.md  # This file
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
- `tools/README.md` → Tools reference
- `docs/SOLUTION_CONTRACT.md` → Solution format
- `.dev/TESTING.md` → Test requirements

### 🛠️ Maintainers (Core Team)

**What they need:**
- Internal architecture
- Release process
- Module deep-dives

**Where to find:**
- `.dev/README.md` → Maintainer guide
- `tools/*/README.md` → Module details
- `.dev/DOCUMENTATION_ARCHITECTURE.md` → This file

---

## 📋 Documentation Checklist

### When Adding a New Feature

- [ ] Update `README.md` if user-facing
- [ ] Update `tools/README.md` if developer tool
- [ ] Add module README if new module
- [ ] Update relevant CONTRACT files if API change

### When Adding a New Tool

- [ ] Add to `tools/README.md` quick reference table
- [ ] Add detailed section in `tools/README.md`
- [ ] Create `tools/<module>/README.md` if complex
- [ ] Add tests to `.dev/tests/` or `tools/tests/`

### When Modifying Documentation Structure

- [ ] Update this file (`DOCUMENTATION_ARCHITECTURE.md`)
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

### Why separate `docs/` from `tools/`?

- `docs/` → Published to website, user-facing
- `tools/` → GitHub-only, developer-facing

Different audiences, different update cycles, different review requirements.

### Why `.dev/` for maintainer docs?

- Clearly signals "internal" documentation
- Keeps root directory clean
- Groups with test files (same audience)

### Why not put everything in `docs/`?

- MkDocs publishes everything in `docs/` to the website
- Internal documentation shouldn't be public-facing
- Separation allows different access controls

### How do I know where to add new documentation?

Ask: **Who is the primary reader?**

| Reader | Location |
|--------|----------|
| User learning the framework | `docs/` |
| Contributor adding features | `tools/README.md` |
| Maintainer debugging issues | `.dev/` |

---

## 📝 Update Log

- **2025-12-12**: Initial version - Documented architecture after consolidating tools documentation

---

## 🔗 Related Documents

- [Maintainer Guide](.dev/README.md)
- [Testing Documentation](.dev/TESTING.md)
- [MkDocs Content Guide](docs/MKDOCS_CONTENT_GUIDE.md)
- [Tools Reference](tools/README.md)


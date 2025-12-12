# MkDocs Website Content Guide

This document explains which content is **NOT** included in the MkDocs-generated website and how to properly link to these resources in README.md.

---

## 📋 Table of Contents

- [Content Included in Website](#content-included-in-website)
- [Content NOT Included in Website](#content-not-included-in-website)
- [Linking Strategy Guide](#linking-strategy-guide)
- [Frequently Asked Questions](#frequently-asked-questions)

---

## 🌐 Content Included in Website

Based on the `nav` configuration in `mkdocs.yml`, the following content is included in the MkDocs website:

### ✅ Included Pages

| Path | Description | Website URL |
|:-----|:------------|:------------|
| `docs/index.md` | Homepage (includes README.md content) | `https://lufftw.github.io/neetcode/` |
| `docs/index_zh-TW.md` | Traditional Chinese homepage | `https://lufftw.github.io/neetcode/index_zh-TW/` |
| `docs/patterns/*.md` | Pattern documentation | `https://lufftw.github.io/neetcode/patterns/...` |
| `docs/mindmaps/*.md` | All mind map Markdown files | `https://lufftw.github.io/neetcode/mindmaps/...` |
| `docs/pages/mindmaps/*.html` | Interactive mind map HTML files | `https://lufftw.github.io/neetcode/pages/mindmaps/...` |
| `docs/SOLUTION_CONTRACT.md` | Solution file specification | `https://lufftw.github.io/neetcode/SOLUTION_CONTRACT/` |
| `docs/GENERATOR_CONTRACT.md` | Generator file specification | `https://lufftw.github.io/neetcode/GENERATOR_CONTRACT/` |
| `docs/ARCHITECTURE_MIGRATION.md` | Architecture migration guide | `https://lufftw.github.io/neetcode/ARCHITECTURE_MIGRATION/` |
| `docs/GITHUB_PAGES_SETUP.md` | GitHub Pages deployment guide | `https://lufftw.github.io/neetcode/GITHUB_PAGES_SETUP/` |

### 📝 Special Notes

- **README.md** and **README_zh-TW.md**: These files do **NOT** appear as separate pages on the website. Instead, they are included in `docs/index.md` and `docs/index_zh-TW.md` via the `include-markdown` plugin.
- **docs/patterns/**: ✅ Now configured in `nav` and available on the website.
- **docs/GITHUB_PAGES_SETUP.md**: ✅ Now configured in `nav` and available on the website.
- **Reference docs**: ✅ `SOLUTION_CONTRACT.md`, `GENERATOR_CONTRACT.md`, and `ARCHITECTURE_MIGRATION.md` are now configured in `nav`.
- **Tools docs**: Developer tools documentation is in [`tools/README.md`](https://github.com/lufftw/neetcode/blob/main/tools/README.md) (not on website, GitHub only).

---

## ❌ Content NOT Included in Website

The following directories and files **do NOT** appear in the MkDocs website and can only be accessed via the GitHub repository:

### 📁 Code Directories

| Directory/File | Description | GitHub Link Format |
|:---------------|:------------|:-------------------|
| `solutions/` | Solution code files | `https://github.com/lufftw/neetcode/blob/main/solutions/...` |
| `tests/` | Test case files | `https://github.com/lufftw/neetcode/blob/main/tests/...` |
| `generators/` | Random test generators | `https://github.com/lufftw/neetcode/blob/main/generators/...` |
| `runner/` | Test execution engine | `https://github.com/lufftw/neetcode/blob/main/runner/...` |
| `templates/` | Problem templates | `https://github.com/lufftw/neetcode/blob/main/templates/...` |

### 🛠️ Tools and Configuration

| Directory/File | Description | GitHub Link Format |
|:---------------|:------------|:-------------------|
| `tools/*.py` | Tool scripts (code only) | `https://github.com/lufftw/neetcode/blob/main/tools/...` |
| `tools/README.md` | Comprehensive tools reference | `https://github.com/lufftw/neetcode/blob/main/tools/README.md` |
| `ontology/` | Algorithm ontology data (TOML) | `https://github.com/lufftw/neetcode/blob/main/ontology/...` |
| `meta/` | Problem and pattern metadata | `https://github.com/lufftw/neetcode/blob/main/meta/...` |
| `roadmaps/` | Learning path definitions | `https://github.com/lufftw/neetcode/blob/main/roadmaps/...` |
| `.vscode/` | VS Code configuration | `https://github.com/lufftw/neetcode/blob/main/.vscode/...` |
| `.github/` | GitHub Actions configuration | `https://github.com/lufftw/neetcode/blob/main/.github/...` |

### 📚 Documentation (Not in nav)

| File | Description | GitHub Link Format |
|:-----|:------------|:-------------------|
| `docs/ONTOLOGY_DESIGN.md` | Ontology design documentation | `https://github.com/lufftw/neetcode/blob/main/docs/ONTOLOGY_DESIGN.md` |
| `docs/MKDOCS_CONTENT_GUIDE.md` | This file | `https://github.com/lufftw/neetcode/blob/main/docs/MKDOCS_CONTENT_GUIDE.md` |

**Note**: The following docs are now configured in `nav` and available on the website:

- `docs/patterns/` - Pattern documentation
- `docs/GITHUB_PAGES_SETUP.md` - GitHub Pages setup guide
- `docs/SOLUTION_CONTRACT.md` - Solution file specification
- `docs/GENERATOR_CONTRACT.md` - Generator file specification
- `docs/ARCHITECTURE_MIGRATION.md` - Architecture migration guide

See [Content Included in Website](#content-included-in-website) section above.

### 🔧 Maintainer Documentation

| Directory/File | Description | GitHub Link Format |
|:---------------|:------------|:-------------------|
| `.dev/` | Maintainer zone (unit tests) | `https://github.com/lufftw/neetcode/blob/main/.dev/...` |
| `.dev/README.md` | Maintainer guide | `https://github.com/lufftw/neetcode/blob/main/.dev/README.md` |
| `.dev/TESTING.md` | Testing documentation | `https://github.com/lufftw/neetcode/blob/main/.dev/TESTING.md` |

**Note**: Maintainer documentation (`.dev/` directory) is **intentionally NOT** added to the website navigation (`nav` in `mkdocs.yml`) because:
- These are maintainer-only documents (Target Audience: 🔧 Maintainers)
- They are better suited for GitHub repository viewing rather than public website navigation
- Adding them to nav would expose internal documentation to all website visitors
- Badge links (e.g., `.dev/tests/`) should use GitHub absolute URLs since they point to code directories, not documentation pages

### 🐍 Environment Files

| Directory/File | Description | Status |
|:---------------|:------------|:------|
| `leetcode/` | Python virtual environment | Gitignored, not in repository |
| `site/` | MkDocs build output | Gitignored, not in repository |
| `*.pyc`, `__pycache__/` | Python cache files | Gitignored |

---

## 🔗 Linking Strategy Guide

When linking to content in README.md, follow these strategies:

### ✅ Recommended Practices

#### 1. For `.dev/` Directory Files (Not in Website)

**Use full GitHub URLs:**

```markdown
- [`.dev/README.md`](https://github.com/lufftw/neetcode/blob/main/.dev/README.md) — Maintainer guide
- [`.dev/TESTING.md`](https://github.com/lufftw/neetcode/blob/main/.dev/TESTING.md) — Testing documentation
```

#### 2. For `docs/` Directory Files (May Not Be in Website)

**If the document IS configured in `nav`:**
- Use relative paths (MkDocs will automatically convert to website links)
- Or use website URLs (more explicit)

**If the document is NOT configured in `nav`:**
- Use full GitHub URLs

```markdown
<!-- Document in nav - can use relative paths -->
- [📐 Patterns](docs/patterns/) — Pattern documentation
- [GitHub Pages Setup](docs/GITHUB_PAGES_SETUP.md) — Deployment guide

<!-- Document NOT in nav - use GitHub URLs -->
- [`docs/ONTOLOGY_DESIGN.md`](https://github.com/lufftw/neetcode/blob/main/docs/ONTOLOGY_DESIGN.md) — Ontology design documentation
```

#### 3. For Code Files (Not in Website)

**Always use full GitHub URLs:**

```markdown
- [Solution Example](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)
- [Test Generator](https://github.com/lufftw/neetcode/blob/main/generators/0001_two_sum.py)
```

#### 4. For Mind Maps (In Website)

**Use relative paths for Static links (they're in nav), and website URLs for Interactive:**

```markdown
| Mind Map | Links |
|:---------|:------|
| Pattern Hierarchy | [Static](docs/mindmaps/pattern_hierarchy.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/pattern_hierarchy.html) |
```

**Why relative paths work**: All `docs/mindmaps/*.md` files are configured in `nav`, so relative paths automatically work in both GitHub (points to repository) and website (points to website page).

### ❌ Practices to Avoid

1. **Don't** use relative paths in README.md for `.dev/` directory files (they don't exist on the website)
2. **Don't** assume all files in `docs/` are on the website (check `mkdocs.yml` `nav` configuration)
3. **Don't** use `.md` extensions in website links (MkDocs handles this automatically)

---

## ❓ Frequently Asked Questions

### Q: How do I check if a file is on the website?

A: Check the `nav` configuration in `mkdocs.yml`. Only files listed in `nav` appear in the website navigation.

### Q: Is `docs/patterns/` on the website?

A: ✅ Yes! `docs/patterns/` is now configured in `nav` and available on the website at `https://lufftw.github.io/neetcode/patterns/`. You can use relative paths in README.md to link to it.

### Q: Are Reference docs on the website?

A: ✅ Yes! The "📚 Reference" section is now configured in `nav` and includes:

- Solution Contract at `https://lufftw.github.io/neetcode/SOLUTION_CONTRACT/`
- Generator Contract at `https://lufftw.github.io/neetcode/GENERATOR_CONTRACT/`
- Architecture Migration at `https://lufftw.github.io/neetcode/ARCHITECTURE_MIGRATION/`

**Note**: Tools documentation is in [`tools/README.md`](https://github.com/lufftw/neetcode/blob/main/tools/README.md) (GitHub only, not on website).

### Q: Do links in README.md work in both GitHub and the website?

A: It depends on the link type:
- **GitHub absolute URLs**: Work in both GitHub and website, but redirect to GitHub
- **Relative paths**: Point to repository files on GitHub, point to website pages on the website
- **Website absolute URLs**: Work correctly on the website, redirect to website from GitHub

### Q: How do I make links work in both environments?

A: For content not on the website, use GitHub absolute URLs. For content on the website, you can:
1. Use relative paths (MkDocs handles this automatically)
2. Or provide both GitHub and website links

### Q: Why are `.dev/` documents not added to the website navigation?

A: Maintainer documentation (`.dev/README.md`, `.dev/TESTING.md`) is intentionally kept out of the website navigation because:
- **Target Audience**: These documents are for maintainers only (🔧 Maintainers), not general users
- **Better Context**: Maintainer docs are better viewed in GitHub where they're alongside the code and tests
- **Navigation Clarity**: Keeping internal documentation out of public website navigation keeps the site focused on user-facing content
- **Badge Links**: Badge links pointing to `.dev/tests/` should use GitHub URLs since they reference code directories, not documentation pages

If you need to access these documents, use the GitHub absolute URLs provided in README.md.

---

## 📝 Update Log

- **2025-01-XX**: Initial version
- **2025-01-XX**: Updated - Added `docs/patterns/` and `docs/GITHUB_PAGES_SETUP.md` to website navigation
- **2025-12-12**: Added "📚 Reference" section to nav with Solution Contract, Generator Contract, Architecture Migration
- **2025-12-12**: Moved Tools documentation from `docs/TOOLS.md` to `tools/README.md` (developer docs belong with code)
- Check `mkdocs.yml` `nav` configuration for the latest list

---

## 🔍 Quick Reference

### Checklist

Before adding links in README.md, confirm:

- [ ] Is the file in `mkdocs.yml` `nav`?
  - ✅ Yes → Can use relative paths or website URLs
  - ❌ No → Use GitHub absolute URLs
- [ ] Is the file in `.dev/`, `solutions/`, `tests/`, `tools/*.py`, or other code directories?
  - ✅ Yes → Use GitHub absolute URLs
- [ ] Is the file in `docs/` directory but not in `nav`?
  - ✅ Yes → Use GitHub absolute URLs, or add it to `nav` first

---

**Tip**: Regularly check the `nav` configuration in `mkdocs.yml` to ensure your documentation linking strategy stays consistent with the website structure.

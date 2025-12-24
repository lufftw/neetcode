# MkDocs Website Content Guide

> **Status**: Normative  
> **Scope**: MkDocs website content  
> **Last Updated**: {{ git_revision_date_localized }}  
> **Created**: {{ git_creation_date_localized }}

This document explains which content is **NOT** included in the MkDocs-generated website and how to properly link to these resources in README.md.

---

## 📋 Table of Contents

- [Content Included in Website](#content-included-in-website)
- [Content NOT Included in Website](#content-not-included-in-website)
- [Linking Strategy Guide](#linking-strategy-guide)
- [Frequently Asked Questions](#frequently-asked-questions)

---

## 🌐 Content Included in Website {#content-included-in-website}

Based on the `nav` configuration in `mkdocs.yml`, the following content is included in the MkDocs website:

### ✅ Included Pages

| Path | Description | Website URL |
|:-----|:------------|:------------|
| `docs/index.md` | Homepage (includes README.md content) | `https://lufftw.github.io/neetcode/` |
| `docs/index_zh-TW.md` | Traditional Chinese homepage | `https://lufftw.github.io/neetcode/index_zh-TW/` |
| `docs/patterns/*.md` | Pattern documentation overview | `https://lufftw.github.io/neetcode/patterns/` |
| `docs/patterns/*/intuition.md` | Pattern intuition guides | `https://lufftw.github.io/neetcode/patterns/.../intuition/` |
| `docs/patterns/*/templates.md` | Pattern template guides | `https://lufftw.github.io/neetcode/patterns/.../templates/` |
| `docs/mindmaps/*.md` | All mind map Markdown files | `https://lufftw.github.io/neetcode/mindmaps/...` |
| `docs/pages/mindmaps/*.html` | Interactive mind map HTML files | `https://lufftw.github.io/neetcode/pages/mindmaps/...` |
| `docs/SOLUTION_CONTRACT.md` | Solution file specification | `https://lufftw.github.io/neetcode/SOLUTION_CONTRACT/` |
| `docs/GENERATOR_CONTRACT.md` | Generator file specification | `https://lufftw.github.io/neetcode/GENERATOR_CONTRACT/` |
| `docs/ARCHITECTURE_MIGRATION.md` | Architecture migration guide | `https://lufftw.github.io/neetcode/ARCHITECTURE_MIGRATION/` |
| `docs/GITHUB_PAGES_SETUP.md` | GitHub Pages deployment guide | `https://lufftw.github.io/neetcode/GITHUB_PAGES_SETUP/` |
| `docs/BUILD_DOCS_MANUAL.md` | Local documentation build (manual method) | `https://lufftw.github.io/neetcode/BUILD_DOCS_MANUAL/` |
| `docs/LOCAL_DOCS_BUILD.md` | Local docs build options | `https://lufftw.github.io/neetcode/LOCAL_DOCS_BUILD/` |
| `docs/ACT_LOCAL_GITHUB_ACTIONS.md` | Run GitHub Actions locally with act | `https://lufftw.github.io/neetcode/ACT_LOCAL_GITHUB_ACTIONS/` |
| `docs/ONTOLOGY_DESIGN.md` | Ontology design documentation | `https://lufftw.github.io/neetcode/ONTOLOGY_DESIGN/` |
| `docs/MKDOCS_CONTENT_GUIDE.md` | MkDocs content guide (this file) | `https://lufftw.github.io/neetcode/MKDOCS_CONTENT_GUIDE/` |

### 📝 Special Notes

- **README.md** and **README_zh-TW.md**: These files do **NOT** appear as separate pages on the website. Instead, they are included in `docs/index.md` and `docs/index_zh-TW.md` via the `include-markdown` plugin.
- **docs/patterns/**: ✅ Now configured in `nav` and available on the website.
- **docs/GITHUB_PAGES_SETUP.md**: ✅ Now configured in `nav` and available on the website.
- **Local build guides**: ✅ `BUILD_DOCS_MANUAL.md` (recommended), `LOCAL_DOCS_BUILD.md`, and `ACT_LOCAL_GITHUB_ACTIONS.md` (optional) are now configured in `nav`.
- **Reference docs**: ✅ `SOLUTION_CONTRACT.md`, `GENERATOR_CONTRACT.md`, `ARCHITECTURE_MIGRATION.md`, and `ONTOLOGY_DESIGN.md` are now configured in `nav`.
- **Guides**: ✅ `MKDOCS_CONTENT_GUIDE.md` is now configured in `nav`.
- **Patterns**: ✅ `backtracking_exploration` pattern is now available in `nav` alongside `sliding_window` and `two_pointers`.
- **Contributors docs**: ✅ Maintainer documentation is now in `docs/contributors/` and available on the website.
- **Tools docs**: ✅ Developer tools documentation is now in `docs/tools/` and available on the website.

---

## ❌ Content NOT Included in Website {#content-not-included-in-website}

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
| `ontology/` | Algorithm ontology data (TOML) | `https://github.com/lufftw/neetcode/blob/main/ontology/...` |
| `meta/` | Problem and pattern metadata | `https://github.com/lufftw/neetcode/blob/main/meta/...` |
| `roadmaps/` | Learning path definitions | `https://github.com/lufftw/neetcode/blob/main/roadmaps/...` |
| `.vscode/` | VS Code configuration | `https://github.com/lufftw/neetcode/blob/main/.vscode/...` |
| `.github/` | GitHub Actions configuration | `https://github.com/lufftw/neetcode/blob/main/.github/...` |

**Note**: Tools documentation (`tools/README.md` and module-specific READMEs) has been moved to `docs/tools/` and is now available on the website. See [Content Included in Website](#content-included-in-website) section above.

### 📚 Documentation (Not in nav)

**Note**: All major documentation files are now configured in `nav` and available on the website. See [Content Included in Website](#content-included-in-website) section above for the complete list.

The following files are **intentionally NOT** in the website navigation (GitHub only):
- Internal development notes and drafts
- Temporary documentation files

### 🔧 Maintainer Documentation

| Directory/File | Description | GitHub Link Format |
|:---------------|:------------|:-------------------|
| `.dev/` | Maintainer zone (unit tests, test scripts) | `https://github.com/lufftw/neetcode/blob/main/.dev/...` |
| `.dev/README.md` | Maintainer guide (shortened version, links to full docs) | `https://github.com/lufftw/neetcode/blob/main/.dev/README.md` |
| `tools/README.md` | Tools overview (shortened version, links to full docs) | `https://github.com/lufftw/neetcode/blob/main/tools/README.md` |

**Note**: Full maintainer documentation (`.dev/README.md`, `.dev/TESTING.md`, `.dev/DOCUMENTATION_ARCHITECTURE.md`, `.dev/VIRTUAL_ENV_SETUP.md`) has been moved to `docs/contributors/` and is now available on the website. The original `.dev/README.md` and `tools/README.md` now contain shortened versions with links to the full documentation on the website.

**Note**: Full maintainer and tools documentation has been moved to `docs/contributors/` and `docs/tools/` respectively, and is now available on the website under the "Contributors" and "Tools" navigation sections. The original `.dev/README.md` and `tools/README.md` contain shortened versions for GitHub repository browsing convenience, with links to the full documentation on the website.
- Badge links (e.g., `.dev/tests/`) should use GitHub absolute URLs since they point to code directories, not documentation pages

### 🐍 Environment Files

| Directory/File | Description | Status |
|:---------------|:------------|:------|
| `leetcode/` | Python virtual environment | Gitignored, not in repository |
| `site/` | MkDocs build output | Gitignored, not in repository |
| `*.pyc`, `__pycache__/` | Python cache files | Gitignored |

---

## 🔗 Linking Strategy Guide {#linking-strategy-guide}

When linking to content in documentation files, follow these strategies:

### 📋 Core Linking Rules

**General Principle**: 
- ✅ **Files inside `docs/` directory**: Use relative paths (MkDocs automatically handles these)
- ✅ **Files outside `docs/` directory**: Use GitHub absolute URLs

This ensures links work correctly in both GitHub repository browsing and the MkDocs website.

### ✅ Recommended Practices

#### 1. For Maintainer Documentation (Now in `docs/contributors/`)

**Full documentation has been moved to `docs/contributors/` and is available on the website. Use relative paths:**

```markdown
- [Contributors Overview](docs/contributors/README.md) — Maintainer guide
- [Testing Documentation](docs/contributors/TESTING.md) — Testing documentation
- [Documentation Architecture](docs/contributors/DOCUMENTATION_ARCHITECTURE.md) — Documentation structure
- [Virtual Environment Setup](docs/contributors/VIRTUAL_ENV_SETUP.md) — Environment setup guide
```

**Why relative paths work**: All files in `docs/contributors/` are configured in `nav`, so relative paths automatically work in both GitHub (points to repository) and website (points to website page).

**Note**: The original `.dev/README.md` now contains a shortened version with links to the full documentation on the website. This maintains GitHub browsing context while centralizing full content in `docs/`.

#### 2. For Tools Documentation (Now in `docs/tools/`)

**Full documentation has been moved to `docs/tools/` and is available on the website. Use relative paths:**

```markdown
- [Tools Overview](docs/tools/README.md) — Complete tools reference
- [AI Markmap Agent](docs/tools/ai-markmap-agent/README.md) — AI-powered mind map generation
- [Mind Maps Generator](docs/tools/mindmaps/README.md) — Rule-based mind map generation
- [Pattern Docs Generator](docs/tools/patterndocs/README.md) — Pattern documentation generation
```

**Why relative paths work**: All files in `docs/tools/` are configured in `nav`, so relative paths automatically work in both GitHub (points to repository) and website (points to website page).

**Note**: The original `tools/README.md` now contains a shortened version with links to the full documentation on the website. This maintains GitHub browsing context while centralizing full content in `docs/`.

#### 3. For Other `docs/` Directory Files (May Not Be in Website)

**If the document IS configured in `nav`:**
- Use relative paths (MkDocs will automatically convert to website links)
- Or use website URLs (more explicit)

**If the document is NOT configured in `nav`:**
- Use full GitHub URLs

```markdown
<!-- Document in nav - can use relative paths -->
- [📐 Patterns](docs/patterns/) — Pattern documentation overview
- [Sliding Window Intuition](docs/patterns/sliding_window/intuition.md) — Sliding window intuition guide
- [Sliding Window Templates](docs/patterns/sliding_window/templates.md) — Sliding window templates
- [Two Pointers Intuition](docs/patterns/two_pointers/intuition.md) — Two pointers intuition guide
- [Two Pointers Templates](docs/patterns/two_pointers/templates.md) — Two pointers templates
- [Backtracking Exploration Intuition](docs/patterns/backtracking_exploration/intuition.md) — Backtracking intuition guide
- [Backtracking Exploration Templates](docs/patterns/backtracking_exploration/templates.md) — Backtracking templates
- [GitHub Pages Setup](docs/GITHUB_PAGES_SETUP.md) — Deployment guide
- [Build Documentation Locally](docs/BUILD_DOCS_MANUAL.md) — Manual build method (recommended)
- [Local Docs Build Options](docs/LOCAL_DOCS_BUILD.md) — Build options guide
- [Run GitHub Actions Locally](docs/ACT_LOCAL_GITHUB_ACTIONS.md) — Act method (optional, advanced)
- [Ontology Design](docs/ONTOLOGY_DESIGN.md) — Ontology design documentation
- [MkDocs Content Guide](docs/MKDOCS_CONTENT_GUIDE.md) — Content guide (this file)
```

#### 4. For Code Files (Not in Website)

**Always use full GitHub URLs:**

```markdown
- [Solution Example](https://github.com/lufftw/neetcode/blob/main/solutions/0001_two_sum.py)
- [Test Generator](https://github.com/lufftw/neetcode/blob/main/generators/0001_two_sum.py)
- [Runner README](https://github.com/lufftw/neetcode/blob/main/runner/README.md)
- [LICENSE](https://github.com/lufftw/neetcode/blob/main/LICENSE)
- [pytest.ini](https://github.com/lufftw/neetcode/blob/main/pytest.ini)
- [requirements.txt](https://github.com/lufftw/neetcode/blob/main/requirements.txt)
```

**Why**: These files are not in `docs/` and won't be accessible on the MkDocs website. GitHub URLs ensure they work in both GitHub and website contexts.

#### 5. For Mind Maps (In Website)

**Use relative paths for Static links (they're in nav), and website URLs for Interactive:**

```markdown
| Mind Map | Links |
|:---------|:------|
| Pattern Hierarchy | [Static](docs/mindmaps/pattern_hierarchy.md) · [Interactive ✨](https://lufftw.github.io/neetcode/pages/mindmaps/pattern_hierarchy.html) |
```

**Why relative paths work**: All `docs/mindmaps/*.md` files are configured in `nav`, so relative paths automatically work in both GitHub (points to repository) and website (points to website page).

### 📋 Document Migration Strategy

To ensure all documentation is accessible via MkDocs website while maintaining GitHub browsing context, we follow this migration pattern:

1. **Move full documentation to `docs/` directory**:
   - Maintainer documentation → `docs/contributors/`
   - Tools documentation → `docs/tools/`

2. **Create shortened READMEs in original locations**:
   - `.dev/README.md` → Brief overview + links to full docs on website
   - `tools/README.md` → Brief overview + links to full docs on website

3. **Update navigation in `mkdocs.yml`**:
   - Add new sections to `nav` for migrated documentation

4. **Update all links to use relative paths**:
   - Since migrated files are in `docs/` and in `nav`, relative paths work in both GitHub and website

**Benefits of this approach**:
- ✅ All documentation accessible on MkDocs website
- ✅ Maintains GitHub browsing context with shortened READMEs
- ✅ Links work correctly in both GitHub and website
- ✅ Single source of truth for full documentation content

### 📐 Link Strategy Summary

| File Location | Link Type | Example |
|:--------------|:----------|:--------|
| Inside `docs/` (in `nav`) | Relative path | `[README](README.md)` or `[Tools](../tools/README.md)` |
| Inside `docs/` (not in `nav`) | GitHub URL | `[Internal Doc](https://github.com/lufftw/neetcode/blob/main/docs/internal.md)` |
| Outside `docs/` (code/config) | GitHub URL | `[Runner](https://github.com/lufftw/neetcode/blob/main/runner/README.md)` |
| Outside `docs/` (root files) | GitHub URL | `[LICENSE](https://github.com/lufftw/neetcode/blob/main/LICENSE)` |

**Quick Decision Tree**:
1. Is the file in `docs/` directory? 
   - ✅ Yes → Check if it's in `nav`:
     - ✅ In `nav` → Use relative path
     - ❌ Not in `nav` → Use GitHub URL
   - ❌ No → Use GitHub URL

### ❌ Practices to Avoid

1. **Don't** use relative paths for files outside `docs/` directory (they won't work on the website)
2. **Don't** use relative paths like `../runner/README.md` or `../../meta/patterns/README.md` (these point outside `docs/`)
3. **Don't** assume all files in `docs/` are on the website (check `mkdocs.yml` `nav` configuration)
4. **Don't** use `.md` extensions in website links (MkDocs handles this automatically)
5. **Don't** create duplicate documentation in multiple locations (use the migration strategy above)
6. **Don't** mix relative paths and GitHub URLs inconsistently (follow the strategy above)

---

## ❓ Frequently Asked Questions {#frequently-asked-questions}

### Q: How do I check if a file is on the website?

A: Check the `nav` configuration in `mkdocs.yml`. Only files listed in `nav` appear in the website navigation.

### Q: Is `docs/patterns/` on the website?

A: ✅ Yes! `docs/patterns/` is now configured in `nav` and available on the website at `https://lufftw.github.io/neetcode/patterns/`. You can use relative paths in README.md to link to it.

### Q: Are Reference docs on the website?

A: ✅ Yes! The "📚 Reference" section is now configured in `nav` and includes:

- Solution Contract at `https://lufftw.github.io/neetcode/SOLUTION_CONTRACT/`
- Generator Contract at `https://lufftw.github.io/neetcode/GENERATOR_CONTRACT/`
- Architecture Migration at `https://lufftw.github.io/neetcode/ARCHITECTURE_MIGRATION/`
- Ontology Design at `https://lufftw.github.io/neetcode/ONTOLOGY_DESIGN/`

**Note**: Tools documentation has been moved to `docs/tools/` and is now available on the website under the "Tools" navigation section. The original `tools/README.md` now contains a shortened version with links to the full documentation.

### Q: What patterns are available on the website?

A: ✅ The following patterns are now configured in `nav`:

- **Sliding Window**
  - Intuition: `https://lufftw.github.io/neetcode/patterns/sliding_window/intuition/`
  - Templates: `https://lufftw.github.io/neetcode/patterns/sliding_window/templates/`
- **Two Pointers**
  - Intuition: `https://lufftw.github.io/neetcode/patterns/two_pointers/intuition/`
  - Templates: `https://lufftw.github.io/neetcode/patterns/two_pointers/templates/`
- **Backtracking Exploration**
  - Intuition: `https://lufftw.github.io/neetcode/patterns/backtracking_exploration/intuition/`
  - Templates: `https://lufftw.github.io/neetcode/patterns/backtracking_exploration/templates/`

Each pattern includes both Intuition and Templates documentation as separate pages in the navigation.

### Q: Do links in README.md work in both GitHub and the website?

A: It depends on the link type:
- **GitHub absolute URLs**: Work in both GitHub and website, but redirect to GitHub
- **Relative paths**: Point to repository files on GitHub, point to website pages on the website
- **Website absolute URLs**: Work correctly on the website, redirect to website from GitHub

### Q: How do I make links work in both environments?

A: For content not on the website, use GitHub absolute URLs. For content on the website, you can:
1. Use relative paths (MkDocs handles this automatically)
2. Or provide both GitHub and website links

### Q: Where are maintainer and tools documents now?

A: Full maintainer and tools documentation has been **migrated to the website**:

- **Maintainer documentation** → `docs/contributors/` (available on website under "Contributors" section)
  - `docs/contributors/README.md` - Full maintainer guide
  - `docs/contributors/TESTING.md` - Complete testing documentation
  - `docs/contributors/DOCUMENTATION_ARCHITECTURE.md` - Documentation structure
  - `docs/contributors/VIRTUAL_ENV_SETUP.md` - Virtual environment setup

- **Tools documentation** → `docs/tools/` (available on website under "Tools" section)
  - `docs/tools/README.md` - Complete tools reference
  - `docs/tools/ai-markmap-agent/README.md` - AI Markmap Agent documentation
  - `docs/tools/mindmaps/README.md` - Mind Maps Generator documentation
  - `docs/tools/patterndocs/README.md` - Pattern Docs Generator documentation

**Original locations now contain shortened versions**:
- `.dev/README.md` - Shortened version with links to full docs on website
- `tools/README.md` - Shortened version with links to full docs on website

**Why this migration?**
- ✅ Makes all documentation accessible via MkDocs website
- ✅ Maintains GitHub browsing context with shortened READMEs
- ✅ Single source of truth for full documentation content
- ✅ Links work correctly in both GitHub and website using relative paths

**How to link to these documents**: Use relative paths (e.g., `docs/contributors/README.md`) since they're now in `docs/` and configured in `nav`.

### Q: How do I manually embed revision dates in Markdown files?

A: The `git-revision-date-localized` plugin provides template variables that you can use in your Markdown files. Here's how to use them:

**Basic usage in `.md` files:**

```markdown
# My Page Title

Last updated: {{ git_revision_date_localized }}

Created: {{ git_creation_date_localized }}
```

**Note:** Both formats can be used in Markdown files and are **compatible** with each other:
- Without `page.meta.` prefix: Simpler, follows plugin config format
- With `page.meta.` prefix: Access to additional formats (raw ISO, timeago, etc.)

Example using both formats together:
```markdown
Last updated: {{ git_revision_date_localized }}
Raw ISO: {{ page.meta.git_revision_date_localized_raw_iso_datetime }}
```

**Output example** (assuming last commit on 2025-12-17):

```
Last updated: December 17, 2025 14:26
Created: January 1, 2024
(Raw ISO datetime: 2025-12-17T14:26:00+08:00)
```

**Available template variables:**

For direct use in Markdown files (without `page.meta.` prefix):
| Variable | Description |
|:---------|:------------|
| `{{ git_revision_date_localized }}` | Last modified date (formatted according to plugin config) |
| `{{ git_creation_date_localized }}` | Creation date (first commit) |
| `{{ git_site_revision_date_localized }}` | Site-wide last update time (not per-page) |

Also available in Markdown files (with `page.meta.` prefix - provides more format options):
| Variable | Description |
|:---------|:------------|
| `{{ page.meta.git_revision_date_localized }}` | Last modified date (same as above, but accessible in theme templates too) |
| `{{ page.meta.git_creation_date_localized }}` | Creation date (same as above, but accessible in theme templates too) |
| `{{ page.meta.git_revision_date_localized_raw_iso_datetime }}` | Raw ISO datetime format (e.g., "2025-12-17T14:26:00+08:00") |
| `{{ page.meta.git_revision_date_localized_timeago }}` | Time ago format (e.g., "3 days ago") - requires timeago.js |

**Key Points:**
- ✅ Both formats can be used together in the same Markdown file
- ✅ Without `page.meta.` prefix: Simpler, follows plugin config (recommended for most cases)
- ✅ With `page.meta.` prefix: Access to raw formats and timeago, also works in theme templates

**Note**: The plugin configuration in `mkdocs.yml` determines the format and locale of these dates. See `mkdocs.yml` for current settings (locale: en, timezone: Asia/Taipei, type: datetime).

### Q: How do I customize the sitemap.xml to use Git commit dates for lastmod?

A: By default, MkDocs generates a `sitemap.xml` where all pages have the same `lastmod` date (the build date). To use individual Git commit dates for each page's `lastmod`, you can override the sitemap template.

**Steps to override sitemap.xml:**

1. **Create the overrides directory:**
   ```bash
   mkdir docs/overrides
   ```

2. **Create the custom sitemap template:**
   Create `docs/overrides/sitemap.xml` with the following content:
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
     {%- for file in pages -%}
       {% if not file.page.is_link and (file.page.abs_url or file.page.canonical_url) %}
         <url>
           <loc>{% if file.page.canonical_url %}{{ file.page.canonical_url|e }}{% else %}{{ file.page.abs_url|e }}{% endif %}</loc>
           {%- if not file.page.meta.template and file.page.meta.git_revision_date_localized_raw_iso_datetime %}
             <lastmod>{{ (file.page.meta.git_revision_date_localized_raw_iso_datetime + "+00:00") | replace(" ", "T") }}</lastmod>
           {%- endif %}
           <changefreq>daily</changefreq>
         </url>
       {% endif -%}
     {% endfor %}
   </urlset>
   ```

3. **Enable custom_dir in mkdocs.yml:**
   Add `custom_dir: docs/overrides` to the theme configuration:
   ```yaml
   theme:
     name: material
     language: en
     custom_dir: docs/overrides
     # ... other theme settings
   ```

**How it works:**
- The template uses `git_revision_date_localized_raw_iso_datetime` from the `git-revision-date-localized` plugin
- Each page's `lastmod` will reflect its actual last Git commit date
- The date format is converted to ISO 8601 (replacing spaces with "T" and adding timezone)
- Only pages with Git dates will include the `lastmod` tag

**Requirements:**
- The `git-revision-date-localized` plugin must be enabled in `mkdocs.yml`
- The plugin must be configured to provide `raw_iso_datetime` format (this is the default)

After building the documentation, each page in `sitemap.xml` will have its own `lastmod` date based on when it was last committed to Git, rather than all pages sharing the same build date.

---

## 📝 Update Log

- **2025-12-12**: Initial version
- **2025-12-12**: Updated - Added `docs/patterns/` and `docs/GITHUB_PAGES_SETUP.md` to website navigation
- **2025-12-12**: Added "📚 Reference" section to nav with Solution Contract, Generator Contract, Architecture Migration
- **2025-12-12**: Moved Tools documentation from `docs/TOOLS.md` to `tools/README.md` (developer docs belong with code)
- **2025-12-13**: Added local documentation build guides - `BUILD_DOCS_MANUAL.md` (recommended) and `ACT_LOCAL_GITHUB_ACTIONS.md` (optional) to Guides section
- **2025-12-14**: Added `ONTOLOGY_DESIGN.md` to Reference section
- **2025-12-15**: Added `MKDOCS_CONTENT_GUIDE.md` and `LOCAL_DOCS_BUILD.md` to Guides section
- **2025-12-17**: Added `backtracking_exploration` pattern to Patterns section
- **2025-12-20**: Added FAQ section on manually embedding revision dates in Markdown files using git-revision-date-localized plugin template variables
- **2025-12-20**: Added FAQ section on customizing sitemap.xml to use Git commit dates for lastmod
- **2025-12-24**: Enhanced linking strategy guide with core rules, decision tree, and examples for files inside/outside `docs/` directory
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

# GitHub Pages Deployment Guide: Interactive Mind Maps

This guide explains how to deploy mind maps to GitHub Pages with full interactive functionality.

---

## 📊 Complete Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Mind Map Generation & Deployment Flow                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐       │
│  │   Source  │ ──→ │ Generator │ ──→ │  Output   │ ──→ │ GitHub   │       │
│  └──────────┘     └──────────┘     └──────────┘     │ Pages    │       │
│                                                      └──────────┘       │
│  • ontology/*.toml   generate_         • *.md (static)                  │
│  • meta/problems/    mindmaps.py       • *.html (interactive)  Auto     │
│  • Any text          text_to_                      Deploy               │
│                      mindmap.py                                          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🗂️ Directory Structure

```
neetcode/
├── docs/
│   ├── mindmaps/
│   │   ├── index.md                    # Mind map index
│   │   ├── pattern_hierarchy.md        # Static Markdown version
│   │   ├── algorithm_usage.md
│   │   └── ...
│   │
│   ├── pages/                          # 🆕 GitHub Pages root (gitignored)
│   │   ├── mindmaps/                   # Interactive HTML mind maps
│   │   │   ├── pattern_hierarchy.html
│   │   │   └── ...
│   │   └── ...
│   │
│   ├── stylesheets/                    # Custom CSS
│   ├── index.md                        # Homepage (includes README.md)
│   ├── index_zh-TW.md                  # Homepage (Traditional Chinese)
│   └── GITHUB_PAGES_SETUP.md          # This file
│
├── tools/
│   ├── generate_mindmaps.py            # Generate from ontology
│   ├── text_to_mindmap.py              # Generate from any text
│   └── generate_mindmaps.toml          # Configuration
│
├── .github/
│   └── workflows/
│       └── deploy-pages.yml            # 🆕 Auto deployment
│
├── mkdocs.yml                          # MkDocs configuration
└── site/                               # 🆕 MkDocs build output (gitignored)
```

---

## 🚀 Quick Start: Local Development

### Build MkDocs Documentation Locally

Before deploying to GitHub Pages, you can preview the documentation locally:

```bash
# 1. Activate virtual environment
# Windows
.\leetcode\Scripts\activate.ps1

# Linux/macOS
source leetcode/bin/activate

# 2. Install dependencies (if not already installed)
pip install -r requirements.txt

# 3. Build MkDocs site
python -m mkdocs build

# 4. Preview locally
python -m mkdocs serve
# Visit http://127.0.0.1:8000
```

**Output:** The built site will be in the `site/` directory.

### Generate Mind Maps Locally

```bash
# Generate Markdown mind maps
python tools/generate_mindmaps.py

# Generate HTML (interactive) mind maps
python tools/generate_mindmaps.py --html

# Use autoloader mode
python tools/generate_mindmaps.py --html --autoloader
```

**Note:** Generated HTML files are saved to `docs/pages/mindmaps/` (gitignored).

---

## Step 1: Setup MkDocs Configuration

### 1.1 Install Dependencies

```bash
pip install mkdocs-material mkdocs-include-markdown-plugin mkdocs-minify-plugin
```

### 1.2 Configure `mkdocs.yml`

The `mkdocs.yml` file is already configured with:
- Material theme
- `include-markdown` plugin (includes README.md directly)
- Custom CSS for badges and tables
- Navigation structure

---

## Step 2: Build and Preview Locally

### 2.1 Build Documentation

```bash
# Build static site
python -m mkdocs build

# Output directory: site/
```

### 2.2 Preview Locally

```bash
# Start development server
python -m mkdocs serve

# Visit http://127.0.0.1:8000
# The server auto-reloads on file changes
```

### 2.3 Common Build Commands

```bash
# Build with verbose output
python -m mkdocs build --verbose

# Build and check for broken links
python -m mkdocs build --strict

# Clean build (remove site/ directory first)
rm -rf site/  # Linux/macOS
Remove-Item -Recurse -Force site/  # Windows PowerShell
python -m mkdocs build
```

---

## Step 3: Generate Interactive Mind Maps

### 3.1 Generate HTML Mind Maps

```bash
# Generate all interactive mind maps
python tools/generate_mindmaps.py --html

# Generate specific mind map
python tools/generate_mindmaps.py --html --type pattern_hierarchy

# Use autoloader mode (optional)
python tools/generate_mindmaps.py --html --autoloader
```

**Output:** HTML files are generated in `docs/pages/mindmaps/`

### 3.2 Preview Mind Maps Locally

```bash
# Method 1: Open HTML directly
# Windows
start docs/pages/mindmaps/pattern_hierarchy.html

# Linux/macOS
open docs/pages/mindmaps/pattern_hierarchy.html

# Method 2: Use HTTP server
cd docs/pages
python -m http.server 8000
# Visit http://localhost:8000/mindmaps/pattern_hierarchy.html
```

---

## Step 4: Configure GitHub Actions for Auto Deployment

### 4.1 Workflow Configuration

The `.github/workflows/deploy-pages.yml` file handles automatic deployment:

```yaml
# .github/workflows/deploy-pages.yml
name: Deploy Documentation to GitHub Pages

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - 'mkdocs.yml'
      - 'requirements.txt'
      - 'ontology/**'
      - 'meta/**'
  workflow_dispatch:  # Allow manual trigger

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Generate mind maps
        run: python tools/generate_mindmaps.py --html
      
      - name: Build MkDocs site
        run: python -m mkdocs build
      
      - name: Setup Pages
        uses: actions/configure-pages@v4
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: 'site'

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

---

## Step 5: Enable GitHub Pages

### 5.1 GitHub Settings

1. Go to your Repository → **Settings**
2. Find **Pages** in the left sidebar
3. Under "Source", select **GitHub Actions**

### 5.2 First Deployment

```bash
# 1. Ensure file structure is correct
# 2. Commit and push
git add .
git commit -m "feat: setup GitHub Pages with MkDocs"
git push origin main

# 3. GitHub Actions will automatically deploy
# 4. Visit: https://yourusername.github.io/neetcode/
```

---

## Step 6: Update README with Links

The README.md already includes links to interactive mind maps:

```markdown
## 🧠 Interactive Mind Maps

| Mind Map | Description | Links |
|:---------|:------------|:------|
| 📐 Pattern Hierarchy | API Kernels → Patterns → Problems | [Static](docs/mindmaps/pattern_hierarchy.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#pattern-hierarchy) |
| 👨‍👩‍👧‍👦 Family Derivation | Base templates → Derived variants | [Static](docs/mindmaps/family_derivation.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#family-derivation) |
| ⚡ Algorithm Usage | Problems by algorithm | [Static](docs/mindmaps/algorithm_usage.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#algorithm-usage) |
| 🏗️ Data Structure Usage | Problems by data structure | [Static](docs/mindmaps/data_structure.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#data-structure-usage) |
| 🏢 Company Coverage | Company-specific problems | [Static](docs/mindmaps/company_coverage.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#company-coverage) |
| 🗺️ Learning Roadmaps | NeetCode 150, Blind 75, etc. | [Static](docs/mindmaps/roadmap_paths.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#learning-roadmaps) |
| 🔗 Problem Relations | Related problems network | [Static](docs/mindmaps/problem_relations.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#problem-relations) |
| 🔀 Solution Variants | Multiple approaches | [Static](docs/mindmaps/solution_variants.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#solution-variants) |
| 📊 Difficulty × Topics | Topics by difficulty | [Static](docs/mindmaps/difficulty_topics.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#difficulty-topics) |

👉 **[View All Interactive Mind Maps](https://lufftw.github.io/neetcode/mindmaps/)**
```

---

## 🔄 Complete Workflow Summary

```
1. Edit ontology/ or meta/problems/
   ↓
2. Generate mind maps locally (optional)
   python tools/generate_mindmaps.py --html
   ↓
3. Build MkDocs site locally (optional)
   python -m mkdocs build
   python -m mkdocs serve  # Preview
   ↓
4. git push (or manually run generation scripts)
   ↓
5. GitHub Actions automatically triggers
   ↓
6. Generate mind maps (Markdown + HTML)
   ↓
7. Build MkDocs site
   python -m mkdocs build
   ↓
8. Deploy to GitHub Pages
   ↓
9. Visit https://yourusername.github.io/neetcode/
   ↓
10. Use interactive mind maps!
    - 🖱️ Drag to pan
    - 🔍 Scroll to zoom
    - 👆 Click to fold/unfold
```

---

## ❓ Frequently Asked Questions

### Q: Why can't GitHub README display interactive content directly?

A: GitHub disables JavaScript execution for security reasons. GitHub Pages is needed to host the interactive version.

### Q: Can I use a custom domain?

A: Yes! Configure it in Settings → Pages → Custom domain.

### Q: How do I update mind maps?

A: After modifying `ontology/` or `meta/`, push to GitHub. GitHub Actions will automatically regenerate and redeploy.

### Q: How do I preview locally?

A: 

**For MkDocs documentation:**
```bash
python -m mkdocs serve
# Visit http://127.0.0.1:8000
```

**For interactive mind maps:**
```bash
# Method 1: Open HTML directly
open docs/pages/mindmaps/pattern_hierarchy.html

# Method 2: Use HTTP server
cd docs/pages
python -m http.server 8000
# Visit http://localhost:8000/mindmaps/pattern_hierarchy.html
```

### Q: How do I fix MkDocs build warnings?

A: Common fixes:
- Remove anchor links from Table of Contents (MkDocs auto-generates navigation)
- Change relative links to `.dev/` to GitHub full URLs
- Ensure all referenced files exist in `docs/` directory

### Q: What's the difference between `site/` and `docs/pages/`?

A:
- `site/` - MkDocs build output (contains full documentation site)
- `docs/pages/` - Generated HTML mind maps (used by GitHub Pages)

Both are gitignored and regenerated on build/deploy.

---

## 📝 Notes

- **Local Development**: Always test locally with `python -m mkdocs build` and `python -m mkdocs serve` before pushing
- **Build Output**: The `site/` directory contains the complete MkDocs site and is gitignored
- **Mind Maps**: HTML mind maps are generated to `docs/pages/mindmaps/` and are also gitignored
- **Auto Deployment**: GitHub Actions handles generation, building, and deployment automatically

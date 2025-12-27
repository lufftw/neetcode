# GitHub Pages Deployment Guide: Interactive Mind Maps

> **Status**: Informational  
> **Scope**: GitHub Pages deployment  
> **Last Updated**: {{ git_revision_date_localized }}  
> **Created**: {{ git_creation_date_localized }}

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
│   │   ├── index.md                    # Mind map index (tracked)
│   │   ├── README.md                   # Documentation (tracked)
│   │   ├── neetcode_ontology_ai_*.md   # AI mind maps (tracked)
│   │   ├── pattern-hierarchy.md        # Rule-based (gitignored, CI/CD generates)
│   │   ├── algorithm-usage.md          # Rule-based (gitignored, CI/CD generates)
│   │   └── ...
│   │
│   ├── pages/                          # GitHub Pages root (mostly gitignored)
│   │   ├── mindmaps/
│   │   │   ├── neetcode_ontology_ai_*.html  # AI (tracked)
│   │   │   ├── pattern-hierarchy.html       # Rule-based (gitignored)
│   │   │   └── ...
│   │   └── assets/                     # Shared assets (gitignored)
│   │
│   ├── stylesheets/                    # Custom CSS
│   ├── index.md                        # Homepage (includes README.md)
│   ├── index_zh-TW.md                  # Homepage (Traditional Chinese)
│   └── github-pages-setup.md           # This file
│
├── tools/
│   └── mindmaps/                        # Mindmap tools
│       ├── generate_mindmaps.py         # Generate from ontology
│       ├── generate_mindmaps_ai.py      # AI mind map generator
│       ├── text_to_mindmap.py           # Generate from any text
│       └── generate_mindmaps.toml       # Configuration
│
├── .github/
│   └── workflows/
│       └── deploy-pages.yml            # Auto deployment workflow
│
├── mkdocs.yml                          # MkDocs configuration
└── site/                               # MkDocs build output (gitignored)
```

---

## 🚀 Quick Start: Local Development

### Option 1: `act` - Run GitHub Actions Locally (Recommended)

`act` runs the **exact same workflow** as GitHub Actions locally using Docker. This ensures 100% consistency between local and CI/CD builds.

**Install act:**

```bash
# Windows (winget)
winget install nektos.act

# Windows (Chocolatey)
choco install act-cli

# Windows (Scoop)
scoop install act

# macOS
brew install act

# Linux
curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
```

**Usage:**

```bash
# Run the build job (same as CI/CD)
act -j build

# List all available jobs
act -l

# Run with smaller Docker image (faster)
act -j build -P ubuntu-latest=catthehacker/ubuntu:act-latest
```

**What `act` does:**
1. Reads `.github/workflows/deploy-pages.yml`
2. Runs in Docker container (same Ubuntu environment as GitHub)
3. Executes the exact same steps as CI/CD

### Option 2: Manual Steps

```bash
# 1. Activate virtual environment
# Windows
.\leetcode\Scripts\activate.ps1

# Linux/macOS
source leetcode/bin/activate

# 2. Install dependencies (if not already installed)
pip install -r requirements.txt

# 3. Generate mindmaps
python tools/generate_mindmaps.py        # Markdown
python tools/generate_mindmaps.py --html # HTML

# 4. Build MkDocs site
python -m mkdocs build

# 5. Preview locally
python -m mkdocs serve
# Visit http://127.0.0.1:8000
```

**Output:** The built site will be in the `site/` directory.

### Generated Files

**Note:** Generated files are gitignored and regenerated by CI/CD:
- Markdown: `docs/mindmaps/*.md` (except `index.md`, `README.md`, AI files)
- HTML: `docs/pages/mindmaps/*.html` (except AI files)

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

### 3.1 Generate Rule-Based HTML Mind Maps

```bash
# Generate all interactive mind maps (rule-based)
python tools/generate_mindmaps.py --html

# Generate specific mind map
python tools/generate_mindmaps.py --html --type pattern_hierarchy

# Use autoloader mode (optional)
python tools/generate_mindmaps.py --html --autoloader
```

**Output:** HTML files are generated in `docs/pages/mindmaps/`

### 3.2 Generate AI-Powered Mind Maps (Manual Process)

> ⚠️ **Important**: AI mindmaps are **NOT** automatically generated in CI/CD. You must generate them manually and commit the HTML files.

**Why manual?**
- Requires OpenAI API key (should not be stored in CI/CD)
- API calls cost money (better to control when to regenerate)
- Allows review before committing

**Steps:**

1. **Set up API key locally:**
   ```bash
   # Windows PowerShell
   $env:OPENAI_API_KEY = "sk-..."
   
   # Linux/macOS
   export OPENAI_API_KEY="sk-..."
   ```

2. **Generate AI mindmaps:**
   ```bash
   # Generate both English and 繁體中文 versions
   python tools/generate_mindmaps_ai.py --config tools/generate_mindmaps_ai.toml
   
   # Or use interactive mode
   python tools/generate_mindmaps_ai.py
   ```

3. **Verify generated files:**
   ```bash
   # Check that HTML files were created
   ls docs/pages/mindmaps/neetcode_ontology_ai_*.html
   # Should see:
   # - neetcode-ontology-ai-en.html
   # - neetcode-ontology-ai-zh-tw.html
   
   # Check that prompt file was updated
   ls tools/prompts/generated/mindmap-prompt.md
   ```

4. **Review prompt file (optional but recommended):**
   - The prompt used for generation is saved to `tools/prompts/generated/mindmap-prompt.md`
   - This file is **tracked in Git** for traceability — you can always see which prompt generated each version of the AI mind maps
   - Review the prompt to ensure it matches your expectations

5. **Commit and push:**
   ```bash
   # Add AI mindmap HTML files (they are tracked in git)
   git add docs/pages/mindmaps/neetcode_ontology_ai_*.html
   
   # Also commit the prompt file for traceability
   git add tools/prompts/generated/mindmap-prompt.md
   
   git commit -m "docs: Update AI mind maps"
   git push
   ```

6. **CI/CD will automatically deploy** the committed HTML files.

**Why track the prompt file?**
- **Traceability**: You can always see which prompt was used to generate each version of AI mind maps
- **Reproducibility**: Others can understand how the mind maps were generated
- **Transparency**: Makes the AI generation process transparent and auditable

**Configuration:**
- Edit `tools/generate_mindmaps_ai.toml` to customize:
  - Output language(s): `language = ["en", "zh-TW"]`
  - HTML generation: `generate_html = true`
  - Output directory: `html_directory = "docs/pages/mindmaps"`

**Note:** The `.gitignore` file is configured to track AI mindmap HTML files:
```
docs/pages/                    # Ignore all generated HTML
!docs/pages/mindmaps/neetcode_ontology_ai_*.html  # But track AI mindmaps
```

**Prompt File Tracking:**
- The prompt file `tools/prompts/generated/mindmap-prompt.md` is **tracked in Git**
- This ensures full traceability — you can always see which prompt generated each AI mind map version
- The prompt file is automatically updated each time you run `generate_mindmaps_ai.py`

### 3.3 Preview Mind Maps Locally

```bash
# Method 1: Open HTML directly
# Windows
start docs/pages/mindmaps/pattern-hierarchy.html

# Linux/macOS
open docs/pages/mindmaps/pattern-hierarchy.html

# Method 2: Use HTTP server
cd docs/pages
python -m http.server 8000
# Visit http://localhost:8000/mindmaps/pattern-hierarchy.html
```

---

## Step 4: Configure GitHub Actions for Auto Deployment

### 4.1 Workflow Configuration

The `.github/workflows/deploy-pages.yml` file handles automatic deployment:

```yaml
# .github/workflows/deploy-pages.yml
name: Deploy Documentation

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - 'ontology/**'
      - 'meta/**'
      - 'tools/generate_mindmaps.py'
      - 'mkdocs.yml'
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
      
      - name: Generate Mind Maps (Markdown + HTML)
        run: |
          python tools/generate_mindmaps.py        # Generate Markdown
          python tools/generate_mindmaps.py --html # Generate HTML
      
      # Note: AI mindmaps are NOT generated in CI/CD
      # They must be manually generated and committed to the repository
      # See Step 3.2 for manual generation instructions
      
      - name: Build MkDocs site
        run: mkdocs build
      
      - name: Copy mind map HTML files
        run: |
          cp -r docs/pages/mindmaps site/pages/mindmaps
          cp -r docs/pages/assets site/pages/assets 2>/dev/null || true
      
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

### 4.2 What CI/CD Generates

| File Type | Generated By | Tracked in Git |
|-----------|--------------|----------------|
| `docs/mindmaps/*.md` (rule-based) | CI/CD | ❌ No |
| `docs/pages/mindmaps/*.html` (rule-based) | CI/CD | ❌ No |
| `docs/mindmaps/neetcode_ontology_ai_*.md` | Manual | ✅ Yes |
| `docs/pages/mindmaps/neetcode_ontology_ai_*.html` | Manual | ✅ Yes |
| `docs/mindmaps/index.md` | Manual | ✅ Yes |
| `docs/mindmaps/README.md` | Manual | ✅ Yes |

---

### 🔎 Sitemap & Last-Modified Strategy

This project uses a **source-based sitemap strategy** to ensure SEO correctness and build stability.

#### Why this matters

MkDocs rebuilds the entire `site/` directory on every deployment.
If sitemap timestamps were derived from build artifacts, **all pages would appear “updated” on every deploy**, which is harmful for SEO.

To avoid this, **all `<lastmod>` values are derived from source-level timestamps**, not build time.

---

### 📄 Markdown Pages (`docs/**/*.md`)

* Handled by **`mkdocs-document-dates`**
* Timestamp source priority:

  1. Git commit time (if tracked)
  2. Source file modification time (fallback)

Used in sitemap as:

```
page.meta.document_dates_updated
```

✅ Rebuilding or redeploying does **not** change `<lastmod>` unless content actually changes.

---

### 🧠 Static Interactive Mind Maps (`docs/pages/mindmaps/*.html`)

Static HTML mind maps are **not MkDocs pages**, so they are handled separately via a custom plugin:

```
mkdocs_plugins/mindmaps_lastmod.py
```

#### Behavior

For each matched HTML file:

1. Use Git commit time if the file is tracked
2. Otherwise, fall back to the source file’s modification time (`mtime`)
3. Never use build output (`site/`) timestamps

Collected timestamps are injected into:

```
config.extra.static_lastmod
```

The sitemap template then iterates over this mapping directly, ensuring:

* Static HTML files always appear in `sitemap.xml`
* `<lastmod>` reflects **content updates only**
* Rebuilds do not affect timestamps

---

### 🗺️ Sitemap Generation Summary

| Content Type     | Source Location              | `<lastmod>` Source | Affected by Rebuild |
| ---------------- | ---------------------------- | ------------------ | ------------------- |
| MkDocs pages     | `docs/**/*.md`               | Git / source mtime | ❌ No                |
| Static mind maps | `docs/pages/mindmaps/*.html` | Git / source mtime | ❌ No                |
| Build output     | `site/`                      | *Not used*         | —                   |

---

### ✅ Design Guarantee

> Rebuilding or redeploying the site will **not** modify sitemap timestamps unless the underlying content changes.

This ensures:

* Accurate search engine indexing
* Stable crawl signals
* No artificial “site-wide updates”

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
| 📐 Pattern Hierarchy | API Kernels → Patterns → Problems | [Static](docs/mindmaps/pattern-hierarchy.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#pattern-hierarchy) |
| 👨‍👩‍👧‍👦 Family Derivation | Base templates → Derived variants | [Static](docs/mindmaps/family-derivation.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#family-derivation) |
| ⚡ Algorithm Usage | Problems by algorithm | [Static](docs/mindmaps/algorithm-usage.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#algorithm-usage) |
| 🏗️ Data Structure Usage | Problems by data structure | [Static](docs/mindmaps/data-structure.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#data-structure-usage) |
| 🏢 Company Coverage | Company-specific problems | [Static](docs/mindmaps/company-coverage.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#company-coverage) |
| 🗺️ Learning Roadmaps | NeetCode 150, Blind 75, etc. | [Static](docs/mindmaps/roadmap-paths.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#learning-roadmaps) |
| 🔗 Problem Relations | Related problems network | [Static](docs/mindmaps/problem-relations.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#problem-relations) |
| 🔀 Solution Variants | Multiple approaches | [Static](docs/mindmaps/solution-variants.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#solution-variants) |
| 📊 Difficulty × Topics | Topics by difficulty | [Static](docs/mindmaps/difficulty-topics.md) · [Interactive ✨](https://lufftw.github.io/neetcode/mindmaps/#difficulty-topics) |

👉 **[View All Interactive Mind Maps](https://lufftw.github.io/neetcode/mindmaps/)**
```

---

## 🔄 Complete Workflow Summary

### Rule-Based Mind Maps (Auto-Generated in CI/CD)

```
1. Edit ontology/ or meta/problems/
   ↓
2. git push
   ↓
3. GitHub Actions automatically triggers
   ↓
4. Generate rule-based mind maps
   python tools/generate_mindmaps.py        # Markdown
   python tools/generate_mindmaps.py --html # HTML
   ↓
5. Build MkDocs site
   mkdocs build
   ↓
6. Copy HTML files to site/
   cp -r docs/pages/mindmaps site/pages/mindmaps
   ↓
7. Deploy to GitHub Pages
   ↓
8. Visit https://lufftw.github.io/neetcode/
```

> **Note**: Rule-based Markdown files (`docs/mindmaps/*.md`) are NOT tracked in Git.
> They are generated fresh by CI/CD on every deployment.

### AI-Powered Mind Maps (Manual Process)

```
1. Set up OpenAI API key locally
   $env:OPENAI_API_KEY = "sk-..."
   ↓
2. Generate AI mindmaps locally
   python tools/generate_mindmaps_ai.py
   ↓
3. Review generated HTML files
   docs/pages/mindmaps/neetcode_ontology_ai_*.html
   ↓
4. Commit and push
   git add docs/pages/mindmaps/neetcode_ontology_ai_*.html
   git commit -m "docs: Update AI mind maps"
   git push
   ↓
5. GitHub Actions automatically triggers
   ↓
6. Build MkDocs site (uses committed AI mindmap HTML files)
   python -m mkdocs build
   ↓
7. Deploy to GitHub Pages
   ↓
8. Visit https://yourusername.github.io/neetcode/mindmaps/
```

### Using Interactive Mind Maps

- 🖱️ Drag to pan
- 🔍 Scroll to zoom
- 👆 Click to fold/unfold

---

## ❓ Frequently Asked Questions

### Q: Why can't GitHub README display interactive content directly?

A: GitHub disables JavaScript execution for security reasons. GitHub Pages is needed to host the interactive version.

### Q: Can I use a custom domain?

A: Yes! Configure it in Settings → Pages → Custom domain.

### Q: How do I update mind maps?

**For rule-based mind maps:**
After modifying `ontology/` or `meta/`, push to GitHub. GitHub Actions will automatically regenerate and redeploy.

**For AI-powered mind maps:**
1. Generate locally with `python tools/generate_mindmaps_ai.py`
2. Commit the generated HTML files (`docs/pages/mindmaps/neetcode_ontology_ai_*.html`)
3. Also commit the prompt file (`tools/prompts/generated/mindmap-prompt.md`) for traceability
4. Push to GitHub
5. CI/CD will automatically deploy the committed files

**Why commit the prompt file?**
The prompt file is tracked in Git so you can always see which prompt was used to generate each version of the AI mind maps. This provides full traceability and transparency.

**Why manual for AI mindmaps?**
- Requires OpenAI API key (not stored in CI/CD for security)
- Allows cost control (you decide when to regenerate)
- Enables review before committing

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
open docs/pages/mindmaps/pattern-hierarchy.html

# Method 2: Use HTTP server
cd docs/pages
python -m http.server 8000
# Visit http://localhost:8000/mindmaps/pattern-hierarchy.html
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

- **Local Development**: Always test locally with `mkdocs build` and `mkdocs serve` before pushing
- **Build Output**: The `site/` directory contains the complete MkDocs site and is gitignored
- **Generated Files**: Both Markdown (`docs/mindmaps/*.md`) and HTML (`docs/pages/mindmaps/*.html`) mind maps are gitignored (except AI and manual files)
- **Auto Deployment**: GitHub Actions handles generation, building, and deployment automatically
- **AI Mind Maps**: Must be generated manually and committed (require API key, not in CI/CD)

### Version Control Summary

| File | Tracked | Reason |
|------|---------|--------|
| `docs/mindmaps/index.md` | ✅ | Manual index page |
| `docs/mindmaps/README.md` | ✅ | Manual documentation |
| `docs/mindmaps/neetcode_ontology_ai_*.md` | ✅ | AI generated (costly) |
| `docs/mindmaps/*.md` (others) | ❌ | CI/CD generates |
| `docs/pages/mindmaps/neetcode_ontology_ai_*.html` | ✅ | AI generated (costly) |
| `docs/pages/mindmaps/*.html` (others) | ❌ | CI/CD generates |
| `site/` | ❌ | MkDocs build output |

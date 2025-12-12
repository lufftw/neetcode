# Building Documentation Locally (Manual Method)

This guide shows you how to build documentation locally using simple batch/shell scripts **without requiring Docker or any external CI/CD tools**.

> 📖 **Looking for other options?** See [Local Documentation Build Options](LOCAL_DOCS_BUILD.md) for a comparison of all available methods, including the act method for testing exact CI/CD workflows.

> ⚠️ **Important: This is an Optional Feature**
> 
> This documentation is **completely optional** and is intended for:
> - **Project maintainers** who want to build documentation locally
> - **Contributors** who are working on documentation improvements
> 
> **Core LeetCode practice functionality does NOT require this:**
> - ✅ Solving problems (`solutions/`, `generators/`)
> - ✅ Running tests (`run_tests.bat/sh`, `run_case.bat/sh`)
> - ✅ Using the runner framework (`runner/`)
> - ✅ All core practice features work without any documentation build setup
> 
> **This build setup is ONLY for:**
> - 📚 Building documentation website locally
> - 🧠 Generating mind maps for local preview
> - 🔧 Testing documentation changes before committing

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [What It Does](#what-it-does)
- [Output](#output)
- [Troubleshooting](#troubleshooting)

---

## ⚡ Quick Start

**One command to build everything:**

```bash
# Windows
scripts\build_docs.bat

# Linux/macOS
./scripts/build_docs.sh
```

**Build and preview locally:**

```bash
# Windows
scripts\build_docs.bat --serve

# Linux/macOS
./scripts/build_docs.sh --serve
```

Then visit http://127.0.0.1:8000 in your browser.

---

## Prerequisites

### Required

1. **Python 3.11** (already required for the project)
2. **Virtual environment** (already set up if you're using the project)
3. **Dependencies** (already installed if you've run `pip install -r requirements.txt`)

### No Additional Tools Needed

- ❌ No Docker
- ❌ No act tool
- ❌ No external CI/CD tools
- ✅ Just Python and the project dependencies

---

## Usage

### Basic Build

Build the documentation site:

```bash
# Windows
scripts\build_docs.bat

# Linux/macOS
./scripts/build_docs.sh
```

**Output:** The built site will be in the `site/` directory.

### Build and Serve Locally

Build and start a local server to preview:

```bash
# Windows
scripts\build_docs.bat --serve

# Linux/macOS
./scripts/build_docs.sh --serve
```

Then open http://127.0.0.1:8000 in your browser.

**To stop the server:** Press `Ctrl+C`

### Clean Build

Remove the existing `site/` directory before building:

```bash
# Windows
scripts\build_docs.bat --clean

# Linux/macOS
./scripts/build_docs.sh --clean
```

### Combined Options

```bash
# Clean build and serve
scripts\build_docs.bat --clean --serve
./scripts/build_docs.sh --clean --serve
```

---

## What It Does

The script automatically executes these steps:

1. **Check virtual environment**
   - Verifies that `leetcode` virtual environment exists
   - Installs dependencies if missing

2. **Generate Mind Maps (Markdown)**
   - Runs `python tools/generate_mindmaps.py`
   - Generates markdown mind map files

3. **Generate Mind Maps (HTML)**
   - Runs `python tools/generate_mindmaps.py --html`
   - Generates interactive HTML mind map files

4. **Build MkDocs Site**
   - Runs `mkdocs build`
   - Builds the complete documentation site

5. **Copy Mind Map HTML Files**
   - Copies `docs/pages/mindmaps/` to `site/pages/mindmaps/`
   - Copies `docs/pages/assets/` to `site/pages/assets/`

**Total time:** Usually 10-30 seconds (depending on your machine)

---

## Output

After running the script, you'll have:

```
site/
├── index.html
├── index_zh-TW/
├── pages/
│   ├── mindmaps/
│   │   ├── neetcode_ontology_ai_en.html
│   │   ├── neetcode_ontology_ai_zh-TW.html
│   │   └── ... (other mind maps)
│   └── assets/
├── patterns/
├── search/
└── ... (other documentation files)
```

**Note:** The `site/` directory is gitignored and can be safely deleted or regenerated.

---

## Troubleshooting

### Error: Virtual environment not found

**Solution:**
```bash
# Windows
py -3.11 -m venv leetcode
leetcode\Scripts\activate
pip install -r requirements.txt

# Linux/macOS
python -m venv leetcode
source leetcode/bin/activate
pip install -r requirements.txt
```

### Error: Failed to install dependencies

**Solution:**
```bash
# Make sure virtual environment is activated
# Windows
leetcode\Scripts\activate

# Linux/macOS
source leetcode/bin/activate

# Then install manually
pip install -r requirements.txt
```

### Error: Failed to generate mind maps

**Possible causes:**
- Missing dependencies (run `pip install -r requirements.txt`)
- Syntax errors in `ontology/` or `meta/problems/` files
- File permission issues

**Solution:**
- Check error messages for specific issues
- Verify all TOML files in `ontology/` and `meta/problems/` are valid
- Try running `python tools/generate_mindmaps.py` manually to see detailed errors

### Error: Failed to build MkDocs site

**Possible causes:**
- Missing MkDocs or dependencies
- Syntax errors in `mkdocs.yml`
- Missing documentation files

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check mkdocs.yml syntax
python -m mkdocs build --verbose
```

### Port 8000 already in use (when using --serve)

**Solution:**
```bash
# Find and stop the process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS
lsof -ti:8000 | xargs kill -9

# Or use a different port (modify script or run manually)
python -m mkdocs serve -a 127.0.0.1:8001
```

---

## Comparison with Other Methods

| Method | Requires Docker | Requires act | Setup Complexity | Speed |
|:-------|:---------------|:-------------|:-----------------|:------|
| **This Method (Manual Scripts)** | ❌ No | ❌ No | ⭐ Simple | ⚡ Fast |
| [act Method](ACT_LOCAL_GITHUB_ACTIONS.md) | ✅ Yes | ✅ Yes | ⭐⭐⭐ Complex | 🐢 Slower |

**When to use this method:**
- ✅ You want the simplest setup
- ✅ You don't want to install Docker
- ✅ You just need to build documentation locally
- ✅ You're testing documentation changes

**When to use act method:**
- ✅ You want to test the exact GitHub Actions workflow
- ✅ You want to verify CI/CD behavior locally
- ✅ You're debugging GitHub Actions issues

---

## Related Documentation

- [Local Documentation Build Options](LOCAL_DOCS_BUILD.md) - Overview of all local build methods
- [Running GitHub Actions Locally with Act](ACT_LOCAL_GITHUB_ACTIONS.md) - Using act to simulate CI/CD
- [GitHub Pages Setup Guide](GITHUB_PAGES_SETUP.md) - Complete deployment guide

---

## Changelog

- **2025-01-XX**: Initial version
  - ✅ Added `build_docs.bat` and `build_docs.sh` scripts
  - ✅ Created comprehensive manual build guide
  - ✅ Cross-platform support (Windows, Linux, macOS)


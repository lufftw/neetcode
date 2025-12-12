# Local Documentation Build Options

This guide provides an overview of different methods to build documentation locally. Choose the method that best fits your needs.

> ⚠️ **Important: This is an Optional Feature**
> 
> Building documentation locally is **completely optional**. Core LeetCode practice functionality does NOT require any of these methods.
> 
> **These methods are ONLY for:**
> - 📚 Building documentation website locally
> - 🧠 Generating mind maps for local preview
> - 🔧 Testing documentation changes before committing
> - 🔍 Debugging documentation build issues

---

## 📋 Available Methods

### Method 1: Manual Scripts (Recommended for Most Users)

**Best for:** Quick local builds, testing documentation changes

- ✅ **No Docker required**
- ✅ **No external tools required**
- ✅ **Simple one-command build**
- ✅ **Fast execution**
- ⚠️ **Not identical to CI/CD environment**

**Quick Start:**
```bash
# Windows
build_docs.bat --serve

# Linux/macOS
./build_docs.sh --serve
```

📖 **[Full Guide →](BUILD_DOCS_MANUAL.md)**

---

### Method 2: Act (GitHub Actions Simulator)

**Best for:** Testing exact CI/CD workflow, debugging GitHub Actions

- ✅ **Identical to GitHub Actions environment**
- ✅ **Tests exact CI/CD workflow**
- ⚠️ **Requires Docker**
- ⚠️ **Requires act tool installation**
- ⚠️ **Slower (Docker overhead)**

**Quick Start:**
```bash
# Install act first (see guide)
act -P ubuntu-latest=catthehacker/ubuntu:act-latest -j build
```

📖 **[Full Guide →](ACT_LOCAL_GITHUB_ACTIONS.md)**

---

## 🎯 Which Method Should I Use?

### Use Manual Scripts If:
- ✅ You want the simplest setup
- ✅ You don't want to install Docker
- ✅ You're just testing documentation changes
- ✅ You want fast builds
- ✅ You're a casual contributor

### Use Act If:
- ✅ You want to test the exact GitHub Actions workflow
- ✅ You're debugging CI/CD issues
- ✅ You want 100% consistency with production
- ✅ You're a maintainer working on CI/CD
- ✅ You already have Docker installed

---

## 📊 Comparison Table

| Feature | Manual Scripts | Act |
|:--------|:---------------|:----|
| **Setup Complexity** | ⭐ Simple | ⭐⭐⭐ Complex |
| **Docker Required** | ❌ No | ✅ Yes |
| **External Tools** | ❌ None | ✅ act tool |
| **Build Speed** | ⚡ Fast (10-30s) | 🐢 Slower (2-5min) |
| **CI/CD Consistency** | ⚠️ Similar | ✅ Identical |
| **Best For** | Quick testing | CI/CD debugging |
| **Platform Support** | ✅ All | ✅ All (with Docker) |

---

## 🚀 Quick Start Comparison

### Manual Scripts Method

```bash
# 1. No installation needed (just use existing Python venv)
# 2. Run script
build_docs.bat --serve    # Windows
./build_docs.sh --serve   # Linux/macOS
# 3. Done! Visit http://127.0.0.1:8000
```

**Time to first build:** ~30 seconds (if dependencies already installed)

### Act Method

```bash
# 1. Install Docker Desktop
# 2. Install act tool
winget install nektos.act  # Windows
brew install act            # macOS
# 3. Run act
act -P ubuntu-latest=catthehacker/ubuntu:act-latest -j build
# 4. Wait for Docker image download (first time: 5-10 minutes)
```

**Time to first build:** ~10 minutes (first time, includes Docker setup)

---

## 📚 Detailed Guides

- **[Manual Scripts Guide](BUILD_DOCS_MANUAL.md)** - Complete guide for batch/shell script method
- **[Act Guide](ACT_LOCAL_GITHUB_ACTIONS.md)** - Complete guide for act method
- **[GitHub Pages Setup](GITHUB_PAGES_SETUP.md)** - Production deployment guide

---

## 🔄 Workflow Recommendations

### For Documentation Contributors

1. **Make changes** to documentation files
2. **Test locally** using Manual Scripts method (fast)
3. **Commit and push** changes
4. **GitHub Actions** will automatically build and deploy

### For CI/CD Maintainers

1. **Make changes** to workflow files or documentation
2. **Test locally** using Act method (matches production)
3. **Verify** build succeeds
4. **Commit and push** changes

### For Quick Preview

1. **Just want to see changes?** → Use Manual Scripts with `--serve`
2. **Need exact CI/CD test?** → Use Act method

---

## ❓ FAQ

### Do I need to build documentation locally?

**No.** Documentation building is completely optional. Core LeetCode practice features work without any documentation build setup.

### Which method is better?

**It depends on your needs:**
- **Most users:** Manual Scripts (simpler, faster)
- **Maintainers:** Act (more accurate, matches CI/CD)

### Can I use both methods?

**Yes!** You can use Manual Scripts for quick testing and Act for final verification.

### Do I need Docker for Manual Scripts?

**No.** Manual Scripts only require Python and project dependencies (which you already have).

### Why would I use Act if Manual Scripts are simpler?

Act provides **exact CI/CD simulation**, which is useful when:
- Debugging GitHub Actions workflow issues
- Ensuring local builds match production exactly
- Testing workflow changes before committing

---

## 🆘 Need Help?

- **Manual Scripts issues:** See [BUILD_DOCS_MANUAL.md](BUILD_DOCS_MANUAL.md#troubleshooting)
- **Act issues:** See [ACT_LOCAL_GITHUB_ACTIONS.md](ACT_LOCAL_GITHUB_ACTIONS.md#troubleshooting)
- **General questions:** Check [GitHub Pages Setup Guide](GITHUB_PAGES_SETUP.md)

---

## Changelog

- **2025-01-XX**: Initial version
  - ✅ Added comparison of local build methods
  - ✅ Created overview guide
  - ✅ Linked to detailed guides for each method


# Scripts Directory

This directory contains utility scripts for project maintenance and development.

> ⚠️ **Note**: These scripts are **optional** and intended for project maintainers and contributors. Core LeetCode practice functionality does NOT require these scripts.

---

## 📋 Available Scripts

### Documentation Build Scripts

| Script | Purpose | Usage |
|:-------|:--------|:------|
| `build_docs.bat` / `build_docs.sh` | Build documentation site locally | `scripts\build_docs.bat --serve` (Windows)<br>`./scripts/build_docs.sh --serve` (Linux/macOS) |

**Features:**
- ✅ No Docker required
- ✅ No external tools required
- ✅ Simple one-command build
- ✅ Fast execution

📖 **[Full Documentation →](../docs/BUILD_DOCS_MANUAL.md)**

---

## 🎯 Usage

### Build Documentation

```bash
# Windows
scripts\build_docs.bat

# Linux/macOS
./scripts/build_docs.sh
```

### Build and Preview Locally

```bash
# Windows
scripts\build_docs.bat --serve

# Linux/macOS
./scripts/build_docs.sh --serve
```

Then visit http://127.0.0.1:8000 in your browser.

---

## 📚 Related Documentation

- [Local Documentation Build Options](../docs/LOCAL_DOCS_BUILD.md) - Overview of all local build methods
- [Manual Build Guide](../docs/BUILD_DOCS_MANUAL.md) - Complete guide for manual script method
- [Act Guide](../docs/ACT_LOCAL_GITHUB_ACTIONS.md) - Using act to simulate CI/CD

---

## 🔄 Future Scripts

This directory may contain additional utility scripts in the future:
- Deployment scripts
- Maintenance scripts
- Development helper scripts

All scripts will follow the same naming convention: `script_name.bat` (Windows) and `script_name.sh` (Linux/macOS).


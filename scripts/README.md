# Scripts Directory

This directory contains utility scripts for project maintenance and development.

> ⚠️ **Note**: These scripts are **optional** and intended for project maintainers and contributors. Core LeetCode practice functionality does NOT require these scripts.

---

## 📋 Available Scripts

### Problem Management Scripts

| Script | Purpose | Usage |
|:-------|:--------|:------|
| `new_problem.bat` / `new_problem.sh` | Create new problem from template | `scripts\new_problem.bat 0001_two_sum` (Windows)<br>`./scripts/new_problem.sh 0001_two_sum` (Linux/macOS) |
| `run_tests.bat` / `run_tests.sh` | Run all tests for a problem | `scripts\run_tests.bat 0001_two_sum` (Windows)<br>`./scripts/run_tests.sh 0001_two_sum` (Linux/macOS) |
| `run_case.bat` / `run_case.sh` | Run single test case | `scripts\run_case.bat 0001_two_sum 1` (Windows)<br>`./scripts/run_case.sh 0001_two_sum 1` (Linux/macOS) |

**Features:**
- ✅ Create problems from templates (single or multi-solution)
- ✅ Run all test cases or individual cases
- ✅ Support for benchmarking and multiple solutions
- ✅ Cross-platform (Windows/Linux/macOS)

### Documentation Build Scripts

| Script | Purpose | Usage |
|:-------|:--------|:------|
| `build_docs.bat` / `build_docs.sh` | Build documentation site locally | `scripts\build_docs.bat --serve` (Windows)<br>`./scripts/build_docs.sh --serve` (Linux/macOS) |

**Features:**
- ✅ No Docker required
- ✅ No external tools required
- ✅ Simple one-command build
- ✅ Fast execution
- ✅ Interactive prompt for AI mind map generation (optional, requires OPENAI_API_KEY)

📖 **[Full Documentation →](../docs/BUILD_DOCS_MANUAL.md)**

---

## 🎯 Usage

### Create New Problem

```bash
# Windows
scripts\new_problem.bat 0001_two_sum
scripts\new_problem.bat 0023_merge_k_lists --multi

# Linux/macOS
./scripts/new_problem.sh 0001_two_sum
./scripts/new_problem.sh 0023_merge_k_lists --multi
```

### Run Tests

```bash
# Windows - Run all tests
scripts\run_tests.bat 0001_two_sum
scripts\run_tests.bat 0001_two_sum --all --benchmark

# Windows - Run single test case
scripts\run_case.bat 0001_two_sum 1

# Linux/macOS - Run all tests
./scripts/run_tests.sh 0001_two_sum
./scripts/run_tests.sh 0001_two_sum --all --benchmark

# Linux/macOS - Run single test case
./scripts/run_case.sh 0001_two_sum 1
```

### Build Documentation

The build script will:
1. Generate standard mind maps (Markdown)
2. Generate mind maps (HTML)
3. **Ask if you want to generate AI-powered mind maps** (requires OPENAI_API_KEY)
4. Build MkDocs site
5. Copy mind map files

```bash
# Windows
scripts\build_docs.bat

# Linux/macOS
./scripts/build_docs.sh
```

> **Note:** AI mind map generation is optional. The script will prompt you during the build process. You can skip it if you don't have an OpenAI API key configured.

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


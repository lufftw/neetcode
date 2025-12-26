# Virtual Environment Setup Guide

> **Status**: Informational  
> **Scope**: Virtual environment setup for the project  
> **Last Updated**: {{ git_revision_date_localized }}  
> **Created**: {{ git_creation_date_localized }}

## 📋 Overview

This project uses a `leetcode` Python virtual environment to isolate dependencies. Unit test scripts automatically use this virtual environment.

---

## 🔧 Virtual Environment Setup

### Windows

#### 1. Create Virtual Environment
```powershell
# From project root directory
python -m venv leetcode
```

#### 2. Activate Virtual Environment
```powershell
# PowerShell
leetcode\Scripts\Activate.ps1

# CMD
leetcode\Scripts\activate.bat
```

#### 3. Install Dependencies
```powershell
# Install basic dependencies
pip install -r requirements.txt

# Install test dependencies
pip install pytest pytest-cov
```

### Linux / macOS

#### 1. Create Virtual Environment
```bash
# From project root directory
python3 -m venv leetcode
```

#### 2. Activate Virtual Environment
```bash
source leetcode/bin/activate
```

#### 3. Install Dependencies
```bash
# Install basic dependencies
pip install -r requirements.txt

# Install test dependencies
pip install pytest pytest-cov
```

---

## 🧪 Running Tests

### Method 1: Using Test Scripts (Recommended)

Test scripts automatically use the virtual environment:

```bash
# Windows
cd .dev
run_tests.bat

# Linux/Mac
cd .dev
./run_tests.sh
```

### Method 2: Manual Virtual Environment Usage

```bash
# Windows
leetcode\Scripts\activate
cd .dev
leetcode\..\Scripts\python.exe -m pytest tests -v

# Linux/Mac
source leetcode/bin/activate
cd .dev
python -m pytest tests -v
```

### Method 3: Direct Virtual Environment Python Usage

No need to activate the virtual environment:

```bash
# Windows (from project root)
leetcode\Scripts\python.exe -m pytest .dev/tests -v

# Linux/Mac (from project root)
leetcode/bin/python -m pytest .dev/tests -v
```

---

## 🔍 Verify Setup

### Check if Virtual Environment Exists

```bash
# Windows
dir leetcode\Scripts\python.exe

# Linux/Mac
ls -la leetcode/bin/python
```

### Check if pytest is Installed

```bash
# Windows
leetcode\Scripts\python.exe -m pytest --version

# Linux/Mac
leetcode/bin/python -m pytest --version
```

### Check Installed Packages

```bash
# Windows
leetcode\Scripts\activate
pip list

# Linux/Mac
source leetcode/bin/activate
pip list
```

---

## 📦 Virtual Environment Paths

Test scripts use the following paths:

### Windows
- Python executable: `leetcode\Scripts\python.exe`
- Activation script: `leetcode\Scripts\activate.bat` (CMD) or `leetcode\Scripts\Activate.ps1` (PowerShell)

### Linux/Mac
- Python executable: `leetcode/bin/python`
- Activation script: `leetcode/bin/activate`

---

## ⚠️ Common Issues

### Q1: Virtual Environment Not Found

**Error Message**:
```
[ERROR] Virtual environment not found: leetcode\Scripts\python.exe
```

**Solution**:
```bash
# Create virtual environment
python -m venv leetcode

# Activate and install dependencies
leetcode\Scripts\activate
pip install -r requirements.txt
pip install pytest pytest-cov
```

### Q2: pytest Not Installed

**Error Message**:
```
[ERROR] pytest is not installed in virtual environment
```

**Solution**:
```bash
# Activate virtual environment
leetcode\Scripts\activate  # Windows
source leetcode/bin/activate  # Linux/Mac

# Install pytest
pip install pytest pytest-cov
```

### Q3: Module 'runner' Not Found

**Error Message**:
```
ModuleNotFoundError: No module named 'runner'
```

**Solution**:
Ensure you run tests from the project root directory, or use the test scripts.

---

## 🔄 Updating Dependencies

### Update Test Dependencies

```bash
# Activate virtual environment
leetcode\Scripts\activate  # Windows
source leetcode/bin/activate  # Linux/Mac

# Update packages
pip install --upgrade pytest pytest-cov
```

### Update All Dependencies

```bash
# Activate virtual environment
leetcode\Scripts\activate  # Windows
source leetcode/bin/activate  # Linux/Mac

# Update all packages
pip install --upgrade -r requirements.txt
```

---

## 📝 requirements.txt

Ensure `requirements.txt` includes test dependencies:

```txt
# LeetCode Practice Framework - Dependencies

# Required packages:
debugpy>=1.8.0          # Debug support for VS Code

# Testing packages:
pytest>=7.4.0           # Unit testing framework
pytest-cov>=4.1.0       # Coverage reporting

# Optional packages (for complexity estimation):
big-O>=0.10.0           # Time complexity estimation

# Documentation generation (MkDocs):
mkdocs>=1.6.0           # MkDocs static site generator
mkdocs-material>=9.5.0  # Material theme for MkDocs
mkdocs-minify-plugin>=0.7.0  # Minify HTML output
mkdocs-include-markdown-plugin>=7.0.0  # Include markdown files
```

---

## 🎯 Best Practices

1. **Use Virtual Environment**: Always install dependencies in the virtual environment
2. **Use Test Scripts**: Test scripts automatically handle the virtual environment
3. **Regular Updates**: Regularly update dependencies to get the latest features and fixes
4. **Version Control**: Do not add the `leetcode/` folder to Git

---

## 📞 Need Help?

If you have questions, please refer to:
- [Contributors README](README.md) - Maintainer Guide
- [Testing Documentation](testing.md) - Complete Testing Documentation
- [Project main README.md](https://github.com/lufftw/neetcode/blob/main/README.md) - Python Environment section

---

**Test Maintainer**: luffdev  
**Created Date**: 2025-12-08

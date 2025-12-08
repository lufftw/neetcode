# 虛擬環境設定指南

## 📋 概述

本專案使用 `leetcode` Python 虛擬環境來隔離依賴。單元測試腳本會自動使用此虛擬環境。

---

## 🔧 虛擬環境設定

### Windows

#### 1. 建立虛擬環境
```powershell
# 從專案根目錄
python -m venv leetcode
```

#### 2. 啟動虛擬環境
```powershell
# PowerShell
leetcode\Scripts\Activate.ps1

# CMD
leetcode\Scripts\activate.bat
```

#### 3. 安裝依賴
```powershell
# 安裝基本依賴
pip install -r requirements.txt

# 安裝測試依賴
pip install pytest pytest-cov
```

### Linux / macOS

#### 1. 建立虛擬環境
```bash
# 從專案根目錄
python3 -m venv leetcode
```

#### 2. 啟動虛擬環境
```bash
source leetcode/bin/activate
```

#### 3. 安裝依賴
```bash
# 安裝基本依賴
pip install -r requirements.txt

# 安裝測試依賴
pip install pytest pytest-cov
```

---

## 🧪 運行測試

### 方法 1: 使用測試腳本（推薦）

測試腳本會自動使用虛擬環境：

```bash
# Windows
cd .dev
run_tests.bat

# Linux/Mac
cd .dev
./run_tests.sh
```

### 方法 2: 手動使用虛擬環境

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

### 方法 3: 直接使用虛擬環境 Python

不需要啟動虛擬環境：

```bash
# Windows（從專案根目錄）
leetcode\Scripts\python.exe -m pytest .dev/tests -v

# Linux/Mac（從專案根目錄）
leetcode/bin/python -m pytest .dev/tests -v
```

---

## 🔍 驗證設定

### 檢查虛擬環境是否存在

```bash
# Windows
dir leetcode\Scripts\python.exe

# Linux/Mac
ls -la leetcode/bin/python
```

### 檢查 pytest 是否安裝

```bash
# Windows
leetcode\Scripts\python.exe -m pytest --version

# Linux/Mac
leetcode/bin/python -m pytest --version
```

### 檢查安裝的套件

```bash
# Windows
leetcode\Scripts\activate
pip list

# Linux/Mac
source leetcode/bin/activate
pip list
```

---

## 📦 虛擬環境路徑

測試腳本使用以下路徑：

### Windows
- Python 執行檔: `leetcode\Scripts\python.exe`
- 啟動腳本: `leetcode\Scripts\activate.bat` (CMD) 或 `leetcode\Scripts\Activate.ps1` (PowerShell)

### Linux/Mac
- Python 執行檔: `leetcode/bin/python`
- 啟動腳本: `leetcode/bin/activate`

---

## ⚠️ 常見問題

### Q1: 虛擬環境不存在

**錯誤訊息**:
```
[ERROR] Virtual environment not found: leetcode\Scripts\python.exe
```

**解決方法**:
```bash
# 建立虛擬環境
python -m venv leetcode

# 啟動並安裝依賴
leetcode\Scripts\activate
pip install -r requirements.txt
pip install pytest pytest-cov
```

### Q2: pytest 未安裝

**錯誤訊息**:
```
[ERROR] pytest is not installed in virtual environment
```

**解決方法**:
```bash
# 啟動虛擬環境
leetcode\Scripts\activate  # Windows
source leetcode/bin/activate  # Linux/Mac

# 安裝 pytest
pip install pytest pytest-cov
```

### Q3: 找不到 runner 模組

**錯誤訊息**:
```
ModuleNotFoundError: No module named 'runner'
```

**解決方法**:
確保從專案根目錄運行測試，或使用測試腳本。

---

## 🔄 更新依賴

### 更新測試依賴

```bash
# 啟動虛擬環境
leetcode\Scripts\activate  # Windows
source leetcode/bin/activate  # Linux/Mac

# 更新套件
pip install --upgrade pytest pytest-cov
```

### 更新所有依賴

```bash
# 啟動虛擬環境
leetcode\Scripts\activate  # Windows
source leetcode/bin/activate  # Linux/Mac

# 更新所有套件
pip install --upgrade -r requirements.txt
```

---

## 📝 requirements.txt

確保 `requirements.txt` 包含測試依賴：

```txt
# LeetCode Practice Framework - Dependencies

# Required packages:
debugpy>=1.8.0          # Debug support for VS Code

# Testing packages:
pytest>=7.4.0           # Unit testing framework
pytest-cov>=4.1.0       # Coverage reporting

# Optional packages (for complexity estimation):
big-O>=0.10.0           # Time complexity estimation
```

---

## 🎯 最佳實踐

1. **使用虛擬環境**: 始終在虛擬環境中安裝依賴
2. **使用測試腳本**: 測試腳本會自動處理虛擬環境
3. **定期更新**: 定期更新依賴以獲得最新功能和修復
4. **版本控制**: 不要將 `leetcode/` 資料夾加入 Git

---

## 📞 需要幫助？

如有問題，請參考：
- [.dev/README.md](.dev/README.md) - 維護者指南
- [.dev/TESTING.md](.dev/TESTING.md) - 完整測試文檔
- 專案主 README.md - Python 環境章節

---

**測試負責人**: luffdev  
**建立日期**: 2025-12-08


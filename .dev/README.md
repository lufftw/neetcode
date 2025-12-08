# 開發者與維護者專區

> ⚠️ **注意**: 此資料夾專為專案維護者使用，包含單元測試、開發文檔和維護工具。  
> 一般使用者請參考根目錄的 [README.md](../README.md)

---

## 📁 資料夾結構

```
.dev/
├── tests/                      # 單元測試套件（行為測試）
│   ├── __init__.py
│   ├── test_util.py           # util.py 的測試 (40+ tests)
│   ├── test_case_runner.py    # case_runner.py 的測試 (15+ tests)
│   ├── test_test_runner.py    # test_runner.py 的測試 (30+ tests)
│   ├── test_complexity_estimator.py  # complexity_estimator.py 的測試 (25+ tests)
│   ├── test_edge_cases.py     # 邊界條件測試 (40+ tests)
│   ├── test_integration.py    # 整合測試 (20+ tests)
│   └── README.md              # 測試詳細說明
│
├── run_tests.bat              # Windows 測試執行腳本
├── run_tests.sh               # Unix/Linux 測試執行腳本
│
├── TESTING.md                 # 完整測試文檔
├── VIRTUAL_ENV_SETUP.md      # 虛擬環境設定指南
└── README.md                  # 本文件
```

---

## 🎯 用途說明

### 此資料夾是什麼？

`.dev/` 是**開發與維護專區**，包含：

1. **單元測試套件** - 確保代碼重構不會破壞現有功能
2. **測試文檔** - 測試策略、使用方法、最佳實踐
3. **開發工具** - 測試執行腳本、配置文件

### 誰需要使用？

- ✅ **專案維護者** - 進行代碼重構、新增功能
- ✅ **貢獻者** - 提交 Pull Request 前運行測試
- ✅ **QA 測試人員** - 驗證系統功能
- ❌ **一般使用者** - 不需要關注此資料夾

---

## 🚀 快速開始

### 1. 確保虛擬環境已建立

```bash
# Windows
python -m venv leetcode
leetcode\Scripts\activate

# Linux/Mac
python -m venv leetcode
source leetcode/bin/activate
```

### 2. 安裝測試依賴

```bash
# 在虛擬環境中安裝
pip install pytest pytest-cov
```

### 3. 運行所有測試

```bash
# Windows
cd .dev
run_tests.bat

# Linux/Mac
cd .dev
./run_tests.sh

# 或直接使用虛擬環境的 Python（從專案根目錄）
# Windows
leetcode\Scripts\python.exe -m pytest .dev/tests -v

# Linux/Mac
leetcode/bin/python -m pytest .dev/tests -v
```

### 3. 運行特定測試

```bash
# 只運行單元測試
python -m pytest .dev/tests -v -m unit

# 只運行整合測試
python -m pytest .dev/tests -v -m integration

# 只運行邊界測試
python -m pytest .dev/tests -v -m edge_case

# 運行特定文件
python -m pytest .dev/tests/test_util.py -v
```

---

## 📊 測試統計

| 項目 | 數量 |
|------|------|
| 測試檔案 | 6 |
| 測試類別 | 50+ |
| 測試案例 | 150+ |
| 代碼覆蓋率 | 80-100% |

### 測試覆蓋範圍

- ✅ `runner/util.py` - 100% 覆蓋
- ✅ `runner/case_runner.py` - 90% 覆蓋
- ✅ `runner/test_runner.py` - 85% 覆蓋
- ✅ `runner/complexity_estimator.py` - 80% 覆蓋

---

## 📚 文檔索引

### 核心文檔

1. **[TESTING.md](TESTING.md)** - 完整的測試文檔
   - 測試策略和原則
   - 如何運行測試
   - 如何添加新測試
   - 重構工作流程

2. **[VIRTUAL_ENV_SETUP.md](VIRTUAL_ENV_SETUP.md)** - 虛擬環境設定指南
   - 虛擬環境建立
   - 依賴安裝
   - 常見問題排除

3. **[tests/README.md](tests/README.md)** - 測試目錄詳細說明
   - 測試結構
   - 測試標記
   - 使用範例

---

## 🎯 測試目的

### 核心目標

> **用測試把「行為」釘死，幫忙守住重構不爆炸**

### 測試價值

1. **🛡️ 重構保護** - 確保重構不會破壞現有功能
2. **🔄 回歸預防** - 新功能不會破壞舊功能
3. **📚 文檔作用** - 測試即使用範例
4. **💪 信心提升** - 讓開發者放心修改代碼

---

## 🔧 開發工作流程

### 添加新功能

1. 先寫測試（TDD）
2. 實作功能
3. 運行測試確保通過
4. 提交代碼

### 修復 Bug

1. 先寫測試重現 bug
2. 修復 bug
3. 確保測試通過
4. 提交代碼

### 重構代碼

1. 確保現有測試全部通過
2. 進行重構
3. 再次運行測試
4. 如果失敗，修復代碼或更新測試
5. 提交代碼

---

## 📈 測試命令參考

> **注意**: 以下命令使用虛擬環境的 Python  
> Windows: `leetcode\Scripts\python.exe`  
> Linux/Mac: `leetcode/bin/python`

```bash
# === 基本命令 ===

# 運行所有測試（使用虛擬環境）
# Windows
leetcode\Scripts\python.exe -m pytest .dev/tests -v

# Linux/Mac
leetcode/bin/python -m pytest .dev/tests -v

# 運行並顯示詳細輸出
python -m pytest .dev/tests -v --tb=long

# 在第一個失敗時停止
python -m pytest .dev/tests -v -x

# === 測試選擇 ===

# 按標記運行
python -m pytest .dev/tests -v -m unit
python -m pytest .dev/tests -v -m integration
python -m pytest .dev/tests -v -m edge_case

# 按文件運行
python -m pytest .dev/tests/test_util.py -v

# 按測試類運行
python -m pytest .dev/tests/test_util.py::TestNormalizeOutput -v

# 按測試函數運行
python -m pytest .dev/tests/test_util.py::TestNormalizeOutput::test_basic_normalization -v

# === 覆蓋率報告 ===

# 生成覆蓋率報告
python -m pytest .dev/tests --cov=runner --cov-report=html

# 查看覆蓋率報告
# Windows: start htmlcov/index.html
# Linux/Mac: open htmlcov/index.html

# === 重新運行 ===

# 只運行失敗的測試
python -m pytest .dev/tests -v --lf

# 先運行失敗的，再運行其他的
python -m pytest .dev/tests -v --ff
```

---

## 🎓 測試原則

### 1. 行為測試優先
測試「做什麼」而不是「怎麼做」

### 2. 獨立性
每個測試獨立運行，不依賴其他測試

### 3. 可重複性
測試結果是確定性的

### 4. 清晰性
測試易於理解和維護

### 5. 完整性
覆蓋正常情況和邊界情況

---

## 📞 聯絡資訊

**測試負責人**: luffdev  
**分支**: `test/core-runner-baseline`  
**建立日期**: 2025-12-08

---

## 🔗 相關連結

- [專案主 README](../README.md) - 專案整體說明
- [根目錄 pytest.ini](../pytest.ini) - pytest 配置文件
- [requirements.txt](../requirements.txt) - 專案依賴

---

**注意**: 此資料夾的內容專為維護者使用，一般使用者無需關注。


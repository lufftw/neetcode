# Unit Tests for NeetCode Runner System

這個目錄包含了 neetcode **runner 系統**的**行為測試（Characterization Tests）**。

**注意**：此目錄測試的是 **runner 系統的功能**（test_runner, executor, module_loader 等），
而非 solutions 本身。要測試所有 solutions，請使用 `.dev/tests_solutions/`。

## 目的

這些測試的主要目的是：

1. **釘住現有行為**：確保重構時不會改變現有功能
2. **邊界條件驗證**：測試空輸入、錯誤輸入、大資料等邊界情況
3. **整合測試**：驗證各個組件能正確協同工作
4. **回歸測試**：防止未來的修改破壞現有功能

## 測試分類

| 測試類型 | 目錄 | 用途 |
|---------|------|------|
| **Runner 系統測試** | `.dev/tests/` | 測試 runner 框架功能 |
| **Solutions 測試** | `.dev/tests_solutions/` | 測試所有 solution 檔案 |

## 測試結構

```
tests_unit/
├── test_util.py              # util.py 的行為測試
├── test_case_runner.py       # case_runner.py 的行為測試
├── test_test_runner.py       # test_runner.py 的行為測試
├── test_complexity_estimator.py  # complexity_estimator.py 的行為測試
├── test_edge_cases.py        # 邊界條件測試
├── test_integration.py       # 整合測試（端到端）
└── README.md                 # 本文件
```

## 如何運行測試

### 前置要求

首先安裝測試依賴：

```bash
# Windows
python -m pip install pytest pytest-cov

# Linux/Mac
python3 -m pip install pytest pytest-cov
```

### 運行所有測試

```bash
# Windows
run_unit_tests.bat

# Linux/Mac
./run_unit_tests.sh
```

或直接使用 pytest：

```bash
python -m pytest tests_unit -v
```

### 運行特定測試文件

```bash
# 只運行 util.py 的測試
python -m pytest tests_unit/test_util.py -v

# 只運行邊界測試
python -m pytest tests_unit/test_edge_cases.py -v

# 只運行整合測試
python -m pytest tests_unit/test_integration.py -v
```

### 運行特定測試類別

```bash
# 只運行單元測試
python -m pytest tests_unit -v -m unit

# 只運行整合測試
python -m pytest tests_unit -v -m integration

# 只運行邊界測試
python -m pytest tests_unit -v -m edge_case
```

### 生成覆蓋率報告

```bash
# 生成覆蓋率報告
python -m pytest tests_unit --cov=runner --cov-report=html

# 查看報告
# Windows: start htmlcov/index.html
# Linux/Mac: open htmlcov/index.html
```

## 測試標記（Markers）

測試使用以下標記來分類：

- `@pytest.mark.unit` - 單元測試
- `@pytest.mark.integration` - 整合測試
- `@pytest.mark.edge_case` - 邊界條件測試
- `@pytest.mark.slow` - 運行時間較長的測試
- `@pytest.mark.requires_big_o` - 需要 big-O 套件的測試

## 測試覆蓋範圍

### 1. util.py 測試

- ✅ `normalize_output()` - 輸出正規化
- ✅ `compare_outputs()` - 輸出比較（exact/sorted/set 模式）
- ✅ `compare_result()` - 結果比較（支援 JUDGE_FUNC）
- ✅ `_compare_sorted()` - 排序比較
- ✅ `_compare_set()` - 集合比較
- ✅ 路徑輔助函數
- ✅ 檔案操作函數

### 2. case_runner.py 測試

- ✅ 命令列參數處理
- ✅ 檔案路徑驗證
- ✅ 單一測試案例執行
- ✅ 錯誤處理

### 3. test_runner.py 測試

- ✅ 模組載入（solution/generator）
- ✅ 測試案例執行
- ✅ 多解法支援
- ✅ 比較模式（exact/sorted/set）
- ✅ JUDGE_FUNC 支援
- ✅ 效能測試
- ✅ 失敗案例保存

### 4. complexity_estimator.py 測試

- ✅ 可用性檢查
- ✅ 複雜度估算
- ✅ Mock stdin 機制
- ✅ 結果格式化

### 5. 邊界條件測試

- ✅ 空輸入
- ✅ 錯誤輸入
- ✅ 大資料
- ✅ 特殊字元（Unicode、emoji、CJK）
- ✅ 格式錯誤的資料

### 6. 整合測試

- ✅ 端到端工作流程
- ✅ 多解法整合
- ✅ 比較模式整合
- ✅ JUDGE_FUNC 整合

## 測試原則

1. **行為測試優先**：測試「做什麼」而不是「怎麼做」
2. **輸入輸出驗證**：給定相同輸入，確保得到相同輸出
3. **邊界條件覆蓋**：測試極端情況和錯誤處理
4. **獨立性**：每個測試應該獨立運行，不依賴其他測試
5. **可重複性**：測試結果應該是確定性的

## 重構指南

當你重構 runner 系統時：

1. **先運行所有測試**：確保當前狀態下所有測試都通過
2. **進行重構**：修改實作細節
3. **再次運行測試**：確保行為沒有改變
4. **如果測試失敗**：
   - 如果是預期的行為改變，更新測試
   - 如果是意外的破壞，修復代碼

## 添加新測試

當你添加新功能時：

1. 在對應的測試文件中添加測試
2. 使用適當的測試標記
3. 確保測試覆蓋正常情況和邊界情況
4. 更新本 README

## 已知限制

- 某些測試需要 `big-O` 套件（標記為 `@pytest.mark.requires_big_o`）
- 整合測試會創建臨時檔案和目錄
- 某些測試可能在不同作業系統上有細微差異（路徑分隔符等）

## 聯絡資訊

如有問題或建議，請聯絡測試負責人：luffdev


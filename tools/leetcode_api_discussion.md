# LeetCode API 後處理與格式討論

## API 結構分析

### API 端點
```
https://leetcode.com/api/problems/all/
```

### 關鍵欄位（在 `stat` 物件中）

| 欄位 | 類型 | 範例 | 用途 |
|------|------|------|------|
| `question_id` | int | `11` | 題號（後端 ID） |
| `question__title` | str | `"Container With Most Water"` | 完整題目名稱 |
| `question__title_slug` | str | `"container-with-most-water"` | URL slug（用於生成連結） |
| `frontend_question_id` | int/str | `11` 或 `"11"` | 前端顯示的題號 |

### 其他重要欄位（在根物件中）

| 欄位 | 類型 | 說明 |
|------|------|------|
| `difficulty.level` | int | `1`=Easy, `2`=Medium, `3`=Hard |
| `paid_only` | bool | 是否需要付費 |
| `status` | str/null | `null`, `"ac"`, `"notac"`, `"notstart"` |

### API 回應結構範例

```json
{
  "stat_status_pairs": [
    {
      "stat": {
        "question_id": 11,
        "question__title": "Container With Most Water",
        "question__title_slug": "container-with-most-water",
        "frontend_question_id": 11,
        "total_acs": 4834315,
        "total_submitted": 8179392
      },
      "difficulty": {
        "level": 2
      },
      "paid_only": false,
      "status": null
    }
  ],
  "num_total": 3778,
  "num_solved": 0
}
```

---

## 我們的格式對應

### 檔案命名格式
```
{question_id:04d}_{question__title_slug}.py
```

**範例：**
- API: `question_id=11`, `slug="container-with-most-water"`
- 檔案: `0011_container_with_most_water.py`

### 問題連結格式
```
https://leetcode.com/problems/{question__title_slug}/description/
```

**範例：**
- `https://leetcode.com/problems/container-with-most-water/description/`

---

## 後處理流程建議

### 1. 資料擷取與轉換

```python
def extract_problem_data(api_response):
    """從 API 回應中提取問題資料"""
    problems = {}
    
    for pair in api_response['stat_status_pairs']:
        stat = pair['stat']
        qid = stat['question_id']
        
        problem = {
            'id': f"{qid:04d}",  # 標準化為 4 位數
            'question_id': qid,
            'title': stat['question__title'],
            'slug': stat['question__title_slug'],
            'url': f"https://leetcode.com/problems/{stat['question__title_slug']}/description/",
            'difficulty': ['Easy', 'Medium', 'Hard'][pair['difficulty']['level'] - 1],
            'paid_only': pair.get('paid_only', False),
            'status': pair.get('status'),
        }
        
        problems[problem['id']] = problem
    
    return problems
```

### 2. 檔案名稱對應

**問題：** API 的 `question__title_slug` 使用連字號（`container-with-most-water`），
但我們的檔案名稱使用底線（`0011_container_with_most_water.py`）。

**解決方案：**
- **選項 A：** 保持現有格式，在後處理時轉換
  ```python
  def slug_to_filename(slug: str) -> str:
      """將 slug 轉換為檔案名稱格式"""
      return slug.replace('-', '_')
  
  def filename_to_slug(filename: str) -> str:
      """將檔案名稱轉換為 slug"""
      # 移除前綴數字和底線
      slug = re.sub(r'^\d+_', '', filename)
      return slug.replace('_', '-')
  ```

- **選項 B：** 統一使用 API 的 slug 格式（需要重命名現有檔案）

### 3. 連結生成策略

**當前後處理邏輯**（`post_processing.py`）：

1. **文字替換**：`LC 11` → `LeetCode 11`
2. **連結轉換**：`LeetCode 11` → `[LeetCode 11 - Title](url)`
3. **URL 正規化**：確保所有連結以 `/description/` 結尾
4. **GitHub 連結**：自動添加 solution 連結

**建議改進：**

```python
def generate_leetcode_url(slug: str, use_description: bool = True) -> str:
    """生成 LeetCode 問題連結"""
    base = f"https://leetcode.com/problems/{slug}"
    if use_description:
        return f"{base}/description/"
    return base

def normalize_slug(slug: str) -> str:
    """
    正規化 slug 格式
    
    處理情況：
    - 0011_container_with_most_water → container-with-most-water
    - container-with-most-water → container-with-most-water (已正確)
    - container_with_most_water → container-with-most-water
    """
    # 移除前綴數字和底線
    slug = re.sub(r'^\d+_', '', slug)
    # 將底線轉換為連字號
    slug = slug.replace('_', '-')
    return slug
```

---

## 資料同步策略

### 方案 1：定期同步（推薦）

```python
# tools/sync_leetcode_data.py
def sync_leetcode_data():
    """定期從 LeetCode API 同步問題資料"""
    api_data = fetch_leetcode_problems()
    problems = extract_problem_data(api_data)
    
    # 更新本地 metadata
    update_problem_metadata(problems)
    
    # 驗證檔案存在性
    validate_solution_files(problems)
```

### 方案 2：按需查詢

```python
# 在生成 mindmap 時動態查詢
def get_problem_info(problem_id: int):
    """從 API 或快取獲取問題資訊"""
    # 先檢查本地快取
    if problem_id in local_cache:
        return local_cache[problem_id]
    
    # 查詢 API
    api_data = fetch_leetcode_problems()
    problem = find_problem_by_id(api_data, problem_id)
    
    # 更新快取
    local_cache[problem_id] = problem
    return problem
```

---

## 格式一致性檢查

### 檢查項目

1. **檔案命名一致性**
   - 檔案名稱是否與 `question_id` 和 `slug` 對應？
   - 是否有重複或衝突的檔案名稱？

2. **連結正確性**
   - 所有 LeetCode 連結是否使用正確的 slug？
   - 是否都包含 `/description/` 後綴？

3. **資料完整性**
   - 是否有本地檔案但 API 中找不到對應問題？
   - 是否有 API 問題但本地沒有檔案？

### 驗證腳本

```python
def validate_format_consistency():
    """驗證格式一致性"""
    api_data = fetch_leetcode_problems()
    local_files = list_solution_files()
    
    issues = []
    
    for file in local_files:
        # 解析檔案名稱
        match = re.match(r'(\d{4})_(.+)\.py', file)
        if not match:
            issues.append(f"Invalid filename format: {file}")
            continue
        
        qid, slug = match.groups()
        
        # 檢查 API 中是否存在
        api_problem = find_problem_by_id(api_data, int(qid))
        if not api_problem:
            issues.append(f"Problem {qid} not found in API")
            continue
        
        # 檢查 slug 是否匹配
        expected_slug = api_problem['stat']['question__title_slug']
        if slug.replace('_', '-') != expected_slug:
            issues.append(
                f"Slug mismatch for {qid}: "
                f"file={slug}, api={expected_slug}"
            )
    
    return issues
```

---

## 討論重點

### 1. Slug 格式統一

**問題：** API 使用連字號，檔案名稱使用底線。

**實際情況：**
- API 的 `question__title_slug`: `"container-with-most-water"` (連字號)
- 我們的檔案名稱: `0011_container_with_most_water.py` (底線)
- LeetCode URL: `https://leetcode.com/problems/container-with-most-water/` (連字號)

**為什麼保持現狀？**
1. **檔案名稱用底線**：Python 檔案名稱慣例，避免連字號（會被視為減號）
2. **URL 用連字號**：網頁 URL 標準格式
3. **後處理轉換**：在生成連結時自動轉換，不需要改動現有檔案

**轉換邏輯（已實作在 `post_processing.py`）：**
```python
# 檔案名稱 → URL slug
"0011_container_with_most_water" 
  → 移除前綴 "0011_" 
  → "container_with_most_water"
  → 底線轉連字號
  → "container-with-most-water"
  → URL: "https://leetcode.com/problems/container-with-most-water/description/"
```

**建議：** ✅ 保持現狀，在後處理層面處理轉換（無需改動現有檔案）。

### 2. 問題 ID 對應

**問題：** API 提供兩個 ID 欄位，應該用哪一個？

**兩個 ID 的區別：**
- `question_id` (後端 ID)：內部資料庫 ID，例如 `4169`
- `frontend_question_id` (前端 ID)：顯示給用戶的題號，例如 `3764`

**實際觀察：**
- 經典問題（如 LeetCode 1-300）：兩者通常相同
  - 問題 11: `question_id=11`, `frontend_question_id=11` ✅ 相同
- 較新問題：兩者可能不同
  - 問題 4169: `question_id=4169`, `frontend_question_id=3764` ❌ 不同

**為什麼使用 `question_id`？**
1. **檔案命名一致性**：我們的檔案是 `0011_container_with_most_water.py`，使用 `question_id=11`
2. **唯一性保證**：`question_id` 是後端主鍵，保證唯一
3. **向後相容**：現有檔案都基於 `question_id` 命名

**建議：** ✅ 使用 `question_id` 作為主要 ID（與檔案命名一致）。

### 3. 連結格式

**當前格式：**
```
https://leetcode.com/problems/{slug}/description/
```

**選項：**
- ✅ `/description/` - 包含完整描述頁面
- `/` - 簡潔版本
- `/solutions/` - 解決方案頁面

**建議：** 保持 `/description/` 格式（當前標準）。

### 4. 資料更新頻率

**選項：**
- **即時查詢**：每次生成時查詢 API（慢，但最新）
- **定期快取**：每日/每週更新一次（快，但可能過時）
- **手動觸發**：需要時手動更新（可控）

**建議：** 定期快取 + 手動觸發更新。

---

## 實作建議

### 階段 1：資料擷取工具
- [x] 建立 `tools/fetch_leetcode_api.py`（已完成）
- [x] 建立資料轉換函數（`sync_leetcode_data.py`）
- [x] 建立快取機制（`tools/.cache/leetcode_problems.json`）

**使用方式：**
```bash
# 更新快取（如果過期）
python tools/sync_leetcode_data.py

# 檢查快取狀態
python tools/sync_leetcode_data.py --check

# 強制更新（忽略快取）
python tools/sync_leetcode_data.py --force
```

**快取設定：**
- 位置：`tools/.cache/leetcode_problems.json`
- 有效期：7 天
- 自動檢查：使用時自動檢查是否過期

### 階段 2：後處理增強
- [x] 整合 API 資料到 `PostProcessor`（已完成）
- [x] 改進 slug 正規化邏輯（已存在於 `_normalize_slug`）
- [x] 驗證連結正確性（自動從 API 資料生成）

**實作細節：**
- 建立 `tools/ai-markmap-agent/src/leetcode_api.py` 模組
- 修改 `PostProcessor.__init__` 自動合併 API 快取資料
- 優先使用本地資料，API 資料作為補充
- 自動為缺少 URL 的問題生成正確的 LeetCode 連結

### 階段 3：驗證工具
- [ ] 建立格式一致性檢查腳本
- [ ] 建立資料同步腳本
- [ ] 整合到 CI/CD

---

## 已實作功能

### ✅ 資料同步工具 (`sync_leetcode_data.py`)

**功能：**
- 從 LeetCode API 獲取所有問題資料
- 自動轉換為本地格式
- 快取到本地檔案（有效期 7 天）
- 支援手動觸發更新

**使用方式：**
```bash
# 更新快取（如果過期）
python tools/sync_leetcode_data.py

# 檢查快取狀態
python tools/sync_leetcode_data.py --check

# 強制更新（忽略快取）
python tools/sync_leetcode_data.py --force
```

**快取位置：**
- 問題資料：`tools/.cache/leetcode_problems.json`
- 元資料：`tools/.cache/leetcode_cache_meta.json`

### ✅ 使用範例 (`leetcode_api_usage_example.py`)

展示如何：
- 根據題號查找問題
- 根據難度篩選問題
- 生成 LeetCode 連結
- 驗證 slug 格式轉換

---

## 下一步行動

1. ✅ **確認格式偏好**：檔案名稱保持底線格式（已確認）
2. ✅ **決定同步策略**：定期快取 + 手動觸發更新（已實作）
3. ✅ **實作資料轉換**：已建立轉換函數
4. ✅ **整合後處理**：將 API 資料整合到現有後處理流程（已完成）

**整合方式：**
- `PostProcessor` 自動載入並合併 LeetCode API 快取資料
- 如果本地 TOML 檔案缺少 URL 或 slug，自動從 API 資料補充
- 無需修改現有程式碼，自動生效

---

## 參考資料

- [LeetCode API 結構分析腳本](tools/fetch_leetcode_api.py)
- [資料同步工具](tools/sync_leetcode_data.py)
- [API 整合模組](tools/ai-markmap-agent/src/leetcode_api.py)
- [後處理模組](tools/ai-markmap-agent/src/post_processing.py)
- [問題資料結構](tools/mindmaps/data.py)
- [使用範例](tools/leetcode_api_usage_example.py)
- [整合測試](tools/test_leetcode_api_integration.py)

---

## 完成總結

### ✅ 已實作功能

1. **資料同步工具** (`sync_leetcode_data.py`)
   - 從 LeetCode API 獲取所有問題資料
   - 自動快取到本地（有效期 7 天）
   - 支援手動觸發更新

2. **API 整合模組** (`ai-markmap-agent/src/leetcode_api.py`)
   - 載入快取資料
   - 合併本地與 API 資料
   - 提供 URL 和 slug 查詢函數

3. **後處理整合** (`post_processing.py`)
   - 自動合併 API 資料
   - 為缺少 URL 的問題自動生成連結
   - 無需修改現有程式碼

4. **測試與驗證**
   - 整合測試腳本
   - 使用範例
   - 所有功能測試通過

### 🎯 使用方式

```bash
# 1. 首次同步（建立快取）
python tools/sync_leetcode_data.py

# 2. 檢查快取狀態
python tools/sync_leetcode_data.py --check

# 3. 強制更新
python tools/sync_leetcode_data.py --force

# 4. 測試整合
python tools/test_leetcode_api_integration.py
```

### 📝 注意事項

- 快取位置：`tools/.cache/leetcode_problems.json`
- 快取有效期：7 天（自動檢查）
- 整合方式：`PostProcessor` 自動載入，無需額外配置
- 資料優先順序：本地 TOML > API 快取


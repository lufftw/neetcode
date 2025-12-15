# Post-Processing Solution Links 检查报告

## 处理流程

后处理按以下顺序执行（`PostProcessor.process()` 方法）：

### Step 1: 文本替换
- `LC 11` → `LeetCode 11`
- `LC-11` → `LeetCode 11`

### Step 2: 转换纯文本为链接 (`_convert_plain_leetcode_to_links`)
- 处理现有链接：`[LeetCode 79 - Word Search](wrong_url)` → `[LeetCode 79](correct_url)`
- 处理纯文本：`LeetCode 79` → `[LeetCode 79](url)`
- 使用 `meta/problems/*.toml` 中的 URL 数据

### Step 3: 规范化 LeetCode 链接 (`_normalize_leetcode_links`)
- 修复 URL 格式，确保以 `/description/` 结尾
- 例如：`https://leetcode.com/problems/word-search/` → `https://leetcode.com/problems/word-search/description/`

### Step 4: 添加 Solution 链接 (`_add_github_solution_links`)
- 查找所有 `[LeetCode {id}](url)` 格式的链接
- 如果该问题在 `meta/problems/*.toml` 中有 `[files].solution` 字段
- 添加 Solution 链接：`[LeetCode 79](url) | [Solution](github_url)`

## Solution 链接处理逻辑

### 1. 问题查找 (`_add_github_solution_links`)

```python
# 从链接文本中提取问题ID
id_match = re.search(r'LeetCode\s+(\d+)', link_text)
problem_id = id_match.group(1)  # 例如: "79"

# 尝试多种ID格式查找
lookup_keys = [
    problem_id.zfill(4),      # "0079"
    problem_id,              # "79"
    str(int(problem_id)).zfill(4),  # "0079" (normalized)
    str(int(problem_id))     # "79" (normalized)
]

for key in lookup_keys:
    problem = self.problems_lookup.get(key)
    if problem:
        break
```

### 2. Solution 文件检查

```python
# 检查是否有solution文件
files = problem.get("files", {})
solution_file = files.get("solution", "")

if solution_file:
    # 生成GitHub URL
    github_url = self.github_template.format(solution_file=solution_file)
    # 添加链接
    return f"{full_text} | [Solution]({github_url})"
```

### 3. 问题数据查找表构建 (`_build_problems_lookup`)

从 `meta/problems/*.toml` 文件加载数据：

```toml
# 0079_word_search.toml
id = "0079"
leetcode_id = 79
[files]
solution = "solutions/0079_word_search.py"
```

查找表会存储多个key格式：
- `"0079"` → problem data
- `"79"` → problem data
- `str(int("0079"))` → problem data (如果不同)

## 数据流

```
state.get("problems", {})  # 从DataSourcesLoader加载
    ↓
PostProcessor(config, problems=problems)
    ↓
merge_leetcode_api_data(problems)  # 合并API缓存数据
    ↓
_build_problems_lookup(problems)  # 构建ID查找表
    ↓
_add_github_solution_links(content)  # 添加Solution链接
```

## 验证检查点

### ✅ 已检查的项目

1. **Problems数据传递**
   - `graph.py:1053`: `PostProcessor(config, problems=state.get("problems", {}))`
   - ✅ 正确传递

2. **查找表构建**
   - `_build_problems_lookup`: 支持多种ID格式
   - ✅ 逻辑正确

3. **Solution链接添加**
   - `_add_github_solution_links`: 检查`files.solution`字段
   - ✅ 逻辑正确

4. **正则表达式匹配**
   - Pattern: `r'\[(LeetCode\s+\d+[^\]]*)\]\(([^)]+)\)'`
   - ✅ 能匹配 `[LeetCode 79](url)` 和 `[LeetCode 79 - Title](url)`

### 🔍 需要验证的项目

1. **Problems数据是否正确加载到state**
   - 检查 `graph.py:1188`: `"problems": data.get("problems", {})`
   - 检查 `main.py:293`: `data = loader.load_all()`

2. **TOML文件中的files字段格式**
   - 确认格式为：`[files] solution = "solutions/0079_word_search.py"`
   - 不是：`files.solution` 或 `files["solution"]`

3. **实际运行时的数据流**
   - 可能需要添加调试输出来验证

## 示例

### 输入
```markdown
[LeetCode 79](https://leetcode.com/problems/word-search/)
```

### 处理过程
1. Step 2: 规范化URL → `[LeetCode 79](https://leetcode.com/problems/word-search/description/)`
2. Step 4: 查找问题ID "79" → 找到 `0079_word_search.toml`
3. Step 4: 检查 `files.solution` → 找到 `"solutions/0079_word_search.py"`
4. Step 4: 生成GitHub URL → `https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py`

### 输出
```markdown
[LeetCode 79](https://leetcode.com/problems/word-search/description/) | [Solution](https://github.com/lufftw/neetcode/blob/main/solutions/0079_word_search.py)
```

## 潜在问题

1. **如果Solution链接没有添加，可能的原因：**
   - Problems数据未正确加载到state
   - TOML文件中缺少 `[files].solution` 字段
   - 问题ID匹配失败（已改进查找逻辑）
   - 正则表达式匹配失败（已验证应该能匹配）

2. **调试建议：**
   - 在 `_add_github_solution_links` 中添加调试输出
   - 检查 `self.problems_lookup` 的内容
   - 验证 `problem.get("files", {})` 的结构

## 改进建议

1. ✅ 已改进：问题ID查找逻辑，支持多种格式
2. ✅ 已改进：更清晰的查找键列表
3. 🔄 可选：添加调试模式，输出查找过程


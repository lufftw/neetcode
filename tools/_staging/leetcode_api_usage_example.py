#!/usr/bin/env python3
"""
LeetCode API 快取資料使用範例

展示如何載入和使用快取的 LeetCode 問題資料。
"""

from pathlib import Path
import json
import sys

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

TOOLS_DIR = Path(__file__).parent.parent
CACHE_FILE = TOOLS_DIR / "leetcode-api" / "crawler" / ".cache" / "leetcode_problems.json"


def load_cached_problems():
    """載入快取的 LeetCode 問題資料"""
    if not CACHE_FILE.exists():
        print(f"❌ 快取檔案不存在: {CACHE_FILE}")
        print("   請先執行: python tools/leetcode-api/crawler/sync_leetcode_data.py")
        return None
    
    with open(CACHE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def example_1_find_problem_by_id():
    """範例 1: 根據題號查找問題"""
    print("\n" + "="*60)
    print("範例 1: 根據題號查找問題")
    print("="*60)
    
    problems = load_cached_problems()
    if not problems:
        return
    
    # 查找問題 11
    problem_id = "0011"
    problem = problems.get(problem_id)
    
    if problem:
        print(f"找到問題 {problem_id}:")
        print(f"  標題: {problem['title']}")
        print(f"  Slug: {problem['slug']}")
        print(f"  URL: {problem['url']}")
        print(f"  難度: {problem['difficulty']}")
        print(f"  付費: {'是' if problem['paid_only'] else '否'}")
    else:
        print(f"未找到問題 {problem_id}")


def example_2_find_problems_by_difficulty():
    """範例 2: 根據難度篩選問題"""
    print("\n" + "="*60)
    print("範例 2: 根據難度篩選問題")
    print("="*60)
    
    problems = load_cached_problems()
    if not problems:
        return
    
    difficulty = "Medium"
    medium_problems = [
        p for p in problems.values()
        if p['difficulty'] == difficulty and not p['paid_only']
    ]
    
    print(f"找到 {len(medium_problems)} 個免費的 {difficulty} 問題")
    print("\n前 10 個問題:")
    for p in medium_problems[:10]:
        print(f"  LeetCode {p['question_id']}: {p['title']}")


def example_3_generate_leetcode_url():
    """範例 3: 生成 LeetCode 連結"""
    print("\n" + "="*60)
    print("範例 3: 生成 LeetCode 連結")
    print("="*60)
    
    problems = load_cached_problems()
    if not problems:
        return
    
    # 從檔案名稱生成連結
    filename = "0011_container_with_most_water.py"
    
    # 解析檔案名稱
    parts = filename.replace('.py', '').split('_', 1)
    if len(parts) == 2:
        problem_id = parts[0]
        problem = problems.get(problem_id)
        
        if problem:
            print(f"檔案: {filename}")
            print(f"問題 ID: {problem_id}")
            print(f"LeetCode 連結: {problem['url']}")
            print(f"Markdown 格式:")
            print(f"  [LeetCode {problem['question_id']} - {problem['title']}]({problem['url']})")
        else:
            print(f"未找到問題 {problem_id}")


def example_4_validate_slug_format():
    """範例 4: 驗證 slug 格式轉換"""
    print("\n" + "="*60)
    print("範例 4: 驗證 slug 格式轉換")
    print("="*60)
    
    problems = load_cached_problems()
    if not problems:
        return
    
    # 測試幾個問題的 slug 轉換
    test_cases = [
        ("0011", "container-with-most-water"),
        ("0001", "two-sum"),
        ("0003", "longest-substring-without-repeating-characters"),
    ]
    
    print("檔案名稱格式 → URL slug 格式:")
    for problem_id, expected_slug in test_cases:
        problem = problems.get(problem_id)
        if problem:
            # 模擬檔案名稱（底線格式）
            filename_slug = problem['slug'].replace('-', '_')
            # API slug（連字號格式）
            api_slug = problem['slug']
            
            print(f"  {problem_id}_{filename_slug}.py")
            print(f"    → {api_slug}")
            print(f"    → {problem['url']}")
            print()


if __name__ == "__main__":
    print("LeetCode API 快取資料使用範例")
    print("="*60)
    
    example_1_find_problem_by_id()
    example_2_find_problems_by_difficulty()
    example_3_generate_leetcode_url()
    example_4_validate_slug_format()
    
    print("\n" + "="*60)
    print("✅ 範例執行完成")
    print("="*60)


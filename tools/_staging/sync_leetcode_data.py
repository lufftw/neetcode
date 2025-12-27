#!/usr/bin/env python3
"""
LeetCode API 資料同步工具

功能：
1. 從 LeetCode API 獲取所有問題資料
2. 轉換為本地格式
3. 快取到本地檔案
4. 支援手動觸發更新

使用方式：
    python tools/sync_leetcode_data.py              # 更新快取
    python tools/sync_leetcode_data.py --check      # 檢查快取是否過期
    python tools/sync_leetcode_data.py --force      # 強制更新（忽略快取）
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Paths
TOOLS_DIR = Path(__file__).parent
PROJECT_ROOT = TOOLS_DIR.parent
CACHE_DIR = TOOLS_DIR / ".cache"
CACHE_FILE = CACHE_DIR / "leetcode_problems.json"
CACHE_META_FILE = CACHE_DIR / "leetcode_cache_meta.json"

# Cache settings
CACHE_EXPIRY_DAYS = 7  # 快取有效期：7 天


def fetch_leetcode_problems() -> Dict[str, Any]:
    """從 LeetCode API 獲取所有問題資料"""
    print("📡 正在從 LeetCode API 獲取資料...")
    url = "https://leetcode.com/api/problems/all/"
    
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode())
        print(f"✅ 成功獲取 {len(data.get('stat_status_pairs', []))} 個問題")
        return data
    except urllib.error.URLError as e:
        print(f"❌ 無法連接到 LeetCode API: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ API 回應格式錯誤: {e}")
        sys.exit(1)


def extract_problem_data(api_response: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    從 API 回應中提取並轉換問題資料
    
    轉換規則：
    - question_id → id (標準化為 4 位數)
    - question__title_slug → slug
    - 生成 LeetCode URL
    - 轉換難度等級
    """
    problems = {}
    difficulty_map = {1: "Easy", 2: "Medium", 3: "Hard"}
    
    for pair in api_response.get('stat_status_pairs', []):
        stat = pair.get('stat', {})
        qid = stat.get('question_id')
        
        if not qid:
            continue
        
        slug = stat.get('question__title_slug', '')
        title = stat.get('question__title', '')
        difficulty_level = pair.get('difficulty', {}).get('level', 0)
        
        problem = {
            'id': f"{qid:04d}",  # 標準化為 4 位數，例如 "0011"
            'question_id': qid,  # 原始 ID
            'frontend_question_id': stat.get('frontend_question_id', qid),
            'title': title,
            'slug': slug,
            'url': f"https://leetcode.com/problems/{slug}/description/" if slug else "",
            'difficulty': difficulty_map.get(difficulty_level, "Unknown"),
            'difficulty_level': difficulty_level,
            'paid_only': pair.get('paid_only', False),
            'status': pair.get('status'),
            'total_acs': stat.get('total_acs', 0),
            'total_submitted': stat.get('total_submitted', 0),
            'is_new_question': stat.get('is_new_question', False),
        }
        
        problems[problem['id']] = problem
    
    return problems


def save_cache(problems: Dict[str, Dict[str, Any]], metadata: Dict[str, Any]) -> None:
    """儲存快取資料"""
    CACHE_DIR.mkdir(exist_ok=True)
    
    # 儲存問題資料
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(problems, f, indent=2, ensure_ascii=False)
    
    # 儲存元資料
    with open(CACHE_META_FILE, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"💾 快取已儲存到: {CACHE_FILE}")
    print(f"   共 {len(problems)} 個問題")


def load_cache() -> tuple[Dict[str, Dict[str, Any]] | None, Dict[str, Any] | None]:
    """載入快取資料"""
    if not CACHE_FILE.exists() or not CACHE_META_FILE.exists():
        return None, None
    
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            problems = json.load(f)
        
        with open(CACHE_META_FILE, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        return problems, metadata
    except (json.JSONDecodeError, IOError) as e:
        print(f"⚠️  無法讀取快取: {e}")
        return None, None


def is_cache_valid(metadata: Dict[str, Any] | None) -> bool:
    """檢查快取是否有效（未過期）"""
    if not metadata:
        return False
    
    cache_time_str = metadata.get('cached_at')
    if not cache_time_str:
        return False
    
    try:
        cache_time = datetime.fromisoformat(cache_time_str)
        expiry_time = cache_time + timedelta(days=CACHE_EXPIRY_DAYS)
        return datetime.now() < expiry_time
    except (ValueError, TypeError):
        return False


def get_cache_age(metadata: Dict[str, Any] | None) -> str:
    """獲取快取年齡（人類可讀格式）"""
    if not metadata:
        return "無快取"
    
    cache_time_str = metadata.get('cached_at')
    if not cache_time_str:
        return "無時間戳"
    
    try:
        cache_time = datetime.fromisoformat(cache_time_str)
        age = datetime.now() - cache_time
        
        if age.days > 0:
            return f"{age.days} 天前"
        elif age.seconds > 3600:
            return f"{age.seconds // 3600} 小時前"
        elif age.seconds > 60:
            return f"{age.seconds // 60} 分鐘前"
        else:
            return "剛剛"
    except (ValueError, TypeError):
        return "時間戳格式錯誤"


def sync_data(force: bool = False) -> Dict[str, Dict[str, Any]]:
    """
    同步 LeetCode 資料
    
    Args:
        force: 是否強制更新（忽略快取）
    
    Returns:
        問題資料字典
    """
    # 檢查快取
    if not force:
        problems, metadata = load_cache()
        if problems and is_cache_valid(metadata):
            age = get_cache_age(metadata)
            print(f"✅ 使用快取資料（{age}）")
            print(f"   共 {len(problems)} 個問題")
            return problems
    
    # 從 API 獲取資料
    api_data = fetch_leetcode_problems()
    problems = extract_problem_data(api_data)
    
    # 儲存快取
    metadata = {
        'cached_at': datetime.now().isoformat(),
        'total_problems': len(problems),
        'cache_version': '1.0',
    }
    save_cache(problems, metadata)
    
    return problems


def check_cache_status() -> None:
    """檢查快取狀態"""
    problems, metadata = load_cache()
    
    if not problems or not metadata:
        print("❌ 無快取資料")
        print("   執行 'python tools/sync_leetcode_data.py' 來建立快取")
        return
    
    age = get_cache_age(metadata)
    is_valid = is_cache_valid(metadata)
    
    print(f"📊 快取狀態:")
    print(f"   問題數量: {len(problems)}")
    print(f"   快取時間: {age}")
    print(f"   是否有效: {'✅ 是' if is_valid else '❌ 已過期'}")
    
    if not is_valid:
        expiry_days = CACHE_EXPIRY_DAYS
        print(f"   建議: 執行 'python tools/sync_leetcode_data.py' 更新快取（有效期 {expiry_days} 天）")


def main():
    parser = argparse.ArgumentParser(
        description="LeetCode API 資料同步工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例:
  python tools/sync_leetcode_data.py          # 更新快取（如果過期）
  python tools/sync_leetcode_data.py --check  # 只檢查快取狀態
  python tools/sync_leetcode_data.py --force  # 強制更新（忽略快取）
        """
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='只檢查快取狀態，不更新'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='強制更新，忽略快取'
    )
    
    args = parser.parse_args()
    
    if args.check:
        check_cache_status()
    else:
        problems = sync_data(force=args.force)
        print(f"\n✅ 同步完成！共 {len(problems)} 個問題")


if __name__ == "__main__":
    main()


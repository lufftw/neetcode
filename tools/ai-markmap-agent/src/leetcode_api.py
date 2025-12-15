"""
LeetCode API 快取資料載入模組

提供函數來載入和整合 LeetCode API 快取資料到後處理流程。
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict

# 快取檔案路徑（相對於專案根目錄）
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
CACHE_FILE = PROJECT_ROOT / "tools" / ".cache" / "leetcode_problems.json"


def load_leetcode_cache() -> Dict[str, Dict[str, Any]] | None:
    """
    載入 LeetCode API 快取資料。
    
    Returns:
        問題資料字典，key 為標準化的 4 位數 ID（如 "0011"），
        如果快取不存在則返回 None
    """
    if not CACHE_FILE.exists():
        return None
    
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def merge_leetcode_api_data(
    existing_problems: Dict[str, Any],
    api_problems: Dict[str, Dict[str, Any]] | None = None
) -> Dict[str, Any]:
    """
    合併現有問題資料與 LeetCode API 資料。
    
    優先順序：
    1. 現有資料（如果存在）
    2. API 資料（作為補充）
    
    Args:
        existing_problems: 現有的問題資料（從 TOML 檔案載入）
        api_problems: LeetCode API 快取資料
    
    Returns:
        合併後的問題資料字典
    """
    if api_problems is None:
        api_problems = load_leetcode_cache()
    
    if not api_problems:
        return existing_problems
    
    # 複製現有資料
    merged = existing_problems.copy()
    
    # 為每個問題補充 API 資料
    for problem_id, problem_data in merged.items():
        # 標準化 ID 以查找 API 資料
        normalized_id = problem_id
        if isinstance(problem_id, str) and problem_id.isdigit():
            normalized_id = problem_id.zfill(4)
        
        api_data = api_problems.get(normalized_id)
        if api_data:
            # 補充 API 資料（不覆蓋現有欄位）
            if "url" not in problem_data or not problem_data.get("url"):
                problem_data["url"] = api_data.get("url", "")
            
            if "slug" not in problem_data or not problem_data.get("slug"):
                problem_data["slug"] = api_data.get("slug", "")
            
            if "title" not in problem_data or not problem_data.get("title"):
                problem_data["title"] = api_data.get("title", "")
            
            # 添加 API 特有的欄位（如果不存在）
            if "question_id" not in problem_data:
                problem_data["question_id"] = api_data.get("question_id")
            
            if "difficulty" not in problem_data:
                problem_data["difficulty"] = api_data.get("difficulty", "")
    
    # 添加 API 中有但本地沒有的問題（作為參考）
    # 注意：只添加真正本地沒有的問題，避免覆蓋本地 TOML 資料
    for api_id, api_data in api_problems.items():
        # 檢查是否已經存在（可能以不同的 key 格式存在，如 "0001_two_sum"）
        # 標準化 api_id 以便比較
        normalized_api_id = api_id
        if isinstance(api_id, str) and api_id.isdigit():
            normalized_api_id = api_id.zfill(4)
        
        # 檢查是否已經存在（檢查所有可能的 key 格式）
        exists = False
        for key in merged.keys():
            # 檢查 key 是否匹配（可能是 "0001" 或 "0001_two_sum"）
            if key == normalized_api_id or key == api_id:
                exists = True
                break
            # 檢查 key 是否以 ID 開頭（如 "0001_two_sum"）
            if isinstance(key, str):
                match = re.match(r'^(\d+)_', key)
                if match and match.group(1).zfill(4) == normalized_api_id:
                    exists = True
                    break
        
        if not exists:
            # 只添加基本資訊，標記為 API 來源
            merged[api_id] = {
                "id": api_id,
                "title": api_data.get("title", ""),
                "slug": api_data.get("slug", ""),
                "url": api_data.get("url", ""),
                "difficulty": api_data.get("difficulty", ""),
                "question_id": api_data.get("question_id"),
                "_source": "api",  # 標記來源
            }
    
    return merged


def get_problem_url_from_api(problem_id: str | int) -> str | None:
    """
    從 API 快取獲取問題的 LeetCode URL。
    
    Args:
        problem_id: 問題 ID（可以是字串或整數）
    
    Returns:
        LeetCode URL，如果找不到則返回 None
    """
    api_problems = load_leetcode_cache()
    if not api_problems:
        return None
    
    # 標準化 ID
    if isinstance(problem_id, int):
        normalized_id = f"{problem_id:04d}"
    elif isinstance(problem_id, str) and problem_id.isdigit():
        normalized_id = problem_id.zfill(4)
    else:
        normalized_id = problem_id
    
    problem = api_problems.get(normalized_id)
    if problem:
        return problem.get("url")
    
    return None


def get_problem_slug_from_api(problem_id: str | int) -> str | None:
    """
    從 API 快取獲取問題的 slug。
    
    Args:
        problem_id: 問題 ID（可以是字串或整數）
    
    Returns:
        問題 slug，如果找不到則返回 None
    """
    api_problems = load_leetcode_cache()
    if not api_problems:
        return None
    
    # 標準化 ID
    if isinstance(problem_id, int):
        normalized_id = f"{problem_id:04d}"
    elif isinstance(problem_id, str) and problem_id.isdigit():
        normalized_id = problem_id.zfill(4)
    else:
        normalized_id = problem_id
    
    problem = api_problems.get(normalized_id)
    if problem:
        return problem.get("slug")
    
    return None


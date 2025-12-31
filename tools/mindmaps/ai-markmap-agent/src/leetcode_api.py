"""
LeetCode API 快取資料載入模組

使用 leetcode_datasource package 提供函數來載入和整合 LeetCode 問題資料。
"""

from __future__ import annotations

import re
from typing import Any, Dict, Optional

# Use leetcode_datasource package for problem index lookup
from leetcode_datasource import LeetCodeDataSource

# Singleton datasource instance
_datasource: Optional[LeetCodeDataSource] = None


def get_datasource() -> LeetCodeDataSource:
    """Get or initialize the LeetCodeDataSource singleton."""
    global _datasource
    if _datasource is None:
        _datasource = LeetCodeDataSource()
    return _datasource


def load_leetcode_cache() -> Dict[str, Dict[str, Any]] | None:
    """
    載入 LeetCode 問題資料，使用 leetcode_datasource package。
    
    Returns:
        包含 datasource 的 dict，用於後續查找
    """
    ds = get_datasource()
    
    # Check if problem_index is populated
    stats = ds.stats()
    if stats.get('problem_index_count', 0) == 0:
        # Try to sync
        try:
            ds.sync_problem_list()
        except Exception:
            return None
    
    return {"_datasource": ds}


def _get_problem_info_as_dict(ds: LeetCodeDataSource, frontend_id: int) -> Dict[str, Any] | None:
    """Get problem info from datasource as a dict."""
    info = ds.get_problem_info(frontend_id)
    if info:
        return {
            "frontend_question_id": info.frontend_question_id,
            "question_id": info.question_id,
            "title": info.title,
            "slug": info.title_slug,
            "url": info.url,
            "difficulty": info.difficulty,
        }
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
    
    # Get datasource
    ds = api_problems.get("_datasource")
    if not ds:
        return existing_problems
    
    # 複製現有資料
    merged = existing_problems.copy()
    
    # 為每個問題補充 API 資料
    for problem_id, problem_data in merged.items():
        # Extract frontend_id for lookup
        frontend_id = None
        
        if isinstance(problem_id, str):
            if problem_id.isdigit():
                frontend_id = int(problem_id)
            else:
                # Try to extract from key like "0001_two_sum"
                match = re.match(r'^(\d+)', problem_id)
                if match:
                    frontend_id = int(match.group(1))
        elif isinstance(problem_id, int):
            frontend_id = problem_id
        
        if frontend_id is None:
            continue
        
        api_data = _get_problem_info_as_dict(ds, frontend_id)
        if api_data:
            # 使用 API 快取資料作為一致性來源
            # Title 優先使用 API 快取（確保資料一致）
            api_title = api_data.get("title", "")
            if api_title:
                problem_data["title"] = api_title
            
            # 補充缺失欄位
            if "url" not in problem_data or not problem_data.get("url"):
                problem_data["url"] = api_data.get("url", "")
            
            if "slug" not in problem_data or not problem_data.get("slug"):
                problem_data["slug"] = api_data.get("slug", "")
            
            if "difficulty" not in problem_data or not problem_data.get("difficulty"):
                problem_data["difficulty"] = api_data.get("difficulty", "")
            
            # 添加 API 特有的欄位（如果不存在）
            if "question_id" not in problem_data:
                problem_data["question_id"] = api_data.get("question_id")
    
    return merged


def get_problem_url_from_api(problem_id: str | int) -> str | None:
    """
    從 problem_index 獲取問題的 LeetCode URL。
    
    Args:
        problem_id: 問題 ID（可以是字串或整數）
    
    Returns:
        LeetCode URL，如果找不到則返回 None
    """
    ds = get_datasource()
    
    # 標準化 ID
    if isinstance(problem_id, int):
        frontend_id = problem_id
    elif isinstance(problem_id, str) and problem_id.isdigit():
        frontend_id = int(problem_id)
    else:
        return None
    
    info = ds.get_problem_info(frontend_id)
    if info:
        return info.url
    
    return None


def get_problem_slug_from_api(problem_id: str | int) -> str | None:
    """
    從 problem_index 獲取問題的 slug。
    
    Args:
        problem_id: 問題 ID（可以是字串或整數）
    
    Returns:
        問題 slug，如果找不到則返回 None
    """
    ds = get_datasource()
    
    # 標準化 ID
    if isinstance(problem_id, int):
        frontend_id = problem_id
    elif isinstance(problem_id, str) and problem_id.isdigit():
        frontend_id = int(problem_id)
    else:
        return None
    
    slug = ds.get_slug(frontend_id)
    return slug

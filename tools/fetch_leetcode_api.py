"""
Fetch and analyze LeetCode API data structure.
Temporary script to understand API format for discussion.
"""
import json
import sys
import urllib.request
from typing import Dict, List, Any

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def fetch_leetcode_problems() -> Dict[str, Any]:
    """Fetch all problems from LeetCode API."""
    url = "https://leetcode.com/api/problems/all/"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
    return data


def analyze_api_structure(data: Dict[str, Any], sample_count: int = 5) -> None:
    """Analyze and display API structure with samples."""
    print("=" * 80)
    print("LeetCode API Structure Analysis")
    print("=" * 80)
    
    print(f"\n📊 Total problems: {len(data.get('stat_status_pairs', []))}")
    print(f"📊 User name: {data.get('user_name', 'N/A')}")
    print(f"📊 Num solved: {data.get('num_solved', 0)}")
    print(f"📊 Num total: {data.get('num_total', 0)}")
    
    print("\n" + "=" * 80)
    print("Sample Problem Structure (first 5):")
    print("=" * 80)
    
    pairs = data.get('stat_status_pairs', [])[:sample_count]
    for i, pair in enumerate(pairs, 1):
        print(f"\n--- Problem {i} ---")
        stat = pair.get('stat', {})
        difficulty = pair.get('difficulty', {})
        
        print(f"  question_id: {stat.get('question_id')}")
        print(f"  question__title: {stat.get('question__title')}")
        print(f"  question__title_slug: {stat.get('question__title_slug')}")
        print(f"  total_acs: {stat.get('total_acs', 0)}")
        print(f"  total_submitted: {stat.get('total_submitted', 0)}")
        print(f"  frontend_question_id: {stat.get('frontend_question_id')}")
        print(f"  is_new_question: {stat.get('is_new_question', False)}")
        print(f"  difficulty.level: {difficulty.get('level')} (1=Easy, 2=Medium, 3=Hard)")
        print(f"  paid_only: {pair.get('paid_only', False)}")
        print(f"  status: {pair.get('status')}")
        
        # Show full structure for first item
        if i == 1:
            print(f"\n  Full structure (JSON):")
            print(json.dumps(pair, indent=4, ensure_ascii=False)[:500] + "...")
    
    print("\n" + "=" * 80)
    print("Key Fields for Our Use Case:")
    print("=" * 80)
    print("""
From 'stat' object:
  - question_id: Integer ID (e.g., 11)
  - question__title: Full title (e.g., "Container With Most Water")
  - question__title_slug: URL slug (e.g., "container-with-most-water")
  - frontend_question_id: String ID with leading zeros (e.g., "11" or "1")
  
From root of pair:
  - difficulty.level: 1 (Easy), 2 (Medium), 3 (Hard)
  - paid_only: Boolean
  - status: null, "ac", "notac", "notstart"
    """)


def compare_with_existing_format(data: Dict[str, Any]) -> None:
    """Compare API format with our existing file naming convention."""
    print("\n" + "=" * 80)
    print("Format Comparison: API vs Our Convention")
    print("=" * 80)
    
    # Our format: 0011_container_with_most_water.py
    # API provides:
    #   - question_id: 11 (integer)
    #   - question__title_slug: "container-with-most-water"
    
    pairs = data.get('stat_status_pairs', [])[:10]
    
    print("\nExample mappings:")
    print(f"{'API question_id':<15} {'API slug':<40} {'Our format':<50}")
    print("-" * 105)
    
    for pair in pairs:
        stat = pair.get('stat', {})
        qid = stat.get('question_id')
        slug = stat.get('question__title_slug', '')
        
        # Our format: {question_id:04d}_{slug}.py
        our_format = f"{qid:04d}_{slug}.py"
        
        print(f"{qid:<15} {slug:<40} {our_format:<50}")


if __name__ == "__main__":
    try:
        data = fetch_leetcode_problems()
        analyze_api_structure(data, sample_count=5)
        compare_with_existing_format(data)
        
        print("\n" + "=" * 80)
        print("✅ API fetch successful!")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


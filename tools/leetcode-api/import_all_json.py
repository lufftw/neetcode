#!/usr/bin/env python3
"""
Import LeetScrape all.json into SQLite database.

This script reads the all.json file from LeetScrape and imports
all questions into the local SQLite cache.

Data source:
    https://raw.githubusercontent.com/nikhil-ravi/LeetScrape/refs/heads/main/example/data/all.json

Usage:
    python tools/leetcode-api/import_all_json.py
    python tools/leetcode-api/import_all_json.py --json-path path/to/all.json
    python tools/leetcode-api/import_all_json.py --dry-run
"""

import json
import argparse
import sys
from pathlib import Path
from typing import Dict, Any, List

from question_store import QuestionStore, get_default_store

# Default path to all.json
DEFAULT_JSON_PATH = Path(__file__).parent / "data" / "all.json"


def convert_leetscrape_json(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a single LeetScrape JSON item to storage format.
    
    LeetScrape JSON format:
    {
        "QID": 1,
        "title": "Two Sum",
        "titleSlug": "two-sum",
        "difficulty": "Easy",
        "acceptanceRate": 50.15,
        "paidOnly": false,
        "topicTags": "array,hash-table",
        "categorySlug": "algorithms",
        "Hints": ["hint1", "hint2"],
        "Companies": null,
        "SimilarQuestions": [15, 18, 167],
        "Code": "class Solution:...",
        "Body": "<p>Given an array...",
        "isPaidOnly": false
    }
    
    Args:
        item: Dictionary from all.json
        
    Returns:
        Dictionary suitable for QuestionStore.save()
    """
    return {
        'qid': int(item.get('QID', 0) or 0),
        'title': item.get('title', '') or '',
        'title_slug': item.get('titleSlug', '') or '',
        'difficulty': item.get('difficulty', '') or '',
        'acceptance_rate': float(item.get('acceptanceRate', 0.0) or 0.0),
        'paid_only': bool(item.get('paidOnly', False)),
        'topic_tags': item.get('topicTags', '') or '',
        'category_slug': item.get('categorySlug', '') or '',
        'hints': item.get('Hints', []) or [],
        'companies': item.get('Companies'),  # Can be None
        'similar_questions': item.get('SimilarQuestions', []) or [],
        'code': item.get('Code', '') or '',
        'body': item.get('Body', '') or '',
        'is_paid_only': bool(item.get('isPaidOnly', False)),
    }


def import_all_json(
    json_path: Path,
    store: QuestionStore,
    dry_run: bool = False,
    skip_paid: bool = False,
    skip_empty_body: bool = True,
) -> Dict[str, int]:
    """
    Import all questions from all.json into SQLite.
    
    Args:
        json_path: Path to all.json file
        store: QuestionStore instance
        dry_run: If True, don't actually save to database
        skip_paid: If True, skip paid-only questions
        skip_empty_body: If True, skip questions with empty Body
        
    Returns:
        Dictionary with import statistics
    """
    stats = {
        'total': 0,
        'imported': 0,
        'skipped_paid': 0,
        'skipped_empty': 0,
        'errors': 0,
    }
    
    # Read JSON file
    print(f"Reading: {json_path}")
    with open(json_path, 'r', encoding='utf-8') as f:
        data: List[Dict[str, Any]] = json.load(f)
    
    stats['total'] = len(data)
    print(f"Found {stats['total']} questions")
    
    # Import each question
    for i, item in enumerate(data, 1):
        qid = item.get('QID', '?')
        title = item.get('title', 'Unknown')
        slug = item.get('titleSlug', '')
        
        # Skip paid-only if requested
        if skip_paid and (item.get('paidOnly') or item.get('isPaidOnly')):
            stats['skipped_paid'] += 1
            continue
        
        # Skip empty body if requested
        if skip_empty_body and not item.get('Body'):
            stats['skipped_empty'] += 1
            continue
        
        try:
            # Convert to storage format
            storage_data = convert_leetscrape_json(item)
            
            if not dry_run:
                store.save(storage_data)
            
            stats['imported'] += 1
            
            # Progress indicator
            if i % 100 == 0 or i == stats['total']:
                print(f"  Progress: {i}/{stats['total']} ({i*100//stats['total']}%)")
                
        except Exception as e:
            stats['errors'] += 1
            print(f"  Error importing [{qid}] {title}: {e}")
    
    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Import LeetScrape all.json into SQLite database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "--json-path", 
        type=Path, 
        default=DEFAULT_JSON_PATH,
        help=f"Path to all.json file (default: {DEFAULT_JSON_PATH})"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true",
        help="Parse JSON but don't save to database"
    )
    parser.add_argument(
        "--include-paid", 
        action="store_true",
        help="Include paid-only questions (skipped by default)"
    )
    parser.add_argument(
        "--include-empty", 
        action="store_true",
        help="Include questions with empty Body (skipped by default)"
    )
    
    args = parser.parse_args()
    
    # Check if JSON file exists
    if not args.json_path.exists():
        print(f"Error: JSON file not found: {args.json_path}")
        print("\nDownload from:")
        print("  https://raw.githubusercontent.com/nikhil-ravi/LeetScrape/refs/heads/main/example/data/all.json")
        return 1
    
    # Get store
    store = get_default_store()
    print(f"Database: {store.db_path}")
    print(f"Existing questions: {store.count()}")
    
    if args.dry_run:
        print("\n[DRY RUN - No changes will be made]\n")
    
    # Import
    stats = import_all_json(
        json_path=args.json_path,
        store=store,
        dry_run=args.dry_run,
        skip_paid=not args.include_paid,
        skip_empty_body=not args.include_empty,
    )
    
    # Print summary
    print("\n" + "=" * 50)
    print("Import Summary")
    print("=" * 50)
    print(f"  Total in JSON:    {stats['total']}")
    print(f"  Imported:         {stats['imported']}")
    print(f"  Skipped (paid):   {stats['skipped_paid']}")
    print(f"  Skipped (empty):  {stats['skipped_empty']}")
    print(f"  Errors:           {stats['errors']}")
    print("=" * 50)
    
    if not args.dry_run:
        print(f"\nDatabase now has: {store.count()} questions")
    
    return 0 if stats['errors'] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())


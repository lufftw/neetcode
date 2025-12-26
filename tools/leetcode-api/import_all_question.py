#!/usr/bin/env python3
"""
Import LeetCode questions from LeetScrape data files into SQLite database.

This script reads data from multiple LeetScrape files and combines them
to build complete question objects:

Data Sources:
    - all.json: Complete question data (primary source)
    - questions.csv: Basic question metadata (fallback)
    - questionBody.pickle: Question body/problem statement
    - questionTopics.csv: QID to topic tag mapping
    - topicTags.csv: Topic tag details
    - companies.csv: Company information

Question Object Structure:
    - QID: Question ID
    - title: Question title
    - titleSlug: Question title slug
    - difficulty: Question difficulty
    - Hints: Question hints
    - Companies: Question companies
    - topics: Question topic tags
    - SimilarQuestions: Similar question IDs
    - Code: Code stubs
    - Body: Question body / problem statement
    - isPaidOnly: Whether the question is only available to premium users

Usage:
    python tools/leetcode-api/import_all_question.py
    python tools/leetcode-api/import_all_question.py --source json
    python tools/leetcode-api/import_all_question.py --source csv
    python tools/leetcode-api/import_all_question.py --dry-run
"""

import json
import csv
import pickle
import argparse
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

from question_store import QuestionStore, get_default_store

# Data directory
DATA_DIR = Path(__file__).parent / "data"


class QuestionDataLoader:
    """Load and combine question data from multiple LeetScrape files."""
    
    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = data_dir
        self._questions_csv: Optional[Dict[int, Dict]] = None
        self._topics_by_qid: Optional[Dict[int, List[str]]] = None
        self._topic_names: Optional[Dict[str, str]] = None
        self._question_bodies: Optional[Dict[int, str]] = None
    
    def _load_questions_csv(self) -> Dict[int, Dict]:
        """Load questions.csv into a dict keyed by QID."""
        if self._questions_csv is not None:
            return self._questions_csv
        
        self._questions_csv = {}
        csv_path = self.data_dir / "questions.csv"
        if not csv_path.exists():
            return self._questions_csv
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                qid = int(row.get('QID', 0))
                self._questions_csv[qid] = row
        
        return self._questions_csv
    
    def _load_topics_by_qid(self) -> Dict[int, List[str]]:
        """Load questionTopics.csv - mapping QID to topic slugs."""
        if self._topics_by_qid is not None:
            return self._topics_by_qid
        
        self._topics_by_qid = {}
        csv_path = self.data_dir / "questionTopics.csv"
        if not csv_path.exists():
            return self._topics_by_qid
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                qid = int(row.get('QID', 0))
                tag_slug = row.get('tagSlug', '')
                if qid not in self._topics_by_qid:
                    self._topics_by_qid[qid] = []
                if tag_slug:
                    self._topics_by_qid[qid].append(tag_slug)
        
        return self._topics_by_qid
    
    def _load_topic_names(self) -> Dict[str, str]:
        """Load topicTags.csv - mapping slug to display name."""
        if self._topic_names is not None:
            return self._topic_names
        
        self._topic_names = {}
        csv_path = self.data_dir / "topicTags.csv"
        if not csv_path.exists():
            return self._topic_names
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                slug = row.get('slug', '')
                name = row.get('name', '')
                if slug:
                    self._topic_names[slug] = name
        
        return self._topic_names
    
    def _load_question_bodies(self) -> Dict[int, str]:
        """Load questionBody.pickle - QID to HTML body mapping."""
        if self._question_bodies is not None:
            return self._question_bodies
        
        self._question_bodies = {}
        pickle_path = self.data_dir / "questionBody.pickle"
        if not pickle_path.exists():
            return self._question_bodies
        
        try:
            with open(pickle_path, 'rb') as f:
                data = pickle.load(f)
                # Assuming it's a dict with slug or QID as keys
                if isinstance(data, dict):
                    self._question_bodies = data
        except Exception:
            pass
        
        return self._question_bodies
    
    def load_from_json(self) -> List[Dict[str, Any]]:
        """
        Load questions from all.json (primary source).
        
        Returns:
            List of question dictionaries in storage format
        """
        json_path = self.data_dir / "all.json"
        if not json_path.exists():
            print(f"Warning: {json_path} not found")
            return []
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        questions = []
        for item in data:
            questions.append(self._convert_json_item(item))
        
        return questions
    
    def load_from_csv(self) -> List[Dict[str, Any]]:
        """
        Load questions by combining CSV and pickle files.
        
        This is a fallback when all.json is not available.
        Combines:
            - questions.csv (basic metadata)
            - questionTopics.csv (topic tags)
            - questionBody.pickle (problem statement)
        
        Returns:
            List of question dictionaries in storage format
        """
        questions_data = self._load_questions_csv()
        topics_by_qid = self._load_topics_by_qid()
        bodies = self._load_question_bodies()
        
        questions = []
        for qid, row in questions_data.items():
            # Get topic tags for this question
            topic_slugs = topics_by_qid.get(qid, [])
            topic_tags = ','.join(topic_slugs) if topic_slugs else row.get('topicTags', '')
            
            # Get body from pickle if available
            body = bodies.get(qid, '') or bodies.get(row.get('titleSlug', ''), '')
            
            questions.append({
                'qid': qid,
                'title': row.get('title', ''),
                'title_slug': row.get('titleSlug', ''),
                'difficulty': row.get('difficulty', ''),
                'acceptance_rate': float(row.get('acceptanceRate', 0) or 0),
                'paid_only': row.get('paidOnly', '').lower() == 'true',
                'topic_tags': topic_tags,
                'category_slug': row.get('categorySlug', ''),
                'hints': [],  # Not available in CSV
                'companies': None,  # Not available in CSV
                'similar_questions': [],  # Not available in CSV
                'code': '',  # Not available in CSV
                'body': body,
                'is_paid_only': row.get('paidOnly', '').lower() == 'true',
            })
        
        return questions
    
    def _convert_json_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert a single all.json item to storage format.
        
        Maps LeetScrape JSON format to our storage schema:
            QID -> qid
            title -> title
            titleSlug -> title_slug
            difficulty -> difficulty
            acceptanceRate -> acceptance_rate
            paidOnly -> paid_only
            topicTags -> topic_tags
            categorySlug -> category_slug
            Hints -> hints
            Companies -> companies
            SimilarQuestions -> similar_questions
            Code -> code
            Body -> body
            isPaidOnly -> is_paid_only
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


def import_questions(
    questions: List[Dict[str, Any]],
    store: QuestionStore,
    dry_run: bool = False,
    skip_paid: bool = False,
    skip_empty_body: bool = True,
) -> Dict[str, int]:
    """
    Import questions into SQLite.
    
    Args:
        questions: List of question dictionaries
        store: QuestionStore instance
        dry_run: If True, don't actually save to database
        skip_paid: If True, skip paid-only questions
        skip_empty_body: If True, skip questions with empty body
        
    Returns:
        Dictionary with import statistics
    """
    stats = {
        'total': len(questions),
        'imported': 0,
        'skipped_paid': 0,
        'skipped_empty': 0,
        'errors': 0,
    }
    
    for i, q in enumerate(questions, 1):
        qid = q.get('qid', '?')
        title = q.get('title', 'Unknown')
        
        # Skip paid-only if requested
        if skip_paid and (q.get('paid_only') or q.get('is_paid_only')):
            stats['skipped_paid'] += 1
            continue
        
        # Skip empty body if requested
        if skip_empty_body and not q.get('body'):
            stats['skipped_empty'] += 1
            continue
        
        try:
            if not dry_run:
                store.save(q)
            
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
        description="Import LeetCode questions into SQLite database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "--source",
        choices=['json', 'csv', 'auto'],
        default='auto',
        help="Data source: 'json' (all.json), 'csv' (combine CSVs), 'auto' (json first, fallback to csv)"
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DATA_DIR,
        help=f"Path to data directory (default: {DATA_DIR})"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse data but don't save to database"
    )
    parser.add_argument(
        "--include-paid",
        action="store_true",
        help="Include paid-only questions (skipped by default)"
    )
    parser.add_argument(
        "--include-empty",
        action="store_true",
        help="Include questions with empty body (skipped by default)"
    )
    
    args = parser.parse_args()
    
    # Initialize loader
    loader = QuestionDataLoader(args.data_dir)
    
    # Load questions based on source
    print(f"Data directory: {args.data_dir}")
    
    questions = []
    if args.source == 'json' or args.source == 'auto':
        json_path = args.data_dir / "all.json"
        if json_path.exists():
            print(f"Loading from: all.json")
            questions = loader.load_from_json()
        elif args.source == 'json':
            print(f"Error: all.json not found in {args.data_dir}")
            return 1
    
    if not questions and (args.source == 'csv' or args.source == 'auto'):
        print(f"Loading from: CSV files")
        questions = loader.load_from_csv()
    
    if not questions:
        print("Error: No questions loaded")
        return 1
    
    print(f"Loaded {len(questions)} questions")
    
    # Get store
    store = get_default_store()
    print(f"Database: {store.db_path}")
    print(f"Existing questions: {store.count()}")
    
    if args.dry_run:
        print("\n[DRY RUN - No changes will be made]\n")
    
    # Import
    stats = import_questions(
        questions=questions,
        store=store,
        dry_run=args.dry_run,
        skip_paid=not args.include_paid,
        skip_empty_body=not args.include_empty,
    )
    
    # Print summary
    print("\n" + "=" * 50)
    print("Import Summary")
    print("=" * 50)
    print(f"  Total loaded:     {stats['total']}")
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


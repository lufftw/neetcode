#!/usr/bin/env python3
"""
Test script to verify leetscrape can fetch description and constraints
"""

import sys

def test_leetscrape():
    """Test if leetscrape can fetch problem description and constraints."""
    try:
        from leetscrape import GetQuestion
        print("[OK] leetscrape imported successfully")
    except ImportError as e:
        print(f"[ERROR] Failed to import leetscrape: {e}")
        print("\nPlease install leetscrape: pip install leetscrape")
        return False

    # Test with a simple problem (two-sum)
    test_slug = "two-sum"
    print(f"\nTesting with problem slug: {test_slug}")
    print("=" * 60)
    
    try:
        q = GetQuestion(titleSlug=test_slug)
        print("[OK] GetQuestion object created")
        
        q.scrape()
        print("[OK] Scraping completed")
        
        # Check question_content
        print("\n--- Description (question_content) ---")
        if hasattr(q, 'question_content'):
            content = q.question_content
            if content:
                print(f"Type: {type(content)}")
                print(f"Length: {len(content)} characters")
                print(f"\nFirst 200 characters:")
                print(content[:200])
                print("\nFirst 5 lines:")
                lines = content.split("\n")
                for i, line in enumerate(lines[:5], 1):
                    print(f"{i}: {repr(line)}")
            else:
                print("question_content is empty or None")
        else:
            print("question_content attribute not found")
            print(f"Available attributes: {[attr for attr in dir(q) if not attr.startswith('_')]}")
        
        # Check constraints
        print("\n--- Constraints ---")
        if hasattr(q, 'constraints'):
            constraints = q.constraints
            if constraints:
                print(f"Type: {type(constraints)}")
                print(f"Count: {len(constraints)}")
                print("\nConstraints:")
                for i, c in enumerate(constraints, 1):
                    print(f"{i}: {repr(c)}")
            else:
                print("constraints is empty or None")
        else:
            print("constraints attribute not found")
            print(f"Available attributes: {[attr for attr in dir(q) if not attr.startswith('_')]}")
        
        # Show all available attributes
        print("\n--- All Available Attributes ---")
        attrs = [attr for attr in dir(q) if not attr.startswith('_')]
        for attr in attrs:
            try:
                value = getattr(q, attr)
                if not callable(value):
                    print(f"{attr}: {type(value).__name__}")
            except:
                pass
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Error during scraping: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_leetscrape()
    sys.exit(0 if success else 1)


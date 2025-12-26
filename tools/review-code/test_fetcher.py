#!/usr/bin/env python3
"""
Test script for leetscrape_fetcher module
"""

import sys

def test_fetcher():
    """Test the get_description_and_constraints function."""
    try:
        from leetscrape import GetQuestion
    except ImportError as e:
        print(f"[ERROR] Failed to import leetscrape: {e}")
        return False
    
    # Test with a simple problem
    test_slug = "two-sum"
    print(f"Testing with problem slug: {test_slug}")
    print("=" * 60)
    
    try:
        # First, let's see what attributes are available
        q = GetQuestion(titleSlug=test_slug)
        q.scrape()
        
        print("\n--- Available Attributes ---")
        attrs = [attr for attr in dir(q) if not attr.startswith('_')]
        for attr in attrs:
            try:
                value = getattr(q, attr)
                if not callable(value):
                    if isinstance(value, str) and len(value) > 100:
                        print(f"{attr}: {type(value).__name__} (length: {len(value)})")
                        print(f"  Preview: {value[:100]}...")
                    elif isinstance(value, (list, dict)) and len(str(value)) > 100:
                        print(f"{attr}: {type(value).__name__} (length: {len(value) if hasattr(value, '__len__') else 'N/A'})")
                        if isinstance(value, list) and value:
                            print(f"  First item: {value[0]}")
                    else:
                        print(f"{attr}: {repr(value)}")
            except Exception:
                print(f"{attr}: (error accessing)")
        
        # Check Body attribute
        print("\n--- Body Attribute ---")
        if hasattr(q, 'Body'):
            body = q.Body
            print(f"Type: {type(body)}")
            print(f"Length: {len(body) if body else 0} characters")
            if body:
                print(f"\nFirst 500 characters:")
                print(body[:500])
                print(f"\nLast 200 characters:")
                print(body[-200:])
        else:
            print("Body attribute not found!")
        
        # Check Constraints attribute
        print("\n--- Constraints Attribute ---")
        if hasattr(q, 'Constraints'):
            constraints = q.Constraints
            print(f"Type: {type(constraints)}")
            if constraints:
                if isinstance(constraints, list):
                    print(f"Length: {len(constraints)} items")
                    for i, c in enumerate(constraints[:5], 1):
                        print(f"  {i}: {repr(c)}")
                else:
                    print(f"Value: {repr(constraints)}")
            else:
                print("Constraints is empty/None")
        else:
            print("Constraints attribute not found!")
        
        # Now test our function
        print("\n" + "=" * 60)
        print("Testing get_description_and_constraints function:")
        print("=" * 60)
        
        from leetscrape_fetcher import get_description_and_constraints
        desc_lines, const_lines = get_description_and_constraints(test_slug)
        
        print(f"\n--- Description ({len(desc_lines)} lines) ---")
        if desc_lines:
            for i, line in enumerate(desc_lines[:30], 1):  # Show first 30 lines
                print(f"{i:2d}: {line}")
            if len(desc_lines) > 30:
                print(f"... ({len(desc_lines) - 30} more lines)")
        else:
            print("(empty)")
        
        print(f"\n--- Constraints ({len(const_lines)} items) ---")
        if const_lines:
            for i, constraint in enumerate(const_lines, 1):
                print(f"{i}: {constraint}")
        else:
            print("(empty)")
        
        return True
    except Exception as e:
        print(f"\n[ERROR] Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_fetcher()
    sys.exit(0 if success else 1)


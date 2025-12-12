#!/usr/bin/env python3
"""
Standalone script to run solution format tests.

Usage:
    python tools/run_format_tests.py
    python tools/run_format_tests.py --verbose
    python tools/run_format_tests.py --quiet
"""
import sys
import unittest
from pathlib import Path

# Add tools directory to path
TOOLS_DIR = Path(__file__).parent
sys.path.insert(0, str(TOOLS_DIR))

from tests.test_solution_format import TestSolutionFormat


def main():
    """Run format tests."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSolutionFormat)
    
    # Parse arguments
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    quiet = '--quiet' in sys.argv or '-q' in sys.argv
    
    if quiet:
        verbosity = 0
    elif verbose:
        verbosity = 2
    else:
        verbosity = 1
    
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main())


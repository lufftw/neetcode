"""Test import of leetcode_datasource package."""

try:
    from leetcode_datasource import LeetCodeDataSource
    print('✅ Import successful!')
except ImportError as e:
    print(f'❌ Import failed: {e}')
    print('   Make sure you have run: pip install -e .')


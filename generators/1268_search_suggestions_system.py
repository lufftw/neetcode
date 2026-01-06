# generators/1268_search_suggestions_system.py
"""
Test Case Generator for Problem 1268 - Search Suggestions System

LeetCode Constraints:
- 1 <= products.length <= 1000
- 1 <= products[i].length <= 3000
- 1 <= sum(products[i].length) <= 2 * 10^4
- All the strings of products are unique.
- products[i] consists of lowercase English letters.
- 1 <= searchWord.length <= 1000
- searchWord consists of lowercase English letters.
"""
import json
import random
import string
from typing import Iterator, Optional, List


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate test case inputs for Search Suggestions System.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility

    Yields:
        str: Products and searchWord in format
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # Example 1
        (["mobile", "mouse", "moneypot", "monitor", "mousepad"], "mouse"),
        # Example 2
        (["havana"], "havana"),
        # No matches
        (["apple", "apricot", "application"], "banana"),
        # Single character products
        (["a", "b", "c", "d"], "ab"),
        # Long common prefix
        (["phone", "phonecase", "phonebook", "phones"], "phone"),
        # Gradual narrowing
        (["abc", "abd", "abe", "abf", "xyz"], "abc"),
    ]

    for products, searchWord in edge_cases:
        yield _format_case(products, searchWord)
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _format_case(products: List[str], searchWord: str) -> str:
    """Format a test case as input string."""
    return f"{json.dumps(products, separators=(',', ':'))}\n{searchWord}"


def _generate_random_case() -> str:
    """Generate a single random test case."""
    num_products = random.randint(3, 20)

    # Generate products with some common prefixes
    products = set()
    base_prefixes = [_random_word(random.randint(1, 4)) for _ in range(3)]

    for _ in range(num_products):
        if random.random() < 0.6:
            # Build on common prefix
            prefix = random.choice(base_prefixes)
            suffix = _random_word(random.randint(0, 8))
            products.add(prefix + suffix)
        else:
            # Random product
            products.add(_random_word(random.randint(2, 12)))

    products = list(products)

    # Generate search word - sometimes from products, sometimes random
    if products and random.random() < 0.7:
        base = random.choice(products)
        # Use prefix of a product
        search_len = random.randint(1, len(base))
        searchWord = base[:search_len]
    else:
        searchWord = _random_word(random.randint(2, 8))

    return _format_case(products, searchWord)


def _random_word(length: int) -> str:
    """Generate a random lowercase word."""
    if length == 0:
        return ""
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    Args:
        n: Target number of products

    Returns:
        str: Test case with approximately n products
    """
    num_products = max(3, n)

    products = set()
    prefixes = [_random_word(2) for _ in range(5)]

    while len(products) < num_products:
        if random.random() < 0.5:
            prefix = random.choice(prefixes)
            products.add(prefix + _random_word(random.randint(1, 10)))
        else:
            products.add(_random_word(random.randint(3, 12)))

    products = list(products)[:num_products]

    # Search word based on common prefix
    searchWord = random.choice(prefixes) + _random_word(random.randint(1, 5))

    return _format_case(products, searchWord)

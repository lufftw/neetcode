# generators/0721_accounts_merge.py
"""
Test Case Generator for Problem 0721 - Accounts Merge

LeetCode Constraints:
- 1 <= accounts.length <= 1000
- 2 <= accounts[i].length <= 10
- 1 <= accounts[i][j].length <= 30
"""
import json
import random
import string
from typing import Iterator, Optional


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """Generate test case inputs for Accounts Merge."""
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        [["John", "johnsmith@mail.com", "john_newyork@mail.com"],
         ["John", "johnsmith@mail.com", "john00@mail.com"],
         ["Mary", "mary@mail.com"],
         ["John", "johnnybravo@mail.com"]],
        [["John", "a@mail.com"], ["John", "b@mail.com"]],  # Same name, different accounts
        [["John", "a@mail.com", "b@mail.com"], ["John", "b@mail.com", "c@mail.com"]],  # Chain merge
    ]

    for accounts in edge_cases:
        yield json.dumps(accounts, separators=(',', ':'))
        count -= 1
        if count <= 0:
            return

    for _ in range(count):
        yield _generate_case()


def _random_email() -> str:
    """Generate a random email."""
    name = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 8)))
    domain = random.choice(['mail.com', 'gmail.com', 'test.com'])
    return f"{name}@{domain}"


def _generate_case() -> str:
    """Generate a single random test case."""
    num_accounts = random.randint(2, 20)
    names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank']

    # Generate some shared emails
    shared_emails = [_random_email() for _ in range(random.randint(1, 5))]

    accounts = []
    for _ in range(num_accounts):
        name = random.choice(names)
        num_emails = random.randint(1, 5)
        emails = [_random_email() for _ in range(num_emails)]
        # Maybe add a shared email
        if random.random() < 0.3 and shared_emails:
            emails.append(random.choice(shared_emails))
        accounts.append([name] + list(set(emails)))

    return json.dumps(accounts, separators=(',', ':'))


def generate_for_complexity(n: int) -> str:
    """Generate test case with specific input size."""
    return _generate_case()


if __name__ == "__main__":
    for i, case in enumerate(generate(3)):
        print(f"Case {i + 1}: {case[:80]}...")

# generators/0355_design_twitter.py
"""
Test Case Generator for Problem 0355 - Design Twitter

LeetCode Constraints:
- 1 <= userId, followerId, followeeId <= 500
- 0 <= tweetId <= 10^4
- All tweets have unique IDs
- At most 3 * 10^4 calls total
"""
import json
import random
from typing import Iterator, Optional, List, Set


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test case inputs for Design Twitter.

    Args:
        count: Number of test cases to generate
        seed: Random seed for reproducibility (optional)

    Yields:
        str: Test input (operations and arguments as JSON)
    """
    if seed is not None:
        random.seed(seed)

    # Edge cases first
    edge_cases = [
        # LeetCode Example (modified with user 2 posting)
        (
            ["Twitter", "postTweet", "getNewsFeed", "follow", "postTweet", "getNewsFeed", "unfollow", "getNewsFeed"],
            [[], [1, 5], [1], [1, 2], [2, 6], [1], [1, 2], [1]],
        ),
        # Multiple tweets from same user
        (
            ["Twitter", "postTweet", "postTweet", "postTweet", "getNewsFeed"],
            [[], [1, 1], [1, 2], [1, 3], [1]],
        ),
        # Self-follow attempt (should be no-op)
        (
            ["Twitter", "postTweet", "follow", "getNewsFeed"],
            [[], [1, 5], [1, 1], [1]],
        ),
        # Unfollow without following first
        (
            ["Twitter", "unfollow", "postTweet", "getNewsFeed"],
            [[], [1, 2], [1, 5], [1]],
        ),
        # Empty news feed
        (
            ["Twitter", "getNewsFeed"],
            [[], [1]],
        ),
    ]

    for ops, args in edge_cases:
        yield f"{json.dumps(ops, separators=(',', ':'))}\n{json.dumps(args, separators=(',', ':'))}"
        count -= 1
        if count <= 0:
            return

    # Random cases
    for _ in range(count):
        yield _generate_random_case()


def _generate_random_case() -> str:
    """Generate a random sequence of Twitter operations."""
    num_ops = random.randint(10, 50)
    num_users = random.randint(2, 10)

    operations = ["Twitter"]
    args = [[]]

    tweet_id = 0
    used_tweet_ids: Set[int] = set()

    for _ in range(num_ops):
        op_type = random.choices(
            ["postTweet", "getNewsFeed", "follow", "unfollow"],
            weights=[4, 3, 2, 1],  # Favor post and getNewsFeed
            k=1,
        )[0]

        if op_type == "postTweet":
            user_id = random.randint(1, num_users)
            while tweet_id in used_tweet_ids:
                tweet_id += 1
            used_tweet_ids.add(tweet_id)
            operations.append("postTweet")
            args.append([user_id, tweet_id])
            tweet_id += 1

        elif op_type == "getNewsFeed":
            user_id = random.randint(1, num_users)
            operations.append("getNewsFeed")
            args.append([user_id])

        elif op_type == "follow":
            follower_id = random.randint(1, num_users)
            followee_id = random.randint(1, num_users)
            operations.append("follow")
            args.append([follower_id, followee_id])

        elif op_type == "unfollow":
            follower_id = random.randint(1, num_users)
            followee_id = random.randint(1, num_users)
            operations.append("unfollow")
            args.append([follower_id, followee_id])

    return f"{json.dumps(operations, separators=(',', ':'))}\n{json.dumps(args, separators=(',', ':'))}"


# ============================================
# Complexity Estimation
# ============================================
def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific input size for complexity estimation.

    For Design Twitter:
    - n is the total number of operations
    - getNewsFeed is O(k log k) where k = followees

    Args:
        n: Number of operations (will be clamped to [2, 30000])

    Returns:
        str: Test input
    """
    # Clamp to LeetCode constraints
    n = max(2, min(n, 30000))

    num_users = min(100, n // 10)
    operations = ["Twitter"]
    args = [[]]

    tweet_id = 0

    # Create a scenario with many followees per user
    # First, make everyone follow user 1
    for user in range(2, num_users + 1):
        if len(operations) >= n:
            break
        operations.append("follow")
        args.append([user, 1])

    # Post many tweets from user 1
    while len(operations) < n - n // 4:
        operations.append("postTweet")
        args.append([1, tweet_id])
        tweet_id += 1

    # Query news feeds
    while len(operations) < n:
        user_id = random.randint(2, num_users) if num_users > 1 else 1
        operations.append("getNewsFeed")
        args.append([user_id])

    return f"{json.dumps(operations, separators=(',', ':'))}\n{json.dumps(args, separators=(',', ':'))}"


if __name__ == "__main__":
    print("Sample test cases:")
    for i, test in enumerate(generate(3, seed=42), 1):
        lines = test.split("\n")
        ops = json.loads(lines[0])
        print(f"Test {i}: {len(ops)} operations")
        print(f"  Sample ops: {ops[:5]}...")
        print()

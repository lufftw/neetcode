"""
Problem: Design Twitter
Link: https://leetcode.com/problems/design-twitter/

Design a simplified version of Twitter where users can post tweets, follow/unfollow
another user, and is able to see the 10 most recent tweets in the user's news feed.

Implement the Twitter class:
- Twitter() Initializes your twitter object.
- void postTweet(int userId, int tweetId) Composes a new tweet with ID tweetId by
  the user userId. Each call to this function will be made with a unique tweetId.
- List<Integer> getNewsFeed(int userId) Retrieves the 10 most recent tweet IDs in
  the user's news feed. Each item in the news feed must be posted by users who the
  user followed or by the user themself. Tweets must be ordered from most recent to
  least recent.
- void follow(int followerId, int followeeId) The user with ID followerId started
  following the user with ID followeeId.
- void unfollow(int followerId, int followeeId) The user with ID followerId started
  unfollowing the user with ID followeeId.

Example 1:
    Input:
        ["Twitter", "postTweet", "getNewsFeed", "follow", "getNewsFeed", "unfollow", "getNewsFeed"]
        [[], [1, 5], [1], [1, 2], [1], [1, 2], [1]]
    Output:
        [null, null, [5], null, [5, 6], null, [5]]
    Explanation:
        Twitter twitter = new Twitter();
        twitter.postTweet(1, 5);   // User 1 posts tweet 5
        twitter.getNewsFeed(1);    // Returns [5], user 1's own tweet
        twitter.follow(1, 2);      // User 1 follows user 2
        twitter.getNewsFeed(1);    // Returns [5, 6], includes user 2's tweet
        twitter.unfollow(1, 2);    // User 1 unfollows user 2
        twitter.getNewsFeed(1);    // Returns [5], only user 1's tweet

Constraints:
- 1 <= userId, followerId, followeeId <= 500
- 0 <= tweetId <= 10^4
- All the tweets have unique IDs.
- At most 3 * 10^4 calls will be made to postTweet, getNewsFeed, follow, unfollow.

Topics: Hash Table, Linked List, Design, Heap (Priority Queue)
"""

import json
import heapq
from typing import List, Dict, Set
from collections import defaultdict
from _runner import get_solver


# ============================================================================
# SOLUTIONS metadata
# ============================================================================
SOLUTIONS = {
    "default": {
        "class": "TwitterHeap",
        "method": "_run_operations",
        "complexity": "O(1) post/follow/unfollow, O(k log k) getNewsFeed where k = followees",
        "description": "Min-heap merge of k sorted tweet lists from followed users",
    },
    "simple": {
        "class": "TwitterSimple",
        "method": "_run_operations",
        "complexity": "O(1) post/follow/unfollow, O(n log n) getNewsFeed where n = total tweets",
        "description": "Simple sorting approach - collect all tweets then sort",
    },
}


# ============================================================================
# Solution 1: Heap-Based Merge (Optimal for getNewsFeed)
# Time: O(1) for post/follow/unfollow, O(k log k) for getNewsFeed
# Space: O(users + tweets + follows)
#
# Key Insight:
#   The news feed problem is essentially merging k sorted lists (each user's
#   tweets are naturally sorted by time). This is the classic "merge k sorted
#   lists" problem solvable with a min-heap.
#
# Algorithm:
#   - Store tweets per user as list of (timestamp, tweetId)
#   - Store followee sets per user
#   - For getNewsFeed: use heap to merge tweets from self + followees
#     - Initialize heap with most recent tweet from each relevant user
#     - Pop from heap, push next tweet from same user
#     - Continue until 10 tweets or heap empty
#
# Why Heap Over Sorting:
#   If user follows k people each with t tweets, sorting takes O(kt log kt).
#   Heap merge only examines tweets until we have 10, taking O(k log k) when
#   each user has many tweets but we only need 10.
# ============================================================================
class TwitterHeap:
    """
    Twitter implementation using min-heap for efficient news feed generation.

    The key insight is that news feed requires merging k sorted lists (each
    user's timeline). We use a max-heap (negated timestamps) to efficiently
    extract the 10 most recent tweets across all followed users.
    """

    def __init__(self):
        self.timestamp = 0  # Global timestamp for ordering tweets
        self.tweets: Dict[int, List[tuple]] = defaultdict(list)  # userId -> [(time, tweetId)]
        self.following: Dict[int, Set[int]] = defaultdict(set)  # userId -> set of followeeIds

    def postTweet(self, userId: int, tweetId: int) -> None:
        """O(1) - Append tweet to user's timeline."""
        self.tweets[userId].append((self.timestamp, tweetId))
        self.timestamp += 1

    def getNewsFeed(self, userId: int) -> List[int]:
        """
        O(k log k) where k = number of followees + 1.

        Merge k sorted lists using a max-heap. We only need the 10 most recent,
        so we stop early rather than merging everything.
        """
        result = []

        # Max-heap: (-timestamp, tweetId, userId, tweet_index)
        # We negate timestamp because Python has min-heap
        heap = []

        # Include self and all followees
        relevant_users = self.following[userId] | {userId}

        # Initialize heap with most recent tweet from each user
        for uid in relevant_users:
            if self.tweets[uid]:
                idx = len(self.tweets[uid]) - 1  # Most recent tweet index
                time, tweet_id = self.tweets[uid][idx]
                heapq.heappush(heap, (-time, tweet_id, uid, idx))

        # Extract up to 10 most recent tweets
        while heap and len(result) < 10:
            neg_time, tweet_id, uid, idx = heapq.heappop(heap)
            result.append(tweet_id)

            # Push next tweet from same user (if exists)
            if idx > 0:
                idx -= 1
                time, next_tweet_id = self.tweets[uid][idx]
                heapq.heappush(heap, (-time, next_tweet_id, uid, idx))

        return result

    def follow(self, followerId: int, followeeId: int) -> None:
        """O(1) - Add followee to follower's set."""
        if followerId != followeeId:  # Users shouldn't follow themselves
            self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        """O(1) - Remove followee from follower's set."""
        self.following[followerId].discard(followeeId)

    def _run_operations(self, operations: List[str], args: List[List]) -> List:
        """Execute a sequence of operations and return results."""
        results = []
        for op, arg in zip(operations, args):
            if op == "Twitter":
                results.append(None)
            elif op == "postTweet":
                self.postTweet(arg[0], arg[1])
                results.append(None)
            elif op == "getNewsFeed":
                results.append(self.getNewsFeed(arg[0]))
            elif op == "follow":
                self.follow(arg[0], arg[1])
                results.append(None)
            elif op == "unfollow":
                self.unfollow(arg[0], arg[1])
                results.append(None)
        return results


# ============================================================================
# Solution 2: Simple Sorting Approach
# Time: O(1) for post/follow/unfollow, O(n log n) for getNewsFeed
# Space: O(users + tweets + follows)
#
# Key Insight:
#   For simplicity, we can collect all relevant tweets and sort by timestamp.
#   This is less efficient than heap merge but easier to implement and
#   understand. Good for small datasets or when getNewsFeed is rare.
#
# Trade-off:
#   - Simpler implementation
#   - Worse worst-case complexity for getNewsFeed
#   - May be faster for very few followees due to lower constants
# ============================================================================
class TwitterSimple:
    """
    Twitter implementation using simple sorting for news feed.

    This approach collects all tweets from self and followees, sorts by
    timestamp, and returns the top 10. Simpler but less efficient than
    heap-based merge for users following many people.
    """

    def __init__(self):
        self.timestamp = 0
        self.tweets: Dict[int, List[tuple]] = defaultdict(list)
        self.following: Dict[int, Set[int]] = defaultdict(set)

    def postTweet(self, userId: int, tweetId: int) -> None:
        """O(1) - Append tweet to user's timeline."""
        self.tweets[userId].append((self.timestamp, tweetId))
        self.timestamp += 1

    def getNewsFeed(self, userId: int) -> List[int]:
        """
        O(n log n) where n = total tweets from self and followees.

        Collect all relevant tweets, sort by timestamp descending, return top 10.
        """
        all_tweets = []

        # Collect tweets from self and all followees
        relevant_users = self.following[userId] | {userId}
        for uid in relevant_users:
            all_tweets.extend(self.tweets[uid])

        # Sort by timestamp descending
        all_tweets.sort(key=lambda x: -x[0])

        # Return top 10 tweet IDs
        return [tweet_id for _, tweet_id in all_tweets[:10]]

    def follow(self, followerId: int, followeeId: int) -> None:
        """O(1) - Add followee to follower's set."""
        if followerId != followeeId:
            self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        """O(1) - Remove followee from follower's set."""
        self.following[followerId].discard(followeeId)

    def _run_operations(self, operations: List[str], args: List[List]) -> List:
        """Execute a sequence of operations and return results."""
        results = []
        for op, arg in zip(operations, args):
            if op == "Twitter":
                results.append(None)
            elif op == "postTweet":
                self.postTweet(arg[0], arg[1])
                results.append(None)
            elif op == "getNewsFeed":
                results.append(self.getNewsFeed(arg[0]))
            elif op == "follow":
                self.follow(arg[0], arg[1])
                results.append(None)
            elif op == "unfollow":
                self.unfollow(arg[0], arg[1])
                results.append(None)
        return results


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: operations as JSON array
        Line 2: arguments as JSON 2D array

    Example:
        ["Twitter","postTweet","getNewsFeed","follow","getNewsFeed","unfollow","getNewsFeed"]
        [[],[1,5],[1],[1,2],[1],[1,2],[1]]
    """
    import sys

    lines = sys.stdin.read().strip().split("\n")

    operations = json.loads(lines[0])
    args = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver._run_operations(operations, args)

    # Convert None to null for JSON output
    output = [None if r is None else r for r in result]
    print(json.dumps(output, separators=(",", ":")))


if __name__ == "__main__":
    solve()

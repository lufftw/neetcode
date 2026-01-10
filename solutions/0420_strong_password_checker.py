"""
Problem: Strong Password Checker
Link: https://leetcode.com/problems/strong-password-checker/

A password is considered strong if the below conditions are all met:
- It has at least 6 characters and at most 20 characters.
- It contains at least one lowercase letter, at least one uppercase letter, and at least one digit.
- It does not contain three repeating characters in a row (i.e., "Baaabb0" is weak, but "Baaba0" is strong).

Given a string password, return the minimum number of steps required to make password strong.
In one step, you can:
- Insert one character to password,
- Delete one character from password, or
- Replace one character of password with another character.

Constraints:
- 1 <= password.length <= 50
- password consists of letters, digits, dot '.' or exclamation mark '!'.

Topics: String, Greedy, Heap Priority Queue
"""
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "strongPasswordChecker",
        "complexity": "O(n) time, O(n) space",
        "description": "Greedy with optimal deletion strategy for repeat sequences",
    },
}


# ============================================================================
# JUDGE_FUNC - For generated tests without expected output
# Uses the same algorithm as reference to compute correct answer
# ============================================================================
def _reference_solution(password: str) -> int:
    """Reference implementation for validation."""
    n = len(password)

    # Count missing types
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    missing = 3 - (has_lower + has_upper + has_digit)

    # Find repeat sequences
    repeats = []
    i = 0
    while i < len(password):
        j = i
        while j < len(password) and password[j] == password[i]:
            j += 1
        if j - i >= 3:
            repeats.append(j - i)
        i = j

    if n < 6:
        return max(6 - n, missing)

    if n <= 20:
        return max(sum(r // 3 for r in repeats), missing)

    # n > 20
    deletions = n - 20
    replacements = sum(r // 3 for r in repeats)

    # Optimal deletion strategy
    remaining = deletions
    for i, r in enumerate(repeats):
        if remaining <= 0:
            break
        if r % 3 == 0 and r >= 3:
            repeats[i] -= 1
            replacements -= 1
            remaining -= 1

    for i, r in enumerate(repeats):
        if remaining <= 1:
            break
        if r % 3 == 1 and r >= 3:
            d = min(2, remaining, r - 2)
            if d == 2:
                repeats[i] -= 2
                replacements -= 1
                remaining -= 2

    for i, r in enumerate(repeats):
        if remaining <= 0:
            break
        if r >= 3:
            d = min(remaining, r - 2)
            replacements -= d // 3
            remaining -= d

    return deletions + max(replacements, missing)


def judge(actual, expected, input_data: str) -> bool:
    """
    Validate Strong Password Checker result.

    For this problem, there is exactly one correct answer.
    We compute the expected answer using a reference solution.
    """
    import json
    password = json.loads(input_data.strip())

    correct_answer = _reference_solution(password)

    if expected is not None:
        # Static test: verify against expected output
        return actual == expected
    else:
        # Generated test: verify against reference solution
        return actual == correct_answer


JUDGE_FUNC = judge


# ============================================================================
# Solution: Greedy with Case Analysis
# Time: O(n), Space: O(n) for storing repeat sequences
#   - Three length regimes require different strategies
#   - For n > 20: prioritize deletions from (3k) sequences first, then (3k+1), then (3k+2)
#   - Each replacement breaks one group of 3 consecutive repeats
# ============================================================================
class Solution:
    # Strong password requirements:
    #   1. Length in [6, 20]
    #   2. At least one lowercase, uppercase, digit
    #   3. No 3+ consecutive identical characters
    #
    # Operations: insert, delete, replace (each costs 1)
    #
    # Key insight: the relationship between operations and fixing repeats
    #   - For a run of length L, we need ceil(L/3) replacements to break it
    #   - Deletions can reduce replacements needed, but the efficiency varies:
    #     * L % 3 == 0: 1 delete saves 1 replacement
    #     * L % 3 == 1: 2 deletes save 1 replacement
    #     * L % 3 == 2: 3 deletes save 1 replacement

    def strongPasswordChecker(self, password: str) -> int:
        n = len(password)

        # Count missing character types
        missing_types = self._count_missing_types(password)

        # Find all consecutive repeat sequences of length >= 3
        # Store the length of each sequence
        repeats = self._find_repeat_sequences(password)

        # Case 1: Password too short (n < 6)
        if n < 6:
            return self._handle_short_password(n, missing_types, repeats)

        # Case 2: Password length in valid range [6, 20]
        if n <= 20:
            return self._handle_valid_length(missing_types, repeats)

        # Case 3: Password too long (n > 20)
        return self._handle_long_password(n, missing_types, repeats)

    def _count_missing_types(self, password: str) -> int:
        """Count how many character types are missing (lowercase, uppercase, digit)."""
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        return 3 - (has_lower + has_upper + has_digit)

    def _find_repeat_sequences(self, password: str) -> list:
        """
        Find all runs of 3+ consecutive identical characters.
        Returns list of run lengths.
        """
        repeats = []
        i = 0
        while i < len(password):
            j = i
            while j < len(password) and password[j] == password[i]:
                j += 1
            run_length = j - i
            if run_length >= 3:
                repeats.append(run_length)
            i = j
        return repeats

    def _handle_short_password(self, n: int, missing_types: int, repeats: list) -> int:
        """
        Handle n < 6: need to insert characters.

        Insight: Each insert can simultaneously:
        1. Increase length toward 6
        2. Add a missing character type
        3. Break a repeat sequence (insert in middle of 3+ repeats)

        We need max(6 - n, missing_types) operations at minimum.
        The repeat-breaking is handled implicitly since we have enough
        operations to break any sequence when adding to reach length 6.
        """
        chars_needed = 6 - n
        # Both insertions and the resulting length are enough to fix repeats
        # since max repeat length is 50 and we're going to length 6
        return max(chars_needed, missing_types)

    def _handle_valid_length(self, missing_types: int, repeats: list) -> int:
        """
        Handle 6 <= n <= 20: only need replacements.

        For each repeat sequence of length L, we need ceil(L/3) replacements.
        A replacement can also add a missing character type.
        """
        replacements_for_repeats = sum(length // 3 for length in repeats)
        # Replacements can fix missing types simultaneously
        return max(replacements_for_repeats, missing_types)

    def _handle_long_password(self, n: int, missing_types: int, repeats: list) -> int:
        """
        Handle n > 20: need deletions first, then possibly replacements.

        Strategy: Use deletions strategically to reduce replacement count.

        For a repeat of length L needing ceil(L/3) replacements:
        - If L % 3 == 0: 1 deletion reduces replacement count by 1 (most efficient)
        - If L % 3 == 1: 2 deletions reduce replacement count by 1
        - If L % 3 == 2: 3 deletions reduce replacement count by 1

        We prioritize deletions in order of efficiency: mod0 -> mod1 -> mod2
        """
        deletions_needed = n - 20
        total_deletions = deletions_needed

        # Calculate initial replacements needed for all repeats
        # Also categorize by (length % 3) for optimal deletion
        replacements = sum(length // 3 for length in repeats)

        # Phase 1: Use deletions on sequences where L % 3 == 0
        # Each single deletion from such a sequence saves 1 replacement
        remaining_deletions = deletions_needed
        for i, length in enumerate(repeats):
            if remaining_deletions <= 0:
                break
            if length % 3 == 0 and length >= 3:
                # Delete 1 character to reduce this sequence's replacement need by 1
                repeats[i] -= 1
                replacements -= 1
                remaining_deletions -= 1

        # Phase 2: Use deletions on sequences where L % 3 == 1
        # Need 2 deletions to save 1 replacement
        for i, length in enumerate(repeats):
            if remaining_deletions <= 1:
                break
            if length % 3 == 1 and length >= 3:
                # Delete 2 characters
                delete_count = min(2, remaining_deletions, length - 2)
                if delete_count == 2:
                    repeats[i] -= 2
                    replacements -= 1
                    remaining_deletions -= 2

        # Phase 3: Use remaining deletions on any sequence (3 deletions save 1 replacement)
        # This handles L % 3 == 2 and any remaining cases
        for i, length in enumerate(repeats):
            if remaining_deletions <= 0:
                break
            if length >= 3:
                # Delete up to (length - 2) characters, in groups of 3 for efficiency
                max_deletions = length - 2
                deletions_used = min(remaining_deletions, max_deletions)
                # Each 3 deletions saves 1 replacement
                saved_replacements = deletions_used // 3
                replacements -= saved_replacements
                remaining_deletions -= deletions_used

        # Total operations: deletions + max(remaining replacements, missing types)
        # Missing types are fixed by replacements (replacement with correct char type)
        return total_deletions + max(replacements, missing_types)


# ============================================================================
# solve() - stdin/stdout interface
# ============================================================================
def solve():
    """
    Input format:
        Line 1: password (JSON string with quotes)

    Example:
        "a"
        -> 5
    """
    import sys
    import json

    lines = sys.stdin.read().strip().split('\n')
    password = json.loads(lines[0])

    solver = get_solver(SOLUTIONS)
    result = solver.strongPasswordChecker(password)

    print(result)


if __name__ == "__main__":
    solve()

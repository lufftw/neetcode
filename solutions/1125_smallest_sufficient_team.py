# solutions/1125_smallest_sufficient_team.py
"""
Problem: Smallest Sufficient Team
Link: https://leetcode.com/problems/smallest-sufficient-team/

In a project, you have a list of required skills req_skills, and a list of people.
The ith person people[i] contains a list of skills that the person has.

Consider a sufficient team: a set of people such that for every required skill
in req_skills, there is at least one person in the team who has that skill.

Return any sufficient team of the smallest possible size, represented by the
index (0-indexed) of each person.

Example 1:
    Input: req_skills = ["java","nodejs","reactjs"],
           people = [["java"],["nodejs"],["nodejs","reactjs"]]
    Output: [0,2]

Example 2:
    Input: req_skills = ["algorithms","math","java","reactjs","csharp","aws"],
           people = [["algorithms","math","java"],["algorithms","math","reactjs"],
                     ["java","csharp","aws"],["reactjs","csharp"],
                     ["csharp","math"],["aws","java"]]
    Output: [1,2]

Constraints:
- 1 <= req_skills.length <= 16
- 1 <= req_skills[i].length <= 16
- req_skills[i] consists of lowercase English letters.
- All the strings of req_skills are unique.
- 1 <= people.length <= 60
- 0 <= people[i].length <= 16
- 1 <= people[i][j].length <= 16
- people[i][j] consists of lowercase English letters.
- All the strings of people[i] are unique.
- Every skill in people[i] is a skill in req_skills.
- It is guaranteed an answer exists.

Topics: Array, Dynamic Programming, Bit Manipulation, Bitmask
"""
from typing import List
from _runner import get_solver


SOLUTIONS = {
    "default": {
        "class": "Solution",
        "method": "smallestSufficientTeam",
        "complexity": "O(people × 2^skills) time, O(2^skills) space",
        "description": "Bitmask DP for set cover",
    },
}


# ============================================================================
# JUDGE_FUNC - Validate team covers all skills
# ============================================================================
def judge(actual, expected, input_data: str) -> bool:
    """Validate smallest sufficient team."""
    import json
    lines = input_data.strip().split('\n')
    req_skills = json.loads(lines[0])
    people = json.loads(lines[1])

    # Build skill index
    skill_to_idx = {s: i for i, s in enumerate(req_skills)}

    # Calculate team's skill coverage
    team_skills = 0
    for person_idx in actual:
        for skill in people[person_idx]:
            team_skills |= (1 << skill_to_idx[skill])

    # Check all skills are covered
    full_mask = (1 << len(req_skills)) - 1
    if team_skills != full_mask:
        return False

    # Check team size is minimal (at most as good as expected)
    if len(actual) > len(expected):
        return False

    return True


JUDGE_FUNC = judge


# ============================================================================
# Solution: Bitmask DP for Set Cover
# Time: O(people × 2^skills) - for each person, iterate all masks
# Space: O(2^skills) - store team for each skill mask
#
# Key Insight:
#   - dp[mask] = smallest team to cover skills represented by mask
#   - For each person, update all reachable masks
#   - This is the classic set cover problem with bitmask optimization
# ============================================================================
class Solution:
    def smallestSufficientTeam(self, req_skills: List[str],
                                people: List[List[str]]) -> List[int]:
        """
        Find minimum team to cover all required skills using bitmask DP.

        State: dp[skill_mask] = list of person indices forming smallest team
               to achieve exactly those skills

        Transition: For each person, if adding them gives a smaller team
                   for the new skill mask, update it.

        Time: O(people × 2^skills)
        Space: O(2^skills) for storing teams
        """
        m = len(req_skills)
        n = len(people)

        # Map skills to indices
        skill_to_idx = {skill: i for i, skill in enumerate(req_skills)}

        # Encode each person's skills as bitmask
        person_masks = []
        for skills in people:
            mask = 0
            for skill in skills:
                mask |= (1 << skill_to_idx[skill])
            person_masks.append(mask)

        # Target: all skills covered
        full_mask = (1 << m) - 1

        # dp[mask] = smallest team achieving skill mask
        # Start with empty team having no skills
        dp = {0: []}

        # Process each person
        for person_idx in range(n):
            person_mask = person_masks[person_idx]

            # Skip people with no skills
            if person_mask == 0:
                continue

            # Iterate over copy of current states
            # (to avoid modifying dict during iteration)
            for current_mask, team in list(dp.items()):
                # New skill mask after adding this person
                new_mask = current_mask | person_mask

                # Only update if this gives a strictly smaller team
                if new_mask not in dp or len(dp[new_mask]) > len(team) + 1:
                    dp[new_mask] = team + [person_idx]

        return dp[full_mask]


def solve():
    """
    Input format:
    Line 1: req_skills (JSON array)
    Line 2: people (JSON array of arrays)

    Example:
    ["java","nodejs","reactjs"]
    [["java"],["nodejs"],["nodejs","reactjs"]]
    """
    import sys
    import json
    lines = sys.stdin.read().strip().split('\n')

    req_skills = json.loads(lines[0])
    people = json.loads(lines[1])

    solver = get_solver(SOLUTIONS)
    result = solver.smallestSufficientTeam(req_skills, people)

    print(json.dumps(result, separators=(',', ':')))


if __name__ == "__main__":
    solve()

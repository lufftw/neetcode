# generators/1125_smallest_sufficient_team.py
"""
Random test generator for LC 1125: Smallest Sufficient Team

Constraints:
- 1 <= req_skills.length <= 16
- 1 <= req_skills[i].length <= 16
- All strings in req_skills are unique
- 1 <= people.length <= 60
- 0 <= people[i].length <= 16
- Every skill in people[i] is a skill in req_skills
- It is guaranteed an answer exists
"""
import random
import json
import string
from typing import Iterator, Optional


def generate_skill_name(length: int = None) -> str:
    """Generate a random skill name."""
    if length is None:
        length = random.randint(3, 8)
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def generate(count: int = 10, seed: Optional[int] = None) -> Iterator[str]:
    """
    Generate random test cases for Smallest Sufficient Team.

    Yields test input strings in the format:
        ["skill1", "skill2", ...]
        [["skill1"], ["skill2", "skill3"], ...]

    Ensures an answer exists by having at least one person per skill.
    """
    if seed is not None:
        random.seed(seed)

    for _ in range(count):
        # Random number of skills (1 to 10 for reasonable test times)
        num_skills = random.randint(2, 8)

        # Generate unique skill names
        req_skills = []
        used_names = set()
        while len(req_skills) < num_skills:
            name = generate_skill_name()
            if name not in used_names:
                used_names.add(name)
                req_skills.append(name)

        # Random number of people (num_skills to 30)
        num_people = random.randint(num_skills, min(30, num_skills * 3))

        # Ensure every skill is covered by at least one person
        # Strategy: first num_skills people each have at least one unique skill
        people = []

        # Ensure coverage: assign each skill to at least one person
        skill_assignments = list(range(num_skills))
        random.shuffle(skill_assignments)

        for i in range(num_people):
            person_skills = []

            if i < num_skills:
                # This person must have skill i (ensuring coverage)
                person_skills.append(req_skills[skill_assignments[i]])

            # Add random additional skills
            num_extra = random.randint(0, min(3, num_skills - 1))
            for _ in range(num_extra):
                skill = random.choice(req_skills)
                if skill not in person_skills:
                    person_skills.append(skill)

            people.append(person_skills)

        yield f"{json.dumps(req_skills, separators=(',', ':'))}\n{json.dumps(people, separators=(',', ':'))}"


def generate_for_complexity(n: int) -> str:
    """
    Generate test case with specific number of skills for complexity estimation.

    Args:
        n: Number of skills

    Returns:
        Test input string
    """
    # Cap at 16 per constraints
    n = min(n, 16)

    # Generate skills
    req_skills = [f"skill{i}" for i in range(n)]

    # Generate people (about 2x skills)
    num_people = n * 2

    people = []

    # First n people each have one skill (ensures coverage)
    for i in range(n):
        people.append([req_skills[i]])

    # Add more people with random skills
    for i in range(n, num_people):
        num_skills_person = random.randint(1, min(4, n))
        person_skills = random.sample(req_skills, num_skills_person)
        people.append(person_skills)

    return f"{json.dumps(req_skills, separators=(',', ':'))}\n{json.dumps(people, separators=(',', ':'))}"


if __name__ == "__main__":
    # Test the generator
    print("Sample test cases:")
    for i, test in enumerate(generate(3, seed=42), 1):
        print(f"Test {i}:")
        print(test)
        print()

    print("Complexity test (n=10):")
    print(generate_for_complexity(10))

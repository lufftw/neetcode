"""Check status of all problems."""
import subprocess
from pathlib import Path

solutions_dir = Path('solutions')
problems = sorted([f.stem for f in solutions_dir.glob('*.py') if not f.name.startswith('_')])

failing = []
passing = []

for problem in problems:
    try:
        result = subprocess.run(
            ['leetcode/Scripts/python.exe', 'runner/test_runner.py', problem],
            capture_output=True,
            timeout=30,
            encoding='utf-8',
            errors='replace'
        )
        stdout = result.stdout or ''
        if 'FAIL' in stdout or result.returncode != 0:
            failing.append(problem)
        else:
            passing.append(problem)
    except Exception as e:
        failing.append(problem)

print(f"Passing: {len(passing)}/45")
print(f"Failing: {len(failing)}")
if failing:
    print("\nFailing problems:")
    for p in failing:
        print(f"  - {p}")



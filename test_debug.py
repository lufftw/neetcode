#!/usr/bin/env python3
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent / 'tools'))

from generate_mindmaps import load_problems, load_ontology

output = []

output.append("=== Loading Problems ===")
problems = load_problems()
output.append(f"Loaded {len(problems)} problems")

for pid, prob in list(problems.items())[:3]:
    output.append(f"\nID: {pid}")
    output.append(f"Title: {prob.title}")
    output.append(f"LeetCode ID: {prob.leetcode_id}")
    output.append(f"Solution File: {prob.solution_file}")
    output.append(f"Display Name: {prob.display_name}")
    output.append(f"Short Name: {prob.short_name}")
    output.append(f"Linked Name: {prob.linked_name}")

# Write output
Path(__file__).parent.joinpath("test_debug_output.txt").write_text("\n".join(output), encoding="utf-8")

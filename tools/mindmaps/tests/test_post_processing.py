#!/usr/bin/env python3
"""
Unit tests for AI Markmap Agent post-processing module.

This module tests the post-processing functions that handle:
- Input preprocessing (simplify links for LLM)
- Output post-processing (convert to complete links)
- Solution artifact removal
- Duplicate prevention

Related files:
- tools/ai-markmap-agent/src/post_processing.py
"""
import unittest
import re
import sys
from pathlib import Path

# Add ai-markmap-agent src to path
AI_AGENT_SRC = Path(__file__).parent.parent / "ai-markmap-agent" / "src"
sys.path.insert(0, str(AI_AGENT_SRC))


class TestSimplifyLeetcodeLinks(unittest.TestCase):
    """Test input preprocessing (simplify links for LLM)."""
    
    def setUp(self):
        """Import the function to test."""
        from post_processing import simplify_leetcode_links
        self.simplify = simplify_leetcode_links
    
    def test_link_with_solution_separator_dot(self):
        """Test simplifying link with · separator."""
        inp = "[LeetCode 1 - Two Sum](https://leetcode.com/problems/two-sum/) · [Solution](https://github.com/...)"
        expected = "LeetCode 1 - Two Sum"
        self.assertEqual(self.simplify(inp), expected)
    
    def test_link_with_solution_separator_pipe(self):
        """Test simplifying link with | separator."""
        inp = "[LeetCode 11](https://leetcode.com/problems/container/) | [Solution](url)"
        expected = "LeetCode 11"
        self.assertEqual(self.simplify(inp), expected)
    
    def test_link_without_solution(self):
        """Test simplifying link without Solution."""
        inp = "[LeetCode 79 - Word Search](url)"
        expected = "LeetCode 79 - Word Search"
        self.assertEqual(self.simplify(inp), expected)
    
    def test_plain_text_unchanged(self):
        """Test that plain text is not changed."""
        inp = "Plain LeetCode 11 text"
        expected = "Plain LeetCode 11 text"
        self.assertEqual(self.simplify(inp), expected)
    
    def test_link_with_solution_no_separator(self):
        """Test simplifying link with no separator (edge case)."""
        inp = "[LeetCode 11](url)[Solution](url)"
        expected = "LeetCode 11"
        self.assertEqual(self.simplify(inp), expected)
    
    def test_link_with_solution_space_separator(self):
        """Test simplifying link with space separator."""
        inp = "[LeetCode 11 - Title](url) [Solution](url)"
        expected = "LeetCode 11 - Title"
        self.assertEqual(self.simplify(inp), expected)
    
    def test_preserves_title(self):
        """Test that problem title is preserved."""
        inp = "[LeetCode 79 - Word Search](https://leetcode.com/problems/word-search/) · [Solution](github)"
        result = self.simplify(inp)
        self.assertIn("Word Search", result)
        self.assertIn("LeetCode 79", result)


class TestSolutionArtifactsRemoval(unittest.TestCase):
    """Test removal of plain text Solution artifacts."""
    
    def setUp(self):
        """Create the removal function inline (to avoid import issues)."""
        def remove_solution_artifacts(content: str) -> str:
            return re.sub(r'\s*(?:·|\xb7|\|)\s*Solution(?!\])', '', content, flags=re.IGNORECASE)
        self.remove = remove_solution_artifacts
    
    def test_remove_dot_solution(self):
        """Test removing · Solution."""
        inp = "LeetCode 11 · Solution"
        expected = "LeetCode 11"
        self.assertEqual(self.remove(inp).strip(), expected)
    
    def test_remove_pipe_solution(self):
        """Test removing | Solution."""
        inp = "LeetCode 11 | Solution"
        expected = "LeetCode 11"
        self.assertEqual(self.remove(inp).strip(), expected)
    
    def test_remove_multiple_solutions(self):
        """Test removing multiple Solution artifacts."""
        inp = "LeetCode 11 · Solution · Solution"
        expected = "LeetCode 11"
        self.assertEqual(self.remove(inp).strip(), expected)
    
    def test_preserve_solution_link(self):
        """Test that [Solution] links are NOT removed."""
        inp = "[Solution](github)"
        expected = "[Solution](github)"
        self.assertEqual(self.remove(inp), expected)
    
    def test_preserve_solution_link_with_context(self):
        """Test that [Solution] links in context are preserved."""
        inp = "[LeetCode 11](url) · [Solution](github)"
        result = self.remove(inp)
        self.assertIn("[Solution]", result)


class TestLinkPatternMatching(unittest.TestCase):
    """Test that the regex pattern matches all expected formats."""
    
    def setUp(self):
        """Define the pattern used in post-processing."""
        self.pattern = r'\[(LeetCode\s+\d+[^\]]*)\]\(([^)]+)\)(\s*(?:·|\xb7|\|)?\s*\[Solution\]\([^)]+\))?'
    
    def test_simple_link(self):
        """Test matching simple LeetCode link."""
        inp = "[LeetCode 11](url)"
        match = re.search(self.pattern, inp, flags=re.IGNORECASE)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(0), inp)
        self.assertIsNone(match.group(3))  # No Solution
    
    def test_link_with_title(self):
        """Test matching link with title."""
        inp = "[LeetCode 11 - Container With Most Water](url)"
        match = re.search(self.pattern, inp, flags=re.IGNORECASE)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(0), inp)
    
    def test_link_with_solution_dot(self):
        """Test matching link with · Solution."""
        inp = "[LeetCode 11](url) · [Solution](github)"
        match = re.search(self.pattern, inp, flags=re.IGNORECASE)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(0), inp)  # Full match including Solution
        self.assertIsNotNone(match.group(3))  # Has Solution
    
    def test_link_with_solution_pipe(self):
        """Test matching link with | Solution."""
        inp = "[LeetCode 11](url) | [Solution](github)"
        match = re.search(self.pattern, inp, flags=re.IGNORECASE)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(0), inp)
        self.assertIsNotNone(match.group(3))
    
    def test_link_with_solution_no_separator(self):
        """Test matching link with no separator."""
        inp = "[LeetCode 11](url)[Solution](github)"
        match = re.search(self.pattern, inp, flags=re.IGNORECASE)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(0), inp)
        self.assertIsNotNone(match.group(3))
    
    def test_link_with_solution_space(self):
        """Test matching link with space separator."""
        inp = "[LeetCode 11](url) [Solution](github)"
        match = re.search(self.pattern, inp, flags=re.IGNORECASE)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(0), inp)


class TestDuplicatePrevention(unittest.TestCase):
    """Test that processing won't create duplicate Solution links."""
    
    def setUp(self):
        """Define the pattern."""
        self.pattern = r'\[(LeetCode\s+\d+[^\]]*)\]\(([^)]+)\)(\s*(?:·|\xb7|\|)?\s*\[Solution\]\([^)]+\))?'
    
    def test_full_match_prevents_duplicate_dot(self):
        """Test full match with · separator prevents duplicate."""
        inp = "[LeetCode 11](url) · [Solution](github)"
        match = re.search(self.pattern, inp, flags=re.IGNORECASE)
        self.assertEqual(match.group(0), inp)  # Entire string matched
    
    def test_full_match_prevents_duplicate_no_sep(self):
        """Test full match with no separator prevents duplicate."""
        inp = "[LeetCode 11](url)[Solution](github)"
        match = re.search(self.pattern, inp, flags=re.IGNORECASE)
        self.assertEqual(match.group(0), inp)
    
    def test_full_match_prevents_duplicate_pipe(self):
        """Test full match with | separator prevents duplicate."""
        inp = "[LeetCode 11](url) | [Solution](github)"
        match = re.search(self.pattern, inp, flags=re.IGNORECASE)
        self.assertEqual(match.group(0), inp)


class TestPreprocessForLLM(unittest.TestCase):
    """Test the full preprocess_for_llm function."""
    
    def setUp(self):
        """Import the function."""
        from post_processing import preprocess_for_llm
        self.preprocess = preprocess_for_llm
    
    def test_simplifies_links(self):
        """Test that links are simplified."""
        inp = "[LeetCode 1 - Two Sum](url) · [Solution](github)"
        result = self.preprocess(inp)
        self.assertEqual(result, "LeetCode 1 - Two Sum")
    
    def test_collapses_blank_lines(self):
        """Test that multiple blank lines are collapsed."""
        inp = "Line 1\n\n\n\nLine 2"
        result = self.preprocess(inp)
        self.assertEqual(result, "Line 1\n\nLine 2")
    
    def test_combined(self):
        """Test combined preprocessing."""
        inp = "[LeetCode 1](url) · [Solution](github)\n\n\n\n[LeetCode 2](url)"
        result = self.preprocess(inp)
        self.assertIn("LeetCode 1", result)
        self.assertIn("LeetCode 2", result)
        self.assertNotIn("[Solution]", result)
        self.assertNotIn("\n\n\n", result)


if __name__ == '__main__':
    unittest.main()


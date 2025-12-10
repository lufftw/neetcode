# .dev/tests/test_generate_mindmaps.py
"""
Characterization tests for tools/generate_mindmaps.py

These tests capture the current behavior of the mind map generator
to ensure refactoring doesn't break existing functionality.

Test categories:
1. TOML Parser - parse_toml_simple, parse_toml_value
2. Data Loading - load_ontology, load_problems
3. Mind Map Generation - each generator function
4. HTML Generation - HTML template generation
5. Configuration - config loading
6. Edge Cases - empty data, missing files
"""
import pytest
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

# Import from the refactored modules
from mindmaps.toml_parser import parse_toml_simple, parse_toml_value
from mindmaps.loader import OntologyData, load_ontology, load_problems
from mindmaps.data import ProblemData
from mindmaps.helpers import markmap_frontmatter, format_problem_entry
from mindmaps.config import MindmapsConfig, load_config, get_config, DIFFICULTY_ICONS
from mindmaps.html import markdown_to_html_content, generate_html_mindmap
from mindmaps.generators import (
    generate_pattern_hierarchy,
    generate_family_derivation,
    generate_algorithm_usage,
    generate_data_structure,
    generate_company_coverage,
    generate_roadmap_paths,
    generate_problem_relations,
    generate_solution_variants,
    generate_difficulty_topics,
)


# ===========================================================================
# Test: TOML Parser
# ===========================================================================

class TestTomlParser:
    """Test parse_toml_simple and parse_toml_value functions."""
    
    def test_parse_toml_value_string(self):
        """Test parsing string values."""
        assert parse_toml_value('"hello"') == "hello"
        assert parse_toml_value('"hello world"') == "hello world"
        assert parse_toml_value('""') == ""
    
    def test_parse_toml_value_array(self):
        """Test parsing array values."""
        assert parse_toml_value('["a", "b", "c"]') == ["a", "b", "c"]
        assert parse_toml_value('[]') == []
        assert parse_toml_value('["single"]') == ["single"]
    
    def test_parse_toml_value_boolean(self):
        """Test parsing boolean values."""
        assert parse_toml_value("true") is True
        assert parse_toml_value("false") is False
    
    def test_parse_toml_value_number(self):
        """Test parsing integer values."""
        assert parse_toml_value("123") == 123
        assert parse_toml_value("0") == 0
        assert parse_toml_value("-1") == -1
    
    def test_parse_toml_value_unquoted_string(self):
        """Test parsing unquoted strings (returned as-is)."""
        assert parse_toml_value("some_id") == "some_id"
    
    def test_parse_toml_simple_basic(self):
        """Test basic TOML parsing."""
        content = '''
id = "0003"
title = "Test Problem"
leetcode_id = 3
'''
        result = parse_toml_simple(content)
        assert result["id"] == "0003"
        assert result["title"] == "Test Problem"
        assert result["leetcode_id"] == 3
    
    def test_parse_toml_simple_array_of_tables(self):
        """Test parsing [[array]] syntax."""
        content = '''
[[api_kernels]]
id = "Kernel1"
summary = "First kernel"

[[api_kernels]]
id = "Kernel2"
summary = "Second kernel"
'''
        result = parse_toml_simple(content)
        assert "api_kernels" in result
        assert len(result["api_kernels"]) == 2
        assert result["api_kernels"][0]["id"] == "Kernel1"
        assert result["api_kernels"][1]["id"] == "Kernel2"
    
    def test_parse_toml_simple_table(self):
        """Test parsing [table] syntax."""
        content = '''
[pattern_role]
is_base_template = true
base_for_kernel = "SubstringSlidingWindow"
'''
        result = parse_toml_simple(content)
        assert "pattern_role" in result
        assert result["pattern_role"]["is_base_template"] is True
        assert result["pattern_role"]["base_for_kernel"] == "SubstringSlidingWindow"
    
    def test_parse_toml_simple_with_arrays(self):
        """Test parsing array values in TOML."""
        content = '''
topics = ["string", "hash_table", "sliding_window"]
companies = ["google", "amazon"]
'''
        result = parse_toml_simple(content)
        assert result["topics"] == ["string", "hash_table", "sliding_window"]
        assert result["companies"] == ["google", "amazon"]
    
    def test_parse_toml_simple_skip_comments(self):
        """Test that comments are skipped."""
        content = '''
# This is a comment
id = "test"
# Another comment
title = "Test Title"
'''
        result = parse_toml_simple(content)
        assert result["id"] == "test"
        assert result["title"] == "Test Title"
        assert len(result) == 2


# ===========================================================================
# Test: Data Classes
# ===========================================================================

class TestProblemData:
    """Test ProblemData class methods."""
    
    def test_display_name(self):
        """Test display_name property."""
        prob = ProblemData(id="0003", title="Test Problem", leetcode_id=3)
        assert prob.display_name == "LeetCode 3 - Test Problem"
    
    def test_display_name_without_leetcode_id(self):
        """Test display_name when leetcode_id is not set."""
        prob = ProblemData(id="0003", title="Test Problem", leetcode_id=0)
        assert prob.display_name == "LeetCode 3 - Test Problem"
    
    def test_difficulty_icon(self):
        """Test difficulty_icon property."""
        easy = ProblemData(id="1", title="Easy", difficulty="easy")
        medium = ProblemData(id="2", title="Medium", difficulty="medium")
        hard = ProblemData(id="3", title="Hard", difficulty="hard")
        unknown = ProblemData(id="4", title="Unknown", difficulty="unknown")
        
        assert easy.difficulty_icon == "🟢"
        assert medium.difficulty_icon == "🟡"
        assert hard.difficulty_icon == "🔴"
        assert unknown.difficulty_icon == "⚪"
    
    def test_solution_link_with_solution_file(self):
        """Test solution_link with explicit solution_file."""
        prob = ProblemData(
            id="0003",
            title="Test",
            solution_file="solutions/0003_test.py"
        )
        # With GitHub links
        link = prob.solution_link(use_github_link=True)
        assert "solutions/0003_test.py" in link
        assert link.startswith("https://")
        
        # With relative links
        link = prob.solution_link(use_github_link=False)
        assert link == "../../solutions/0003_test.py"
    
    def test_solution_link_with_slug(self):
        """Test solution_link fallback to slug."""
        prob = ProblemData(
            id="0003",
            title="Test",
            slug="0003_test_problem"
        )
        link = prob.solution_link(use_github_link=False)
        assert link == "../../solutions/0003_test_problem.py"
    
    def test_markdown_link_with_difficulty(self):
        """Test markdown_link includes difficulty icon."""
        prob = ProblemData(
            id="0003",
            title="Test Problem",
            leetcode_id=3,
            difficulty="medium",
            slug="0003_test"
        )
        link = prob.markdown_link(include_difficulty=True, use_github_link=False)
        assert "🟡" in link
        assert "LeetCode 3 - Test Problem" in link
    
    def test_markdown_link_without_difficulty(self):
        """Test markdown_link without difficulty icon."""
        prob = ProblemData(
            id="0003",
            title="Test Problem",
            leetcode_id=3,
            difficulty="medium",
            slug="0003_test"
        )
        link = prob.markdown_link(include_difficulty=False, use_github_link=False)
        assert "🟡" not in link
        assert "LeetCode 3 - Test Problem" in link
    
    def test_leetcode_link(self):
        """Test leetcode_link returns LeetCode URL."""
        prob = ProblemData(
            id="0003",
            title="Test Problem",
            leetcode_id=3,
            url="https://leetcode.com/problems/test/"
        )
        link = prob.leetcode_link()
        assert "https://leetcode.com/problems/test/" in link
        assert "LeetCode 3 - Test Problem" in link


class TestOntologyData:
    """Test OntologyData class."""
    
    def test_default_empty_lists(self):
        """Test that OntologyData initializes with empty lists."""
        data = OntologyData()
        assert data.api_kernels == []
        assert data.patterns == []
        assert data.families == []
        assert data.algorithms == []
        assert data.data_structures == []
        assert data.topics == []
        assert data.difficulties == []
        assert data.companies == []
        assert data.roadmaps == []


# ===========================================================================
# Test: Markmap Helpers
# ===========================================================================

class TestMarkmapHelpers:
    """Test markmap helper functions."""
    
    def test_markmap_frontmatter(self):
        """Test markmap_frontmatter generates valid YAML."""
        result = markmap_frontmatter("Test Title")
        assert "---" in result
        assert "title: Test Title" in result
        assert "markmap:" in result
        assert "colorFreezeLevel:" in result
    
    def test_markmap_frontmatter_custom_freeze_level(self):
        """Test markmap_frontmatter with custom color freeze level."""
        result = markmap_frontmatter("Test", color_freeze_level=5)
        assert "colorFreezeLevel: 5" in result
    
    def test_format_problem_entry_basic(self):
        """Test format_problem_entry returns formatted string."""
        prob = ProblemData(
            id="0003",
            title="Test Problem",
            leetcode_id=3,
            difficulty="medium",
            slug="0003_test"
        )
        result = format_problem_entry(prob)
        assert "🟡" in result
        assert "LeetCode 3" in result
    
    def test_format_problem_entry_with_complexity(self):
        """Test format_problem_entry shows complexity when requested."""
        prob = ProblemData(
            id="0003",
            title="Test Problem",
            leetcode_id=3,
            difficulty="medium",
            slug="0003_test",
            solutions=[{"complexity": "O(n)"}]
        )
        result = format_problem_entry(prob, show_complexity=True)
        assert "O(n)" in result


# ===========================================================================
# Test: Mind Map Generators
# ===========================================================================

class TestMindMapGenerators:
    """Test mind map generation functions."""
    
    @pytest.fixture
    def sample_ontology(self):
        """Create sample ontology data for testing."""
        ontology = OntologyData()
        ontology.api_kernels = [
            {"id": "SubstringSlidingWindow", "description": "Sliding window over sequences"},
            {"id": "GridBFSMultiSource", "description": "BFS on grids"},
        ]
        ontology.patterns = [
            {"id": "sliding_window_unique", "api_kernel": "SubstringSlidingWindow", "description": "Unique chars"},
            {"id": "sliding_window_freq_cover", "api_kernel": "SubstringSlidingWindow", "description": "Freq cover"},
            {"id": "grid_bfs_propagation", "api_kernel": "GridBFSMultiSource", "description": "BFS propagation"},
        ]
        ontology.algorithms = [
            {"id": "sliding_window", "summary": "Sliding window technique"},
            {"id": "bfs", "summary": "Breadth-first search"},
        ]
        ontology.data_structures = [
            {"id": "hash_map", "summary": "Hash table"},
            {"id": "queue", "summary": "FIFO queue"},
        ]
        ontology.companies = [
            {"id": "google", "name": "Google"},
            {"id": "amazon", "name": "Amazon"},
        ]
        ontology.roadmaps = [
            {"id": "neetcode_150", "name": "NeetCode 150"},
        ]
        return ontology
    
    @pytest.fixture
    def sample_problems(self):
        """Create sample problem data for testing."""
        return {
            "0003": ProblemData(
                id="0003",
                title="Longest Substring Without Repeating Characters",
                slug="0003_longest_substring",
                leetcode_id=3,
                difficulty="medium",
                topics=["string", "sliding_window"],
                companies=["google", "amazon"],
                roadmaps=["neetcode_150"],
                api_kernels=["SubstringSlidingWindow"],
                patterns=["sliding_window_unique"],
                algorithms=["sliding_window"],
                data_structures=["hash_map"],
                related_problems=["0076"],
                is_base_template=True,
                base_for_kernel="SubstringSlidingWindow",
                derived_problems=["0076"],
                solutions=[{"key": "default", "complexity": "O(n)", "notes": "Base template"}],
            ),
            "0076": ProblemData(
                id="0076",
                title="Minimum Window Substring",
                slug="0076_minimum_window",
                leetcode_id=76,
                difficulty="hard",
                topics=["string", "sliding_window"],
                companies=["google"],
                roadmaps=["neetcode_150"],
                api_kernels=["SubstringSlidingWindow"],
                patterns=["sliding_window_freq_cover"],
                algorithms=["sliding_window"],
                data_structures=["hash_map"],
                related_problems=["0003"],
                solutions=[
                    {"key": "default", "role": "base", "complexity": "O(n)"},
                    {"key": "optimized", "role": "variant", "complexity": "O(n)", "delta": "Optimized version"},
                ],
            ),
        }
    
    def test_generate_pattern_hierarchy(self, sample_ontology, sample_problems):
        """Test pattern hierarchy mind map generation."""
        result = generate_pattern_hierarchy(sample_ontology, sample_problems)
        
        # Check structure
        assert "# Pattern Hierarchy" in result
        assert "SubstringSlidingWindow" in result
        assert "Sliding Window Unique" in result
        assert "LeetCode 3" in result
    
    def test_generate_family_derivation(self, sample_ontology, sample_problems):
        """Test family derivation mind map generation."""
        result = generate_family_derivation(sample_ontology, sample_problems)
        
        assert "# Problem Family Derivation" in result
        assert "Base Template" in result
        assert "Derived Problems" in result
        assert "LeetCode 3" in result
    
    def test_generate_family_derivation_no_base_templates(self, sample_ontology):
        """Test family derivation when no base templates exist."""
        result = generate_family_derivation(sample_ontology, {})
        
        assert "No Base Templates Found" in result
    
    def test_generate_algorithm_usage(self, sample_ontology, sample_problems):
        """Test algorithm usage mind map generation."""
        result = generate_algorithm_usage(sample_ontology, sample_problems)
        
        assert "# Algorithm Usage" in result
        assert "Sliding Window" in result
        assert "LeetCode 3" in result
    
    def test_generate_data_structure(self, sample_ontology, sample_problems):
        """Test data structure mind map generation."""
        result = generate_data_structure(sample_ontology, sample_problems)
        
        assert "# Data Structure Usage" in result
        assert "Hash Map" in result
    
    def test_generate_company_coverage(self, sample_ontology, sample_problems):
        """Test company coverage mind map generation."""
        result = generate_company_coverage(sample_ontology, sample_problems)
        
        assert "# Company Interview Coverage" in result
        assert "Google" in result
        assert "Amazon" in result
    
    def test_generate_roadmap_paths(self, sample_ontology, sample_problems):
        """Test roadmap paths mind map generation."""
        result = generate_roadmap_paths(sample_ontology, sample_problems)
        
        assert "# Learning Roadmaps" in result
        assert "NeetCode 150" in result or "neetcode_150" in result
    
    def test_generate_problem_relations(self, sample_ontology, sample_problems):
        """Test problem relations mind map generation."""
        result = generate_problem_relations(sample_ontology, sample_problems)
        
        assert "# Problem Relations Network" in result
        assert "Related Problems" in result
    
    def test_generate_solution_variants(self, sample_ontology, sample_problems):
        """Test solution variants mind map generation."""
        result = generate_solution_variants(sample_ontology, sample_problems)
        
        assert "# Solution Variants" in result
        # Problem 0076 has 2 solutions
        assert "LeetCode 76" in result or "approaches" in result
    
    def test_generate_solution_variants_no_multi_solution(self, sample_ontology):
        """Test solution variants when no multi-solution problems exist."""
        problems = {
            "0001": ProblemData(
                id="0001",
                title="Single Solution",
                leetcode_id=1,
                difficulty="easy",
                solutions=[{"key": "default"}]  # Only one solution
            )
        }
        result = generate_solution_variants(sample_ontology, problems)
        
        assert "No Multi-Solution Problems" in result
    
    def test_generate_difficulty_topics(self, sample_ontology, sample_problems):
        """Test difficulty × topics mind map generation."""
        result = generate_difficulty_topics(sample_ontology, sample_problems)
        
        assert "# Difficulty × Topics Matrix" in result
        assert "🟡" in result or "Medium" in result
        assert "🔴" in result or "Hard" in result


# ===========================================================================
# Test: HTML Generation
# ===========================================================================

class TestHtmlGeneration:
    """Test HTML generation functions."""
    
    def test_markdown_to_html_content_strips_frontmatter(self):
        """Test that frontmatter is removed from markdown."""
        content = '''---
title: Test
markmap:
  colorFreezeLevel: 2
---

# Main Title

Content here
'''
        result = markdown_to_html_content(content)
        
        assert "---" not in result.strip()[:10]  # No frontmatter at start
        assert "# Main Title" in result
        assert "Content here" in result
    
    def test_markdown_to_html_content_no_frontmatter(self):
        """Test content without frontmatter is unchanged."""
        content = '''# Main Title

Content here
'''
        result = markdown_to_html_content(content)
        
        assert "# Main Title" in result
        assert "Content here" in result
    
    def test_generate_html_mindmap_structure(self):
        """Test that generated HTML has required structure."""
        markdown = '''# Test Map

## Section 1

Content
'''
        result = generate_html_mindmap("Test Title", markdown, use_autoloader=False)
        
        assert "<!DOCTYPE html>" in result
        assert "<title>Test Title" in result
        assert "markmap" in result.lower()
        assert "d3" in result
    
    def test_generate_html_mindmap_with_autoloader(self):
        """Test HTML generation with autoloader option."""
        markdown = "# Test"
        result = generate_html_mindmap("Test", markdown, use_autoloader=True)
        
        assert "markmap-autoloader" in result


# ===========================================================================
# Test: Configuration
# ===========================================================================

class TestConfiguration:
    """Test configuration loading."""
    
    def test_mindmaps_config_defaults(self):
        """Test MindmapsConfig default values."""
        config = MindmapsConfig()
        
        assert config.github_repo_url != ""
        assert config.github_branch != ""
        assert isinstance(config.use_github_links, bool)
    
    def test_load_config_returns_config_object(self):
        """Test load_config returns MindmapsConfig instance."""
        config = load_config()
        
        assert isinstance(config, MindmapsConfig)
    
    def test_get_config_singleton(self):
        """Test get_config returns same instance."""
        config1 = get_config()
        config2 = get_config()
        
        # Should be same instance (singleton)
        assert config1 is config2


# ===========================================================================
# Test: Edge Cases
# ===========================================================================

class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_ontology(self):
        """Test generators work with empty ontology."""
        ontology = OntologyData()
        problems = {}
        
        # Should not raise exceptions
        result = generate_pattern_hierarchy(ontology, problems)
        assert "# Pattern Hierarchy" in result
        
        result = generate_algorithm_usage(ontology, problems)
        assert "# Algorithm Usage" in result
    
    def test_problem_without_solutions(self):
        """Test ProblemData without solutions."""
        prob = ProblemData(
            id="0001",
            title="No Solutions",
            leetcode_id=1,
            difficulty="easy"
        )
        
        result = format_problem_entry(prob, show_complexity=True)
        assert "LeetCode 1" in result
        # Should not crash, just no complexity shown
    
    def test_problem_with_empty_fields(self):
        """Test ProblemData with minimal fields."""
        prob = ProblemData(id="0001", title="Minimal")
        
        assert prob.display_name == "LeetCode 1 - Minimal"
        assert prob.difficulty_icon == "⚪"
        assert prob.solution_link() == ""
    
    def test_parse_toml_empty_content(self):
        """Test TOML parser with empty content."""
        result = parse_toml_simple("")
        assert result == {}
    
    def test_parse_toml_only_comments(self):
        """Test TOML parser with only comments."""
        content = '''
# Comment 1
# Comment 2
'''
        result = parse_toml_simple(content)
        assert result == {}
    
    def test_difficulty_icons_coverage(self):
        """Test all difficulty levels have icons."""
        assert "easy" in DIFFICULTY_ICONS
        assert "medium" in DIFFICULTY_ICONS
        assert "hard" in DIFFICULTY_ICONS


# ===========================================================================
# Test: Integration with Real Data
# ===========================================================================

class TestIntegrationWithRealData:
    """Integration tests using actual project data."""
    
    @pytest.fixture
    def real_ontology(self):
        """Load actual ontology if available."""
        try:
            return load_ontology()
        except Exception:
            pytest.skip("Ontology files not available")
    
    @pytest.fixture
    def real_problems(self):
        """Load actual problems if available."""
        try:
            return load_problems()
        except Exception:
            pytest.skip("Problem metadata not available")
    
    def test_load_ontology_structure(self, real_ontology):
        """Test loaded ontology has expected structure."""
        # Should have API kernels
        assert len(real_ontology.api_kernels) > 0
        
        # Each kernel should have id and summary
        for kernel in real_ontology.api_kernels:
            assert "id" in kernel
    
    def test_load_problems_structure(self, real_problems):
        """Test loaded problems have expected structure."""
        # Should have some problems
        assert len(real_problems) > 0
        
        # Each problem should be ProblemData instance
        for prob_id, prob in real_problems.items():
            assert isinstance(prob, ProblemData)
            assert prob.id != ""
            assert prob.title != ""
    
    def test_generate_all_mindmaps_no_crash(self, real_ontology, real_problems):
        """Test all generators complete without crashing."""
        generators = [
            generate_pattern_hierarchy,
            generate_family_derivation,
            generate_algorithm_usage,
            generate_data_structure,
            generate_company_coverage,
            generate_roadmap_paths,
            generate_problem_relations,
            generate_solution_variants,
            generate_difficulty_topics,
        ]
        
        for gen in generators:
            result = gen(real_ontology, real_problems)
            assert isinstance(result, str)
            assert len(result) > 0


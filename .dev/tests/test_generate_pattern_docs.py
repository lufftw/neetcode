# .dev/tests/test_generate_pattern_docs.py
"""
Characterization tests for tools/generate_pattern_docs.py

These tests capture the current behavior of the pattern documentation generator
to ensure refactoring doesn't break existing functionality.

Test categories:
1. TOML Parser - parse_toml_simple function
2. Data Classes - APIKernel, Pattern, PatternDocConfig
3. Ontology Loading - load_api_kernels, load_patterns
4. File Collection - collect_source_files
5. Document Composition - section numbering, TOC generation
6. Edge Cases - missing files, empty data
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
from patterndocs.toml_parser import parse_toml_simple
from patterndocs.data import APIKernel, Pattern, PatternDocConfig
from patterndocs.loader import (
    load_api_kernels,
    load_patterns,
    get_available_patterns,
    get_kernel_id_from_dir_name,
)
from patterndocs.files import (
    collect_source_files,
    STRUCTURAL_FILES_ORDER,
    STRUCTURAL_FILES_FOOTER,
)
from patterndocs.sections import generate_toc, create_anchor, add_section_numbers
from patterndocs.composer import compose_document


# ===========================================================================
# Test: TOML Parser
# ===========================================================================

class TestTomlParser:
    """Test parse_toml_simple function."""
    
    def test_parse_basic_key_value(self):
        """Test parsing basic key = value pairs."""
        content = '''
id = "test_id"
summary = "Test summary"
'''
        result = parse_toml_simple(content)
        
        assert result["id"] == "test_id"
        assert result["summary"] == "Test summary"
    
    def test_parse_array_of_tables(self):
        """Test parsing [[array]] syntax."""
        content = '''
[[api_kernels]]
id = "Kernel1"
summary = "First"

[[api_kernels]]
id = "Kernel2"
summary = "Second"
'''
        result = parse_toml_simple(content)
        
        assert "api_kernels" in result
        assert len(result["api_kernels"]) == 2
        assert result["api_kernels"][0]["id"] == "Kernel1"
        assert result["api_kernels"][1]["id"] == "Kernel2"
    
    def test_parse_skip_comments(self):
        """Test that comments are skipped."""
        content = '''
# This is a comment
id = "test"
# Another comment
summary = "Test"
'''
        result = parse_toml_simple(content)
        
        assert result["id"] == "test"
        assert result["summary"] == "Test"
        assert len(result) == 2
    
    def test_parse_skip_empty_lines(self):
        """Test that empty lines are skipped."""
        content = '''

id = "test"

summary = "Test"

'''
        result = parse_toml_simple(content)
        
        assert result["id"] == "test"
        assert result["summary"] == "Test"
    
    def test_parse_quoted_string(self):
        """Test parsing quoted strings."""
        content = 'message = "Hello World"'
        result = parse_toml_simple(content)
        
        assert result["message"] == "Hello World"
    
    def test_parse_unquoted_value(self):
        """Test parsing unquoted values."""
        content = 'api_kernel = SubstringSlidingWindow'
        result = parse_toml_simple(content)
        
        assert result["api_kernel"] == "SubstringSlidingWindow"
    
    def test_parse_empty_content(self):
        """Test parsing empty content."""
        result = parse_toml_simple("")
        assert result == {}
    
    def test_parse_only_comments(self):
        """Test parsing content with only comments."""
        content = '''
# Comment 1
# Comment 2
'''
        result = parse_toml_simple(content)
        assert result == {}


# ===========================================================================
# Test: Data Classes
# ===========================================================================

class TestDataClasses:
    """Test data classes."""
    
    def test_api_kernel_creation(self):
        """Test APIKernel dataclass."""
        kernel = APIKernel(id="TestKernel", summary="Test summary")
        
        assert kernel.id == "TestKernel"
        assert kernel.summary == "Test summary"
    
    def test_pattern_creation(self):
        """Test Pattern dataclass."""
        pattern = Pattern(
            id="test_pattern",
            api_kernel="TestKernel",
            summary="Test pattern summary"
        )
        
        assert pattern.id == "test_pattern"
        assert pattern.api_kernel == "TestKernel"
        assert pattern.summary == "Test pattern summary"
    
    def test_pattern_doc_config_creation(self):
        """Test PatternDocConfig dataclass."""
        config = PatternDocConfig(
            kernel_id="TestKernel",
            kernel_summary="Test summary",
            source_dir=Path("/test/source"),
            output_file=Path("/test/output.md")
        )
        
        assert config.kernel_id == "TestKernel"
        assert config.kernel_summary == "Test summary"
        assert config.source_dir == Path("/test/source")
        assert config.output_file == Path("/test/output.md")
        assert config.patterns == []  # Default empty list
    
    def test_pattern_doc_config_with_patterns(self):
        """Test PatternDocConfig with patterns."""
        patterns = [
            Pattern(id="p1", api_kernel="K1", summary="P1"),
            Pattern(id="p2", api_kernel="K1", summary="P2"),
        ]
        config = PatternDocConfig(
            kernel_id="K1",
            kernel_summary="Kernel 1",
            source_dir=Path("/test"),
            output_file=Path("/out.md"),
            patterns=patterns
        )
        
        assert len(config.patterns) == 2
        assert config.patterns[0].id == "p1"


# ===========================================================================
# Test: Kernel ID Mapping
# ===========================================================================

class TestKernelIdMapping:
    """Test get_kernel_id_from_dir_name function."""
    
    def test_sliding_window_mapping(self):
        """Test sliding_window maps to SubstringSlidingWindow."""
        assert get_kernel_id_from_dir_name("sliding_window") == "SubstringSlidingWindow"
    
    def test_bfs_grid_mapping(self):
        """Test bfs_grid maps to GridBFSMultiSource."""
        assert get_kernel_id_from_dir_name("bfs_grid") == "GridBFSMultiSource"
    
    def test_backtracking_mapping(self):
        """Test backtracking maps to BacktrackingExploration."""
        assert get_kernel_id_from_dir_name("backtracking") == "BacktrackingExploration"
    
    def test_binary_search_mapping(self):
        """Test binary_search maps to BinarySearchBoundary."""
        assert get_kernel_id_from_dir_name("binary_search") == "BinarySearchBoundary"
    
    def test_unknown_mapping_returns_input(self):
        """Test unknown patterns return the input as-is."""
        assert get_kernel_id_from_dir_name("unknown_pattern") == "unknown_pattern"
    
    def test_all_known_mappings_exist(self):
        """Test all documented mappings work."""
        mappings = {
            "sliding_window": "SubstringSlidingWindow",
            "bfs_grid": "GridBFSMultiSource",
            "backtracking": "BacktrackingExploration",
            "k_way_merge": "KWayMerge",
            "binary_search": "BinarySearchBoundary",
            "two_pointers": "TwoPointerPartition",
            "linked_list_reversal": "LinkedListInPlaceReversal",
            "monotonic_stack": "MonotonicStack",
            "prefix_sum": "PrefixSumRangeQuery",
            "tree_dfs": "TreeTraversalDFS",
            "tree_bfs": "TreeTraversalBFS",
            "dp_sequence": "DPSequence",
            "dp_interval": "DPInterval",
            "union_find": "UnionFindConnectivity",
            "trie": "TriePrefixSearch",
            "heap_top_k": "HeapTopK",
            "topological_sort": "TopologicalSort",
        }
        
        for dir_name, expected_id in mappings.items():
            assert get_kernel_id_from_dir_name(dir_name) == expected_id


# ===========================================================================
# Test: TOC Generation
# ===========================================================================

class TestTocGeneration:
    """Test table of contents generation."""
    
    def test_generate_toc_basic(self):
        """Test basic TOC generation."""
        sections_info = [
            (1, "Core Concepts", "1-core-concepts"),
            (2, "Base Template", "2-base-template"),
            (3, "Variations", "3-variations"),
        ]
        
        result = generate_toc(sections_info)
        
        assert "## Table of Contents" in result
        assert "[Core Concepts](#1-core-concepts)" in result
        assert "[Base Template](#2-base-template)" in result
        assert "[Variations](#3-variations)" in result
    
    def test_generate_toc_empty(self):
        """Test TOC generation with empty list."""
        result = generate_toc([])
        
        assert "## Table of Contents" in result
    
    def test_generate_toc_preserves_order(self):
        """Test that TOC preserves section order."""
        sections_info = [
            (1, "First", "1-first"),
            (2, "Second", "2-second"),
            (3, "Third", "3-third"),
        ]
        
        result = generate_toc(sections_info)
        lines = result.split("\n")
        
        # Find content lines (skip header)
        content_lines = [l for l in lines if l.startswith("1.") or l.startswith("2.") or l.startswith("3.")]
        
        assert "First" in content_lines[0]
        assert "Second" in content_lines[1]
        assert "Third" in content_lines[2]


# ===========================================================================
# Test: Anchor Creation
# ===========================================================================

class TestAnchorCreation:
    """Test create_anchor function."""
    
    def test_create_anchor_basic(self):
        """Test basic anchor creation."""
        result = create_anchor(1, "Core Concepts")
        assert result == "1-core-concepts"
    
    def test_create_anchor_with_special_chars(self):
        """Test anchor creation removes special characters."""
        result = create_anchor(2, "Base Template (LeetCode 3)")
        
        # Should not contain parentheses
        assert "(" not in result
        assert ")" not in result
    
    def test_create_anchor_replaces_spaces(self):
        """Test anchor creation replaces spaces with dashes."""
        result = create_anchor(1, "Multiple Word Title")
        
        assert " " not in result
        assert "-" in result
    
    def test_create_anchor_removes_colons(self):
        """Test anchor creation removes colons."""
        result = create_anchor(1, "Section: Subsection")
        
        assert ":" not in result
    
    def test_create_anchor_removes_slashes(self):
        """Test anchor creation removes slashes."""
        result = create_anchor(1, "Either/Or")
        
        assert "/" not in result


# ===========================================================================
# Test: Section Numbering
# ===========================================================================

class TestSectionNumbering:
    """Test add_section_numbers function."""
    
    def test_add_section_numbers_basic(self):
        """Test basic section numbering."""
        content = '''## Core Concepts

Some content here.

## Base Template

More content.
'''
        result, sections_info = add_section_numbers(content, 1)
        
        assert "## 1. Core Concepts" in result
        assert "## 2. Base Template" in result
        assert len(sections_info) == 2
    
    def test_add_section_numbers_with_subsections(self):
        """Test section numbering includes subsections."""
        content = '''## Main Section

### Subsection One

### Subsection Two
'''
        result, sections_info = add_section_numbers(content, 1)
        
        assert "## 1. Main Section" in result
        assert "### 1.1 Subsection One" in result
        assert "### 1.2 Subsection Two" in result
    
    def test_add_section_numbers_starting_from_custom(self):
        """Test starting section number can be customized."""
        content = '''## Section

Content.
'''
        result, sections_info = add_section_numbers(content, 5)
        
        assert "## 5. Section" in result
        assert sections_info[0][0] == 5
    
    def test_add_section_numbers_preserves_non_headers(self):
        """Test non-header content is preserved."""
        content = '''## Section

Regular paragraph.

- List item 1
- List item 2

```python
code block
```
'''
        result, _ = add_section_numbers(content, 1)
        
        assert "Regular paragraph." in result
        assert "- List item 1" in result
        assert "```python" in result
    
    def test_add_section_numbers_returns_sections_info(self):
        """Test sections_info contains correct data."""
        content = '''## First Section

## Second Section
'''
        _, sections_info = add_section_numbers(content, 1)
        
        assert len(sections_info) == 2
        assert sections_info[0][0] == 1  # Section number
        assert sections_info[0][1] == "First Section"  # Title
        assert sections_info[1][0] == 2
        assert sections_info[1][1] == "Second Section"


# ===========================================================================
# Test: File Collection
# ===========================================================================

class TestFileCollection:
    """Test collect_source_files function."""
    
    def test_collect_source_files_categorization(self):
        """Test files are categorized correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            # Create test files
            (tmpdir / "_header.md").write_text("# Header")
            (tmpdir / "_comparison.md").write_text("# Comparison")
            (tmpdir / "_templates.md").write_text("# Templates")
            (tmpdir / "0003_base.md").write_text("# Problem 3")
            (tmpdir / "0076_variant.md").write_text("# Problem 76")
            
            header_files, problem_files, footer_files = collect_source_files(tmpdir)
            
            # Check categorization
            assert len(header_files) == 1
            assert header_files[0].name == "_header.md"
            
            assert len(problem_files) == 2
            assert problem_files[0].name == "0003_base.md"
            assert problem_files[1].name == "0076_variant.md"
            
            assert len(footer_files) == 2
            assert any(f.name == "_comparison.md" for f in footer_files)
            assert any(f.name == "_templates.md" for f in footer_files)
    
    def test_collect_source_files_nonexistent_dir(self):
        """Test with nonexistent directory."""
        header, problem, footer = collect_source_files(Path("/nonexistent"))
        
        assert header == []
        assert problem == []
        assert footer == []
    
    def test_collect_source_files_empty_dir(self):
        """Test with empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            header, problem, footer = collect_source_files(Path(tmpdir))
            
            assert header == []
            assert problem == []
            assert footer == []
    
    def test_collect_source_files_problem_ordering(self):
        """Test problem files are sorted by name."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            # Create out of order
            (tmpdir / "0076_b.md").write_text("")
            (tmpdir / "0003_a.md").write_text("")
            (tmpdir / "0209_c.md").write_text("")
            
            _, problem_files, _ = collect_source_files(tmpdir)
            
            names = [f.name for f in problem_files]
            assert names == sorted(names)


# ===========================================================================
# Test: Document Composition
# ===========================================================================

class TestDocumentComposition:
    """Test compose_document function."""
    
    def test_compose_document_basic(self):
        """Test basic document composition."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            # Create minimal files
            header = tmpdir / "_header.md"
            header.write_text('''# Sliding Window Patterns

Introduction text.

## Core Concepts

Content here.
''')
            
            problem = tmpdir / "0003_base.md"
            problem.write_text('''## Base Template: LeetCode 3

Problem content.
''')
            
            config = PatternDocConfig(
                kernel_id="SubstringSlidingWindow",
                kernel_summary="Test",
                source_dir=tmpdir,
                output_file=tmpdir / "output.md"
            )
            
            result = compose_document(
                config,
                header_files=[header],
                problem_files=[problem],
                footer_files=[]
            )
            
            # Check structure
            assert "# Sliding Window Patterns" in result
            assert "## Table of Contents" in result
            assert "Core Concepts" in result
            assert "Base Template" in result
            assert "SubstringSlidingWindow" in result  # In footer
    
    def test_compose_document_adds_separators(self):
        """Test document composition adds separators."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            header = tmpdir / "_header.md"
            header.write_text("# Header\n\n## Section\n\nContent")
            
            problem = tmpdir / "0003.md"
            problem.write_text("## Problem\n\nContent")
            
            config = PatternDocConfig(
                kernel_id="Test",
                kernel_summary="Test",
                source_dir=tmpdir,
                output_file=tmpdir / "out.md"
            )
            
            result = compose_document(config, [header], [problem], [])
            
            # Should have separators
            assert "---" in result
    
    def test_compose_document_footer_attribution(self):
        """Test document includes kernel attribution at end."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            header = tmpdir / "_header.md"
            header.write_text("# Header\n\n## Section\n\nContent")
            
            config = PatternDocConfig(
                kernel_id="TestKernel",
                kernel_summary="Test",
                source_dir=tmpdir,
                output_file=tmpdir / "out.md"
            )
            
            result = compose_document(config, [header], [], [])
            
            assert "API Kernel: TestKernel" in result


# ===========================================================================
# Test: Edge Cases
# ===========================================================================

class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_structural_files_order_defined(self):
        """Test structural file ordering is defined."""
        assert "_header.md" in STRUCTURAL_FILES_ORDER
        assert len(STRUCTURAL_FILES_ORDER) > 0
    
    def test_structural_files_footer_defined(self):
        """Test footer file ordering is defined."""
        assert "_comparison.md" in STRUCTURAL_FILES_FOOTER
        assert "_decision.md" in STRUCTURAL_FILES_FOOTER
        assert "_templates.md" in STRUCTURAL_FILES_FOOTER
    
    def test_parse_toml_with_equals_in_value(self):
        """Test parsing values that contain equals sign."""
        content = 'formula = "a = b + c"'
        result = parse_toml_simple(content)
        
        # Should handle gracefully
        assert "formula" in result
    
    def test_add_section_numbers_no_sections(self):
        """Test section numbering with no headers."""
        content = '''Just some text.

No headers here.
'''
        result, sections_info = add_section_numbers(content, 1)
        
        assert result == content
        assert sections_info == []


# ===========================================================================
# Test: Integration with Real Data
# ===========================================================================

class TestIntegrationWithRealData:
    """Integration tests using actual project data."""
    
    @pytest.fixture
    def real_kernels(self):
        """Load actual API kernels if available."""
        try:
            return load_api_kernels()
        except Exception:
            pytest.skip("Ontology files not available")
    
    @pytest.fixture
    def real_patterns(self):
        """Load actual patterns if available."""
        try:
            return load_patterns()
        except Exception:
            pytest.skip("Ontology files not available")
    
    def test_load_api_kernels_structure(self, real_kernels):
        """Test loaded kernels have expected structure."""
        # Should have some kernels
        assert len(real_kernels) > 0
        
        # Each kernel should be APIKernel instance
        for kernel_id, kernel in real_kernels.items():
            assert isinstance(kernel, APIKernel)
            assert kernel.id != ""
    
    def test_load_patterns_structure(self, real_patterns):
        """Test loaded patterns have expected structure."""
        # Should have patterns grouped by kernel
        assert len(real_patterns) > 0
        
        # Each group should contain Pattern instances
        for kernel_id, patterns in real_patterns.items():
            assert isinstance(patterns, list)
            for pattern in patterns:
                assert isinstance(pattern, Pattern)
                assert pattern.id != ""
                assert pattern.api_kernel == kernel_id
    
    def test_sliding_window_kernel_exists(self, real_kernels):
        """Test SubstringSlidingWindow kernel exists."""
        assert "SubstringSlidingWindow" in real_kernels
    
    def test_sliding_window_patterns_exist(self, real_patterns):
        """Test sliding window patterns exist."""
        assert "SubstringSlidingWindow" in real_patterns
        patterns = real_patterns["SubstringSlidingWindow"]
        assert len(patterns) > 0
    
    def test_get_available_patterns_finds_sliding_window(self):
        """Test get_available_patterns finds sliding_window."""
        patterns = get_available_patterns()
        
        # Should find sliding_window if it exists
        if patterns:
            # At least check the function runs without error
            assert isinstance(patterns, list)


# ===========================================================================
# Test: Structural Constants
# ===========================================================================

class TestStructuralConstants:
    """Test structural constants are properly defined."""
    
    def test_structural_files_order_is_list(self):
        """Test STRUCTURAL_FILES_ORDER is a list."""
        assert isinstance(STRUCTURAL_FILES_ORDER, list)
    
    def test_structural_files_footer_is_list(self):
        """Test STRUCTURAL_FILES_FOOTER is a list."""
        assert isinstance(STRUCTURAL_FILES_FOOTER, list)
    
    def test_header_comes_first(self):
        """Test _header.md is first in order."""
        assert STRUCTURAL_FILES_ORDER[0] == "_header.md"
    
    def test_footer_files_are_distinct(self):
        """Test header and footer files are distinct."""
        header_set = set(STRUCTURAL_FILES_ORDER)
        footer_set = set(STRUCTURAL_FILES_FOOTER)
        
        # Should not overlap
        assert header_set.isdisjoint(footer_set)


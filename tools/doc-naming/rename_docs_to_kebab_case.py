#!/usr/bin/env python3
"""
Documentation Filename Standardization Tool

Renames all documentation files (except README, index, and _-prefixed files)
to kebab-case naming convention, and updates all references.

Based on: docs/contributors/documentation-naming.md

Usage:
    # Generate mapping table for review
    python tools/rename_docs_to_kebab_case.py --dry-run

    # Execute full migration
    python tools/rename_docs_to_kebab_case.py

    # Verify after migration
    python tools/rename_docs_to_kebab_case.py --verify-only
"""

import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
import json


class DocRenamer:
    """Main class for documentation file renaming."""

    # Files to exclude from renaming
    EXCLUDED_NAMES = {
        'README.md',
        'README_zh-TW.md',
    }

    # Special file name mappings (manual overrides)
    # Note: All paths use forward slashes for cross-platform compatibility
    SPECIAL_MAPPINGS = {
        'tools/ai-markmap-agent/prompts/writer/writer_behavior - 預備.md': 
            'tools/ai-markmap-agent/prompts/writer/writer-behavior-delete.md',
    }

    def __init__(self, dry_run: bool = False, verify_only: bool = False):
        self.dry_run = dry_run
        self.verify_only = verify_only
        self.mapping: Dict[str, str] = {}
        self.updated_files: Set[str] = set()

    def should_rename(self, filepath: str) -> bool:
        """Check if a file should be renamed based on exclusion rules."""
        path = Path(filepath)
        name = path.name

        # Exclude README variants
        if name in self.EXCLUDED_NAMES:
            return False

        # Exclude index files
        if name.startswith('index') and name.endswith('.md'):
            return False

        # Exclude files starting with underscore
        if name.startswith('_'):
            return False

        return True

    def to_kebab_case(self, filename: str) -> str:
        """Convert filename to kebab-case."""
        # Remove .md extension
        if filename.endswith('.md'):
            name = filename[:-3]
            ext = '.md'
        else:
            name = filename
            ext = ''

        # Step 1: Replace underscores and spaces with hyphens
        name = re.sub(r'[_\s]+', '-', name)

        # Step 2: Handle CamelCase - insert hyphen before uppercase letters
        # But be smart about it: don't break up consecutive uppercase letters
        # (e.g., "ACT" should stay together, but "ActLocal" -> "act-local")
        
        # First, handle sequences of uppercase letters followed by lowercase
        # e.g., "ACTLocal" -> "ACT-Local"
        name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1-\2', name)
        
        # Then insert hyphens before uppercase letters that follow lowercase
        # e.g., "actLocal" -> "act-Local"
        name = re.sub(r'([a-z\d])([A-Z])', r'\1-\2', name)
        
        # Also handle uppercase followed by lowercase (start of word)
        # e.g., "LocalGitHub" -> "Local-GitHub" (will be handled by previous rule)

        # Step 3: Convert to lowercase
        name = name.lower()

        # Step 4: Handle version suffixes: v2, v3, v4 (already lowercase)
        # These should already be handled correctly

        # Step 5: Remove multiple consecutive hyphens
        name = re.sub(r'-+', '-', name)

        # Step 6: Remove leading/trailing hyphens
        name = name.strip('-')

        # Reattach extension
        return f"{name}{ext}" if ext else name

    def get_all_md_files(self) -> List[str]:
        """Get all .md files tracked by git."""
        try:
            result = subprocess.run(
                ['git', 'ls-files', '*.md'],
                capture_output=True,
                text=True,
                check=True
            )
            files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
            return files
        except subprocess.CalledProcessError as e:
            print(f"❌ Error getting file list: {e.stderr.decode()}")
            sys.exit(1)

    def create_rename_mapping(self) -> Dict[str, str]:
        """Create mapping of old filepath -> new filepath."""
        files = self.get_all_md_files()
        mapping = {}
        new_paths_seen = {}  # Track new_path -> old_path for collision detection

        for filepath in files:
            # Normalize filepath to use forward slashes
            filepath = filepath.replace('\\', '/')
            
            # Check special mappings first
            if filepath in self.SPECIAL_MAPPINGS:
                new_path = self.SPECIAL_MAPPINGS[filepath].replace('\\', '/')
                if filepath != new_path:
                    # Check for collision
                    if new_path in new_paths_seen:
                        print(f"  WARNING: Collision detected!")
                        print(f"    {filepath}")
                        print(f"    {new_paths_seen[new_path]}")
                        print(f"    Both map to: {new_path}")
                        continue
                    mapping[filepath] = new_path
                    new_paths_seen[new_path] = filepath
                continue

            # Check if should rename
            if not self.should_rename(filepath):
                continue

            path = Path(filepath)
            old_name = path.name
            new_name = self.to_kebab_case(old_name)

            # Only add to mapping if name actually changes
            if old_name != new_name:
                # Use as_posix() to ensure forward slashes (cross-platform)
                new_path = (path.parent / new_name).as_posix()
                
                # Check for collision: same new_path from different old_path
                if new_path in new_paths_seen:
                    print(f"  WARNING: Collision detected!")
                    print(f"    {filepath}")
                    print(f"    {new_paths_seen[new_path]}")
                    print(f"    Both map to: {new_path}")
                    continue
                
                # Check if target already exists (and it's not the same file)
                if Path(new_path).exists() and Path(new_path).resolve() != Path(filepath).resolve():
                    print(f"  WARNING: Target path already exists: {new_path}")
                    print(f"    Source: {filepath}")
                    continue
                
                mapping[filepath] = new_path
                new_paths_seen[new_path] = filepath

        return mapping

    def save_mapping(self, mapping: Dict[str, str], filename: str = 'rename_mapping.json'):
        """Save mapping to JSON file for review."""
        # Also create a human-readable text version
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, indent=2, ensure_ascii=False)

        txt_filename = filename.replace('.json', '.txt')
        with open(txt_filename, 'w', encoding='utf-8') as f:
            f.write("# Documentation Filename Rename Mapping\n\n")
            f.write(f"Total files to rename: {len(mapping)}\n\n")
            f.write("| Old Path | New Path |\n")
            f.write("|----------|----------|\n")
            for old, new in sorted(mapping.items()):
                f.write(f"| `{old}` | `{new}` |\n")

        print(f"Mapping saved to:")
        print(f"   - {filename} (JSON)")
        print(f"   - {txt_filename} (Markdown table)")

    def rename_files(self, mapping: Dict[str, str]) -> int:
        """Rename files using git mv."""
        if self.dry_run:
            print("DRY RUN MODE - No files will be renamed")
            return 0

        print(f"\nRenaming {len(mapping)} files using git mv...\n")
        success_count = 0

        for old_path, new_path in sorted(mapping.items()):
            try:
                # Ensure paths use forward slashes for git mv (git handles this cross-platform)
                # Convert to forward slashes for git command
                old_path_git = old_path.replace('\\', '/')
                new_path_git = new_path.replace('\\', '/')
                
                result = subprocess.run(
                    ['git', 'mv', old_path_git, new_path_git],
                    check=True,
                    capture_output=True
                )
                print(f"OK: {old_path_git}")
                print(f"   -> {new_path_git}")
                success_count += 1
            except subprocess.CalledProcessError as e:
                error_msg = e.stderr.decode() if e.stderr else str(e)
                print(f"ERROR: Renaming {old_path}: {error_msg}")
                # Continue with other files

        print(f"\nSuccessfully renamed {success_count}/{len(mapping)} files")
        return success_count

    def find_references(self, old_name: str, old_path: str) -> List[Tuple[str, int, str]]:
        """Find all references to old filename in the repository."""
        references = []

        # Search patterns
        patterns = [
            old_name,  # Just filename
            old_path,  # Full path
            Path(old_path).name,  # Basename
        ]

        # Get all files that might contain references
        search_extensions = ['.md', '.yml', '.yaml', '.py', '.txt', '.json', '.toml']
        files_to_search = []
        for ext in search_extensions:
            try:
                result = subprocess.run(
                    ['git', 'ls-files', f'*{ext}'],
                    capture_output=True,
                    text=True,
                    check=True
                )
                files_to_search.extend(result.stdout.strip().split('\n'))
            except subprocess.CalledProcessError:
                continue

        files_to_search = [f for f in files_to_search if f.strip()]

        for filepath in files_to_search:
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    for line_num, line in enumerate(lines, 1):
                        for pattern in patterns:
                            if pattern in line:
                                references.append((filepath, line_num, line.strip()))
                                break
            except Exception:
                continue

        return references

    def update_references(self, mapping: Dict[str, str]) -> int:
        """Update all references to renamed files."""
        if self.dry_run:
            print("\nDRY RUN MODE - References will not be updated")
            return 0

        print(f"\nStep 3: Updating references to {len(mapping)} renamed files...")

        # Create reverse mappings for efficient lookup
        filename_mapping = {}  # old_filename -> new_filename
        path_mapping = {}      # old_path -> new_path

        for old_path, new_path in mapping.items():
            # Normalize all paths to use forward slashes
            old_path_norm = old_path.replace('\\', '/')
            new_path_norm = new_path.replace('\\', '/')
            
            old_name = Path(old_path_norm).name
            new_name = Path(new_path_norm).name
            filename_mapping[old_name] = new_name
            path_mapping[old_path_norm] = new_path_norm
            # Also map relative paths
            path_mapping[f"./{old_path_norm}"] = f"./{new_path_norm}"
            # Map Windows-style paths too (for compatibility)
            path_mapping[old_path_norm.replace('/', '\\')] = new_path_norm.replace('/', '\\')

        # Get all files that might contain references
        search_extensions = ['.md', '.yml', '.yaml', '.py', '.txt', '.json', '.toml']
        files_to_check = []
        for ext in search_extensions:
            try:
                result = subprocess.run(
                    ['git', 'ls-files', f'*{ext}'],
                    capture_output=True,
                    text=True,
                    check=True
                )
                files_to_check.extend(result.stdout.strip().split('\n'))
            except subprocess.CalledProcessError:
                continue

        files_to_check = [f for f in files_to_check if f.strip()]

        updated_count = 0
        for filepath in files_to_check:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                original_content = content

                # Strategy 1: Replace full paths (exact match)
                for old_path, new_path in path_mapping.items():
                    content = content.replace(old_path, new_path)

                # Strategy 2: Replace relative paths (directory + filename)
                # This handles:
                # - YAML configs: "contributors/VSCODE_SETUP.md"
                # - Markdown text: "../docs/SOLUTION_CONTRACT.md"
                # - Code comments: "See docs/SOLUTION_CONTRACT.md"
                for old_path, new_path in mapping.items():
                    old_name = Path(old_path).name
                    new_name = Path(new_path).name
                    old_dir = str(Path(old_path).parent)
                    new_dir = str(Path(new_path).parent)
                    
                    if old_dir != '.':
                        # Build relative path variants
                        old_rel_path_slash = f"{old_dir}/{old_name}"
                        new_rel_path_slash = f"{new_dir}/{new_name}"
                        old_rel_path_back = f"{old_dir}\\{old_name}"
                        new_rel_path_back = f"{new_dir}\\{new_name}"
                        
                        # Variant 1: YAML format (unquoted, after colon)
                        # Format: "  - Title: dir/old_name" or "  - Title: dir\\old_name"
                        # Use string replacement for YAML to avoid regex escape issues
                        pattern1 = f'  - {old_rel_path_slash}'
                        replacement1 = f'  - {new_rel_path_slash}'
                        content = content.replace(pattern1, replacement1)
                        
                        # Also handle with title format
                        yaml_pattern = re.compile(
                            r'(\s+[-\w\s]+:\s+)' + re.escape(old_rel_path_slash) + r'(\s|$)',
                            re.MULTILINE
                        )
                        content = yaml_pattern.sub(r'\1' + new_rel_path_slash + r'\2', content)
                        
                        yaml_pattern2 = re.compile(
                            r'(\s+[-\w\s]+:\s+)' + re.escape(old_rel_path_back) + r'(\s|$)',
                            re.MULTILINE
                        )
                        content = yaml_pattern2.sub(r'\1' + new_rel_path_back + r'\2', content)
                        
                        # Variant 2: Markdown/Text format (with ../ prefix)
                        # Format: "../docs/SOLUTION_CONTRACT.md" or "../docs\\SOLUTION_CONTRACT.md"
                        old_rel_path_up = f"../{old_rel_path_slash}"
                        new_rel_path_up = f"../{new_rel_path_slash}"
                        # Use compiled regex to avoid escape issues
                        up_pattern = re.compile(
                            re.escape(old_rel_path_up) + r'(#.*?)?(\s|\)|"|\'|$)',
                            re.MULTILINE
                        )
                        content = up_pattern.sub(new_rel_path_up + r'\1\2', content)
                        
                        # Variant 3: Direct relative path (without quotes, in text)
                        # Format: "docs/SOLUTION_CONTRACT.md" or "contributors/VSCODE_SETUP.md"
                        # Use string replacement instead of regex to avoid escape issues
                        content = content.replace(old_rel_path_slash, new_rel_path_slash)

                # Strategy 3: Replace in Markdown links: [text](path/to/file.md)
                # This handles various markdown link formats:
                # - [text](path/to/old_name)
                # - [text](old_name)
                # - [text](../path/to/old_name)
                # - [text](path/to/old_name#anchor)
                for old_name, new_name in filename_mapping.items():
                    # Use compiled regex to avoid escape issues
                    # Match markdown link format: [text](path/to/old_name) or [text](../path/to/old_name)
                    link_pattern1 = re.compile(
                        r'(\[.*?\]\([^)]*/)' + re.escape(old_name) + r'(#.*?)?(\))',
                        re.MULTILINE
                    )
                    content = link_pattern1.sub(r'\1' + new_name + r'\2\3', content)
                    
                    # Match: [text](old_name) or [text](old_name#anchor)
                    link_pattern2 = re.compile(
                        r'(\[.*?\]\()' + re.escape(old_name) + r'(#.*?)?(\))',
                        re.MULTILINE
                    )
                    content = link_pattern2.sub(r'\1' + new_name + r'\2\3', content)
                    
                    # Match relative paths: [text](../old_name) or [text](../path/old_name)
                    link_pattern3 = re.compile(
                        r'(\[.*?\]\(\.\./[^)]*/)' + re.escape(old_name) + r'(#.*?)?(\))',
                        re.MULTILINE
                    )
                    content = link_pattern3.sub(r'\1' + new_name + r'\2\3', content)
                    
                    # Match: [text](../old_name) (direct relative)
                    link_pattern4 = re.compile(
                        r'(\[.*?\]\(\.\./)' + re.escape(old_name) + r'(#.*?)?(\))',
                        re.MULTILINE
                    )
                    content = link_pattern4.sub(r'\1' + new_name + r'\2\3', content)

                # Strategy 4: Replace in Python string literals (all types)
                # This handles:
                # - Single quotes: 'docs/SOLUTION_CONTRACT.md'
                # - Double quotes: "docs/SOLUTION_CONTRACT.md"
                # - Triple quotes: """docs/SOLUTION_CONTRACT.md"""
                # - f-strings: f"See {path}/SOLUTION_CONTRACT.md"
                # - Raw strings: r"docs/SOLUTION_CONTRACT.md"
                for old_name, new_name in filename_mapping.items():
                    # Use compiled regex to avoid escape issues
                    escaped_old = re.escape(old_name)
                    
                    # Pattern 1: Single or double quoted strings
                    # Match: "path/to/old_name" or 'path/to/old_name'
                    str_pattern1 = re.compile(
                        r'(["\'])([^"\']*/)?' + escaped_old + r'\1',
                        re.MULTILINE
                    )
                    content = str_pattern1.sub(r'\1\2' + new_name + r'\1', content)
                    
                    # Pattern 2: Triple-quoted strings (multiline)
                    # Match: """path/to/old_name""" or '''path/to/old_name'''
                    str_pattern2 = re.compile(
                        r'("""|\'\'\')([^"\']*/)?' + escaped_old + r'\1',
                        re.MULTILINE | re.DOTALL
                    )
                    content = str_pattern2.sub(r'\1\2' + new_name + r'\1', content)
                    
                    # Pattern 3: f-strings (formatted string literals)
                    # Match: f"path/to/old_name" or f'path/to/old_name'
                    str_pattern3 = re.compile(
                        r'(f["\'])([^"\']*/)?' + escaped_old + r'\1',
                        re.MULTILINE
                    )
                    content = str_pattern3.sub(r'\1\2' + new_name + r'\1', content)
                    # Also handle f-strings with expressions: f"See {var}/old_name"
                    str_pattern3b = re.compile(
                        r'(f["\'][^"\']*?/)' + escaped_old + r'(["\'])',
                        re.MULTILINE
                    )
                    content = str_pattern3b.sub(r'\1' + new_name + r'\2', content)
                    
                    # Pattern 4: Raw strings
                    # Match: r"path/to/old_name" or r'path/to/old_name'
                    str_pattern4 = re.compile(
                        r'(r["\'])([^"\']*/)?' + escaped_old + r'\1',
                        re.MULTILINE
                    )
                    content = str_pattern4.sub(r'\1\2' + new_name + r'\1', content)
                    
                    # Pattern 5: Comments (Python # comments)
                    # Match: # See docs/SOLUTION_CONTRACT.md
                    comment_pattern1 = re.compile(
                        r'(#\s*[^#\n]*?/)' + escaped_old + r'(\s|$)',
                        re.MULTILINE
                    )
                    content = comment_pattern1.sub(r'\1' + new_name + r'\2', content)
                    comment_pattern2 = re.compile(
                        r'(#\s*[^#\n]*?)' + escaped_old + r'(\s|$)',
                        re.MULTILINE
                    )
                    content = comment_pattern2.sub(r'\1' + new_name + r'\2', content)

                # Strategy 5: Replace standalone filenames in YAML (unquoted, after colon)
                # This handles cases like: "  - Title: SOLUTION_CONTRACT.md"
                for old_name, new_name in filename_mapping.items():
                    # Match YAML format: "  - Title: old_name" (standalone filename)
                    content = re.sub(
                        rf'(\s+[-\w\s]+:\s+){re.escape(old_name)}(\s|$)',
                        rf'\1{new_name}\2',
                        content
                    )

                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    updated_count += 1
                    self.updated_files.add(filepath)
                    print(f"  OK: Updated {filepath}")

            except Exception as e:
                print(f"  WARNING: Could not process {filepath}: {e}")

        print(f"\n  Updated references in {updated_count} files")
        return updated_count

    def verify_old_references(self, mapping: Dict[str, str]) -> bool:
        """Verify that no old filenames remain in the repository."""
        print("\nStep 4: Verifying no old filenames remain...")

        all_clean = True
        for old_path in mapping.keys():
            old_name = Path(old_path).name

            try:
                result = subprocess.run(
                    ['git', 'grep', '-l', old_name],
                    capture_output=True,
                    text=True
                )
                if result.stdout.strip():
                    files = result.stdout.strip().split('\n')
                    print(f"  WARNING: Found references to '{old_name}' in:")
                    for f in files:
                        print(f"     - {f}")
                    all_clean = False
            except subprocess.CalledProcessError:
                # git grep returns non-zero if no matches found (which is good)
                pass

        if all_clean:
            print("  OK: No old filenames found in repository")
        else:
            print("  ERROR: Some old filenames still referenced!")

        return all_clean

    def verify_mkdocs_build(self) -> bool:
        """Verify MkDocs build succeeds."""
        print("\nStep 5: Verifying MkDocs build...")

        try:
            result = subprocess.run(
                ['mkdocs', 'build', '--strict'],
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0:
                print("  OK: MkDocs build successful")
                return True
            else:
                print("  ERROR: MkDocs build failed:")
                print(result.stderr)
                return False
        except subprocess.TimeoutExpired:
            print("  WARNING: MkDocs build timed out")
            return False
        except FileNotFoundError:
            print("  WARNING: MkDocs not found, skipping build verification")
            return True
        except Exception as e:
            print(f"  WARNING: Error running MkDocs: {e}")
            return False

    def generate_report(self, mapping: Dict[str, str], renamed_count: int, 
                       updated_count: int, verify_clean: bool, build_ok: bool):
        """Generate a summary report."""
        print("\n" + "="*70)
        print("MIGRATION SUMMARY REPORT")
        print("="*70)
        print(f"Total files in mapping: {len(mapping)}")
        print(f"Files renamed: {renamed_count}")
        print(f"Files with updated references: {updated_count}")
        print(f"Old references cleaned: {'OK' if verify_clean else 'FAILED'}")
        print(f"MkDocs build: {'OK' if build_ok else 'FAILED'}")
        print("="*70)

        if self.dry_run:
            print("\nThis was a dry run. To execute, run without --dry-run flag.")
        else:
            print("\nMigration completed!")
            print("\nNext steps:")
            print("   1. Review changes: git status")
            print("   2. Review diff: git diff")
            print("   3. Test documentation: mkdocs serve")
            print("   4. Commit changes when ready")

    def run(self):
        """Main execution flow."""
        print("Step 1: Scanning files and creating rename mapping...")
        self.mapping = self.create_rename_mapping()

        if not self.mapping:
            print("OK: No files need renaming (all already in kebab-case)")
            return

        print(f"\nFound {len(self.mapping)} files to rename:\n")
        for old, new in sorted(list(self.mapping.items())[:10]):  # Show first 10
            print(f"  {old}")
            print(f"  -> {new}\n")
        if len(self.mapping) > 10:
            print(f"  ... and {len(self.mapping) - 10} more files\n")

        # Save mapping
        self.save_mapping(self.mapping)

        if self.verify_only:
            print("\nVERIFY-ONLY MODE")
            verify_clean = self.verify_old_references(self.mapping)
            build_ok = self.verify_mkdocs_build()
            self.generate_report(self.mapping, 0, 0, verify_clean, build_ok)
            return

        if self.dry_run:
            print("\nThis is a dry run. Files will not be renamed.")
            print("Run without --dry-run to execute the migration.")
            return

        # Step 2: Rename files
        renamed_count = self.rename_files(self.mapping)

        # Step 3: Update references
        updated_count = self.update_references(self.mapping)

        # Step 4: Verify
        verify_clean = self.verify_old_references(self.mapping)
        build_ok = self.verify_mkdocs_build()

        # Generate report
        self.generate_report(self.mapping, renamed_count, updated_count, verify_clean, build_ok)


def main():
    """Entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Rename documentation files to kebab-case and update references'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Generate mapping table but do not rename files'
    )
    parser.add_argument(
        '--verify-only',
        action='store_true',
        help='Only verify that no old filenames remain (after migration)'
    )

    args = parser.parse_args()

    if args.dry_run and args.verify_only:
        print("ERROR: Cannot use --dry-run and --verify-only together")
        sys.exit(1)

    renamer = DocRenamer(dry_run=args.dry_run, verify_only=args.verify_only)
    renamer.run()


if __name__ == '__main__':
    main()


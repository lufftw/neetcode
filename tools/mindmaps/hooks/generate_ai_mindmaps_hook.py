#!/usr/bin/env python3
"""
Pre-commit hook for generating AI mind maps.

Only runs when:
1. Files in ontology/, meta/problems/, or tools/generate_mindmaps.py are modified
2. Not skipped via [skip-ai] in commit message or SKIP_AI_MINDMAPS env var

API Key: Interactive input (not stored)
"""

import os
import subprocess
import sys
from pathlib import Path

# Project root (assuming hook is in tools/hooks/)
PROJECT_ROOT = Path(__file__).parent.parent.parent
TOOLS_DIR = PROJECT_ROOT / 'tools'


def get_current_branch() -> str:
    """Get current Git branch name."""
    result = subprocess.run(
        ['git', 'branch', '--show-current'],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT
    )
    if result.returncode != 0:
        return ''
    return result.stdout.strip()


def check_changed_files() -> bool:
    """Check if relevant files were changed in staged area."""
    result = subprocess.run(
        ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT
    )
    
    if result.returncode != 0:
        return False
    
    changed_files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
    
    # Check if any relevant file was changed
    relevant_patterns = [
        'ontology/',
        'meta/problems/',
        'tools/mindmaps/generate_mindmaps.py'
    ]
    
    for file in changed_files:
        for pattern in relevant_patterns:
            if file.startswith(pattern) or file == pattern:
                return True
    
    return False


def should_skip() -> bool:
    """Check if AI generation should be skipped."""
    # Check environment variable
    if os.environ.get('SKIP_AI_MINDMAPS', '').lower() in ('true', '1', 'yes'):
        return True
    
    # Check commit message (from .git/COMMIT_EDITMSG)
    commit_msg_file = PROJECT_ROOT / '.git' / 'COMMIT_EDITMSG'
    if commit_msg_file.exists():
        try:
            commit_msg = commit_msg_file.read_text(encoding='utf-8')
            if '[skip-ai]' in commit_msg or '[no-ai]' in commit_msg:
                return True
        except Exception:
            pass
    
    return False


def main() -> int:
    """Main hook function."""
    # Check if should skip
    if should_skip():
        print("ℹ️  AI mind map generation skipped (via [skip-ai] or SKIP_AI_MINDMAPS).")
        return 0
    
    # Check if relevant files changed
    if not check_changed_files():
        print("ℹ️  No relevant files changed (ontology/, meta/problems/, tools/generate_mindmaps.py).")
        print("   Skipping AI mind map generation.")
        return 0
    
    # Get current branch for display
    current_branch = get_current_branch()
    
    # Show what triggered the hook
    print("=" * 70)
    print("🔍 Pre-commit Hook: AI Mind Map Generation")
    print("=" * 70)
    print(f"📍 Branch: {current_branch}")
    print("📝 Detected changes in:")
    print("   - ontology/")
    print("   - meta/problems/")
    print("   - tools/mindmaps/generate_mindmaps.py")
    print("")
    print("🤖 Running AI mind map generation...")
    print("")
    
    # Check for API key
    if not os.environ.get('OPENAI_API_KEY'):
        print("⚠️  OPENAI_API_KEY not set in environment")
        print("💡 The script will prompt you to enter the API key interactively.")
        print("   (API key will NOT be stored)")
        print("")
    
    # Run the AI mind map generator
    script_path = TOOLS_DIR / 'mindmaps' / 'generate_mindmaps_ai.py'
    
    if not script_path.exists():
        print(f"❌ Error: Script not found: {script_path}")
        return 1
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path), '--goal', 'creative'],
            cwd=PROJECT_ROOT,
            # Don't capture output so user can see progress and enter API key
        )
        
        if result.returncode == 0:
            print("")
            print("=" * 70)
            print("✅ AI mind map generation completed successfully!")
            print("=" * 70)
            return 0
        else:
            print("")
            print("=" * 70)
            print("❌ AI mind map generation failed!")
            print("=" * 70)
            print("")
            print("💡 Options:")
            print("   1. Fix the error and commit again")
            print("   2. Skip this hook: git commit --no-verify")
            print("   3. Skip with message: git commit -m 'message [skip-ai]'")
            print("   4. Skip with env var: SKIP_AI_MINDMAPS=true git commit")
            return 1
            
    except KeyboardInterrupt:
        print("")
        print("⚠️  Interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Error running AI mind map generator: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())



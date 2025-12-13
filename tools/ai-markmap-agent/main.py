#!/usr/bin/env python3
# =============================================================================
# AI Markmap Agent - Main Entry Point
# =============================================================================
# Usage:
#   python main.py                    # Run pipeline
#   python main.py --config path/to/config.yaml
#   python main.py --no-openai        # Skip OpenAI API key request
#   python main.py --dry-run          # Load data but don't run pipeline
#
# API keys are requested at runtime and NEVER stored.
# They exist only in memory and are cleared when the program exits.
# =============================================================================

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config_loader import (
    ConfigLoader,
    load_config,
    request_api_keys,
    get_api_key,
)
from src.data_sources import DataSourcesLoader, load_data_sources
from src.graph import run_pipeline, build_markmap_graph


def print_banner() -> None:
    """Print application banner."""
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                         AI Markmap Agent                                  ║
║                                                                           ║
║  Multi-Agent Collaborative System for Markmap Generation                  ║
║                                                                           ║
║  Features:                                                                ║
║    • Structure Specification (YAML) based workflow                        ║
║    • Content Strategists discuss concepts, not formatting                 ║
║    • Writer is the ONLY agent producing final Markdown                    ║
║                                                                           ║
║  Outputs:                                                                 ║
║    • neetcode_general_ai_en.md / .html                                    ║
║    • neetcode_general_ai_zh-TW.md / .html                                 ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """)


def print_data_summary(summary: dict) -> None:
    """Print summary of loaded data sources."""
    print("\n" + "=" * 60)
    print("Data Sources Summary")
    print("=" * 60)
    
    for source_name, info in summary.items():
        status = "✓ Enabled" if info.get("enabled") else "✗ Disabled"
        count = info.get("loaded_count", 0)
        print(f"\n{source_name.upper()}:")
        print(f"  Status: {status}")
        print(f"  Loaded: {count} items")
        if "items" in info and info["items"]:
            items_str = ", ".join(info["items"][:5])
            if len(info["items"]) > 5:
                items_str += f"... (+{len(info['items']) - 5} more)"
            print(f"  Items: {items_str}")
    
    print("\n" + "=" * 60)


def print_workflow_summary(config: dict) -> None:
    """Print workflow configuration summary."""
    workflow = config.get("workflow", {})
    naming = config.get("output", {}).get("naming", {})
    
    print("\n" + "=" * 60)
    print("Workflow Configuration")
    print("=" * 60)
    print(f"  Optimization rounds: {workflow.get('optimization_rounds', 3)}")
    print(f"  Optimizer count: {workflow.get('optimizer_count', 3)}")
    print(f"  Judge count: {workflow.get('judge_count', 2)}")
    print(f"  Enable debate: {workflow.get('enable_debate', False)}")
    print(f"\n  Languages: {', '.join(naming.get('languages', ['en', 'zh-TW']))}")
    print(f"  Types: {', '.join(naming.get('types', {}).keys())}")
    print("=" * 60)


def main() -> int:
    """
    Main entry point.
    
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="AI Markmap Agent - Multi-Agent Markmap Generation System"
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to configuration file (default: config/config.yaml)"
    )
    parser.add_argument(
        "--no-openai",
        action="store_true",
        help="Skip OpenAI API key request"
    )
    parser.add_argument(
        "--no-anthropic",
        action="store_true",
        help="Skip Anthropic API key request"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Load data sources but don't run the agent pipeline"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    try:
        # Print banner
        print_banner()
        
        # Step 1: Load configuration
        print("Loading configuration...")
        config = load_config(args.config)
        print("  ✓ Configuration loaded\n")
        
        # Print workflow summary
        print_workflow_summary(config)
        
        # Step 2: Request API keys at runtime (NOT STORED)
        providers = []
        if not args.no_openai:
            providers.append("openai")
        if not args.no_anthropic:
            providers.append("anthropic")
        
        if providers:
            request_api_keys(providers)
        else:
            print("Skipping API key input (--no-openai and/or --no-anthropic specified)\n")
        
        # Step 3: Load data sources
        print("\nLoading data sources...")
        loader = DataSourcesLoader(config)
        data = loader.load_all()
        
        # Print summary
        print_data_summary(loader.get_summary())
        
        # Step 4: If dry-run, stop here
        if args.dry_run:
            print("\n[DRY RUN] Data sources loaded successfully. Exiting.")
            return 0
        
        # Step 5: Check required API keys
        if not args.no_openai and not ConfigLoader.has_api_key("openai"):
            print("\n❌ Error: OpenAI API key is required but not provided.")
            print("   Use --no-openai to skip if not needed.")
            return 1
        
        # Step 6: Build and run the LangGraph pipeline
        print("\n" + "=" * 60)
        print("Starting Markmap Generation Pipeline")
        print("=" * 60)
        
        print("\n📋 Workflow:")
        print("  1. Generate Structure Specifications (Planners)")
        print("  2. Optimize content strategy (Strategists + Integrator)")
        print("  3. Evaluate structure quality (Evaluators)")
        print("  4. Render final Markmap (Writer)")
        print("  5. Translate if needed")
        print("  6. Post-process and save")
        result = run_pipeline(data, config)
        
        # Report results
        print("\n" + "=" * 60)
        print("Pipeline Complete")
        print("=" * 60)
        
        if result.get("errors"):
            print("\n⚠ Warnings/Errors:")
            for error in result["errors"]:
                print(f"  - {error}")
        
        if result.get("final_outputs"):
            print(f"\n✓ Generated {len(result['final_outputs'])} Markmap outputs")
            
            # Print output locations
            output_config = config.get("output", {}).get("final_dirs", {})
            print(f"\n  Markdown files: {output_config.get('markdown', 'outputs/final')}")
            print(f"  HTML files: {output_config.get('html', 'outputs/final')}")
        else:
            print("\n⚠ No outputs generated")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user.")
        return 130
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1
    finally:
        # Ensure API keys are cleared (also registered with atexit)
        ConfigLoader.clear_api_keys()
        print("\n🔒 API keys cleared from memory.")


if __name__ == "__main__":
    sys.exit(main())

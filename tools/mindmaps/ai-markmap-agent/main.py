#!/usr/bin/env python3
# =============================================================================
# AI Markmap Agent - Main Entry Point
# =============================================================================
# Refinement Mode: Start from a high-quality baseline Markmap and improve it
# through multi-expert review and consensus-based discussion.
#
# Usage:
#   python main.py                    # Run refinement pipeline
#   python main.py --config path/to/config.yaml
#   python main.py --baseline path/to/markmap.md
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

# Add local src to path for agent-specific imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config_loader import (
    ConfigLoader,
    load_config,
    request_api_keys,
)
from src.data_sources import DataSourcesLoader
from src.graph import run_pipeline, load_baseline_markmap, handle_versioning_mode
from src.resume import (
    scan_previous_runs,
    select_run_interactive,
    ask_reuse_stage,
    RunInfo,
)


def print_banner() -> None:
    """Print application banner."""
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                         AI Markmap Agent                                  ║
║                                                                           ║
║  Multi-Expert Refinement System for Markmap Improvement                   ║
║                                                                           ║
║  Workflow:                                                                ║
║    1. Load baseline Markmap                                               ║
║    2. Expert Review (Round 1) - Independent suggestions                   ║
║    3. Full Discussion (Round 2) - Vote on all suggestions                 ║
║    4. Consensus Calculation - Majority voting (code, not AI)              ║
║    5. Writer - Apply adopted improvements                                 ║
║    6. Post-processing and translation                                     ║
║                                                                           ║
║  API Calls: 2N + 1 (N = number of experts, typically 3)                   ║
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
    experts = config.get("experts", {})
    naming = config.get("output", {}).get("naming", {})
    
    enabled_experts = experts.get("enabled", ["architect", "professor", "engineer"])
    definitions = experts.get("definitions", {})
    
    print("\n" + "=" * 60)
    print("Refinement Configuration")
    print("=" * 60)
    print(f"\n  Experts ({len(enabled_experts)}):")
    for expert_id in enabled_experts:
        expert_def = definitions.get(expert_id, {})
        emoji = expert_def.get("emoji", "•")
        name = expert_def.get("name", expert_id)
        print(f"    {emoji} {name}")
    
    print(f"\n  Discussion rounds: {workflow.get('discussion_rounds', 2)}")
    print(f"  Consensus threshold: {workflow.get('consensus_threshold', 0.67):.0%}")
    
    # Calculate API calls
    n_experts = len(enabled_experts)
    api_calls = 2 * n_experts + 1
    print(f"  API calls: {api_calls} (2×{n_experts} + 1)")
    
    print(f"\n  Languages: {', '.join(naming.get('languages', {}).keys())}")
    print("=" * 60)


def main() -> int:
    """
    Main entry point.
    
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="AI Markmap Agent - Multi-Expert Refinement System"
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to configuration file (default: config/config.yaml)"
    )
    parser.add_argument(
        "--baseline",
        type=str,
        default=None,
        help="Path to baseline Markmap file (overrides config)"
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
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from a previous run (interactive mode)"
    )
    parser.add_argument(
        "--from-stage",
        type=str,
        choices=["expert_review", "full_discussion", "consensus", "writer", "translate", "post_process"],
        help="Start from a specific stage (requires --resume)"
    )
    
    args = parser.parse_args()
    
    try:
        # Print banner
        print_banner()
        
        # Step 1: Load configuration
        print("Loading configuration...")
        config = load_config(args.config)
        print("  ✓ Configuration loaded\n")
        
        # Step 1.5: Resume mode selection
        resume_config = None
        if args.resume or args.from_stage:
            print("\n" + "=" * 60)
            print("Resume Mode")
            print("=" * 60)
            
            # Scan for previous runs
            debug_config = config.get("debug_output", {})
            debug_output_dir = Path(debug_config.get("output_dir", "outputs/debug"))
            runs = scan_previous_runs(debug_output_dir)
            
            if not runs:
                print("\n  ⚠ No previous runs found")
                if args.resume:
                    print("  Starting fresh run instead...\n")
                else:
                    return 1
            else:
                # Let user select a run
                selected_run = select_run_interactive(runs)
                if not selected_run:
                    print("\n  ⚠ Cancelled")
                    return 0
                
                print(f"\n  ✓ Selected: {selected_run.run_id}")
                
                # Determine which stages to reuse
                reuse_stages = {}
                stages = ["expert_review", "full_discussion", "consensus", "writer", "translation", "post_processing"]
                
                # If --from-stage is specified, reuse everything before that stage
                if args.from_stage:
                    # Map CLI stage names to internal stage names
                    stage_map = {
                        "translate": "translation",
                        "post_process": "post_processing",
                    }
                    internal_stage = stage_map.get(args.from_stage, args.from_stage)
                    stage_idx = stages.index(internal_stage) if internal_stage in stages else -1
                    if stage_idx >= 0:
                        for i in range(stage_idx):
                            if selected_run.has_stage_output(stages[i]):
                                reuse_stages[stages[i]] = True
                        print(f"  → Will start from stage: {args.from_stage}")
                        if reuse_stages:
                            print(f"  → Will reuse stages: {', '.join(reuse_stages.keys())}")
                else:
                    # Interactive: ask for each stage
                    print("\n  Select which stages to reuse:")
                    for stage in stages:
                        if selected_run.has_stage_output(stage):
                            should_reuse = ask_reuse_stage(stage, selected_run)
                            reuse_stages[stage] = should_reuse
                
                resume_config = {
                    "run_dir": str(selected_run.run_dir),
                    "reuse_stages": reuse_stages,
                }
        
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
        
        # Step 3: Handle versioning mode (reset prompts here)
        # Note: In resume mode, versioning is separate - it only affects final output
        #       Debug outputs are reused regardless of versioning mode
        print("\nChecking versioning mode...")
        is_resume_mode = resume_config is not None
        if not handle_versioning_mode(config, skip_if_resume=is_resume_mode):
            # User cancelled reset
            return 0
        
        # Step 4: Load baseline Markmap
        print("\nLoading baseline Markmap...")
        if args.baseline:
            baseline_path = Path(args.baseline)
            if baseline_path.exists():
                baseline_markmap = baseline_path.read_text(encoding="utf-8")
                print(f"  ✓ Loaded from {args.baseline}")
            else:
                print(f"  ✗ Baseline file not found: {args.baseline}")
                return 1
        else:
            try:
                baseline_markmap = load_baseline_markmap(config)
                if baseline_markmap:
                    lines = len(baseline_markmap.splitlines())
                    print(f"  ✓ Loaded ({lines} lines, {len(baseline_markmap)} chars)")
                else:
                    print("  ⚠ No baseline found - will need reference data")
                    baseline_markmap = ""
            except FileNotFoundError as e:
                print(f"  ⚠ {e}")
                baseline_markmap = ""
        
        # Step 5: Load data sources
        print("\nLoading reference data...")
        loader = DataSourcesLoader(config)
        data = loader.load_all()
        
        # Add baseline to data
        data["baseline_markmap"] = baseline_markmap
        
        # Add resume config if available
        if resume_config:
            data["_resume_config"] = resume_config
        
        # Print summary
        print_data_summary(loader.get_summary())
        
        # Step 6: If dry-run, stop here
        if args.dry_run:
            print("\n[DRY RUN] Data sources loaded successfully. Exiting.")
            return 0
        
        # Step 7: Check required API keys
        if not args.no_openai and not ConfigLoader.has_api_key("openai"):
            print("\n❌ Error: OpenAI API key is required but not provided.")
            print("   Use --no-openai to skip if not needed.")
            return 1
        
        # Step 8: Build and run the LangGraph pipeline
        print("\n" + "=" * 60)
        print("Starting Markmap Refinement Pipeline")
        print("=" * 60)
        
        result = run_pipeline(data, config)
        
        # Report results
        print("\n" + "=" * 60)
        print("Pipeline Complete")
        print("=" * 60)
        
        # Print consensus summary
        consensus = result.get("consensus_result")
        if consensus:
            print(f"\n📊 Consensus Summary:")
            print(f"   Adopted: {len(consensus.adopted)} improvements")
            print(f"   Rejected: {len(consensus.rejected)} suggestions")
        
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

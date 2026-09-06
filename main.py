"""
Master Orchestrator CLI for GitHub Starred Repositories Intelligence Pipeline.
Supports initial full build as well as recurring incremental syncs.

Usage:
    python3 main.py                 # Smart run (incremental if cache exists)
    python3 main.py --incremental   # Fast incremental sync for new stars
    python3 main.py --full          # Force full refresh of all repos and READMEs
    python3 main.py --generate-only # Only re-generate HTML from current caches
"""

import argparse
import sys
import time

import config
from src.fetcher import fetch_starred_list, fetch_repo_details
from src.analyzer import run_analysis_pipeline
from src.categorizer import build_groups_data
from src.generator import generate_html_report

def main():
    parser = argparse.ArgumentParser(
        description="GitHub Starred Repositories Analyzer & Intelligence Dashboard Generator"
    )
    parser.add_argument(
        "--incremental",
        action="store_true",
        help="Run fast incremental sync (only fetch stars added since last run)"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Force full re-fetch of all repositories, READMEs, and re-analysis"
    )
    parser.add_argument(
        "--generate-only",
        action="store_true",
        help="Skip fetching and analysis, only regenerate HTML dashboard"
    )

    args = parser.parse_args()

    print("=" * 70)
    print("🌟 GitHub Starred Repositories Intelligence Pipeline (zh-TW)")
    print("=" * 70)

    start_time = time.time()

    if args.generate_only:
        print("[*] Mode: Generate HTML dashboard only.")
        build_groups_data()
        html_path = generate_html_report()
        print(f"\n✨ Done! HTML Dashboard generated in {time.time() - start_time:.2f}s:")
        print(f"👉 {html_path}")
        return

    # Determine sync mode
    is_incremental = args.incremental or (not args.full and config.STARRED_CACHE_FILE.exists())
    print(f"[*] Pipeline mode: {'INCREMENTAL SYNC' if is_incremental else 'FULL BUILD'}")

    # Step 1: Fetch Starred Repositories
    print("\n[Step 1/4] Fetching Starred Repositories via GitHub CLI...")
    starred_list = fetch_starred_list(incremental=is_incremental)

    # Step 2: Fetch Details & READMEs
    print("\n[Step 2/4] Syncing Repository Details and READMEs...")
    details_cache = fetch_repo_details(starred_list, force=args.full)

    # Step 3: Run Deep Why/How/What Analysis
    print("\n[Step 3/4] Analyzing Repositories (Why, How, What, Metrics)...")
    run_analysis_pipeline(force=args.full)

    # Step 4: Grouping, Cross-Comparisons & Top 3 Selection
    print("\n[Step 4/4] Grouping Repositories, Comparing Architectures & Selecting Top 3...")
    build_groups_data()

    # Step 5: HTML Generation
    print("\n[Output] Generating Standalone Interactive zh-TW HTML Dashboard...")
    html_path = generate_html_report()

    elapsed = time.time() - start_time
    print("=" * 70)
    print(f"🎉 All pipeline stages completed successfully in {elapsed:.2f} seconds!")
    print(f"📂 Report Location: {html_path}")
    print("=" * 70)

if __name__ == "__main__":
    main()

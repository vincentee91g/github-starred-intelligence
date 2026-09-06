"""
Merge reviewed chunks into data/analysis_cache.json and trigger categorization and HTML rebuild.
"""

import json
from pathlib import Path
from typing import Dict, Any

import config
from src.categorizer import build_groups_data
from src.generator import generate_html_report

def merge_reviewed_chunks() -> int:
    reviewed_dir = Path("data/reviewed_chunks")
    if not reviewed_dir.exists():
        print("No reviewed chunks directory found.")
        return 0

    merged_data: Dict[str, Any] = {}
    
    # Load existing if available
    if config.ANALYSIS_CACHE_FILE.exists():
        with open(config.ANALYSIS_CACHE_FILE, "r", encoding="utf-8") as f:
            merged_data = json.load(f)

    total_chunks = 0
    total_items = 0
    for chunk_file in sorted(reviewed_dir.glob("reviewed_*.json")):
        try:
            with open(chunk_file, "r", encoding="utf-8") as f:
                chunk_items = json.load(f)
                merged_data.update(chunk_items)
                total_chunks += 1
                total_items += len(chunk_items)
                print(f"[+] Merged {chunk_file.name}: {len(chunk_items)} repos.")
        except Exception as e:
            print(f"Error reading {chunk_file}: {e}")

    # Write back to analysis_cache.json
    with open(config.ANALYSIS_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)

    print(f"[✓] Successfully merged {total_chunks} chunks ({total_items} repos) into {config.ANALYSIS_CACHE_FILE} (Total: {len(merged_data)} repos).")

    # Re-build groups and HTML
    build_groups_data()
    generate_html_report()
    return len(merged_data)

if __name__ == "__main__":
    merge_reviewed_chunks()

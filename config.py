import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Cache files
STARRED_CACHE_FILE = DATA_DIR / "starred_with_dates.json"
REPOS_CACHE_FILE = DATA_DIR / "repos_cache.json"
ANALYSIS_CACHE_FILE = DATA_DIR / "analysis_cache.json"
GROUPS_CACHE_FILE = DATA_DIR / "groups_cache.json"
HTML_OUTPUT_FILE = OUTPUT_DIR / "index.html"

# Batching & API limits
GRAPHQL_BATCH_SIZE = 20
README_MAX_CHARS = 10000  # Cap README length per repo to avoid memory bloat

def atomic_save_json(filepath: Path, data: any, indent: int = 2) -> None:
    """Safely write JSON to a temporary file first, then atomically replace target."""
    import json
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    temp_file = filepath.with_suffix(f".tmp.{os.getpid()}")
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
        temp_file.replace(filepath)
    except Exception:
        if temp_file.exists():
            temp_file.unlink(missing_ok=True)
        raise

def safe_load_json(filepath: Path, default: any = None) -> any:
    """Safely load JSON from file, returning default if file is missing, empty, or corrupted."""
    import json
    filepath = Path(filepath)
    if not filepath.exists():
        return default
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Failed to load {filepath} ({e}), returning fallback.")
        return default

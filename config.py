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

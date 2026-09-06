# AGENTS.md — AI Agent Guidelines & Architecture Manual

> **Repository**: `vincentee91g/github-starred-intelligence`  
> **Target Audience**: AI Coding Agents (Antigravity `agy`, Claude Code, Codex, Cursor, etc.) and human developers.  
> **Live Site**: https://vincentee91g.github.io/github-starred-intelligence/

This document establishes the architectural principles, operational constraints, codebase navigation map, and verification workflows for any AI agent collaborating on this repository.

---

## 1. Project Philosophy & Non-Negotiable Invariants

### 🔒 Invariant 1: Zero Third-Party Dependencies (100% Python Standard Library)
- **Rule**: NEVER introduce external Python packages (no `pip install`, no `requests`, no `pandas`, no `beautifulsoup4`, etc.).
- **Enforcement**: [`tests/test_zero_dependencies.py`](tests/test_zero_dependencies.py) strictly validates that every `import` across all `.py` files belongs solely to the Python standard library or the local project.

### 🔒 Invariant 2: Standalone & Offline-Capable Frontend
- **Rule**: The generated [`output/index.html`](output/index.html) MUST remain a 100% self-contained single file (~1.5 MB).
- **No External CDNs**: Do NOT link to external CSS frameworks (Tailwind, Bootstrap), icon libraries (FontAwesome), or JS CDNs (React, Vue, jQuery, Chart.js).
- **Security & Portability**: The file must function identically whether opened via `file://` locally or hosted on GitHub Pages.

### 🔒 Invariant 3: Frameless Minimalist Table View & Direct Full-Text Expansion
- **Table View**: Keep the data table layout (`<table class="repo-table">`). Do NOT revert to bulky cards (`.repo-card`).
- **6 Core Columns**: `#` (Rank), `專案名稱 (Repository with topics & lang)`, `Stars ⭐`, `Why 痛點緣起`, `How 技術架構`, `What 核心功能`.
- **Direct Expansion**: All text in Why, How, and What MUST display directly in full without `-webkit-line-clamp` or expand/collapse buttons.
- **No Scrollbars**: Container scrollbars are strictly disabled (`overflow: visible; max-height: none`). Natural page flow with global scrollbar suppression (`scrollbar-width: none`).

### 🔒 Invariant 4: Deterministic Code vs LLM Evaluation Boundary
- **Fixed Logic in Code**: Category classification rules, scoring formulas ($100 \times Priority + 12 \times \log_{10}(Stars) + \dots$), sorting, filtering, caching, and table HTML generation must be executed deterministically in code.
- **Semantic Intelligence in Knowledge Base**: Deep architectural pros, cons, scenarios, and domain cross-comparisons reside in [`src/top5_evaluations.py`](src/top5_evaluations.py).

### 🔒 Invariant 5: Safe Atomic I/O & API Protection
- Always write caches and artifacts using [`config.atomic_save_json`](config.py) (`os.replace`) to prevent file corruption during interrupts.
- Use the prefix-break incremental sync algorithm in [`src/fetcher.py`](src/fetcher.py) to prevent rate limit exhaustion.

---

## 2. Codebase Navigation Map

```
.
├── AGENTS.md                  # This file: Agent instructions and project rules
├── README.md                  # Human-facing project documentation
├── config.py                  # Global configurations, file paths, atomic I/O helpers
├── main.py                    # CLI dispatcher (--incremental, --full, --generate-only)
├── .agents/                   # Agent customizations (skills: ponytail, etc.)
├── .github/
│   └── workflows/deploy.yml   # Daily 08:00 UTC+8 cron sync & GitHub Pages deployment
├── data/
│   ├── starred_with_dates.json # Raw GitHub starred repositories cache
│   ├── repos_cache.json        # Detailed repo metadata and full README text cache
│   ├── analysis_cache.json     # Why / How / What structured analysis cache
│   └── groups_cache.json       # 20 taxonomy categories with Top 5 selections
├── output/
│   └── index.html              # Final standalone interactive HTML dashboard
├── src/
│   ├── __init__.py
│   ├── fetcher.py              # GitHub CLI runner & prefix-break incremental fetcher
│   ├── analyzer.py             # Why/How/What semantic extractor with self-healing
│   ├── categorizer.py          # 20-category classifier & deterministic Top 5 scoring
│   ├── top5_evaluations.py     # Curated 100 Top 5 profiles & 20 cross-comparisons
│   └── generator.py            # Frameless HTML table generator with dark/light mode
└── tests/                      # Automated test suite (19/19 passing)
    ├── run_all_tests.py        # Master test runner
    ├── test_distribution.py    # 364 repo complete coverage & 20 categories check
    ├── test_top5_structure.py  # 100 Top 5 project profiles structure validation
    ├── test_zero_dependencies.py # AST-based standard library verification
    ├── test_cache_schemas.py   # Strict schema enforcement for data/*.json
    └── test_resilience_and_caching.py # Atomic write, CLI, and corruption self-healing
```

---

## 3. Essential Commands & Verification Workflows

Before committing or concluding any task, agents MUST run verification:

```bash
# 1. Run all 19 automated tests (Must be 100% passing)
python3 tests/run_all_tests.py

# 2. Regenerate HTML dashboard offline (Fast, ~0.05s)
python3 main.py --generate-only

# 3. Test incremental synchronization
python3 main.py --incremental

# 4. Verify git status is clean
git status
```

---

## 4. Coding & Architecture Standards

1. **Python Conventions**:
   - Python 3.10+ compatible syntax.
   - Comprehensive type hints (`typing.Dict`, `typing.List`, `typing.Optional`, `typing.Any`).
   - Clean docstrings for all exported functions and classes.
   - Defensive error handling with fallback defaults (`config.safe_load_json`).

2. **Frontend Conventions**:
   - Vanilla HTML5, CSS3, and modern JavaScript (ES6+).
   - High contrast support for both Dark mode (`.dark`) and Light mode (`.light`) meeting WCAG AA/AAA.
   - Multi-word search with whitespace splitting (`searchQuery.split(/\s+/)`).
   - CSV export must prepend UTF-8 BOM (`\uFEFF`) to prevent character distortion in Microsoft Excel.

3. **Ponytail Mindset (Anti-Over-Engineering)**:
   - Prefer standard library before writing custom logic.
   - Prefer native browser/CSS features over heavy scripting.
   - Question whether a feature is truly necessary (YAGNI).
   - Keep code concise, readable, and maintainable.

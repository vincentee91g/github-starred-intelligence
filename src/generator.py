"""
HTML Report Generator for GitHub Starred Repositories Intelligence Dashboard.
Generates an interactive, modern, standalone HTML dashboard in Traditional Chinese (zh-TW).
Features:
- Frameless, flat, minimalist modern editorial design (盡可能無外框/卡片嵌套)
- Full text directly expanded for Why, How, What without toggle buttons (文字直接展開無須按鈕)
- No container scrollbars; pure natural page flow with hidden scrollbars (無捲軸設計)
- 6 focused columns: #, Repository (with topics & lang), Stars, Why, How, What (移除收藏日期)
- 20 Granular Technical Domains
- Top 5 Selection per domain with Pros/Cons, Cross-Comparisons & Scenario Recommendations
- Live Multi-Keyword Search, Dynamic Column Sorting, Language Filter, and Smart CSV/JSON Export
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

import config

def format_number(num: int) -> str:
    """Format large numbers with commas or K/M suffix."""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    if num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)

def generate_html_report() -> Path:
    """
    Load data/groups_cache.json and data/analysis_cache.json,
    generate a comprehensive, frameless zh-TW HTML dashboard, and write to output/index.html.
    """
    if not config.GROUPS_CACHE_FILE.exists():
        raise FileNotFoundError(f"Missing {config.GROUPS_CACHE_FILE}. Please run categorizer first.")

    with open(config.GROUPS_CACHE_FILE, "r", encoding="utf-8") as f:
        groups_data = json.load(f)

    with open(config.ANALYSIS_CACHE_FILE, "r", encoding="utf-8") as f:
        analysis_data = json.load(f)

    # Calculate overall KPIs
    total_repos = len(analysis_data)
    total_stars = sum(r.get("stargazers_count", 0) for r in analysis_data.values())
    
    languages: Dict[str, int] = {}
    for r in analysis_data.values():
        lang = r.get("primary_language") or "Other"
        languages[lang] = languages.get(lang, 0) + 1
    sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)

    generation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Serialize data for client-side instant interactivity
    repos_json = json.dumps(list(analysis_data.values()), ensure_ascii=False)
    groups_json = json.dumps(groups_data, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="zh-TW" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GitHub Starred Repositories 智慧分析與精選儀表板 (20大領域 · 表格版)</title>
  <style>
    :root {{
      --bg-primary: #090d16;
      --bg-secondary: #0f172a;
      --bg-tertiary: #1e293b;
      --text-primary: #f8fafc;
      --text-secondary: #94a3b8;
      --text-muted: #64748b;
      --border-color: #334155;
      --border-subtle: #1e293b;
      --table-header-bg: #090d16;
      --table-row-hover: rgba(56, 189, 248, 0.05);
      --table-row-top5-bg: rgba(245, 158, 11, 0.04);
      --table-row-stripe: rgba(15, 23, 42, 0.4);
      --accent-blue: #38bdf8;
      --accent-purple: #c084fc;
      --accent-amber: #fbbf24;
      --accent-emerald: #34d399;
      --accent-rose: #fb7185;
      --accent-indigo: #818cf8;
      --badge-gold: #f59e0b;
      --badge-silver: #94a3b8;
      --badge-bronze: #b45309;
      --badge-merit: #3b82f6;
      --badge-frontier: #8b5cf6;
      --whw-border-why: rgba(56, 189, 248, 0.4);
      --whw-border-how: rgba(192, 132, 252, 0.4);
      --whw-border-what: rgba(52, 211, 153, 0.4);
    }}

    .light {{
      --bg-primary: #ffffff;
      --bg-secondary: #f8fafc;
      --bg-tertiary: #f1f5f9;
      --text-primary: #0f172a;
      --text-secondary: #334155;
      --text-muted: #64748b;
      --border-color: #e2e8f0;
      --border-subtle: #f1f5f9;
      --table-header-bg: #ffffff;
      --table-row-hover: rgba(2, 132, 199, 0.05);
      --table-row-top5-bg: rgba(245, 158, 11, 0.04);
      --table-row-stripe: rgba(248, 250, 252, 0.6);
      --accent-blue: #0284c7;
      --accent-purple: #7c3aed;
      --accent-amber: #b45309;
      --accent-emerald: #059669;
      --accent-rose: #e11d48;
      --accent-indigo: #4338ca;
      --badge-gold: #d97706;
      --badge-silver: #64748b;
      --badge-bronze: #92400e;
      --badge-merit: #2563eb;
      --badge-frontier: #7c3aed;
      --whw-border-why: rgba(2, 132, 199, 0.45);
      --whw-border-how: rgba(124, 58, 237, 0.45);
      --whw-border-what: rgba(5, 150, 105, 0.45);
    }}

    /* Global Scrollbar Suppression (No scrollbars anywhere) */
    html, body, * {{
      scrollbar-width: none !important; /* Firefox */
      -ms-overflow-style: none !important; /* IE 10+ */
    }}
    *::-webkit-scrollbar {{
      display: none !important;
      width: 0 !important;
      height: 0 !important;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans TC", "Helvetica Neue", Arial, sans-serif;
      background-color: var(--bg-primary);
      color: var(--text-primary);
      line-height: 1.6;
      transition: background-color 0.2s, color 0.2s;
      min-height: 100vh;
    }}

    /* Frameless Header */
    header {{
      background: var(--bg-primary);
      border-bottom: 1px solid var(--border-color);
      position: sticky;
      top: 0;
      z-index: 50;
      padding: 0.85rem 2rem;
    }}

    .header-container {{
      max-width: 1720px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 1.5rem;
      flex-wrap: wrap;
    }}

    .logo-section h1 {{
      font-size: 1.3rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      color: var(--text-primary);
    }}

    .logo-section p {{
      font-size: 0.82rem;
      color: var(--text-secondary);
      margin-top: 0.15rem;
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
      flex-wrap: wrap;
    }}

    .theme-toggle, .btn-secondary {{
      background: transparent;
      border: 1px solid var(--border-color);
      color: var(--text-primary);
      padding: 0.4rem 0.8rem;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.82rem;
      font-weight: 500;
      display: flex;
      align-items: center;
      gap: 0.35rem;
      transition: all 0.15s;
    }}

    .theme-toggle:hover, .btn-secondary:hover {{
      border-color: var(--accent-blue);
      color: var(--accent-blue);
      background: var(--bg-secondary);
    }}

    /* Main Container (Frameless, wide canvas) */
    main {{
      max-width: 1720px;
      margin: 1.5rem auto;
      padding: 0 2rem;
    }}

    /* Frameless KPI Statistics Row */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 1.5rem;
      margin-bottom: 2rem;
      padding-bottom: 1.5rem;
      border-bottom: 1px solid var(--border-subtle);
    }}

    .kpi-item {{
      display: flex;
      flex-direction: column;
    }}

    .kpi-title {{
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-secondary);
      margin-bottom: 0.2rem;
      font-weight: 600;
    }}

    .kpi-value {{
      font-size: 1.65rem;
      font-weight: 800;
      color: var(--text-primary);
    }}

    .kpi-desc {{
      font-size: 0.78rem;
      color: var(--text-muted);
      margin-top: 0.15rem;
    }}

    /* Clean Section Headers */
    .section-header {{
      margin-bottom: 1.25rem;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 0.6rem;
      flex-wrap: wrap;
      gap: 0.8rem;
    }}

    .section-header h2 {{
      font-size: 1.25rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}

    .section-header p {{
      font-size: 0.84rem;
      color: var(--text-secondary);
      margin-top: 0.15rem;
    }}

    /* Category Navigation (Natural wrapping, no horizontal scrollbars) */
    .category-tabs {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.45rem;
      margin-bottom: 1.75rem;
    }}

    .category-tab {{
      background: transparent;
      border: 1px solid var(--border-color);
      color: var(--text-secondary);
      padding: 0.4rem 0.85rem;
      border-radius: 6px;
      font-size: 0.82rem;
      font-weight: 500;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.15s;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}

    .category-tab:hover {{
      border-color: var(--accent-blue);
      color: var(--text-primary);
    }}

    .category-tab.active {{
      background: var(--bg-secondary);
      border-color: var(--accent-blue);
      color: var(--accent-blue);
      font-weight: 700;
    }}

    /* Frameless Active Group Overview */
    .group-overview-box {{
      margin-bottom: 2rem;
      padding-bottom: 1.5rem;
      border-bottom: 1px solid var(--border-subtle);
    }}

    .group-overview-title {{
      font-size: 1.15rem;
      font-weight: 700;
      margin-bottom: 0.35rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}

    .group-overview-desc {{
      font-size: 0.88rem;
      color: var(--text-secondary);
      margin-bottom: 1rem;
      line-height: 1.55;
    }}

    .group-comparison-block {{
      border-left: 3px solid var(--accent-blue);
      padding-left: 0.85rem;
      font-size: 0.86rem;
      color: var(--text-primary);
      margin-bottom: 0.9rem;
      line-height: 1.6;
    }}

    .group-comparison-block strong.header-tag {{
      color: var(--accent-blue);
      display: block;
      font-size: 0.88rem;
      margin-bottom: 0.25rem;
    }}

    .group-scenarios-block {{
      border-left: 3px solid var(--accent-emerald);
      padding-left: 0.85rem;
      font-size: 0.86rem;
      color: var(--text-primary);
      margin-bottom: 0.9rem;
      line-height: 1.6;
    }}

    .group-scenarios-block strong.header-tag {{
      color: var(--accent-emerald);
      display: block;
      font-size: 0.88rem;
      margin-bottom: 0.25rem;
    }}

    .aspect-pill {{
      display: inline-block;
      border: 1px solid var(--border-color);
      padding: 0.15rem 0.55rem;
      border-radius: 4px;
      font-size: 0.74rem;
      color: var(--text-secondary);
      margin-right: 0.4rem;
      margin-bottom: 0.3rem;
    }}

    /* Frameless Top 5 Grid */
    .top5-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
      gap: 1.5rem;
      margin-bottom: 2.75rem;
    }}

    .top5-card {{
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 1.25rem;
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .top5-card.rank-1 {{ border-left: 4px solid var(--badge-gold); }}
    .top5-card.rank-2 {{ border-left: 4px solid var(--badge-silver); }}
    .top5-card.rank-3 {{ border-left: 4px solid var(--badge-bronze); }}
    .top5-card.rank-4 {{ border-left: 4px solid var(--badge-merit); }}
    .top5-card.rank-5 {{ border-left: 4px solid var(--badge-frontier); }}

    .top5-rank-badge {{
      display: inline-block;
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--text-secondary);
      margin-bottom: 0.4rem;
    }}

    .top5-card-header {{
      margin-bottom: 0.75rem;
    }}

    .top5-repo-name a {{
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--accent-blue);
      text-decoration: none;
      word-break: break-word;
    }}

    .top5-repo-name a:hover {{
      text-decoration: underline;
    }}

    .top5-meta-chips {{
      display: flex;
      gap: 0.5rem;
      align-items: center;
      margin-top: 0.35rem;
      flex-wrap: wrap;
    }}

    .star-chip {{
      color: var(--accent-amber);
      font-size: 0.76rem;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 0.2rem;
    }}

    .lang-badge {{
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      font-size: 0.76rem;
      color: var(--text-secondary);
      font-weight: 500;
    }}

    .lang-dot {{
      width: 7px;
      height: 7px;
      border-radius: 50%;
      display: inline-block;
      flex-shrink: 0;
    }}

    .highlight-box {{
      border-left: 2px solid var(--accent-blue);
      padding-left: 0.6rem;
      font-size: 0.82rem;
      margin-bottom: 0.8rem;
      line-height: 1.5;
    }}

    .highlight-box strong {{
      color: var(--accent-blue);
      display: block;
      margin-bottom: 0.15rem;
      font-size: 0.76rem;
      font-weight: 700;
    }}

    .pros-cons-box {{
      display: flex;
      flex-direction: column;
      gap: 0.55rem;
      margin-bottom: 0.8rem;
      font-size: 0.81rem;
    }}

    .pros-list {{
      border-left: 2px solid var(--accent-emerald);
      padding-left: 0.6rem;
    }}

    .pros-list strong {{
      color: var(--accent-emerald);
      display: block;
      margin-bottom: 0.2rem;
      font-size: 0.76rem;
      font-weight: 700;
    }}

    .cons-list {{
      border-left: 2px solid var(--accent-rose);
      padding-left: 0.6rem;
    }}

    .cons-list strong {{
      color: var(--accent-rose);
      display: block;
      margin-bottom: 0.2rem;
      font-size: 0.76rem;
      font-weight: 700;
    }}

    .bullet-item {{
      margin-bottom: 0.2rem;
      line-height: 1.45;
      color: var(--text-primary);
    }}

    .bullet-item:last-child {{
      margin-bottom: 0;
    }}

    .pros-list .bullet-item::before {{
      content: "✓ ";
      color: var(--accent-emerald);
      font-weight: 700;
    }}

    .cons-list .bullet-item::before {{
      content: "– ";
      color: var(--accent-rose);
      font-weight: 700;
    }}

    .scenario-rec-text {{
      font-size: 0.81rem;
      color: var(--text-primary);
      border-left: 2px solid var(--accent-blue);
      padding-left: 0.6rem;
      line-height: 1.5;
      margin-bottom: 0.8rem;
    }}

    .top5-card-footer {{
      margin-top: 0.8rem;
      padding-top: 0.6rem;
      border-top: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .btn-locate-row {{
      background: none;
      border: none;
      color: var(--accent-blue);
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.25rem;
    }}

    .btn-locate-row:hover {{
      text-decoration: underline;
    }}

    /* Frameless Controls Bar */
    .controls-bar {{
      margin-bottom: 1.25rem;
      display: flex;
      flex-direction: column;
      gap: 0.85rem;
    }}

    .search-row {{
      display: flex;
      gap: 0.75rem;
      flex-wrap: wrap;
      align-items: center;
    }}

    .search-input-wrapper {{
      flex: 1;
      min-width: 280px;
      position: relative;
    }}

    .search-input {{
      width: 100%;
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-radius: 6px;
      padding: 0.55rem 2rem 0.55rem 2.2rem;
      color: var(--text-primary);
      font-size: 0.88rem;
      outline: none;
      transition: border-color 0.15s;
    }}

    .search-input:focus {{
      border-color: var(--accent-blue);
    }}

    .search-icon {{
      position: absolute;
      left: 0.75rem;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      font-size: 0.85rem;
      pointer-events: none;
    }}

    .search-clear-btn {{
      position: absolute;
      right: 0.75rem;
      top: 50%;
      transform: translateY(-50%);
      background: none;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 0.95rem;
      display: none;
    }}

    .filter-select {{
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-radius: 6px;
      padding: 0.55rem 0.85rem;
      color: var(--text-primary);
      font-size: 0.82rem;
      font-weight: 500;
      outline: none;
      cursor: pointer;
      transition: border-color 0.15s;
    }}

    .filter-select:focus {{
      border-color: var(--accent-blue);
    }}

    .chips-row {{
      display: flex;
      gap: 0.35rem;
      flex-wrap: wrap;
    }}

    .filter-chip {{
      background: transparent;
      border: 1px solid var(--border-color);
      color: var(--text-secondary);
      padding: 0.3rem 0.65rem;
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.15s;
      white-space: nowrap;
    }}

    .filter-chip:hover {{
      color: var(--text-primary);
      border-color: var(--accent-blue);
    }}

    .filter-chip.active {{
      background: var(--bg-secondary);
      color: var(--accent-blue);
      border-color: var(--accent-blue);
      font-weight: 700;
    }}

    /* Frameless Table Container (Natural Page Flow, No Scrollbars) */
    .table-container {{
      width: 100%;
      overflow: visible;
      background: transparent;
      border: none;
      margin-bottom: 2.5rem;
    }}

    .repo-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.86rem;
      text-align: left;
    }}

    .repo-table thead tr th {{
      background: var(--table-header-bg);
      color: var(--text-secondary);
      font-weight: 700;
      padding: 0.85rem 0.9rem;
      border-bottom: 2px solid var(--border-color);
      border-top: 1px solid var(--border-color);
      cursor: pointer;
      user-select: none;
      white-space: nowrap;
      position: sticky;
      top: 56px;
      z-index: 25;
      transition: color 0.15s;
    }}

    .repo-table thead tr th:hover {{
      color: var(--accent-blue);
    }}

    .repo-table thead tr th.sorted-asc,
    .repo-table thead tr th.sorted-desc {{
      color: var(--accent-blue);
    }}

    .sort-indicator {{
      display: inline-block;
      margin-left: 0.3rem;
      font-size: 0.8rem;
      opacity: 0.75;
    }}

    .repo-table td {{
      padding: 1.1rem 0.9rem;
      border-bottom: 1px solid var(--border-subtle);
      vertical-align: top;
      line-height: 1.6;
    }}

    .repo-table tbody tr {{
      transition: background-color 0.15s;
    }}

    .repo-table tbody tr:hover {{
      background: var(--table-row-hover);
    }}

    .repo-table tbody tr.row-top5 {{
      background: var(--table-row-top5-bg);
    }}

    .repo-table tbody tr.row-flash {{
      animation: highlightRow 2s ease-out;
    }}

    @keyframes highlightRow {{
      0% {{ background: rgba(56, 189, 248, 0.35); }}
      100% {{ background: transparent; }}
    }}

    /* 6-Column Layout (Frameless, wide text areas) */
    .col-rank {{
      width: 52px;
      min-width: 52px;
      text-align: center;
      font-weight: 700;
    }}

    .rank-medal-badge {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 1.15rem;
    }}

    .col-name {{
      width: 260px;
      min-width: 220px;
      max-width: 290px;
    }}

    .table-repo-link {{
      color: var(--accent-blue);
      text-decoration: none;
      font-weight: 700;
      font-size: 0.92rem;
      display: inline-block;
      margin-bottom: 0.3rem;
      word-break: break-word;
    }}

    .table-repo-link:hover {{
      text-decoration: underline;
    }}

    .table-category-tag {{
      display: inline-block;
      font-size: 0.72rem;
      padding: 0.1rem 0.45rem;
      border-radius: 4px;
      border: 1px solid var(--border-color);
      color: var(--text-secondary);
      margin-top: 0.3rem;
      cursor: pointer;
      transition: all 0.15s;
    }}

    .table-category-tag:hover {{
      border-color: var(--accent-blue);
      color: var(--accent-blue);
    }}

    .col-stars {{
      width: 95px;
      min-width: 95px;
      text-align: right;
      white-space: nowrap;
    }}

    .col-whw-header {{
      min-width: 260px;
    }}

    .col-why {{
      width: 32%;
      min-width: 260px;
    }}

    .col-how {{
      width: 32%;
      min-width: 260px;
    }}

    .col-what {{
      width: 28%;
      min-width: 240px;
    }}

    .whw-cell-container {{
      display: flex;
      flex-direction: column;
      height: 100%;
    }}

    .whw-cell-why {{
      border-left: 2px solid var(--whw-border-why);
      padding-left: 0.7rem;
    }}

    .whw-cell-how {{
      border-left: 2px solid var(--whw-border-how);
      padding-left: 0.7rem;
    }}

    .whw-cell-what {{
      border-left: 2px solid var(--whw-border-what);
      padding-left: 0.7rem;
    }}

    /* Text Directly Expanded (No buttons, no clamp) */
    .whw-text {{
      color: var(--text-primary);
      font-size: 0.85rem;
      line-height: 1.65;
      text-align: left;
      word-break: break-word;
    }}

    .topic-pill {{
      display: inline-block;
      font-size: 0.69rem;
      padding: 0.08rem 0.35rem;
      border-radius: 3px;
      background: var(--bg-tertiary);
      color: var(--text-secondary);
      margin-right: 0.25rem;
      margin-top: 0.25rem;
      cursor: pointer;
      transition: all 0.15s;
    }}

    .topic-pill:hover {{
      color: var(--accent-blue);
    }}

    /* Frameless Guide Section */
    .guide-card {{
      margin-bottom: 2rem;
      padding-top: 1.5rem;
      border-top: 1px solid var(--border-color);
    }}

    .guide-card h3 {{
      font-size: 1.1rem;
      margin-bottom: 0.4rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}

    .code-block {{
      background: var(--bg-secondary);
      color: var(--accent-blue);
      border: 1px solid var(--border-color);
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      padding: 0.85rem 1.1rem;
      border-radius: 6px;
      font-size: 0.84rem;
      margin-top: 0.6rem;
      line-height: 1.5;
    }}

    footer {{
      text-align: center;
      padding: 2rem 1rem;
      color: var(--text-muted);
      font-size: 0.82rem;
      border-top: 1px solid var(--border-color);
    }}
  </style>
</head>
<body>

  <header>
    <div class="header-container">
      <div class="logo-section">
        <h1>🌟 GitHub Starred Repositories 智慧分析儀表板</h1>
        <p>全量 364 個開源專案 · 20 大精細技術領域 · 各領域 Top 5 優缺點交叉對比 · 完整表格呈現 (繁體中文 zh-TW)</p>
      </div>
      <div class="header-actions">
        <button class="theme-toggle" id="themeToggleBtn" onclick="toggleTheme()" title="切換深色 / 淺色主題">🌓 切換主題</button>
        <button class="btn-secondary" id="exportCsvBtn" onclick="exportDataCSV()" title="匯出符合當前篩選之 CSV 表格">📊 匯出 CSV</button>
        <button class="btn-secondary" id="exportJsonBtn" onclick="exportDataJSON()" title="匯出符合當前篩選之 JSON 資料">📥 匯出 JSON</button>
      </div>
    </div>
  </header>

  <main>

    <!-- Executive KPIs (Frameless Stats Row) -->
    <section class="kpi-grid">
      <div class="kpi-item">
        <span class="kpi-title">總星標專案 (Total Repos)</span>
        <span class="kpi-value">{total_repos:,}</span>
        <span class="kpi-desc">全量收錄個人 Starred 軌跡</span>
      </div>
      <div class="kpi-item">
        <span class="kpi-title">社群總 Stars 累積</span>
        <span class="kpi-value">{format_number(total_stars)}★</span>
        <span class="kpi-desc">累計 {total_stars:,} 顆星標影響力</span>
      </div>
      <div class="kpi-item">
        <span class="kpi-title">精細劃分領域 (Categories)</span>
        <span class="kpi-value">{len(groups_data)} 大領域</span>
        <span class="kpi-desc">由原 10 大類深度擴展為 20 類</span>
      </div>
      <div class="kpi-item">
        <span class="kpi-title">主要程式語言 (Languages)</span>
        <span class="kpi-value">{sorted_langs[0][0]} / {sorted_langs[1][0]}</span>
        <span class="kpi-desc">{sorted_langs[0][0]} ({sorted_langs[0][1]}), {sorted_langs[1][0]} ({sorted_langs[1][1]}), {sorted_langs[2][0]} ({sorted_langs[2][1]})</span>
      </div>
    </section>

    <!-- Hall of Fame: Top 5 & Group Comparisons -->
    <section id="top5-section">
      <div class="section-header">
        <div>
          <h2>🏆 20 大領域 Top 5 評選 · 優缺點交叉比對與適用場景推薦</h2>
          <p>由固定代碼評分邏輯遴選各領域 Top 5，並由 LLM 進行深度橫向優缺點交叉對比與適用場景決策指引</p>
        </div>
      </div>

      <!-- 20 Category Filter Tabs (Wrapping, no scrollbar) -->
      <div class="category-tabs" id="categoryTabs">
        <!-- Rendered dynamically -->
      </div>

      <!-- Active Group Overview & Cross-Comparison -->
      <div class="group-overview-box" id="groupOverviewBox">
        <!-- Rendered dynamically -->
      </div>

      <!-- Top 5 Showcase Grid -->
      <div class="top5-grid" id="top5Container">
        <!-- Rendered dynamically -->
      </div>
    </section>

    <!-- All Repositories Table View (Frameless, 6 Columns, Text Directly Expanded) -->
    <section id="table-section">
      <div class="section-header">
        <div>
          <h2>📋 專案詳細資訊檢索表格 (全量專案表格化呈現 · 內容直接展開)</h2>
          <p>每一種類均以表格呈現每個專案的完整資訊（專案名稱、Stars、Why 痛點、How 架構、What 功能、標籤），支援表頭吸頂、即時搜尋與欄位排序</p>
        </div>
        <div style="display: flex; align-items: center; gap: 0.8rem;">
          <span id="filteredCountBadge" style="font-size: 0.85rem; color: var(--accent-blue); font-weight: 700;">顯示 364 / 364 個專案</span>
        </div>
      </div>

      <!-- Controls Bar -->
      <div class="controls-bar">
        <div class="search-row">
          <div class="search-input-wrapper">
            <span class="search-icon">🔍</span>
            <input type="text" id="searchInput" class="search-input" placeholder="即時搜尋專案名稱、作者、Why/How/What 關鍵字、領域、語言、標籤 (支援多關鍵字空白分隔)..." oninput="handleSearch()">
            <button class="search-clear-btn" id="searchClearBtn" onclick="clearSearch()" title="清除搜尋">✕</button>
          </div>
          <select id="sortSelect" class="filter-select" onchange="handleSortSelect()">
            <option value="stars_desc">⭐ Stars 降序 (預設)</option>
            <option value="stars_asc">⭐ Stars 升序</option>
            <option value="name_asc">🔤 專案名稱 (A-Z)</option>
            <option value="name_desc">🔤 專案名稱 (Z-A)</option>
            <option value="rank_asc">🏆 領域評選排名 (Top 5 優先)</option>
          </select>
          <select id="languageSelect" class="filter-select" onchange="handleLanguageFilter()">
            <option value="all">🌐 全部語言</option>
            {''.join(f'<option value="{lang}">{lang} ({count})</option>' for lang, count in sorted_langs)}
          </select>
        </div>

        <div class="chips-row" id="categoryChips">
          <!-- Rendered dynamically -->
        </div>
      </div>

      <!-- Repositories Table Container (Natural Page Flow, No Scrollbars) -->
      <div class="table-container" id="repoTableContainer">
        <table class="repo-table" id="repoTable">
          <thead>
            <tr>
              <th class="col-rank" id="th-rank" onclick="toggleSort('rank')" title="點擊依排名排序">
                # <span class="sort-indicator" id="sort-ind-rank">↕</span>
              </th>
              <th class="col-name" id="th-name" onclick="toggleSort('name')" title="點擊依專案名稱排序">
                專案名稱 (Repository) <span class="sort-indicator" id="sort-ind-name">↕</span>
              </th>
              <th class="col-stars" id="th-stars" onclick="toggleSort('stars')" title="點擊依 Stars 排序">
                Stars ⭐ <span class="sort-indicator" id="sort-ind-stars">▼</span>
              </th>
              <th class="col-why col-whw-header" title="專案解決之核心痛點與架構瓶頸">
                🎯 Why 痛點緣起 / 解決瓶頸
              </th>
              <th class="col-how col-whw-header" title="核心技術架構、演算法與實現原理">
                ⚙️ How 技術架構 / 實現原理
              </th>
              <th class="col-what col-whw-header" title="交付套件、核心功能與使用者介面">
                📦 What 核心功能 / 交付套件
              </th>
            </tr>
          </thead>
          <tbody id="repoTableBody">
            <!-- Rendered dynamically -->
          </tbody>
        </table>
      </div>
    </section>

    <!-- Recurring Automation Pipeline Guide -->
    <section class="guide-card">
      <h3>🔄 持續增量更新管線說明 (Incremental Pipeline)</h3>
      <p style="color: var(--text-secondary); font-size: 0.88rem; margin-bottom: 0.6rem;">
        本系統具備時間戳感知與多級快取機制。後續定期執行僅同步新增或有變更的 Starred 專案，秒級完成重新分類、Top 5 評選與 HTML 儀表板更新。
      </p>
      <div class="code-block">
# 1. 智慧增量同步 (僅檢查新增 Starred 倉庫，秒級完成)
python3 main.py --incremental

# 2. 全量強制重構 (重新從 GitHub API 擷取所有 364 個倉庫與 README)
python3 main.py --full

# 3. 僅重新生成 HTML 儀表板
python3 main.py --generate-only
      </div>
    </section>

  </main>

  <footer>
    <p>GitHub Starred Repositories Intelligence Dashboard (20 大領域精細分類 · Top 5 優缺點交叉比對 · 全量表格呈現)</p>
    <p style="margin-top: 0.3rem;">自動建置時間：{generation_time} · Generated by Antigravity</p>
  </footer>

  <!-- Client-side Data and Controller Logic -->
  <script>
    const allRepos = {repos_json};
    const groupsData = {groups_json};

    let activeCategory = Object.keys(groupsData)[0];
    let selectedCategoryFilter = activeCategory;
    let selectedLanguageFilter = 'all';
    let searchQuery = '';
    let sortMode = 'stars_desc';

    // Pre-calculate Top 5 map for each category
    const top5Map = {{}};
    const medals = ['🥇', '🥈', '🥉', '🏅', '🎖️'];
    for (const [catId, g] of Object.entries(groupsData)) {{
      g.top_5.forEach((t, idx) => {{
        top5Map[t.full_name] = {{
          categoryId: catId,
          categoryName: g.meta.name,
          rank: idx + 1,
          medal: medals[idx] || '🎖️',
          rankTitle: t.rank_title
        }};
      }});
    }}

    // Theme Management
    function toggleTheme() {{
      const html = document.documentElement;
      if (html.classList.contains('dark')) {{
        html.classList.remove('dark');
        html.classList.add('light');
        localStorage.setItem('theme', 'light');
      }} else {{
        html.classList.remove('light');
        html.classList.add('dark');
        localStorage.setItem('theme', 'dark');
      }}
    }}

    // Filter Repos Helper for dynamic export
    function getCurrentlyFilteredRepos() {{
      return allRepos.filter(r => {{
        if (selectedCategoryFilter !== 'all' && r.category_id !== selectedCategoryFilter) return false;
        const repoLang = r.primary_language || 'Other';
        if (selectedLanguageFilter !== 'all' && repoLang !== selectedLanguageFilter) return false;
        if (searchQuery) {{
          const searchable = `${{r.full_name}} ${{r.owner}} ${{r.category_name}} ${{repoLang}} ${{r.description || ''}} ${{r.analysis ? r.analysis.why : ''}} ${{r.analysis ? r.analysis.how : ''}} ${{r.analysis ? r.analysis.what : ''}} ${{(r.topics || []).join(' ')}}`.toLowerCase();
          const terms = searchQuery.split(/\\s+/).filter(t => t.length > 0);
          const matchesAll = terms.every(term => searchable.includes(term));
          if (!matchesAll) return false;
        }}
        return true;
      }});
    }}

    // Export Data CSV (Excluded starred_at as requested)
    function exportDataCSV() {{
      const filtered = getCurrentlyFilteredRepos();
      let csv = '專案名稱,GitHub網址,所屬分類,Stars,主要語言,Why痛點緣起,How技術架構,What核心功能,標籤\\n';
      filtered.forEach(r => {{
        const cleanWhy = (r.analysis ? r.analysis.why : (r.description || '')).replace(/"/g, '""').replace(/\\r?\\n/g, ' ');
        const cleanHow = (r.analysis ? r.analysis.how : '').replace(/"/g, '""').replace(/\\r?\\n/g, ' ');
        const cleanWhat = (r.analysis ? r.analysis.what : '').replace(/"/g, '""').replace(/\\r?\\n/g, ' ');
        const topics = (r.topics || []).join('; ');
        const row = [
          `"${{(r.full_name || '').replace(/"/g, '""')}}"`,
          `"${{(r.url || '').replace(/"/g, '""')}}"`,
          `"${{(r.category_name || '').replace(/"/g, '""')}}"`,
          r.stargazers_count || 0,
          `"${{(r.primary_language || 'Other').replace(/"/g, '""')}}"`,
          `"${{cleanWhy}}"`,
          `"${{cleanHow}}"`,
          `"${{cleanWhat}}"`,
          `"${{topics}}"`
        ];
        csv += row.join(',') + '\\n';
      }});
      const blob = new Blob([new Uint8Array([0xEF, 0xBB, 0xBF]), csv], {{ type: 'text/csv;charset=utf-8;' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const catSuffix = selectedCategoryFilter === 'all' ? 'all' : selectedCategoryFilter;
      a.download = `github_starred_${{catSuffix}}_${{new Date().toISOString().slice(0, 10)}}.csv`;
      a.click();
    }}

    // Export Data JSON
    function exportDataJSON() {{
      const filtered = getCurrentlyFilteredRepos();
      const blob = new Blob([JSON.stringify(filtered, null, 2)], {{ type: 'application/json' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const catSuffix = selectedCategoryFilter === 'all' ? 'all' : selectedCategoryFilter;
      a.download = `github_starred_${{catSuffix}}_${{new Date().toISOString().slice(0, 10)}}.json`;
      a.click();
    }}

    // Render 20 Category Tabs & Chips
    function renderCategoryControls() {{
      const tabsContainer = document.getElementById('categoryTabs');
      const chipsContainer = document.getElementById('categoryChips');
      
      let tabsHtml = '';
      let chipsHtml = `<button class="filter-chip ${{selectedCategoryFilter === 'all' ? 'active' : ''}}" onclick="setCategoryFilter('all', this)">🌐 全部領域 (${{allRepos.length}})</button>`;

      for (const [catId, g] of Object.entries(groupsData)) {{
        const isTabActive = catId === activeCategory ? 'active' : '';
        const isChipActive = catId === selectedCategoryFilter ? 'active' : '';

        tabsHtml += `
          <button class="category-tab ${{isTabActive}}" onclick="switchActiveCategory('${{catId}}')" title="${{g.meta.name}}">
            <span>${{g.meta.icon}}</span>
            <span>${{g.meta.name}}</span>
            <span style="opacity: 0.75; font-size: 0.74rem;">(${{g.repos.length}})</span>
          </button>
        `;

        chipsHtml += `
          <button class="filter-chip ${{isChipActive}}" onclick="setCategoryFilter('${{catId}}', this)">
            ${{g.meta.icon}} ${{g.meta.name}} (${{g.repos.length}})
          </button>
        `;
      }}

      tabsContainer.innerHTML = tabsHtml;
      chipsContainer.innerHTML = chipsHtml;
      renderActiveGroupOverview();
    }}

    function switchActiveCategory(catId) {{
      activeCategory = catId;
      selectedCategoryFilter = catId;
      renderCategoryControls();
      renderRepoTable();
    }}

    function setCategoryFilter(catId, btnElem) {{
      selectedCategoryFilter = catId;
      if (catId !== 'all') {{
        activeCategory = catId;
      }}
      renderCategoryControls();
      renderRepoTable();
    }}

    // Render Active Group Overview, Cross-Comparison & Top 5 Cards
    function renderActiveGroupOverview() {{
      const g = groupsData[activeCategory];
      if (!g) return;

      const overviewBox = document.getElementById('groupOverviewBox');

      let formattedComparison = (g.comparison.cross_comparison || g.comparison.summary || '')
        .replace(/【(.*?)】/g, '<strong style="color: var(--accent-blue);">【$1】</strong>')
        .replace(/\\n/g, '<br>');

      let formattedScenarios = (g.comparison.scenario_recommendations || '依據專案約束與架構目標選擇合適方案。')
        .replace(/【(.*?)】/g, '<strong style="color: var(--accent-emerald);">【$1】</strong>')
        .replace(/• (.*?)(?=(• |$|<br>))/g, '<div class="bullet-item">$1</div>')
        .replace(/\\n/g, '<br>');

      const aspectPills = (g.comparison.aspects || ['架構解耦性', '生態相容性', '適用場景']).map(a =>
        `<span class="aspect-pill">📌 ${{a}}</span>`
      ).join('');

      overviewBox.innerHTML = `
        <div class="group-overview-title">
          <span style="font-size: 1.25rem;">${{g.meta.icon}}</span>
          <span>${{g.meta.name}}</span>
          <span style="font-size: 0.78rem; color: var(--accent-blue); font-weight: 700; border: 1px solid var(--border-color); padding: 0.15rem 0.5rem; border-radius: 4px;">本領域共收錄 ${{g.repos.length}} 個專案</span>
        </div>
        <p class="group-overview-desc">${{g.meta.summary}}</p>
        
        <div class="group-comparison-block">
          <strong class="header-tag">⚖️ Top 5 橫向技術架構與優缺點交叉對比剖析：</strong>
          <div>${{formattedComparison}}</div>
        </div>

        <div class="group-scenarios-block">
          <strong class="header-tag">🎯 適用場景推薦與決策指引：</strong>
          <div>${{formattedScenarios}}</div>
        </div>

        <div style="margin-top: 0.6rem;">
          ${{aspectPills}}
        </div>
      `;

      // Render Top 5 Cards
      const top5Container = document.getElementById('top5Container');
      let top5Html = '';

      g.top_5.forEach((t, idx) => {{
        const rankNum = idx + 1;
        const langColor = getLanguageColor(t.primary_language || 'Other');

        const prosListHtml = (t.pros || []).map(p => `<li class="bullet-item">${{p}}</li>`).join('');
        const consListHtml = (t.cons || []).map(c => `<li class="bullet-item">${{c}}</li>`).join('');

        top5Html += `
          <div class="top5-card rank-${{rankNum}}" id="top5-card-${{t.name}}">
            <span class="top5-rank-badge">${{t.rank_title}}</span>
            <div>
              <div class="top5-card-header">
                <div class="top5-repo-name">
                  <a href="${{t.url}}" target="_blank" rel="noopener noreferrer">${{t.full_name}} ↗</a>
                </div>
                <div class="top5-meta-chips">
                  <span class="star-chip">★ ${{t.stargazers_count.toLocaleString()}}</span>
                  <span class="lang-badge">
                    <span class="lang-dot" style="background: ${{langColor}};"></span>
                    <span>${{t.primary_language || 'Other'}}</span>
                  </span>
                </div>
              </div>

              <div class="highlight-box">
                <strong>🌟 核心技術亮點</strong>
                ${{t.highlight}}
              </div>

              <div class="pros-cons-box">
                <div class="pros-list">
                  <strong>✅ 核心優勢 (Pros)</strong>
                  <ul style="list-style: none;">${{prosListHtml}}</ul>
                </div>
                <div class="cons-list">
                  <strong>⚠️ 潛在缺點與局限 (Cons)</strong>
                  <ul style="list-style: none;">${{consListHtml}}</ul>
                </div>
              </div>

              <div class="scenario-rec-text">
                <strong style="color: var(--accent-blue); display: block; margin-bottom: 0.2rem;">🎯 推薦適用場景：</strong>
                ${{t.scenarios}}
              </div>

              <p style="font-size: 0.78rem; color: var(--text-muted); line-height: 1.48; margin-bottom: 0.6rem;">
                <strong style="color: var(--text-secondary);">💡 評選理由：</strong>${{t.rationale}}
              </p>
            </div>

            <div class="top5-card-footer">
              <button class="btn-locate-row" onclick="locateTableRow('${{t.full_name}}')">
                <span>📋 在表格中檢視</span> <span>▾</span>
              </button>
              <a href="${{t.url}}" target="_blank" rel="noopener noreferrer" style="font-size: 0.8rem; color: var(--accent-blue); text-decoration: none; font-weight: 600;">造訪 GitHub →</a>
            </div>
          </div>
        `;
      }});

      top5Container.innerHTML = top5Html;
    }}

    function getLanguageColor(lang) {{
      const colors = {{
        'Python': '#3572A5',
        'TypeScript': '#3178c6',
        'Rust': '#dea584',
        'JavaScript': '#f1e05a',
        'Go': '#00ADD8',
        'Shell': '#89e051',
        'HTML': '#e34c26',
        'C++': '#f34b7d',
        'C': '#555555',
        'Swift': '#F05138',
        'Clojure': '#db5855',
        'Scala': '#c22d40',
        'Other': '#9ca3af'
      }};
      return colors[lang] || '#9ca3af';
    }}

    // Filter, Search & Render Repos Table
    function handleSearch() {{
      const input = document.getElementById('searchInput');
      searchQuery = input.value.trim().toLowerCase();
      const clearBtn = document.getElementById('searchClearBtn');
      clearBtn.style.display = searchQuery ? 'block' : 'none';
      renderRepoTable();
    }}

    function clearSearch() {{
      const input = document.getElementById('searchInput');
      input.value = '';
      searchQuery = '';
      document.getElementById('searchClearBtn').style.display = 'none';
      renderRepoTable();
      input.focus();
    }}

    function handleSortSelect() {{
      sortMode = document.getElementById('sortSelect').value;
      updateSortIndicators();
      renderRepoTable();
    }}

    function toggleSort(field) {{
      if (field === 'stars') {{
        sortMode = sortMode === 'stars_desc' ? 'stars_asc' : 'stars_desc';
      }} else if (field === 'name') {{
        sortMode = sortMode === 'name_asc' ? 'name_desc' : 'name_asc';
      }} else if (field === 'rank') {{
        sortMode = sortMode === 'rank_asc' ? 'stars_desc' : 'rank_asc';
      }}
      document.getElementById('sortSelect').value = sortMode;
      updateSortIndicators();
      renderRepoTable();
    }}

    function updateSortIndicators() {{
      const indicators = {{
        'rank': document.getElementById('sort-ind-rank'),
        'name': document.getElementById('sort-ind-name'),
        'stars': document.getElementById('sort-ind-stars')
      }};
      const ths = {{
        'rank': document.getElementById('th-rank'),
        'name': document.getElementById('th-name'),
        'stars': document.getElementById('th-stars')
      }};

      Object.keys(indicators).forEach(k => {{
        if (indicators[k]) indicators[k].innerText = '↕';
        if (ths[k]) {{
          ths[k].classList.remove('sorted-asc', 'sorted-desc');
        }}
      }});

      if (sortMode === 'stars_desc') {{
        indicators.stars.innerText = '▼';
        ths.stars.classList.add('sorted-desc');
      }} else if (sortMode === 'stars_asc') {{
        indicators.stars.innerText = '▲';
        ths.stars.classList.add('sorted-asc');
      }} else if (sortMode === 'name_asc') {{
        indicators.name.innerText = '▲';
        ths.name.classList.add('sorted-asc');
      }} else if (sortMode === 'name_desc') {{
        indicators.name.innerText = '▼';
        ths.name.classList.add('sorted-desc');
      }} else if (sortMode === 'rank_asc') {{
        indicators.rank.innerText = '▲';
        ths.rank.classList.add('sorted-asc');
      }}
    }}

    function handleLanguageFilter() {{
      selectedLanguageFilter = document.getElementById('languageSelect').value;
      renderRepoTable();
    }}

    function locateTableRow(fullName) {{
      const rowId = 'repo-row-' + fullName.replace(/[^a-zA-Z0-9-_]/g, '_');
      const targetRow = document.getElementById(rowId);
      if (targetRow) {{
        targetRow.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
        targetRow.classList.remove('row-flash');
        void targetRow.offsetWidth; // Trigger reflow
        targetRow.classList.add('row-flash');
      }} else {{
        selectedCategoryFilter = 'all';
        renderCategoryControls();
        renderRepoTable();
        setTimeout(() => {{
          const el = document.getElementById(rowId);
          if (el) {{
            el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
            el.classList.add('row-flash');
          }}
        }}, 100);
      }}
    }}

    function filterByTopic(topic) {{
      const searchInput = document.getElementById('searchInput');
      searchInput.value = topic;
      handleSearch();
      document.getElementById('table-section').scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    }}

    function renderRepoTable() {{
      const tbody = document.getElementById('repoTableBody');
      const countBadge = document.getElementById('filteredCountBadge');
      const csvBtn = document.getElementById('exportCsvBtn');
      const jsonBtn = document.getElementById('exportJsonBtn');

      let filtered = getCurrentlyFilteredRepos();

      // Sorting
      if (sortMode === 'stars_desc') {{
        filtered.sort((a, b) => (b.stargazers_count || 0) - (a.stargazers_count || 0));
      }} else if (sortMode === 'stars_asc') {{
        filtered.sort((a, b) => (a.stargazers_count || 0) - (b.stargazers_count || 0));
      }} else if (sortMode === 'name_asc') {{
        filtered.sort((a, b) => a.full_name.localeCompare(b.full_name));
      }} else if (sortMode === 'name_desc') {{
        filtered.sort((a, b) => b.full_name.localeCompare(a.full_name));
      }} else if (sortMode === 'rank_asc') {{
        filtered.sort((a, b) => {{
          const rankA = top5Map[a.full_name] ? top5Map[a.full_name].rank : 999;
          const rankB = top5Map[b.full_name] ? top5Map[b.full_name].rank : 999;
          if (rankA !== rankB) return rankA - rankB;
          return (b.stargazers_count || 0) - (a.stargazers_count || 0);
        }});
      }}

      countBadge.innerText = `顯示 ${{filtered.length}} / ${{allRepos.length}} 個專案`;
      csvBtn.innerText = `📊 匯出 CSV (${{filtered.length}})`;
      jsonBtn.innerText = `📥 匯出 JSON (${{filtered.length}})`;

      if (filtered.length === 0) {{
        tbody.innerHTML = `
          <tr>
            <td colspan="6" style="text-align: center; padding: 3.5rem; color: var(--text-muted);">
              <p style="font-size: 1.15rem; margin-bottom: 0.5rem;">無符合搜尋條件的開源專案</p>
              <p style="font-size: 0.85rem;">請嘗試放寬關鍵字，或點擊「全部領域」與「全部語言」重設篩選條件</p>
            </td>
          </tr>
        `;
        return;
      }}

      let rowsHtml = '';
      filtered.forEach((r, idx) => {{
        const lang = r.primary_language || 'Other';
        const langColor = getLanguageColor(lang);
        const topInfo = top5Map[r.full_name];

        const rowId = 'repo-row-' + r.full_name.replace(/[^a-zA-Z0-9-_]/g, '_');
        const isTop5Row = topInfo ? 'row-top5' : '';

        let rankDisplay = `<span style="color: var(--text-muted); font-size: 0.8rem;">${{idx + 1}}</span>`;
        if (topInfo) {{
          rankDisplay = `
            <div class="rank-medal-badge" title="${{topInfo.categoryName}} ${{topInfo.rankTitle}}">
              ${{topInfo.medal}}
            </div>
          `;
        }}

        const whyRaw = r.analysis ? r.analysis.why : (r.description || '無詳細說明');
        const howRaw = r.analysis ? r.analysis.how : '標準架構與模組化實作';
        const whatRaw = r.analysis ? r.analysis.what : 'CLI 工具與開發者函式庫';

        // Topics rendered cleanly inside Repository column
        const topicPillsHtml = (r.topics || []).slice(0, 4).map(t =>
          `<span class="topic-pill" onclick="filterByTopic('${{t}}')" title="篩選標籤: ${{t}}">#${{t}}</span>`
        ).join('');

        rowsHtml += `
          <tr id="${{rowId}}" class="${{isTop5Row}}">
            <td class="col-rank">${{rankDisplay}}</td>
            <td class="col-name">
              <a href="${{r.url}}" target="_blank" rel="noopener noreferrer" class="table-repo-link">${{r.full_name}} ↗</a>
              <div class="lang-badge">
                <span class="lang-dot" style="background: ${{langColor}};"></span>
                <span>${{lang}}</span>
              </div>
              <div>
                <span class="table-category-tag" onclick="setCategoryFilter('${{r.category_id}}', null)" title="篩選此領域專案">
                  ${{r.category_name}}
                </span>
              </div>
              ${{topicPillsHtml ? `<div style="margin-top: 0.2rem;">${{topicPillsHtml}}</div>` : ''}}
            </td>
            <td class="col-stars">
              <span class="star-chip" title="精確星標數：${{r.stargazers_count.toLocaleString()}}">
                ★ ${{formatNumberJs(r.stargazers_count)}}
              </span>
            </td>
            <td class="col-why">
              <div class="whw-cell-container whw-cell-why">
                <div class="whw-text">${{whyRaw}}</div>
              </div>
            </td>
            <td class="col-how">
              <div class="whw-cell-container whw-cell-how">
                <div class="whw-text">${{howRaw}}</div>
              </div>
            </td>
            <td class="col-what">
              <div class="whw-cell-container whw-cell-what">
                <div class="whw-text">${{whatRaw}}</div>
              </div>
            </td>
          </tr>
        `;
      }});

      tbody.innerHTML = rowsHtml;
    }}

    function formatNumberJs(num) {{
      if (!num) return '0';
      if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
      if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
      return num.toLocaleString();
    }}

    // Initialization
    window.addEventListener('DOMContentLoaded', () => {{
      const savedTheme = localStorage.getItem('theme');
      if (savedTheme === 'light') {{
        document.documentElement.classList.remove('dark');
        document.documentElement.classList.add('light');
      }}
      renderCategoryControls();
      updateSortIndicators();
      renderRepoTable();
    }});
  </script>
</body>
</html>
"""

    with open(config.HTML_OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[✓] Standalone interactive HTML report generated at {config.HTML_OUTPUT_FILE}")
    return config.HTML_OUTPUT_FILE

if __name__ == "__main__":
    generate_html_report()

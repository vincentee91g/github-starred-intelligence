"""
HTML Report Generator for GitHub Starred Repositories Analysis.
Generates an interactive, modern, standalone HTML dashboard in Traditional Chinese (zh-TW).
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
    generate a comprehensive, high-aesthetic zh-TW HTML dashboard, and write to output/index.html.
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
    
    languages = {}
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
  <title>GitHub Starred Repositories 智慧分析與精選儀表板</title>
  <style>
    :root {{
      --bg-primary: #0f172a;
      --bg-secondary: #1e293b;
      --bg-tertiary: #334155;
      --text-primary: #f8fafc;
      --text-secondary: #94a3b8;
      --text-muted: #64748b;
      --border-color: #334155;
      --accent-blue: #38bdf8;
      --accent-purple: #a855f7;
      --accent-amber: #fbbf24;
      --accent-emerald: #34d399;
      --accent-rose: #fb7185;
      --card-bg: rgba(30, 41, 59, 0.7);
      --card-hover: rgba(51, 65, 85, 0.8);
      --glass-border: rgba(255, 255, 255, 0.08);
      --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.2);
      --shadow-md: 0 4px 20px rgba(0, 0, 0, 0.3);
      --shadow-lg: 0 10px 30px rgba(0, 0, 0, 0.4);
    }}

    .light {{
      --bg-primary: #f8fafc;
      --bg-secondary: #ffffff;
      --bg-tertiary: #f1f5f9;
      --text-primary: #0f172a;
      --text-secondary: #475569;
      --text-muted: #94a3b8;
      --border-color: #e2e8f0;
      --card-bg: rgba(255, 255, 255, 0.9);
      --card-hover: rgba(241, 245, 249, 0.9);
      --glass-border: rgba(0, 0, 0, 0.06);
      --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.05);
      --shadow-md: 0 4px 20px rgba(0, 0, 0, 0.08);
      --shadow-lg: 0 10px 30px rgba(0, 0, 0, 0.12);
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
      transition: background-color 0.3s, color 0.3s;
      min-height: 100vh;
    }}

    /* Layout & Header */
    header {{
      background: var(--card-bg);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border-color);
      position: sticky;
      top: 0;
      z-index: 50;
      padding: 1rem 2rem;
    }}

    .header-container {{
      max-width: 1440px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 1.5rem;
      flex-wrap: wrap;
    }}

    .logo-section h1 {{
      font-size: 1.35rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.6rem;
      background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .logo-section p {{
      font-size: 0.82rem;
      color: var(--text-secondary);
      margin-top: 0.2rem;
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 1rem;
    }}

    .theme-toggle, .btn-secondary {{
      background: var(--bg-tertiary);
      border: 1px solid var(--border-color);
      color: var(--text-primary);
      padding: 0.5rem 0.9rem;
      border-radius: 8px;
      cursor: pointer;
      font-size: 0.85rem;
      display: flex;
      align-items: center;
      gap: 0.4rem;
      transition: all 0.2s;
    }}

    .theme-toggle:hover, .btn-secondary:hover {{
      background: var(--border-color);
    }}

    /* Main Container */
    main {{
      max-width: 1440px;
      margin: 2rem auto;
      padding: 0 2rem;
    }}

    /* Hero & KPIs */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 1.25rem;
      margin-bottom: 2.5rem;
    }}

    .kpi-card {{
      background: var(--card-bg);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 1.25rem;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      position: relative;
      overflow: hidden;
    }}

    .kpi-card::after {{
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple));
    }}

    .kpi-title {{
      font-size: 0.82rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-secondary);
      margin-bottom: 0.4rem;
    }}

    .kpi-value {{
      font-size: 1.85rem;
      font-weight: 800;
      color: var(--text-primary);
    }}

    .kpi-desc {{
      font-size: 0.8rem;
      color: var(--text-muted);
      margin-top: 0.3rem;
    }}

    /* Section Headers */
    .section-header {{
      margin-bottom: 1.5rem;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 0.8rem;
    }}

    .section-header h2 {{
      font-size: 1.45rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}

    .section-header p {{
      font-size: 0.88rem;
      color: var(--text-secondary);
      margin-top: 0.2rem;
    }}

    /* Top 3 Section */
    .category-tabs {{
      display: flex;
      gap: 0.5rem;
      overflow-x: auto;
      padding-bottom: 0.8rem;
      margin-bottom: 1.5rem;
      scrollbar-width: thin;
    }}

    .category-tab {{
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      color: var(--text-secondary);
      padding: 0.6rem 1.1rem;
      border-radius: 20px;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}

    .category-tab:hover {{
      border-color: var(--accent-blue);
      color: var(--text-primary);
    }}

    .category-tab.active {{
      background: linear-gradient(135deg, rgba(56, 189, 248, 0.15), rgba(168, 85, 247, 0.15));
      border-color: var(--accent-blue);
      color: var(--text-primary);
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.2);
    }}

    /* Group Overview Card */
    .group-overview-box {{
      background: var(--card-bg);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 1.25rem 1.5rem;
      margin-bottom: 1.5rem;
      box-shadow: var(--shadow-sm);
    }}

    .group-overview-title {{
      font-size: 1rem;
      font-weight: 700;
      margin-bottom: 0.5rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}

    .group-overview-desc {{
      font-size: 0.9rem;
      color: var(--text-secondary);
      margin-bottom: 0.8rem;
      line-height: 1.5;
    }}

    .group-comparison-text {{
      background: var(--bg-tertiary);
      border-left: 3px solid var(--accent-blue);
      padding: 0.75rem 1rem;
      border-radius: 0 8px 8px 0;
      font-size: 0.88rem;
      color: var(--text-primary);
      margin-bottom: 0.8rem;
      line-height: 1.6;
    }}

    /* Top 3 Cards Grid */
    .top3-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
      gap: 1.5rem;
      margin-bottom: 2.5rem;
    }}

    .top3-card {{
      background: var(--card-bg);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 1.5rem;
      box-shadow: var(--shadow-md);
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.2s, border-color 0.2s;
    }}

    .top3-card:hover {{
      transform: translateY(-3px);
      border-color: var(--accent-blue);
    }}

    .top3-rank-badge {{
      position: absolute;
      top: -10px;
      right: 15px;
      padding: 0.25rem 0.75rem;
      border-radius: 12px;
      font-size: 0.75rem;
      font-weight: 700;
      color: #fff;
      box-shadow: var(--shadow-sm);
    }}

    .badge-gold {{ background: linear-gradient(135deg, #f59e0b, #d97706); }}
    .badge-silver {{ background: linear-gradient(135deg, #94a3b8, #64748b); }}
    .badge-bronze {{ background: linear-gradient(135deg, #b45309, #78350f); }}

    .top3-card-header {{
      margin-bottom: 0.8rem;
    }}

    .top3-repo-name {{
      font-size: 1.15rem;
      font-weight: 700;
      margin-bottom: 0.3rem;
    }}

    .top3-repo-name a {{
      color: var(--text-primary);
      text-decoration: none;
      transition: color 0.2s;
    }}

    .top3-repo-name a:hover {{
      color: var(--accent-blue);
    }}

    .top3-meta-chips {{
      display: flex;
      gap: 0.5rem;
      align-items: center;
      margin-bottom: 0.8rem;
    }}

    .star-chip {{
      background: rgba(251, 191, 36, 0.15);
      color: var(--accent-amber);
      padding: 0.2rem 0.5rem;
      border-radius: 6px;
      font-size: 0.78rem;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 0.25rem;
    }}

    .highlight-box {{
      background: rgba(56, 189, 248, 0.08);
      border: 1px dashed rgba(56, 189, 248, 0.3);
      border-radius: 8px;
      padding: 0.75rem;
      font-size: 0.84rem;
      margin-bottom: 1rem;
    }}

    .highlight-box strong {{
      color: var(--accent-blue);
      display: block;
      margin-bottom: 0.2rem;
    }}

    .rationale-text {{
      font-size: 0.85rem;
      color: var(--text-secondary);
      line-height: 1.5;
      margin-bottom: 1rem;
    }}

    /* Explorer Section Controls */
    .controls-bar {{
      background: var(--card-bg);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 1.25rem;
      margin-bottom: 1.5rem;
      display: flex;
      flex-direction: column;
      gap: 1rem;
      box-shadow: var(--shadow-sm);
    }}

    .search-row {{
      display: flex;
      gap: 1rem;
      flex-wrap: wrap;
    }}

    .search-input-wrapper {{
      flex: 1;
      min-width: 280px;
      position: relative;
    }}

    .search-input {{
      width: 100%;
      background: var(--bg-tertiary);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 0.65rem 1rem 0.65rem 2.5rem;
      color: var(--text-primary);
      font-size: 0.9rem;
      outline: none;
      transition: border-color 0.2s;
    }}

    .search-input:focus {{
      border-color: var(--accent-blue);
    }}

    .search-icon {{
      position: absolute;
      left: 0.8rem;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      font-size: 0.9rem;
    }}

    .filter-select {{
      background: var(--bg-tertiary);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 0.65rem 1rem;
      color: var(--text-primary);
      font-size: 0.85rem;
      outline: none;
      cursor: pointer;
    }}

    .chips-row {{
      display: flex;
      gap: 0.4rem;
      flex-wrap: wrap;
    }}

    .filter-chip {{
      background: var(--bg-tertiary);
      border: 1px solid transparent;
      color: var(--text-secondary);
      padding: 0.35rem 0.75rem;
      border-radius: 6px;
      font-size: 0.78rem;
      cursor: pointer;
      transition: all 0.15s;
    }}

    .filter-chip:hover {{
      color: var(--text-primary);
    }}

    .filter-chip.active {{
      background: var(--accent-blue);
      color: #0f172a;
      font-weight: 700;
    }}

    /* Explorer Cards Grid */
    .repo-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 1.25rem;
      margin-bottom: 3rem;
    }}

    .repo-card {{
      background: var(--card-bg);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 1.25rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
    }}

    .repo-card:hover {{
      border-color: rgba(56, 189, 248, 0.4);
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
    }}

    .repo-card-top {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 0.6rem;
      gap: 0.5rem;
    }}

    .repo-name-link {{
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-primary);
      text-decoration: none;
      word-break: break-word;
    }}

    .repo-name-link:hover {{
      color: var(--accent-blue);
    }}

    .repo-category-tag {{
      font-size: 0.72rem;
      padding: 0.15rem 0.5rem;
      border-radius: 4px;
      font-weight: 600;
      white-space: nowrap;
    }}

    .repo-why-how-what {{
      display: flex;
      flex-direction: column;
      gap: 0.6rem;
      margin: 0.8rem 0;
      font-size: 0.85rem;
    }}

    .pill-label {{
      display: inline-block;
      font-size: 0.7rem;
      font-weight: 700;
      padding: 0.1rem 0.4rem;
      border-radius: 4px;
      margin-right: 0.4rem;
      vertical-align: middle;
    }}

    .label-why {{ background: rgba(236, 72, 153, 0.15); color: #f472b6; }}
    .label-how {{ background: rgba(56, 189, 248, 0.15); color: #38bdf8; }}
    .label-what {{ background: rgba(52, 211, 153, 0.15); color: #34d399; }}

    .whw-item {{
      color: var(--text-secondary);
      line-height: 1.45;
    }}

    .repo-footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid var(--border-color);
      padding-top: 0.75rem;
      margin-top: 0.5rem;
      font-size: 0.78rem;
      color: var(--text-muted);
    }}

    .footer-left {{
      display: flex;
      gap: 0.6rem;
      align-items: center;
    }}

    .lang-badge {{
      display: inline-flex;
      align-items: center;
      gap: 0.3rem;
    }}

    .lang-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      display: inline-block;
    }}

    /* Guide Section */
    .guide-card {{
      background: var(--card-bg);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 1.5rem;
      margin-bottom: 3rem;
    }}

    .guide-card h3 {{
      font-size: 1.15rem;
      margin-bottom: 0.6rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}

    .code-block {{
      background: #090d16;
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 1rem;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.85rem;
      color: #38bdf8;
      overflow-x: auto;
      margin: 0.8rem 0;
    }}

    /* Footer */
    footer {{
      border-top: 1px solid var(--border-color);
      padding: 2rem;
      text-align: center;
      font-size: 0.85rem;
      color: var(--text-muted);
      background: var(--card-bg);
    }}

    /* Responsive */
    @media (max-width: 768px) {{
      header {{ padding: 1rem; }}
      main {{ padding: 0 1rem; }}
      .top3-grid, .repo-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>

  <!-- Top Header -->
  <header>
    <div class="header-container">
      <div class="logo-section">
        <h1>🌟 GitHub Starred Repositories 智慧分析儀表板</h1>
        <p>全量 364 個已收藏開源專案 · 10 大技術領域 · 橫向架構對比 · Top 3 榮譽殿堂 (繁體中文 zh-TW)</p>
      </div>
      <div class="header-actions">
        <button class="theme-toggle" id="themeToggleBtn" onclick="toggleTheme()">🌓 切換主題</button>
        <button class="btn-secondary" onclick="exportDataJSON()">📥 匯出 JSON</button>
      </div>
    </div>
  </header>

  <main>

    <!-- Executive KPIs -->
    <section class="kpi-grid">
      <div class="kpi-card">
        <span class="kpi-title">總星標倉庫 (Total Repos)</span>
        <span class="kpi-value">{total_repos:,}</span>
        <span class="kpi-desc">涵蓋個人完整 Starred 軌跡</span>
      </div>
      <div class="kpi-card">
        <span class="kpi-title">總 Stars 累積 (Total Stars)</span>
        <span class="kpi-value">{format_number(total_stars)}★</span>
        <span class="kpi-desc">開源社群總影響力 ({total_stars:,} Stars)</span>
      </div>
      <div class="kpi-card">
        <span class="kpi-title">涵蓋技術領域 (Categories)</span>
        <span class="kpi-value">{len(groups_data)} 大領域</span>
        <span class="kpi-desc">以 AI 智能體、MCP 與代碼智慧為核心</span>
      </div>
      <div class="kpi-card">
        <span class="kpi-title">主要程式語言 (Languages)</span>
        <span class="kpi-value">{sorted_langs[0][0]} / {sorted_langs[1][0]}</span>
        <span class="kpi-desc">{sorted_langs[0][0]} ({sorted_langs[0][1]}), {sorted_langs[1][0]} ({sorted_langs[1][1]}), {sorted_langs[2][0]} ({sorted_langs[2][1]})</span>
      </div>
    </section>

    <!-- Hall of Fame: Top 3 & Group Comparisons -->
    <section id="top3-section">
      <div class="section-header">
        <div>
          <h2>🏆 領域精選 Top 3 榮譽殿堂與橫向架構對比</h2>
          <p>依據開源影響力、架構創新性、工程完整度與實用生產力評選出各領域金、銀、銅牌首選</p>
        </div>
      </div>

      <!-- Category Filter Tabs -->
      <div class="category-tabs" id="categoryTabs">
        <!-- Rendered dynamically -->
      </div>

      <!-- Active Group Overview & Comparison Box -->
      <div class="group-overview-box" id="groupOverviewBox">
        <!-- Rendered dynamically -->
      </div>

      <!-- Top 3 Grid -->
      <div class="top3-grid" id="top3Container">
        <!-- Rendered dynamically -->
      </div>
    </section>

    <!-- All Repositories Interactive Explorer -->
    <section id="explorer-section">
      <div class="section-header">
        <div>
          <h2>🔍 全量 364 倉庫互動檢索與 Why / How / What 詳解</h2>
          <p>即時關鍵字檢索、多領域與程式語言交叉篩選，完整呈現每個專案的創建緣起、技術架構與核心功能</p>
        </div>
        <span id="filteredCountBadge" style="font-size: 0.85rem; color: var(--accent-blue); font-weight: 600;">顯示 364 / 364 個倉庫</span>
      </div>

      <!-- Filter Controls Bar -->
      <div class="controls-bar">
        <div class="search-row">
          <div class="search-input-wrapper">
            <span class="search-icon">🔍</span>
            <input type="text" id="searchInput" class="search-input" placeholder="搜尋專案名稱、作者、Why/How/What 關鍵字、標籤..." oninput="handleSearch()">
          </div>
          <select id="sortSelect" class="filter-select" onchange="handleSort()">
            <option value="stars_desc">⭐ Stars 降序 (預設)</option>
            <option value="stars_asc">⭐ Stars 升序</option>
            <option value="date_desc">📅 收藏時間 (最新優先)</option>
            <option value="date_asc">📅 收藏時間 (最早優先)</option>
            <option value="name_asc">🔤 倉庫名稱 (A-Z)</option>
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

      <!-- Repositories Grid View -->
      <div class="repo-grid" id="repoGrid">
        <!-- Rendered dynamically -->
      </div>
    </section>

    <!-- Incremental Pipeline Guide -->
    <section class="guide-card">
      <h3>🔄 持續增量更新管線說明 (Recurring Incremental Pipeline)</h3>
      <p style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 0.8rem;">
        本系統具備智慧增量同步機制，後續定期執行時會先比對最後收藏時間，只擷取新增或有更新的倉庫，並保留既有快取，秒級完成重新分析與 HTML 儀表板更新。
      </p>
      <div class="code-block">
# 增量更新 (僅檢查並拉取新增的 Starred 倉庫，秒級完成)
python3 main.py --incremental

# 全量強制重新整理 (重新拉取所有 364 個倉庫資料與 README)
python3 main.py --full

# 僅重新生成 HTML 報告
python3 -m src.generator
      </div>
    </section>

  </main>

  <footer>
    <p>GitHub Starred Repos Intelligence Dashboard · 自動建置時間：{generation_time} · Generated by Antigravity</p>
  </footer>

  <!-- Client-side Data and Controller Logic -->
  <script>
    const allRepos = {repos_json};
    const groupsData = {groups_json};

    let activeCategory = Object.keys(groupsData)[0];
    let selectedCategoryFilter = 'all';
    let selectedLanguageFilter = 'all';
    let searchQuery = '';
    let sortMode = 'stars_desc';

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

    // Export Data JSON
    function exportDataJSON() {{
      const blob = new Blob([JSON.stringify(allRepos, null, 2)], {{ type: 'application/json' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `github_starred_analysis_${{new Date().toISOString().slice(0, 10)}}.json`;
      a.click();
    }}

    // Render Category Tabs & Top 3
    function renderCategoryTabs() {{
      const tabsContainer = document.getElementById('categoryTabs');
      const chipsContainer = document.getElementById('categoryChips');
      
      let tabsHtml = '';
      let chipsHtml = '<button class="filter-chip active" onclick="setCategoryFilter(\\'all\\', this)">全部 (All)</button>';

      for (const [catId, g] of Object.entries(groupsData)) {{
        const isActive = catId === activeCategory ? 'active' : '';
        tabsHtml += `
          <button class="category-tab ${{isActive}}" onclick="switchActiveCategory('${{catId}}')">
            <span>${{g.meta.icon}}</span>
            <span>${{g.meta.name}}</span>
            <span style="opacity: 0.7; font-size: 0.75rem;">(${{g.repos.length}})</span>
          </button>
        `;

        chipsHtml += `
          <button class="filter-chip" onclick="setCategoryFilter('${{catId}}', this)">
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
      renderCategoryTabs();
    }}

    function renderActiveGroupOverview() {{
      const g = groupsData[activeCategory];
      if (!g) return;

      const overviewBox = document.getElementById('groupOverviewBox');
      overviewBox.innerHTML = `
        <div class="group-overview-title">
          <span style="font-size: 1.3rem;">${{g.meta.icon}}</span>
          <span>${{g.meta.name}}</span>
          <span style="font-size: 0.8rem; color: var(--accent-blue); font-weight: 600;">（共收錄 ${{g.repos.length}} 個開源專案）</span>
        </div>
        <p class="group-overview-desc">${{g.meta.summary}}</p>
        <div class="group-comparison-text">
          <strong>⚖️ 橫向架構對比與技術差異剖析：</strong><br>
          ${{g.comparison.summary}}
        </div>
        <div style="font-size: 0.82rem; color: var(--text-muted); display: flex; gap: 1rem; flex-wrap: wrap;">
          <span>📌 核心對比維度：${{g.comparison.aspects ? g.comparison.aspects.join(' · ') : '架構選型、適用環境、整合難易度'}}</span>
        </div>
      `;

      // Render Top 3 Cards
      const top3Container = document.getElementById('top3Container');
      let top3Html = '';
      const badgeClasses = ['badge-gold', 'badge-silver', 'badge-bronze'];

      g.top_3.forEach((t, idx) => {{
        const badgeClass = badgeClasses[idx] || 'badge-bronze';
        top3Html += `
          <div class="top3-card">
            <span class="top3-rank-badge ${{badgeClass}}">${{t.rank_title}}</span>
            <div>
              <div class="top3-card-header">
                <div class="top3-repo-name">
                  <a href="${{t.url}}" target="_blank" rel="noopener noreferrer">${{t.full_name}} ↗</a>
                </div>
                <div class="top3-meta-chips">
                  <span class="star-chip">★ ${{t.stargazers_count.toLocaleString()}}</span>
                  <span style="font-size: 0.75rem; color: var(--text-muted);">${{t.badge_type}} Award</span>
                </div>
              </div>

              <div class="highlight-box">
                <strong>🌟 核心技術亮點：</strong>
                ${{t.highlight}}
              </div>

              <p class="rationale-text">
                <strong>💡 評選理由：</strong>${{t.rationale}}
              </p>
            </div>

            <div style="margin-top: 1rem; padding-top: 0.8rem; border-top: 1px dashed var(--border-color); display: flex; justify-content: space-between; align-items: center;">
              <span style="font-size: 0.78rem; color: var(--text-muted);">領域排名 #${{t.rank}}</span>
              <a href="${{t.url}}" target="_blank" rel="noopener noreferrer" style="font-size: 0.82rem; color: var(--accent-blue); text-decoration: none; font-weight: 600;">造訪倉庫 →</a>
            </div>
          </div>
        `;
      }});

      top3Container.innerHTML = top3Html;
    }}

    // Filter & Search Repos
    function setCategoryFilter(catId, btnElem) {{
      selectedCategoryFilter = catId;
      document.querySelectorAll('#categoryChips .filter-chip').forEach(el => el.classList.remove('active'));
      btnElem.classList.add('active');
      renderRepoGrid();
    }}

    function handleSearch() {{
      searchQuery = document.getElementById('searchInput').value.trim().toLowerCase();
      renderRepoGrid();
    }}

    function handleSort() {{
      sortMode = document.getElementById('sortSelect').value;
      renderRepoGrid();
    }}

    function handleLanguageFilter() {{
      selectedLanguageFilter = document.getElementById('languageSelect').value;
      renderRepoGrid();
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
        'Swift': '#F05138',
        'Clojure': '#db5855',
        'Other': '#94a3b8'
      }};
      return colors[lang] || '#94a3b8';
    }}

    function renderRepoGrid() {{
      const grid = document.getElementById('repoGrid');
      const countBadge = document.getElementById('filteredCountBadge');

      let filtered = allRepos.filter(r => {{
        if (selectedCategoryFilter !== 'all' && r.category_id !== selectedCategoryFilter) return false;
        if (selectedLanguageFilter !== 'all' && r.primary_language !== selectedLanguageFilter) return false;
        if (searchQuery) {{
          const searchable = `${{r.full_name}} ${{r.owner}} ${{r.description}} ${{r.analysis.why}} ${{r.analysis.how}} ${{r.analysis.what}} ${{(r.topics || []).join(' ')}}`.toLowerCase();
          if (!searchable.includes(searchQuery)) return false;
        }}
        return true;
      }});

      // Sorting
      if (sortMode === 'stars_desc') {{
        filtered.sort((a, b) => b.stargazers_count - a.stargazers_count);
      }} else if (sortMode === 'stars_asc') {{
        filtered.sort((a, b) => a.stargazers_count - b.stargazers_count);
      }} else if (sortMode === 'date_desc') {{
        filtered.sort((a, b) => (b.starred_at || '').localeCompare(a.starred_at || ''));
      }} else if (sortMode === 'date_asc') {{
        filtered.sort((a, b) => (a.starred_at || '').localeCompare(b.starred_at || ''));
      }} else if (sortMode === 'name_asc') {{
        filtered.sort((a, b) => a.full_name.localeCompare(b.full_name));
      }}

      countBadge.innerText = `顯示 ${{filtered.length}} / ${{allRepos.length}} 個倉庫`;

      if (filtered.length === 0) {{
        grid.innerHTML = `
          <div style="grid-column: 1 / -1; text-align: center; padding: 3rem; color: var(--text-muted);">
            <p style="font-size: 1.2rem; margin-bottom: 0.5rem;">無符合搜尋條件的倉庫</p>
            <p style="font-size: 0.85rem;">請嘗試放寬關鍵字或切換篩選條件</p>
          </div>
        `;
        return;
      }}

      let html = '';
      filtered.forEach(r => {{
        const starDate = r.starred_at ? r.starred_at.slice(0, 10) : 'N/A';
        const lang = r.primary_language || 'N/A';
        const langColor = getLanguageColor(lang);

        html += `
          <div class="repo-card">
            <div>
              <div class="repo-card-top">
                <a href="${{r.url}}" target="_blank" rel="noopener noreferrer" class="repo-name-link">${{r.full_name}} ↗</a>
                <span class="repo-category-tag" style="background: rgba(56, 189, 248, 0.12); color: var(--accent-blue);">
                  ${{r.category_name}}
                </span>
              </div>

              <div class="repo-why-how-what">
                <div class="whw-item">
                  <span class="pill-label label-why">Why 痛點</span>
                  <span>${{r.analysis.why}}</span>
                </div>
                <div class="whw-item">
                  <span class="pill-label label-how">How 架構</span>
                  <span>${{r.analysis.how}}</span>
                </div>
                <div class="whw-item">
                  <span class="pill-label label-what">What 功能</span>
                  <span>${{r.analysis.what}}</span>
                </div>
              </div>
            </div>

            <div class="repo-footer">
              <div class="footer-left">
                <span class="star-chip">★ ${{r.stargazers_count.toLocaleString()}}</span>
                <span class="lang-badge">
                  <span class="lang-dot" style="background: ${{langColor}};"></span>
                  <span>${{lang}}</span>
                </span>
              </div>
              <div>
                <span>★ 收藏日：${{starDate}}</span>
              </div>
            </div>
          </div>
        `;
      }});

      grid.innerHTML = html;
    }}

    // Initialization
    window.addEventListener('DOMContentLoaded', () => {{
      const savedTheme = localStorage.getItem('theme');
      if (savedTheme === 'light') {{
        document.documentElement.classList.remove('dark');
        document.documentElement.classList.add('light');
      }}
      renderCategoryTabs();
      renderRepoGrid();
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

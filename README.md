# GitHub Starred Repositories Intelligence Pipeline 🌟

> **已 Star 開源專案智慧分析與精選儀表板系統**  
> 全量擷取個人已 Starred 的 364 個 GitHub 開源專案，深度萃取每個專案的 **Why (動機痛點)**、**How (技術架構)**、**What (核心功能)** 與 **Stars 數**，劃分為 **20 大精細技術領域**。每一種類皆以**結構化表格**呈現所有專案的完整資訊（告別傳統卡片網格），並由固定代碼評分邏輯遴選出各領域 **Top 5 標竿專案**，結合 LLM 進行深度的**優缺點橫向交叉比對**與**適用場景決策指引**，產出高品質繁體中文 (`zh-TW`) 獨立互動式 HTML 視覺化儀表板。  
>  
> 🌐 **線上即時互動儀表板 (GitHub Pages)**: [https://vincentee91g.github.io/github-starred-intelligence/](https://vincentee91g.github.io/github-starred-intelligence/)

---

## 🚀 核心亮點 (Key Highlights)

- **全量深入剖析 (364 專案)**：透過 `gh` CLI 與 GraphQL 批次查詢，深度解析包括 `anthropics/claude-code`, `openclaw/openclaw`, `deepseek-ai/deepseek-harness`, `mattpocock/skills`, `firecrawl/firecrawl`, `ast-grep/ast-grep`, `tirth8205/code-review-graph` 等在內的 364 個前沿專案。
- **Why / How / What 三維度解析**：
  - **Why 痛點緣起**：為何建立？解決什麼核心技術或業務瓶頸？
  - **How 技術架構**：採用何種方法論、通訊協議、AST 模式或演算法？
  - **What 核心功能**：提供哪些具體 CLI、API、模組或交付成果？
  - **Stars 影響力**：記錄開源社群星標總量（累計超過 1,140 萬顆星）。
- **20 大精細技術領域劃分**：
  1. 🤖 **AI 終端編程 Agent 與官方 CLI 工具** (Autonomous Coding Agents & Official CLI)
  2. 🐝 **多 Agent 協同編排、蜂巢架構與自主組織** (Multi-Agent Swarms & Collaborative Orchestration)
  3. 🏗️ **Agent 執行環境、沙箱隔離與 Harness 鷹架** (Agent Runtimes, Execution Sandboxes & Harnesses)
  4. ⚡ **Claude Code / Codex 核心技能擴展庫** (Claude Code & Codex Core Agent Skills)
  5. 🎨 **前端 UI/UX、動效微調與設計系統 Skills** (UI/UX, Frontend Motion & Design System Skills)
  6. 🛠️ **專項工程領域、工作流程與實戰技能** (Domain-Specific Engineering & Workflow Skills)
  7. 🔌 **MCP 核心協議、官方伺服器與主機生態** (Model Context Protocol - Core Servers & Ecosystem)
  8. 🖥️ **桌面環境接管、系統自動化與 OS MCP** (OS Automation, Computer Use & Desktop MCP Tools)
  9. 📜 **提示詞工程、逆向 System Prompts 與對齊規範** (System Prompts Reverse-Engineering & Prompting)
  10. 📋 **Agent 規範檔案、AGENTS.md 與規格驅動開發** (Agent Specs, AGENTS.md & Spec-Driven Development)
  11. 🔀 **模型路由、API 代理網關與多模型轉發** (Model Routers, API Gateways & Multi-LLM Proxies)
  12. ⏱️ **Token 用量統計、費用監控與選單列看板** (Token Cost Trackers, Quota Monitors & Status Bars)
  13. 🧠 **程式碼語意圖譜、AST 解析與架構審查** (Code Intelligence, AST Parsing & Knowledge Graphs)
  14. 🌐 **智慧網頁採集、文件格式解析與 OCR 轉換** (Web Crawling, Document Extraction & OCR Parsing)
  15. 🎙️ **語音辨識、多模態音訊與影音處理** (Speech Recognition & Multimodal Audio/Video Pipelines)
  16. 💾 **長期記憶層、跨會話持久化與個性化 Memory** (Long-Term Memory, Stateful Context & Personal Memory)
  17. 🔍 **上下文工程、動態壓縮與知識圖譜 RAG** (Context Engineering, Dynamic Compression & GraphRAG)
  18. 📊 **架構圖表可視化、設計系統與 Markdown 簡報** (Architecture Diagrams, Design Systems & Presentations)
  19. 🎓 **頂級電腦科學課程、AI 工程實戰與面試指南** (CS Curricula, AI Engineering Mastery & Interview Kits)
  20. 🚀 **macOS 系統擴展、終端生產力與日常效率工具** (macOS System Tools, Terminal Shell & Productivity Kits)
- **各領域 Top 5 標竿評選與榮譽殿堂**：
  - 依據開源影響力、架構創新性、工程完整度與實戰生產力，評選各組 🥇 冠軍首選、🥈 亞軍精選、🥉 季軍推薦、🏅 殿軍新星、🎖️ 潛力先鋒。
  - **LLM 深度優缺點交叉對比**：針對各領域 Top 5 進行深度的技術哲學、執行環境、資源開銷橫向剖析。
  - **核心優勢 (Pros) 與潛在局限 (Cons)**：為每個入選專案列出客觀的優勢亮點與潛在妥協代價。
  - **適用場景決策指引 (Scenarios)**：具體推薦在何種業務約束、團隊規模或技術棧下該選用何款專案。
- **全量專案表格化呈現 (Table-Based Dashboard)**：
  - 每一種類皆以高密度、美觀舒適的**互動資料表格**呈現（不再使用佔版面的單一專案卡片）。
  - 表格整合即時關鍵字檢索、多欄位點擊排序（Stars、日期、名稱）、語言過濾、以及一鍵匯出 CSV / JSON。
- **固定邏輯程式碼實作**：
  - 數據抓取、增量快取、評分篩選、排序運算、表格渲染與導出全由 Python 與純 JavaScript 程式碼嚴謹實作。
- **極速增量同步管線 (Incremental Pipeline)**：
  - 建立時間戳感知與多級快取的增量架構，後續執行僅同步新 Star 專案，秒級完成。

---

## 📂 目錄結構 (Directory Structure)

```
git_repo/
├── .github/
│   └── workflows/deploy.yml       # GitHub Actions 每日自動排程與 Pages 部署
├── .gitignore                     # Git 忽略規則
├── README.md                      # 專案說明與增量更新指南
├── main.py                        # 主執行入口 (CLI)
├── config.py                      # 全域設定與快取路徑
├── src/
│   ├── __init__.py
│   ├── fetcher.py                 # GitHub CLI 與 GraphQL 批次增量抓取器
│   ├── analyzer.py                # Why / How / What 深度剖析與語意提煉引擎
│   ├── categorizer.py             # 20 大領域分類、固定邏輯評分與 Top 5 評選
│   ├── top5_evaluations.py        # LLM 深度橫向交叉對比、優缺點分析與場景指引
│   └── generator.py               # 繁體中文現代化互動 HTML 表格儀表板生成器
├── tests/                         # 端到端自動化測試套件 (19/19 Passing)
│   ├── run_all_tests.py           # 統一測試執行器
│   ├── test_distribution.py       # 364 倉庫分佈完整性測試
│   ├── test_top5_structure.py     # Top 5 評選與畫像對齊測試
│   ├── test_zero_dependencies.py  # 100% Python 標準庫驗證
│   ├── test_cache_schemas.py      # 快取 JSON Schema 規範驗證
│   └── test_resilience_and_caching.py # 快取容錯與原子自癒測試
├── data/
│   ├── starred_with_dates.json    # 已 Star 倉庫與收藏時間戳記快取
│   ├── repos_cache.json           # 倉庫中繼資料與 README 內文快取
│   ├── analysis_cache.json        # 結構化 Why/How/What 分析資料庫
│   └── groups_cache.json          # 20 大領域群組、架構對比矩陣與 Top 5 評選資料
└── output/
    └── index.html                 # 最終生成的繁體中文互動式獨立表格儀表板
```

---

## 🛠️ 快速開始 (Quick Start)

### 1. 環境需求
- Python 3.10+ (已在 Python 3.14 驗證，僅使用標準庫，零外部依賴)
- [GitHub CLI (`gh`)](https://cli.github.com/) 且已完成登入授權 (`gh auth status`)

### 2. 執行指令

```bash
# 1. 智慧增量同步 (預設：若已有快取則僅檢查新 Star 倉庫，2 秒內完成)
python3 main.py --incremental

# 2. 全量強制重構 (重新從 GitHub API 擷取所有 364 個倉庫資料與 README)
python3 main.py --full

# 3. 僅重新渲染 HTML 表格儀表板 (不發送任何網路請求)
python3 main.py --generate-only
```

### 3. 開啟儀表板

生成之 HTML 報告位於 `output/index.html`，可直接以瀏覽器開啟：

```bash
open output/index.html
```

---

## 🔄 持續維護與定期自動化 (Recurring Automation)

若要定期每日或每週自動同步新增的 GitHub Stars，可透過系統 `cron` 或配置 GitHub Actions 工作流：

### macOS / Linux 定期排程 (crontab)
```bash
# 每天午夜 12:00 自動進行增量同步
0 0 * * * cd /Users/vincentee91g/Project/git_repo && python3 main.py --incremental >> sync.log 2>&1
```

---

## 📊 成果預覽 (Dashboard Preview)

儀表板提供：
1. **大盤數據指標**：364 總專案數、1,140 萬+ 總星標數、20 大精細領域分佈、程式語言統計。
2. **Top 5 榮譽殿堂**：點擊 20 大領域切換 Tab，即時查看各領域 Top 5 專案、核心技術亮點、評選理由、✅ 專案優勢與 ⚠️ 潛在缺點。
3. **橫向架構對比與場景推薦**：詳細展現同領域各專案的優缺點交叉比對與決策選型指引。
4. **全量 364 專案表格化檢索**：徹底告別卡片式介面，以結構化表格清晰羅列專案名稱、Stars、Why 痛點、How 架構、What 功能與標籤，支援即時搜尋、欄位排序與 CSV/JSON 匯出。

---

## 🧪 端到端自動化測試與管線驗證 (Automated Verification)

本管線具備完整的單元測試與端到端驗證套件，嚴格保證零第三方依賴、快取 Schema 一致性與 364 倉庫 20 大分類無缺漏：

```bash
# 執行全部 19 項自動化驗證測試
python3 tests/run_all_tests.py

# 或使用標準 unittest 模組自動發現
python3 -m unittest discover -s tests
```

驗證範圍包括：
- **分佈完整性**：全量 364 倉庫在 20 大分類中 100% 覆蓋，無一遺漏或重複。
- **Top 5 結構完整性**：20 大分類各含完整 Top 5（共 100 專案），每筆皆含 `pros`, `cons`, `scenarios`, `highlight`, `rationale`。
- **快取 Schema 合規性**：`analysis_cache.json`、`groups_cache.json`、`repos_cache.json` 與 `starred_with_dates.json` 結構校驗。
- **零第三方依賴**：100% 僅使用 Python 3 標準庫（`json`, `re`, `subprocess`, `argparse`, `pathlib`, `unittest` 等）。
- **容錯與自癒機制**：模擬快取遺失、缺損欄位、原子化寫入保護與離線降級。

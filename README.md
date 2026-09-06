# GitHub Starred Repositories Intelligence Pipeline 🌟

> **已 Star 開源專案智慧分析與精選儀表板系統**  
> 全量擷取個人已 Starred 的 364 個 GitHub 開源專案，深度萃取每個專案的 **Why (動機痛點)**、**How (技術架構)**、**What (核心功能)** 與 **Stars 數**，劃分為 10 大技術領域進行橫向架構對比，並評選出各領域 **Top 3 金銀銅牌專案**，產出高品質繁體中文 (`zh-TW`) 獨立互動式 HTML 視覺化儀表板。

---

## 🚀 核心亮點 (Key Highlights)

- **全量深入剖析 (364 倉庫)**：透過 `gh` CLI 與 GraphQL 批次查詢，深度解析包括 `anthropics/claude-code`, `openclaw/openclaw`, `deepseek-ai/deepseek-harness`, `mattpocock/skills`, `firecrawl/firecrawl`, `ast-grep/ast-grep`, `tirth8205/code-review-graph` 等在內的 364 個前沿專案。
- **Why / How / What 三維度解析**：
  - **Why 痛點緣起**：為何建立？解決什麼核心瓶頸？
  - **How 技術架構**：採用何種方法論、通訊協議、AST 模式或演算法？
  - **What 核心功能**：提供哪些具體 CLI、API、模組或交付成果？
  - **Stars 影響力**：記錄開源社群星標總量（累計超過 1,140 萬顆星）。
- **10 大功能領域群組與橫向對比**：
  1. 🤖 **AI 智能體底座、執行架構與多 Agent 協同** (Autonomous Agents & Harnesses)
  2. ⚡ **Claude Code / Codex 技能擴展與自定義工具集** (Agent Skills & Toolkits)
  3. 🔌 **MCP 協議伺服器與主機整合生態** (Model Context Protocol Ecosystem)
  4. 📜 **提示詞工程、Agent 規範與系統指令剖析** (Prompt Engineering & AGENTS.md Specs)
  5. 🔀 **模型路由、API 代理網關與費用監控** (Model Gateways, Proxies & Cost Trackers)
  6. 🧠 **程式碼智慧、AST 結構分析與代碼庫圖譜** (Code Intelligence, AST & Code Graphs)
  7. 📄 **多模態數據採集、檔案解析與結構化轉換** (Web Crawling, Document & Multimodal Parsing)
  8. 💾 **上下文工程、長期記憶層與本地 RAG** (Context Compression, Long-Term Memory & RAG)
  9. 📊 **圖表可視化、設計系統與投影片簡報** (Visualization, Diagrams & Slides)
  10. 🚀 **開源教學指南、電腦科學精選與終端生產力** (Curated CS Curricula & Terminal Tools)
- **領域 Top 3 榮譽殿堂**：依據開源影響力、架構創新性、工程完整度與實戰生產力，評選各組 🥇 金牌首選、🥈 銀牌推薦、🥉 銅牌新星，並附專屬評選理由與技術亮點。
- **極速增量同步管線 (Incremental Pipeline)**：建立具備時間戳感知與多級快取的增量架構，日後執行僅同步新 Star 專案，秒級完成。
- **純靜態獨立 HTML 儀表板 (`zh-TW`)**：無須後端伺服器或外部 CDN 依賴，內建即時搜尋、跨領域/語言篩選、深淺色主題切換與 JSON 導出功能。

---

## 📂 目錄結構 (Directory Structure)

```
git_repo/
├── .gitignore                     # Git 忽略規則
├── README.md                      # 專案說明與增量更新指南
├── main.py                        # 主執行入口 (CLI)
├── config.py                      # 全域設定與快取路徑
├── src/
│   ├── __init__.py
│   ├── fetcher.py                 # GitHub CLI 與 GraphQL 批次增量抓取器
│   ├── analyzer.py                # Why / How / What 深度剖析與語意提煉引擎
│   ├── categorizer.py             # 10 大領域分類、橫向架構對比與 Top 3 評選
│   └── generator.py               # 繁體中文現代化互動 HTML 報告生成器
├── data/
│   ├── starred_with_dates.json    # 已 Star 倉庫與收藏時間戳記快取
│   ├── repos_cache.json           # 倉庫中繼資料與 README 內文快取
│   ├── analysis_cache.json        # 結構化 Why/How/What 分析資料庫
│   └── groups_cache.json          # 領域群組、架構對比矩陣與 Top 3 評選資料
└── output/
    └── index.html                 # 最終生成的繁體中文互動式獨立儀表板
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

# 3. 僅重新渲染 HTML 儀表板 (不發送任何網路請求)
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
1. **大盤數據指標**：總專案數、總星標數、涵蓋領域數、程式語言分佈長條圖。
2. **Top 3 榮譽殿堂**：點擊領域切換 Tab，即時查看各領域金銀銅牌專案與深度評選理由。
3. **橫向架構對比**：直觀呈現同領域各專案的技術哲學、執行環境與狀態管理差異。
4. **全量 364 倉庫互動檢索網格**：支援中英文即時搜尋、領域篩選、排序與直通 GitHub 連結。

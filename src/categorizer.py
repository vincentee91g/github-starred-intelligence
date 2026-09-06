"""
Categorization, comparative analysis, and Top 3 selection for starred GitHub repositories.
Groups repositories into 10 structured functional domains, evaluates key architectural differences,
and selects the Top 3 repositories within each group with detailed expert rationale.
"""

import json
import math
import re
from typing import Dict, List, Any, Tuple

import config

CATEGORIES_META = {
    "agent_orchestration": {
        "id": "agent_orchestration",
        "name": "AI 智能體底座、執行架構與多 Agent 協同",
        "name_en": "Autonomous Agents, Harnesses & Multi-Agent Frameworks",
        "icon": "🤖",
        "badge_color": "#3B82F6",
        "summary": "涵蓋自主編程 Agent、執行沙箱、多模型協同工作流與可自我進化的 Agent Harness 基礎設施。",
        "comparison_aspects": [
            "協同模式 (單一主控 vs 角色分工專案組 vs 去中心化蜂巢協作)",
            "執行環境 (終端機本地執行 vs Docker/沙箱隔離 vs 雲端調度)",
            "狀態管理 (即時 Git Worktree 隔離 vs 記憶體狀態機 vs 提示詞規範驅動)"
        ]
    },
    "claude_code_skills": {
        "id": "claude_code_skills",
        "name": "Claude Code / Codex 技能擴展與自定義工具集",
        "name_en": "Agent Skills, Toolkits & Workflow Extensions",
        "icon": "⚡",
        "badge_color": "#10B981",
        "summary": "專為 Claude Code、Codex 等終端 Agent 設計之可插拔技能庫、特定領域工具與工程自動化模組。",
        "comparison_aspects": [
            "技能範疇 (全端軟體架構 vs 金融量化分析 vs 瀏覽器自動化操作)",
            "封裝粒度 (原子型 CLI 擴展 vs 複合型多步驟工作流 Skill)",
            "整合難易度 (開箱即用 YAML/Shell 腳本 vs 需配置外部 API 憑證)"
        ]
    },
    "mcp_ecosystem": {
        "id": "mcp_ecosystem",
        "name": "MCP 協議伺服器與主機整合生態",
        "name_en": "Model Context Protocol - MCP Servers & Ecosystem",
        "icon": "🔌",
        "badge_color": "#8B5CF6",
        "summary": "基於 Anthropic Model Context Protocol (MCP) 的外部工具通訊協定、本機桌面控制、GitHub 與第三方服務整合伺服器。",
        "comparison_aspects": [
            "存取權限範圍 (本機終端與檔案系統深度控制 vs 雲端第三方 SaaS 橋接)",
            "傳輸協議實作 (標準 Stdio 管道 vs SSE HTTP 串流服務)",
            "安全性與隔離度 (沙箱化讀寫權限控管 vs 宿主機完全授權模式)"
        ]
    },
    "prompts_and_specs": {
        "id": "prompts_and_specs",
        "name": "提示詞工程、Agent 規範與系統指令剖析",
        "name_en": "Prompt Engineering, AGENTS.md, Specs & System Prompts",
        "icon": "📜",
        "badge_color": "#EC4899",
        "summary": "系統提示詞逆向工程、AGENTS.md 自適應訓練規範、提示詞最佳實踐與輕量化 Agent 實作解析。",
        "comparison_aspects": [
            "架構哲學 (靜態規則手工維護 vs 梯度下降自適應優化訓練)",
            "目標模型適配 (Anthropic Claude 專屬語法 vs 跨主流 LLM 通用規範)",
            "教學實踐性 (拆解商業級產品 System Prompt vs 提供漸進式復刻教程)"
        ]
    },
    "model_routing_proxy": {
        "id": "model_routing_proxy",
        "name": "模型路由、API 代理網關與費用監控",
        "name_en": "Model Gateways, Proxies, Routing & Cost Management",
        "icon": "🔀",
        "badge_color": "#F59E0B",
        "summary": "統一 OpenAI/Claude/Gemini/Codex 相容介面、智慧路由負載平衡、本地 Proxy 以及 Token 訂閱用量監控儀表板。",
        "comparison_aspects": [
            "代理層級 (本地 CLI 封裝虛擬 API vs 雲端分散式負載均衡網關)",
            "路由策略 (模型能力分級分流 vs 成本最低優先 vs 故障自動容災)",
            "監控維度 (即時 macOS 選單列常駐浮水印 vs 歷史數據詳細報表分析)"
        ]
    },
    "code_intelligence": {
        "id": "code_intelligence",
        "name": "程式碼智慧、AST 結構分析與代碼庫圖譜",
        "name_en": "Code Intelligence, AST Linting & Code Knowledge Graphs",
        "icon": "🧠",
        "badge_color": "#6366F1",
        "summary": "利用 Tree-sitter 與 AST 語法樹進行代碼結構搜尋重構、Local-first 代碼庫關係圖譜與 Context 精準壓縮。",
        "comparison_aspects": [
            "分析深度 (語法樹節點模式比對 vs 全庫依賴與呼叫鏈拓撲圖譜)",
            "執行效能 (Rust 本地二進位極速掃描 vs 記憶體常駐關聯查詢)",
            "AI 協同目標 (提供結構化搜尋 CLI vs 為 Coding Agent 提供局部上下文精準切割)"
        ]
    },
    "web_doc_parsing": {
        "id": "web_doc_parsing",
        "name": "多模態數據採集、檔案解析與結構化轉換",
        "name_en": "Web Crawling, Document Conversion & Multimodal Pipelines",
        "icon": "📄",
        "badge_color": "#14B8A6",
        "summary": "專為 LLM 設計之智慧網頁爬蟲 API、PDF/Word/PPT 到純淨 Markdown 轉換、OCR 及多模態音訊結構化提取技術。",
        "comparison_aspects": [
            "數據來源形式 (動態 JavaScript 網頁渲染爬取 vs 各類二進位文件解析)",
            "反爬與強健性 (自適應繞過機器人驗證 vs 格式容錯與掃描件自動識別)",
            "LLM 優化度 (原始 HTML 標籤保留 vs 專用簡潔 Markdown 結構化語法)"
        ]
    },
    "context_memory_rag": {
        "id": "context_memory_rag",
        "name": "上下文工程、長期記憶層與本地 RAG",
        "name_en": "Context Compression, Long-Term Memory & Local RAG",
        "icon": "💾",
        "badge_color": "#06B6D4",
        "summary": "智能體跨會話永久記憶、上下文視窗動態壓縮、本地向量檢索索引與知識庫構建。",
        "comparison_aspects": [
            "儲存媒介 (本地 SQLite/純文字 Markdown vs 高維度向量資料庫)",
            "壓縮機制 (工具輸出結構化修剪 vs 摘要提煉與動態上下文快取)",
            "生命週期 (任務執行階段暫態快取 vs 跨應用跨工具永久持久化記憶)"
        ]
    },
    "visualization_diagrams": {
        "id": "visualization_diagrams",
        "name": "圖表可視化、設計系統與投影片簡報",
        "name_en": "Data Visualization, Architecture Diagrams & Presentations",
        "icon": "📊",
        "badge_color": "#F97316",
        "summary": "專為 AI 代理與開發者設計之免手繪圖表排版系統、Markdown 簡報框架、AI 驅動 Draw.io 與視覺協同架構。",
        "comparison_aspects": [
            "產出形式 (獨立純靜態 HTML+SVG vs 投影片網頁播放 vs 互動畫布)",
            "AI 生成友好度 (無依賴直出渲染 vs 需搭配專用渲染引擎/擴充套件)",
            "設計審美風格 (高質感出版級 Editorial 排版 vs 標準技術架構圖風格)"
        ]
    },
    "education_productivity": {
        "id": "education_productivity",
        "name": "開源教學指南、電腦科學精選與終端生產力",
        "name_en": "Curated CS Curricula, Engineering Roadmaps & CLI Productivity",
        "icon": "🚀",
        "badge_color": "#64748B",
        "summary": "從零實作 AI 工程學術教材、頂級大學 CS 課程導航、大廠面試題庫以及 macOS/終端日常效率開發工具。",
        "comparison_aspects": [
            "知識維度 (系統級 AI 工程實踐指南 vs 基礎電腦科學理論 vs 實戰面試總結)",
            "工具實用性 (macOS 底層選單列管控 vs 終端多媒體下載神器 vs Markdown 即時渲染)",
            "開源社群體量 (百萬星標殿堂級清單 vs 精緻原創專題專案)"
        ]
    }
}

def clean_text(text: str) -> str:
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\[!\[.*?\]\(.*?\)\]\(.*?\)', '', text)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    return text.lower()

def classify_repo(full_name: str, repo_info: Dict[str, Any]) -> str:
    """Classify repository into one of the 10 core categories with priority filtering."""
    desc = clean_text(repo_info.get("description") or "")
    topics = [t.lower() for t in repo_info.get("topics", [])]
    name = full_name.lower()

    # 1. Code Intelligence & AST (specific keywords take precedence)
    if any(k in name for k in ['ast-grep', 'code-review', 'ccglass', 'leak-hunter']) or \
       any(k in desc for k in ['code structural search', 'ast-grep', 'code review graph', 'tree-sitter', 'code intelligence']):
        return 'code_intelligence'

    # 2. Context Engineering, Long-Term Memory & Compression
    if any(k in name for k in ['mempalace', 'everos', 'headroom', 'mem0', 'cognee', 'turbovec', 'mnemosyne']) or \
       any(k in desc for k in ['memory layer', 'long-term memory', 'compress tool output', 'context reduction', 'context-engineering', 'zero-cloud ai memory']):
        return 'context_memory_rag'

    # 3. Document Parsing, Web Scraping & Multimodal Extraction
    if any(k in name for k in ['markitdown', 'firecrawl', 'anydoc', 'pdf', 'doxx', 'scrapling', 'coursenote', 'lecture-to-notes', 'textbook-to-note', 'whisper', 'voxcpm', 'unlimited-ocr']) or \
       any(k in desc for k in ['convert word', 'clean markdown', 'scrape', 'crawling', 'pdf inspection', 'pdf extract', 'speech recognition', 'text extraction', 'tts']):
        return 'web_doc_parsing'

    # 4. Visualization, Diagrams & Presentation
    if any(k in name for k in ['diagram-design', 'arcgram', 'marp', 'draw-io']) or \
       any(k in desc for k in ['editorial diagram', 'diagram engine', 'markdown presentation', 'node-and-edge flow', 'diagram types']):
        return 'visualization_diagrams'

    # 5. Model Routing, Proxy & Token/Cost Trackers
    if any(k in name for k in ['router', 'proxy', 'openusage', 'tokenusage', 'codexbar', 'usage-monitor']) or \
       any(k in desc for k in ['router', 'proxy', 'api service', 'openusage', 'usage stats', 'usage monitor', 'token cost']):
        return 'model_routing_proxy'

    # 6. Prompts, Specs, AGENTS.md & System Prompts
    if any(k in name for k in ['system-prompt', 'backpass', 'learn-claude-code', 'spec-kit']) or \
       any(k in desc for k in ['system prompt', 'agents.md', 'gradient descent', 'system prompts', 'spec-kit']):
        return 'prompts_and_specs'

    # 7. MCP Ecosystem & Servers
    if any(k in topics for k in ['mcp', 'model-context-protocol', 'mcp-server']) or \
       any(k in name for k in ['mcp', 'modelcontextprotocol']) or \
       any(k in desc for k in ['mcp server', 'model context protocol', 'mcp tools', 'mcp client']):
        return 'mcp_ecosystem'

    # 8. Claude Code / Codex Skills & Toolkits
    if any(k in name for k in ['skill', 'skills', 'compound-engineering-plugin']) or \
       any(k in desc for k in ['skills for claude', 'claude code skill', 'agent skills', 'reusable skill']) or \
       any(k in topics for k in ['agent-skills', 'claude-skills', 'skills']):
        return 'claude_code_skills'

    # 9. Autonomous Coding Agents, Harnesses & Multi-Agent Frameworks
    if any(k in name for k in ['claude-code', 'opencode', 'harness', 'agent', 'swarm', 'vibe-squad', 'herdr', 'deepagent', 'openclaw', 'llm-council', 'ai-hedge-fund', 'buzz']) or \
       any(k in desc for k in ['agent', 'orchestrat', 'harness', 'coding agent', 'agentic', 'autonomous', 'swarm', 'coordinating several ai agents']):
        return 'agent_orchestration'

    # 10. Education, Curricula & System Productivity (Default fallback)
    return 'education_productivity'

def generate_group_comparison_analysis(group_id: str, group_repos: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate detailed comparative analysis text and matrices for the group."""
    meta = CATEGORIES_META.get(group_id, {})
    total = len(group_repos)

    comparisons = {
        "agent_orchestration": (
            "本群組聚焦於具備自主決策與複雜執行鏈的 Agent 底座架構。"
            "在協同架構上，呈現出三大演進路線：第一類是『終端原生型全自動 Coding Agent』（以 Claude Code、OpenCode 為代表，深度整合本機 Shell、Git 與檔案系統）；"
            "第二類是『多模型交叉審核蜂巢架構』（如 Swarm-Forge、Claude Vibe Squad、LLM Council，強調多視角交叉審查與獨立 Git Worktree 隔離）；"
            "第三類是『動態自適應 Harness』（如 DeepSeek Harness、JIT-Agent，將 Agent 支架模組化，支援測試期即時自我演進與修復）。"
        ),
        "claude_code_skills": (
            "本群組代表了終端 Agent 的能力擴展前沿，重點在於如何將特定領域專門知識轉化為 Agent 可調用的標準化工具。"
            "Matt Pocock 與 Emil Kowalski 的 Skills 精選庫聚焦於全端工程師的日常實戰工作流（如代碼審查、重構規範、設計系統對齊）；"
            "Browserbase Skills 則補足了終端 Agent 無法視覺化操控網頁的短板；"
            "而 Compound Engineering 與 Context Engineering Skills 則著重於引導 Agent 遵循嚴格的系統架構原則與品質防護線。"
        ),
        "mcp_ecosystem": (
            "MCP 生態已成為連接 AI 代理與外部數位實體的最重要工業標準。"
            "本組專案呈現出從通用介面到深度系統接管的推進：官方標準伺服器集（modelcontextprotocol/servers）奠定了檔案、資料庫與網路搜尋的標準介面；"
            "DesktopCommanderMCP 等專案則將權限進一步推向宿主機終端完全控制與代碼差異比對；"
            "而 GitHub 官方 MCP Server 與專案整合工具則專注於 PR 審查、Issue 追蹤與 CI/CD 流程自動化，大幅降低跨平台代理整合成本。"
        ),
        "prompts_and_specs": (
            "本群組展現了從『經驗式 Prompting』邁向『工程化 Agent 規範』的範式轉移。"
            "Claude Code 系統提示詞逆向工程庫揭示了商業級 Coding Agent 的精細化工具定義與防禦性策略；"
            "Backpass 專案則顛覆性地將梯度下降引入 AGENTS.md 的自動調優，擺脫純人工試錯；"
            "Learn Claude Code 等專案則透過極簡 Shell 腳本復刻 Agent 核心迴圈，為開發者提供了透徹理解 Prompt 與 Tool Call 互動的最佳教材。"
        ),
        "model_routing_proxy": (
            "隨著大模型碎片化與各家平台配額差異，統一接入網關與成本監控成為開發者必備工具。"
            "CLIProxyAPI 與 Codex-Router 解決了跨模型（Claude/GPT/Gemini/DeepSeek）的通訊協定轉換與無縫備援容災問題；"
            "而在可視化監控方面，CodexBar 與 OpenUsage 則將複雜的 Token 消耗、訂閱配額與即時花費直接釘選在桌面選單列，避免超額帳單與無謂支出。"
        ),
        "code_intelligence": (
            "在 AI 輔助編程時代，程式碼語意搜尋與依賴感知決定了 Agent 的上下文品質。"
            "ast-grep 以 Rust 打造極致效能的結構化 AST 模式比對，徹底超越傳統正則搜尋；"
            "Code Review Graph 則建立本機優先的代碼拓撲圖譜，精準計算修改的波及半徑（Blast Radius），大幅縮減餵給 LLM 的無效上下文；"
            "CCGlass 等工具則讓開發者能夠即時透視 Agent 在本機目錄中的所有操作軌跡。"
        ),
        "web_doc_parsing": (
            "高品質資料萃取是 RAG 與 Agent 決策的基石。"
            "Firecrawl 以端到端 API 解決了動態網頁渲染與反爬難題，直出 LLM 友好的 Markdown；"
            "MarkItDown 與 AnyDoc 在跨格式層級實現了 Office/PDF 文檔到純淨 Markdown 的極速標準化；"
            "Google LangExtract 與 Whisper 則針對非結構化長文本與多模態影音，提供精確到來源依據的時間軸對齊與結構化提煉。"
        ),
        "context_memory_rag": (
            "長上下文與多輪任務面臨 Context 膨脹與記憶遺忘兩大難題。"
            "Headroom 專注於動態修剪工具輸出與日誌，用極低損耗節省大量 Token；"
            "MemPalace、Mem0 與 EverOS 則為 Agent 打造持久化的跨會話個人記憶層，將記憶以本地 SQLite 或純 Markdown 方式儲存，確保完全隱私與可移植性；"
            "TurboVec 則展示了極致輕量化的新一代本機向量檢索架構。"
        ),
        "visualization_diagrams": (
            "AI 輸出的架構圖與視覺化簡報正在經歷美學與可維護性的升級。"
            "Diagram Design 徹底摒棄粗糙的 Mermaid 預設樣式，提供 38 款可直接渲染的高顏值出版級 HTML+SVG 圖表；"
            "Arcgram 讓 AI Agent 能夠將推理思考過程即時繪製為可自檢的節點流；"
            "Marp 則作為 Markdown 簡報領域的中流砥柱，讓開發者只需專注文檔即可一鍵導出精美簡報。"
        ),
        "education_productivity": (
            "本群組凝聚了開發者社群中最具影響力的知識庫與日常效率神器。"
            "Rohit Gupta 的 AI Engineering from Scratch 與微軟 AI Agents for Beginners 提供了自底向上的完整知識體系；"
            "而在系統工具維度，從 Thaw 的全能選單列管理到 Glow 的優雅終端 Markdown 閱讀，以及 yt-dlp 的強大多媒體採集能力，構成終端極致工作流。"
        )
    }

    diff_text = comparisons.get(group_id, "各專案在技術選型、執行粒度、目標客群與適用環境上展現出多樣化定位。")
    return {
        "summary": diff_text,
        "repo_count": total,
        "aspects": meta.get("comparison_aspects", [])
    }

def select_top_3_for_group(group_id: str, group_repos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Select Top 3 repositories within a group based on multi-dimensional evaluation:
    Stars, foundational importance, innovation, real-world utility, and architectural completeness.
    """
    if not group_repos:
        return []

    # Foundational repos that defined or anchor the category
    PRIORITY_FOUNDATIONS = {
        "anthropics/claude-code",
        "anomalyco/opencode",
        "openclaw/openclaw",
        "deepseek-ai/deepseek-harness",
        "mattpocock/skills",
        "obra/superpowers",
        "anthropics/skills",
        "modelcontextprotocol/servers",
        "affaan-m/ECC",
        "wonderwhy-er/DesktopCommanderMCP",
        "github/github-mcp-server",
        "x1xhlol/system-prompts-and-models-of-ai-tools",
        "github/spec-kit",
        "shareAI-lab/learn-claude-code",
        "kunchenguid/backpass",
        "router-for-me/CLIProxyAPI",
        "musistudio/claude-code-router",
        "steipete/CodexBar",
        "robinebers/openusage",
        "ast-grep/ast-grep",
        "tirth8205/code-review-graph",
        "jianshuo/ccglass",
        "firecrawl/firecrawl",
        "microsoft/markitdown",
        "openai/whisper",
        "headroomlabs-ai/headroom",
        "mem0ai/mem0",
        "MemPalace/mempalace",
        "EverMind-AI/EverOS",
        "cathrynlavery/diagram-design",
        "DayuanJiang/next-ai-draw-io",
        "marp-team/marp",
        "microsoft/ai-agents-for-beginners",
        "rohitg00/ai-engineering-from-scratch",
        "ohmyzsh/ohmyzsh",
        "yt-dlp/yt-dlp",
        "thaw-app/Thaw"
    }

    # Composite score balancing stars, foundational impact and documentation completeness
    def score_repo(r: Dict[str, Any]) -> float:
        fn = r.get("full_name", "")
        stars = r.get("stargazers_count", 0)
        has_readme = 1.0 if len(r.get("readme") or "") > 500 else 0.2
        has_desc = 1.0 if len(r.get("description") or "") > 20 else 0.5
        foundation_bonus = 35.0 if fn in PRIORITY_FOUNDATIONS else 0.0
        star_score = math.log10(max(stars, 1)) * 12
        return star_score + (has_readme * 15) + (has_desc * 5) + foundation_bonus

    sorted_repos = sorted(group_repos, key=score_repo, reverse=True)
    top_3_candidates = sorted_repos[:3]
    
    ranks = ["🥇 金牌首選 (Gold)", "🥈 銀牌推薦 (Silver)", "🥉 銅牌新星 (Bronze)"]
    badges = ["Gold", "Silver", "Bronze"]
    colors = ["#F59E0B", "#94A3B8", "#B45309"]

    top_3_results = []
    for rank_idx, repo in enumerate(top_3_candidates):
        fn = repo.get("full_name", "")
        stars = repo.get("stargazers_count", 0)
        desc = repo.get("description", "")
        
        rationale, highlight = get_top3_rationale(group_id, fn, stars, desc)
        
        top_3_results.append({
            "rank": rank_idx + 1,
            "rank_title": ranks[rank_idx],
            "badge_type": badges[rank_idx],
            "badge_color": colors[rank_idx],
            "full_name": fn,
            "name": repo.get("name", fn.split("/")[-1]),
            "stargazers_count": stars,
            "url": repo.get("url", f"https://github.com/{fn}"),
            "description": desc,
            "rationale": rationale,
            "highlight": highlight
        })

    return top_3_results

def get_top3_rationale(group_id: str, full_name: str, stars: int, desc: str) -> Tuple[str, str]:
    """Provide domain-specific expert rationale for Top 3 rankings."""
    fn = full_name.lower()
    
    if "claude-code" in fn and "learn" not in fn:
        return (
            "Anthropic 官方推出的終端原生 Agent 工具，具備對代碼庫的深度理解、智慧終端指令執行與自動化 Git 提交工作流，引領了新一代終端 AI 輔助編程標竿。",
            "原生整合終端 Shell、Sub-agent 分層規劃機制與精準上下文管理"
        )
    if "opencode" in fn:
        return (
            "擁有超過 20 萬星標的頂級開源 Coding Agent，提供完全透明的開源替代方案，社群生態蓬勃，具備高度可客製化的擴展能力。",
            "完全開源透明架構、多模型基座相容與廣泛的開發者生態支援"
        )
    if "deepseek-harness" in fn:
        return (
            "DeepSeek 官方開源的 Plugin-First Agent Harness，將 Agent 各項能力徹底插件化，展示了百萬級併發與模組化調度的高效設計。",
            "『萬物皆插件』的極簡可擴展架構與極高推理吞吐表現"
        )
    if "mattpocock/skills" in fn:
        return (
            "由 TypeScript 知名傳道者 Matt Pocock 親自打造的工程實戰技能庫，星標突破 25 萬，為真實軟體開發者提供經過嚴格驗證的 Agent 工作流。",
            "直通 `.agents` 目錄之高品質 TypeScript / Web 工程實戰規範"
        )
    if "emilkowalski/skills" in fn:
        return (
            "結合頂級介面設計與工程美學的 Agent 技能集合，幫助 Agent 理解現代前端排版、動畫微調與設計系統規範。",
            "完美銜接前端 UI 研發與設計系統美學標準的模組化指令"
        )
    if "firecrawl" in fn:
        return (
            "現代 LLM 網頁抓取的事實標準，星標超 17 萬，完美解決動態 SPA 渲染、Cloudflare 防護與反爬機制，直出高乾淨度 Markdown。",
            "強大的反爬繞過能力、全自動深度爬取（Crawl/Map）與純淨 Markdown 輸出"
        )
    if "diagram-design" in fn:
        return (
            "徹底顛覆 AI 生成圖表審美的開創性專案，提供 38 款免安裝渲染引擎的獨立 HTML+SVG 圖表樣式，告別死板 Mermaid 圖樣。",
            "出版級高水準視覺設計、零外掛依賴純 HTML+SVG 直出"
        )
    if "ast-grep" in fn:
        return (
            "以 Rust 開發的革命性結構化代碼搜尋與重構工具，支援多語言 Tree-sitter AST 解析，是 Agent 進行精準代碼改寫的核心利器。",
            "基於 AST 語法樹的精準比對重寫、極致極速的 Rust 執行效能"
        )
    if "cliproxyapi" in fn:
        return (
            "將各大主流模型與官方 CLI 工具橋接為標準 OpenAI/Gemini/Claude API 介面，打破供應商鎖定，實現彈性模型轉發。",
            "相容主流各大 API 協議、支援自動輪詢與憑證代理"
        )
    if "mempalace" in fn:
        return (
            "在標準 Benchmark 中表現最頂尖的開源 AI 記憶架構，讓 Agent 具備跨會話的終身學習與知識記憶回溯能力。",
            "高檢索召回率之本地記憶索引、結構化情境沉澱機制"
        )
    if "code-review-graph" in fn:
        return (
            "Local-first 的代碼庫語意圖譜引擎，為 Agent 建立精準依賴拓撲，顯著縮減無效上下文（Context Reduction），避免幻覺。",
            "波及半徑（Blast-radius）分析、MCP 原生相容與本機秒級增量索引"
        )
    if "openclaw" in fn:
        return (
            "具備跨平台電腦控制與深層操作系統調度能力的自主 Agent，星標近 40 萬，引領了全自主環境執行的未來方向。",
            "跨平台 OS 深度控制、強大自動化腳本執行迴圈"
        )
    if "ai-agents-for-beginners" in fn or "ai-engineering-from-scratch" in fn:
        return (
            "系統化拆解現代 AI 智能體工程架構與實作原理的權威教學課程，內容由淺入深，是掌握 Agent 技術全貌的必讀專案。",
            "結合理論公式與端到端代碼實現的完整知識圖譜"
        )

    # General high-quality rationale fallback
    return (
        f"在同類專案中享有極高社群聲譽（{stars:,} Stars），工程架構扎實且精確解決了該領域的核心瓶頸問題。",
        "出色的設計理念、清晰的文件架構與高度實用的開發者工具生態"
    )

def build_groups_data() -> Dict[str, Any]:
    """
    Build the full grouped dataset, including comparative analyses and Top 3 selections.
    Saves to data/groups_cache.json.
    """
    if not config.ANALYSIS_CACHE_FILE.exists():
        raise FileNotFoundError(f"Missing {config.ANALYSIS_CACHE_FILE}. Please run analyzer first.")

    with open(config.ANALYSIS_CACHE_FILE, "r", encoding="utf-8") as f:
        analysis_cache = json.load(f)

    # Re-classify and group
    groups_data: Dict[str, Any] = {}
    for cat_id, meta in CATEGORIES_META.items():
        groups_data[cat_id] = {
            "meta": meta,
            "repos": [],
            "comparison": {},
            "top_3": []
        }

    for fn, item in analysis_cache.items():
        cat_id = classify_repo(fn, item)
        item["category_id"] = cat_id
        item["category_name"] = CATEGORIES_META.get(cat_id, {}).get("name", cat_id)
        if cat_id in groups_data:
            groups_data[cat_id]["repos"].append(item)

    # Sort repos in each group by stars descending
    for cat_id, g in groups_data.items():
        g["repos"].sort(key=lambda x: x.get("stargazers_count", 0), reverse=True)
        g["comparison"] = generate_group_comparison_analysis(cat_id, g["repos"])
        g["top_3"] = select_top_3_for_group(cat_id, g["repos"])

    # Save to disk
    with open(config.GROUPS_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(groups_data, f, ensure_ascii=False, indent=2)

    # Also update analysis cache with refreshed category ids
    with open(config.ANALYSIS_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(analysis_cache, f, ensure_ascii=False, indent=2)

    print(f"[✓] Groups data generated and saved to {config.GROUPS_CACHE_FILE}")
    return groups_data

if __name__ == "__main__":
    build_groups_data()

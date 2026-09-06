"""
Categorization, comparative analysis, and Top 5 selection for starred GitHub repositories.
Groups repositories into 20 structured functional domains, evaluates architectural differences,
and selects the Top 5 repositories within each group with pros/cons cross-comparisons
and applicable scenario recommendations.
"""

import json
import math
import re
from typing import Dict, List, Any, Tuple

import config
from src.top5_evaluations import TOP5_CATEGORY_COMPARISONS, TOP5_PROJECT_PROFILES, TARGET_TOP5

CATEGORIES_META = {
    "coding_agents_cli": {
        "id": "coding_agents_cli",
        "name": "AI 終端編程 Agent 與官方 CLI 工具",
        "name_en": "Autonomous Coding Agents & Official CLI",
        "icon": "🤖",
        "badge_color": "#3B82F6",
        "summary": "深度整合本地 Shell、檔案系統與 Git 工作流之自主編程 Agent 與官方 CLI 開發助手。",
        "comparison_aspects": [
            "系統接管層級 (純終端 Shell 交互 vs 跨桌面 GUI 深度調度)",
            "模型適配彈性 (專屬思考模型綁定 vs 開源模型本地私有化相容)",
            "Git 與工程協同 (自動 Worktree 隔離與分支提交 vs 簡單單點覆蓋)"
        ]
    },
    "multi_agent_swarms": {
        "id": "multi_agent_swarms",
        "name": "多 Agent 協同編排、蜂巢架構與自主組織",
        "name_en": "Multi-Agent Swarms & Collaborative Orchestration",
        "icon": "🐝",
        "badge_color": "#8B5CF6",
        "summary": "跨模型多角色分工、去中心化蜂巢通訊、獨立 Worktree 交叉審查與分散式 Agent 協同架構。",
        "comparison_aspects": [
            "協同拓撲 (層級主控分發 vs 匿名盲審投票 vs 去中心化 Pub/Sub 廣播)",
            "狀態收斂機制 (多輪辯論共識 vs 集中式狀態機 vs 獨立任務隊列)",
            "領域特化深度 (通用軟體工程模擬 vs 金融量化風控 vs 科學科研閉環)"
        ]
    },
    "agent_runtimes_sandboxes": {
        "id": "agent_runtimes_sandboxes",
        "name": "Agent 執行環境、沙箱隔離與 Harness 鷹架",
        "name_en": "Agent Runtimes, Execution Sandboxes & Harnesses",
        "icon": "🏗️",
        "badge_color": "#EC4899",
        "summary": "為編程智能體提供安全隔離之沙箱 Runtime、微內核動態插件 Harness、測試期自演化架構與架構方法論。",
        "comparison_aspects": [
            "架構解耦性 (微內核熱插拔插件 vs 內建單體執行沙箱)",
            "安全防護力 (即時環境狀態快照回滾 vs 容器隔離 vs 宿主機信任執行)",
            "應用場景導向 (高併發企業服務 vs 本機腳本執行 vs 網頁無頭瀏覽器沙箱)"
        ]
    },
    "core_agent_skills": {
        "id": "core_agent_skills",
        "name": "Claude Code / Codex 核心技能擴展庫",
        "name_en": "Claude Code & Codex Core Agent Skills",
        "icon": "⚡",
        "badge_color": "#10B981",
        "summary": "專為終端 Agent 打造之工程實踐工作流、代碼審查標準、架構防護與開箱即用之標準化 Skill 擴展庫。",
        "comparison_aspects": [
            "工程規範深度 (Web/TypeScript 最佳實踐 vs 綜合生產力工具集)",
            "擴展封裝方式 (標準 .agents 規範 vs 一鍵 Shell 自動化腳本)",
            "社群覆蓋體系 (官方標準定義 vs 社群百萬級下載驗證生態)"
        ]
    },
    "ui_ux_frontend_skills": {
        "id": "ui_ux_frontend_skills",
        "name": "前端 UI/UX、動效微調與設計系統 Skills",
        "name_en": "UI/UX, Frontend Motion & Design System Skills",
        "icon": "🎨",
        "badge_color": "#F43F5E",
        "summary": "賦予 Agent 現代前端審美直覺、動畫時序微調、設計系統對齊與互動元件生成的專項技能集。",
        "comparison_aspects": [
            "動效物理模型 (Framer Motion 彈簧物理 vs 靜態 CSS 排版規則)",
            "設計約束維度 (間距比例字體美學 vs SaaS 現代儀表板元件庫)",
            "整合與調用 (npx 一鍵直裝技能 vs 終端快捷斜線指令)"
        ]
    },
    "workflow_domain_skills": {
        "id": "workflow_domain_skills",
        "name": "專項工程領域、工作流程與實戰技能",
        "name_en": "Domain-Specific Engineering & Workflow Skills",
        "icon": "🛠️",
        "badge_color": "#06B6D4",
        "summary": "涵蓋金融量化、論文研讀、臨床醫學決策、CI 成本治理與端到端開源 AI 應用範本之特定領域技能。",
        "comparison_aspects": [
            "專業知識門檻 (高價值金融審計 vs 醫學實證檢索 vs 雲端無頭爬蟲)",
            "生成交互模式 (螢幕操作反向自動轉譯 vs 結構化工程外掛)",
            "範本覆蓋度 (單一專業深度 vs 100+ 端到端真實業務開箱即用矩陣)"
        ]
    },
    "mcp_core_servers": {
        "id": "mcp_core_servers",
        "name": "MCP 核心協議、官方伺服器與主機生態",
        "name_en": "Model Context Protocol - Core Servers & Ecosystem",
        "icon": "🔌",
        "badge_color": "#6366F1",
        "summary": "Anthropic MCP 工業標準通訊協定、官方核心伺服器庫、SaaS 整合主機與開發者工具註冊中心。",
        "comparison_aspects": [
            "通訊傳輸架構 (標準 Stdio 本地管道 vs SSE HTTP 分散式中繼)",
            "外部生態覆蓋 (GitHub/Slack/Postgres 官方核心 vs 雲端無伺服器快取)",
            "系統整合深度 (瀏覽器 CDP 遠端透視 vs 資料庫原生唯讀/寫入介面)"
        ]
    },
    "os_automation_desktop_mcp": {
        "id": "os_automation_desktop_mcp",
        "name": "桌面環境接管、系統自動化與 OS MCP",
        "name_en": "OS Automation, Computer Use & Desktop MCP Tools",
        "icon": "🖥️",
        "badge_color": "#14B8A6",
        "summary": "透過 MCP 與 CDP 協議直接操控宿主機終端、瀏覽器、ADB 行動裝置與作業系統之電腦控制工具。",
        "comparison_aspects": [
            "操作系統調度深度 (macOS 原生視窗像素焦點 vs 跨平臺 Unified Diff 代碼熱打補丁)",
            "安全授權機制 (沙箱化讀寫權限控管 vs 宿主機完全管理員授權)",
            "本地檢索整合 (全盤毫秒級增量檔案搜尋 vs 專業垂直本地資料庫)"
        ]
    },
    "system_prompts_engineering": {
        "id": "system_prompts_engineering",
        "name": "提示詞工程、逆向 System Prompts 與對齊規範",
        "name_en": "System Prompts Reverse-Engineering & Prompting",
        "icon": "📜",
        "badge_color": "#D946EF",
        "summary": "商業級 AI 產品系統提示詞逆向剖析、防禦性策略、認知引導架構與自適應調優提示詞工程。",
        "comparison_aspects": [
            "逆向剖析深度 (商業產品完整工具契約還原 vs 前沿閉源模型即時洩漏追蹤)",
            "輸出約束哲學 (結論先行 BLUF 極限排版 vs 完整思維鏈 Chain-of-Thought 引導)",
            "防禦性防護 (提示詞注入越獄攻防 vs 安全邊界與工具白名單隔離)"
        ]
    },
    "agent_specs_rules": {
        "id": "agent_specs_rules",
        "name": "Agent 規範檔案、AGENTS.md 與規格驅動開發",
        "name_en": "Agent Specs, AGENTS.md & Spec-Driven Development",
        "icon": "📋",
        "badge_color": "#F59E0B",
        "summary": "結構化引導 Agent 行為之 AGENTS.md 規範、梯度下降自動演進規則檔與 12-Factor Agent 規格驅動方法論。",
        "comparison_aspects": [
            "規則維護範式 (人工經驗編寫 vs 軌跡誤差反向傳播自適應梯度優化)",
            "規格標準層次 (跨平台統一開放規範 vs 專屬工具終端實戰避坑守則)",
            "敏捷流程閉環 (規格第一 Spec-first 驗證 vs BMAD 敏捷持續交付)"
        ]
    },
    "model_routing_gateways": {
        "id": "model_routing_gateways",
        "name": "模型路由、API 代理網關與多模型轉發",
        "name_en": "Model Routers, API Gateways & Multi-LLM Proxies",
        "icon": "🔀",
        "badge_color": "#EAB308",
        "summary": "統一各大主流與開源模型相容介面、本機 Reverse Proxy、故障容災路由排程與模型協議無縫轉譯。",
        "comparison_aspects": [
            "網關部署型態 (企業級分散式 Proxy vs 本機反向封裝 CLI 為 API)",
            "路由排程策略 (模型能力加權輪轉 vs 故障自動降級 vs 成本最低優先)",
            "底層執行效能 (極致 Rust 微秒級轉發 vs 完備 Python 治理後台)"
        ]
    },
    "token_cost_monitors": {
        "id": "token_cost_monitors",
        "name": "Token 用量統計、費用監控與選單列看板",
        "name_en": "Token Cost Trackers, Quota Monitors & Status Bars",
        "icon": "⏱️",
        "badge_color": "#84CC16",
        "summary": "本地優先之即時 Token 消耗追蹤、macOS 選單列常駐儀表板、多帳戶配額預警與成本支出審計。",
        "comparison_aspects": [
            "展示載體形態 (macOS 原生選單列圖示 vs 本地優先 Web 儀表板 vs 極簡 CLI)",
            "監控粒度層次 (帳戶級重置視窗倒數 vs 代碼行級 Token 燃燒率分析)",
            "數據隱私安全性 (零雲端外洩純本地計算 vs 需上傳審計日誌)"
        ]
    },
    "code_intelligence_ast": {
        "id": "code_intelligence_ast",
        "name": "程式碼語意圖譜、AST 解析與架構審查",
        "name_en": "Code Intelligence, AST Parsing & Knowledge Graphs",
        "icon": "🧠",
        "badge_color": "#6366F1",
        "summary": "基於 Tree-sitter 的語法樹結構搜尋重構、本地優先代碼庫依賴圖譜與 Context 精準壓縮防幻覺架構。",
        "comparison_aspects": [
            "代碼分析深度 (AST 語法樹節點結構比對 vs 全庫依賴與呼叫鏈拓撲圖譜)",
            "上下文優化目標 (精確波及半徑計算節省 70%+ 上下文 vs 自然語言架構導航)",
            "執行與編程語言 (Rust 高效能本機二進位 vs 記憶體常駐關係圖論資料庫)"
        ]
    },
    "web_doc_parsing_ocr": {
        "id": "web_doc_parsing_ocr",
        "name": "智慧網頁採集、文件格式解析與 OCR 轉換",
        "name_en": "Web Crawling, Document Extraction & OCR Parsing",
        "icon": "🌐",
        "badge_color": "#0EA5E9",
        "summary": "端到端動態網頁渲染反爬爬取、Office/PDF 多格式極速轉換、OCR 字符辨識與純淨 Markdown 輸出。",
        "comparison_aspects": [
            "數據來源管道 (動態 SPA 瀏覽器渲染反爬 vs 辦公室二進位文檔解析)",
            "排版還原精度 (雙欄論文公式 LaTeX 高保真解析 vs 純淨簡約 Markdown 扁平化)",
            "架構依賴規模 (零外部伺服器 Python 標準庫 vs 無頭瀏覽器分散式集群)"
        ]
    },
    "speech_multimodal_audio": {
        "id": "speech_multimodal_audio",
        "name": "語音辨識、多模態音訊與影音處理",
        "name_en": "Speech Recognition & Multimodal Audio/Video Pipelines",
        "icon": "🎙️",
        "badge_color": "#A855F7",
        "summary": "本地語音轉文字、語音合成 TTS、音訊時序對齊、影音字幕提取與多模態音訊生成處理管線。",
        "comparison_aspects": [
            "任務維度 (高精度語音轉錄 ASR vs 擬真情感語音合成 TTS vs 串流多媒體下載)",
            "推論執行環境 (純 C/C++ 零依賴 Apple Silicon 加速 vs 雲端大型多模態模型)",
            "資料處理流水線 (端到端影音抓取字幕分離 vs 長音訊多講者聲學對齊)"
        ]
    },
    "long_term_memory": {
        "id": "long_term_memory",
        "name": "長期記憶層、跨會話持久化與個性化 Memory",
        "name_en": "Long-Term Memory, Stateful Context & Personal Memory",
        "icon": "💾",
        "badge_color": "#059669",
        "summary": "智能體跨會話持久記憶、本地隱私 Markdown/SQLite 儲存層、終身學習檔案與個人工作習慣沉澱。",
        "comparison_aspects": [
            "儲存與所有權 (Local-first 純 Markdown 檔案 vs 高維度向量資料庫儲存)",
            "演化與遺忘機制 (多輪對話動態自適應更新 vs 記憶宮殿層次化拓撲檢索)",
            "生態整合範圍 (Claude Code 專屬會話無縫掛載 vs 跨應用全域數位第二大腦)"
        ]
    },
    "context_engineering_rag": {
        "id": "context_engineering_rag",
        "name": "上下文工程、動態壓縮與知識圖譜 RAG",
        "name_en": "Context Engineering, Dynamic Compression & GraphRAG",
        "icon": "🔍",
        "badge_color": "#2563EB",
        "summary": "工具輸出動態修剪、GraphRAG 全局社群摘要、本地知識圖譜檢索與極致 Context 視窗最佳化。",
        "comparison_aspects": [
            "檢索演算法核心 (知識圖譜社群偵測 Leiden vs 無向量樹狀目錄索引 vs 傳統向量 RAG)",
            "工程處理層級 (執行期工具日誌動態語意剪枝 vs 離線預建索引與層次化摘要)",
            "問題解答維度 (巨集宏觀全局洞察 vs 精確頁碼細節來源對齊)"
        ]
    },
    "diagrams_presentations": {
        "id": "diagrams_presentations",
        "name": "架構圖表可視化、設計系統與 Markdown 簡報",
        "name_en": "Architecture Diagrams, Design Systems & Presentations",
        "icon": "📊",
        "badge_color": "#F97316",
        "summary": "出版級免外部渲染圖表樣式、推理思考圖論可視化、Markdown 編譯投影片與視覺協同工具。",
        "comparison_aspects": [
            "產出交付形式 (純 HTML+SVG 零外掛直出 vs Draw.io 自由畫布 vs Markdown 編譯投影片)",
            "AI 協同美學風格 (出版級極簡排版 vs 標準技術架構圖風格 vs 商業路演投影片)",
            "二次編輯彈性 (純文字代碼直接修改 vs 瀏覽器可視化拖曳微調)"
        ]
    },
    "cs_curricula_learning": {
        "id": "cs_curricula_learning",
        "name": "頂級電腦科學課程、AI 工程實戰與面試指南",
        "name_en": "CS Curricula, AI Engineering Mastery & Interview Kits",
        "icon": "🎓",
        "badge_color": "#4F46E5",
        "summary": "從零構建 Transformer/Agent 權威教材、知名大學 CS 課程索引、架構設計模式與頂級大廠面試題庫。",
        "comparison_aspects": [
            "知識傳授層次 (純 Python 零黑盒手寫底層 Transformer vs 頂級名校 CS 硬核課程)",
            "實踐導向維度 (全生命週期大模型訓練微調部署 vs 系統設計面試真題解析)",
            "內容呈現形態 (手把手 Colab Notebook 實戰 vs 結構化學習路線圖指引)"
        ]
    },
    "terminal_system_productivity": {
        "id": "terminal_system_productivity",
        "name": "macOS 系統擴展、終端生產力與日常效率工具",
        "name_en": "macOS System Tools, Terminal Shell & Productivity Kits",
        "icon": "🚀",
        "badge_color": "#64748B",
        "summary": "終端 Zsh 配置、macOS 選單列管理、視窗螢幕控制、自動化替換與極客必備日常高效工具。",
        "comparison_aspects": [
            "應用層級領域 (命令列 Shell 終端增強 vs 本地 WebUI 大模型對話介面 vs macOS 系統選單列)",
            "生態沉澱規模 (百萬級開源插件與主題總匯 vs 原創專題極致精緻應用)",
            "生產力提升維度 (日常命令列敲擊補全加速 vs 桌面視覺干擾清除與多屏監控)"
        ]
    }
}

PRIORITY_FOUNDATIONS = {
    "anthropics/claude-code", "anomalyco/opencode", "openclaw/openclaw", "deepseek-ai/deepseek-harness",
    "mattpocock/skills", "obra/superpowers", "anthropics/skills", "modelcontextprotocol/servers",
    "affaan-m/ECC", "wonderwhy-er/DesktopCommanderMCP", "github/github-mcp-server",
    "x1xhlol/system-prompts-and-models-of-ai-tools", "github/spec-kit", "shareAI-lab/learn-claude-code",
    "kunchenguid/backpass", "router-for-me/CLIProxyAPI", "musistudio/claude-code-router",
    "steipete/CodexBar", "robinebers/openusage", "ast-grep/ast-grep", "tirth8205/code-review-graph",
    "jianshuo/ccglass", "firecrawl/firecrawl", "microsoft/markitdown", "openai/whisper",
    "headroomlabs-ai/headroom", "mem0ai/mem0", "MemPalace/mempalace", "EverMind-AI/EverOS",
    "cathrynlavery/diagram-design", "DayuanJiang/next-ai-draw-io", "marp-team/marp",
    "microsoft/ai-agents-for-beginners", "rohitg00/ai-engineering-from-scratch", "ohmyzsh/ohmyzsh",
    "yt-dlp/yt-dlp", "thaw-app/Thaw", "emilkowalski/skills", "openinterpreter/openinterpreter",
    "microsoft/graphrag", "BerriAI/litellm", "open-webui/open-webui", "infiniflow/ragflow",
    "supermemoryai/supermemory", "EveryInc/compound-engineering-plugin", "anthropics/financial-services",
    "Shubhamsaboo/awesome-llm-apps", "ChromeDevTools/chrome-devtools-mcp", "mlabonne/llm-course",
    "prakhar1989/awesome-courses", "DopplerHQ/awesome-interview-questions", "herdrdev/herdr"
}

# Explicit mapping dictionary combining target Top 5 and curated boundary overrides
EXPLICIT_MAP: Dict[str, str] = {r.lower(): cat for cat, repos in TARGET_TOP5.items() for r in repos}

ADDITIONAL_MAP = {
    'microsoft/autogen': 'multi_agent_swarms',
    'sakanaai/ai-scientist': 'multi_agent_swarms',
    'shepalderson/copilot-orchestra': 'multi_agent_swarms',
    'marian2js/opengoat': 'multi_agent_swarms',
    'contains-studio/agents': 'multi_agent_swarms',
    'yeachan-heo/oh-my-claudecode': 'multi_agent_swarms',

    'stablyai/orca': 'agent_runtimes_sandboxes',
    'hkuds/openharness': 'agent_runtimes_sandboxes',
    'openabdev/openab': 'agent_runtimes_sandboxes',
    'paperclipai/paperclip': 'agent_runtimes_sandboxes',
    'ml-explore/mlx': 'agent_runtimes_sandboxes',
    'browsh-org/browsh': 'agent_runtimes_sandboxes',

    'rohitg00/agentmemory': 'long_term_memory',
    'memodb-io/acontext': 'long_term_memory',

    'llmware-ai/llmware': 'context_engineering_rag',
    'lfnovo/open-notebook': 'context_engineering_rag',

    'trycua/cua': 'os_automation_desktop_mcp',
    'fathah/hermes-desktop': 'os_automation_desktop_mcp',
    'tinyhumansai/openhuman': 'os_automation_desktop_mcp',

    'kenn-io/agentsview': 'token_cost_monitors',

    'mnfst/manifest': 'model_routing_gateways',
    'qoojoyyoung/mini-llm-arena': 'model_routing_gateways',

    'bloopai/vibe-kanban': 'agent_specs_rules',
    'microsoft/agentrc': 'agent_specs_rules',
    'doggy8088/github-copilot-configs': 'agent_specs_rules',

    'patchy631/ai-engineering-hub': 'cs_curricula_learning',
    'doggy8088/agentic-design-patterns': 'cs_curricula_learning',
    'google-ai-edge/gallery': 'cs_curricula_learning',
    'xai-org/x-algorithm': 'cs_curricula_learning',

    'fincept-corporation/finceptterminal': 'workflow_domain_skills',
    'open-dev-society/openstock': 'workflow_domain_skills',
    'traderalice/openalice': 'workflow_domain_skills',
    'interviewstreet/hiring-agent': 'workflow_domain_skills',
    'huggingface/ml-intern': 'workflow_domain_skills',
    'pleaseprompto/notebooklm-skill': 'workflow_domain_skills',
    'lingbol088-spec/reverse-flow-skill': 'workflow_domain_skills',
    'mvanhorn/cli-printing-press': 'workflow_domain_skills',

    'openai/skills': 'core_agent_skills',
    'huggingface/skills': 'core_agent_skills',
    'android/skills': 'core_agent_skills',
    'simonw/claude-skills': 'core_agent_skills',
    'kulaxyz/self-learning-skills': 'core_agent_skills',
    'alchaincyf/nuwa-skill': 'core_agent_skills',
    'steipete/agent-scripts': 'core_agent_skills',
    'vercel-labs/skills': 'core_agent_skills',

    'siteboon/claudecodeui': 'coding_agents_cli',
    'nesquena/hermes-webui': 'coding_agents_cli',
    'ekkolearnai/hermes-studio': 'coding_agents_cli',
    'andymik90/aperant': 'coding_agents_cli',
    'github/copilot-sdk': 'coding_agents_cli',
    'sigoden/aichat': 'coding_agents_cli',
    'slopus/happy': 'coding_agents_cli',
    'doggy8088/copilot-cli': 'coding_agents_cli',
    'craig7351/bookshell': 'coding_agents_cli',
    'galdawave/pickle-rick-extension': 'coding_agents_cli',
    'microsoft/intelligent-terminal': 'coding_agents_cli',
    'manaflow-ai/cmux': 'coding_agents_cli',
    'shawnpana/smux': 'coding_agents_cli',
    'lencx/noi': 'coding_agents_cli',

    'muset-ai/awesome-nano-banana-pro': 'system_prompts_engineering',
    'badlogic/cchistory': 'system_prompts_engineering',

    'openai/plugins': 'mcp_core_servers',

    'ryanhuge/typegood': 'speech_multimodal_audio',
    'chenlu-hung/vibetyping': 'speech_multimodal_audio',
    'google-research/timesfm': 'speech_multimodal_audio',

    'searxng/searxng': 'web_doc_parsing_ocr',
    'bugzmanov/bookokrat': 'web_doc_parsing_ocr',
}

EXPLICIT_MAP.update({k.lower(): v for k, v in ADDITIONAL_MAP.items()})

def clean_text(text: str) -> str:
    text = re.sub(r'https?://\S+', '', (text or ''))
    text = re.sub(r'\[!\[.*?\]\(.*?\)\]\(.*?\)', '', text)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    return text.lower()

def classify_repo(full_name: str, repo_info: Dict[str, Any]) -> str:
    """Classify repository into one of the 20 core categories with priority filtering."""
    name = full_name.lower()
    if name in EXPLICIT_MAP:
        return EXPLICIT_MAP[name]

    desc = clean_text(repo_info.get("description") or "")
    topics = [t.lower() for t in repo_info.get("topics", [])]
    repo_short = name.split('/')[-1]

    # 1. System Prompts & Prompt Engineering
    if any(k in name for k in ['system-prompt', 'system_prompts', 'cl4r1t4s', 'andrej-karpathy-skills', 'promptfill', 'i-have-adhd', 'markdown_plus', 'knowie']) or \
       any(k in desc for k in ['system prompt', 'leaked prompt', 'jailbreak', 'prompt engineering', 'reverse engineered prompt']):
        return 'system_prompts_engineering'

    # 2. Agent Specs & Rules (AGENTS.md, spec-kit)
    if 'spec-kit' in name or 'openspec' in name or 'bmad-method' in name or 'backpass' in name or '12-factor-agents' in name or 'tempdd' in name or 'claude-code-best-practice' in name or 'context-engineering-intro-zh' in name or 'open-vibe-developers' in name:
        return 'agent_specs_rules'

    # 3. Code Intelligence & AST
    if any(k in name for k in ['ast-grep', 'code-review-graph', 'codegraph', 'leak-hunter', 'bug-hunter', 'graphify', 'understand-anything', 'codebase-memory-mcp', 'contextplus']):
        return 'code_intelligence_ast'

    # 4. Diagrams & Presentations
    if any(k in name for k in ['diagram-design', 'arcgram', 'marp', 'draw-io', 'open-design', 'ppt-master', 'banana-slides', 'open-slide', 'illustrations', 'openclaw-office']) or \
       any(k in desc for k in ['editorial diagram', 'diagram engine', 'markdown presentation', 'node-and-edge flow', 'presentation ecosystem']):
        return 'diagrams_presentations'

    # 5. Speech, Audio & Multimodal Media
    if any(k in name for k in ['whisper', 'vibevoice', 'voxcpm', 'yt-dlp', 'lecture-to-notes', 'caption-convert', 'voicetype', 'subdown']) or \
       any(k in desc for k in ['speech recognition', 'text-to-speech', 'tts', 'audio model', 'voice model', 'youtube-dl', 'subtitles']):
        return 'speech_multimodal_audio'

    # 6. Long Term Memory
    if any(k in name for k in ['mempalace', 'everos', 'mem0', 'claude-mem', 'supermemory', 'gbrain', 'personal-ai-memory', 'emulo', 'honcho', 'agentmemory', 'acontext']):
        return 'long_term_memory'

    # 7. Context Engineering & RAG
    if any(k in name for k in ['headroom', 'graphrag', 'ragflow', 'pageindex', 'cognee', 'qmd', 'openwiki', 'pyrag', 'llm-knowledge-base', 'llm_wiki', 'knowledge-catalog', 'wrenai', 'context-hub', 'turbovec', 'mnemosyne', 'llmware', 'open-notebook']) or \
       any(k in desc for k in ['compress tool output', 'context reduction', 'graphrag', 'knowledge graph', 'retrieval-augmented']):
        return 'context_engineering_rag'

    # 8. Token Cost & Quota Monitoring
    if any(k in name for k in ['codexbar', 'openusage', 'llm-usage-tracker', 'codeburn', 'tokenusageinsights', 'cc-statusline', 'ccglass', 'agentsview']) or \
       ('usage' in repo_short and any(k in name for k in ['aqua5230', 'yanowo', 'tracker'])) or \
       any(k in desc for k in ['token cost', 'usage stats', 'usage monitor', 'rate limit monitor', 'quota tracker', 'tracking token']):
        return 'token_cost_monitors'

    # 9. Model Routing, Gateways & Proxies
    if any(k in name for k in ['litellm', 'cliproxyapi', 'cc-switch', 'claude-code-router', 'opencodex', 'codex-router', 'rtk', 'aisuite', 'ccr-next', 'fox-ai-roundtable', 'rapid-mlx', 'manifest']) or \
       any(k in desc for k in ['model router', 'api gateway', 'ai gateway', 'reverse proxy', 'multi-model routing', 'ask once, get three answers']):
        return 'model_routing_gateways'

    # 10. Document Parsing & OCR
    if any(k in name for k in ['langextract', 'markitdown', 'mineru', 'docling', 'anydoc', 'unlimited-ocr', 'pdf-inspector', 'doc-cleaner', 'imagepdf2txt', 'doxx', 'turndown', 'coursenote', 'textbook-to-note', 'breast-cancer-uptodate', 'firecrawl', 'scrapling', 'open-scouts', 'paste-to-markdown']) or \
       any(k in desc for k in ['convert word', 'clean markdown', 'pdf extract', 'ocr', 'document conversion', 'document parser', 'web scraper', 'crawling api', 'anti-bot', 'bypass cloudflare', 'structured information extraction']):
        return 'web_doc_parsing_ocr'

    # 11. UI/UX & Frontend Design Skills
    if any(k in name for k in ['emilkowalski/skills', 'ui-ux-pro-max-skill', 'taste-skill', 'skilless.ai', 'huashu-design', 'design-md-chrome']) or \
       any(k in desc for k in ['html-native design', 'design skill', 'taste-skill', 'extract styles from any website']):
        return 'ui_ux_frontend_skills'

    # 12. Domain & Workflow Skills
    if any(k in name for k in ['compound-engineering-plugin', 'financial-services', 'paper-review', 'openevidence-skill', 'smart_resume', 'finding-unknowns-skills', 'ai-cost-cutter-skills', 'litellm-skills', 'grok-build-connector', 'skill-recorder', 'awesome-llm-apps', 'browserbase/skills', 'reverse-flow-skill', 'notebooklm-skill']) or \
       any(k in desc for k in ['domain-specific skill', 'cost cutter', 'workflow skill', '100+ open-source ai applications']):
        return 'workflow_domain_skills'

    # 13. Core Agent Skills
    if any(k in name for k in ['mattpocock/skills', 'superpowers', 'anthropics/skills', 'gstack', 'ponytail', 'caveman', 'agent-skills', 'claude-code-workspace', 'ecc', 'nuwa-skill', 'self-learning-skills', 'agent-scripts']) or \
       any(k in desc for k in ['skills for claude', 'claude code skill', 'agent skills', 'agent skill', 'skills catalog']) or \
       any(k in topics for k in ['agent-skills', 'claude-skills']):
        return 'core_agent_skills'

    # 14. Coding Agents & Official CLI
    if any(k in name for k in ['claude-code', 'opencode', 'codex', 'gemini-cli', 'openclaw', 'hermes-agent', 'claw-code', 'learn-claude-code', 'claude-better', 'claude-codex-bridge', 'mini-claw', 'copilot-sdk-demo', 'claudecodeui', 'hermes-webui', 'hermes-studio', 'aperant', 'copilot-sdk', 'aichat', 'happy', 'cmux', 'smux', 'noi']) or \
       any(k in desc for k in ['autonomous coding agent', 'terminal agent', 'coding assistant', 'cli for ai']):
        return 'coding_agents_cli'

    # 15. Agent Runtimes & Sandboxes
    if any(k in name for k in ['deepseek-harness', 'bingreeky/jit', 'herdr', 'awesome-agent-architecture', 'harness-engineering', 'omnigent', 'claudexor', 'baton', 'subtask', 'openinterpreter', 'autoresearch', 'autoreason', 'agent-browser', 'openab', 'orca', 'paperclip']) or \
       any(k in desc for k in ['agent harness', 'runtime for ai agents', 'harness engineering', 'agent sandbox', 'meta-harness', 'research harness']):
        return 'agent_runtimes_sandboxes'

    # 16. Multi-Agent Swarms
    if any(k in name for k in ['swarm-forge', 'claude-vibe-squad', 'deepagents', 'buzz', 'hermes-agency-orchestrator', 'copilot-ralph', 'claw-info', 'hermes-discord-status-line', 'llm-council', 'ai-hedge-fund', 'agency-agents', 'autogen', 'ai-scientist', 'copilot-orchestra', 'opengoat']) or \
       any(k in desc for k in ['multi-agent', 'swarm', 'coordinating several ai agents', 'multiple agents', 'orchestrat']):
        return 'multi_agent_swarms'

    # 17. OS Automation & Desktop MCP
    if any(k in name for k in ['desktopcommandermcp', 'peekaboo', 'ask-bridge', 'agent-adb-control', 'agent-windows-control', 'birdclaw', 'mcp-taiwan-legal-db', 'openevidence-mcp', 'glean', 'cua', 'hermes-desktop', 'openhuman']) or \
       any(k in desc for k in ['control your computer', 'desktop command', 'chrome devtools protocol', 'adb control', 'windows control', 'automate desktop', 'computer-use']):
        return 'os_automation_desktop_mcp'

    # 18. MCP Core Servers & Hosts
    if any(k in topics for k in ['mcp', 'model-context-protocol', 'mcp-server']) or \
       any(k in name for k in ['modelcontextprotocol', 'context7', 'github-mcp-server', 'chrome-devtools-mcp', 'notion-mcp-server', 'mcp-cli', 'toolanything', 'ai-twinkle/hub', 'zhtw-mcp', 'devdocs', 'open-science', 'ruflo']) or \
       any(k in desc for k in ['mcp server', 'model context protocol', 'mcp tools', 'mcp client']):
        return 'mcp_core_servers'

    # 19. CS Curricula & AI Learning
    if any(k in name for k in ['ai-engineering-from-scratch', 'ai-agents-for-beginners', 'llm-course', 'awesome-courses', 'awesome-interview-questions', 'awesome-design-patterns', 'learn-git', 'ai-crash-course', 'ai-agent-deep-dive', 'ai-engineering-hub', 'learning-beyond-gradients', 'ai-system-design-guide', 'awesome-software-design', 'awesome-opensource-ai', 'career-ops', 'deeptutor', 'openstock', 'dictionary-of-ai-coding']) or \
       any(k in desc for k in ['course', 'curriculum', 'learn', 'interview', 'tutorial', 'guide', 'roadmap', 'study']):
        return 'cs_curricula_learning'

    # 20. Terminal & System Productivity (Default fallback)
    return 'terminal_system_productivity'

def select_top_5_for_group(group_id: str, group_repos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Select Top 5 repositories within a group based on multi-dimensional evaluation:
    Stars, foundational importance, documentation depth, and architectural completeness.
    Prioritizes curated target Top 5 list when available.
    Enriches each repository with LLM-evaluated pros, cons, and applicable scenarios.
    """
    if not group_repos:
        return []

    target_list = TARGET_TOP5.get(group_id, [])
    target_rank_map = {fn.lower(): idx for idx, fn in enumerate(target_list)}

    def score_repo(r: Dict[str, Any]) -> float:
        fn = r.get("full_name", "")
        fn_lower = fn.lower()
        if fn_lower in target_rank_map:
            # Deterministic priority score for curated Top 5: 1000 - rank * 10
            return 1000.0 - target_rank_map[fn_lower] * 10.0
        stars = int(r.get("stargazers_count") or 0)
        has_readme = 1.0 if r.get("readme_has_content") else 0.2
        has_desc = 1.0 if len(r.get("description") or "") > 20 else 0.5
        foundation_bonus = 25.0 if fn in PRIORITY_FOUNDATIONS else 0.0
        star_score = math.log10(max(stars, 1)) * 12
        return star_score + (has_readme * 10) + (has_desc * 5) + foundation_bonus

    sorted_repos = sorted(group_repos, key=score_repo, reverse=True)
    top_5_candidates = sorted_repos[:5]

    ranks = [
        "🥇 冠軍首選 (Top 1)",
        "🥈 亞軍精選 (Top 2)",
        "🥉 季軍推薦 (Top 3)",
        "🏅 殿軍新星 (Top 4)",
        "🎖️ 潛力先鋒 (Top 5)"
    ]
    badges = ["Gold", "Silver", "Bronze", "Merit", "Frontier"]
    colors = ["#F59E0B", "#94A3B8", "#B45309", "#3B82F6", "#8B5CF6"]

    top_5_results = []
    for rank_idx, repo in enumerate(top_5_candidates):
        fn = repo.get("full_name", "")
        stars = int(repo.get("stargazers_count") or 0)
        desc = repo.get("description", "")

        # Look up profile with case-insensitive fallback
        profile = TOP5_PROJECT_PROFILES.get(fn)
        if not profile:
            for pk, pv in TOP5_PROJECT_PROFILES.items():
                if pk.lower() == fn.lower():
                    profile = pv
                    break
        if not profile:
            profile = {}

        pros = profile.get("pros")
        if not pros or not isinstance(pros, list):
            pros = [
                f"在開源社群享有極高知名度與採用量（{stars:,} Stars）",
                "代碼架構規範且能精準解決該領域核心瓶頸",
                "具備良好的開源社群維護活力與文件指引"
            ]

        cons = profile.get("cons")
        if not cons or not isinstance(cons, list):
            cons = [
                "需結合特定場景與技術棧進行最佳化配置",
                "進階定制功能需閱讀源碼與深度理解架構設計"
            ]

        scenarios = profile.get("scenarios") or "適用於該技術領域中追求高穩定性與工程可維護性的軟體開發專案"
        highlight = profile.get("highlight") or "出色的架構設計理念與卓越的實戰生產力工具生態"
        rationale = profile.get("rationale") or f"依據星標體量（{stars:,} Stars）、工程成熟度與架構影響力評選為該領域代表性專案。"

        top_5_results.append({
            "rank": rank_idx + 1,
            "rank_title": ranks[rank_idx],
            "badge_type": badges[rank_idx],
            "badge_color": colors[rank_idx],
            "full_name": fn,
            "name": repo.get("name", fn.split("/")[-1] if "/" in fn else fn),
            "stargazers_count": stars,
            "url": repo.get("url", f"https://github.com/{fn}"),
            "description": desc,
            "primary_language": repo.get("primary_language", "Other"),
            "rationale": rationale,
            "highlight": highlight,
            "pros": pros,
            "cons": cons,
            "scenarios": scenarios
        })

    return top_5_results

def generate_group_comparison_analysis(group_id: str, group_repos: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate detailed comparative analysis text and matrices for the group."""
    meta = CATEGORIES_META.get(group_id, {})
    total = len(group_repos)
    eval_data = TOP5_CATEGORY_COMPARISONS.get(group_id, {})

    cross_comp = eval_data.get("cross_comparison", meta.get("summary", "各專案在技術選型、執行粒度與適用環境上展現出多樣化定位。"))
    scenario_rec = eval_data.get("scenario_recommendations", "根據專案具體架構約束與生產力目標選擇合適方案。")

    return {
        "summary": meta.get("summary", ""),
        "repo_count": total,
        "aspects": meta.get("comparison_aspects", []),
        "cross_comparison": cross_comp,
        "scenario_recommendations": scenario_rec
    }

def build_groups_data() -> Dict[str, Any]:
    """
    Build the full grouped dataset with 20 categories, including Top 5 selections,
    comparative analyses, pros/cons, and applicable scenarios.
    Saves to data/groups_cache.json.
    """
    if not config.ANALYSIS_CACHE_FILE.exists():
        if config.REPOS_CACHE_FILE.exists():
            print("[*] Analysis cache not found, automatically triggering analysis pipeline...")
            from src.analyzer import run_analysis_pipeline
            run_analysis_pipeline()
        else:
            raise FileNotFoundError(f"Missing {config.ANALYSIS_CACHE_FILE} and {config.REPOS_CACHE_FILE}. Please run fetcher first.")

    analysis_cache = config.safe_load_json(config.ANALYSIS_CACHE_FILE, default={})
    if not analysis_cache:
        if config.REPOS_CACHE_FILE.exists():
            print("[*] Analysis cache empty or corrupted, re-running analysis...")
            from src.analyzer import run_analysis_pipeline
            analysis_cache = run_analysis_pipeline()
        else:
            raise ValueError("No analysis data available to build groups.")

    # Initialize 20 groups
    groups_data: Dict[str, Any] = {}
    for cat_id, meta in CATEGORIES_META.items():
        groups_data[cat_id] = {
            "meta": meta,
            "repos": [],
            "comparison": {},
            "top_5": []
        }

    repos_cache = config.safe_load_json(config.REPOS_CACHE_FILE, default={})
    # Enrich analysis_cache items with metadata from repos_cache if missing
    for fn, item in analysis_cache.items():
        if fn in repos_cache:
            r = repos_cache[fn]
            if not item.get("description"):
                item["description"] = r.get("description", "")
            if not item.get("topics"):
                item["topics"] = r.get("topics", [])
            if not item.get("stargazers_count"):
                item["stargazers_count"] = r.get("stargazers_count", 0)
            if not item.get("primary_language") or item.get("primary_language") == "Other":
                item["primary_language"] = r.get("primary_language", "Other")

    # Classify all repositories
    for fn, item in analysis_cache.items():
        cat_id = classify_repo(fn, item)
        item["category_id"] = cat_id
        item["category_name"] = CATEGORIES_META.get(cat_id, {}).get("name", cat_id)
        if cat_id in groups_data:
            groups_data[cat_id]["repos"].append(item)
        else:
            groups_data["terminal_system_productivity"]["repos"].append(item)

    # Sort repos in each group by stars descending and generate Top 5
    for cat_id, g in groups_data.items():
        g["repos"].sort(key=lambda x: int(x.get("stargazers_count") or 0), reverse=True)
        g["comparison"] = generate_group_comparison_analysis(cat_id, g["repos"])
        g["top_5"] = select_top_5_for_group(cat_id, g["repos"])

    # Save to disk atomically
    config.atomic_save_json(config.GROUPS_CACHE_FILE, groups_data)

    # Also update analysis cache with refreshed category ids atomically
    config.atomic_save_json(config.ANALYSIS_CACHE_FILE, analysis_cache)

    print(f"[✓] Groups data (20 categories, Top 5 each) generated and saved to {config.GROUPS_CACHE_FILE}")
    return groups_data

if __name__ == "__main__":
    build_groups_data()

"""
LLM-Driven Top 5 Expert Evaluations, Pros/Cons Cross-Comparisons,
and Recommended Applicable Scenarios for 20 Technical Domains.
"""

from typing import Dict, Any, List

TOP5_CATEGORY_COMPARISONS: Dict[str, Dict[str, Any]] = {
    "coding_agents_cli": {
        "cross_comparison": (
            "本領域彙集當前開源與商業陣營最強悍的自主終端編程 Agent。"
            "在【架構哲學】上，形成了三種截然不同的流派：\n"
            "1. 深度系統接管派（OpenClaw）：賦予 Agent 跨桌面與系統底層之全方位控制權，功能極度強大但對主機具潛在侵入風險；\n"
            "2. 官方原生與 Git 協同派（Claude Code、OpenCode）：專注於代碼庫語意理解、Sub-agent 分層規劃與標準 Git Worktree 隔離，編程邏輯最為嚴謹；\n"
            "3. 開源白盒與教育復刻派（Hermes Agent、Learn Claude Code）：將 Agent 執行迴圈解構為極簡腳本或開源模型對齊規範，便於開發者深度定製與學習。\n"
            "在【效能與成本】維度，Claude Code 依賴頂級 Claude 3.7 模型，代碼質量最高但成本昂貴；OpenCode 與 Hermes Agent 則支援本地與低成本模型，性價比更勝一籌。"
        ),
        "scenario_recommendations": (
            "• 企業級或重度代碼重構：首選【Claude Code】或【OpenCode】，具備頂級代碼一致性與原生 Git 提交管理；\n"
            "• 跨軟體自動化與系統級任務：推薦【OpenClaw】，能無縫調用終端、桌面 UI 與自動化腳本；\n"
            "• 開源模型愛好者與隱私自託管：推薦【NousResearch/hermes-agent】，完全相容私有開源模型；\n"
            "• 學習 Agent 底層架構：首選【shareAI-lab/learn-claude-code】，以最短程式碼看懂 Tool Use 與 Loop 循環。"
        )
    },
    "multi_agent_swarms": {
        "cross_comparison": (
            "多 Agent 協同的核心在於『通信拓撲、角色分工與決策收斂』。\n"
            "Agency-Agents 採用經典角色分工架構，模擬真實軟體開發團隊（架構師、前端、後端、QA）；\n"
            "AI-Hedge-Fund 則將多 Agent 應用於金融投研，各角色負責宏觀、基本面與技術指標分析並交叉辯論；\n"
            "Buzz 採用去中心化 Pub/Sub 蜂巢協議，適合高併發事件廣播；\n"
            "DeepAgents 則由 LangChain 團隊打造，著重於開箱即用的模組化與狀態機編排；\n"
            "LLM Council 由 Karpathy 構想，強調多模型投票與交叉審計，有效消除單一模型的盲區幻覺。"
        ),
        "scenario_recommendations": (
            "• 模擬真實軟體工程團隊運作：推薦【Agency-Agents】，開箱即用的角色職責劃分最為完備；\n"
            "• 多視角辯論與防幻覺決策：首選【LLM Council】，透過多模型匿名評審獲得客觀共識；\n"
            "• 金融量化與多因子分析：首選【AI-Hedge-Fund】，現成且成熟的交易決策工作流；\n"
            "• 企業自研複雜工作流：推薦【DeepAgents】，模組化接口最為標準且易於維護。"
        )
    },
    "agent_runtimes_sandboxes": {
        "cross_comparison": (
            "本組專注於智能體的外部執行支架（Harness）、沙箱隔離與科研自動化。\n"
            "DeepSeek-Harness 貫徹『萬物皆插件』思想，以極致解耦的微內核架構支援百萬級高併發吞吐；\n"
            "Open Interpreter 聚焦於本機代碼安全執行，支援雙向自然語言與 Shell 互動；\n"
            "Herdr 則提供專門的輕量隔離容器，提供即時環境快照與秒級還原；\n"
            "AutoResearch 是 Karpathy 打造的端到端機器學習自主研究迴圈；\n"
            "Agent-Browser 則專注於現代 Web 環境的無頭瀏覽器控制沙箱。"
        ),
        "scenario_recommendations": (
            "• 建構企業級高併發 Agent 基礎設施：首選【DeepSeek-Harness】，插件化與效能表現最佳；\n"
            "• 日常代碼執行與本機 Python 自動化：推薦【Open Interpreter】，終端交互最為親民；\n"
            "• 防範未知代碼污染本機開發環境：強烈建議搭配【Herdr】安全沙箱；\n"
            "• Web 端端到端測試與瀏覽器 Agent：首選【vercel-labs/agent-browser】。"
        )
    },
    "core_agent_skills": {
        "cross_comparison": (
            "核心技能庫決定了 Coding Agent 在終端機中的實戰工程素養。\n"
            "Superpowers 提供了全方位的日常生產力超能力技能包，覆蓋範圍最全面；\n"
            "Matt Pocock 的 Skills 庫則深植於現代 Web 與 TypeScript 最佳實踐，代碼審查標準極高；\n"
            "ECC (Everything Claude Code) 彙集社群最完整之 Hook、Skill 與配置資源；\n"
            "Anthropic 官方 Skills 定義了底層標準與安全邊界；\n"
            "GStack 則專注於全端現代化開發者堆疊的一鍵配置與代碼生成。"
        ),
        "scenario_recommendations": (
            "• TypeScript / Web 全端日常開發：首選【mattpocock/skills】，工程規範最嚴密；\n"
            "• 尋求最全面豐富的 Claude Code 擴展：首選【obra/superpowers】與【affaan-m/ECC】；\n"
            "• 追求官方標準與極致穩定性：推薦【anthropics/skills】；\n"
            "• 現代化全端專案快速啟動：推薦【garrytan/gstack】。"
        )
    },
    "ui_ux_frontend_skills": {
        "cross_comparison": (
            "前端與 UI/UX 技能彌補了通用 LLM 缺乏審美直覺、動畫微調與現代設計系統規範的硬傷。\n"
            "Emil Kowalski 的 Skills 由前 Vercel/Linear 頂級動態設計師操刀，專精於 Framer Motion 彈簧物理與微互動時序；\n"
            "UI/UX Pro Max Skill 專注於現代 SaaS 儀表板與 Tailwind/React 生產級響應式排版；\n"
            "Taste-Skill 為 Agent 注入現代極簡美學，嚴格約束排版比例、間距與留白，根除 AI 廉價同質化；\n"
            "Huashu Design 是專為 Claude Code 打造之 HTML 原生設計引擎，內建 20 套頂級設計哲學與 5 維度客觀評審，支援 MP4 演示直出；\n"
            "Design-MD Chrome 則透過瀏覽器擴充套件，一鍵將線上優秀網站的樣式與 Design Tokens 逆向萃取為標準 DESIGN.md / SKILL.md。"
        ),
        "scenario_recommendations": (
            "• 追求高質感動效、物理彈簧與微互動細節：唯一首選【emilkowalski/skills】；\n"
            "• 快速搭建現代化 SaaS 控制面板與儀表板介面：推薦【nextlevelbuilder/ui-ux-pro-max-skill】；\n"
            "• 糾正 Agent 產出老舊粗糙版面、規範排版間距：必備【Leonxlnx/taste-skill】；\n"
            "• Claude Code 原生快速生成高保真原型與動態展示：首選【alchaincyf/huashu-design】；\n"
            "• 借鑒標竿產品視覺系統、一鍵逆向生成設計規範：首選【bergside/design-md-chrome】。"
        )
    },
    "workflow_domain_skills": {
        "cross_comparison": (
            "專項領域技能讓 Agent 能夠跨出單純編程，進入金融、學術、臨床與成本治理等高度專業化領域。\n"
            "Awesome-LLM-Apps 提供了 100+ 個開箱即用的端到端真實應用案例；\n"
            "Anthropic Financial Services 深入投行財務報表分析與合規審計；\n"
            "Compound Engineering Plugin 專注於複雜軟體工程架構原則落地；\n"
            "Skill Recorder 透過記錄螢幕操作自動轉譯為企業級 Copilot 技能；\n"
            "Browserbase Skills 賦予 Agent 雲端無頭瀏覽器的端到端網頁操控能力。"
        ),
        "scenario_recommendations": (
            "• 尋找開箱即用的 AI 專案實戰範本：首選【Shubhamsaboo/awesome-llm-apps】；\n"
            "• 金融量化、財報分析與合規業務：推薦【anthropics/financial-services】；\n"
            "• 規範團隊架構設計與架構防護：推薦【EveryInc/compound-engineering-plugin】；\n"
            "• 螢幕行為反編譯為 Copilot 技能：推薦【microsoft/skill-recorder】；\n"
            "• 雲端免維護無頭瀏覽器爬蟲與操作：推薦【browserbase/skills】。"
        )
    },
    "mcp_core_servers": {
        "cross_comparison": (
            "Model Context Protocol (MCP) 作為連接 AI 與外部工具的通用協議，核心在於介面標準化與連接器生態。\n"
            "modelcontextprotocol/servers 作為官方參考實作，涵蓋 Git、PostgreSQL、Slack 等黃金標準介面；\n"
            "Chrome DevTools MCP 讓 Agent 具備直接透視網頁 DOM 與 Console 日誌的除錯利器；\n"
            "GitHub MCP Server 實現 PR、Issue 與代碼搜尋的一體化操作；\n"
            "Ruflo 專注於多伺服器編排與快速路由；\n"
            "Context7 則提供極致低延遲的向量記憶體與外部上下文檢索服務。"
        ),
        "scenario_recommendations": (
            "• 搭建基礎 MCP 開發環境：必備【modelcontextprotocol/servers】官方標準套件；\n"
            "• Web 前端與瀏覽器深度除錯：首選【ChromeDevTools/chrome-devtools-mcp】；\n"
            "• 自動化 GitHub PR 審查與 Issue 管理：首選【github/github-mcp-server】；\n"
            "• 分散式多 MCP 伺服器動態路由與集群編排：推薦【ruvnet/ruflo】；\n"
            "• 外部高速知識檢索與資料庫快取：推薦【upstash/context7】。"
        )
    },
    "os_automation_desktop_mcp": {
        "cross_comparison": (
            "桌面與作業系統 MCP 突破了傳統 API 限制，使 Agent 具備操作終端、檔案系統、GUI 螢幕與特定垂直領域的強大能力。\n"
            "DesktopCommanderMCP 提供安全且深度的終端執行管道與基於 Unified Diff 的局部代碼熱打補丁；\n"
            "Peekaboo 專為 macOS 深度客製，具備視窗焦點捕捉、高解析度截圖與整合本地/雲端 VLM 的視覺問答（Visual QA）；\n"
            "Glean 聚焦於跨本機海量檔案的高效增量全文檢索與內容探勘；\n"
            "MCP Taiwan Legal DB 展示了垂直領域（台灣法規與判例）的在地化精準深度檢索；\n"
            "OpenEvidence MCP 則串接全球頂尖臨床實證醫學決策平台，免 API Key 巧妙複用本機已登入 Session。"
        ),
        "scenario_recommendations": (
            "• 終端命令自動化與代碼局部 Patch 精確編輯：首選【wonderwhy-er/DesktopCommanderMCP】；\n"
            "• macOS 視覺化桌面感知、視窗截圖與多模態 VLM 審查：首選【openclaw/Peekaboo】；\n"
            "• 本機百萬檔案全文檢索與歷史代碼庫情報探勘：推薦【LeslieLeung/glean】；\n"
            "• 台灣法律條文查詢、司法判例檢索與合約合規審計：推薦【lawchat-oss/mcp-taiwan-legal-db】；\n"
            "• 臨床醫師與醫學研究者即時查閱權威醫學實證指引：推薦【htlin222/openevidence-mcp】。"
        )
    },
    "system_prompts_engineering": {
        "cross_comparison": (
            "系統提示詞是塑造模型角色邊界、工具調用安全性、思維鏈引導與推理深度的核心底座。\n"
            "System-Prompts-And-Models-Of-AI-Tools 彙整了業界最龐大的商業產品提示詞資料庫（Cursor、v0、Perplexity 等）；\n"
            "System Prompts Leaks 專注於即時曝光最新頂級閉源模型（GPT-4o、Claude 3.7、Grok 等）的指令演進與安全變更；\n"
            "CL4R1T4S 深入提示詞越獄防護、認知邊界黑客測試與防禦性架構；\n"
            "I Have ADHD 採用結論先行（BLUF）的高密度精簡規範，徹底消除 AI 客套廢話；\n"
            "Claude Code System Prompts 完整逆向還原了官方編程 Agent 的 27 個工具定義與 Sub-agent（Plan/Task/Explore）協調機制。"
        ),
        "scenario_recommendations": (
            "• 學習頂級商業 AI 編程 Agent 架構與工具契約定義：首選【Piebald-AI/claude-code-system-prompts】；\n"
            "• 全面調研主流商業 AI 產品系統提示詞工程模式：查閱【x1xhlol/system-prompts-and-models-of-ai-tools】；\n"
            "• 追蹤頂級實驗室前沿模型最新指令與對齊策略更新：首選【asgeirtj/system_prompts_leaks】；\n"
            "• 追求極致簡潔、杜絕 AI 囉嗦廢話、結論先行：強烈推薦【ayghri/i-have-adhd】；\n"
            "• 提示詞注入防護、紅隊測試與防禦邊界設計：參考【elder-plinius/CL4R1T4S】。"
        )
    },
    "agent_specs_rules": {
        "cross_comparison": (
            "從隨機 Prompt 走向結構化規格驅動（Spec-Driven Development）是 Agent 工業化的必經之路。\n"
            "GitHub Spec-Kit 提供了規格第一（Spec-first）的開發範本與驗證工具鏈；\n"
            "Backpass 首創將『梯度下降』引入 AGENTS.md 的自動優化，擺脫純人工盲目試錯；\n"
            "OpenSpec 制定了跨框架通用的 Agent 行為規範格式；\n"
            "Claude Code Best Practice 總結了長期實務累積的最佳實戰準則；\n"
            "BMAD-Method 提出了系統化的 Agent 敏捷開發方法論。"
        ),
        "scenario_recommendations": (
            "• 建立專案標準化規格與自動化生成：首選【github/spec-kit】；\n"
            "• 自動優化與微調 AGENTS.md 規則：首選【kunchenguid/backpass】自動梯度調優；\n"
            "• 制定跨工具跨框架統一規則：推薦【Fission-AI/OpenSpec】；\n"
            "• 終端 Agent 日常避坑與最佳實踐：查閱【shanraisshan/claude-code-best-practice】。"
        )
    },
    "model_routing_gateways": {
        "cross_comparison": (
            "隨著模型碎片化加劇，統一介面、負載均衡與自動容災成為基礎設施核心。\n"
            "LiteLLM 作為業界事實標準，支援 100+ 模型轉換為 OpenAI 介面，功能最成熟全面；\n"
            "CLIProxyAPI 反向封裝各大官方 CLI 工具為標準 API，極具開創性；\n"
            "Claude Code Router 專為 Claude Code 使用者設計，無縫轉發至平價第三方模型；\n"
            "CC-Switch 支援一鍵快速切換模型 Provider 與端點；\n"
            "RTK 則以高效能 Rust 重構，專注於超低延遲模型路由。"
        ),
        "scenario_recommendations": (
            "• 企業級多模型統一網關與帳號管理：唯一首選【BerriAI/litellm】；\n"
            "• 想將本機 Antigravity/Codex CLI 轉為通用 API：首選【router-for-me/CLIProxyAPI】；\n"
            "• Claude Code 搭配平價模型（DeepSeek/Kimi）：推薦【musistudio/claude-code-router】；\n"
            "• 追求微秒級轉發效能：推薦【rtk-ai/rtk】。"
        )
    },
    "token_cost_monitors": {
        "cross_comparison": (
            "重度使用 Agent 的開發者普遍面臨額度不可控與帳單超支焦慮。\n"
            "CodexBar 作為 macOS 狀態列神器，即時視覺化展示各供應商剩餘配額與重置時間；\n"
            "OpenUsage 採用完全本地計算，杜絕隱私洩漏，支援多平台；\n"
            "CCGlass 專注於透視 Agent 在本機目錄中的所有檔案改動與操作熱點；\n"
            "Codeburn 具備代碼級 Token 消耗熱圖追蹤；\n"
            "Usage 則提供極簡輕量級的 CLI 監控工具。"
        ),
        "scenario_recommendations": (
            "• macOS 選單列即時監控額度與重置倒數：首選【steipete/CodexBar】；\n"
            "• 嚴格注重隱私、跨平台多帳戶統計：首選【robinebers/openusage】；\n"
            "• 追蹤 Agent 本機操作痕跡與變更歷史：推薦【jianshuo/ccglass】；\n"
            "• 代碼模組級精確成本審計：推薦【getagentseal/codeburn】。"
        )
    },
    "code_intelligence_ast": {
        "cross_comparison": (
            "語意代碼分析決定了 Agent 是在『瞎猜盲寫』還是『精準掌握全庫脈絡』。\n"
            "Code Review Graph 建立本地優先代碼庫拓撲圖譜，精確計算修改的波及半徑（Blast Radius），大幅節省 70%+ 上下文；\n"
            "ast-grep 以 Rust 與 Tree-sitter 為核心，以 AST 語法樹樣式秒級匹配與無損重構，徹底超越傳統正則 Grep；\n"
            "Graphify 專注於全自動構建跨語言代碼知識圖譜與依賴視覺化；\n"
            "Understand-Anything 著重於自然語言架構對話導航與概念提煉；\n"
            "Codegraph 則提供標準結構化依賴矩陣分析與架構防腐檢測。"
        ),
        "scenario_recommendations": (
            "• 縮減 Agent 上下文長度、避免大型專案修改產生幻覺：首選【tirth8205/code-review-graph】；\n"
            "• 高效能結構化代碼搜尋、Linting 規則定制與批量安全重構：首選【ast-grep/ast-grep】；\n"
            "• 接手陌生大型專案、全自動梳理多語言全庫調用拓撲：推薦【Graphify-Labs/graphify】；\n"
            "• 用自然語言大白話提問代碼庫業務架構與模組職責：推薦【Egonex-AI/Understand-Anything】；\n"
            "• 專案分層依賴檢查、防止循環依賴與架構壞味道審查：推薦【colbymchenry/codegraph】。"
        )
    },
    "web_doc_parsing_ocr": {
        "cross_comparison": (
            "高品質資料抽取是 RAG、微調與 Agent 正確決策的第一哩路。\n"
            "MarkItDown (微軟) 擅長將各類 Office (Word/Excel/PPT)、PDF 與音訊標準化轉換為純淨 Markdown，零外部伺服器依賴；\n"
            "Firecrawl 則是現代網頁採集的事實標準，全自動繞過 Cloudflare 盾牆、渲染動態 SPA 並支援整站 Map 探索；\n"
            "MinerU 專攻高難度學術論文、雙欄排版、複雜跨行表格與 LaTeX 數學公式 OCR 深度提取；\n"
            "Scrapling 以自適應瀏覽器指紋偽裝與極致反反爬著稱，輕巧而強韌；\n"
            "Docling (IBM) 專為 GenAI 上下文而生，產出結構化 JSON 與 Markdown，深度契合 RAG 分塊需求。"
        ),
        "scenario_recommendations": (
            "• 抓取現代動態 Web 內容、SPA 與需繞過強烈反爬的網站：唯一首選【firecrawl/firecrawl】；\n"
            "• 本地 Office、PDF、多媒體零依賴極速轉換為 Markdown：首選【microsoft/markitdown】；\n"
            "• 雙欄學術論文、帶複雜公式表格與掃描件 PDF 高保真抽取：首選【opendatalab/MinerU】；\n"
            "• 構建企業級高保真 RAG 語意預處理與結構化分塊管線：推薦【docling-project/docling】；\n"
            "• 輕量自適應模擬瀏覽器指紋、自研數據採集爬蟲管線：推薦【D4Vinci/Scrapling】。"
        )
    },
    "speech_multimodal_audio": {
        "cross_comparison": (
            "影音多模態工具已從單純轉錄進化為端到端結構化提煉。\n"
            "yt-dlp 作為開源多媒體下載無可爭議的霸主，支援數千家影音平台串流解析；\n"
            "OpenAI Whisper 奠定了現代語音識別（ASR）的精準度基石；\n"
            "VibeVoice (微軟) 帶來革命性的長音訊表現力與多講者對齊；\n"
            "Whisper.cpp 以純 C/C++ 實現零依賴極致效能本地推論；\n"
            "VoxCPM 則提供出色的跨語言多模態語音生成能力。"
        ),
        "scenario_recommendations": (
            "• 海量影音資源批次採集與字幕抽取：首選【yt-dlp/yt-dlp】；\n"
            "• 本地離線、追求極限速度與零依賴語音轉錄：首選【ggml-org/whisper.cpp】；\n"
            "• 追求最高語音辨識精準度：首選【openai/whisper】；\n"
            "• 擬真人聲朗讀與多角色語音生成：推薦【microsoft/VibeVoice】。"
        )
    },
    "long_term_memory": {
        "cross_comparison": (
            "長期記憶層打破了會話邊界，使 Agent 能夠隨時間推移持續學習用戶偏好。\n"
            "Mem0 打造跨應用智慧記憶架構，自動提取用戶特徵並動態更新；\n"
            "MemPalace 在權威記憶 Benchmark 中奪冠，專注於結構化殿堂式索引；\n"
            "Supermemory 專注於個人數位生活的全維度書籤、文章與思維記憶庫；\n"
            "EverOS 堅持 Local-first 與純 Markdown 儲存，保障極致隱私；\n"
            "Claude-Mem 則專為 Claude Code 設計之會話持久化記憶擴展。"
        ),
        "scenario_recommendations": (
            "• 構建具備自我演進特徵的個人化 Agent：首選【mem0ai/mem0】；\n"
            "• 追求超高記憶召回率與精準情境檢索：推薦【MemPalace/mempalace】；\n"
            "• 重視完全本地數據自主權與純文字隱私：推薦【EverMind-AI/EverOS】；\n"
            "• 專門為 Claude Code 添加持久跨會話記憶：首選【thedotmack/claude-mem】。"
        )
    },
    "context_engineering_rag": {
        "cross_comparison": (
            "在 Context Window 雖然擴大但成本與注意力仍有限的現狀下，精準檢索與動態壓縮是必經之路。\n"
            "RAGFlow 專注於深度文檔解析（DeepDoc）與端到端企業級 RAG 平台；\n"
            "Headroom 採用動態剪枝算法，直接壓縮終端工具輸出與繁冗日誌，省下大筆 Token；\n"
            "GraphRAG (微軟) 以社群偵測（Leiden）生成層次化全局摘要，解決了傳統向量 RAG 難以回答全局問題的硬傷；\n"
            "PageIndex 實現了革命性的無向量（Vector-free）樹狀索引；\n"
            "Cognee 專注於以圖論結構將非結構化數據連接為知識圖譜。"
        ),
        "scenario_recommendations": (
            "• 解決巨集性宏觀問答（如『本資料集的核心論點是什麼』）：唯一首選【microsoft/graphrag】；\n"
            "• 壓縮 Coding Agent 工具輸出日誌、節省 Token：必備【headroomlabs-ai/headroom】；\n"
            "• 搭建企業級高保真文檔問答知識庫：推薦【infiniflow/ragflow】；\n"
            "• 輕量級本地圖譜檢索：推薦【topoteretes/cognee】。"
        )
    },
    "diagrams_presentations": {
        "cross_comparison": (
            "架構視覺化與簡報生成正在經歷美學與純靜態化的範式轉移。\n"
            "Next-AI-Draw-io 將 Draw.io 的強大畫布能力與 AI 提示詞無縫融合；\n"
            "Diagram-Design 提供 38 款高質感、零依賴的純 HTML+SVG 出版級圖表，徹底告別 Mermaid 的僵硬排版；\n"
            "Marp 是 Markdown 編譯投影片領域的標竿，支援高度可客製化的 CSS 主題；\n"
            "Open-Design 打造現代設計系統與畫布協作介面；\n"
            "PPT-Master 專注於一鍵自動化 PPT 結構化生成。"
        ),
        "scenario_recommendations": (
            "• AI 生成出版級高顏值技術架構圖：強烈首選【cathrynlavery/diagram-design】；\n"
            "• 具備高自由度拖曳編輯與專業向量圖表：首選【DayuanJiang/next-ai-draw-io】；\n"
            "• 純文字 Markdown 工作流生成技術簡報：首選【marp-team/marp】；\n"
            "• 商業宣傳簡報一鍵排版：推薦【hugohe3/ppt-master】。"
        )
    },
    "cs_curricula_learning": {
        "cross_comparison": (
            "優質的學習庫能幫助工程師跨越黑盒調包階段，深入底層原理與架構思維。\n"
            "Awesome-Interview-Questions 涵蓋各大名廠各技術棧的核心考題與系統設計；\n"
            "LLM-Course (mlabonne) 是 GitHub 上最權威端到端大模型工程路徑（涵蓋微調、量化、評測）；\n"
            "AI-Agents-For-Beginners (微軟) 深入淺出拆解智能體基礎理論與實作；\n"
            "Awesome-Courses 匯總全球頂尖名校（MIT、Stanford、CMU）計算機核心課程；\n"
            "AI Engineering from Scratch 堅持以純 Python 從零手寫 Transformer 與 Agent。"
        ),
        "scenario_recommendations": (
            "• 打算徹底弄懂 Transformer 底層代碼與數學推導：強烈推薦【rohitg00/ai-engineering-from-scratch】；\n"
            "• 系統掌握 LLM 訓練、微調與部署全流程：首選【mlabonne/llm-course】；\n"
            "• 初學者快速建立 Agent 架構概念：首選【microsoft/ai-agents-for-beginners】；\n"
            "• 系統架構設計與求職面試準備：必查【DopplerHQ/awesome-interview-questions】。"
        )
    },
    "terminal_system_productivity": {
        "cross_comparison": (
            "極致的本機開發環境是工程師生產力與操作愉悅感的基石。\n"
            "Oh My Zsh 聚集了全球最龐大的終端插件與佈景主題生態；\n"
            "Open-WebUI 打造最強大的自託管本地大模型對話介面，媲美 ChatGPT 官方體驗；\n"
            "Thaw 專注於 macOS 選單列圖示的高級隱藏與靈活管理；\n"
            "Awesome-Mac 精選了 macOS 平台上所有必備的高效開源應用；\n"
            "WorldMonitor 提供即時全球動態與系統資源儀表板。"
        ),
        "scenario_recommendations": (
            "• 打造美觀高效的 macOS/Linux 命令列終端：必裝【ohmyzsh/ohmyzsh】；\n"
            "• 私有部署本機 LLM 聊天平台（搭配 Ollama/vLLM）：首選【open-webui/open-webui】；\n"
            "• 拯救擁擠混亂的 macOS 頂部選單列：首選【thaw-app/Thaw】；\n"
            "• 全新 Mac 裝機與高效軟體推薦：必看【jaywcjlove/awesome-mac】。"
        )
    }
}

TOP5_PROJECT_PROFILES: Dict[str, Dict[str, Any]] = {
    # 1. coding_agents_cli
    "openclaw/openclaw": {
        "pros": ["具備跨平台電腦深度控制能力，支援全自動多步驟作業系統操作", "星標近 40 萬，社群熱度極高，擴展外掛與生態蓬勃", "強大且靈活的自動化腳本調度與環境適應性"],
        "cons": ["本機完全授權模式具備一定環境污染與安全風險", "架構較為龐大，初期配置與依賴相較輕量 CLI 繁瑣"],
        "scenarios": "需要 Agent 自主跨應用程式、接管本機多工具聯動的進階系統自動化任務",
        "highlight": "全自動作業系統級別控制、跨平台環境適應架構",
        "rationale": "開源自主環境控制智能體的代表作，星標與社群體量巨大。"
    },
    "anomalyco/opencode": {
        "pros": ["完全開源透明，無任何商業黑盒限制", "相容多家模型供應商與本地 Ollama 模型，打破平臺鎖定", "模組化終端架構，社群活躍且易於二次開發"],
        "cons": ["在極端複雜的全庫架構重構任務上，需搭配頂級模型才能達到最佳表現", "官方進階協同外掛相對商業產品較少"],
        "scenarios": "需要自建企業內部私有 Coding Agent、不想被閉源廠商綁定的開發團隊",
        "highlight": "完全開源透明架構、多模型基座相容與廣泛開發者生態",
        "rationale": "擁有超過 20 萬星標的頂級開源 Coding Agent，提供最佳自託管替代方案。"
    },
    "anthropics/claude-code": {
        "pros": ["Anthropic 官方原生出品，與 Claude 3.7 Sonnet 思考模型深度契合", "內建精準的 Sub-agent 分層規劃與 Git Worktree 隔離工作流", "終端交互流暢，代碼庫語意搜尋與重構成功率極高"],
        "cons": ["嚴格綁定 Anthropic 官方 API 與訂閱體系，成本較高", "閉源客戶端，無法自由修改內部 Prompt 或調度邏輯"],
        "scenarios": "追求最極致代碼質量、講究流暢 Git 提交與工程完整度的專業全端工程師",
        "highlight": "原生整合終端 Shell、Sub-agent 分層規劃機制與精準上下文管理",
        "rationale": "引領新一代終端原生 AI 輔助編程標準的標竿之作。"
    },
    "shareAI-lab/learn-claude-code": {
        "pros": ["純 Bash 腳本實作，零外部繁雜依賴，代碼清晰透明", "自底向上完全開源復刻 Claude Code 核心循環，極具教學價值", "體積輕巧，可秒級在任何 Linux/macOS 環境啟動"],
        "cons": ["定位為教學與原型參考，缺乏大型專案所需的進階容錯與圖譜索引", "功能覆蓋較為精簡，無複雜 GUI 或多工作區管理"],
        "scenarios": "希望透徹理解 Coding Agent 底層 Tool-Calling 迴圈原理的開發者與架構師",
        "highlight": "以極致精簡的 Shell 腳本還原商業級 Agent 核心驅動引擎",
        "rationale": "社群中復刻與解析商業 Coding Agent 最透徹、最具教學啟發性的開源專案。"
    },
    "NousResearch/hermes-agent": {
        "pros": ["前沿開源研究機構 NousResearch 打造，針對開源推理模型深度調優", "具備出色的 Tool Use 與結構化函數呼叫執行力", "開源社群支援強大，是探索開源 LLM Agent 邊界的利器"],
        "cons": ["若搭配低參數量模型，在極長上下文推理中可能偶現指令偏移", "周邊外掛生態與整合文件相對商業產品稍有欠缺"],
        "scenarios": "探索私有化部署、搭配開源權重進行自主編程研究的技術團隊",
        "highlight": "針對開源模型指令微調深度優化的自主 Agent 底座",
        "rationale": "代表開源模型陣營在終端編程與自主推理領域的最前沿突破。"
    },

    # 2. multi_agent_swarms
    "msitarzewski/agency-agents": {
        "pros": ["完整定義了軟體開發全流程之多角色虛擬團隊（產品經理、架構師、前端、後端、QA）", "角色職責邊界清晰，任務交接規範完備", "星標突破 15 萬，廣受開發者認可與採用"],
        "cons": ["角色過多時會導致 Token 消耗倍增，多輪協調溝通成本高", "需要適配良好的協調器才能確保決策高效收斂"],
        "scenarios": "需要從需求拆解到測試驗證端到端自動化執行的複雜軟體專案",
        "highlight": "標準化虛擬研發組織架構、全生命週期角色協同規範",
        "rationale": "社群中角色定義最為完備、體系最宏大的虛擬多 Agent 組織架構。"
    },
    "virattt/ai-hedge-fund": {
        "pros": ["將多 Agent 協同應用於高價值金融投研領域，邏輯嚴謹", "包含基本面分析師、技術面交易員、風控官等專屬 Agent 交叉審查", "內建豐富的金融數據介面與回測工作流"],
        "cons": ["高度專注於金融投資領域，無法直接遷移至常規代碼開發", "模型推論成本較高，需謹慎配置 API 頻次"],
        "scenarios": "進行多視角金融市場研判、量化投資研究與自動化策略回測",
        "highlight": "多 Agent 交叉風控審計機制、端到端金融決策流水線",
        "rationale": "垂直領域多 Agent 協同的標竿專案，展示了多模型制衡與風控的極致設計。"
    },
    "block/buzz": {
        "pros": ["採用高併發分散式 Pub/Sub 發布-訂閱架構，通信效率極高", "去中心化蜂巢協作，節點擴展能力出眾", "知名大廠 Block 開源，工程質量扎實"],
        "cons": ["概念抽象，對於小型專案而言架構偏重", "缺乏開箱即用的開箱式業務角色定義"],
        "scenarios": "構建大規模分散式多代理系統、需要高頻低延遲事件廣播的架構",
        "highlight": "基於 Pub/Sub 的分散式去中心化群體智慧通信架構",
        "rationale": "大廠出品之底層高性能多 Agent 通信協議與蜂巢協同底座。"
    },
    "langchain-ai/deepagents": {
        "pros": ["LangChain 官方生態打造，架構規範且與現有 LangChain/LangGraph 生態完美相容", "內建模組化記憶、狀態機持久化與沙箱執行器", "文檔齊全，開發者上手難度低"],
        "cons": ["依賴較多 LangChain 抽象層，除錯時追蹤堆疊較深", "極限效能相較於純 Rust/C 輕量架構稍有開銷"],
        "scenarios": "現有 Python/LangChain 技術棧團隊希望快速落地多 Agent 協同",
        "highlight": "Batteries-included 開箱即用理念、規範化狀態持久化機制",
        "rationale": "現代主流 Python 技術棧中架構最規範、文檔最完備的自主 Agent 框架。"
    },
    "karpathy/llm-council": {
        "pros": ["由 AI 大師 Andrej Karpathy 設計，理念極其精妙且程式碼極致簡潔", "利用多個異構模型互相盲審打分，有效破除單一模型的幻覺與偏見", "無需複雜依賴，幾十行代碼即可落地核心思想"],
        "cons": ["每次決策需同時調用多個模型，API 成本相對較高", "主要用於決策諮詢與方案評審，無內建代碼執行器"],
        "scenarios": "關鍵決策諮詢、架構方案評審、多模型交叉核驗重大技術選型",
        "highlight": "多異構模型匿名交叉審查與加權共識機制",
        "rationale": "極簡優雅地解決了 AI 幻覺問題，是多模型協同評議的黃金範式。"
    },

    # 3. agent_runtimes_sandboxes
    "deepseek-ai/deepseek-harness": {
        "pros": ["貫徹『萬物皆插件』微內核設計，模組化徹底解耦", "為高併發推理與動態調度而生，吞吐效能出類拔萃", "DeepSeek 官方開源，具備頂級架構水準與開源社群號召力"],
        "cons": ["偏向底層架構 SDK，需開發者自行封裝終端交互介面", "文檔偏向工程規範，對初學者門檻略高"],
        "scenarios": "企業級自主 Agent 平台底座搭建、需要高彈性熱插拔插件的大規模服務",
        "highlight": "微內核熱插拔架構、超高吞吐調度與動態能力編排",
        "rationale": "大模型頂級實驗室出品，奠定了現代 Agent Harness 模組化設計標竿。"
    },
    "openinterpreter/openinterpreter": {
        "pros": ["直觀友好的終端交互介面，支援代碼本機沙箱執行", "以 Rust 重構底層核心，運行速度與響應延遲顯著優化", "適配多種平價開源模型，大幅降低使用門檻"],
        "cons": ["在超大代碼庫的跨檔案關聯分析上，不如專門的 AST 圖譜引擎深刻", "高權限執行模式需小心防範破壞性命令"],
        "scenarios": "個人開發者進行數據探索、本地腳本執行、系統日常維護自動化",
        "highlight": "Rust 驅動之高效能終端沙箱、友好的自然語言代碼直出執行",
        "rationale": "終端代碼解釋器領域的絕對王者，星標超 6 萬且持續引領本地執行交互。"
    },
    "herdrdev/herdr": {
        "pros": ["專為 Coding Agent 打造之輕量隔離執行環境，杜絕本機污染", "具備秒級環境狀態快照與一鍵復原（Rollback）機制", "資源沙箱化控管，精準監控進程與網路呼叫"],
        "cons": ["聚焦於安全隔離，自身不提供高階 Agent 推理調度邏輯", "需額外維護容器或虛擬隔離層"],
        "scenarios": "企業團隊執行不受信的外部代碼、或防範 Agent 命令誤操作摧毀開發環境",
        "highlight": "即時狀態快照技術、專用 Agent 隔離防護層",
        "rationale": "精準解決了編程 Agent 權限失控與環境污染的頭號痛點。"
    },
    "karpathy/autoresearch": {
        "pros": ["Andrej Karpathy 親自設計的端到端機器學習科研閉環 Harness", "自動提出假設、編寫代碼、啟動訓練並根據評測指標迭代優化", "代碼結構極度優雅，是科研自動化的典範之作"],
        "cons": ["專門針對 ML 論文與實驗場景，無法通用於一般軟體工程業務", "依賴較高算力 GPU 環境"],
        "scenarios": "深度學習研究員進行超參數搜尋、模型架構微調與自主科研實驗",
        "highlight": "端到端自動科研閉環、自適應實驗評估反饋機制",
        "rationale": "展示了 AI 智能體進行科學探索與自我迭代的未來形態。"
    },
    "vercel-labs/agent-browser": {
        "pros": ["專為 Web 場景設計之無頭瀏覽器 Agent 執行沙箱", "與 Vercel 雲端無伺服器架構深度契合，開箱即用", "支援對複雜 DOM 樹的高效語意壓縮與操作映射"],
        "cons": ["僅限於 Web 瀏覽器環境，無法接管本地作業系統終端", "依賴 Node.js 與無頭瀏覽器進程，記憶體開銷稍大"],
        "scenarios": "網頁端端到端自動化驗證、動態網頁內容探勘與跨頁面 Web 互動代理",
        "highlight": "DOM 語意自適應壓縮、高強健性瀏覽器沙箱調度",
        "rationale": "前端巨頭 Vercel 出品，定義了 Web 領域 Agent 沙箱的最佳實踐。"
    },

    # 4. core_agent_skills
    "obra/superpowers": {
        "pros": ["星標超 28 萬，社群熱度第一，技能庫涵蓋範圍最為全面", "包含大量開箱即用的生產力增強指令與工程工作流", "相容各大主流 Agent 工具，安裝極度簡便"],
        "cons": ["部分技能功能存在重疊，需用戶自行篩選最適合自身工作流的組合", "部分垂直領域專業技能深度稍顯分散"],
        "scenarios": "希望一鍵全面武裝 Claude Code / Codex，獲得全方位能力提升的開發者",
        "highlight": "超大規模開箱即用技能庫、覆蓋軟體工程全方位場景",
        "rationale": "社群影響力最大的技能擴展專案，全方位擴展終端 Agent 的能力邊界。"
    },
    "mattpocock/skills": {
        "pros": ["TypeScript 領域頂級大師 Matt Pocock 精心打造，工程水準極高", "針對現代 Web、React、TypeScript 最佳實踐深度定制，規範嚴格", "直通 .agents 規範，產出的代碼結構標準、易讀且型別安全"],
        "cons": ["高度專注於 Web 與 TS 生態，對 Python/C++ 等其他語言幫助有限", "對開發者本身的代碼架構規範意識有一定要求"],
        "scenarios": "追求現代化 Web 與 TypeScript 最高代碼質量標準的專業工程師",
        "highlight": "頂級 TypeScript / Web 架構工程規範、零冗餘型別安全指令",
        "rationale": "工程實戰價值極高，星標超 25 萬，Web 開發者必備的靈魂技能集。"
    },
    "affaan-m/ECC": {
        "pros": ["Everything Claude Code 彙整了社群最全面的設定、Hooks 與工作流", "星標近 25 萬，內容保持持續高頻更新", "提供了極其豐富的實戰腳本與自定義指令範例"],
        "cons": ["偏向資源集合與配置範例，部分腳本需手動調整路徑與環境變數", "無統一包管理器，需開發者手動按需集成"],
        "scenarios": "希望全景掌握 Claude Code 各項進階隱藏配置、打造專屬客製化終端的工程師",
        "highlight": "全景式 Claude Code 實戰手冊、社群經驗精華總匯",
        "rationale": "Claude Code 生態中最權威、最豐富的百科全書式資源寶庫。"
    },
    "anthropics/skills": {
        "pros": ["Anthropic 官方親自發布之標準 Skill 範例，相容性與權威性最高", "工具呼叫 Schema 定義極其標準，安全防護邊界嚴謹", "所有技能均經過官方嚴格回歸測試，穩定性無庸置疑"],
        "cons": ["數量相對社群精選專案較為克制，僅涵蓋核心通用場景", "更新節奏偏向保守穩定，新興實驗性技能較少"],
        "scenarios": "企業生產環境中追求最高穩定度與合規性之 Agent 工具調用",
        "highlight": "官方黃金標準規範、極致嚴謹的安全性與介面定義",
        "rationale": "官方定義之標準架構，所有第三方技能開發者的遵循基準。"
    },
    "garrytan/gstack": {
        "pros": ["由著名投資人與工程師 Garry Tan 打造，聚焦現代全端快速交付", "標準化現代開發者技術棧，顯著加快 MVP 原型構建速度", "代碼範本現代化，內建良好的最佳架構實踐"],
        "cons": ["技術選型帶有較強個人偏好，對舊有老舊系統適配度有限", "靈活性略遜於完全模組化的原子型技能庫"],
        "scenarios": "創業者與全端開發者需要從零快速孵化高質感 Web MVP 專案",
        "highlight": "現代化全端架構一鍵拉起、創業級高效率交付體系",
        "rationale": "將矽谷頂級工程理念轉化為 Agent 技能，大幅壓縮軟體交付週期。"
    },

    # 5. ui_ux_frontend_skills
    "emilkowalski/skills": {
        "pros": ["由前 Vercel/Linear 頂級動態設計師操刀，審美與動效水準無可匹敵", "封裝了 Framer Motion、彈簧物理與微交互的深層領域知識", "一鍵安裝即刻讓 Agent 產出出版級高階動態網頁"],
        "cons": ["專注於高端前端動效，對後端邏輯或底層演算法無直接作用", "需要現代前端技術棧（React/Tailwind/Framer Motion）相容"],
        "scenarios": "追求頂級數位產品美學、需要為網站打造精緻微交互與流暢動畫的前端團隊",
        "highlight": "線性動效物理模型、現代微交互時序規範",
        "rationale": "前端審美與動態交互領域的最高天花板，徹底告別粗糙僵硬的 AI 生成介面。"
    },
    "nextlevelbuilder/ui-ux-pro-max-skill": {
        "pros": ["覆蓋現代 SaaS 儀表板、複雜表單與資料呈現全方位場景", "星標突破 12 萬，社群驗證充分，產出的 Tailwind CSS 代碼極為專業", "大幅減少前端切圖與排版的時間消耗"],
        "cons": ["在高度自定義的非主流設計系統中，需微調 CSS 變數", "產出的樣式略有 SaaS 模板同質化傾向"],
        "scenarios": "快速搭建商業化 SaaS 控制面板、後台系統與響應式現代網站",
        "highlight": "SaaS 級 UI 元件規範、生產就緒的 Tailwind 佈局體系",
        "rationale": "實用性最強的前端 UI 構建技能包，將原型轉為生產級介面的效率神器。"
    },
    "Leonxlnx/taste-skill": {
        "pros": ["專門針對 AI 缺乏『審美品味（Taste）』的痛點，注入專業設計原則", "嚴格規範排版比例（Typography）、間距系統（Spacing）與留白哲學", "星標超 8 萬，立竿見影改善各類 AI 網頁的視覺廉價感"],
        "cons": ["主要為約束性提示詞規範，需搭配具備代碼生成能力的 Agent 協同", "風格偏向極簡克制，不適合炫目花哨的遊戲風格介面"],
        "scenarios": "希望徹底消除 AI 網頁生成中常見的廉價排版、建立高質感品牌形象的專案",
        "highlight": "數位出版級排版比例系統、極簡克制的現代設計原則",
        "rationale": "從根本上提升 Agent 美學素養的關鍵技能，解決了 AI 生成介面的品味荒漠。"
    },
    "alchaincyf/huashu-design": {
        "pros": [
            "專為 Claude Code 量身打造之 HTML 原生設計 Skill，免額外框架直接生成高保真互動原型與現代幻燈片",
            "內建 20 套頂級設計哲學（極簡、Bento、蘋果風等）與 5 維度客觀設計評審機制，確保產出品質高度穩定",
            "支援一鍵將動態設計匯出為 MP4 影片與高解析度截圖，完全 Agent-agnostic，廣泛相容主流終端工具"
        ],
        "cons": [
            "專注於純 HTML/CSS 原生動效與排版，複雜 3D WebGL 渲染需額外整合外部圖形庫",
            "需在支援即時預覽的瀏覽器或本機靜態伺服器環境下檢視最佳視覺效果"
        ],
        "scenarios": "全端工程師與獨立開發者需要用 Claude Code 迅速落地極致現代美感的前端原型、Landing Page 與高階展示動效",
        "highlight": "HTML 原生設計規範引擎、20 套頂級設計哲學與 5 維度自動評審體系",
        "rationale": "突破了 AI 前端設計粗糙死板的瓶頸，星標近 2.4 萬，是 Claude Code 生態中最專業強悍的原生設計技能。"
    },
    "bergside/design-md-chrome": {
        "pros": [
            "創新 Chrome 擴充套件，可直接從任何心儀的現代網站萃取字體、調色盤、邊距與元件風格",
            "自動編譯生成標準化的 DESIGN.md 或 SKILL.md 規格檔，供 Claude Code、Codex 等 Agent 精確對齊設計系統",
            "基於 TypeUI 規範，消除工程師與設計稿之間的溝通鴻溝，實現『所見即所得』的樣式復刻"
        ],
        "cons": [
            "依賴 Chrome 瀏覽器外掛環境進行網頁萃取，無法在純無頭 CLI 伺服器端獨立運作",
            "面對極度高度混淆或動態 Canvas 繪製的介面，CSS 樣式提取精度需手動微調"
        ],
        "scenarios": "開發者希望借鑒業界標竿產品（如 Linear、Stripe、Vercel）的視覺設計系統，快速為專案建立標準 DESIGN.md",
        "highlight": "一鍵網頁樣式萃取逆向工程、標準 DESIGN.md / SKILL.md 自動產生器",
        "rationale": "巧妙打通了現實網站設計系統向 Agent 規格檔轉換的最後一哩路，實用性與創新度極高。"
    },

    # 6. workflow_domain_skills
    "Shubhamsaboo/awesome-llm-apps": {
        "pros": ["收錄超過 100 個經過端到端驗證的開源 AI 應用範本", "星標突破 13 萬，涵蓋各主流模型、Agent 與 RAG 實戰落地案例", "代碼完全開源且附帶詳盡圖文教程，即拷即用"],
        "cons": ["專案眾多，部分早期案例依賴的模型版本需要隨時同步維護", "偏向開箱即用展示，非單一垂直庫架構"],
        "scenarios": "快速探索特定業務場景（如合約審核、影音總結、智能客服）之最佳實踐",
        "highlight": "100+ 端到端開源 AI 應用矩陣、工業級案例代碼庫",
        "rationale": "社群中規模最大、案例最全的 AI Agent 與應用實戰寶典。"
    },
    "anthropics/financial-services": {
        "pros": ["Anthropic 官方針對金融高價值領域打造之專業方案", "內建財務三表解析、合規風險識別與投資研究工作流", "邏輯極度嚴謹，嚴格遵循金融行業專業術語與準則"],
        "cons": ["高度偏向金融財務領域，非金融場景無法複用", "部分高級分析需配合外部付費金融數據 API"],
        "scenarios": "銀行、券商、投資機構進行財報自動化解析、盡職調查與風控合規審計",
        "highlight": "金融領域專業知識深度對齊、合規級財務報表分析流",
        "rationale": "官方展示 LLM 切入垂直高價值商務場景的旗艦標竿。"
    },
    "EveryInc/compound-engineering-plugin": {
        "pros": ["將複合架構工程（Compound Engineering）方法論落地為外掛規範", "引導 Agent 遵循高內聚低耦合、防禦性編程與測試驅動原則", "顯著提升大型複雜專案生成的架構可維護性"],
        "cons": ["會增加 Agent 生成代碼時的思考輪次與 Token 消耗", "小型腳本任務可能會顯得過度工程化"],
        "scenarios": "多人協同的大型長期軟體架構設計、核心系統重構與高可靠性服務研發",
        "highlight": "複合軟體架構防護線、自適應工程原則約束體系",
        "rationale": "從架構設計哲學高度引導 Agent 寫出經得起時間考驗的企業代碼。"
    },
    "microsoft/skill-recorder": {
        "pros": ["微軟出品，透過錄製螢幕實際操作智慧反推業務意圖", "自動將人類操作序列轉譯為標準化 Copilot 技能代碼", "大幅降低業務專家與非程序員編寫自動化技能的門檻"],
        "cons": ["依賴桌面圖形環境與特定錄製套件，終端伺服器環境無法使用", "複雜分支邏輯仍需人工介入代碼二次修訂"],
        "scenarios": "企業將業務員日常繁瑣的桌面軟體重複操作自動化沉澱為 Agent 技能",
        "highlight": "行為錄製智慧反編譯技術、意圖驅動的 Skill 自動生成",
        "rationale": "開創性地打通了非技術人員向 Agent 傳授專業技能的直覺通道。"
    },
    "browserbase/skills": {
        "pros": ["無縫整合 Browserbase 雲端無頭瀏覽器集群，免受本地環境與反爬困擾", "具備極強的 Captcha 繞過與複雜動態頁面操控能力", "API 設計標準簡潔，與各大 Agent 框架原生相容"],
        "cons": ["依賴外部雲端 Browserbase 服務，超額呼叫需要付費憑證", "網路延遲受遠端雲端集群影響"],
        "scenarios": "需要在雲端進行大批量、強反爬動態網頁資料採集與流程操作的自動化 Agent",
        "highlight": "雲端無頭瀏覽器原生託管、全自動反爬驗證突破",
        "rationale": "解決終端 Agent 操控複雜網頁時最棘手的反爬與渲染難題。"
    },

    # 7. mcp_core_servers
    "modelcontextprotocol/servers": {
        "pros": ["Anthropic 官方核心維護之參考伺服器集群，相容性與權威性第一", "涵蓋 Git、Postgres、Slack、SQLite、Fetch 等全套日常必備工具", "星標突破 9 萬，社群維護活躍，代碼標準規範"],
        "cons": ["部分伺服器（如 Postgres/Slack）需手動配置資料庫連線或 OAuth Token", "部分語言實作為 Node.js，對全 Python/Rust 環境需多維護執行時"],
        "scenarios": "所有採用 MCP 協議的 Agent 開發者搭建外部世界連接通道的必裝底座",
        "highlight": "MCP 協議黃金標準實現、全覆蓋的基礎設施連接生態",
        "rationale": "MCP 生態的基石與源頭，官方標準工具庫的無可替代之作。"
    },
    "ChromeDevTools/chrome-devtools-mcp": {
        "pros": ["由 Chrome 官方團隊打造，具備對真實 Chrome 瀏覽器的像素級透視能力", "支援讀取 DOM 節點、Console 日誌、Network 請求與 Performance 面板", "前端除錯體驗極致流暢，Agent 能直接看見並修復前端報錯"],
        "cons": ["需要本機安裝 Chrome 並開啟遠端除錯端口", "涉及隱私瀏覽數據，需妥善控管執行環境權限"],
        "scenarios": "前端開發者進行全自動網頁除錯、Console 報錯修復與網路性能排查",
        "highlight": "深度整合 Chrome DevTools Protocol (CDP)、全方位的即時 DOM/Console 透視",
        "rationale": "將世界第一瀏覽器的底層除錯能力直接賦予 AI 代理，前端維修神器。"
    },
    "github/github-mcp-server": {
        "pros": ["GitHub 官方親自出品，深度整合 GitHub 全平臺 API", "原生支援 PR 審查、Issue 追蹤、代碼庫搜尋與分支管理", "權限管理精確，支援 GitHub 個人存取權杖（PAT）標準授權"],
        "cons": ["受 GitHub API 速率配額（Rate Limits）嚴格約束", "僅專注於 GitHub 平臺，對 GitLab/Gitea 等自託管平臺不支援"],
        "scenarios": "團隊 CI/CD 流程自動化、AI 智能審查 PR、Issue 自動分類與標籤管理",
        "highlight": "GitHub 官方原生 API 封裝、安全的 OAuth/PAT 權限控管機制",
        "rationale": "GitHub 開發者必備的 MCP 核心節點，徹底打通代碼託管與 Agent 協同。"
    },
    "ruvnet/ruflo": {
        "pros": ["星標突破 7 萬，專注於高效能 MCP 路由分發與多伺服器編排", "提供直觀的管理介面與工具註冊發現機制", "具備出色的請求並發處理與故障隔離能力"],
        "cons": ["定位偏向中繼編排層，需搭配具體下游 MCP 伺服器使用", "學習與配置概念相比單一獨立伺服器略微複雜"],
        "scenarios": "需要同時掛載數十個 MCP 伺服器、進行負載均衡與統一權限控管的企業網關",
        "highlight": "動態 MCP 伺服器路由網格、高併發協議分發引擎",
        "rationale": "MCP 生態中規模最大、架構最先進的多伺服器調度與路由網關。"
    },
    "upstash/context7": {
        "pros": ["基於 Upstash 雲端原生架構，具備毫秒級極致檢索延遲", "專門優化外部高頻資料與會話快取，節省本地儲存開銷", "星標超 6 萬，提供現代化 Serverless 雲端部署體驗"],
        "cons": ["依賴外部雲端 Upstash 服務帳號與連線憑證", "離線或純內網隔離環境無法直接調用"],
        "scenarios": "跨裝置共享 Agent 上下文快取、需要極致讀寫速度的雲端記憶層",
        "highlight": "Serverless 超低延遲快取架構、雲端原生 MCP 上下文存取",
        "rationale": "將雲端無伺服器高速儲存引入 MCP，解決了分散式 Agent 上下文共享難題。"
    },

    # 8. os_automation_desktop_mcp
    "wonderwhy-er/DesktopCommanderMCP": {
        "pros": ["提供高度強大的本機終端命令安全執行管道", "內建基於 Unified Diff 的局部代碼精確補丁與覆蓋功能", "支援檔案系統結構深度搜尋與目錄樹感知，響應極快"],
        "cons": ["對宿主機擁有較大執行權限，需使用者具備基本安全意識", "在 Windows 環境下部分 Unix Shell 指令相容性需留意"],
        "scenarios": "讓 Claude Desktop、Claude Code 等 MCP 客戶端具備直接修改本地代碼與執行命令之能力",
        "highlight": "安全終端控制通道、基於 Unified Diff 的局部代碼精確 Patch 系統",
        "rationale": "讓桌面 AI 真正具備動手寫代碼與跑終端能力的開創性 MCP 伺服器。"
    },
    "openclaw/Peekaboo": {
        "pros": [
            "專為 macOS 深度調優之高效 CLI 與標準 MCP 伺服器，具備對全系統與指定視窗的像素級高解析度螢幕截圖能力",
            "深度整合本機與遠端視覺語言模型（VLM / GPT-4o / Claude 3.7），支援自然語言視覺問答（Visual QA）與 GUI 狀態推理",
            "星標突破 5,000，架構極致輕量純粹，無縫賦予終端 Agent 與 Claude Desktop 即時透視螢幕的『視覺感知力』"
        ],
        "cons": [
            "深度依賴 macOS 原生 ScreenCaptureKit API，不相容 Windows 與 Linux 系統",
            "初次配置需在 macOS 系統偏好設定中明確授權螢幕錄製（Screen Recording）與輔助功能權限"
        ],
        "scenarios": "需要讓 Agent 即時觀察本機螢幕渲染反饋、自動化驗證跨桌面應用 UI 狀態與執行視覺引導任務",
        "highlight": "macOS 原生視窗像素級截圖、整合 VLM 視覺問答之桌面感知 MCP",
        "rationale": "macOS 平台上架構最優雅、體驗最流暢的螢幕視覺感知 MCP 伺服器，真正賦予 Agent 桌面視覺透視力。"
    },
    "LeslieLeung/glean": {
        "pros": ["強大的本地優先代碼與檔案全文檢索引導伺服器", "支援極速增量索引，能輕鬆檢索上萬個檔案的代碼庫", "相容 MCP 標準協議，可直接作為 Agent 的即時情報庫"],
        "cons": ["首次建立全盤索引時需要消耗一定的 CPU 與磁碟 I/O", "主要專注於搜尋檢索，無主動寫入修改檔案能力"],
        "scenarios": "在龐大的個人硬碟、文檔目錄或歷史代碼庫中進行快速語意檢索",
        "highlight": "本地高速增量全文搜尋引擎、低記憶體佔用之索引結構",
        "rationale": "為 Agent 提供毫秒級本地檔案情報檢索，徹底消除大海撈針的痛點。"
    },
    "lawchat-oss/mcp-taiwan-legal-db": {
        "pros": ["開源社群罕見的在地化垂直領域 MCP，收錄台灣最新法規與司法判決判例", "資料結構清洗嚴謹，支援條文號碼精確索引與語意檢索", "完全開源免費，無商業法律資料庫昂貴訂閱門檻"],
        "cons": ["高度專注於台灣法律法規體系，其他司法管轄區不適用", "資料庫體積較大，需要配置本地 SQLite 儲存空間"],
        "scenarios": "台灣法律科技從業者、律師團隊與合規人員進行法規檢索與合約合規審查",
        "highlight": "台灣法規判例全量結構化資料庫、標準 MCP 司法檢索介面",
        "rationale": "垂直行業本土化 MCP 的卓越典範，極具專業實用價值。"
    },
    "htlin222/openevidence-mcp": {
        "pros": ["串接全球頂尖臨床實證醫學決策平台 OpenEvidence", "巧妙複用本地已登入之瀏覽器 Session，免去高昂 API 申請門檻", "自動提取標準 BibTeX 與 Crossref 權威學術引用來源，避免醫療幻覺"],
        "cons": ["依賴本機瀏覽器背景守護進程，需保持登入狀態", "主要面向醫學與生命科學領域，常規編程場景不適用"],
        "scenarios": "臨床醫師、醫學研究者在 AI 輔助下即時查閱權威臨床指引與實證文獻",
        "highlight": "本機 Session 橋接守護進程、權威醫學文獻引用溯源機制",
        "rationale": "頂級專業醫學實證平台的無縫 MCP 串接，極大賦能臨床決策。"
    },

    # 9. system_prompts_engineering
    "x1xhlol/system-prompts-and-models-of-ai-tools": {
        "pros": ["星標超 14 萬，收錄業界最齊全的商業 AI 產品系統提示詞清單", "包含 Cursor、v0、Perplexity、Copilot 等數十款明星產品的原始 Prompts", "對研究 AI 產品架構設計、工具定義策略具有極高的參考價值"],
        "cons": ["純文字靜態資料庫，部分提示詞隨官方產品升級可能存在版本時滯", "缺乏自動化測試與即時驗證腳本"],
        "scenarios": "AI 產品經理與架構師進行競品架構調研、設計專屬系統指令的必備參考書",
        "highlight": "覆蓋最廣泛之商業 AI 產品真實 Prompt 逆向資料庫",
        "rationale": "系統提示詞領域的百科全書，星標超 14 萬，行業公認的最強參考庫。"
    },
    "asgeirtj/system_prompts_leaks": {
        "pros": ["星標超 6 萬，聚焦於最新前沿模型（GPT-4o、Claude 3.7、Grok 等）的洩漏剖析", "更新頻次高，第一時間追蹤各大實驗室最新安全與對齊指令變化", "清晰標註各版本的變更歷史與增刪細節"],
        "cons": ["內容受限於逆向工程與社群爆料，部分非官方完全確認", "格式偏向原始 Markdown 文本，缺乏結構化欄位導出"],
        "scenarios": "追蹤頂級 AI 實驗室最新系統提示詞演進、防禦機制與引導技術的研究人員",
        "highlight": "前沿模型系統指令第一手追蹤、精準版本變更對比",
        "rationale": "緊跟頂級模型最新系統指令變化的前哨站，對齊研究者必讀。"
    },
    "elder-plinius/CL4R1T4S": {
        "pros": ["由知名 AI 安全研究員 Plinius 打造，深研提示詞越獄防護與認知邊界", "揭示了現代 LLM 在極端複雜約束下的對齊脆弱點與安全防禦策略", "充滿黑客精神，為防禦性 Prompt 設計提供強大反思視角"],
        "cons": ["專注於安全性與越獄研究，不適合作為常規工程提示詞模板", "部分技巧具爭議性，需在合規測試環境中實踐"],
        "scenarios": "AI 紅隊測試、提示詞注入（Prompt Injection）防護與企業安全評估",
        "highlight": "前沿提示詞對齊攻擊防禦研究、極限約束下的模型行為剖析",
        "rationale": "提示詞安全與對齊領域的傳奇專案，深刻啟發防禦性系統提示詞的構建。"
    },
    "ayghri/i-have-adhd": {
        "pros": ["強制模型遵循結論先行（BLUF）原則，徹底剔除 AI 廢話與客套鋪墊", "採用極簡的條列式、加粗關鍵詞與短句排版，視覺掃描效率極致提升", "相容各大主流 Agent 與聊天介面，一鍵掛載即刻生效"],
        "cons": ["風格極其冷峻簡潔，不適合需要發散思考或細膩文學創作的場景", "部分初學者可能需要習慣沒有背景說明的直接代碼輸出"],
        "scenarios": "講求極致效率、討厭 AI 冗長廢話、需要一眼抓取代碼與終端命令的工程師",
        "highlight": "結論先行（BLUF）認知約束框架、極高資訊密度的排版過濾",
        "rationale": "精準擊中無數開發者對 AI 囉嗦回覆的痛點，以最簡規範換取最高工作效率。"
    },
    "Piebald-AI/claude-code-system-prompts": {
        "pros": ["完整逆向 Anthropic 官方 Claude Code 最新系統提示詞", "精確還原 27 個內建工具定義、Sub-agent（Plan/Task/Explore）分工邏輯", "包含官方設計的防禦性提示詞與代碼審查標準，含金量極高"],
        "cons": ["高度針對 Claude Code 本體，跨模型適配時需微調語法結構", "需隨官方版本發布持續同步校準"],
        "scenarios": "自研終端編程 Agent、深度理解頂級商業 Coding Agent 架構與工具契約",
        "highlight": "商業級 Coding Agent 核心提示詞全景還原、完整工具調用協議解析",
        "rationale": "透視頂級商業編程 Agent 大腦中樞的唯一權威逆向檔案，極具工程借鑒價值。"
    },

    # 10. agent_specs_rules
    "github/spec-kit": {
        "pros": ["GitHub 官方主導的規格驅動開發（Spec-Driven Development）權威工具集", "星標超 13 萬，提供完備的專案規格模板、驗證工具與 CI 流程", "引導 AI 在動工前先完善架構規格，從根本上避免隨機盲寫與返工"],
        "cons": ["需要團隊建立嚴格的規格先導文化，前期文檔編寫需投入時間", "對極其簡單的一行代碼微調可能略感流程繁瑣"],
        "scenarios": "正規中大型工程專案、團隊多人協同、需要確保 AI 代碼可控與高品質的研發管線",
        "highlight": "GitHub 官方規格驅動體系、前置架構驗證與合約防護",
        "rationale": "推動 AI 編程從經驗式瞎猜邁向工業化規格工程的旗艦標竿。"
    },
    "kunchenguid/backpass": {
        "pros": ["顛覆性地將機器學習『梯度下降（Gradient Descent）』引入 AGENTS.md 規則優化", "透過回測執行軌跡誤差，自動迭代微調規則文字，實現自適應演進", "徹底擺脫全憑人類直覺反覆試錯微調提示詞的原始做法"],
        "cons": ["需要構建測試集與評估反饋環境才能發揮自動優化威力", "演算法計算需調用一定數量的評估推論，產生額外 Token 支出"],
        "scenarios": "企業擁有明確評測指標、希望全自動讓 Agent 規則越用越聰明的自動化 CI 體系",
        "highlight": "可微分代理規則優化理論、AGENTS.md 自動反向傳播調優迴圈",
        "rationale": "提示詞與 Agent 規範優化領域最具顛覆性的數學架構創新，開創自動調優先河。"
    },
    "Fission-AI/OpenSpec": {
        "pros": ["跨框架通用的開放規格標準，星標超 6 萬，廣受開源社群推崇", "結構化定義了 Agent 能力契約、依賴項與交付標準", "具備良好的模組化擴展性，可輕鬆轉換為各大工具的配置文件"],
        "cons": ["在極端特異性的廠商專屬功能上需要自定義擴展 Schema", "社群仍在快速演進中，需注意規格版本相容性"],
        "scenarios": "需要同時適配多種不同 AI 工具、希望維護單一權威規格源頭（Single Source of Truth）的團隊",
        "highlight": "開放跨平台規格標準、結構化能力與約束 Schema",
        "rationale": "打破封閉規格壁壘的通用開放標準，促成 Agent 規格生態的標準化。"
    },
    "shanraisshan/claude-code-best-practice": {
        "pros": ["星標超 6 萬，彙集真實全端工程師在生產環境中使用 Claude Code 的血淚經驗", "總結了上下文視窗管理、Git 分支隔離、測試驅動的最佳實務守則", "完全由實戰踩坑沉澱而來，實用性極強"],
        "cons": ["偏向經驗總結與實踐清單，無專屬二進位 CLI 工具鏈", "部分經驗需配合特定的工程環境方能發揮最大效益"],
        "scenarios": "剛開始使用終端 Agent、希望迅速繞過各種常見陷阱與暗坑的開發者",
        "highlight": "生產實戰血淚避坑手冊、經過實務檢驗的終端協同方法論",
        "rationale": "最接地氣、實戰價值最高的經驗法則寶典，極大縮短學習曲線。"
    },
    "bmad-code-org/BMAD-METHOD": {
        "pros": ["提出了結構化的 BMAD（Build, Measure, Analyze, Deploy）Agent 敏捷開發方法論", "星標突破 5 萬，為 Agent 自主協同提供了完整的工程反饋閉環", "架構邏輯嚴謹，強調可量化與可持續交付"],
        "cons": ["框架相對宏大，需要開發者全面理解其整套方法論模型", "在微型腳本上應用顯得流程偏重"],
        "scenarios": "希望將傳統敏捷開發（Agile）全面升級為 Agent 驅動敏捷體系的高級架構團隊",
        "highlight": "閉環敏捷工程體系、可量化的 Agent 交付生命週期管理",
        "rationale": "為 Agent 時代的軟體工程學提供了完整且自洽的敏捷方法論架構。"
    },

    # 11. model_routing_gateways
    "BerriAI/litellm": {
        "pros": ["業界公認事實標準，統一 100+ 模型供應商為標準 OpenAI 格式介面", "星標近 6 萬，支援負載均衡、金鑰輪轉、費用追蹤與故障自動容災", "生產級高穩定性，具備完備的 Proxy 伺服器與 Python SDK 雙模式"],
        "cons": ["功能極其豐富導致配置項較多，新手部署 Proxy 時有一定學習成本", "高併發代理模式下需合理配置 Redis 快取"],
        "scenarios": "企業級統一大模型網關搭建、混合多供應商接入、生產環境高可用高容災",
        "highlight": "統一跨供應商 API 介面抽象、生產級負載均衡與自動容災機制",
        "rationale": "模型路由與網關領域的無可爭議王者，現代 AI 基礎設施必備組件。"
    },
    "router-for-me/CLIProxyAPI": {
        "pros": ["極具開創性：將本機官方 Antigravity/Codex/Claude CLI 反向封裝為標準 HTTP API", "星標超 5 萬，徹底打破官方工具只能在命令列單獨使用的局限", "零成本讓外部 IDE 與第三方軟體自由調用各大官方官方能力"],
        "cons": ["依賴本機已登入授權之 CLI 工具，不適合無頭伺服器直接部署", "受限於官方 CLI 底層傳輸延遲，極限並發能力受本地進程約束"],
        "scenarios": "想將付費官方 CLI（如 Codex/Claude Code）能力導出為 API 供第三方工具無縫調用",
        "highlight": "反向代理封裝技術、將本機 CLI 轉化為標準 API 服務",
        "rationale": "巧妙打破商業 CLI 生態壁壘的殺手級工具，極大拓寬了官方工具的應用邊界。"
    },
    "musistudio/claude-code-router": {
        "pros": ["專為 Claude Code 使用者量身打造，支援無縫將請求轉發至 DeepSeek/Kimi 等模型", "星標超 3 萬，有效降低日常代碼生成的 Token 帳單費用", "配置簡單，支援動態端點替換與憑證轉發"],
        "cons": ["若轉發至未針對編程對齊的小模型，可能會影響複雜重構的生成品質", "專門優化 Claude Code，通用多模型網關功能不及 LiteLLM 全面"],
        "scenarios": "Claude Code 重度使用者希望在日常簡單任務中無痛換用高性價比模型以節省開支",
        "highlight": "專用協議無損轉譯、平價模型無縫透明替換",
        "rationale": "精準解決了 Claude Code 官方費用高昂問題，為廣大開發者節省巨額帳單。"
    },
    "farion1231/cc-switch": {
        "pros": ["星標高達 13 萬，提供極速便捷的模型切換與端點切換介面", "支援多設定檔一鍵切換，操作體驗極致順暢", "跨平臺相容性好，開箱即用"],
        "cons": ["偏向客戶端配置切換工具，無自建分散式代理網關核心", "高級路由策略（如根據複雜度自動分流）需額外腳本配合"],
        "scenarios": "開發者在不同工作場景下頻繁需要切換不同模型、Proxy 與 API Key",
        "highlight": "極簡直觀的多模型配置動態切換引擎",
        "rationale": "社群中採用率極高的模型切換工具，星標體量巨大，日常實用性極高。"
    },
    "rtk-ai/rtk": {
        "pros": ["以 Rust 語言打造，星標近 8 萬，路由轉發延遲達到微秒級極致", "記憶體與 CPU 開銷極小，極度適合高吞吐場景", "二進位檔案獨立運行，零 Python 依賴開銷"],
        "cons": ["功能偏向純粹的核心路由與轉發，進階商業治理後台不如 LiteLLM 豐富", "二次開發需具備 Rust 語言基礎"],
        "scenarios": "對請求延遲與吞吐有極致苛刻要求的底層推理服務與微服務網關",
        "highlight": "Rust 原生高吞吐核心、極低記憶體腳印與微秒級代理轉發",
        "rationale": "代表了 AI 網關領域在極致效能與工程底層上的最高技術水平。"
    },

    # 12. token_cost_monitors
    "steipete/CodexBar": {
        "pros": ["由頂級 Mac 開發者打造，常駐 macOS 選單列，介面精緻優雅", "即時解析多帳戶（Claude Pro、Codex、Gemini）的即時消耗與配額重置時間", "星標超 2 萬，零延遲監控，徹底杜絕無預警額度耗盡"],
        "cons": ["專門針對 macOS 平台開發，Windows/Linux 使用者無法使用", "依賴解析官方 Session 或 API 介面，官方介面調整時需同步更新"],
        "scenarios": "macOS 上同時使用多款付費 Agent 的重度開發者，隨時掌握配額重置窗口",
        "highlight": "macOS 選單列像素級原生整合、跨供應商配額重置倒數預警",
        "rationale": "macOS 平台上最優雅、最實用的 AI 配額選單列工具，開發者一致好評。"
    },
    "robinebers/openusage": {
        "pros": ["堅持本地優先（Local-first）與純本地計算，完全杜絕隱私洩漏", "跨平臺支援 macOS/Linux/Windows，支援桌面與 CLI 雙重展示", "支援訂閱制與 Token 計費雙重統計，報表詳盡直觀"],
        "cons": ["介面美觀度相較原生 macOS 專用軟體略顯工程化", "需要本地常駐輕量背景守護進程"],
        "scenarios": "嚴格注重隱私安全、跨平臺多裝置的個人與企業團隊費用統籌",
        "highlight": "零數據外洩隱私保證、本地優先多維度用量統計",
        "rationale": "以完全開源與隱私安全立足的配額監控標竿，跨平臺體驗可靠。"
    },
    "jianshuo/ccglass": {
        "pros": ["獨特視角：即時透視 Coding Agent 在本機目錄中的所有檔案修改與動作歷史", "像穿透鏡一樣直觀呈現每次對話消耗的 Token 與檔案 Diff 熱圖", "極大幫助開發者排查 Agent 偷偷修改的代碼檔案"],
        "cons": ["主要專注於本機操作軌跡視覺化，跨雲端費用審計功能相對精簡", "社群知名度尚在擴散中"],
        "scenarios": "需要精確審計 Agent 在本機專案中的每一筆代碼更動與 Token 成本",
        "highlight": "本機操作軌跡穿透透視、檔案變更熱點與成本聯動檢視",
        "rationale": "巧妙結合了代碼安全審計與用量監控，讓 Agent 的所有黑盒操作完全透明。"
    },
    "getagentseal/codeburn": {
        "pros": ["星標突破 1 萬，將 Token 消耗精確定位到具體代碼行與模組", "具備生動的『代碼燃燒率（Burn Rate）』視覺化圖表", "幫助開發者精準找出最吃 Token 的不良 Prompt 與巨型代碼檔案"],
        "cons": ["配置略需與特定專案構建流程相結合", "在超大型項目中持續追蹤需一定記憶體開銷"],
        "scenarios": "團隊需要進行代碼級 Token 成本瘦身（Context Diet）、揪出肥大無效上下文",
        "highlight": "代碼行級 Token 消耗熱力分佈、燃燒率即時預警",
        "rationale": "將成本監控下沉到代碼行細粒度，是企業進行 Token 支出精細化治理的必備利器。"
    },
    "aqua5230/usage": {
        "pros": ["極度輕量純粹的 Python CLI 用量追蹤腳本，零繁重依賴", "幾秒內即可在任何終端機環境完成配置並輸出簡報", "相容標準終端管線，易於整合至個人 Shell 啟動腳本"],
        "cons": ["功能偏向簡潔單一，無圖形化 GUI 儀表板", "缺乏歷史長期趨勢分析與高階報表導出"],
        "scenarios": "追求極簡的終端黑客，希望在命令列敲一行指令即可速查當前額度",
        "highlight": "極簡無依賴 CLI 架構、毫秒級用量數據萃取",
        "rationale": "極簡主義工程工具的典型代表，小巧精悍，滿足純終端極客需求。"
    },

    # 13. code_intelligence_ast
    "tirth8205/code-review-graph": {
        "pros": ["建立本地優先代碼庫拓撲關係圖譜，精確計算修改的波及半徑（Blast Radius）", "為 Agent 提供精準局部上下文，在大型代碼庫中實現 70%+ 上下文節省", "原生相容 MCP 協議，秒級增量索引更新"],
        "cons": ["對於超小型單檔案專案，圖譜優勢不易完全體現", "首次建圖對多語言混合大型倉庫需稍微消耗算力"],
        "scenarios": "大型多檔案代碼庫重構、預防 Agent 盲目載入整個專案引發幻覺",
        "highlight": "波及半徑拓撲分析、MCP 原生相容、70%+ 上下文精準壓縮",
        "rationale": "從根本上攻克了大型倉庫編程時 Context Window 爆炸與幻覺的難題。"
    },
    "ast-grep/ast-grep": {
        "pros": ["以 Rust 深度整合 Tree-sitter，執行速度達到微秒級極致", "基於 AST 抽象語法樹進行代碼模式匹配，徹底超越傳統正則 Grep", "支援多語言精確代碼重構、Linting 規則定制與 VS Code 外掛"],
        "cons": ["需要開發者理解基本語法樹節點概念以撰寫高階比對模式", "純語法層級匹配，不包含運行時型別推斷"],
        "scenarios": "大規模跨檔案結構化代碼搜尋、全自動批量代碼重構與架構規則檢查",
        "highlight": "Tree-sitter 語法樹模式比對、極致 Rust 執行效能、精確代碼置換",
        "rationale": "代碼結構搜尋與重構領域的革命性工具，現代 AI Coding Agent 的核心引擎之一。"
    },
    "Graphify-Labs/graphify": {
        "pros": ["星標超 11 萬，社群熱度最高，全自動構建跨語言代碼語意關聯圖譜", "直觀呈現函數呼叫鏈、類別繼承結構與模組依賴矩陣", "極大幫助開發者和 Agent 快速掌握陌生專案全貌"],
        "cons": ["圖譜規模龐大時前端視覺化渲染對瀏覽器負載較高", "部分動態語言的動態調用難以完全靜態解析"],
        "scenarios": "快速接手數十萬行遺留代碼庫、架構全景梳理與依賴解耦分析",
        "highlight": "全自動多語言代碼拓撲視覺化、端到端架構相依性解析",
        "rationale": "代碼知識圖譜領域體量最大、視覺化最直觀的開源領先專案。"
    },
    "Egonex-AI/Understand-Anything": {
        "pros": ["星標突破 8 萬，專注於自然語言架構導航與代碼語意提煉", "讓開發者可以用大白話提問代碼庫的任何模組與業務邏輯", "支援互動式導覽與架構文檔自適應生成"],
        "cons": ["偏向高層級架構理解，極限細節處的語法樹微重構不及 ast-grep 精準", "需要較高品質的模型支持自然語言問答"],
        "scenarios": "新加入團隊的新人快速熟悉專案、架構文檔自動撰寫與維護",
        "highlight": "自然語言代碼庫對話導航、自適應架構概念提取",
        "rationale": "極大降低了人類工程師與 Agent 理解陌生代碼庫的認知門檻。"
    },
    "colbymchenry/codegraph": {
        "pros": ["星標近 7 萬，輕量且專注的代碼依賴圖分析工具", "易於整合至現有 CI/CD 流程中進行架構防腐檢測", "生成標準結構化依賴矩陣，相容各類視覺化工具"],
        "cons": ["進階跨專案依賴追蹤功能相對精簡", "主要面向靜態依賴分析，無內建 Agent 交互界面"],
        "scenarios": "專案架構分層依賴檢查、防止循環引用與代碼壞味道審查",
        "highlight": "輕量級代碼依賴矩陣分析、架構防腐自動化檢查",
        "rationale": "小巧精悍的高品質代碼依賴分析利器，是工程治理的可靠守門員。"
    },

    # 14. web_doc_parsing_ocr
    "microsoft/markitdown": {
        "pros": ["微軟官方出品，星標近 18 萬，將 Word、PDF、PPT、Excel 一鍵轉為純淨 Markdown", "原生支援音訊 EXIF 提取與圖片 OCR 文字轉換，跨格式相容性無可挑剔", "Python 標準庫設計，無任何複雜外部伺服器依賴，開箱即用"],
        "cons": ["對於排版極其複雜的雙欄學術論文或手寫體掃描件，解析精度不及專用 OCR 引擎", "不支援直接爬取動態網頁"],
        "scenarios": "企業海量文檔標準化入庫、將各類辦公室檔案預處理為 LLM 友好的 Markdown",
        "highlight": "微軟官方多格式解析標準、純淨 Markdown 輸出、零複雜伺服器依賴",
        "rationale": "本地文檔轉換領域的事實標準，星標近 18 萬，實用性與穩定性無可替代。"
    },
    "firecrawl/firecrawl": {
        "pros": ["現代 LLM 網頁抓取的事實標準，星標近 18 萬，完美突破 Cloudflare 盾牆", "全自動無頭瀏覽器集群渲染 SPA 動態頁面，一鍵直出乾淨無雜訊 Markdown", "支援 Crawl（整站爬取）、Map（網站地圖探索）、Scrape（單頁抓取）全功能"],
        "cons": ["自建自託管需要配置 Docker 與無頭瀏覽器集群，稍微耗費伺服器資源", "雲端官方 API 超額需付費訂閱"],
        "scenarios": "需要抓取現代動態 Web 內容、反爬嚴格之網站、構建大模型 Web 知識庫的必備引擎",
        "highlight": "強大的動態 SPA 渲染、自動化反爬繞過、整站地圖映射與純淨 Markdown 直出",
        "rationale": "網頁採集與 RAG 領域最具統治力的新一代基礎設施，徹底終結傳統爬蟲噩夢。"
    },
    "opendatalab/MinerU": {
        "pros": ["星標近 8 萬，專門針對高難度學術論文、教材與複雜 PDF 進行深度結構化解析", "具備頂尖的公式辨識（LaTeX）、複雜跨行表格抽取與雙欄圖文排版還原", "全面超越常規開源 PDF 工具，學術資料處理神器"],
        "cons": ["深度學習模型體積較大，本地運行需依賴 GPU 算力支援", "轉換單頁高解析度文件的耗時相較純文字提取稍長"],
        "scenarios": "海量學術論文入庫、科學教材數位化、金融券商研報高保真結構化提取",
        "highlight": "頂級學術論文公式解析、複雜表格 LaTeX 還原、高保真版面分析",
        "rationale": "學術界與科研領域公認最強的 PDF 與複雜文檔抽取神器，精度拔群。"
    },
    "D4Vinci/Scrapling": {
        "pros": ["星標近 8 萬，極致輕量且具備強大反反爬能力的新一代 Python 爬蟲庫", "自適應模擬真實用戶瀏覽器指紋，輕鬆繞過現代 WAF 與機器人偵測", "語法優雅直觀，兼顧了 Requests 的簡潔與 Playwright 的強健"],
        "cons": ["需要配合自定義清洗邏輯以產出專門針對 LLM 的 Markdown 結構", "無內建整站自動 Map 探索器，需開發者自行編排 URL 隊列"],
        "scenarios": "輕量級高效採集高防護網站、自研數據採集管線、不想維護龐大無頭集群的場景",
        "highlight": "先進瀏覽器指紋偽裝技術、極致輕量反反爬爬蟲引擎",
        "rationale": "將反反爬技術推向新高度的現代採集庫，小巧而極具威力。"
    },
    "docling-project/docling": {
        "pros": ["IBM 開源前沿文檔解析架構，星標超 6 萬，專為 GenAI 上下文構建而生", "支援 PDF、DOCX、PPTX、HTML 等格式的高保真層次化語意解析", "原生產出富結構（Rich Structured）JSON 與 Markdown，便於分塊（Chunking）"],
        "cons": ["對純二進位非結構化文件的處理速度中規中矩", "需要安裝特定的 Python 深度學習相依庫"],
        "scenarios": "構建企業級高保真 RAG 資料預處理管線、精確保持標題階層與文檔邏輯",
        "highlight": "GenAI 專屬文檔階層語意抽取、端到端 RAG 友善分塊輸出",
        "rationale": "大廠開源的現代化文檔處理旗艦，精準契合 RAG 與 Agent 上下文需求。"
    },

    # 15. speech_multimodal_audio
    "yt-dlp/yt-dlp": {
        "pros": ["全球開源多媒體採集無可爭議的絕對霸主，星標近 19 萬", "支援數千家影音串流平台，全自動提取最佳畫質、多語言字幕與音訊軌", "社群極速維護，反制各大平台加密限制的能力無人能及"],
        "cons": ["CLI 參數極其龐大，新手需查閱文檔才能掌握進階過濾指令", "純音訊轉換需本地配合 FFmpeg 套件"],
        "scenarios": "大規模影音數據採集、線上演講課程音訊提取、影音多模態預處理第一步",
        "highlight": "數千家串流平台全相容、多語言字幕無損提取、極致強健之採集管道",
        "rationale": "開源世界最強大的多媒體採集工具，影音多模態資料管線的不二基石。"
    },
    "openai/whisper": {
        "pros": ["OpenAI 官方推出的里程碑語音識別（ASR）模型，星標近 11 萬", "在 68 萬小時多語言多任務數據上訓練，強健性與抗雜訊能力傲視群雄", "廣泛成為全球開源語音轉錄工具的事實標準與底層基石"],
        "cons": ["Large 模型在本地 CPU 執行速度較慢，需要高規格 GPU 或專用推論優化", "長音訊直接轉錄偶有重複幻覺（Hallucination Loop）現象"],
        "scenarios": "高精度語音轉錄、多語言同傳翻譯、課堂與會議錄音結構化文字提取",
        "highlight": "全球語音辨識技術標竿、頂級抗雜訊與多語言泛化能力",
        "rationale": "開啟現代 AI 語音辨識新紀元的傳奇之作，技術成熟度與社群基礎無可撼動。"
    },
    "microsoft/VibeVoice": {
        "pros": ["微軟最新前沿語音多模態研究，星標超 5 萬，表現力與自然度突破性提升", "具備極強的長音訊情感表現力與多講者精確聲學對齊", "架構現代化，深度融合語音合成（TTS）與多模態語音理解"],
        "cons": ["屬於較前沿的研究專案，開箱即用之各平臺打包 GUI 仍在快速完善", "模型推論算力要求相對較高"],
        "scenarios": "高品質長音頻有聲書朗讀、虛擬數字人對話、多角色播客音訊生成",
        "highlight": "長音訊聲學時序精準對齊、高保真情感語音合成架構",
        "rationale": "微軟展示未來語音多模態表現力的開創性項目，引領擬真語音技術方向。"
    },
    "ggml-org/whisper.cpp": {
        "pros": ["純 C/C++ 打造，星標超 5 萬，零外部 Python 依賴，體積極小啟動極速", "極致優化 Apple Silicon（Metal/NEON）與 x86 AVX，在 Mac 上速度飛起", "記憶體佔用極低，甚至可流暢運行於樹莓派與行動裝置"],
        "cons": ["專門針對推論優化，不包含訓練與微調功能", "進階音訊前處理需依賴命令列參數控制"],
        "scenarios": "本地 macOS/Linux 追求微秒級極速啟動、離線純文字轉錄、嵌入式設備部署",
        "highlight": "純 C/C++ 零依賴推論、Apple Silicon 深度加速、極限效能最佳化",
        "rationale": "將 Whisper 推論效能發揮到極致的工程奇蹟，終端本地語音轉錄首選。"
    },
    "OpenBMB/VoxCPM": {
        "pros": ["星標近 4 萬，端到端開源多模態語音大模型，具備優秀的跨語言泛化", "具備語音理解與生成雙重能力，實現流暢的擬真語音對話迴圈", "模型參數量經過精細設計，具備較高的推論性價比"],
        "cons": ["主要面向開源研究與自建對話服務，桌面開箱即用工具鏈仍在繁榮中", "特定稀有方言表現需進一步微調"],
        "scenarios": "搭建全雙工低延遲語音對話 Agent、即時語音問答客服系統",
        "highlight": "端到端語音理解生成一體化、高效能雙向多模態對話架構",
        "rationale": "國產開源在端到端語音多模態模型領域的卓越代表，表現全面。"
    },

    # 16. long_term_memory
    "mem0ai/mem0": {
        "pros": ["開創性自適應個人化記憶架構，星標近 6.5 萬，廣受主流企業採納", "全自動從多輪對話提取用戶偏好與事實知識，並自適應更新與遺忘", "提供極致簡潔的 Python/REST API，幾行代碼即可為任何 Agent 注入永久記憶"],
        "cons": ["高頻記憶寫入與特徵提取會產生額外的 LLM 處理開銷", "預設雲端託管模式需配置憑證，本地自託管需配置向量庫"],
        "scenarios": "為聊天機器人、個人助理注入跨越幾個月的個人習慣與偏好持久記憶",
        "highlight": "動態自我演進記憶架構、跨應用個人特徵自適應沉澱",
        "rationale": "當前開源世界最受推崇的跨會話長期記憶層，引領個人化 Agent 潮流。"
    },
    "MemPalace/mempalace": {
        "pros": ["在權威 Agent 記憶 Benchmark 評測中多項指標斬獲第一，星標近 6 萬", "借鑒人類『記憶宮殿』認知理論，建立層次化空間語意索引", "檢索召回率與防混淆能力出眾，極大避免了傳統記憶的時序錯亂"],
        "cons": ["架構理論相對深奧，自定義底層空間節點時需閱讀論文與規範", "在超海量資料下記憶結構樹構建略耗時"],
        "scenarios": "複雜多步驟任務、需要精準回溯幾週前關鍵指令與約束的進階編程 Agent",
        "highlight": "記憶宮殿層次化拓撲架構、Benchmark 冠軍級高召回檢索能力",
        "rationale": "認知科學與計算機架構完美結合的記憶典範，權威評測實力證明一切。"
    },
    "supermemoryai/supermemory": {
        "pros": ["專注於個人『第二大腦』記憶庫，星標近 3 萬，介面與體驗極致現代", "支援將書籤、推文、筆記、對話一鍵沉澱為可檢索的智慧記憶雲", "具備出色的向量與全文化混合檢索，支援隱私保護"],
        "cons": ["偏向面向使用者的終端知識管理，較底層嵌入式 SDK 略有差異", "完整功能依賴其前端 Web 與服務端架構部署"],
        "scenarios": "個人知識工作者整合碎片化靈感、為自己的所有 AI 工具提供統一記憶源",
        "highlight": "個人全維度數位記憶庫、現代化混合檢索與書籤整合體系",
        "rationale": "個人知識沉澱與 Agent 記憶共享的極致產品化實踐，顏值與實力兼具。"
    },
    "EverMind-AI/EverOS": {
        "pros": ["堅持本地優先（Local-first）與純 Markdown 原生儲存，完全確保用戶隱私", "利用標準檔案系統自演化記憶，跨工具完全便攜（Portable），零廠商鎖定", "對代碼庫與日常筆記完全透明可審計，可用常規文字編輯器隨意修改"],
        "cons": ["在超大規模非結構化語意檢索上，需搭配本地向量索引方能達最佳效能", "社群知名度尚在成長爆發期"],
        "scenarios": "對雲端隱私極度敏感、堅持本地 Markdown 筆記（如 Obsidian/Logseq）工作流的開發者",
        "highlight": "Local-first 純 Markdown 記憶層、完全用戶自主可移植架構",
        "rationale": "堅守本地優先與完全隱私透明的記憶哲學，開創了極客最愛的純文字記憶新路。"
    },
    "thedotmack/claude-mem": {
        "pros": ["星標突破 9 萬，社群中採用率極高，專為 Claude Code 會話記憶打造", "無縫在本地終端保存會話脈絡，讓 Claude Code 在重啟後依舊認識你的專案與偏好", "輕量實用，開箱即用，極大改善重複輸入背景的痛點"],
        "cons": ["高度偏向 Claude Code 生態，跨其他獨立 Agent 工具通用性有限", "主要保存工作區即時會話，非通用向量知識庫"],
        "scenarios": "每天使用 Claude Code 進行軟體開發、希望跨終端工作階段保持記憶連續性",
        "highlight": "終端會話狀態自動持久化、Claude Code 原生無縫掛載",
        "rationale": "精準擊中終端 Agent『重啟即失憶』的核心痛點，社群星標超 9 萬認可。"
    },

    # 17. context_engineering_rag
    "infiniflow/ragflow": {
        "pros": ["星標突破 9 萬，企業級開源 RAG 平台的集大成者", "內建革命性的 DeepDoc 深度文檔理解引擎，對表格、公式、複雜排版精準提取", "提供視覺化工作流編排、豐富檢索調優與可自定義 Chunking 範本"],
        "cons": ["系統較為龐大，完整部署需要配置 Docker 與多個微服務容器", "硬體資源需求相較輕量腳本偏高"],
        "scenarios": "企業構建大規模私有文檔問答系統、金融與政企嚴格排版文檔解析檢索",
        "highlight": "DeepDoc 深度版面理解、端到端視覺化 RAG 工作流編排",
        "rationale": "開源企業級 RAG 平台中的標竿領頭羊，文檔解析深度傲視群雄。"
    },
    "headroomlabs-ai/headroom": {
        "pros": ["星標近 7 萬，專為 Agent 終端日誌與工具輸出打造的極速動態修剪引擎", "在不丟失關鍵報錯與代碼信息的前提下，實現高達 60%+ 的 Token 壓縮", "顯著降低長上下文消耗，大幅預防 Agent 注意力迷失與記憶漂移"],
        "cons": ["專注於上下文修剪，需搭配檢索器才能組成完整 RAG 鏈路", "過度壓縮極少數情況可能遺漏冷門上下文邊角料"],
        "scenarios": "重度終端 Coding Agent 工作流，工具輸出巨長（如測試報告、日誌）的急需瘦身場景",
        "highlight": "動態工具輸出語意修剪、60%+ Token 節省、防止 Agent 注意力分散",
        "rationale": "上下文工程（Context Engineering）領域最精準的減脂神器，大幅降低對話成本。"
    },
    "microsoft/graphrag": {
        "pros": ["微軟官方研發的革命性知識圖譜 RAG，星標超 3.5 萬，顛覆傳統向量相似度檢索", "利用 LLM 自動從非結構化文本抽取實體與關係，Leiden 演算法分群生成層次化摘要", "完美回答宏觀全局問題（如『整份資料集的核心矛盾是什麼』），傳統 RAG 完全無法匹敵"],
        "cons": ["建圖與社群偵測索引階段需調用大量 LLM，前期建立圖譜的 Token 成本較高", "對實時性要求秒級更新的流式資料維護成本較高"],
        "scenarios": "海量非結構化文檔的全局洞察、跨章節複雜概念關聯、宏觀情報綜合分析",
        "highlight": "知識圖譜社群偵測（Leiden）、自下而上層次化摘要、全局問題無損解答",
        "rationale": "徹底打破向量 RAG 檢索邊界的劃時代發明，高階知識架構師必修體系。"
    },
    "VectifyAI/PageIndex": {
        "pros": ["星標突破 3.5 萬，提出大膽創新的『無向量（Vector-free）』分頁索引範式", "以類似書籍目錄與索引頁的樹狀結構直接映射原文，零向量漂移誤差", "檢索結果完全可解釋、可精確定位到具體頁碼與章節段落"],
        "cons": ["對於無固定結構、缺乏邏輯段落的純混亂文字流，目錄組織難度較大", "需要開發者適應跳脫傳統 Embedding 相似度的新思維"],
        "scenarios": "長篇結構化書籍、法律合約合集、技術規格文檔的高保真精確定位與檢索",
        "highlight": "無向量樹狀目錄索引、精確來源對齊、可解釋性百分百檢索",
        "rationale": "挑戰傳統向量 Embedding 霸權的新銳思維，展示了結構化檢索的獨特威力。"
    },
    "topoteretes/cognee": {
        "pros": ["星標超 3 萬，專注於將非結構化資料極速轉換為結構化圖論知識層", "支援多種圖資料庫與向量庫混合存儲，靈活性出眾", "專為 AI Agent 上下文工程設計，提供乾淨易用的 Python 介面"],
        "cons": ["在大規模百萬級節點下需合理配置圖資料庫索引以保證查詢延遲", "學習概念涉及知識圖譜三元組定義"],
        "scenarios": "需要將分散的業務筆記與文檔自動關聯成知識網絡、提供給 Agent 探索推理",
        "highlight": "非結構化文字圖論結構化轉譯、混合圖向量檢索接口",
        "rationale": "將知識圖譜工程化簡化的典範，讓普通開發者也能輕鬆玩轉 Graph RAG。"
    },

    # 18. diagrams_presentations
    "DayuanJiang/next-ai-draw-io": {
        "pros": ["將全球最受歡迎的開源畫布 Draw.io 與 AI 智慧生成深度融合", "支援用自然語言一鍵繪製架構圖，並可在完整的 Draw.io 畫布上自由拖曳二次微調", "支援導出為 XML、SVG、PNG，生態相容性百分百"],
        "cons": ["需要瀏覽器圖形介面互動，不適合純終端 CLI 靜態管線直出", "極其龐大的複雜流程圖初次生成可能需要手動排版微調"],
        "scenarios": "架構師設計系統拓撲圖、開發者需要邊聊邊改、具備高自由度二次編輯的技術圖表",
        "highlight": "Draw.io 原生畫布整合、自然語言草圖秒轉專業可編輯向量圖",
        "rationale": "完美平衡了 AI 生成速度與人類手動精確編輯，架構師最強畫布工具。"
    },
    "cathrynlavery/diagram-design": {
        "pros": ["徹底顛覆 AI 圖表審美的神作，提供 38 款出版級極致美感圖表樣式", "以純 HTML5 與 SVG 標籤編寫，零外部渲染外掛（無須安裝 Mermaid/Graphviz）", "Claude Code、Codex 等 Agent 可直接在終端直出純靜態漂亮圖表"],
        "cons": ["為純靜態 HTML+SVG 程式碼輸出，無拖曳畫布互動編輯界面", "新增全新自定義圖表類型需具備基本 SVG 排版美學素養"],
        "scenarios": "終端 Agent 生成獨立報告、技術部落格架構圖插入、需要高質感出版級設計的場合",
        "highlight": "38 款出版級原創設計範本、純 HTML+SVG 零外掛依賴直出渲染",
        "rationale": "終端 AI 視覺化美學的革命性突破，讓技術報告徹底擺脫死板醜陋的預設圖樣。"
    },
    "marp-team/marp": {
        "pros": ["Markdown 投影片編譯領域無可爭議的行業標竿，生態成熟穩定", "只需專注編寫純文字 Markdown 語法，CSS 樣式引擎一鍵編譯為專業簡報", "相容 VS Code、CLI、GitHub Actions，可輕鬆整合進自動化 CI/CD 導出 PDF"],
        "cons": ["高度依賴 CSS 主題排版，自定義複雜動畫過渡不及專業 Keynote 自由", "排版細節完全由純文字語法控制，需適應純文字排版思維"],
        "scenarios": "技術演講、產品發表會、教學課堂需快速用 Markdown 產出高質感投影片",
        "highlight": "純 Markdown 現代化投影片編譯核心、靈活可擴展之 CSS 主題生態",
        "rationale": "開發者世界最受歡迎的簡報框架，純文字與簡報美學的最佳交匯點。"
    },
    "nexu-io/open-design": {
        "pros": ["星標突破 9 萬，社群影響力巨大的開放設計協作系統", "打通設計師規範與工程師代碼交付，具備出色的畫布協同與元件庫管理", "支援豐富的向量導出與前端代碼即時聯動"],
        "cons": ["系統較為龐大，更適合團隊級協同，個人輕量生成略顯偏重", "學習全套設計工作流有一定門檻"],
        "scenarios": "跨職能團隊（設計師、前端工程師、產品經理）協同打造企業級 Design System",
        "highlight": "設計即代碼協同工作流、高擴展性向量畫布引擎",
        "rationale": "設計領域與前端工程深度融合的開放標竿，星標超 9 萬的實力證明。"
    },
    "hugohe3/ppt-master": {
        "pros": ["專注於中文商務與技術 PPT 的端到端自動化生成，星標超 5 萬", "內建大綱構思、範本匹配、排版最佳化與一鍵導出 PPTX/PDF 完整流程", "貼合國內商業路演、工作匯報與學術答辯的結構化美學"],
        "cons": ["高度聚焦於完整 PPT 簡報結構，單一架構圖繪製並非其核心", "部分範本版式需配合特定的中文字體庫"],
        "scenarios": "職場人士快速生成工作匯報 PPT、創業者準備融資商業路演簡報",
        "highlight": "端到端大綱至 PPTX 自動化編排、符合商業標準之版式美學引擎",
        "rationale": "大幅解放職場人製作 PPT 的繁瑣勞動，端到端交付體驗極佳。"
    },

    # 19. cs_curricula_learning
    "DopplerHQ/awesome-interview-questions": {
        "pros": ["星標超 8.4 萬，全球規模最大的軟體工程面試題庫與系統設計真題匯總", "涵蓋架構設計、演算法、分佈式系統、資安及數十種程式語言的核心考點", "題目均附帶深入淺出的權威解析與工程背景脈絡"],
        "cons": ["內容體量浩瀚龐大，需要讀者具備目標性地選讀與梳理", "偏向綜合技術題庫，非專門針對 LLM 訓練細節"],
        "scenarios": "資深架構師求職準備、技術團隊招聘出題、系統設計深度自我檢驗",
        "highlight": "全語言全技術棧覆蓋之面試真題庫、高含金量系統設計考點解析",
        "rationale": "全球開發者求職與架構複習的鎮山之寶，星標超 8 萬，經久不衰。"
    },
    "mlabonne/llm-course": {
        "pros": ["星標超 8.2 萬，GitHub 上最權威、最系統化的現代大模型工程實戰路線圖", "自底向上涵蓋數學基礎、架構演進、模型預訓練、微調（SFT/RLHF）、量化與部署", "每個模組皆附帶可直接在 Colab/本地運行的端到端手把手代碼 Notebook"],
        "cons": ["內容具備一定深度，完全零基礎初學者需循序漸進", "部分微調代碼需具備基本 GPU 算力配合驗證"],
        "scenarios": "希望從常規軟體開發者徹底轉型為大模型演算法與 AI 工程專家的工程師",
        "highlight": "大模型全生命週期工程知識圖譜、手把手實戰 Notebook 矩陣",
        "rationale": "當前公認最高品質、最全面系統的大模型學習課程，AI 工程師必讀聖經。"
    },
    "microsoft/ai-agents-for-beginners": {
        "pros": ["微軟官方打造之 AI 智能體權威入門指南，星標達 7.4 萬", "深入淺出拆解 Agent 的感知、記憶、規劃與行動四大核心模組", "以模組化代碼範例手把手引導，理論與工程實作高度平衡"],
        "cons": ["偏向初學者與入門進階，對超大規模分散式蜂巢架構涉及較少", "主要展示微軟推薦之架構模式"],
        "scenarios": "初學者系統建立現代 Agent 概念框架、大學課堂教學與企業內訓",
        "highlight": "微軟官方標準 Agent 教學體系、深入淺出的四大核心能力拆解",
        "rationale": "大廠出品之最高品質 Agent 入門權威教材，概念架構清晰無比。"
    },
    "prakhar1989/awesome-courses": {
        "pros": ["星標超 7 萬，匯總世界頂級名校（MIT、Stanford、UC Berkeley、CMU）計算機課程", "收錄操作系統、計算機網路、編譯原理、分佈式系統等 CS 底層核心科目", "所有收錄課程皆附帶官方視頻、講義與作業 Assignment 連結"],
        "cons": ["名校課程對自學者的自律性與數學基礎有較高要求", "耗時較長，適合長期系統化深造而非短期速成"],
        "scenarios": "希望補齊名校 CS 底層基礎（作業系統、編譯原理、網路）、打牢內功的開發者",
        "highlight": "全球頂級名校 CS 硬核課程地圖、完全開放可自學之作業資源",
        "rationale": "電腦科學底層內功修煉的無價寶庫，真正硬核工程師的成長搖籃。"
    },
    "rohitg00/ai-engineering-from-scratch": {
        "pros": ["堅持『從零手寫（From Scratch）』哲學，純 Python 徒手實現 Transformer 與 Agent", "徹底破除黑盒 High-level 庫的迷信，一行一行代碼推導注意力矩陣與反向傳播", "星標突破 5.2 萬，代碼高度自包含，不玩花哨封裝"],
        "cons": ["手寫代碼偏向原理解析與教學驗證，非工業級高效能生產庫", "需要讀者具備基本的矩陣代數運算直覺"],
        "scenarios": "想徹底理解 Attention 機制每一步維度變化與底層數學原理的求知極客",
        "highlight": "純 Python 零黑盒手寫 Transformer、底層注意力矩陣直觀透明解析",
        "rationale": "真正弄懂 AI 工程底層原理的唯一捷徑，拒絕浮躁調包的最佳實踐。"
    },

    # 20. terminal_system_productivity
    "ohmyzsh/ohmyzsh": {
        "pros": ["星標近 19 萬，全球終端機命令列配置無可撼動的事實標準", "擁有數百個官方插件（Git、Docker、Zsh-autosuggestions）與華麗主題", "極致提升日常命令列敲擊速度、歷史命令搜尋與自動補全體驗"],
        "cons": ["載入過多複雜外掛可能稍微增加終端啟動的毫秒級延遲", "需適應 Zsh 語法與設定檔結構"],
        "scenarios": "任何 macOS/Linux 開發者打造終極個人終端機環境的開機第一件事",
        "highlight": "全球最龐大之終端外掛生態、數百款主題與生產力自動補全",
        "rationale": "終端效率領域的傳奇豐碑，星標近 19 萬，現代開發者必備環境。"
    },
    "open-webui/open-webui": {
        "pros": ["星標超 15 萬，自託管本地大模型 WebUI 介面的無冕之王", "具備媲美 ChatGPT 官方的極致視覺體驗，支援多模型並排比對與語音對話", "原生支援 Ollama、vLLM、OpenAI 協議，具備完善的 RAG、外掛與使用者權限管理"],
        "cons": ["部署依賴 Docker 容器，對本機記憶體與硬碟空間有一定要求", "功能極其繁多，初次管理配置項較為豐富"],
        "scenarios": "團隊搭建私有化內網 AI 對話平台、個人本機模型視覺化互動介面",
        "highlight": "媲美官方級高顏值 Web 介面、完整自託管 RAG 與多模型接入支援",
        "rationale": "開源本機 AI 交互介面的絕對天花板，星標突破 15 萬，用戶體驗極佳。"
    },
    "thaw-app/Thaw": {
        "pros": ["以 Swift 深度調用 macOS 底層 API，對選單列圖示進行像素級精準管理", "自定義圖示折疊隱藏、快捷鍵一鍵召回，告別劉海屏遮擋圖示的噩夢", "效能開銷趨近於零，介面優雅簡約，完美契合 macOS 現代設計規範"],
        "cons": ["專門針對 macOS 平台開發，Windows/Linux 不適用", "需要授予 macOS Accessibility 系統權限"],
        "scenarios": "拯救 Mac 頂部狀態列擁擠、解決劉海屏隱藏圖示痛點的強迫症開發者",
        "highlight": "macOS 底層視窗系統深度接管、零效能損耗之選單列動態收納",
        "rationale": "macOS 日常效率工具的顏值與實力典範，精緻解決了現代 Mac 用戶最大痛點。"
    },
    "jaywcjlove/awesome-mac": {
        "pros": ["星標超 11 萬，GitHub 上最全面、分類最權威的 macOS 必備開源與精選軟體清單", "涵蓋開發者工具、效率神器、設計工具、音訊剪輯與系統增強各領域", "長期高頻維護，所有推薦軟體皆標明開源與免費屬性，良心精選"],
        "cons": ["純靜態精選導航清單，需用戶自行前往各自官網下載安裝", "內容龐大，初次閱讀需按需索引"],
        "scenarios": "全新 Mac 裝機必備指南、探索 macOS 平台頂級效率軟體的必查字典",
        "highlight": "全覆蓋 macOS 頂級軟體矩陣、長達數年的社群良心口碑精選",
        "rationale": "Mac 用戶無人不知的裝機第一清單，星標超 11 萬，社群影響力深遠。"
    },
    "koala73/worldmonitor": {
        "pros": ["星標超 8.5 萬，極具極客科幻感的多功能即時全球動態與系統監控儀表板", "整合全球新聞情報、系統資源指標、網路流量與時間軸視覺化", "開源現代化前端架構，支援全螢幕展示與多屏儀表板釘選"],
        "cons": ["偏向資訊監控看板，非日常代碼編輯交互工具", "長時間常駐運行需消耗一定的前端瀏覽器資源"],
        "scenarios": "副螢幕常駐監控看板、團隊作戰指揮中心資訊大屏、極客個人即時情報站",
        "highlight": "極客科幻級視覺儀表板、多源情報流即時彙整與資源監控",
        "rationale": "將終端極客美學與即時情報監控發揮到極致的高人氣開源作品。"
    }
}

TARGET_TOP5 = {
    "coding_agents_cli": [
        "openclaw/openclaw",
        "anomalyco/opencode",
        "anthropics/claude-code",
        "shareAI-lab/learn-claude-code",
        "NousResearch/hermes-agent"
    ],
    "multi_agent_swarms": [
        "msitarzewski/agency-agents",
        "virattt/ai-hedge-fund",
        "block/buzz",
        "langchain-ai/deepagents",
        "karpathy/llm-council"
    ],
    "agent_runtimes_sandboxes": [
        "deepseek-ai/deepseek-harness",
        "openinterpreter/openinterpreter",
        "herdrdev/herdr",
        "karpathy/autoresearch",
        "vercel-labs/agent-browser"
    ],
    "core_agent_skills": [
        "obra/superpowers",
        "mattpocock/skills",
        "affaan-m/ECC",
        "anthropics/skills",
        "garrytan/gstack"
    ],
    "ui_ux_frontend_skills": [
        "emilkowalski/skills",
        "nextlevelbuilder/ui-ux-pro-max-skill",
        "Leonxlnx/taste-skill",
        "alchaincyf/huashu-design",
        "bergside/design-md-chrome"
    ],
    "workflow_domain_skills": [
        "Shubhamsaboo/awesome-llm-apps",
        "anthropics/financial-services",
        "EveryInc/compound-engineering-plugin",
        "microsoft/skill-recorder",
        "browserbase/skills"
    ],
    "mcp_core_servers": [
        "modelcontextprotocol/servers",
        "ChromeDevTools/chrome-devtools-mcp",
        "github/github-mcp-server",
        "ruvnet/ruflo",
        "upstash/context7"
    ],
    "os_automation_desktop_mcp": [
        "wonderwhy-er/DesktopCommanderMCP",
        "openclaw/Peekaboo",
        "LeslieLeung/glean",
        "lawchat-oss/mcp-taiwan-legal-db",
        "htlin222/openevidence-mcp"
    ],
    "system_prompts_engineering": [
        "x1xhlol/system-prompts-and-models-of-ai-tools",
        "asgeirtj/system_prompts_leaks",
        "elder-plinius/CL4R1T4S",
        "ayghri/i-have-adhd",
        "Piebald-AI/claude-code-system-prompts"
    ],
    "agent_specs_rules": [
        "github/spec-kit",
        "kunchenguid/backpass",
        "Fission-AI/OpenSpec",
        "shanraisshan/claude-code-best-practice",
        "bmad-code-org/BMAD-METHOD"
    ],
    "model_routing_gateways": [
        "BerriAI/litellm",
        "router-for-me/CLIProxyAPI",
        "musistudio/claude-code-router",
        "farion1231/cc-switch",
        "rtk-ai/rtk"
    ],
    "token_cost_monitors": [
        "steipete/CodexBar",
        "robinebers/openusage",
        "jianshuo/ccglass",
        "getagentseal/codeburn",
        "aqua5230/usage"
    ],
    "code_intelligence_ast": [
        "tirth8205/code-review-graph",
        "ast-grep/ast-grep",
        "Graphify-Labs/graphify",
        "Egonex-AI/Understand-Anything",
        "colbymchenry/codegraph"
    ],
    "web_doc_parsing_ocr": [
        "microsoft/markitdown",
        "firecrawl/firecrawl",
        "opendatalab/MinerU",
        "D4Vinci/Scrapling",
        "docling-project/docling"
    ],
    "speech_multimodal_audio": [
        "yt-dlp/yt-dlp",
        "openai/whisper",
        "microsoft/VibeVoice",
        "ggml-org/whisper.cpp",
        "OpenBMB/VoxCPM"
    ],
    "long_term_memory": [
        "mem0ai/mem0",
        "MemPalace/mempalace",
        "supermemoryai/supermemory",
        "EverMind-AI/EverOS",
        "thedotmack/claude-mem"
    ],
    "context_engineering_rag": [
        "infiniflow/ragflow",
        "headroomlabs-ai/headroom",
        "microsoft/graphrag",
        "VectifyAI/PageIndex",
        "topoteretes/cognee"
    ],
    "diagrams_presentations": [
        "DayuanJiang/next-ai-draw-io",
        "cathrynlavery/diagram-design",
        "marp-team/marp",
        "nexu-io/open-design",
        "hugohe3/ppt-master"
    ],
    "cs_curricula_learning": [
        "DopplerHQ/awesome-interview-questions",
        "mlabonne/llm-course",
        "microsoft/ai-agents-for-beginners",
        "prakhar1989/awesome-courses",
        "rohitg00/ai-engineering-from-scratch"
    ],
    "terminal_system_productivity": [
        "ohmyzsh/ohmyzsh",
        "open-webui/open-webui",
        "thaw-app/Thaw",
        "jaywcjlove/awesome-mac",
        "koala73/worldmonitor"
    ]
}


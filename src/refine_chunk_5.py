"""
Script to apply curated, high-quality Traditional Chinese (zh-TW) reviews
and accurate categorizations for all 59 repositories in Chunk 5.
"""

import json
from pathlib import Path
from src.categorizer import CATEGORIES_META

CURATED_CHUNK_5 = {
    "parcadei/Continuous-Claude-v3": {
        "category_id": "agent_orchestration",
        "why": "為了解決 Claude Code 終端代理在進行跨會話或長週期開發時，上下文極易中斷遺失、每次重啟需重複說明專案背景，以及 MCP 工具輸出過度膨脹污染 Context Window 造成 Token 浪費的痛點。",
        "how": "透過 Hook 機制結合賬本（Ledgers）與交接文件（Handoffs）進行跨 Session 狀態持久化；設計隔離上下文的子智能體編排系統，並在獨立環境中執行 MCP 呼叫以避免污染主上下文視窗。",
        "what": "提供 109+ Skills、32+ 專門領域 Agents、30+ 自動化 Hooks、跨會話上下文持久化、智慧代碼分析器與多智能體協同開發環境。"
    },
    "espanso/espanso": {
        "category_id": "education_productivity",
        "why": "為了解決日常編程與辦公中頻繁重複輸入長文本、程式碼片段、公式、樣板郵件低效耗時，且傳統文字擴展工具往往跨平台相容性差、閉源且有雲端隱私洩漏疑慮的痛點。",
        "how": "基於 Rust 語言編寫極致效能且隱私優先的系統守護程序，監聽全域鍵盤事件，依據本地 YAML 設定檔匹配觸發縮寫（Triggers），支援自訂 Shell 腳本執行、正則比對與動態表單對話框。",
        "what": "提供跨平台（Windows, macOS, Linux）極速文字替換引擎、豐富的 Package Hub 擴充市集、支援日期/代碼動態計算、完全本機運行的隱私保護機制。"
    },
    "doggy8088/TampermonkeyUserscripts": {
        "category_id": "education_productivity",
        "why": "為了解決日常頻繁使用的各大網站（如 GitHub、Facebook、巴哈姆特、各類技術論壇等）UI 排版不良、操作動線繁瑣、資訊密度過低或缺乏常用自訂捷徑的使用者體驗問題。",
        "how": "基於 JavaScript 為 Tampermonkey 油猴擴充套件編寫使用者腳本（Userscripts），透過 DOM 操縱、樣式注入與請求攔截，對特定網頁進行無侵入式的前端介面改造與功能增強。",
        "what": "提供 Will 保哥多年累積維護的數十款精選油猴腳本合集，涵蓋社群排版優化、開發者輔助工具、表單自動填寫，並附帶繁體中文安裝指引與一鍵更新機制。"
    },
    "anthropics/skills": {
        "category_id": "claude_code_skills",
        "why": "為了解決通用大語言模型助手缺乏特定組織與領域的專門知識、難以遵循嚴格企業規範、標準工作流程（SOP）進行高重複性複雜任務交付的根本限制。",
        "how": "由 Anthropic 官方制定的 Agent Skills 開放標準，將特定領域的提示詞指引、執行腳本、參考手冊封裝為模組化資料夾結構，供 Claude / Claude Code 在對話中依據任務意圖動態按需載入。",
        "what": "提供 Anthropic 官方參考 Skills 實作庫（涵蓋文檔處理、數據分析、企業品牌指南對齊等範例）、Agent Skills 標準規範文件與跨平台部署範本。"
    },
    "qoojoyyoung/mini-llm-arena": {
        "category_id": "education_productivity",
        "why": "為了解決工程師在評估比較不同大模型（LLM）回答品質時，缺乏輕量、無依賴且完全在瀏覽器端運行的對戰工具，並消除將私密 API Key 上傳至第三方後端伺服器的資安隱憂。",
        "how": "採用純靜態架構（純 HTML5 + CSS + 原生 JavaScript，Tailwind CDN 載入），無任何後端、無資料庫與 Docker 依賴；API Key 僅存於瀏覽器 localStorage，直接以前端 Fetch 向模型供應商發起即時呼叫。",
        "what": "提供雙模型即時盲測對戰介面（Model A vs Model B）、本機獨立盲測投票與勝率統計、預設支援 OpenAI、Gemini、Grok 等多端點，支援自訂內部 Gateway 與 i18n 多國語系。"
    },
    "Anionex/banana-slides": {
        "category_id": "visualization_diagrams",
        "why": "為了解決傳統簡報製作過程繁瑣低效、市售 AI PPT 工具模板千篇一律且難以精準解析用戶上傳素材，產出成果往往無法直接導出為可深度二次編輯的 PPTX 檔案的痛點。",
        "how": "基於 Nano Banana Pro 視覺多模態底座與原生 AI 生成架構，支援上傳任意模板圖片與業務素材進行語意解析，透過大綱推演與佈局控制引擎生成幻燈片，並支援對話式局部修改。",
        "what": "提供一站式 AI 原生 PPT 製作 Web 應用、一句話/大綱/文檔生成幻燈片功能、任意自訂模板圖片解析適配、口頭局部微調、一鍵導出高保真可編輯 PPTX 及影片，支援 Docker 本機私有化部署。"
    },
    "thedotmack/claude-mem": {
        "category_id": "context_memory_rag",
        "why": "為了解決各類 Coding Agent（Claude Code, OpenClaw, Codex, Gemini, OpenCode 等）跨 Session 會話時完全失憶、每次開啟新終端都需要重新灌輸專案背景與架構規範的上下文斷層難題。",
        "how": "透過背景守護進程自動攔截捕獲 Agent 會話期間的所有操作與終端互動軌跡，利用 AI 進行語意分析與增量壓縮，在未來的會話啟動時精準比對關聯性並自動注入最關鍵的上下文。",
        "what": "提供跨 Agent 永久記憶層工具庫、會話行為自動捕獲記錄器、AI 上下文壓縮引擎、相關記憶自動檢索注入模組，廣泛支援各大主流編程代理。"
    },
    "abiosoft/colima": {
        "category_id": "education_productivity",
        "why": "為了解決 macOS (及 Linux) 開發者使用 Docker Desktop 時面臨商業授權費用、肥大資源佔用、記憶體洩漏以及對自訂輕量容器運行時支援不足的工程痛點。",
        "how": "以 Go 語言基於 Lima (Linux on Mac) 虛擬化核心打造，提供極簡 CLI 管理輕量 Linux 虛擬機，原生支援 Docker、containerd 運行時與 Kubernetes (k3s)，具備自動通訊埠轉發與目錄掛載。",
        "what": "提供極速容器運行時管理 CLI (`colima start/stop/status`)、完全相容 Docker CLI、Docker Compose 與 nerdctl、一鍵啟用 Kubernetes、多 Profile 虛擬機環境配置。"
    },
    "doggy8088/better-rm": {
        "category_id": "education_productivity",
        "why": "為了解決 Linux/macOS 終端機傳統 `rm` 指令過於危險，一旦誤操作會立即永久清除檔案且無法救援，特別是誤刪根目錄 `/` 或專案 `.git` 目錄會造成災難性損失的問題。",
        "how": "以 Shell 腳本實現智慧安全攔截邏輯，內建高危險系統目錄黑名單防護；將刪除目標移動至垃圾桶目錄而非物理刪除，並在垃圾桶中完整保留原檔案系統路徑結構以便隨時還原。",
        "what": "提供完整相容原生 `rm` 參數（`-r`, `-f`, `-i`, `-v`）的安全刪除工具、危險目錄防護機制、目錄路徑結構保留、彩色狀態日誌輸出與一鍵安裝 Shell 腳本。"
    },
    "Darthwares/ccr-next": {
        "category_id": "model_routing_proxy",
        "why": "為了解決 Claude Code 原生僅限使用 Anthropic 官方帳號與模型、無法靈活接入其他高性價比模型（如 DeepSeek, OpenAI, Ollama 本地模型等）且缺乏針對不同任務智慧分流的限制。",
        "how": "以 TypeScript 打造本機透明路由代理，攔截 Claude Code 的輸出請求，透過內建的轉換器（Transformers）將請求格式與參數自動轉換為目標提供商的 API 協議，支援自訂分流策略。",
        "what": "提供 Claude Code 請求轉發代理 CLI、任務類型智慧路由（背景任務/複雜推理/長文本依需求分流）、`/model` 即時動態切換、相容 OpenAI, Azure, DeepSeek, Ollama 等多家供應商。"
    },
    "musistudio/claude-code-router": {
        "category_id": "model_routing_proxy",
        "why": "為了解決 AI Agent 在終端開發時過度依賴單一昂貴模型、缺乏統一本地控制平面來調度不同能力與成本的模型、以及無法靈活融合自訂工具的架構缺陷。",
        "how": "構建本地統一控制平面（Local Control Plane）與高併發路由網關，在本地終端透明接管各大 Coding Agent 流量，依據規則引擎將複雜推理、日常編碼、背景掃描分發至最適模型。",
        "what": "提供全功能本地路由 CLI、多模型負載均衡與容災備援、Token 成本控管與用量分析、支援 Kimi K3、DeepSeek、OpenAI 等主流模型的無縫融合接入。"
    },
    "memodb-io/Acontext": {
        "category_id": "context_memory_rag",
        "why": "為了解決 AI Agent 在面對多輪複雜任務時缺乏自我學習與經驗積累機制、每次解決問題都從零摸索，且傳統向量 RAG 難以有效儲存與檢索高階技能操作邏輯的難題。",
        "how": "提出「將 Agent Skills 作為記憶層」的全新架構，將 Agent 成功的執行軌跡與反思經驗自動提煉為結構化、可重複調用的 Skill 模組，並透過情境語意匹配在後續任務中動態喚醒。",
        "what": "提供 Acontext 核心運行庫（支援 Python 與 npm 套件）、經驗自動轉化為 Skill 的提取引擎、自我進化記憶中介軟體、以及與 Anthropic Claude 生態的深度適配。"
    },
    "muset-ai/awesome-nano-banana-pro": {
        "category_id": "prompts_and_specs",
        "why": "為了解決新世代視覺生成模型 Nano Banana Pro 在發布前夕，社群開發者與創作者缺乏系統性提示詞（Prompt）工程範例、視覺風格控制手法與多圖一致性生成技巧參考的盲區。",
        "how": "精選並彙整來自社群實測的高品質圖像與完整 Prompt 提示詞，透過靜態 Web Gallery 進行視覺化對比展示，拆解主體描述、風格濾鏡、光影控制與微調參數的結構化撰寫範式。",
        "what": "提供 Awesome 案例精選庫、完整的 Prompt 提示詞手冊、線上展示畫廊（Web Gallery）、以及角色一致性、文字生成、圖像編輯等多場景實測案例。"
    },
    "modelcontextprotocol/servers": {
        "category_id": "mcp_ecosystem",
        "why": "為了解決大語言模型助手與本機環境、檔案系統、資料庫及各類 SaaS 服務溝通時，API 介面碎片化、重複編寫專屬整合代碼且缺乏工業級安全通用標準的核心產業瓶頸。",
        "how": "由 Anthropic 官方引領的 Model Context Protocol (MCP) 核心參考實作庫，定義以 JSON-RPC 為基礎的標準 Client-Server 通訊規範（Stdio / SSE），規範 Tools、Resources 與 Prompts 的暴露與呼叫標準。",
        "what": "提供官方標準參考 MCP 伺服器集（包含 Filesystem, Git, GitHub, PostgreSQL, SQLite, Memory, Fetch, Puppeteer, Slack 等）與 TypeScript / Python SDK 範例。"
    },
    "github/github-mcp-server": {
        "category_id": "mcp_ecosystem",
        "why": "為了解決各類 AI 助理（Claude Code, Cursor, Windsurf 等）無法原生、流暢且安全地存取 GitHub 平台資源，導致程式碼搜尋、PR 審查與 Issue 追蹤工作流嚴重割裂的痛點。",
        "how": "GitHub 官方以 Go 語言實現的 Model Context Protocol (MCP) 伺服器，直接封裝 GitHub 官方 REST 與 GraphQL API，透過 Stdio 或遠端服務為 AI Agent 提供細粒度權限控制的工具調用介面。",
        "what": "提供官方 GitHub MCP 伺服器、自然語言程式庫瀏覽與全文檢索、Issue/PR 自動化管理、Commit 歷史解析、代碼審查與 CI/CD 狀態監控工具集。"
    },
    "doggy8088/copilot-cli": {
        "category_id": "education_productivity",
        "why": "為了解決 GitHub Copilot CLI 終端編程代理剛推出時官方文檔多為英文、且指令與工作流整合細節繁瑣，台灣與華語開發者難以迅速在命令列落地 AI 編程實踐的入門門檻。",
        "how": "微軟 MVP Will 保哥親自撰寫與翻譯整理之繁體中文指南，深入剖析 Copilot CLI 的底層 Agent Harness 運行架構，結合實際開發場景展示如何透過自然語言操作終端與結合 MCP 進行能力擴展。",
        "what": "提供 GitHub Copilot CLI 完整繁體中文使用教學、安裝配置指南、實戰指令示範、MCP 整合技巧與常見問題疑難排解手冊。"
    },
    "ComposioHQ/awesome-claude-skills": {
        "category_id": "claude_code_skills",
        "why": "為了解決 Claude 及 Claude Code 用戶在連接第三方 SaaS 軟體與日常生產力工具時，自建技能門檻高、工具封裝重複度大、且缺乏社群高質量精選技能資源整合的瓶頸。",
        "how": "結合 Anthropic Agent Skills 規範與 Composio 強大的外部工具生態，系統性彙整並標準化數百款涵蓋開發、通訊、生產力與數據分析領域的即插即用技能庫。",
        "what": "提供 Awesome 精選技能索引、詳細的 Claude Skills 撰寫與安裝指南、豐富的第三方服務整合範例（Slack, GitHub, Linear, Notion 等）與二次開發範本。"
    },
    "ShepAlderson/copilot-orchestra": {
        "category_id": "agent_orchestration",
        "why": "為了解決使用 GitHub Copilot 輔助開發時，開發者常在規劃、實作、測試之間頻繁切換造成上下文混亂，且缺乏架構約束容易導致測試覆蓋率下降或破壞既有代碼的難題。",
        "how": "提出「管弦樂團（Orchestra）」多 Agent 編排模式，嚴格落實測試驅動開發（TDD）原則，將任務流轉劃分為 Planning（規劃）→ Implementation（實作）→ Review（審查）→ Commit（提交）四個由專用子智能體執行的閉環。",
        "what": "提供 GitHub Copilot 多 Agent 協同編排工作流、TDD 規範約束模版、代碼品質審查守門機制（Quality Gates）與標準化敏捷交付指南。"
    },
    "x1xhlol/system-prompts-and-models-of-ai-tools": {
        "category_id": "prompts_and_specs",
        "why": "為了解決業界頂尖商業 AI 編程與生產力產品（Cursor, Devin, Lovable, v0, Windsurf 等）系統指令高度黑盒化、工程師與研究者缺乏公開真實的商業級 Prompt 與工具設計參考的困境。",
        "how": "透過社群協同逆向工程、封包分析與安全審計，精確提取各大頂級 AI 工具底層完整的 System Prompts、內部工具 Schema 定義、多輪對話防禦機制與模型調度規則。",
        "what": "收錄 30+ 款主流商業 AI 工具（包含 Cursor, Claude Code, Devin AI, Manus, Lovable, v0 等）之完整系統提示詞典藏、內部工具規格清單與模型參數架構解析。"
    },
    "openai/codex": {
        "category_id": "agent_orchestration",
        "why": "為了解決軟體開發者在終端環境中需要一個極致輕量、無依賴且具備高度自主性（能直接理解代碼庫、執行終端機命令與運行測試）的本地原生 AI 編程智能體。",
        "how": "OpenAI 官方以 Rust 打造的高效能輕量終端 Coding Agent，直接在本地運行，深入整合終端 Shell 與本機檔案系統，支援端到端任務規劃、自主代碼編輯與錯誤自動修復。",
        "what": "提供 Codex CLI 終端命令列二進位工具、VS Code / Cursor / Windsurf 編輯器整合外掛、沙箱指令執行環境與跨平台安裝套件。"
    },
    "google-gemini/gemini-cli": {
        "category_id": "agent_orchestration",
        "why": "為了解決終端工程師需要直接在命令列環境中充分發揮 Google Gemini 百萬級 Token 超長上下文、多模態理解與強大代碼推理能力的原生代理工具需求。",
        "how": "Google 官方以 TypeScript 開發的開源終端 AI Agent，深度整合命令列與 Git 工作區，支援自然語言規劃、檔案讀寫與 Shell 執行，並內建 Model Context Protocol (MCP) 雙向整合能力。",
        "what": "提供 Gemini CLI 終端交互式 Agent、多輪對話與工具呼叫循環、MCP 伺服器/客戶端支援、長文本專案分析與命令列自動化執行功能。"
    },
    "yusufkaraaslan/Skill_Seekers": {
        "category_id": "claude_code_skills",
        "why": "為了解決將龐大複雜的開源專案技術文件、GitHub 儲存庫或 PDF 格式規格書手動轉為 Claude Skills 過程極為繁複，且各技能間容易因語意重疊而引發執行衝突的痛點。",
        "how": "以 Python 打造全自動抓取與結構化提煉管線，解析爬取網頁、原始碼與 PDF，利用 AI 生成標準 Claude Skills，並內建自動化衝突檢測演算法（Conflict Detection）以確保技能互不干擾。",
        "what": "提供文件自動爬取與 Skill 轉換 CLI、技能衝突檢測工具、MCP Server 整合支援、多語言文件抓取模組與一鍵打包部署腳本。"
    },
    "doggy8088/spec-kit": {
        "category_id": "prompts_and_specs",
        "why": "為了解決開發者在使用 AI 輔助編程時盲目進行「直覺式寫程式（Vibe Coding）」、導致缺乏驗收標準、架構走樣與邊界條件遺漏的軟體工程失控危機。",
        "how": "Will 保哥推廣維護的規格驅動開發（Spec-Driven Development, SDD）繁體中文工具包，以結構化 Markdown 規格引導需求定義、技術方案與驗收測試，讓 AI Coding Agent 有章可循。",
        "what": "提供 Spec Kit 規格生成工具、SDD 標準流程範本、繁體中文實戰指南、與 GitHub Copilot / Claude Code 的規格協同整合腳本。"
    },
    "Open-Dev-Society/OpenStock": {
        "category_id": "education_productivity",
        "why": "為了解決彭博終端等專業金融市場資訊平台訂閱費用高不可攀、廣大散戶投資者與獨立開發者難以取得即時高頻行情與深度財務分析工具的資源不均問題。",
        "how": "採用 Next.js、TypeScript、Tailwind CSS 與 Shadcn UI 打造現代化響應式全端架構，整合 Inngest 背景非同步事件流與即時金融資料 API，提供完全開源、透明且永久免費的市場監控方案。",
        "what": "提供即時股票行情走勢圖、個人化自訂價格警報、公司財務指標與新聞洞察、完全開源的自託管儀表板與現代化 UI 介面。"
    },
    "Fission-AI/OpenSpec": {
        "category_id": "prompts_and_specs",
        "why": "為了解決 AI Coding Assistants 在處理跨檔案大型功能時常常因為需求語意不清而重複打轉、修改偏離架構設計且缺乏全生命週期單一事實來源的難題。",
        "how": "提出規格驅動開發（Spec-Driven Development）標準化架構，將軟體工程的需求規範（Specs / PRDs）轉化為 AI 可解析執行的機器指令，串聯設計、編碼、審查與驗收各環節。",
        "what": "提供 `@fission-ai/openspec` 命令列工具、多款 AI 助手（Claude Code, Cursor 等）的規格驅動模版、規格一致性自動化檢查器與工程交付規範。"
    },
    "simonw/claude-skills": {
        "category_id": "claude_code_skills",
        "why": "為了解決初期 Anthropic 在 Claude.ai 程式碼直譯器環境內預載之 `/mnt/skills` 技能庫內容封閉不透明、社群無從得知其官方預設工具實現邏輯的研究障礙。",
        "how": "由知名開源開發者 Simon Willison 利用提示詞引導 Claude 將其沙箱環境中的 `/mnt/skills` 整個目錄打包壓縮並公開存檔，揭露其內部 Python 腳本與提示詞架構。",
        "what": "提供早期 Anthropic 官方程式碼直譯器技能庫存檔（文檔處理、PDF 解析等）、提取手法提示詞範例、以及指向後續官方開放倉庫的演進歷程說明。"
    },
    "GitYCC/TempDD": {
        "category_id": "prompts_and_specs",
        "why": "為了解決 AI 輔助編程中黑盒自主代理容易脫離控制、缺乏規範約束，而純手動引導又耗費過多溝通時間的人機協同（Human-in-the-loop）效率瓶頸。",
        "how": "提出範本驅動開發（Template-Driven Development）工程框架，透過結構化範本規範人機互動邊界與思考流程，降低溝通歧義，確保 AI 生成代碼的架構穩定性。",
        "what": "提供 TempDD 範本管理 CLI、多語系範本庫（繁體中文、簡體中文、英文、日語、西班牙語）、工作流程編排規則與 AI 程式設計實戰規範。"
    },
    "doggy8088/Learn-Git-in-30-days": {
        "category_id": "education_productivity",
        "why": "為了解決軟體工程師從傳統版控轉換至 Git 分散式版本控管時，概念抽象、分支合併衝突頻繁且缺乏高品質繁體中文體系化實戰教材的痛點。",
        "how": "微軟 MVP Will 保哥第 6 屆 iT 邦幫忙鐵人賽年度大獎得獎著作，由淺入深解析 Git 底層資料物件、工作區與暫存區狀態機，並分享大型團隊由 SVN 遷移至 Git 的真實避坑心法。",
        "what": "提供完整的「30 天精通 Git 版本控管」開源繁中電子書、圖解教程、多國語系目錄、常見問題指南與日常高頻實用 Git 指令速查手冊。"
    },
    "doggy8088/codex": {
        "category_id": "agent_orchestration",
        "why": "為華語開發者提供 OpenAI 官方 Codex CLI 輕量終端編程代理的實踐指南、在地化相容性測試與環境設定參考。",
        "how": "基於 Rust 構建的本地端原生編程 Agent，深度整合終端 Shell 與檔案讀寫，Will 保哥維護之分支聚焦於終端命令執行安全、權限管理與華語開發者上手路徑。",
        "what": "提供 Codex CLI 本地安裝手冊、終端交互配置優化、命令列自動化執行教學與實用輔助腳本。"
    },
    "doggy8088/gemini-cli": {
        "category_id": "agent_orchestration",
        "why": "為台灣與華語開發者提供 Google Gemini CLI 終端 AI 智能體的在地化繁中推廣、實戰測試與最佳化配置示範。",
        "how": "以 TypeScript 開發的終端 AI 助手，封裝 Google Gemini API 與命令列互動循環，支援工具調用、長上下文分析與自動化終端機指令執行。",
        "what": "提供 Gemini CLI 快速安裝手冊、繁中說明文檔、本地 API 端點配置範例與命令列 AI 自動化開發指引。"
    },
    "github/spec-kit": {
        "category_id": "prompts_and_specs",
        "why": "為了解決現代軟體工程在使用 AI Coding Agent 時過度依賴直覺（Vibe Coding）導致需求理解偏差、測試覆蓋不足與大型專案架構崩壞的失控難題。",
        "how": "GitHub 官方倡導的規格驅動開發（Spec-Driven Development）開源工具包，建立「先定義規格、後撰寫代碼」的標準流程，以結構化 PRD 與 Spec 模版約束並引導各類 AI 編程智能體。",
        "what": "提供 Spec Kit CLI 工具、規格生成與檢查腳本、跨 AI 代理標準化工作流、組織級架構對齊規範模版與開源社群實踐指南。"
    },
    "doggy8088/best-wsl-ubuntu-setup": {
        "category_id": "education_productivity",
        "why": "為了解決 Windows 開發者在初次搭建 WSL2 與 Ubuntu 開發環境時，字型渲染不良、終端機配置繁瑣、Docker 整合障礙與 Shell 工具鏈缺乏最佳化設定的踩坑痛點。",
        "how": "Will 保哥結合多年 Windows + Linux 混合環境全端開發經驗，系統化梳理出最佳環境配置方案，透過標準化 Shell 腳本自動安裝 Windows Terminal、zsh/oh-my-zsh 與開發必備套件。",
        "what": "提供 WSL2 + Ubuntu 22+ 最佳化配置手冊、一鍵環境初始化 Shell 腳本、Windows Terminal 設定檔優化指引與開發者避坑問答。"
    },
    "microsoft/VibeVoice": {
        "category_id": "web_doc_parsing",
        "why": "為了解決傳統語音合成（TTS）與語音辨識（ASR）模型在多說話者對話自然度不足、串流延遲高、缺乏生動情感表達以及長音訊生成難以對齊的技術瓶頸。",
        "how": "微軟開源的前沿語音 AI 基礎架構，融合先進的神經音訊編解碼器、擴散模型與自回歸架構，支援極低延遲的即時雙向串流語音合成與超高精度語音辨識。",
        "what": "提供 VibeVoice 預訓練模型權重、Streaming TTS 即時串流示範、ASR 語音辨識管線、Colab 實作筆記本與多語言語音推理 API。"
    },
    "bmad-code-org/BMAD-METHOD": {
        "category_id": "prompts_and_specs",
        "why": "為了解決在 AI 驅動開發（AiDD）興起後，工程師容易完全交出架構主導權而放棄深度思考，導致軟體架構腐化、技術債迅速累積且無法應對敏捷需求變更的危機。",
        "how": "提出突破性敏捷 AI 驅動開發方法論（BMAD），主張「把想法變成可用軟體而不放棄思考」，透過架構決策顯式化（ADR）、明確模組邊界與敏捷反思迴圈全程把控軟體演進。",
        "what": "提供 BMAD 方法論全套實務規範、架構決策紀錄範本、敏捷 AI 協同提示工程清單與工程交付流程指引。"
    },
    "vijaythecoder/awesome-claude-agents": {
        "category_id": "agent_orchestration",
        "why": "為了解決單一 Claude Code 終端智能體在執行大型全端專案時難以同時兼顧多種專業角色、容易因上下文混合而降低各項任務精準度的問題。",
        "how": "構建基於 Claude Code 的子智能體（Sub-agent）虛擬開發團隊架構，將全端工作流拆解為專職角色（架構師、前端、後端、QA、DevOps），透過調度器進行流水線任務交接。",
        "what": "提供多專門子智能體配置範本、端到端功能開發編排腳本、Token 消耗監控指引與跨技術棧專家級提示詞集合。"
    },
    "contains-studio/agents": {
        "category_id": "claude_code_skills",
        "why": "為了解決開發者在使用 Claude Code 時缺乏生產驗證過的專業 Agent 角色配置、手動從頭編寫各技術棧專屬提示詞費時費力的困擾。",
        "how": "將 Contains Studio 團隊內部實際於生產環境使用之專業 AI Agents 規範全面開源，採用模組化 Markdown 角色定義，直接部署至 `~/.claude/agents/` 目錄即可被 Claude Code 自動調用。",
        "what": "提供涵蓋軟體架構、前端設計、後端邏輯與代碼重構的多款開箱即用 AI Agent 設定檔集合，支援一鍵複製導入本機終端。"
    },
    "wshobson/agents": {
        "category_id": "claude_code_skills",
        "why": "為了解決主流 AI 編程工具（Claude Code, Codex, Cursor, OpenCode, Antigravity, Copilot）外掛協議各自為政、開發者難以跨平台共用優質 Agent 技能與命令的碎片化難題。",
        "how": "構建跨 Harness 的 Agentic 外掛市集架構，以單一 Markdown 原始碼為基準，自動跨端轉譯並原生適配各大主流 Coding Agent 執行環境。",
        "what": "提供收錄 94+ 插件、202+ 智能體、183+ 技能與 105+ 命令的生產級 Agent 外掛庫，全方位適配 Claude Code、Codex CLI、Cursor、OpenCode 與 Google Antigravity。"
    },
    "amitkmaraj/gemini-cli-custom-slash-commands": {
        "category_id": "claude_code_skills",
        "why": "為了解決 Google Gemini CLI 使用者在終端進行日常重複性工作（如相片智慧分類整理、數據報表自動產出等）時缺乏便捷直觀的快捷命令封裝的效率問題。",
        "how": "利用 Gemini CLI 提供的客製化斜線命令（Slash Commands）架構，將多模態提示詞、終端指令與檔案處理腳本封裝為高可用的一鍵式終端指令。",
        "what": "提供 10 款專門面向日常生產力與開發任務的 Slash Commands（包含 `/photo-rename` 照片依內容命名、`/report-gen` 數據分析報告等）與完整自訂手冊。"
    },
    "GitYCC/Open-Vibe-Developers": {
        "category_id": "prompts_and_specs",
        "why": "為了解決 Vibe Coding（直覺式 AI 編程）在工程實踐中常面臨的程式碼脆弱、改動牽一髮動全身、缺乏長期脈絡引導以及架構不合理的生產級障礙。",
        "how": "凝聚社群開發者智慧，共同研究如何將 Vibe Coding 引入生產級工程領域，深入探討脈絡構建（Context Building）、系統架構推演、UI/UX 規範與人機協同品質把控。",
        "what": "提供 Open Vibe 開源社群研討綜合文件、脈絡引導技巧手冊、合適系統架構推演指引與生產級 AI 輔助開發實踐指南。"
    },
    "ggml-org/whisper.cpp": {
        "category_id": "web_doc_parsing",
        "why": "為了解決 OpenAI 官方 Python 版 Whisper 模型體積龐大、依賴複雜且推論速度受限，難以在資源受限的終端或邊緣設備上極速進行本機語音識別的瓶頸。",
        "how": "Georgi Gerganov 以純 C/C++ 重新實現 Whisper 模型（基於 GGML 算子庫），零外部依賴、極致輕量，針對 ARM NEON、AVX 以及 Apple Silicon Metal 進行硬體級深度優化。",
        "what": "提供高效能語音轉文字 CLI 工具 (`whisper-cli`)、C/C++ 核心動態庫、多語言綁定（Python, Go, Node.js 等）、即時語音流辨識範例與 WebAssembly 瀏覽器運行支援。"
    },
    "shareAI-lab/learn-claude-code": {
        "category_id": "prompts_and_specs",
        "why": "為了解決廣大工程師對 Claude Code 等先進 Coding Agent 內部架構存在黑盒迷思、缺乏自底向上透過原生代碼理解 Agent Harness 核心機制的教學資源。",
        "how": "提出「Agency 來自模型，Agent 產品 = Model + Harness」核心觀點，僅使用最純粹的 Bash 與極簡 Python，從零開始（0 to 1）逐步復刻出一個 nano 版本的 Claude Code 式 Agent 運行架構。",
        "what": "提供自底向上構建 Coding Agent 的完整教學庫、逐步實現的 Bash/Python 腳本、工具呼叫循環實作、上下文修剪機制與繁中/簡中/英文對照手冊。"
    },
    "GitYCC/context-engineering-intro-zh": {
        "category_id": "prompts_and_specs",
        "why": "為了解決 AI 編程助理在面對複雜真實專案時，傳統 Prompt Engineering 與純直覺 Vibe Coding 難以維持上下文一致性、容易產生低階失誤的困境。",
        "how": "系統性建立「上下文工程（Context Engineering）」實戰體系，以 Claude Code 為核心，透過 `CLAUDE.md`（專案規範）、`INITIAL.md`（初始需求）與自動產生的 PRP（Product Requirements Prompt）三層上下文架構引導 Agent 端到端交付。",
        "what": "提供 Context Engineering 繁體中文範本專案、`/generate-prp` 與 `/execute-prp` 工作流腳本、豐富範例程式庫與工程化落地實踐手冊。"
    },
    "microsoft/markitdown": {
        "category_id": "web_doc_parsing",
        "why": "為了解決在建立 LLM 與 RAG 應用時，企業中大量各類格式的文件（PDF, Word, Excel, PowerPoint, 音訊等）解析繁瑣、格式雜亂且缺乏官方標準化轉換工具的痛點。",
        "how": "微軟 AutoGen 團隊開發的 Python 工具庫，整合多種底層文檔解析引擎與多模態模型（Whisper/視覺 OCR），自動將各類二進位文件抽離並轉換為段落分明、表格保留的高品質 Markdown。",
        "what": "提供 MarkItDown CLI 與 Python SDK，支援 PDF, DOCX, PPTX, XLSX, 音訊（語音轉逐字稿）, 圖片 OCR, HTML 與各類純文字格式轉換。"
    },
    "open-webui/open-webui": {
        "category_id": "education_productivity",
        "why": "為了解決開源模型（如 Ollama, vLLM）以及商業 API 缺乏一個介面美觀、功能完備、完全支援本機離線私有化部署且具備企業級權限管理的 Web 操作平台。",
        "how": "基於 Python 與 SvelteKit 開發的現代化全端平台，原生適配 Ollama 與 OpenAI 相容 API，內建基於本機向量資料庫的 RAG 檢索管道、多模態支援與精細的 RBAC 角色權限管理。",
        "what": "提供開箱即用的現代化 AI 對話 Web 介面、支援 Ollama 與各大商業 API、內建文件 RAG 問答、自訂 Modelfile 智能體市集、Pip/Docker 一鍵安裝部署方案。"
    },
    "humanlayer/12-factor-agents": {
        "category_id": "prompts_and_specs",
        "why": "為了解決當前 AI Agent 原型展示眾多但難以穩定運行於真實生產環境、業界缺乏類似雲原生 12-Factor App 那樣權威且具備工程實踐性的 Agent 設計指導方針。",
        "how": "HumanLayer 團隊結合大量生產環境 Agent 構建經驗，系統化提煉出打造高可靠性 LLM 應用程式的 12 項工程設計原則（包含上下文精準管理、工具單一職責、人機協同審核等）。",
        "what": "提供 12-Factor Agents 白皮書規範、架構原則深度剖析指引、實務對比案例與面向生產級 Agent 的開源參考實作。"
    },
    "sigoden/aichat": {
        "category_id": "agent_orchestration",
        "why": "為了解決終端開發者需要在命令列環境快速調用多種大模型、自動生成並執行 Shell 命令、使用本機檔案 RAG 與工具呼叫時，現有工具過於龐大或依賴繁瑣的痛點。",
        "how": "以 Rust 編寫的高效能單一二進位 CLI 工具，相容 OpenAI, Claude, Gemini, Ollama, Groq 等主流後端，內建命令列代碼生成、交互式 Chat-REPL、本地輕量向量 RAG 與 Function Calling 智能體引擎。",
        "what": "提供 `aichat` 跨平台命令列工具、Shell 提示與指令自動執行、多輪對話 REPL、自訂角色與 Prompt 模板管理、輕量 RAG 文件檢索支援。"
    },
    "upstash/context7": {
        "category_id": "mcp_ecosystem",
        "why": "為了解決 Coding Agent 與大語言模型受限於訓練資料時間截止點、對最新釋出的第三方開源軟體庫與框架 API 缺乏認知，容易生成過期或不存在之幻覺代碼的嚴重問題。",
        "how": "Upstash 打造的即時程式碼文件檢索平台，以 Model Context Protocol (MCP) 伺服器形式運行，在 AI 生成代碼時按需檢索官方最新套件文檔，將精準切片即時注入上下文中。",
        "what": "提供 Context7 MCP 伺服器、`ctx7` 軟體庫搜尋工具、與 Cursor / Windsurf / Claude Code 等主流 AI 編輯器的無縫整合、以及涵蓋主流套件的即時文檔索引庫。"
    },
    "mixmark-io/turndown": {
        "category_id": "web_doc_parsing",
        "why": "為了解決網頁數據抓取、富文本編輯器與內容管理系統中，將冗長混亂且包含大量垃圾標籤的 HTML 代碼轉換為純淨、結構化之 Markdown 文本的剛性需求。",
        "how": "JavaScript 編寫的輕量級、跨環境（Node.js / 瀏覽器）HTML 轉 Markdown 引擎，透過解析 DOM 樹並套用靈活的可擴展規則系統（Rules），將 HTML 標籤精準映射為 CommonMark / GFM 語法。",
        "what": "提供 Turndown 核心轉換庫、GFM 表格與核取清單外掛程式、自訂過濾規則 API 與線上即時轉換預覽工具。"
    },
    "doggy8088/doggy8088": {
        "category_id": "education_productivity",
        "why": "彙整微軟 19 屆 MVP、Google 雲端與 AI 領域 GDE Will 保哥的開源貢獻精粹、最新技術演講、技術書籍著作與華語軟體工程社群教學資源。",
        "how": "利用 GitHub Profile 特性，結合動態 SVG 渲染、GitHub Actions 自動化工作流即時同步最新技術文章與影音動態，提供層次分明的個人工程履歷與資源地圖。",
        "what": "提供 Will 保哥的個人技術成就總覽、精選開源工具庫連結、全系列影音與技術課程索引、社群交流管道與繁體中文技術指南入口。"
    },
    "makenotion/notion-mcp-server": {
        "category_id": "mcp_ecosystem",
        "why": "為了解決 AI 智能體（Claude Desktop, Claude Code 等）無法直接讀取、檢索與更新使用者在 Notion 工作區中沉澱的大量文檔、知識庫與資料庫表格的數據孤島困境。",
        "how": "Notion 官方提供的 Model Context Protocol (MCP) 伺服器實作，直接封裝 Notion 官方 API，透過標準 OAuth 授權或本機 Stdio 連線，將 Notion 頁面操作安全暴露給 AI Agent，並針對 Markdown 與 Token 消耗進行了深度優化。",
        "what": "提供 Notion 官方 MCP 伺服器、頁面讀寫與 Markdown 結構化編輯工具、資料庫查詢介面、遠端 OAuth 連線支援與 AI 協同工作流程。"
    },
    "cyberagiinc/DevDocs": {
        "category_id": "mcp_ecosystem",
        "why": "為了解決開發者在使用 AI 輔助編程時，手動查找第三方官方技術文檔繁瑣，且市售文檔抓取服務（如 Firecrawl）收費高昂且有企業內部程式碼與文件外洩隱私疑慮的痛點。",
        "how": "以 TypeScript 與 Python (Playwright, Crawl4AI) 打造完全免費、隱私優先且具備圖形化介面（UI-based）的技術文件 MCP 伺服器，在本機端離線抓取目標文件並向量化快取，透過 MCP 協議為 AI 編輯器提供精準上下文。",
        "what": "提供 DevDocs UI 管理介面、技術文件抓取與索引引擎、MCP Server 整合端點（完美支援 Cursor, Windsurf, Cline, Claude Desktop）、離線快取與錯誤自動重試機制。"
    },
    "doggy8088/github-copilot-configs": {
        "category_id": "prompts_and_specs",
        "why": "為了解決 GitHub Copilot 與 GitHub Copilot Chat 設定選項繁雜分散、預設參數未達最佳效能、開發者往往不知道如何調整編輯器各項進階設定以發揮 AI 最大效能的困擾。",
        "how": "微軟 MVP Will 保哥經大量實測 Copilot 所有選項設定後梳理出最佳實踐，以繁體中文詳解 VS Code 與各類 IDE 中的核心參數（如補全延遲、幽靈文字、Chat 指令模式、自訂 instructions 等）。",
        "what": "提供 GitHub Copilot 最佳化設定檔（`settings.json` 指南）、Prompt 指令範本、快捷鍵推薦、實戰課程導航與繁中配置說明。"
    },
    "docling-project/docling": {
        "category_id": "web_doc_parsing",
        "why": "為了解決各類企業非結構化文件（PDF, Word, PPTX, Excel, HTML 等）排版多樣、包含複雜跨頁表格、公式與多欄佈局，傳統解析工具難以提取高品質內容直接餵給 GenAI / RAG 的瓶頸。",
        "how": "IBM 開發的高效能多模態文件解析框架，採用專屬視覺模型深度理解文檔頁面版面分析（Layout Analysis）與表格結構還原（Table Structure Extraction），精準將各格式轉譯為豐富且純淨的 Markdown / JSON。",
        "what": "提供 Docling CLI 與 Python 函式庫、先進的 PDF 與 Office 文件解析器、端到端表格/圖片結構化提取、原生支援 LlamaIndex, LangChain 等主流 RAG 框架。"
    },
    "andrewyng/aisuite": {
        "category_id": "model_routing_proxy",
        "why": "為了解決開發者在調用不同大語言模型提供商（OpenAI, Anthropic, Google, AWS, Azure, Groq, Mistral, Ollama 等）時，API 規範各異、SDK 介面割裂、切換供應商需重構代碼的標準化痛點。",
        "how": "吳恩達（Andrew Ng）團隊打造的輕量統一 Python 封裝庫，以 OpenAI 語法風格為基準統一不同廠商的調用介面，支援簡單字串切換 provider/model，並實現一鍵式原生 Python 工具呼叫（Tool Calling）。",
        "what": "提供 `aisuite` 統一客戶端 SDK、跨供應商無縫切換介面、單行 Python 函式 Tool Calling 封裝、以及桌面 AI 同事應用 OpenWorker 的基礎底座。"
    },
    "henrythe9th/AI-Crash-Course": {
        "category_id": "education_productivity",
        "why": "為了解決忙碌的軟體創業者與資深工程師在面對爆炸式增長的 AI 研究論文與開源工具時，缺乏高度凝練、由淺入深且能於 2 週內迅速補齊至前沿 AI 研究認知的系統化路徑。",
        "how": "由 Super.com 創始人 Henry Shi 梳理自身從傳統軟體轉型 AI 前沿的精選學習資料，以最短路徑串聯神經網絡、Transformer 架構、LLM 預訓練與後訓練（RLHF/DPO）、推理模型與自主 Agent。",
        "what": "提供 2 週速成課程指引、精選高含金量影音與論文清單、核心概念知識結構導航與創業者視角的機會落點分析。"
    },
    "microsoft/ai-agents-for-beginners": {
        "category_id": "education_productivity",
        "why": "為了解決初學者面對日益複雜的 AI Agent 概念（Planning, Memory, Tools, Multi-Agent）缺乏系統性、理論與實務兼備的權威開源教材問題。",
        "how": "微軟官方團隊精心設計的 18 課端到端實戰課程，基於 Jupyter Notebook、Semantic Kernel 與 AutoGen 等微軟生態，透過圖文並茂的教學設計與豐富代碼範例引導讀者構建自主智能體。",
        "what": "提供 18 課完整教程專案、Jupyter Notebook 實作練習代碼、Agentic RAG / Multi-Agent 範例應用、架構圖解與微軟官方認證學習路徑。"
    },
    "llmware-ai/llmware": {
        "category_id": "context_memory_rag",
        "why": "為了解決企業在構建本地化、隱私安全且高合規的 RAG 知識庫時，依賴雲端超大模型成本高昂且資料存在外洩風險，而開源小模型缺乏針對性微調與整合框架的難題。",
        "how": "專為在本地筆記型電腦、AI PC 與企業自託管環境打造的統一 RAG 框架，整合高吞吐文件解析器（支援 10+ 種格式）、向量資料庫與針對 RAG 專項微調的 SLIM 小型專用模型（Small Specialized Models）。",
        "what": "提供 LLMWare Python 框架、SLIM 模型套件、本地向量索引管線、企業級 RAG 檢索生成 API 與開箱即用的跨平台部署支援。"
    },
    "microsoft/autogen": {
        "category_id": "agent_orchestration",
        "why": "為了解決構建下一代自主多智能體系統時，多 Agent 間的非同步對話協調、動態角色分配、人機協同互動以及複雜工作流編排缺乏標準化程式設計範式的挑戰。",
        "how": "微軟主導的多 Agent 程式設計框架（包含 AutoGen 0.2 與新一代 AutoGen 0.4 事件驅動架構），實作分散式訊息傳遞、非同步事件驅動、狀態持久化、沙箱執行器與可擴展工具整合。",
        "what": "提供 AutoGen 核心運行庫、多 Agent 協同對話模式（群聊、分層、巢狀對話）、AutoGen Studio 視覺化低代碼開發介面、Docker 沙箱與豐富的實務範例。"
    },
    "fsantini/KoboCloud": {
        "category_id": "education_productivity",
        "why": "為了解決 Kobo 電子書閱讀器原廠僅支援少數付費或受限的同步管道、無法直接與用戶常用的個人雲端硬碟（Dropbox, Google Drive, Nextcloud 等）自動無線同步電子書的封閉限制。",
        "how": "基於 Shell 腳本開發並深度整合入 Kobo 作業系統（利用 udev 事件或開機/Wi-Fi 連線觸發），直接在閱讀器本機透過 curl 與雲端服務公開連結或 API 進行增量檔案同步。",
        "what": "提供 `KoboRoot.tgz` 一鍵安裝包、支援 Dropbox / Google Drive / Nextcloud / pCloud / Box 等多雲端硬碟同步腳本、自動下載配置與設定指南。"
    }
}

def update_reviewed_chunk_5():
    reviewed_path = Path("data/reviewed_chunks/reviewed_5.json")
    with open(reviewed_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated_count = 0
    for fn, item in data.items():
        if fn in CURATED_CHUNK_5:
            curated = CURATED_CHUNK_5[fn]
            cat_id = curated["category_id"]
            cat_name = CATEGORIES_META.get(cat_id, {}).get("name", cat_id)

            item["category_id"] = cat_id
            item["category_name"] = cat_name
            item["analysis"]["why"] = curated["why"]
            item["analysis"]["how"] = curated["how"]
            item["analysis"]["what"] = curated["what"]
            updated_count += 1
        else:
            print(f"Warning: {fn} not in curated dictionary!")

    with open(reviewed_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[✓] Successfully refined all {updated_count} / {len(data)} repositories in {reviewed_path}")

if __name__ == "__main__":
    update_reviewed_chunk_5()

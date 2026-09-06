"""
Refine Chunk 1 reviewed data with high-fidelity Traditional Chinese (zh-TW) Why, How, What,
verified category classifications, and comprehensive metadata.
"""

import json
from pathlib import Path
from src.categorizer import CATEGORIES_META

REFINEMENTS = {
    "steipete/CodexBar": {
        "category_id": "model_routing_proxy",
        "why": "重度使用 Claude Code、OpenAI Codex、OpenCode 等 CLI 與 IDE Coding Agents 的開發者，面臨 Token 配額消耗極快且各供應商配額重置週期不同的問題。頻繁登入各家官網查詢費時費力，容易在關鍵任務進行中突然遭遇 Rate Limit 導致工作流中斷。",
        "how": "基於 Swift 打造之原生 macOS 選單列應用（亦具備 Linux CLI 與 AUR 支援），採用本機非同步輪詢與憑證解析機制，直接自官方 Session Cookie、OAuth 權杖或本機設定檔提取各家供應商用量數據，無需重複手動登入。",
        "what": "於 macOS 選單列即時監控超過 60 家主流 AI 提供商（包含 OpenAI Codex、Claude Code、OpenCode、Gemini、DeepSeek 等）的 Token 用量百分比、剩餘配額、重置倒數計時器；支援自定義用量警報臨界值、歷史消耗趨勢統計與深淺色主題切換。",
        "bullets": [
            "支援超過 60 家主流 AI 模型服務商（OpenAI, Claude, OpenCode, Gemini 等）",
            "原生 macOS 選單列常駐顯示，無縫掌控各平台配額與重置倒數",
            "免反覆登入，直接從本機 Session 或 OAuth 權杖安全獲取用量數據",
            "提供 Linux CLI 與 Arch Linux AUR 獨立套件發行版本"
        ]
    },
    "karpathy/llm-council": {
        "category_id": "agent_orchestration",
        "why": "由 Andrej Karpathy 發起的開源專案。面對複雜棘手或具爭議性的問題時，單一大語言模型容易受限於自身訓練偏見或產生推理盲點；需要借鑒人類陪審團或委員會機制，匯聚多個頂級模型共同研討、交叉審核並綜合評判以得出更全面客觀的決策。",
        "how": "後端採用 Python (FastAPI + async httpx)，前端採用 React + Vite。核心為三階段評議架構：第一階段平行向多個 LLM 發起查詢收集各自觀點；第二階段匿名化洗牌所有回答發送給各模型進行同行盲審與打分（避免偏袒）；第三階段由指定的主席模型（Chairman LLM）綜合同行審查矩陣與最佳論點生成最終定案。",
        "what": "提供極簡高雅的本機 Web 界面，整合 OpenRouter 統一 API 網關，可自由配置 GPT-4o、Claude 3.5 Sonnet、Gemini 1.5 Pro、Grok 等組建自定義評議委員會；視覺化展示各模型的獨立觀點、匿名互評打分矩陣與主席綜合決議報告。",
        "bullets": [
            "三階段委員會評議流程：獨立提議、匿名同行互評打分、主席綜合裁決",
            "消除模型偏見，評審階段對各模型回應完全匿名化處理",
            "基於 OpenRouter API，支援自由混搭 OpenAI、Anthropic、Google、xAI 等多廠商旗艦模型",
            "輕量化 FastAPI + React 架構，極易在本機快速部署並擴展自定義提示詞"
        ]
    },
    "Dimillian/CodexSkillManager": {
        "category_id": "claude_code_skills",
        "why": "隨著 OpenAI Codex 與 Claude Code 等 Agent 技能生態的蓬勃發展，開發者本機安裝的自定義 Skills 與擴充腳本大量累積，缺乏現代化圖形介面來直觀預覽、分類檢視、版本比對以及自社群技能中心快速安裝管理。",
        "how": "純 Swift 與 SwiftUI 打造之原生 macOS 桌面應用程式，基於 SwiftPM 輕量架構（無需龐大 Xcode 專案檔），整合 swift-markdown-ui 實現流暢富文本渲染，底層直接對接本機技能目錄 `~/.codex/skills`、`~/.codex/skills/public` 與 `~/.claude/skills`。",
        "what": "支援本地技能清單瀏覽與狀態分類（區分已安裝於 Codex 或 Claude）、SKILL.md 文檔即時 Markdown 渲染與內嵌代碼預覽；支援自資料夾或 ZIP 封裝包一鍵匯入、側邊欄快速移除；內嵌 Clawdhub 線上技能市集瀏覽器，支援搜尋、一鍵下載安裝與安裝狀態版本標籤。",
        "bullets": [
            "原生 macOS SwiftUI 介面，無需 Xcode 專案依賴（純 SwiftPM 構建）",
            "全面覆蓋 `~/.codex/skills` 與 `~/.claude/skills` 本地技能目錄",
            "內建 Markdown 即時渲染引擎與內嵌代碼參照預覽",
            "整合 Clawdhub 線上技能市集，支援一鍵搜尋、版本比對與下載安裝"
        ]
    },
    "searxng/searxng": {
        "category_id": "education_productivity",
        "why": "現代商業搜尋引擎普遍存在使用者畫像追蹤、搜尋氣泡、商業廣告干擾以及隱私外洩風險；同時現代 AI 代理和 RAG 系統急需一個乾淨、無速率限制且不留存個人隱私數據的元搜尋後端。",
        "how": "基於 Python 3 異步架構與 aiohttp 開發的去中心化開源元搜尋引擎（Metasearch Engine），聚合超過 70 個搜尋服務與公共資料庫（Google、Bing、DuckDuckGo、維基百科、GitHub、ArXiv 等），透過隨機 User-Agent、IP 代理池與查詢混淆對使用者隱私進行端到端保護。",
        "what": "提供自託管的現代響應式搜尋 Web 介面與強大的 REST JSON API（可直接作為 LangChain、LlamaIndex、OpenClaw 等 AI Agent 系統的即時聯網檢索工具）；支援多語言、分類篩選（通用、檔案、圖片、代碼、新聞）、自定義搜尋引擎權重與完全無追蹤、無 Cookies 機制。",
        "bullets": [
            "聚合超過 70 種搜尋服務與資料庫，消除單一搜尋引擎偏誤與廣告注入",
            "100% 隱私保護，絕不記錄使用者 IP、Cookies、搜尋歷程與畫像特徵",
            "提供標準 REST JSON API，廣泛作為 AI Agent 與本地 RAG 的即時聯網搜尋後端",
            "支援高度自訂搜尋引擎權重、代理池整合與 Docker 容器化一鍵部署"
        ]
    },
    "Sakshxm1/hermes-agency-orchestrator": {
        "category_id": "agent_orchestration",
        "why": "傳統 Coding Agent 多數採用硬編碼的 DAG 工作流或單一龐大提示詞，面對大型專案時難以在複雜度、執行成本與靈活度間取得平衡；需要一個像指揮家帶領交響樂團般、具備動態階梯式成本控制與多代理協奏的編排架構。",
        "how": "零依賴的宣告式 Agent 編排框架（OrchestralFlow），借鑒 Claude Code 多代理潛能，引入「Conductor Agent（指揮家）」進行元推理與成本仲裁，將工作劃分為分層樂章（Movements）。結合 Hermes Agent 與 Claude Code，透過子代理階梯調度（Opus/Sonnet/Haiku）在不同階段自適應切換模型。",
        "what": "支援從 `/goal` 一鍵引導專案規劃，提供多代理樂章協同架構（Strings 程式架構、Woodwinds 業務邏輯、Brass 測試驗證、Percussion CI/CD 交付）；內建動態成本階梯分析器，視覺化監控各樂章之 Token 支出並自動降級非核心任務以控制預算。",
        "bullets": [
            "交響樂章架構（Movements）：將大型工程拆解為架構、實現、測試與交付多樂章協奏",
            "Conductor Agent 元推理指揮中樞，負責跨樂章任務分發與品質把控",
            "動態成本階梯（Cost Ladders）：依任務複雜度自適應切換旗艦與輕量模型，嚴控預算",
            "零外部依賴宣告式設計，無縫對接 Claude Code 與 Hermes Agent 工作流"
        ]
    },
    "Kulaxyz/self-learning-skills": {
        "category_id": "prompts_and_specs",
        "why": "開發者在與 AI Coding Agent（如 Claude Code、Cursor）協作調試時，常需反覆踩坑才摸索出特定指令、資料庫連線路徑或發布流程，但這些得來不易的經驗（Golden Path）隨會話結束而蒸發，下次會話 Agent 又重蹈覆轍。",
        "how": "一種自我進化的元技能（Meta-Skill）機制，透過監聽與捕獲會話中的成功經驗與關鍵失敗教訓，將其自動萃取成結構化的黃金路徑規則，並自動沉澱更新至專案根目錄的 `AGENTS.md` 或全域常駐指令檔案。",
        "what": "具備「辨識高價值時刻（Recognize）」、「無感捕獲（Capture）」與「自動沉澱（Harvest）」三大迴圈；支援主動口令（如「記住這個操作」）與自動失敗規避記錄（避免重複踩坑）；相容 Claude Code、Cursor、OpenCode 及任何支援 AGENTS.md 的智能體。",
        "bullets": [
            "自我進化元技能（Meta-Skill）：捕獲「工作如何完成」而非僅記錄工作產物",
            "失敗規避記錄：將已知無效死胡同固化為規則，避免跨會話重複踩坑",
            "自動沉澱至 `AGENTS.md`，使後續會話開箱即用歷史積累經驗",
            "全面適配 Claude Code、Cursor、OpenCode 與遵循 AGENTS.md 的各類 Agent"
        ]
    },
    "virgiliojr94/book-to-skill": {
        "category_id": "claude_code_skills",
        "why": "技術書籍、PDF 規範和長篇技術手冊蘊含極高專業知識，但將數百頁的書籍手動轉換為 Coding Agent 在開發時可實時查詢調用的標準技能規格，耗時費力且格式難以統一。",
        "how": "雙階段管線設計：第一階段為確定性 Python 提取器（Extractor），支援 PDF、EPUB、DOCX、Markdown 等多格式文件，自動切分章節、清理雜訊並提取概念元數據；第二階段為規格驅動生成器（Generator），遵循開放 Agent Skills 規範，生成結構化的 `SKILL.md` 與分級檢索索引。",
        "what": "提供 `/book-to-skill [skill-name]` 一鍵生成工作流，具備純分析模式、從分析生成技能模式與增量更新模式；相容 GitHub Copilot CLI、Amp、Claude Code 與 Hermes Agent，將整本技術專著轉化為 Agent 能在編程時即時引用的領域技能。",
        "bullets": [
            "支援 PDF, EPUB, DOCX, MD, HTML, RTF 等多元長篇技術文檔格式解析",
            "確定性提取器搭配規格驅動生成器，確保知識結構嚴謹無幻覺",
            "產出標準開放 Agent Skills（含 SKILL.md、參考索引與實用法則）",
            "無縫適配 Claude Code, Copilot CLI, Amp 與 Hermes Agent 等終端環境"
        ]
    },
    "doggy8088/Agentic-Design-Patterns": {
        "category_id": "agent_orchestration",
        "why": "由 Antonio Gulli 和 Mauro Sauco 所著的《Agentic Design Patterns》是當前構建自主 AI Agent 最權威的系統化專著，但社群缺乏高品質的繁體中文在地化整理與結構化導讀，導致多數工程師仍停留在單純調用 LLM API 的粗淺層面。",
        "how": "由知名技術專家 Will 保哥（doggy8088）維護之繁體中文完整翻譯專案，全書深入剖析 4 大核心板塊共 21 種代理設計模式，涵蓋提示鏈（Prompt Chaining）、路由、規劃、工具調用、長短期記憶、RAG、異常防護與多代理協同架構。",
        "what": "提供長達 424 頁指南的完整繁體中文 Markdown 譯文與代碼範例庫；詳細剖析 MCP（Model Context Protocol）工具整合、人機協同回路（Human-in-the-loop）與真實生產環境的除錯除錯模式，附錄收錄超過 70 頁之進階 Prompt 技巧與主流 Agent 框架對比。",
        "bullets": [
            "424 頁權威專著完整繁體中文版，覆蓋 4 大板塊 21 種核心代理設計模式",
            "包含大量生產級代碼範例，跳脫單純調用 API 邁向強健自主架構",
            "收錄專題章節深入剖析 MCP 協議整合、人機協作護欄與異常恢復",
            "附錄提供 70+ 頁進階提示工程技術與主流 Agent 框架架構矩陣"
        ]
    },
    "YurunChen/repo-docs-skills": {
        "category_id": "claude_code_skills",
        "why": "在 Vibe Coding 與 AI Agent 快速迭代代碼的時代，代碼變更速度遠超人類記憶與傳統文檔維護速度；專案迅速累積技術債，新進開發者或後續 Agent 會話難以掌握真實架構與邊界約束。",
        "how": "以證據導向（Evidence-based）之動態文檔架構，將 Agent 每次執行的實際歷程與代碼變更映射為實時架構圖譜；採用 Claude Code Skill 形式封裝，在代碼變更提交時自動觸發文檔同步規則，確保文檔與源代碼同步演進。",
        "what": "自動生成並維護專案導覽（Walkthroughs）、核心架構概念（Concepts）、模組參考清單（References）與上下文移交總結（Handoff Context）；提供視覺化 Web 靜態展示站點，為 Agent 協同編程建立即時可靠的「代碼證據地圖（Evidence Atlas）」。",
        "bullets": [
            "證據導向動態文檔系統（Evidence Atlas），專為 Agent 輔助編程設計",
            "自動生成專案導覽、架構概念清單、模組參照表與上下文交接記錄",
            "遵循 Claude Code Skill 規範，在代碼變更時自動執行同步更新規則",
            "提供靜態 Web 預覽站點，大幅降低人類工程師與後續 Agent 的代碼理解成本"
        ]
    },
    "lfnovo/open-notebook": {
        "category_id": "education_productivity",
        "why": "Google NotebookLM 展現了基於特定來源資料庫進行深度提問與筆記整理的強大能力，但其閉源架構存在數據隱私外洩風險、模型選擇受限，且無法彈性自定義底層 RAG 管線與音訊播客生成流程。",
        "how": "採用現代全端架構（TypeScript、Next.js、FastAPI/Python 後端），支援 Docker 容器化一鍵自託管；整合先進的 RAG 檢索管道，支援本地嵌入模型、Ollama 本機私有化部署以及各大商用大模型 API（OpenAI、Claude、DeepSeek）。",
        "what": "提供完全開源且注重個人隱私的 NotebookLM 替代方案；支援匯入多種檔案（PDF、TXT、Markdown、網頁 URL、YouTube 字幕）；具備多來源交叉引用對話、筆記摘錄與管理、自動化多角色對話播客生成（AI Podcast Audio Overviews）。",
        "bullets": [
            "完全開源、隱私優先的 Google NotebookLM 替代產品，支援 100% 本地運行",
            "多來源文件支援：PDF、Markdown、網頁、YouTube 字幕與純文字",
            "高品質多角色 AI 對話播客（Podcast Audio Overviews）自動合成生成",
            "彈性架構，相容 Ollama 本地模型與各大商業 LLM API 服務"
        ]
    },
    "elder-plinius/CL4R1T4S": {
        "category_id": "prompts_and_specs",
        "why": "商業 AI 實驗室（OpenAI、Anthropic、Google 等）透過龐大且封閉的 System Prompts 塑造模型人格、引導回答偏好、設置拒絕條款與安全護欄；使用者無法得知輸入背後的底層約束，導致 AI 系統缺乏透明度與可審計性。",
        "how": "由知名白帽研究員 Plinius 發起的 AI 系統指令可觀測性庫，透過逆向工程、越獄探針（Jailbreak Probing）與社群洩漏審計機制，完整提取各大商業前沿模型與 Coding Agent 的真實系統提示詞與工具定義。",
        "what": "收錄 ChatGPT、Claude 3.5/3.7、Gemini 2.0、Grok、Perplexity、Cursor、Windsurf、Devin、Manus、Replit 等主流商業產品的底層 System Prompts、引導規範、隱藏工具描述與安全性邊界策略；推動 AI 透明度研究與提示詞工程分析。",
        "bullets": [
            "業界最全面的商業模型與 AI Agent 系統提示詞（System Prompts）逆向審計庫",
            "覆蓋 ChatGPT, Claude, Gemini, Grok, Cursor, Windsurf, Devin, Manus 等",
            "揭示隱藏的安全護欄、自定義工具呼叫語法與角色人格塑造指令",
            "為提示詞工程師與安全性研究員提供不可或缺的權威對照基準"
        ]
    },
    "shanraisshan/claude-code-best-practice": {
        "category_id": "prompts_and_specs",
        "why": "許多開發者使用 Claude Code 時僅停留在隨意的「Vibe Coding」問答層次，缺乏系統化工程規範、子代理協同原則與結構化提示詞設計，導致在複雜代碼庫中容易迷失方向或產生代碼回歸。",
        "how": "系統化梳理 Anthropic 官方團隊（如 Boris Cherny 等）與社群前沿實踐，將 Claude Code 的能力抽象為「Agents（代理分工）」、「Commands（自定義命令）」與「Skills（可複用技能）」三大維度，並建構宣告式編排工作流（Orchestration Workflow）。",
        "what": "提供完整的 Claude Code 最佳實踐手冊，涵蓋架構拆解、Git Worktree 多分支隔離開發、大型重構指南、測試驅動驗證流程、Token 成本控制策略與開箱即用的 Skills/Commands 配置範本。",
        "bullets": [
            "從隨性 Vibe Coding 邁向嚴謹 Agentic Engineering 的系統化指南",
            "三大架構維度：Agents 職責劃分、Commands 自定義命令、Skills 技能封裝",
            "實戰收錄 Git Worktree 隔離工作流、大型項目重構與測試驅動迴圈",
            "整合 Anthropic 核心工程師第一手經驗與即時社群最佳配置範本"
        ]
    },
    "topoteretes/cognee": {
        "category_id": "context_memory_rag",
        "why": "傳統 RAG 僅基於文本切片的向量相似度檢索，缺乏跨會話的實體關聯、邏輯推理與結構化記憶能力；AI Agent 急需一套具備知識圖譜拓撲結構的本機記憶中樞。",
        "how": "基於 Python 打造的開源 Agent 記憶平台，創新結合知識圖譜（Knowledge Graphs）與向量資料庫（Vector Stores），透過圖神經網路與實體關係抽取算法，將非結構化文本轉換為高度關聯的認知圖譜，支援自託管部署。",
        "what": "為 AI Agent 提供跨會話的持久化認知記憶層；支援全量數據攝取（文檔、代碼、對話歷史）、自動抽取實體關聯、拓撲關聯查詢與圖譜可視化；提供 Python SDK、FastAPI 服務與社群外掛生態，大幅提升多步驟 Agent 決策精度。",
        "bullets": [
            "結合向量資料庫與知識圖譜（Graph RAG），具備拓撲實體推理能力",
            "為 AI Agent 賦予跨越獨立會話的永久認知記憶層",
            "支援非結構化文檔、代碼庫與多輪對話歷史的高效自動攝取與圖譜建構",
            "支援本地私有化部署，提供 Python SDK 與標準 REST API 接口"
        ]
    },
    "hugohe3/ppt-master": {
        "category_id": "visualization_diagrams",
        "why": "現有 AI 生成簡報工具多數僅輸出死板的 HTML 頁面或無法在微軟 Office 中自由編輯的靜態背景圖片；商務與技術展示急需直接生成原生、向量可編輯、動畫流暢的標準 `.pptx` 簡報檔案。",
        "how": "基於 Python 與 `python-pptx` 底層庫開發，結合大語言模型的結構化輸出與版面排版引擎；能精確解析文檔大綱，動態計算文字階層、圖表佈局與形狀座標，並支援載入企業專屬 `.pptx` 母片範本。",
        "what": "輸入任何長篇文檔或概念主題，全自動生成具備原生 Shape 向量圖形、原生數據圖表、轉場與動畫效果的 PowerPoint 投影片；支援講者備忘錄（Speaker Notes）以及語音旁白合成；支援企業自定義模板與多語言輸出。",
        "bullets": [
            "真正原生 PowerPoint（.pptx）輸出，支援 Office / Keynote 完整二度編輯",
            "內建向量圖形、原生數據圖表、表格與頁面過渡動畫效果",
            "支援基於演講者備忘錄自動合成語音旁白音訊",
            "支援導入自定義企業 PPT 範本母片，完美保持品牌識別風格"
        ]
    },
    "tradermonty/claude-trading-skills": {
        "category_id": "claude_code_skills",
        "why": "個人投資者與量化交易者在進行市場覆盤、技術分析、財報篩選與風險管理時面臨資訊龐雜、流程繁瑣的挑戰；需要將嚴謹的交易紀律與分析框架封裝成 AI Agent 可自動執行的標準工作流。",
        "how": "基於 Claude Code Skills 開放規範構建的量化與交易工作流套件，底層整合 Python 數據分析庫（pandas、numpy）與主流金融行情 API（Yahoo Finance、FRED、Polygon 等），將交易流程拆解為規格化的 Skill 模組。",
        "what": "提供一整套開箱即用的交易技能：包含技術指標圖表繪製、經濟數據行事曆追蹤、高勝率型態選股器（Screeners）、交易日誌結構化覆盤、持倉風險敞口計算與回測策略模板；秉持「輔助決策而非盲目委任」的工程理念。",
        "bullets": [
            "專為美股/ETF/波段交易者設計的 Claude Code 結構化工作流套件",
            "涵蓋技術指標分析、經濟日曆、形態選股器與交易日誌覆盤",
            "整合 Python 金融數據生態系，圖表繪製與回測數據客觀清晰",
            "堅持決策輔助與風控紀律導向，杜絕不可控的黑盒交易"
        ]
    },
    "lawve-ai/awesome-legal-skills": {
        "category_id": "claude_code_skills",
        "why": "法律專業工作（如合約審閱、法規遵循審查、判例檢索、專利撰寫）面臨極高的專業門檻與繁重的人工重複勞動；律師與法務團隊急需標準化的 AI Agent 技能來精確自動化法律工作流。",
        "how": "精選收錄超過 250 項符合 Agent Skills 規範的法律專用技能清單，涵蓋跨司法管轄區（如美、英、歐盟等法系）的法規實體識別、爭議條款比對與合規風險量化演算法，支援 Claude Code、Codex 等主流智能體一鍵掛載。",
        "what": "涵蓋 NDA 與商業合約自動審查標註、GDPR/隱私政策合規檢查、專利權利要求書起草、智慧財產權授權分析、法律盡職調查（Due Diligence）工作流與法庭訴狀草擬輔助工具集。",
        "bullets": [
            "收錄逾 250 項專業法律 AI Agent Skills，覆蓋多國法系與實務範疇",
            "商業合約與保密協定（NDA）異常條款自動標註與修改建議",
            "數據隱私（GDPR/CCPA）合規性自動審查與盡職調查管線",
            "標準化 Agent Skills 格式，隨插即用支援 Claude Code 與 Codex"
        ]
    },
    "interviewstreet/hiring-agent": {
        "category_id": "agent_orchestration",
        "why": "傳統技術招聘中履歷初篩耗費大量 HR 與主管時間，且關鍵字過濾容易錯失真正具備開源貢獻與工程實力的候選人，評判標準常缺乏客觀可解釋的依據。",
        "how": "基於 Python 3.11+ 開發的自動化招聘代理管線（Resume-to-Score pipeline）；第一步從 PDF 履歷中抽取結構化實體與工作歷程；第二步聯網調取候選人的 GitHub 開源貢獻、代碼質量信號與真實專案影響力；第三步經由多維度評估模型輸出具備可解釋論據的量化評分卡。",
        "what": "自動化履歷解析與實體提取、GitHub 開源活動交叉比對驗證、客觀公正的評分卡生成（技術深度、專案經驗、代碼活躍度）；提供清晰可追溯的推薦理由，消除主觀偏見並大幅縮減技術初篩週期。",
        "bullets": [
            "端到端 Resume-to-Score 自動化管線，從 PDF 直出客觀評分卡",
            "深度整合 GitHub 活躍信號與開源代碼質量分析，跳脫純文字履歷限制",
            "多維度客觀量化指標，具備完整可解釋的評價論據與依據來源",
            "極致模組化設計，易於整合現有企業 ATS（Applicant Tracking System）系統"
        ]
    },
    "kepano/obsidian-skills": {
        "category_id": "claude_code_skills",
        "why": "由 Obsidian CEO Steph Ango (kepano) 親自構建。Obsidian 擁有龐大的本地 Markdown 筆記生態，但 AI Agent 往往缺乏對 Obsidian CLI、雙向鏈接（Wikilinks）、Canvas 畫布及 Frontmatter 元數據的原生操作能力。",
        "how": "嚴格遵循 Agent Skills 開放規範（agentskills.io），基於 Obsidian CLI 與開放檔案格式（Markdown, Bases, JSON Canvas）打造；可被任何相容 Skills 協議的代理（Claude Code、Codex、OpenCode 等）原生調用。",
        "what": "提供一整套操作 Obsidian 倉庫的強大技能：自動檢索與編輯筆記、管理 Obsidian Canvas 視覺化畫布、動態維護雙向反向鏈接、批次更新 Frontmatter 標籤與屬性；支援 `/plugin install obsidian@obsidian-skills` 或 `npx skills add` 快速安裝。",
        "bullets": [
            "Obsidian 官方 CEO 親自維護之 Agent Skills 標準擴充包",
            "原生支援 Markdown、JSON Canvas 視覺畫布與雙向鏈接知識庫操作",
            "遵循開放 Agent Skills 規範，相容 Claude Code, Codex 與 OpenCode",
            "支援一鍵透過 `/plugin install` 或 `npx skills add` 快速配置"
        ]
    },
    "kenn-io/agentsview": {
        "category_id": "agent_orchestration",
        "why": "開發者同時使用 Claude Code、Codex、Aider 等多種 Coding Agents 時，歷史會話分散於本機各處，缺乏統一檢索日誌、分析對話輪次以及精確統計各 Agent 實際花費與 Token 消耗的工具。",
        "how": "基於 Go 語言打造之單一靜態二進位執行檔（Single Binary），堅持 Local-first 本地優先原則，無需註冊帳號或上傳數據；背景自動解析多達 20 餘種主流 Agent 的本機快取日誌與狀態檔案，內建極速全文檢索索引。",
        "what": "提供優雅現代的本機 Web 儀表板，支援跨 Agent 歷史對話極速全文搜尋、會話重放與代碼差異回顧；即時統計 Token 消耗量、API 費用花費趨勢圖表與高頻調用工具分析；支援 macOS/Linux/Windows 跨平台一鍵安裝。",
        "bullets": [
            "單一 Go 二進位無依賴執行檔，100% 本地運行，無需註冊帳號",
            "支援 Claude Code、Codex、Aider 等超過 20 種主流 Coding Agents",
            "極速全文檢索跨代理歷史對話記錄與代碼 Diff 變更軌跡",
            "精確 Token 用量分析與多維度費用花費趨勢統計儀表板"
        ]
    },
    "patchy631/ai-engineering-hub": {
        "category_id": "education_productivity",
        "why": "生成式 AI 與 Agent 技術演進極快，各類新框架（LangChain, CrewAI, AutoGen, LlamaIndex, MCP）層出不窮，開發者急需一份從基礎理論、前沿架構到工業級落地實踐的高品質開源實戰教材。",
        "how": "結構化收錄數十個完整且可直接運行的 Jupyter Notebooks 與 Python 專案範例，涵蓋大模型微調、多模態 RAG 管線、MCP 伺服器建置、多代理協同架構與評估體系（Evals）。",
        "what": "提供詳盡的端到端教學指南與程式碼倉庫，包含進階 RAG（混合檢索、重排序、圖 RAG）、自主編程 Agent 開發、MCP 協議整合實作、本地開源模型（Ollama/vLLM）量化微調與推理優化教學。",
        "bullets": [
            "全方位 AI 工程實踐樞紐，涵蓋 RAG、微調、多模態與 Agentic 系統",
            "提供數十個可即開即用的 Jupyter Notebooks 與生產級代碼範例",
            "深入覆蓋 MCP 伺服器開發、CrewAI/AutoGen 多代理協作與 Evaluation 體系",
            "持續緊跟 2026 前沿技術演進，GitHub 熱門星標工程指南"
        ]
    },
    "baidu/Unlimited-OCR": {
        "category_id": "web_doc_parsing",
        "why": "傳統 OCR 模型在面對超長文檔、密集排版、複雜表格跨頁與多語言混合時，常因上下文長度受限或幾何形變而發生切分崩潰或文字遺漏；需要具備單次長序列端到端解析能力的統一視覺引擎。",
        "how": "百度開源之端到端長上下文 OCR 解析架構（One-shot Long-horizon Parsing），基於先進視覺-語言多模態大模型，突破傳統切塊檢測再識別的分步模式，支援單次推理解析超高解析度長文檔。",
        "what": "支援書籍、期刊、論文等超長 PDF 的端到端高品質文字提取；高精度識別複雜數學公式（LaTeX）、多級跨欄表格（HTML/Markdown）、手寫筆記與罕見字符；提供預訓練模型權重、推論文檔與批次轉換工具。",
        "bullets": [
            "首創 One-shot Long-horizon Parsing 架構，單次推理完成超長複雜文檔解析",
            "突破傳統 OCR 幾何切片局限，端到端精確提取多欄排版與跨頁文字",
            "完美還原複雜數學 LaTeX 公式、嵌套表格（HTML/Markdown）與特殊符號",
            "開源預訓練權重與推論文檔，支援工業級高吞吐文檔數位化流程"
        ]
    },
    "stablyai/orca": {
        "category_id": "agent_orchestration",
        "why": "單一編程代理在面對大型軟體專案時串行工作效率低下，開發者需要像管理雲端叢集一樣，在桌面端或行動端並行調度大量 Coding Agents 同步解決多個 Issue、測試與重構任務。",
        "how": "專為平行代理設計的專用代理開發環境（Agent Development Environment, ADE），採用 TypeScript / Electron / React 全端架構；透過抽象化 Runtime 介面解耦底層模型，支援自備 API Key（BYO Subscription）在獨立的沙箱環境中並行運行多個 Agent 實例。",
        "what": "支援桌面端、行動端及遠端服務端運行，可同時監控並行運行的十數個 Coding Agent 艦隊；提供視覺化工作區、即時代碼差異預覽、終端交互與會話切換；與現有 Git 工作流及 CI 流程無縫整合。",
        "bullets": [
            "專為平行代理艦隊（Fleet of Agents）打造的現代化 Agent 開發環境（ADE）",
            "支援自備模型訂閱（BYO Subscription），無供應商綁定",
            "覆蓋桌面端、手機行動端與遠端雲端 Runtime 跨平台運行",
            "即時多代理代碼 Diff 比對、終端日誌流與可視化工作區管理"
        ]
    },
    "steipete/birdclaw": {
        "category_id": "mcp_ecosystem",
        "why": "由知名開源開發者 Peter Steinberger (steipete) 發起。Twitter / X 官方 API 費用昂貴且限制嚴格，導致 AI 智能體無法便捷獲取使用者的歷史推文、收藏與社交脈絡作為個人知識庫。",
        "how": "基於 Node.js 與最新 Bun 工具鏈開發的 CLI 與 Model Context Protocol (MCP) 伺服器；利用本機 Twitter 導出的資料存檔或輕量爬蟲機制，將推文數據轉化為結構化、可供 Agent 隨時調用的 JSON 格式與本地記憶體快取。",
        "what": "提供 `birdclaw` 命令列工具與標準 MCP Server 介面；讓 Claude Code、Codex、Hermes 等代理能夠直接檢索、引用使用者的歷史推文、書籤與回覆；提供結構化搜尋、時間軸過濾與本地離線索引功能。",
        "bullets": [
            "為 AI Agent 建立永久可檢索的個人 Twitter / X 歷史記憶庫",
            "同時提供標準 MCP Server 介面與命令列 CLI 工具",
            "基於 Bun 工具鏈開發，執行效能極佳且冷啟動迅速",
            "支援本地存檔導入與自適應抓取，擺脫昂貴官方 API 限制"
        ]
    },
    "nashsu/llm_wiki": {
        "category_id": "context_memory_rag",
        "why": "傳統 RAG 系統每次提問都必須從頭搜尋不相關片段並臨時拼接，缺乏全域概覽與知識沉澱；個人知識庫需要像 Wikipedia 一樣具備結構化章節、交叉引用與持續自我演進的機制。",
        "how": "跨平台桌面應用程式（基於 TypeScript / Tauri / React），採用「增量建構與持續維護」的 Wiki-RAG 新範式：LLM 深入閱讀所有導入的文件，主動抽取知識節點、概念與實體，自動建立相互鏈接的 Markdown Wiki 頁面。",
        "what": "支援導入 PDF、Markdown、網頁等多種格式文檔；自動生成維基首頁、概念索引、實體定義與上下文超鏈接；支援互動式知識探索、自然語言問答；本地資料庫儲存，保障個人敏感資料安全。",
        "bullets": [
            "創新的 Wiki-RAG 範式：大模型主動建構相互鏈接的結構化持久維基知識庫",
            "增量更新維護，導入新文件時自動演進現有維基頁面與交叉引用",
            "跨平台桌面應用（Tauri + React），所有資料均本地儲存保護隱私",
            "支援多格式文檔攝取（PDF, MD, 網頁）與多語言知識問答"
        ]
    },
    "Waishnav/devspace": {
        "category_id": "agent_orchestration",
        "why": "ChatGPT 網頁版等對話介面缺乏本機環境執行命令、讀寫檔案與 Git 協同的能力，開發者渴望在 ChatGPT 等標準介面中獲得如同 OpenAI Codex 的全自動編程體驗。",
        "how": "極簡的 Coding Agent Harness 框架，基於 Model Context Protocol (MCP) 與 npm 套件封裝；在使用者本機運行輕量 MCP 守護進程，將本機終端、檔案系統與 Git 操作暴露為標準 MCP 工具，供 ChatGPT、Claude、Hermes 等客戶端安全調用。",
        "what": "一鍵將本機開發環境接入 ChatGPT / Claude；提供檔案讀取、代碼編輯、終端命令執行、測試運行等核心 Coding 能力；支援嚴格的權限安全沙箱，讓開發者在日常對話介面即可完成複雜軟體工程任務。",
        "bullets": [
            "將 Codex 風格的全自動編程工作流帶入 ChatGPT 與各大標準 Web 介面",
            "基於 MCP 協議，將本機終端、檔案讀寫與 Git 控制轉化為標準 Agent 工具",
            "支援安全沙箱與使用者權限授權確認，保障本機系統安全",
            "透過 npm 一鍵全域安裝（@waishnav/devspace），配置流程極簡"
        ]
    },
    "DeusData/codebase-memory-mcp": {
        "category_id": "code_intelligence",
        "why": "現有代碼庫分析工具或 RAG 方案在大型倉庫中索引緩慢（需數分鐘甚至數小時），且向 LLM 傳遞上下文時浪費大量無效 Token，查詢延遲高。",
        "how": "以純 C 語言打造的高效能代碼智慧 MCP 伺服器，單一靜態二進位檔無任何外部依賴；利用極速語法解析與記憶體內知識圖譜技術，在毫秒級時間內完成整個代碼庫的索引，並支援 10 種語言的混合 LSP（Hybrid LSP）深層語意感知。",
        "what": "支援高達 162 種程式語言的代碼庫索引；提供亞毫秒級（sub-ms）圖譜查詢，可為 AI Agent 節省高達 99% 的上下文 Token；提供符號跳轉、調用鏈追蹤、影響範圍分析等 MCP 工具，大幅提昇 Coding Agent 的程式理解能力。",
        "bullets": [
            "純 C 語言靜態二進位建構，毫秒級極速代碼庫索引，零外部運行時依賴",
            "支援高達 162 種程式語言，涵蓋主流與小眾編程語言生態",
            "獨創 Hybrid LSP 技術，深入理解語意拓撲，節省 99% 上下文 Token",
            "亞毫秒級（sub-ms）查詢延遲，極大提升 Coding Agent 代碼導航效率"
        ]
    },
    "timcsy/knowie": {
        "category_id": "prompts_and_specs",
        "why": "台灣開發者 timcsy 發起的開源專案。AI Coding Agent 雖然能寫出能運行的代碼，但完全不懂專案背後的架構決策脈絡，經常破壞既有約定、引入錯誤套件或重蹈覆轍；專案在累積 30-50 個功能後往往開始失控漂移。",
        "how": "提出一套精簡而深刻的「三檔案思考同步法」（Three Markdown Files Protocol），透過在倉庫中維護結構化的規範、決策與學習歷史檔案，強制引導 Agent 在每輪開發前先讀取思考框架，在開發後沉澱踩坑經驗。",
        "what": "提供完整的繁體中文教學與方法論指南，核心包含專案規範定義（`specs.md`）、技術決策記錄（`decisions.md`）與踩坑教訓（`learnings.md`）；提供實戰影片介紹與範例模板，有效防止 AI 輔助編程中的架構漂移。",
        "bullets": [
            "首創「三檔案同步思考法」：specs.md, decisions.md, learnings.md",
            "解決 AI 編程累積 30-50 功能後的架構失控與原則漂移問題",
            "讓 AI 不僅看懂代碼，更能精確繼承人類工程師的架構意圖與決策脈絡",
            "提供繁體中文教學文檔、起源故事與完整實戰示範影片"
        ]
    },
    "DietrichGebert/ponytail": {
        "category_id": "claude_code_skills",
        "why": "AI 程式生成工具往往過度熱情，傾向寫出冗長、過度工程化且容易出錯的樣板代碼；軟體開發中「最好的代碼是從未寫出的代碼」，需要引導 Agent 擁有資深工程師的極簡主義思維。",
        "how": "一款專為 AI Coding Agent 設計的高級工程師思維提示詞與技能外掛（Skill），以詼諧的「Ponytail（扎馬尾的慵懶資深工程師）」為人格設定，將簡約至上、防禦性編程、刪除多餘代碼與優先複用成熟庫的原則植入 Agent 推理鏈中。",
        "what": "提供開箱即用的 Agent Skill；強制 Agent 在寫新代碼前先質疑需求、優先使用現有標準庫、嚴格限制代碼行數與抽象層次；有效大幅精簡生成代碼量，減少維護成本與潛在漏洞。",
        "bullets": [
            "「扎馬尾的資深工程師」心智模型：極簡、精準、一行代碼搞定",
            "強制 Agent 優先複用現有模組，杜絕不必要的過度設計與冗長代碼",
            "強調刪除代碼與防禦性工程，以最小變更達成業務目標",
            "開箱即用的 Agent Skill，相容 Claude Code, Codex 等終端智能體"
        ]
    },
    "openai/plugins": {
        "category_id": "claude_code_skills",
        "why": "隨著 OpenAI Codex 與外掛生態的演進，官方需要一套標準化的範例庫與市場清單（Marketplace Manifests），指導開發者如何規範化構建結合 Skills、MCP、自定義命令與代理的多功能外掛。",
        "how": "官方 Codex 外掛規範示範倉庫，每個外掛封裝於獨立目錄，包含 `.codex-plugin/plugin.json` 清單配置、伴隨的 `skills/` 目錄、`.mcp.json` 伺服器連接配置、`hooks.json` 生命週期攔截器與自定義代理設定。",
        "what": "提供豐富的官方級別外掛範本，包括 Figma（代碼轉畫布與設計系統）、Notion（知識庫同步與規劃）、iOS App 構建工作流等；同時包含標準市場（Marketplace）清單結構，是構建現代 Codex 外掛的標準參考樣板。",
        "bullets": [
            "OpenAI 官方 Codex 插件生態標準範例與清單規範倉庫",
            "完整包含 .codex-plugin/plugin.json 清單、skills 目錄與 hooks 鉤子",
            "提供 Figma、Notion、iOS 等多個工業級示範插件",
            "規範化打包命令、MCP 伺服器與專屬代理設定，推動外掛標準化"
        ]
    },
    "Panniantong/Agent-Reach": {
        "category_id": "agent_orchestration",
        "why": "AI Agent 在終端機環境中受限於封閉的本地上下文，無法即時檢索與閱讀主流社群平台（Twitter/X、Reddit、YouTube、Bilibili、小紅書等）上的最新動態，而各平台 API 申請繁瑣、成本高昂或存在嚴格反爬限制。",
        "how": "基於 Python 打造的開源跨平台聯網 CLI 工具與 Agent 擴充包，整合多種經過抗反爬強化的開源解析器與輕量抓取協議，無需配置昂貴的官方 API 密鑰，自動選擇最穩定通道提取網頁內文與多媒體元數據。",
        "what": "為 AI Agent 一鍵賦予全網視覺與資料檢索能力；支援一鍵讀取與搜尋 Twitter 推文、Reddit 討論串、YouTube 字幕、GitHub 倉庫、B站影片內容與小紅書貼文；提供標準化命令列介面與結構化 JSON 輸出，零 API 費用開箱即用。",
        "bullets": [
            "一鍵為 AI 智能體裝上全網視野，覆蓋國內外主流社交與內容平台",
            "支援 Twitter, Reddit, YouTube, GitHub, Bilibili, 小紅書等六大平台",
            "零 API 費用，底層自動自適應維護最穩定的數據接入與抗反爬機制",
            "提供乾淨簡練的 CLI 命令列工具與結構化 JSON 輸出格式"
        ]
    },
    "ucb-bar/ucie": {
        "category_id": "education_productivity",
        "why": "Universal Chiplet Interconnect Express (UCIe) 是半導體產業新一代的小晶片（Chiplet）互連開放工業標準，但業界長期缺乏透明、開源且相容於學術與硬體研究的 RTL 實作。",
        "how": "由加州大學柏克萊分校 BAR 實驗室（UC Berkeley Architecture Research）打造，採用 Chisel / Scala 硬體構建語言，嚴格實現 UCIe 3.0 規範。包含類比 PHY 介面、UCIe 數位堆疊（協議層、晶片到晶片適配器、邏輯 PHY）以及可經由 TileLink 匯流排存取的暫存器區塊。",
        "what": "開源的 UCIe 3.0 控制器 IP 核；提供完整的 Chisel 原始碼、RTL 生成工具鏈（透過 Mill 構建）與單元測試套件；支援單一或多模組實例化參數配置，推動開源硬體與先進小晶片封裝架構研究。",
        "bullets": [
            "UC Berkeley 官方開源之 UCIe 3.0 規範晶片互連 IP 實作",
            "基於 Chisel / Scala 硬體構建語言，包含完整數位堆疊與 TileLink 介面",
            "提供端到端 RTL 生成工具鏈與完備的單元驗證測試套件",
            "推動半導體先進 Chiplet 異質整合封裝技術的開源研究與產業普及"
        ]
    },
    "Gerkinfeltser/hermes-discord-status-line": {
        "category_id": "agent_orchestration",
        "why": "使用 Hermes Agent 在 Discord 頻道協同辦公時，使用者無法直觀得知每輪推理所花費的 API 時間、Token 消耗量、模型名稱與上下文視窗佔用比例，缺乏即時效能回饋。",
        "how": "基於 Python 開發的 Hermes Agent 官方插件，借鑒 Claude Code 的 Statusline 設計理念；在 Hermes 完成每輪對話生成後，自動透過 Discord Webhook 或 Bot API 追加一條自定義格式的斜體狀態訊息。",
        "what": "即時顯示每則回覆的推理延遲（如 4.5s）、上下文視窗佔用率（如 7%）、Token 使用計數（如 71K/1M）與調用模型名稱（如 deepseek-v4-flash）；支援自定義 Discord Markdown 樣式模板。",
        "bullets": [
            "為 Discord 上的 Hermes Agent 帶來 Claude Code 風格的即時狀態列",
            "精準展示推理延遲、上下文視窗佔用百分比、Token 計數與調用模型",
            "支援自定義 Discord 格式模板（如斜體或 subtext 子文字樣式）",
            "安裝極簡，直接符號連結至 `~/.hermes/plugins/` 即可生效"
        ]
    },
    "mnemosyne-oss/mnemosyne": {
        "category_id": "context_memory_rag",
        "why": "許多雲端 Agent 記憶體解決方案依賴遠端 SaaS 服務或笨重的分散式向量資料庫，存在數據隱私外洩風險、網路延遲高且難以在本地單機或邊緣設備上輕量化部署。",
        "how": "零雲端依賴（Zero-cloud）的開源 AI 記憶體庫，純 Python 實作僅有一個純 Python 依賴，底層採用本地標準 SQLite 資料庫進行持久化儲存；結合語意關聯與記憶衰減演算法，實現高效率本機記憶檢索。",
        "what": "為 AI 智能體提供持久化、可跨會話漫遊的長期記憶中樞；支援對話記憶寫入、語意聯想檢索、重要性權重衰減與記憶遺忘機制；體積極致精簡，開箱即用，全面保障資料隱私。",
        "bullets": [
            "100% 零雲端依賴（Zero-cloud），所有記憶資料持久化儲存於本地 SQLite",
            "純 Python 實作，僅有單一純 Python 依賴，啟動毫秒級無額外負擔",
            "具備語意關聯檢索、記憶衰減權重與動態遺忘機制",
            "提供標準輕量 API，輕鬆嵌入各類自主 Agent 與助理對話迴圈"
        ]
    },
    "bradAGI/awesome-cli-coding-agents": {
        "category_id": "agent_orchestration",
        "why": "終端機原生（Terminal-native）的 AI 編程代理正在迎來大爆發，但生態呈現高度碎片化，開發者難以全面了解各種開源 CLI Agent、商業代理平台、平行調度框架與自主迴圈支架的優劣定位。",
        "how": "精選且持續維護之 Awesome 領域知識庫，依據架構屬性將終端編程代理分類為：開源工具（Pi, OpenCode, Aider, Goose）、官方平台代理（Claude Code, Codex, Gemini CLI）、平行執行器與自主 Harness 基礎設施。",
        "what": "提供全網最完整的 CLI Coding Agent 與 Harness 清單；包含各專案的星標活躍度、技術選型、執行模式、終端交互特性對比以及社群最佳實踐指南，為開發者選型提供權威導航。",
        "bullets": [
            "全網最詳盡的終端機原生（CLI）AI 編程代理與 Harness 精選清單",
            "分類收錄開源工具（Pi, OpenCode, Aider）、官方平台與平行調度器",
            "深度對比各代理的架構設計、執行沙箱、自主迴圈與 Git 協同能力",
            "為開發者與工程團隊選型終端編程助手提供最權威的參考指標"
        ]
    },
    "googlecolab/google-colab-cli": {
        "category_id": "education_productivity",
        "why": "Google Colab 提供強大的免費與付費雲端 GPU/TPU 運算資源，但長期以來主要透過網頁瀏覽器 Notebook 介面互動，無法與開發者本地終端、CLI 工作流及 AI Agent 自動化管線深度融合。",
        "how": "Google Colab 官方推出的命令列客戶端（Python 開發），底層透過 Google Cloud 授權認證與 Colab 內部 API 通訊，實現雲端硬體實例的遠端無頭（Headless）調度與生命週期管理。",
        "what": "支援從終端一鍵配置高效能 CPU、GPU 及 TPU 執行環境；直接自本機終端執行腳本、管理遠端檔案傳輸、監控執行狀態與自動化執行機器學習工作流；支援無縫接入 AI Agent 實現自動化雲端運算。",
        "bullets": [
            "Google Colab 官方命令列介面，直接從終端調度雲端 GPU/TPU 運算資源",
            "支援無頭（Headless）腳本執行、自動化機器學習訓練管線構建",
            "本機與雲端環境無縫檔案雙向同步傳輸與資源生命週期監控",
            "極佳支援 AI Agent 與 CI/CD 流程自動化調用雲端加速硬體"
        ]
    },
    "charmbracelet/glow": {
        "category_id": "education_productivity",
        "why": "開發者在終端中查看 Markdown 格式的 README 或技術文檔時，傳統 `cat` 或 `less` 工具無法解析語法，閱讀體驗雜亂無章且缺乏視覺階層與色彩高亮。",
        "how": "由知名終端工具團隊 Charm 採用 Go 語言打造，基於 Glamour 樣式渲染引擎與 Lip Gloss 終端樣式庫，在 CLI 環境中原生支援 ANSI 256 色與 Truecolor 樣式渲染，支援分頁閱讀（Pager）與本地目錄掃描。",
        "what": "提供終端機內極致美觀的 Markdown 渲染閱讀器；支援即時富文本語法高亮、表格排版、代碼塊著色；可直接讀取本地檔案、GitHub/GitLab 倉庫文檔或標準輸入管道（Pipe）；支援滑鼠滾動與自定義主題樣式。",
        "bullets": [
            "終端機內極致優雅的 Markdown 渲染閱讀器，支援 Truecolor 與 ANSI 256 色",
            "自動解析並美化排版 Markdown 標題、清單、表格與代碼塊",
            "可直接讀取本地檔案、Standard Input 管道或 GitHub/GitLab 遠端倉庫文檔",
            "內建分頁器（Pager）支援鍵盤導航、滑鼠滾動與豐富自定義樣式主題"
        ]
    },
    "doggy8088/mcp-cli": {
        "category_id": "mcp_ecosystem",
        "why": "台灣微軟 MVP Will 保哥（doggy8088）作品。開發者或 AI 代理在調試與調用 Model Context Protocol (MCP) 伺服器時，缺乏一個輕量、啟動極速且便於在 Shell 腳本中透過管道（Pipe）串接的專用 CLI 工具。",
        "how": "純 Rust 語言開發的獨立二進位工具與函式庫，無外部 Runtime 依賴；同時支援標準輸入輸出（stdio）與 HTTP (SSE) MCP 伺服器協議；內建連線池（Connection Pool）與 lazy-spawn 守護程序以保留暖連線（預設 60 秒逾時）。",
        "what": "提供簡練的命令列指令（如 `mcp-cli call`）直接調用 MCP 工具並輸出乾淨 JSON，完美配合 `jq` 與 Shell 腳本；支援工具過濾白名單/黑名單、伺服器指令顯示與包含修復建議的結構化錯誤代碼。",
        "bullets": [
            "純 Rust 高效實作，單一二進位執行檔，啟動極速且記憶體佔用極低",
            "全面相容 stdio 與 HTTP/SSE 兩種 MCP 伺服器傳輸協議",
            "輸出結構化 JSON，極度適合搭配 `jq`、Shell Pipeline 與自動化腳本",
            "內建暖連線快取池（Connection Pool）與白名單工具過濾機制"
        ]
    },
    "mvanhorn/last30days-skill": {
        "category_id": "claude_code_skills",
        "why": "LLM 的訓練數據存在時間截止點，即使聯網搜尋也常被過時的 SEO 垃圾文章干擾，難以精確掌握過去 30 天內在真實社群（Reddit, X, YouTube, HN 等）中發生的最新技術進展與真實從業者討論。",
        "how": "基於 Python 開發之 Agent Skill，設計「搜尋真實人類而非網站編輯」的抓取邏輯；並行調用 Reddit、X (Twitter)、Hacker News、YouTube 與 Polymarket 等多元平台檢索源，透過時間戳過濾與交叉去噪演算法提煉高信噪比內容。",
        "what": "提供 `/last30days` 技能指令；輸入任何技術主題或熱門事件，自動檢索過去 30 天內社群最熱門的真實回饋與爭論焦點，並輸出結構化、附帶原始引用連結的深度總結報告；支援多語言輸出。",
        "bullets": [
            "專注於「搜尋真實從業人員反饋而非搜尋引擎優化垃圾內容」",
            "聚合 Reddit, X (Twitter), Hacker News, YouTube, Polymarket 等多元信號源",
            "嚴格限定過去 30 天時間戳，實時捕獲最前沿技術與爭鳴焦點",
            "標準 Claude Code / Codex Skill 封裝，一鍵生成附帶真實引用的調研報告"
        ]
    },
    "1weiho/open-slide": {
        "category_id": "visualization_diagrams",
        "why": "傳統簡報製作耗費大量時間調整版面排版，而市面上的 AI 簡報生成器多為閉源 SaaS，無法讓 AI Agent 直接在終端機中透過自然語言和結構化代碼靈活操縱投影片內容與動畫。",
        "how": "專為 AI Agent 設計的開源現代投影片框架，基於 TypeScript、Next.js 與 Tailwind CSS；提供結構化的簡報語法與組件系統，使 Coding Agent 能精確輸出符合版面幾何約束的投影片代碼並進行熱重載預覽。",
        "what": "提供豐富的科技感投影片範本、現代字體排版、靈活的網格系統與程式碼高亮組件；支援一鍵導出 PDF 或線上全螢幕演講播放；Agent 可直接根據大綱自動生成並微調每張 Slide 的細節佈局。",
        "bullets": [
            "專為 AI 智能體設計的開源投影片簡報框架（TypeScript + Tailwind）",
            "提供現代化排版、代碼高亮、數據可視化組件與流暢動畫支援",
            "Agent 可直接透過自然語言生成或熱重載修改投影片結構代碼",
            "支援線上全螢幕演講者視角播放與高解析度 PDF 一鍵導出"
        ]
    },
    "openai/skills": {
        "category_id": "claude_code_skills",
        "why": "OpenAI 官方為了推廣 Codex 智慧體的可重用能力，建立了一套讓團隊與個人能夠以「一次編寫、處處運行」方式打包各類工程操作的標準技能目錄（Skills Catalog）。",
        "how": "採用標準化目錄架構封裝指令說明、執行腳本（Shell/Python）與輔助資源；定義了清晰的元數據規範與執行邊界，使 Codex 等 Agent 能夠在任務執行過程中自動發現並動態調用特定技能。",
        "what": "官方歷史性技能示範庫，包含環境配置、代碼審查、自動化測試、安全檢查等標準化技能包；展示了如何將重複性的軟體工程最佳實踐固化為 Agent 可自動執行的標準資產（後續整合進 OpenAI Plugins 生態）。",
        "bullets": [
            "OpenAI 官方首個 Agent Skills 目錄規範示範倉庫",
            "「一次撰寫，處處運行」設計哲學，封裝標準化工程指令與可執行腳本",
            "涵蓋自動化環境設定、代碼審計、單元測試等多種工程實踐場景",
            "為後續 Codex Plugins 與現代開放 Agent Skills 標準奠定基礎"
        ]
    },
    "openai/whisper": {
        "category_id": "web_doc_parsing",
        "why": "傳統語音辨識系統對口音、背景噪聲、專業術語及多語言混雜的魯棒性極差，且需要繁複的特徵工程與聲學模型 pipeline，無法滿足多模態數據採集與真實環境音訊轉錄的苛刻要求。",
        "how": "基於端到端 Transformer 序列到序列（Seq2Seq）架構，採用弱監督學習（Weak Supervision）在長達 68 萬小時的大規模、多語言多任務音訊資料集上進行聯合預訓練；將梅爾頻譜圖直接映射為文字序列。",
        "what": "提供目前開源領域最強大的多語言語音辨識（ASR）與即時翻譯開源模型；支援多達 99 種語言的自動語言識別、精準時間戳對齊、語音轉文字與語音翻譯；廣泛應用於影音字幕生成、播客分析與多模態 RAG 前置資料處理。",
        "bullets": [
            "68 萬小時海量多語言弱監督資料聯合預訓練，抗噪聲與抗口音能力極佳",
            "端到端 Transformer Seq2Seq 架構，涵蓋自動語音識別（ASR）與即時翻譯",
            "支援 99 種語言識別、單詞/句子級精準時間戳對齊",
            "開源多尺寸模型權重（tiny 到 large），成為語音轉錄與多模態處理的工業標竿"
        ]
    },
    "DannyMac180/skills": {
        "category_id": "claude_code_skills",
        "why": "很多開發者在指揮 AI Agent 執行複雜長鏈條任務時，缺乏監督式的動態工作流控制，也缺乏能根據學習者個人認知習慣深入淺出解釋複雜技術文檔的自適應工具。",
        "how": "開發者 Dan McAteer 開發的開源 Agent Skills 套件，包含 `codex-dynamic-workflows` 與 `explain-this` 兩大核心技能；採用結構化目標模式（Goal Mode）、審批門控（Approval Gates）與持久化學習者檔案機制。",
        "what": "`codex-dynamic-workflows` 支援動態規劃與執行受監督的 AI 代理工作流，劃分工作包並生成可驗證產物；`explain-this` 則能根據初次訪談建立的個人檔案，深度解析任何技術論文或複雜代碼，並生成理解測驗與間隔重複複習卡片。",
        "bullets": [
            "提供動態受監督工作流（codex-dynamic-workflows）與自適應學習（explain-this）",
            "引入目標模式、子代理工作包分配與關鍵節點人工審批門控機制",
            "建立個人學習者持久畫像（~/.explain-this/），提供量身定制的技術解析",
            "結合間隔重複複習與概念測驗，顯著增強開發者對新代碼庫的掌握度"
        ]
    },
    "microsoft/intelligent-terminal": {
        "category_id": "agent_orchestration",
        "why": "微軟官方探索終端創新的重要專案。傳統終端機僅是純粹的字符輸入輸出介面，工程師在使用命令列時常遇到語法遺忘、錯誤訊息晦澀難懂以及重複切換外部 AI 工具的問題。",
        "how": "基於微軟 Windows Terminal 開源核心深度分支開發（C++ 打造），原生集成 Agent Client Protocol (ACP) 通訊協定，將大語言模型能力直接無縫注入控制台虛擬終端與緩衝區渲染管線中。",
        "what": "提供原生集成於終端標題列與狀態列的智慧代理面板；具備命令列自動補全、語意化錯誤診斷、多步驟 Shell 腳本自動生成、終端歷史會話語意搜尋與可視化執行授權護欄。",
        "bullets": [
            "微軟 Windows Terminal 官方深度分支，終端底層原生整合 AI Agent",
            "原生實作 Agent Client Protocol (ACP) 通訊協定，低延遲流暢交互",
            "具備終端命令智能補全、執行報錯即時診斷與一鍵修復建議",
            "提供嚴格的操作確認安全護欄，防止危險命令誤執行"
        ]
    },
    "Trinkle23897/learning-beyond-gradients": {
        "category_id": "education_productivity",
        "why": "現代深度學習高度依賴反向傳播與梯度下降，但在許多離散決策、符號推理、元提示詞優化以及智能體策略演進的場景下，梯度無法直接傳遞，啟發式非梯度學習（Heuristic Learning）成為重要研究方向。",
        "how": "清華大學研究員 Trinkle23897 發布的高品質開源學術研究與雙語博客文案倉庫，深入探討遺傳演算法、強化學習、啟發式搜索與大語言模型提示詞自我演進的理論邊界與算法實現。",
        "what": "包含完整的論文復現腳本、Python 雙語渲染器（`render_learning_beyond_gradient.py`）與高品質交互式 HTML 成果；詳細梳理了超越梯度更新的 Agent 自我優化方法，為提示詞優化器（如 DSPy、SkillOpt）提供深刻理論借鑒。",
        "bullets": [
            "非梯度啟發式學習（Heuristic Learning）理論與實踐深度剖析",
            "探討遺傳演算法、進化策略與離散符號優化在 AI 智能體中的應用",
            "提供中英雙語對照之高質量渲染文檔與互動式學術成果頁面",
            "為無梯度反向傳播的 Agentic 自我演化算法提供堅實理論依據"
        ]
    },
    "headroomlabs-ai/headroom": {
        "category_id": "context_memory_rag",
        "why": "AI Coding Agent 在執行命令時常產生數萬行龐大的終端日誌、JSON 回應或資料庫輸出，直接餵給 LLM 會瞬間撐爆上下文視窗、耗費昂貴 Token，甚至引發「迷失在中間（Lost in the Middle）」導致關鍵錯誤被忽略。",
        "how": "採用精密的語法感知壓縮管線，提供 Python 內嵌函式庫、本地反向代理（Proxy）與標準 MCP 伺服器三種接入模式；利用結構化語法樹剪枝與關鍵行過濾算法，在不丟失核心語意與 FATAL/ERROR 錯誤行的前提下極限壓縮。",
        "what": "針對 Coding Agent 的終端輸出可減少約 20% Token，針對 JSON/API 輸出可大幅減少 60% 至 95% Token，且保持模型回答準確性完全不變；支援無縫接入 Claude Code、LangChain 與自建 Agent 流程。",
        "bullets": [
            "智慧上下文壓縮層，針對 JSON 數據最高減少 60-95% Token 消耗",
            "針對編程代理日誌節省約 20% Token，同時確保 ERROR/FATAL 行 100% 完整保留",
            "三種靈活接入方式：Python 內嵌函式庫、透明反向代理與標準 MCP 伺服器",
            "消除上下文冗餘，解決 LLM 注意力稀釋與「迷失在中間」盲區"
        ]
    },
    "DayuanJiang/next-ai-draw-io": {
        "category_id": "visualization_diagrams",
        "why": "Draw.io 是一款強大的圖表繪製工具，但手動繪製複雜架構圖、流程圖耗時費力；而傳統純文字生圖（如 Mermaid）風格過於單一，缺乏豐富的樣式控制與專業元件庫。",
        "how": "基於 Next.js 全端架構開發，內嵌開源 Draw.io 繪圖畫布引擎，深度整合大型語言模型自然語言推理能力，並內建支援 Claude Code CLI 的標準 MCP Server 伺服器介面。",
        "what": "支援透過自然語言提示詞直接生成、修改與擴展專業 Draw.io 架構圖與流程圖；支援在畫布上進行拖曳二次微調；提供 MCP Server 供 AI Agent 直接調用生成可視化圖表資產。",
        "bullets": [
            "Next.js 深度整合 Draw.io 繪圖引擎與大語言模型自然語言生成能力",
            "支援自然語言直出可編輯向量架構圖，支援在畫布上拖曳微調",
            "內建 MCP Server，使 Claude Code 等終端 Agent 具備直接繪製圖表之能力",
            "支援多種技術架構圖、UML、流程圖與時序圖範本庫"
        ]
    },
    "farion1231/cc-switch": {
        "category_id": "model_routing_proxy",
        "why": "開發者同時使用 Claude Code、Codex、OpenCode、OpenClaw、Hermes Agent 等多種終端代理時，需要在不同的 API Key、第三方代理服務商、自定義端點與 MCP 配置間頻繁手動編輯設定檔，極易出錯。",
        "how": "基於 Rust 與 Tauri 跨平台框架打造之極致輕量、美觀的桌面全能管理工具（ccswitch.io），記憶體佔用極低；直接讀寫管理各大 Coding Agent 位於本地的設定檔、環境變數與安全金鑰，完美支援 Windows WSL2 與 macOS/Linux。",
        "what": "一鍵在多家模型服務商（Anthropic 官方、OpenAI、DeepSeek、第三方轉發網關）與模型版本間無縫切換；集中管理與熱加載 MCP 伺服器清單；提供優雅視覺化介面、配置備份還原與診斷工具。",
        "bullets": [
            "基於 Rust + Tauri 打造之跨平台極致輕量桌面管理器（ccswitch.io）",
            "支援一鍵切換 Claude Code, Codex, OpenCode, Hermes 等多個 Agent 供應商配置",
            "集中管理 MCP 伺服器列表，支援熱加載與一鍵啟用/禁用",
            "完美支援 Windows WSL2 與 macOS 原生環境，配置自動備份與防呆校驗"
        ]
    },
    "can1357/oh-my-pi": {
        "category_id": "agent_orchestration",
        "why": "許多終端編程代理缺乏與本地編輯器（如 VS Code/Cursor）的深度雙向通訊機制，開發者在終端機中無法即時感知 IDE 的游標位置、選取區域與開啟檔案狀態。",
        "how": "基於 Bun 與 TypeScript 開發之高響應性 AI 編程代理 Harness，透過 IPC 管道與 IDE 建立原生雙向通訊通道；全面支援 Anthropic Claude、OpenAI 等多種大模型後端，並支援 Nix Home Manager 與 Zsh 自動補全。",
        "what": "提供極速、深度整合 IDE 的終端 Coding Agent；支援自動讀取當前 IDE 焦點代碼、即時代碼差異比對、多輪交互式編輯；提供靈活的 MCP 工具擴充介面與完整的 Shell 自動補全腳本。",
        "bullets": [
            "Bun + TypeScript 打造的高性能終端 Coding Agent，啟動極速無延遲",
            "深度雙向連接 IDE（VS Code / Cursor），即時感知游標與選區上下文",
            "多模型後端支援（Claude, OpenAI 等），靈活配置不同推理引擎",
            "原生整合 Nix Home Manager 模組與 Zsh 自動補全，極致終端體驗"
        ]
    },
    "supermemoryai/supermemory": {
        "category_id": "context_memory_rag",
        "why": "開發者日常瀏覽的書籤、筆記、推文與技術文檔極度分散，傳統筆記工具搜尋效率低；更關鍵的是，各類 AI 助理無法感知使用者的這些歷史知識，每次對話都像陌生人。",
        "how": "基於 Cloudflare Workers / Pages 邊緣計算、Postgres (Drizzle ORM) 與向量嵌入構建的高擴展性記憶引擎，支援完全本地離線運行；提供標準 REST API 與 MCP 伺服器，將使用者的數位軌跡轉化為語意化個人知識索引。",
        "what": "打造「AI 時代的第二大腦」；提供瀏覽器擴充套件一鍵儲存網頁與推文；提供極速語意搜尋與對話式問答；提供標準 MCP 伺服器，讓 Claude Code 等 Agent 能夠直接讀取使用者的長期個人記憶庫。",
        "bullets": [
            "AI 時代的專屬外接大腦（Memory API for the AI Era），支援 100% 本機私有化運行",
            "整合瀏覽器外掛一鍵保存網頁、推文、對話與文檔，自動生成語意索引",
            "提供標準 MCP 伺服器與 REST API，使任何 Coding Agent 具備個人長期記憶",
            "基於 Cloudflare 邊緣架構與向量檢索，極速低延遲且支援海量知識庫"
        ]
    },
    "EveryInc/compound-engineering-plugin": {
        "category_id": "claude_code_skills",
        "why": "傳統軟體工程中每次完成任務往往消耗精力，後續任務依然從零開始；Compound Engineering（複利工程）理念強調透過規格化沉澱，讓工程團隊的每一次任務產出都能成為後續工作的加速槓桿。",
        "how": "官方 Compound Engineering 插件，支援 Claude Code、Codex、Cursor 等主流工具；將經過實戰檢驗的架構原則、代碼審查檢查清單、單元測試約定與重構工作流封裝為可執行的 Agent Skills 規範。",
        "what": "提供一整套引導 AI Agent 遵循高標準工程實踐的技能庫；包含架構一致性檢查、自動化變更日誌提煉、技術債預防指南與持續交付輔助腳本，使團隊代碼庫具備隨時間自我增強的複利效應。",
        "bullets": [
            "貫徹 Compound Engineering（複利工程）哲學：讓每個任務成為下個任務的加速跳板",
            "支援 Claude Code, Codex, Cursor, Grok Bot 等主流開發環境",
            "內建架構約定檢查、重構防護線與代碼質量驗證技能集",
            "減少工程重複勞動，使專案隨時間推移累積正向技術複利"
        ]
    },
    "D4Vinci/Scrapling": {
        "category_id": "web_doc_parsing",
        "why": "傳統網頁爬蟲（如 BeautifulSoup, Scrapy）在面對現代反爬機制（Cloudflare Turnstile, DataDome, 複雜 JS 動態渲染）時極易被封鎖，而無頭瀏覽器往往資源消耗龐大且啟動緩慢。",
        "how": "Python 打造之新一代自適應網頁抓取框架，兼具極速 HTTP 請求與 Playwright 智慧偽裝隱身能力；採用自適應選擇器（Adaptive Selectors）演算法，在網頁 DOM 結構改版時能自動智慧修正定位路徑，具備極高強健性。",
        "what": "提供從單次隱蔽請求到全站大規模爬取的完整解決方案；原生繞過頂級機器人驗證機制；提供內建的 MCP Server 介面，讓 AI Agent 能夠直接調用抓取動態網頁並精確提取結構化數據。",
        "bullets": [
            "自適應選擇器（Adaptive Selectors）：網頁 DOM 結構改動自動自我修復路徑",
            "頂級防封鎖能力，原生繞過 Cloudflare、DataDome 等嚴格機器人驗證",
            "融合極速輕量 HTTP 請求與 Playwright 無頭瀏覽器雙模執行",
            "提供官方 MCP Server 介面，方便 AI Coding Agent 一鍵調用進行動態抓取"
        ]
    },
    "NVIDIA/SkillSpector": {
        "category_id": "claude_code_skills",
        "why": "隨著 Claude Code、Codex 與 MCP 技能生態爆發，大量第三方 Skills 湧入社群；惡意技能可能暗藏 Prompt Injection 攻擊、敏感憑證竊取、數據回傳外洩或供應鏈後門，造成嚴重的本地安全威脅。",
        "how": "NVIDIA 開發之專用 AI Agent 技能安全掃描器（Python 3.12+ 開發，遵循 Apache 2.0 開源協議）；結合靜態 AST 代碼分析、啟發式規則引擎與專屬安全大模型，在技能安裝前對其指令文檔、Shell 腳本與 API 進行全方位深度安全審計。",
        "what": "一鍵掃描 Claude Code、Codex 與 MCP 技能目錄；精確檢測 Prompt Injection 隱藏提示詞、敏感憑證（API Keys/SSH）讀取行為、惡意網路外聯請求與依賴供應鏈風險；輸出結構化安全評估報告與風險防範建議。",
        "bullets": [
            "NVIDIA 官方出品之 AI Agent 技能與 MCP 工具專屬安全審查掃描器",
            "精確偵測 Prompt Injection 隱蔽注入、憑證洩漏與惡意數據外傳",
            "多維度靜態分析與啟發式規則引擎，全面審查 SKILL.md 與伴隨腳本",
            "在安裝未知社群技能前建立關鍵安全防線，保護開發者本機環境安全"
        ]
    },
    "nesquena/hermes-webui": {
        "category_id": "agent_orchestration",
        "why": "Nous Research 開發的 Hermes Agent 具備優秀的自我學習與自主決策能力，但原生地基於終端 CLI 或聊天軟體互動，缺乏一個直觀、專屬且適合在手機或瀏覽器隨時操作的現代 Web 介面。",
        "how": "基於 Python 與現代前端技術構建的輕量化 WebUI，專注於低延遲串流響應與暗黑風格美學；透過 WebSocket / HTTP 與伺服器端運行的 Hermes Agent 守護進程進行雙向通訊，支援動態記憶預填（Dynamic Recall Prefill）。",
        "what": "提供響應式 Web 界面，支援在桌面電腦與行動手機上無縫調度 Hermes Agent；完整支援多輪對話歷史、工具調用視覺化過程、記憶庫檢視與切換模型網關；具備極低資源佔用與極致易用性。",
        "bullets": [
            "專為 Nous Research Hermes Agent 量身打造的輕量化 Web 界面",
            "支援桌面端與手機行動瀏覽器無縫操作，隨時隨地掌控自主 Agent",
            "可視化展示多步驟工具調用過程、思考軌跡與長期記憶庫",
            "支援 Dynamic Recall Prefill 與 Gateway 多模型切換"
        ]
    },
    "doggy8088/Paste-to-Markdown": {
        "category_id": "web_doc_parsing",
        "why": "開發者或寫作者從網頁、Word 或線上文檔複製富文本時，貼上至 Markdown 編輯器往往夾雜混亂的 HTML 標籤、格式跑版，特別是數學公式（LaTeX）常損壞遺失；且許多線上轉換工具存在資料上傳的隱私隱患。",
        "how": "Will 保哥開發的純前端客戶端轉換工具（100% Client-Side，JavaScript 開發）；利用現代瀏覽器 Clipboard API 讀取剪貼簿多格式內容，採用優化正則與 Turndown 改進引擎將 HTML/RTF 即時轉化為乾淨標準 Markdown。",
        "what": "只需要在瀏覽器中按下 Ctrl+V 即可瞬間轉換；強大支援數學公式自動轉化為標準 LaTeX 語法（支援 MathJax / KaTeX）；提供代碼高亮、表格完美排版、一鍵複製與完全離線隱私保障，數據絕不上傳任何伺服器。",
        "bullets": [
            "100% 純前端客戶端運行，數據絕不上傳伺服器，完全保障隱私安全",
            "按下 Ctrl+V 即時將剪貼簿 HTML/RTF 內容轉換為純淨標準 Markdown",
            "獨家強化數學公式識別，自動還原 MathJax / KaTeX 為乾淨 LaTeX 代碼",
            "完美保留多欄表格排版與程式代碼區塊語法高亮"
        ]
    },
    "mem0ai/mem0": {
        "category_id": "context_memory_rag",
        "why": "現有 LLM 每次會話均為無狀態（Stateless），在多輪長週期協同、個人助理與自適應教學場景中，模型無法記住使用者的長期喜好、歷史決策與個人事實，導致用戶體驗重複且割裂。",
        "how": "專為 AI Agent 打造的生產級持久化記憶架構（The Memory Layer for AI Agents）；採用 2026 年最新動態記憶演算法，自動從對話中提取實體、偏好與時序關係，結合向量檢索與記憶圖譜（Memory Graph），實現記憶的分級儲存與智慧動態檢索。",
        "what": "提供開箱即用的 Python SDK、REST API 與多種 Agent 框架適配器（LangChain, CrewAI, AutoGen 等）；支援使用者級別、會話級別與 Agent 級別的多租戶記憶隔離；具備記憶即時更新、矛盾修正與歷史回溯能力。",
        "bullets": [
            "生產級 AI 記憶層基礎設施（The Memory Layer for AI Agents）",
            "採用 2026 最新記憶演算法，結合向量搜尋與 Memory Graph 拓撲關聯",
            "支援使用者（User）、會話（Session）與代理（Agent）三層記憶隔離",
            "提供即插即用的 Python SDK、REST API，無縫適配 LangChain, CrewAI, AutoGen"
        ]
    },
    "ombharatiya/ai-system-design-guide": {
        "category_id": "education_productivity",
        "why": "構建生產級 AI 系統涉及高維度向量檢索、多 Agent 編排、動態上下文工程、低延遲推理快取與評估體系（Evals），但工程師缺乏一份系統化梳理架構權衡與大廠系統設計面試標準的權威參考手冊。",
        "how": "由前沿工程師精心撰寫的全面技術指南（線上站點 aidaddy.tech 支援即時檢索）；結構化拆解從基礎大模型調度到百萬級並發 Agent 系統的架構模式，深入分析 AWS、Azure、Claude、Gemini 等平台選型權衡。",
        "what": "涵蓋 RAG 架構演進、Agent 容錯與狀態管理、Prompt Cache 快取優化、成本控制策略、AI 系統評估與安全護欄設計；包含真實大廠高頻面試案例架構圖與工業界最佳實踐清單。",
        "bullets": [
            "生產級 AI 系統設計與大廠面試必備的完整權威參考手冊（aidaddy.tech）",
            "深入解析進階 RAG、動態 Prompt 快取、延遲優化與成本控制策略",
            "包含海量真實架構拓撲圖與具體工業案例分析（涵蓋 AWS/Azure/Claude）",
            "覆蓋 AI 安全護欄、幻覺抑制與 LLM 評估體系（Evals）最佳實務"
        ]
    },
    "Leonxlnx/taste-skill": {
        "category_id": "claude_code_skills",
        "why": "AI 編程代理（如 Claude Code）在生成前端 UI 時，往往採用陳舊死板的預設模板、俗氣的漸層色與千篇一律的元件排列（俗稱 AI Slop），缺乏現代高質感設計美學與細膩的微互動。",
        "how": "專為前端開發設計的「Anti-Slop」風格約束框架與 Agent Skill；將當代頂級 UI/UX 設計原則（如瑞士排版風格、極簡留白、精緻微動效、精緻 Typography 與色彩語義）固化為 Agent 可強制遵循的提示詞規則庫。",
        "what": "一鍵掛載至 Claude Code 等 Coding Agent；徹底杜絕俗套的 AI 模板化前端代碼，強制生成具備高級審美質感的現代介面；支援 Tailwind CSS、Framer Motion、現代字體選型與精緻配圖生成規範。",
        "bullets": [
            "「Anti-Slop」前端審美框架，徹底擺脫 AI 生成的陳腐通用 UI 樣式",
            "強制 Agent 遵循現代高質感設計準則：優雅留白、微動效與精緻字體排印",
            "無縫適配 Tailwind CSS, Framer Motion, shadcn/ui 等現代前端生態",
            "作為標準 Claude Code Skill 隨插即用，立竿見影提升生成介面品味"
        ]
    },
    "helloianneo/ian-xiaohei-illustrations": {
        "category_id": "visualization_diagrams",
        "why": "許多技術文章、Notion 文檔與博客在配圖時面臨兩難：商業插畫成本高昂，通用 AI 生圖又容易產生油膩塑料感；需要一種具有鮮明識別度、手繪質感且能精確傳達核心認知判斷的專屬配圖風格。",
        "how": "專為 Codex 與 Claude Code 設計的視覺提示工程與技能外掛（Skill）；以「小黑」原創 IP（黑色實心、白點眼、荒誕認真的工作者角色）為視覺錨點，指導生圖模型繪製 16:9 白底、黑白線條手繪、輔以少量紅橙藍批注的解釋性插圖。",
        "what": "自動理解技術文章中的抽象判斷、流程拓撲或隱喻，精確轉化為具備記憶點的正文配圖；提供豐富的生圖提示詞範例、風格約束規則與批次生成腳本，讓技術作者能穩定產出高質感原創插畫。",
        "bullets": [
            "以原創「小黑」荒誕工作者為 IP，打造高辨識度手繪正文配圖風格",
            "16:9 橫版白底手繪，輔以少量紅橙藍批注，精準視覺化核心認知判斷",
            "專為 Codex 與 Claude Code 設計的 Skill 規範，自動解析文章隱喻",
            "杜絕油膩 AI 塑料感插圖，為技術博客與方法論文章提供靈魂配圖"
        ]
    },
    "microsoft/SkillOpt": {
        "category_id": "claude_code_skills",
        "why": "微軟研究院重磅專案。現有 Agent 技能（Skills）多由人類憑經驗手動撰寫，面對複雜任務時難以窮盡所有邊界情況；而在固定大模型權重（Frozen LLM）的前提下，如何系統化自我演進與優化自然語言技能是前沿難題。",
        "how": "基於文字空間的優化器（Text-space Optimizer），將神經網絡訓練的理念（Epochs, Mini-batch, Learning Rates, 驗證集門控）遷移到自然語言技能的優化上；透過軌跡驅動編輯（Trajectory-driven edits）與執行回饋循環，自動疊代優化 `SKILL.md`。",
        "what": "提供完整的 Python 套件（`pip install skillopt`）與 WebUI 視覺化監控介面；支援多種 LLM 後端；在基準測試中自動演化出表現最佳的 `best_skill.md` 產物，顯著提升 Agent 在多步驟任務中的成功率與穩健性。",
        "bullets": [
            "微軟開創之文字空間優化器（Text-space Optimizer），實現 Agent 技能自演化",
            "類比神經網路訓練機制：支援 Epochs, Batchsize, 學習率與驗證門控",
            "在不微調模型權重的前提下，自動疊代產出最優 `best_skill.md` 規範文檔",
            "提供 WebUI 監控面板與多後端支援，顯著提高複雜 Agent 任務成功率"
        ]
    },
    "jianshuo/ccglass": {
        "category_id": "model_routing_proxy",
        "why": "開發者使用 Claude Code、Codex、Kimi 等編程代理時，Agent 就像一個黑盒子，開發者無法直接看到每次請求實際向大模型發送了什麼完整提示詞、耗費多少 Token 與快取命中情況，難以除錯與控制成本。",
        "how": "基於 Node.js 打造之輕量化本機反向代理（Logging Reverse-Proxy）與即時 Web 儀表板，支援一鍵命令列啟動；透過攔截並透明轉發 Agent 的 HTTP/API 請求，在本地即時記錄所有上下文、工具呼叫與模型回應。",
        "what": "提供即時 Web 視覺化看板，即時捕獲請求明細、Token/Cache 統計與真實花費；展示 Agent 迴圈流程圖（Agent-loop Flow View）與輪次間增量差異比對（Turn-to-turn Diff）；支援一鍵無縫對接 Claude Code、Codex、OpenCode 等多種客戶端。",
        "bullets": [
            "輕量化本機透明反向代理與 Web 儀表板，一條指令 `ccglass` 即可運行",
            "穿透黑盒子：完整捕獲 Agent 向大模型發送的真實 System Prompt 與工具調用",
            "即時統計 Token 消耗、快取命中率與 API 費用花費",
            "提供清晰的 Agent 迴圈流程視圖（Flow View）與輪次間增量 Diff 對比"
        ]
    },
    "superset-sh/superset": {
        "category_id": "agent_orchestration",
        "why": "在大型軟體工程中，單個 Coding Agent 串行修改代碼速度緩慢，且切換分支極為繁瑣；開發者需要一個能平行調度上百個 AI 代理同時在多個隔離工作區中編程的現代化 IDE 基礎設施。",
        "how": "專為並行代理打造的 Agentic IDE，採用 TypeScript / React 全端架構；底層深度整合 Git Worktrees 技術，為每個並行運行的 Agent 自動創建獨立隔離的檔案工作樹，避免代碼衝突；支援自備訂閱（BYO Subscription）。",
        "what": "支援同時平行編排超過 100 個 Coding Agents（支援 Claude Code, Codex, OpenCode, Cursor Agent 等）；提供即時代碼差異監控、內建整合終端、跨代理任務分發面板與直觀的衝突解決工作流，使團隊開發速度實現數量級躍升。",
        "bullets": [
            "革命性 Agentic IDE，支援同時平行調度 100+ 個 Coding Agents",
            "深度集成 Git Worktrees 技術，各代理在獨立工作區安全運行互不干擾",
            "支援 Claude Code, Codex, OpenCode, Cursor 等多種主流編程智能體",
            "即時代碼 Diff 差異審查、任務分發儀表板與內建整合終端"
        ]
    }
}

def run():
    chunk_path = Path("data/chunks/chunk_1.json")
    out_path = Path("data/reviewed_chunks/reviewed_1.json")
    
    with open(chunk_path, "r", encoding="utf-8") as f:
        chunk_data = json.load(f)
        
    reviewed_items = {}
    
    for fn, r in chunk_data.items():
        if fn not in REFINEMENTS:
            raise KeyError(f"Missing refinement for {fn}")
            
        ref = REFINEMENTS[fn]
        cat_id = ref["category_id"]
        cat_meta = CATEGORIES_META.get(cat_id, {})
        cat_name = cat_meta.get("name", cat_id)
        
        stars = r.get("stargazers_count") or 0
        forks = r.get("forks_count") or 0
        lang = r.get("primary_language") or "N/A"
        topics = r.get("topics") or []
        readme = r.get("readme") or ""
        
        reviewed_items[fn] = {
            "full_name": fn,
            "name": fn.split("/")[-1],
            "owner": fn.split("/")[0],
            "url": r.get("url") or f"https://github.com/{fn}",
            "homepage": r.get("homepage"),
            "stargazers_count": stars,
            "forks_count": forks,
            "primary_language": lang,
            "topics": topics,
            "license": r.get("license"),
            "starred_at": r.get("starred_at"),
            "pushed_at": r.get("pushed_at"),
            "category_id": cat_id,
            "category_name": cat_name,
            "readme_has_content": len(readme) > 200,
            "analysis": {
                "why": ref["why"],
                "how": ref["how"],
                "what": ref["what"]
            },
            "bullets": ref["bullets"]
        }
        
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(reviewed_items, f, ensure_ascii=False, indent=2)
        
    print(f"[✓] Successfully refined all {len(reviewed_items)} repos in chunk 1 and saved to {out_path}")

if __name__ == "__main__":
    run()

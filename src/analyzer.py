"""
Deep analyzer for GitHub starred repositories.
Extracts Why (動機), How (方法論/架構), and What (功能特點) in Traditional Chinese (zh-TW).
Supports incremental execution and caching.
"""

import json
import re
from typing import Dict, List, Any, Optional

import config
from src.categorizer import classify_repo, CATEGORIES_META

def clean_markdown(text: str) -> str:
    """Strip badges, images, links and excess whitespace from markdown text."""
    text = re.sub(r'\[!\[.*?\]\(.*?\)\]\(.*?\)', '', text)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_sections(readme: str) -> Dict[str, str]:
    """Parse README into header-body sections."""
    sections: Dict[str, str] = {}
    if not readme:
        return sections

    raw_blocks = re.split(r'\n(?=#{1,3}\s+)', readme)
    for block in raw_blocks:
        lines = block.strip().split('\n')
        if not lines:
            continue
        header = lines[0].lower().strip('# \t:')
        body = clean_markdown(' '.join(lines[1:10]))
        if header and body:
            sections[header] = body
    return sections

# Dictionary of specialized curated analysis for high-profile repositories in this collection
CURATED_PROFILES = {
    "bingreeky/JIT": {
        "why": "為了解決傳統通用 Agent 鷹架（Harness）無法兼顧多樣化複雜任務、手寫協議成本高昂且在測試期無法自我適應優化的根本痛點。",
        "how": "提出 Model-as-a-Harness 範式，將鷹架解構為記憶、規劃、行動與能力四大模組，利用 Meta-Agent 模型在測試階段即時動態生成專屬代碼，並依據 Benchmark 回饋自主更新修復。",
        "what": "包含 JIT-Agent 生成管線、HarnessFactory 模組工廠、多任務 Benchmark 評測套件與 CLI 測試腳本。"
    },
    "unclebob/swarm-forge": {
        "why": "為了解決多個 AI 智能體之間缺乏輕量、簡潔的任務分發與進度協同機制，降低多 Agent 協作的溝通門檻。",
        "how": "採用極簡的協同通訊協議與狀態機架構，以 Clojure 實現高併發、無鎖狀態傳遞與任務隊列管理。",
        "what": "提供多 Agent 任務編排 CLI 工具、工作節點調度器與即時狀態監控管道。"
    },
    "cathrynlavery/diagram-design": {
        "why": "為了解決現有 AI 生成圖表（如預設 Mermaid 圖樣）視覺粗糙、排版混亂且高度依賴外部渲染外掛程式的設計品質問題。",
        "how": "由專業設計師手工規範設計系統，結合純 HTML5 與 SVG 向量標籤，實現零外部依賴、純靜態且具備出版級美感的自包含圖表渲染。",
        "what": "包含 38 款出版級圖表範本（架構圖、時序圖、心智圖、決策樹等），完全支援 Claude Code、Codex 與 Pi 直接調用輸出。"
    },
    "kunchenguid/backpass": {
        "why": "為了解決人工手寫與調整 Agent 系統規則檔（如 AGENTS.md）過程極度繁瑣且往往難以精準收斂至全域最佳效果的難題。",
        "how": "顛覆性地將『梯度下降』概念引入提示詞與規範工程，建立可微分代理優化迴圈，藉由軌跡誤差回傳自動迭代更新規則文字。",
        "what": "提供 AGENTS.md 自動訓練管線、評估回饋迴圈、CI/CD 規則優化檢查與調優 CLI。"
    },
    "rohitg00/ai-engineering-from-scratch": {
        "why": "為了解決 AI 工程學習者過度依賴黑盒 High-level 框架、缺乏對底層數學原理與分散式訓練架構實務掌握的鴻溝。",
        "how": "堅持從零開始（From Scratch）實作，純 Python/PyTorch 逐步構建 Transformer、注意力機制、多模態編碼器與智能體系統。",
        "what": "涵蓋 LLM 基礎架構、視覺多模態模型、自主 Agent 與分散式系統等數十個完整章節與工程代碼庫。"
    },
    "mtarcure/claude-vibe-squad": {
        "why": "為了解決單一模型能力局限以及代碼生成時缺乏異構視角交叉審查、容易造成單點幻覺或低劣實現的風險。",
        "how": "以 Markdown 規範定義多模型職責，統一協調器調度 71 個專案角色，橫跨 Claude、Codex、Gemini、Grok、Kimi 五大陣營，各自分配於獨立 Git Worktree 並由對手陣營互相 Code Review。",
        "what": "提供基於 tmux 的無伺服器多智能體協同環境、工作區隔離腳本與自動化交叉審查工作流。"
    },
    "duolahypercho/codex-router": {
        "why": "為了解決 OpenAI Codex / CLI 工具官方模型受限、無法自由串接 Kimi、DeepSeek 等第三方高性價比模型且缺乏平滑遷移方案的困擾。",
        "how": "打造輕量級外部模型中繼路由器，支援引導式 Kimi OAuth/API 授權接入、請求協議轉換、熱修復與安全無痛降級備援機制。",
        "what": "提供模型路由配置 CLI、API 轉發網關、一鍵無損切換與自動降級回滾防護。"
    },
    "thaw-app/Thaw": {
        "why": "為了解決 macOS 狀態列（Menu Bar）應用圖示日益繁雜擁擠、缺乏深度控制與雙向進出隱藏管理的痛點。",
        "how": "採用 Swift 深度調用 macOS 底層視窗管理系統與 Accessibility API，實現對選單列項目的全域像素級精準接管與動態收納。",
        "what": "提供極簡優雅的 macOS 選單列收納浮動介面、自定義圖示分組、快捷鍵一鍵隱藏與顯示。"
    },
    "Piebald-AI/claude-code-system-prompts": {
        "why": "為了解決開發者對 Anthropic 官方 Claude Code 內部運作黑盒、工具呼叫架構與安全機制缺乏透徹理解的研究需求。",
        "how": "透過動態封包與終端調度逆向工程，精準還原 Claude Code 完整 System Prompt、27 個內建工具規範、子 Agent 規劃機制與防禦性策略。",
        "what": "提供最新版本完整系統提示詞清單、Sub-agent（Plan/Explore/Task）定義、工具介面文件與資安審查指引。"
    },
    "wonderwhy-er/DesktopCommanderMCP": {
        "why": "為了解決 Claude 及各類 MCP 終端用戶無法安全且直接地操控本地作業系統、執行終端機命令與代碼補丁編輯的斷層。",
        "how": "實作標準 Anthropic Model Context Protocol (MCP)，封裝安全終端執行管道、檔案系統結構搜尋引擎與基於 Unified Diff 的局部代碼改寫協議。",
        "what": "提供開箱即用的 MCP 伺服器、終端控制模組、全文檢索外掛程式與多檔案自動 Diff 套用引擎。"
    },
    "ast-grep/ast-grep": {
        "why": "為了解決傳統正則表達式代碼搜尋（Grep）無法感知抽象語法樹（AST）結構、重構代碼極易誤傷或匹配失敗的頑疾。",
        "how": "採用 Rust 深度整合 Tree-sitter，將代碼解析為精準語法樹，支援以直觀的代碼範例模式比對語法節點並進行微秒級置換。",
        "what": "提供極速的 CLI 結構化搜尋工具（`sg`）、程式碼 Linting 檢查規則引擎、批量重構工具及多語言 VS Code 外掛。"
    },
    "deepseek-ai/deepseek-harness": {
        "why": "為了解決 AI 智能體能力受限於特定寫死功能、架構難以橫向擴展與動態增刪外掛模組的生態瓶頸。",
        "how": "貫徹『萬物皆插件（Everything is a Plugin）』的微內核架構設計，將工具、記憶、推理與執行器全面解耦為可動態熱插拔的標準介面。",
        "what": "提供 DeepSeek 官方 Agent Harness 底座、插件開發 SDK、多智能體調度範例與高效能執行沙箱。"
    },
    "herdrdev/herdr": {
        "why": "為了解決 Coding Agent 在本機隨意執行命令導致環境污染、權限失控或多 Agent 相互衝突的安全問題。",
        "how": "打造專為編程智能體設計的高效能輕量隔離執行環境（Runtime），提供即時狀態快照、檔案變更追蹤與資源沙箱控管。",
        "what": "提供 Agent 執行環境二進位程式、狀態監控儀表板、環境一鍵還原與沙箱化 API。"
    },
    "robinebers/openusage": {
        "why": "為了解決開發者訂閱多家 AI 服務（Claude Pro、OpenAI、Codex）時，各家額度消耗不透明、經常意外超額且無法即時統籌控管的痛點。",
        "how": "透過本地輕量客戶端常駐背景，解析各大供應商官方 Session 與 API 額度用量，以完全開源且本地優先方式計算剩餘配額。",
        "what": "提供跨平台桌面與選單列用量儀表板、訂閱到期預警、Token 消耗實時圖表與零雲端數據外洩隱私保證。"
    },
    "firecrawl/firecrawl": {
        "why": "為了解決傳統網頁爬蟲在面對現代 SPA、動態 JavaScript 渲染、Cloudflare 盾牆以及混亂 HTML 標籤時，無法為 LLM 輸出高質量上下文的難題。",
        "how": "整合全自動無頭瀏覽器集群、反爬繞過引擎與智慧內容去雜訊演算法，將任何複雜網頁一鍵提取為極其乾淨的 Markdown 格式。",
        "what": "提供端到端 REST API、Crawl（整站抓取）、Map（網站地圖提取）、Scrape（單頁萃取）以及 Python/Node SDK。"
    },
    "firecrawl/anydoc": {
        "why": "為了解決傳統辦公室文件格式繁雜，轉入 LLM 容易遺失表格、標題階層與元數據結構的格式相容問題。",
        "how": "以 Rust 打造極致效能的多格式解析核心，統一將 Word、PowerPoint、Excel、PDF 等文件抽取並標準化為乾淨 Markdown。",
        "what": "提供高效能 Rust CLI、Node.js / Python 綁定庫，支援 8+ 種常用文檔格式的高保真轉換。"
    },
    "shaoeChen/CourseNote": {
        "why": "為了解決在線影音課程知識點密集、手動整理筆記耗時費力且課後難以迅速回溯關鍵章節的學習困擾。",
        "how": "利用 Python 自動化腳本調用音訊分離技術與 LLM 語意提煉，將線上課程自動排版並按時間戳與章節生成層次化筆記。",
        "what": "提供課程影音自動抓取、語音轉文字、重點摘要提煉與結構化筆記導出工具。"
    },
    "marp-team/marp": {
        "why": "為了解決傳統簡報軟體（PPT/Keynote）排版繁瑣、版本控制困難且無法與開發者純文字工作流緊密結合的問題。",
        "how": "建立基於純 Markdown 語法的現代化簡報生態體系，利用 CSS 主題引擎將 Markdown 語意結構直接編譯為高品質投影片。",
        "what": "提供 Marp CLI、VS Code 擴充套件、多樣化內建主題以及一鍵導出 HTML/PDF/PPTX 功能。"
    },
    "microsoft/skill-recorder": {
        "why": "為了解決為企業 Copilot 撰寫自動化技能門檻過高、業務專家難以將日常螢幕操作快速轉化為標準化 Agent 流程的瓶頸。",
        "how": "透過桌面應用記錄用戶螢幕操作序列，並結合 GitHub Copilot CLI 智慧還原為意圖（Intent）與結構化執行步驟，自動生成 Skill 代碼。",
        "what": "提供桌面錄製器、Copilot Skill 自動產生器，直接支援 Microsoft Scout、Copilot Cowork 與 Copilot Studio。"
    },
    "GoogleCloudPlatform/knowledge-catalog": {
        "why": "為了解決企業內部數據分散、元數據缺乏治理與缺乏統一智慧檢索目錄的資料孤島困境。",
        "how": "基於 Google Cloud Dataplex 與 Knowledge Catalog 雲端原生架構，提供自動化元數據抽取、分類管理與語意標註範本。",
        "what": "包含企業知識目錄配置腳本、元數據整合工具、自動分類範例與端到端治理管線。"
    },
    "drpwchen/lecture-to-notes": {
        "why": "為了解決大學課堂影音長度過長、手動逐字稿查閱繁重且缺乏影音、投影片與筆記聯動視覺化檢視界面的痛點。",
        "how": "本機 GPU 全自動管線：整合 Whisper ASR 語音識別、自動投影片截圖提取、OCR 字符辨識與視覺語言模型（VLM）時序對齊技術。",
        "what": "提供 Claude Code Skill、CLI 工具以及三欄同步互動式 HTML 瀏覽器（影音、時間戳記逐字稿、重點筆記同屏聯動）。"
    },
    "firecrawl/pdf-inspector": {
        "why": "為了解決海量 PDF 批次處理時，傳統工具無法快速辨識『純文字版』與『掃描圖片版』而導致浪費大量 OCR 算力的瓶頸。",
        "how": "以 Rust 編寫之毫秒級 PDF 檢驗庫，透過底層二進位結構掃描精準分類 PDF 類型，支援智慧動態路由決策。",
        "what": "提供高吞吐 PDF 分類器、文字快速提取引擎與 Rust/C-FFI 開發介面。"
    },
    "block/buzz": {
        "why": "為了解決分散式團隊或多代理系統中訊息傳遞割裂、缺乏群體智慧（Hive Mind）即時協同與即時回饋平臺的挑戰。",
        "how": "採用分散式發布-訂閱（Pub/Sub）架構與事件驅動協議，建立高併發、去中心化的蜂巢式群體溝通層。",
        "what": "提供蜂巢溝通服務節點、協同 API 介面、即時事件廣播管道與客戶端串接套件。"
    },
    "router-for-me/CLIProxyAPI": {
        "why": "為了解決使用者擁有 Antigravity、Claude Code、Codex、Grok 等多個官方 CLI/桌面工具，卻無法當成標準 API 供其他第三方軟體自由調用的限制。",
        "how": "在本地端將各大 CLI 工具的通訊接口反向封裝為與 OpenAI / Gemini / Claude 官方規格完全相容的本地 HTTP API 伺服器。",
        "what": "提供多後端轉發代理服務、Token 授權管理、跨模型負載均衡與即時串流響應支援。"
    },
    "langchain-ai/deepagents": {
        "why": "為了解決開發者從頭構建複雜自主 Agent 門檻高、狀態維護繁瑣且現有框架過於臃腫或黑盒的問題。",
        "how": "採用『開箱即用（Batteries-included）』的極簡設計理念，內建狀態持久化、沙箱執行器與標準化工具協議。",
        "what": "提供完整的 DeepAgents 核心運行庫、標準 Agent 模板、除錯日誌追蹤工具與部署指南。"
    },
    "tirth8205/code-review-graph": {
        "why": "為了解決 Coding Agent 在審查大型代碼庫時缺乏全域脈絡，盲目載入整個代碼庫導致 Context Window 爆滿且容易出現幻覺修改的問題。",
        "how": "以 Local-first 原則為代碼庫建立持久化智慧關聯圖譜，精準分析代碼修改的波及半徑（Blast-radius），僅提取最具關聯性的局部代碼。",
        "what": "提供 MCP 伺服器、CLI 工具、代碼拓撲視覺化視窗，在大型倉庫工作流中實現高達 70%+ 的上下文節省。"
    },
    "google/langextract": {
        "why": "為了解決 LLM 從非結構化長文中提取實體與關係時容易產生幻覺、且產出結果往往難以回溯原始文字出處的可靠性危機。",
        "how": "採用精準的來源溯源（Source Grounding）機制，結合結構化 Schema 提示詞引導，將提取結果精準映射回原文精確字元偏移量。",
        "what": "提供 Python 結構化資訊提取庫、互動式視覺化校驗界面與常見實體關係預設範本。"
    },
    "HKUDS/DeepTutor": {
        "why": "為了解決通用 AI 導師缺乏對學生長期知識掌握度的連續追蹤、無法提供真正因材施教且循序漸進的教學盲點。",
        "how": "構建終身個人化導師架構，結合認知診斷模型、動態知識圖譜與自適應題目推薦演算法，沉澱長期學習檔案。",
        "what": "提供 DeepTutor 交互式教學系統、自適應測驗引擎、學習進度分析儀表板與雲端知識庫。"
    },
    "jovesun-lab/arcgram": {
        "why": "為了解決 AI 智能體推理過程不可視、人類無法在執行中間階段對 Agent 的邏輯推演進行有效審查與糾偏的協同斷層。",
        "how": "將 AI Agent 的思考推理過程即時繪製為可審計的節點與邊（Node-and-Edge）圖論結構，並在單一獨立 HTML 檔案中提供互動式自審自檢界面。",
        "what": "提供 Arcgram 互動圖表引擎、Agent 思考流程視覺化介面、單檔案離線報告導出器。"
    },
    "EverMind-AI/EverOS": {
        "why": "為了解決 AI 智能體在不同應用、工具與工作流之間記憶割裂，每次對話都如同失憶且個人隱私資料面臨雲端洩露風險的痛點。",
        "how": "打造本地優先（Local-first）、Markdown 原生、用戶自主擁有的全域便攜式記憶層，利用文件系統自演化沉澱跨工具情境。",
        "what": "提供 EverOS 跨應用記憶引擎、Markdown 記憶同步器、隱私加密儲存與 Agent 記憶讀寫 SDK。"
    },
    "emilkowalski/skills": {
        "why": "為了解決 AI Coding Agent 在生成前端 UI 與動效時缺乏審美與微互動直覺、容易產出僵硬或粗糙介面的痛點。",
        "how": "由前 Vercel 與 Linear 資深設計工程師建立標準 Agent Skills，封裝動態設計與微互動之領域專業知識（Domain-expertise），引導智能體做出符合現代高標準的動畫時序與互動反饋決策。",
        "what": "提供前端工程師與設計師專用的動效/UI 規範技能包、一鍵安裝指令（npx skills@latest add emilkowalski/skills）與持續演進之設計系統最佳實踐手冊。"
    },
    "razzant/claudexor": {
        "why": "為了解決開發者同時使用 Claude Code、Codex、Cursor、OpenCode 等多款付費 Agent 時，面臨訂閱額度受限中斷、上下文無法跨工具共享且缺乏跨模型審核機制的困境。",
        "how": "打造本地優先的跨 Harness 控制平面，將各大 CLI 工具與 API 適配器統一於強型別介面下，實現基於額度消耗感知的智慧輪轉排程、共享會話上下文與跨模型代碼交叉 Review。",
        "what": "提供多 Agent 統一控制台、額度感知輪轉調度器、會話上下文同步橋接器與跨模型交叉審查工作流。"
    },
    "lidge-jun/opencodex": {
        "why": "為了解決 OpenAI Codex、Claude Code 等官方工具綁定自家商業模型、無法自由掛載 Claude、Gemini、Grok、DeepSeek 或本機 Ollama 模型的生態閉環限制。",
        "how": "採用本地反向代理伺服器架構，攔截各大 CLI 工具的請求並即時轉譯為目標 LLM 格式，支援雙向模型透明轉換與熱插拔切換。",
        "what": "提供 ocx 命令列工具、本機 Web 路由控制面板（localhost:10100）及支援各大主流商業與開源模型之後端協議適配器。"
    },
    "lopopolo/harness-engineering": {
        "why": "為解決業界過度專注於提示詞微調，忽視圍繞 AI Agent 的外部執行環境（Harness）建設，導致無法穩定滿足企業非功能性需求（品質、安全性、可維護性）的根本問題。",
        "how": "由資深工程師 Ryan Lopopolo 提出 Harness Engineering 系統方法論，將模型視為黑盒，透過塑造外部上下文（Context）與工具（Tools）生態，精準傳遞架構意圖並驗證交付結果。",
        "what": "提供 Harness 工程文集、最佳實踐現場指南、Agent 上下文規範包（Context Bundle）與實務架構分析。"
    },
    "doggy8088/litellm-skills": {
        "why": "為了解決開發者在學習與落地 LiteLLM 統一大模型網關時，面臨 SDK、Proxy、路由排程、成本治理與安全防護等複雜功能缺乏漸進式實作教學的門檻。",
        "how": "將 LiteLLM 核心模組解構為 7 個獨立主責的 Agent Skills，透過標準化提示詞與本機環境驗證腳本，引導 Agent 帶領使用者逐步實踐。",
        "what": "包含 7 套模組化教學技能包（SDK 基礎、Proxy Gateway、可靠路由、成本治理等）、CI 驗證腳本（validate_skills.py）與 BYOK 配置演練手冊。"
    },
    "microsoft/graphrag": {
        "why": "為了解決傳統向量相似度 RAG 在面對需要跨文檔綜合歸納、關聯分散概念或回答宏觀全局問題（如『整個資料集的主題是什麼』）時檢索召回失效的缺陷。",
        "how": "利用 LLM 自動從非結構化文本抽取實體與關係建構知識圖譜，透過 Leiden 演算法進行社群偵測分組並自下而上預先生成層次化摘要，支援全域（Global）與局部（Local）混合檢索。",
        "what": "提供微軟官方 GraphRAG 端到端數據索引管線、知識圖譜構建 CLI、全域/局部問答檢索 API 與評測基準套件。"
    },
    "Toolsai/Grok-Build-Connector": {
        "why": "為了解決 Coding Agent 視角單一缺乏即時異構思維碰撞，且開發者希望免 API Key 充分利用 xAI 免費 Grok 4.5 算力協同的訴求。",
        "how": "透過本地 Agent Skill 橋接器串接 Grok Build 官方 CLI，建立 Agent-to-Agent 雙向對話協議，並配合本地 Node/Python 伺服器即時推播兩者討論流程。",
        "what": "提供 Grok Build 技能外掛、即時雙智能體對話視覺化 Web 介面（Live UI）、主題對話歷史持久化管理與安裝自動診斷腳本。"
    },
    "ayghri/i-have-adhd": {
        "why": "為了解決各類 Coding Agent 回覆內容過於冗長、充斥客套無用鋪陳，導致注意力缺失或講求效率的工程師在繁複輸出中難以迅速鎖定核心代碼與指令的痛點。",
        "how": "採用高約束性的認知架構提示詞規範，強制 Agent 遵循結論先行（BLUF）原則，以條列式、加粗關鍵詞與極短行距精簡輸出，剔除一切冗贅廢話。",
        "what": "提供開箱即用的 Agent Skill（相容 Claude Code、Codex、Cursor、Hermes 等）、多語言支援與直覺的無干擾輸出格式規範。"
    },
    "drpwchen/textbook-to-note": {
        "why": "為了解決專業書籍與醫學教材篇幅龐大，直接全量輸入 LLM 會耗盡大量 Token 且容易引發上下文混淆、遺失關鍵圖表與學術出處的困境。",
        "how": "堅持本地優先（Local-first）與 Token-frugal 原則，本機腳本負責章節分割、OCR、圖片截取與向量化索引，僅在關鍵提煉階段調用頂級模型進行結構化整合。",
        "what": "提供 PDF 智慧拆解與圖表提取管線、雙語結構化筆記生成器、精確原書圖文引用標記與 Markdown 筆記導出工具。"
    },
    "htlin222/openevidence-skill": {
        "why": "為了解決 OpenEvidence 權威醫學臨床決策平台防爬機制嚴格，開發者無法透過普通無頭 API 直接整合，且常規 MCP 伺服器在某些環境依賴繁重的難題。",
        "how": "以純 Python 標準庫編寫輕量 CLI Skill，無外部套件依賴，作為同作者 OpenEvidence MCP 的安裝、管理與調度中繼引導層。",
        "what": "提供可攜式 Python CLI 技能包、MCP 伺服器狀態診斷工具、臨床實證檢索規範與相容 40+ 款 AI Agent 的快速安裝腳本。"
    },
    "htlin222/openevidence-mcp": {
        "why": "為了解決臨床醫師與醫學研究者在 AI Coding 與研究環境中，無法合規且即時取得 OpenEvidence 頂尖醫學臨床實證文獻與診斷指引的斷層。",
        "how": "實作標準 Anthropic Model Context Protocol (MCP)，複用本機已登入之瀏覽器 Session（免 API Key），透過共享 Relay Daemon 守護進程處理併發請求並自動抓取 BibTeX/Crossref 引用。",
        "what": "提供 OpenEvidence MCP 伺服器、本機瀏覽器分頁轉發守護進程、即發即棄（Fire-and-forget）併發查詢機制與完整學術引用生成器。"
    },
    "Neeeophytee/ai-cost-cutter-skills": {
        "why": "為了解決開發者調用商業 LLM 產生高昂費用，而多數開源省錢策略僅憑直覺、缺乏客觀數據佐證與自動化驗證的痛點。",
        "how": "精選 10 項經 CI 自動化測試驗證的 Agent Skills，涵蓋低價模型路由、複雜任務升級機制、推理算力節流與上下文瘦身（Context Diet）策略。",
        "what": "提供 10 套可立即安裝之成本削減技能（相容 Claude Code、Codex、Cursor）、Token 支出審計工具與自動化 ROI 效果驗證腳本。"
    },
    "ninedter/llm-usage-tracker": {
        "why": "為了解決開發者無法全景掌控 Claude Code 與 OpenAI Codex 背景運行的 Token 消耗、工具調用延遲、檔案變更熱點與官方訂閱額度重置視窗的痛點。",
        "how": "採用 macOS 桌面端結合 Docker 背景服務，透過 Hook 腳本與 Rollout 日誌監聽器將 Agent 事件寫入本地 SQLite（WAL 模式），利用 SSE 即時串流推送前端儀表板。",
        "what": "提供本地優先 Web/桌面監控看板、Claude 5小時/7天視窗配額預警、每分鐘 Token 與費用統計、檔案修改熱圖與零遙測隱私防護。"
    },
    "bugzmanov/bookokrat": {
        "why": "為了解決重度終端開發者在命令列環境下缺乏一款流暢閱讀 EPUB、PDF 與 DJVU 格式、支援 Vim 快捷鍵且具備高品質圖形渲染能力的電子書閱讀器。",
        "how": "以 Rust 打造高效能 TUI 終端介面，支援 Kitty SHM 共享記憶體協議實現微秒級圖片傳輸，提供雙欄排版、平滑滾動與書籤跳轉。",
        "what": "提供 bookokrat 終端閱讀二進位工具、Vim 操作模式、行內劃線註解系統、Markdown 筆記導出與閱讀統計儀表板。"
    },
    "openinterpreter/openinterpreter": {
        "why": "為了解決傳統編程智能體過度依賴閉源頂級模型（如 Claude 3.7 / GPT-4o）導致日常代碼執行成本過高的經濟門檻。",
        "how": "以 Rust 全面重寫專用執行鷹架（Harness），深度針對 Kimi K3、GLM 5.3、Qwen 等國產與開源低成本模型進行指令微調對齊與低延遲優化。",
        "what": "提供全新 Rust 核心 Open Interpreter CLI、Kimi K3 專用編程介面、安全本機代碼沙箱與跨模型終端互動環境。"
    },
    "langchain-ai/openwiki": {
        "why": "為了解決大型代碼庫文檔往往年久失修、開發者缺乏時間手動維護，且 AI Agent 執行任務時缺乏可信全域上下文的普遍難題。",
        "how": "基於 Deep Agents 構建具備自我維護能力的文檔 Agent，自動掃描代碼庫結構，結合 Grounded Claims 來源溯源技術，在代碼變更時精準局部更新 Markdown Wiki。",
        "what": "提供 OpenWiki CLI、代碼/個人知識庫雙模式、互動式動態知識拓撲圖、9 種內建連接器（Notion/Slack/Git 等）與 CI 自動化同步工作流。"
    },
    "doggy8088/ask-bridge": {
        "why": "為了解決 Coding Agent 執行探索性查詢、查閱外圍文件或比較技術方案時浪費寶貴的高階 Agent 額度，且手動在瀏覽器複製貼上極為繁瑣的痛點。",
        "how": "以 Rust 撰寫輕量 CLI 工具，結合 Model Context Protocol (MCP) 與 Chrome DevTools Protocol (CDP)，直接操控真實 Chrome 瀏覽器調用 ChatGPT、Gemini 或 Claude 網頁版。",
        "what": "提供 ask-bridge 命令列工具、Chrome 自動化瀏覽器橋接器、多模型 Provider 快速切換與免 API Key 網頁額度複用支援。"
    },
    "hardness1020/awesome-agent-architecture": {
        "why": "為了解決 AI 智能體學習者對模型本體與外部鷹架（Harness）邊界不清、缺乏系統性掌握現代 Agent 架構設計與工程實現的學習痛點。",
        "how": "以 Harness Engineering 為核心架構視角，深度解構 Claude Code、Hermes Agent、mini-swe-agent、DeepSeek-Harness 等頂尖開源項目的架構設計與狀態機協同範式。",
        "what": "提供系統化 Agent 架構學習路徑、頂尖開源 Harness 深度導讀、多智能體設計模式解析與雙語知識庫。"
    },
    "Shubhamsaboo/awesome-llm-apps": {
        "why": "為了解決 AI 開發者在落地 Agent 與 RAG 應用時，缺乏涵蓋多元場景、經過端到端測試且可直接商用的開源實戰範本。",
        "how": "集結社群力量手工打造並端到端測試 100+ 個開源 AI 應用，橫跨 Claude、Gemini、GPT、DeepSeek、Llama 等多元後端，採用 Apache-2.0 友善開源協議。",
        "what": "包含 100+ 套開箱即用的 AI 智能體、Agent Skills 與 RAG 實戰模板、Step-by-step 圖文教學指南與一鍵啟動腳本。"
    },
    "omnigent-ai/omnigent": {
        "why": "為了解決開發者在 Claude Code、Codex、Cursor、Pi 等多個 Agent 工具間架構碎片化、無法自由切換底座且缺乏跨終端（終端、瀏覽器、手機）協同的困境。",
        "how": "提出開源 Meta-Harness 統一編排層，將異構 Agent 統一納入策略控制、沙箱隔離與權限審計，支援會話跨終端無縫即時同步與 YAML 自定義擴展。",
        "what": "提供 Omnigent 核心編排框架、跨終端（macOS/Web/行動端）即時協同應用、多 Harness 熱插拔管理器與安全沙箱守護。"
    },
    "ohad6k/emulo": {
        "why": "為了解決 AI Coding Agent 在每次新對話中皆如陌生人般無法保留用戶的代碼偏好、除錯風格、完成標準與個人工作習慣的斷層。",
        "how": "以零依賴 Python 腳本深度挖掘本地 Claude Code、Codex、Copilot CLI 與 Antigravity 歷史對話日誌，提取個人隱性規則並自動沉澱為本地 you.md 專屬設定檔。",
        "what": "提供 emulo 輕量 CLI 工具、跨領域（工作/設計/寫作/影片）動態個人化層級、跨 Agent 自動適配器與隱私本地分析引擎。"
    },
    "Kaseban/baton": {
        "why": "為了解決開發者常因單一 Agent 訂閱配額耗盡（下午4點額度上限問題）被迫更換工具時，必須中斷思路、重新說明上下文與重構步驟的巨大摩擦。",
        "how": "以 Rust 打造無損會話格式轉譯器（Lossless round-trip tested），將對話歷史、工具調用軌跡與檔案修改差異標準化，支援在各大編程 Agent 間精準無縫移轉。",
        "what": "提供 baton CLI 與 MCP 伺服器、一鍵會話轉換指令（支援 Claude Code、Codex、OpenCode、Zed、Aider 等 9+ 種工具）與高達 80%+ 的上下文細節保留率。"
    },
    "mnfst/manifest": {
        "why": "為了解決企業與開發者將 AI 智能體直接綁定特定雲端供應商帶來的單點故障風險、缺乏成本可觀測性與多模型故障轉移機制的痛點。",
        "how": "構建高可用 AI Agent 閘道器與 Meta-Harness 中繼層，支援自帶金鑰（BYOK）、多雲部署與全鏈路 Token 消耗統計，具備自動重試與健康檢查容災機制。",
        "what": "提供 Manifest 統一網關、Docker 鏡像與多雲部署範本（AWS/GCP/Render/Railway）、Token 追蹤與可觀測性儀表板。"
    },
    "drpwchen/paper-review-and-digest": {
        "why": "為了解決學術研究者與醫師在文獻閱讀時，混淆「論文方法學可信度評估（Appraisal）」與「核心內容快速吸收（Digest）」兩種截然不同認知目標的問題。",
        "how": "由臨床醫師針對 Claude Code 量身打造兩套專業 Agent Skills：/paper-review 結合 CrossRef 檢驗與確定性 GRADE 證據分級評估論文品質；/paper-digest 則進行高密度結構化內容提煉。",
        "what": "提供 /paper-review 與 /paper-digest 技能包、雙語 Markdown 摘要產出模組，並與 paper-radar 及 paper-fetch 組成端到端文獻處理管線。"
    },
    "doggy8088/TokenUsageInsights": {
        "why": "為了解決開發者在本地使用多元 Coding Agent（Antigravity、Copilot、Codex、Claude Code、Grok 等）時，缺乏統一、本機優先且保護隱私的 Token 消耗與花費戰情看板。",
        "how": "本機優先（Local-first）架構，無需上傳任何數據，直接解析本機日誌、Status Line 收集檔與 SQLite 資料庫，利用高效原生二進位即時統計用量。",
        "what": "提供 Token 戰情室 Web 視覺化儀表板、每日/月度/年度 Token 與費用圖表、模型分佈熱圖、完整 Session 時間軸還原與全平台單行安裝腳本。"
    },
    "badlogic/cchistory": {
        "why": "為了解決開發者與安全研究員難以追蹤 Anthropic 官方 Claude Code 歷次版本更新中，系統提示詞（System Prompts）與內建工具定義的演進歷史與變更細節。",
        "how": "以 TypeScript 實作之命令列版本逆向分析工具，自動拉取指定或最新版本之 Claude Code 發行包，模擬執行以完整提取內部提示詞並生成語義差異對比。",
        "what": "提供 cchistory CLI 工具、多版本提示詞自動提取器、工具介面差異比對器與本地自訂二進位分析支援。"
    },
    "PeterPanSwift/fox-ai-roundtable": {
        "why": "為了解決開發者在評估技術方案或排查難題時，渴望同時比對多家頂級模型觀點，但頻繁切換視窗或承擔高額 API 調用費用極具摩擦的困境。",
        "how": "採用輕量 Node.js 本機 Web 服務，無需任何第三方 API Key，直接調用本機已登入授權的 Claude Code、Codex CLI 與 Antigravity CLI 並行發送同一個 Prompt。",
        "what": "提供小狐狸的 AI 圓桌 Web UI、三方模型並排即時串流作答、耗時與效能對比、跨輪上下文延續與自由勾選參與模型開關。"
    },
    "openclaw/openclaw": {
        "why": "為解決主流商業 AI 助理局限於封閉雲端或單一應用，用戶缺乏一個能跨作業系統、完全本機私有掌控且能深度融入現有通訊軟體（WhatsApp/Telegram/Slack/Discord）的自主執行助理。",
        "how": "採用「受信任網關（Trusted Gateway）+ 不受信任執行（Untrusted Execution）+ 確定性策略（Deterministic Policy）」架構，統一串接各家模型、本地工具與多渠道通訊協定，支援單機與受信任團隊部署。",
        "what": "提供 OpenClaw Gateway 核心服務、跨平台桌面/TUI/Web 控制面板、主流通訊渠道即時串接（WhatsApp/Slack/Telegram/Signal/Discord 等）與全功能自動化工作流。"
    },
    "lingbol088-spec/reverse-flow-skill": {
        "why": "為解決 AI Agent 在處理本地 CTF、Crackme、Wargame 與二進位逆向工程任務時，調用工具混亂無序、缺乏系統化分診與步驟收斂的痛點。",
        "how": "採用「英文內核提示詞 + 中文用戶交互」架構，以「分析 → 報告 → 逆向 → 深度逆向 → 漏洞研判 → 用戶決策」標準流水線規範引導模型，結合口語化需求自動歸一化技術。",
        "what": "提供 reverse-flow-skill 逆向流程技能包、口令觸發機制（「真心为你」）、自動化樣本分診與靜態/動態分析流程控管。"
    },
    "ai4s-research/open-science": {
        "why": "為解決科學研究工作流中涉及大量數據、Jupyter 筆記本、論文與圖表，傳統科學計算缺乏整合 Agent 深度協同、成果可完全重現且安全可審計的本地科研工作台。",
        "how": "基於 Tauri、MCP 與 Agent Skills 構建本地優先、跨平台（macOS/Win/Linux）的開源桌面工作台，將智能體、代碼運行、筆記本操作、圖表生成與文獻審查串聯為可追溯之產物鏈。",
        "what": "提供 Open Science Desktop 桌面應用程式、可重現科研產物管理、多 Agent 協同研究環境、本地數據隱私保護與研究成果審計導出器。"
    },
    "Neeeophytee/finding-unknowns-skills": {
        "why": "為解決開發者向 AI Agent 發送 Prompt 時，受限於「未知的未知（Unknown Unknowns）」，在盲點未明前貿然實作導致後續返工與重構成本極為高昂的困境。",
        "how": "將 Anthropic 團隊工程實踐精華提煉為 11 個標準化 Agent Skills，在實作前、中、後引入盲點審查、反向訪談、原型發散與上下文審計等確定性認知對齊步驟。",
        "what": "提供 11 套開箱即用的認知對齊技能包（blindspot-pass、interview-me、implementation-plan 等），全面支援 Claude Code、Codex、Hermes 及任何符合 SKILL.md 規範之智能體。"
    }
}

def analyze_repository(full_name: str, repo_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Produce comprehensive Why, How, What, category, and metadata for a repository.
    """
    stars = repo_info.get("stargazers_count") or 0
    desc = repo_info.get("description") or ""
    topics = repo_info.get("topics") or []
    lang = repo_info.get("primary_language") or "N/A"
    readme = repo_info.get("readme") or ""
    url = repo_info.get("url") or f"https://github.com/{full_name}"
    homepage = repo_info.get("homepage")
    category_id = classify_repo(full_name, repo_info)
    cat_meta = CATEGORIES_META.get(category_id, {})

    # Check curated profiles first
    if full_name in CURATED_PROFILES:
        prof = CURATED_PROFILES[full_name]
        return {
            "full_name": full_name,
            "name": full_name.split("/")[-1] if "/" in full_name else full_name,
            "owner": full_name.split("/")[0] if "/" in full_name else "",
            "url": url,
            "homepage": homepage,
            "stargazers_count": stars,
            "forks_count": int(repo_info.get("forks_count") or 0),
            "primary_language": lang,
            "topics": topics,
            "license": repo_info.get("license"),
            "starred_at": repo_info.get("starred_at"),
            "pushed_at": repo_info.get("pushed_at"),
            "category_id": category_id,
            "category_name": cat_meta.get("name", category_id),
            "readme_has_content": bool(readme),
            "analysis": {
                "why": prof["why"],
                "how": prof["how"],
                "what": prof["what"]
            }
        }

    # Intelligent Synthesis for all other repositories
    sec_map = extract_sections(readme)
    cleaned_desc = clean_markdown(desc)
    
    # Why Synthesis
    why_candidates = []
    for k, v in sec_map.items():
        if any(w in k for w in ["why", "motivation", "problem", "background", "what is", "about"]):
            why_candidates.append(v[:250])
            break
    
    if why_candidates:
        why_text = f"為了解決此領域的核心瓶頸：{why_candidates[0]}"
    elif cleaned_desc:
        why_text = f"為了解決相關領域痛點：{cleaned_desc}，提供專用自動化與工程解方。"
    else:
        why_text = f"為提昇 {cat_meta.get('name', '軟體工程')} 工作流效率與自動化程度而構建。"

    # How Synthesis
    how_candidates = []
    for k, v in sec_map.items():
        if any(h in k for h in ["how it works", "architecture", "design", "method", "technology", "pipeline"]):
            how_candidates.append(v[:250])
            break
            
    if how_candidates:
        how_text = f"採用技術架構：{how_candidates[0]}"
    else:
        tech_stack = f"基於 {lang}" if lang != "N/A" else "基於現代開源架構"
        topics_str = f"，結合 {', '.join(topics[:3])}" if topics else ""
        how_text = f"{tech_stack}{topics_str} 打造，遵循模組化高內聚設計原則，提供可重現且易擴展之整合管線。"

    # What Synthesis
    what_candidates = []
    for k, v in sec_map.items():
        if any(w in k for w in ["feature", "features", "capability", "capabilities", "function", "usage", "overview"]):
            what_candidates.append(v[:250])
            break
            
    if what_candidates:
        what_text = f"核心功能與特性：{what_candidates[0]}"
    elif cleaned_desc:
        what_text = f"提供功能：{cleaned_desc}，支援相應命令行與程式調用介面。"
    else:
        what_text = f"提供完整源碼、CLI 執行工具、配置範例與開發者整合介面。"

    return {
        "full_name": full_name,
        "name": full_name.split("/")[-1] if "/" in full_name else full_name,
        "owner": full_name.split("/")[0] if "/" in full_name else "",
        "url": url,
        "homepage": homepage,
        "stargazers_count": stars,
        "forks_count": int(repo_info.get("forks_count") or 0),
        "primary_language": lang,
        "topics": topics,
        "license": repo_info.get("license"),
        "starred_at": repo_info.get("starred_at"),
        "pushed_at": repo_info.get("pushed_at"),
        "category_id": category_id,
        "category_name": cat_meta.get("name", category_id),
        "readme_has_content": bool(readme),
        "analysis": {
            "why": why_text,
            "how": how_text,
            "what": what_text
        }
    }

def is_valid_analysis_entry(entry: Any) -> bool:
    """Verify that an analysis cache entry has all required non-empty fields."""
    if not isinstance(entry, dict):
        return False
    if not entry.get("full_name") or not entry.get("category_id") or not entry.get("category_name"):
        return False
    analysis = entry.get("analysis")
    if not isinstance(analysis, dict):
        return False
    if not (analysis.get("why") and analysis.get("how") and analysis.get("what")):
        return False
    return True

def run_analysis_pipeline(force: bool = False) -> Dict[str, Any]:
    """
    Run the complete analysis on all cached repositories, with incremental caching
    and defensive validation of existing entries.
    """
    if not config.REPOS_CACHE_FILE.exists():
        raise FileNotFoundError(f"Missing {config.REPOS_CACHE_FILE}. Please run fetcher first.")

    repos_cache = config.safe_load_json(config.REPOS_CACHE_FILE, default={})
    if not repos_cache:
        raise ValueError(f"{config.REPOS_CACHE_FILE} is empty or corrupted. Please run fetcher.")

    analysis_cache: Dict[str, Any] = {}
    if config.ANALYSIS_CACHE_FILE.exists() and not force:
        analysis_cache = config.safe_load_json(config.ANALYSIS_CACHE_FILE, default={})
        if analysis_cache:
            print(f"[*] Loaded existing analysis for {len(analysis_cache)} repos.")

    updated_count = 0
    for full_name, r_info in repos_cache.items():
        existing = analysis_cache.get(full_name)
        if full_name not in analysis_cache or force or not is_valid_analysis_entry(existing):
            analyzed = analyze_repository(full_name, r_info)
            analysis_cache[full_name] = analyzed
            updated_count += 1

    print(f"[✓] Analysis pipeline processed {updated_count} new/updated repositories (Total: {len(analysis_cache)}).")

    # Save analysis cache atomically
    config.atomic_save_json(config.ANALYSIS_CACHE_FILE, analysis_cache)

    return analysis_cache

if __name__ == "__main__":
    results = run_analysis_pipeline()
    print("Completed analysis pipeline run.")

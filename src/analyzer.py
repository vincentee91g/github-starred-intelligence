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
            "name": full_name.split("/")[-1],
            "owner": full_name.split("/")[0],
            "url": url,
            "homepage": homepage,
            "stargazers_count": stars,
            "forks_count": repo_info.get("forks_count", 0),
            "primary_language": lang,
            "topics": topics,
            "license": repo_info.get("license"),
            "starred_at": repo_info.get("starred_at"),
            "pushed_at": repo_info.get("pushed_at"),
            "category_id": category_id,
            "category_name": cat_meta.get("name", category_id),
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
        "name": full_name.split("/")[-1],
        "owner": full_name.split("/")[0],
        "url": url,
        "homepage": homepage,
        "stargazers_count": stars,
        "forks_count": repo_info.get("forks_count", 0),
        "primary_language": lang,
        "topics": topics,
        "license": repo_info.get("license"),
        "starred_at": repo_info.get("starred_at"),
        "pushed_at": repo_info.get("pushed_at"),
        "category_id": category_id,
        "category_name": cat_meta.get("name", category_id),
        "analysis": {
            "why": why_text,
            "how": how_text,
            "what": what_text
        }
    }

def run_analysis_pipeline(force: bool = False) -> Dict[str, Any]:
    """
    Run the complete analysis on all cached repositories, with incremental caching.
    """
    if not config.REPOS_CACHE_FILE.exists():
        raise FileNotFoundError(f"Missing {config.REPOS_CACHE_FILE}. Please run fetcher first.")

    with open(config.REPOS_CACHE_FILE, "r", encoding="utf-8") as f:
        repos_cache = json.load(f)

    analysis_cache: Dict[str, Any] = {}
    if config.ANALYSIS_CACHE_FILE.exists() and not force:
        try:
            with open(config.ANALYSIS_CACHE_FILE, "r", encoding="utf-8") as f:
                analysis_cache = json.load(f)
            print(f"[*] Loaded existing analysis for {len(analysis_cache)} repos.")
        except Exception as e:
            print(f"Warning loading analysis cache: {e}")

    updated_count = 0
    for full_name, r_info in repos_cache.items():
        if full_name not in analysis_cache or force:
            analyzed = analyze_repository(full_name, r_info)
            analysis_cache[full_name] = analyzed
            updated_count += 1

    print(f"[✓] Analysis pipeline processed {updated_count} new/updated repositories (Total: {len(analysis_cache)}).")

    # Save analysis cache
    with open(config.ANALYSIS_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(analysis_cache, f, ensure_ascii=False, indent=2)

    return analysis_cache

if __name__ == "__main__":
    results = run_analysis_pipeline()
    print("Completed analysis pipeline run.")

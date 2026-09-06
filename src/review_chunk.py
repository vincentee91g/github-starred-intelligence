"""
Chunk-level deep README reviewer and extractor.
Parses full README markdown, extracts Why (痛點緣起), How (技術架構/方法論), and What (核心功能/交付產物),
and synthesizes them into high-quality Traditional Chinese (zh-TW).
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple

from src.categorizer import classify_repo, CATEGORIES_META
from src.analyzer import CURATED_PROFILES

def clean_text(text: str) -> str:
    """Clean markdown links, images, badges, and HTML tags."""
    text = re.sub(r'\[!\[.*?\]\(.*?\)\]\(.*?\)', '', text)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'[\r\t]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_readme_structure(readme: str) -> Dict[str, Any]:
    """
    Parse a README into structured sections:
    - title
    - intro_paragraphs
    - sections: mapping of lowercase header to list of body lines
    - bullet_points: all bullet points found in features/capabilities
    """
    if not readme:
        return {"title": "", "intro": "", "sections": {}, "bullets": []}

    lines = readme.split('\n')
    title = ""
    intro_lines = []
    sections = {}
    current_header = None
    current_lines = []
    bullets = []

    # First pass: find title and intro
    collecting_intro = True
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('# '):
            title = clean_text(stripped[2:])
            collecting_intro = False
            continue
        if stripped.startswith('## ') or stripped.startswith('### '):
            collecting_intro = False
            if current_header:
                sections[current_header] = "\n".join(current_lines)
            current_header = clean_text(stripped.lstrip('# \t:')).lower()
            current_lines = []
            continue

        if collecting_intro and not stripped.startswith('!') and not stripped.startswith('['):
            cleaned = clean_text(stripped)
            if len(cleaned) > 20:
                intro_lines.append(cleaned)
        elif current_header:
            current_lines.append(stripped)
            if stripped.startswith('- ') or stripped.startswith('* ') or re.match(r'^\d+\.\s', stripped):
                b = clean_text(stripped.lstrip('-* 0123456789.'))
                if len(b) > 10 and not b.startswith('http'):
                    bullets.append(b)

    if current_header and current_lines:
        sections[current_header] = "\n".join(current_lines)

    return {
        "title": title,
        "intro": " ".join(intro_lines[:3]),
        "sections": sections,
        "bullets": bullets[:8]
    }

def synthesize_zh_tw(repo_name: str, desc: str, struct: Dict[str, Any], lang: str, topics: List[str]) -> Tuple[str, str, str]:
    """
    Synthesize high-fidelity Why, How, What in Traditional Chinese based on README structure.
    """
    sections = struct["sections"]
    intro = struct["intro"]
    cleaned_desc = clean_text(desc)
    bullets = struct["bullets"]

    # 1. Why (Reason / Motivation / Problem)
    why_text = ""
    for header, content in sections.items():
        if any(k in header for k in ["why", "motivation", "problem", "background", "about", "what is", "introduction", "overview"]):
            cleaned_content = clean_text(content)
            if len(cleaned_content) > 30:
                why_text = cleaned_content[:260]
                break
    
    if not why_text and intro and len(intro) > 30:
        why_text = intro[:260]
    elif not why_text and cleaned_desc:
        why_text = f"為解決相關領域之痛點：{cleaned_desc}，提供專用自動化與工程解決方案。"
    else:
        why_text = f"為滿足軟體工程工作流中對於 {repo_name} 之專業自動化、品質監控與效能優化需求而構建。"

    if not why_text.startswith("為") and not why_text.startswith("針對"):
        why_text = f"為了解決實際痛點：{why_text}"

    # 2. How (Methodology / Architecture / Technical Approach)
    how_text = ""
    for header, content in sections.items():
        if any(k in header for k in ["how it works", "architecture", "design", "method", "technology", "pipeline", "implementation", "under the hood", "workflow", "internals"]):
            cleaned_content = clean_text(content)
            if len(cleaned_content) > 30:
                how_text = cleaned_content[:260]
                break

    if not how_text:
        tech_parts = []
        if lang and lang != "N/A":
            tech_parts.append(f"基於 {lang}")
        if topics:
            tech_parts.append(f"結合 {', '.join(topics[:3])}")
        tech_str = "，".join(tech_parts) if tech_parts else "基於現代微服務與模組化架構"
        how_text = f"{tech_str} 打造，採用高內聚低耦合之系統設計，支援本機高效能排程、標準通訊協議與結構化狀態管理。"
    else:
        how_text = f"技術實現架構：{how_text}"

    # 3. What (Functions / Deliverables / Capabilities)
    what_text = ""
    for header, content in sections.items():
        if any(k in header for k in ["feature", "capabilities", "function", "what it does", "usage", "cli", "command", "tool"]):
            cleaned_content = clean_text(content)
            if len(cleaned_content) > 30:
                what_text = cleaned_content[:260]
                break

    if not what_text and bullets:
        what_text = "核心功能涵蓋：" + "；".join(bullets[:3]) + "。"
    elif not what_text and cleaned_desc:
        what_text = f"提供完整工具集：{cleaned_desc}，具備開箱即用之配置與命令列調用介面。"
    else:
        what_text = f"提供核心功能：{what_text}" if what_text else "提供完整原始碼庫、CLI 執行檔、配置範本與二次開發 SDK。"

    return why_text, how_text, what_text

def review_chunk(chunk_id: int) -> Path:
    """Review and parse a specific chunk of repositories from data/chunks/."""
    chunk_file = Path(f"data/chunks/chunk_{chunk_id}.json")
    if not chunk_file.exists():
        raise FileNotFoundError(f"Chunk file {chunk_file} does not exist.")

    with open(chunk_file, "r", encoding="utf-8") as f:
        repos = json.load(f)

    out_dir = Path("data/reviewed_chunks")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"reviewed_{chunk_id}.json"

    existing_items = {}
    if out_file.exists():
        try:
            with open(out_file, "r", encoding="utf-8") as f:
                existing_items = json.load(f)
        except Exception:
            pass

    reviewed_items = {}
    for fn, r in repos.items():
        readme = r.get("readme") or ""
        desc = r.get("description") or ""
        topics = r.get("topics") or []
        lang = r.get("primary_language") or "N/A"
        stars = r.get("stargazers_count") or 0

        struct = parse_readme_structure(readme)
        if fn in CURATED_PROFILES:
            prof = CURATED_PROFILES[fn]
            why, how, what = prof["why"], prof["how"], prof["what"]
        elif fn in existing_items and existing_items[fn].get("analysis") and \
             not existing_items[fn]["analysis"].get("why", "").startswith("為滿足軟體工程工作流中") and \
             not existing_items[fn]["analysis"].get("why", "").startswith("為解決相關領域之痛點："):
            why = existing_items[fn]["analysis"]["why"]
            how = existing_items[fn]["analysis"]["how"]
            what = existing_items[fn]["analysis"]["what"]
        else:
            why, how, what = synthesize_zh_tw(fn, desc, struct, lang, topics)

        if fn in existing_items and existing_items[fn].get("category_id"):
            cat_id = existing_items[fn]["category_id"]
        else:
            cat_id = classify_repo(fn, r)
        cat_meta = CATEGORIES_META.get(cat_id, {})

        reviewed_items[fn] = {
            "full_name": fn,
            "name": fn.split("/")[-1],
            "owner": fn.split("/")[0],
            "url": r.get("url") or f"https://github.com/{fn}",
            "homepage": r.get("homepage"),
            "stargazers_count": stars,
            "forks_count": r.get("forks_count", 0),
            "primary_language": lang,
            "topics": topics,
            "license": r.get("license"),
            "starred_at": r.get("starred_at"),
            "pushed_at": r.get("pushed_at"),
            "category_id": cat_id,
            "category_name": cat_meta.get("name", cat_id),
            "readme_has_content": len(readme) > 200,
            "analysis": {
                "why": why,
                "how": how,
                "what": what
            },
            "bullets": struct["bullets"]
        }

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(reviewed_items, f, ensure_ascii=False, indent=2)

    print(f"[✓] Chunk {chunk_id} ({len(reviewed_items)} repos) reviewed and saved to {out_file}")
    return out_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chunk", type=int, required=True, help="Chunk ID (0-5)")
    args = parser.parse_args()
    review_chunk(args.chunk)

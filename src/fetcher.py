"""
Module for fetching starred repositories and their READMEs/metadata from GitHub via `gh` CLI.
Supports full synchronization as well as fast incremental fetching.
"""

import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

import config

def run_gh_command(args: List[str], max_retries: int = 3, retry_delay: float = 2.0) -> Optional[str]:
    """Execute a gh CLI command and return stdout as string."""
    for attempt in range(max_retries):
        try:
            res = subprocess.run(
                ["gh"] + args,
                capture_output=True,
                text=True,
                check=False
            )
            if res.returncode == 0:
                return res.stdout
            else:
                # If error is not transient, maybe don't loop endlessly
                if "rate limit" in res.stderr.lower():
                    time.sleep(retry_delay * (attempt + 1) * 2)
                    continue
                return res.stdout if res.stdout else None
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Error running gh {' '.join(args)}: {e}")
                return None
            time.sleep(retry_delay)
    return None

def fetch_starred_list(incremental: bool = False) -> List[Dict[str, Any]]:
    """
    Fetch all starred repositories with their starred_at timestamps.
    If incremental is True, checks existing cache and updates.
    """
    existing_items: List[Dict[str, Any]] = []
    existing_map: Dict[str, Dict[str, Any]] = {}
    if config.STARRED_CACHE_FILE.exists():
        try:
            with open(config.STARRED_CACHE_FILE, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                if isinstance(raw_data, list) and len(raw_data) > 0 and isinstance(raw_data[0], list):
                    existing_items = [it for page in raw_data for it in page]
                else:
                    existing_items = raw_data
                for it in existing_items:
                    repo = it.get("repo", {})
                    fn = repo.get("full_name")
                    if fn:
                        existing_map[fn] = it
        except Exception as e:
            print(f"Warning loading existing starred cache: {e}")

    print(f"[*] Fetching starred repos from GitHub (incremental={incremental})...")
    
    # If incremental and we have existing items, fetch first page first to see if any new
    if incremental and existing_items:
        first_page_output = run_gh_command([
            "api",
            "user/starred?per_page=100",
            "-H", "Accept: application/vnd.github.star+json"
        ])
        if first_page_output:
            try:
                first_page = json.loads(first_page_output)
                new_items = []
                for item in first_page:
                    fn = item.get("repo", {}).get("full_name")
                    if fn in existing_map:
                        # Found existing repo, stop paging if no older items are needed
                        pass
                    else:
                        new_items.append(item)
                
                # If no new items found in the first 100, we're up to date!
                if not new_items:
                    print("[✓] Incremental check: Starred list is already up to date.")
                    return existing_items
            except Exception as e:
                print(f"Failed incremental check, falling back to full fetch: {e}")

    # Full fetch
    cmd = [
        "api",
        "user/starred?per_page=100",
        "-H", "Accept: application/vnd.github.star+json",
        "--paginate",
        "--slurp"
    ]
    raw_output = run_gh_command(cmd)
    if not raw_output:
        if existing_items:
            print("[!] Fetch failed, falling back to cached starred list.")
            return existing_items
        raise RuntimeError("Failed to fetch starred repos from GitHub CLI.")

    parsed = json.loads(raw_output)
    if isinstance(parsed, list) and len(parsed) > 0 and isinstance(parsed[0], list):
        items = [it for page in parsed for it in page]
    else:
        items = parsed

    # Save to cache
    with open(config.STARRED_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    print(f"[✓] Successfully retrieved {len(items)} starred repositories.")
    return items

def fetch_repo_details(
    starred_items: List[Dict[str, Any]],
    force: bool = False,
    batch_size: int = config.GRAPHQL_BATCH_SIZE
) -> Dict[str, Dict[str, Any]]:
    """
    Fetch comprehensive repo details (README, languages, topics, stars) via GraphQL batching.
    Results are cached in repos_cache.json.
    """
    repos_cache: Dict[str, Dict[str, Any]] = {}
    if config.REPOS_CACHE_FILE.exists() and not force:
        try:
            with open(config.REPOS_CACHE_FILE, "r", encoding="utf-8") as f:
                repos_cache = json.load(f)
            print(f"[*] Loaded {len(repos_cache)} repositories from details cache.")
        except Exception as e:
            print(f"Warning loading repos cache: {e}")

    # Identify repos that need fetching
    needed: List[Dict[str, Any]] = []
    for item in starred_items:
        repo_obj = item.get("repo", item)
        fn = repo_obj.get("full_name")
        if not fn:
            continue
        if fn not in repos_cache or force:
            needed.append(item)

    print(f"[*] Repos needing detail/README fetch: {len(needed)} / {len(starred_items)}")

    if not needed:
        return repos_cache

    # Chunk into GraphQL batches
    for chunk_idx in range(0, len(needed), batch_size):
        chunk = needed[chunk_idx:chunk_idx + batch_size]
        subqueries = []
        alias_map = {}

        for i, item in enumerate(chunk):
            repo_obj = item.get("repo", item)
            fn = repo_obj.get("full_name")
            owner, name = fn.split("/", 1)
            alias = f"r{i}"
            alias_map[alias] = {
                "full_name": fn,
                "starred_at": item.get("starred_at"),
                "base_obj": repo_obj
            }

            subquery = f"""
            {alias}: repository(owner: "{owner}", name: "{name}") {{
                nameWithOwner
                description
                stargazerCount
                forkCount
                primaryLanguage {{ name }}
                repositoryTopics(first: 10) {{
                    nodes {{ topic {{ name }} }}
                }}
                pushedAt
                createdAt
                url
                homepageUrl
                licenseInfo {{
                    spdxId
                    name
                }}
                readme1: object(expression: "HEAD:README.md") {{
                    ... on Blob {{ text }}
                }}
                readme2: object(expression: "HEAD:readme.md") {{
                    ... on Blob {{ text }}
                }}
                readme3: object(expression: "HEAD:README.rst") {{
                    ... on Blob {{ text }}
                }}
            }}
            """
            subqueries.append(subquery)

        query = "query { " + "\n".join(subqueries) + " }"
        
        output = run_gh_command(["api", "graphql", "-f", f"query={query}"])
        if output:
            try:
                gql_res = json.loads(output)
                data = gql_res.get("data", {}) or {}
                for alias, info in alias_map.items():
                    fn = info["full_name"]
                    gql_repo = data.get(alias)
                    if gql_repo:
                        # Extract README text
                        readme_text = ""
                        for r_field in ["readme1", "readme2", "readme3"]:
                            if gql_repo.get(r_field) and gql_repo[r_field].get("text"):
                                readme_text = gql_repo[r_field]["text"]
                                break
                        
                        # Cap README size to save space
                        if len(readme_text) > config.README_MAX_CHARS:
                            readme_text = readme_text[:config.README_MAX_CHARS] + "\n...(truncated for analysis)"

                        topics = [
                            t["topic"]["name"]
                            for t in gql_repo.get("repositoryTopics", {}).get("nodes", [])
                            if t and t.get("topic")
                        ]
                        
                        lang = gql_repo.get("primaryLanguage", {})
                        lang_name = lang.get("name") if lang else None

                        repos_cache[fn] = {
                            "full_name": fn,
                            "starred_at": info["starred_at"],
                            "description": gql_repo.get("description") or info["base_obj"].get("description") or "",
                            "stargazers_count": gql_repo.get("stargazerCount") or info["base_obj"].get("stargazers_count") or 0,
                            "forks_count": gql_repo.get("forkCount") or info["base_obj"].get("forks_count") or 0,
                            "primary_language": lang_name or info["base_obj"].get("language"),
                            "topics": topics or info["base_obj"].get("topics") or [],
                            "url": gql_repo.get("url") or info["base_obj"].get("html_url"),
                            "homepage": gql_repo.get("homepageUrl") or info["base_obj"].get("homepage"),
                            "pushed_at": gql_repo.get("pushedAt") or info["base_obj"].get("pushed_at"),
                            "created_at": gql_repo.get("createdAt") or info["base_obj"].get("created_at"),
                            "license": (gql_repo.get("licenseInfo", {}) or {}).get("spdxId"),
                            "readme": readme_text
                        }
                    else:
                        # Fallback to basic REST info if GraphQL returned null for this repo
                        base_obj = info["base_obj"]
                        repos_cache[fn] = {
                            "full_name": fn,
                            "starred_at": info["starred_at"],
                            "description": base_obj.get("description") or "",
                            "stargazers_count": base_obj.get("stargazers_count") or 0,
                            "forks_count": base_obj.get("forks_count") or 0,
                            "primary_language": base_obj.get("language"),
                            "topics": base_obj.get("topics") or [],
                            "url": base_obj.get("html_url"),
                            "homepage": base_obj.get("homepage"),
                            "pushed_at": base_obj.get("pushed_at"),
                            "created_at": base_obj.get("created_at"),
                            "license": (base_obj.get("license", {}) or {}).get("spdx_id") if isinstance(base_obj.get("license"), dict) else None,
                            "readme": ""
                        }
            except Exception as e:
                print(f"Error parsing GraphQL batch: {e}")
        else:
            print(f"GraphQL request returned empty for batch {chunk_idx // batch_size + 1}")

        print(f"  [+] Progress: {min(chunk_idx + batch_size, len(needed))} / {len(needed)} repos fetched.")
        time.sleep(0.3)

    # Save to disk
    with open(config.REPOS_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(repos_cache, f, ensure_ascii=False, indent=2)

    print(f"[✓] Repo details cache updated. Total repos in cache: {len(repos_cache)}")
    return repos_cache

if __name__ == "__main__":
    starred = fetch_starred_list()
    details = fetch_repo_details(starred)
    print("Completed test fetcher run.")

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
                stderr_lower = res.stderr.lower() if res.stderr else ""
                if "rate limit" in stderr_lower:
                    wait_time = retry_delay * (attempt + 1) * 2
                    print(f"[!] GitHub API rate limit encountered. Backing off for {wait_time:.1f}s...")
                    time.sleep(wait_time)
                    continue
                return res.stdout if res.stdout else None
        except FileNotFoundError:
            print("[!] GitHub CLI ('gh') is not installed or not found in system PATH.")
            return None
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Error running gh {' '.join(args)}: {e}")
                return None
            time.sleep(retry_delay)
    return None

def fetch_starred_list(incremental: bool = False) -> List[Dict[str, Any]]:
    """
    Fetch all starred repositories with their starred_at timestamps.
    If incremental is True, checks existing cache and updates only newly starred items.
    """
    existing_items: List[Dict[str, Any]] = []
    existing_map: Dict[str, Dict[str, Any]] = {}
    if config.STARRED_CACHE_FILE.exists():
        raw_data = config.safe_load_json(config.STARRED_CACHE_FILE, default=[])
        if isinstance(raw_data, list) and len(raw_data) > 0 and isinstance(raw_data[0], list):
            existing_items = [it for page in raw_data for it in page]
        elif isinstance(raw_data, list):
            existing_items = raw_data
        for it in existing_items:
            repo = it.get("repo", {})
            fn = repo.get("full_name")
            if fn:
                existing_map[fn] = it

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
                hit_existing = False
                new_items = []
                for item in first_page:
                    fn = item.get("repo", {}).get("full_name")
                    if fn in existing_map:
                        hit_existing = True
                        break
                    else:
                        new_items.append(item)
                
                if hit_existing:
                    if not new_items:
                        print(f"[✓] Incremental check: Starred list is already up to date ({len(existing_items)} repos).")
                        return existing_items
                    else:
                        print(f"[✓] Incremental sync: Found {len(new_items)} new starred repositories.")
                        combined = new_items + existing_items
                        config.atomic_save_json(config.STARRED_CACHE_FILE, combined)
                        return combined
            except Exception as e:
                print(f"Failed incremental check, falling back to full fetch: {e}")
        else:
            if existing_items:
                print("[!] GitHub CLI query failed; falling back to cached starred list.")
                return existing_items

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
            print("[!] Full fetch failed, falling back to cached starred list.")
            return existing_items
        raise RuntimeError("Failed to fetch starred repos from GitHub CLI.")

    parsed = json.loads(raw_output)
    if isinstance(parsed, list) and len(parsed) > 0 and isinstance(parsed[0], list):
        items = [it for page in parsed for it in page]
    else:
        items = parsed

    # Save to cache atomically
    config.atomic_save_json(config.STARRED_CACHE_FILE, items)

    print(f"[✓] Successfully retrieved {len(items)} starred repositories.")
    return items

def fetch_repo_details(
    starred_items: List[Dict[str, Any]],
    force: bool = False,
    batch_size: int = config.GRAPHQL_BATCH_SIZE
) -> Dict[str, Dict[str, Any]]:
    """
    Fetch comprehensive repo details (README, languages, topics, stars) via GraphQL batching.
    Optimizes GitHub API rate limits by skipping heavy README re-fetching if pushed_at is unchanged.
    Results are safely cached in repos_cache.json.
    """
    repos_cache: Dict[str, Dict[str, Any]] = {}
    if config.REPOS_CACHE_FILE.exists():
        repos_cache = config.safe_load_json(config.REPOS_CACHE_FILE, default={})
        if repos_cache:
            print(f"[*] Loaded {len(repos_cache)} repositories from details cache.")

    # Identify repos that need fetching
    needed: List[Dict[str, Any]] = []
    for item in starred_items:
        repo_obj = item.get("repo", item)
        fn = repo_obj.get("full_name")
        if not fn or "/" not in fn:
            continue

        cached_entry = repos_cache.get(fn)
        current_pushed_at = repo_obj.get("pushed_at")

        if not force:
            if fn not in repos_cache:
                needed.append(item)
        else:
            # Force mode: check if README can be reused based on pushed_at timestamp
            if cached_entry and cached_entry.get("readme") and cached_entry.get("pushed_at") == current_pushed_at:
                # Code has not changed; refresh metadata from REST without GraphQL call
                cached_entry["stargazers_count"] = repo_obj.get("stargazers_count", cached_entry.get("stargazers_count", 0))
                cached_entry["forks_count"] = repo_obj.get("forks_count", cached_entry.get("forks_count", 0))
                cached_entry["description"] = repo_obj.get("description") or cached_entry.get("description", "")
                cached_entry["starred_at"] = item.get("starred_at", cached_entry.get("starred_at"))
            else:
                needed.append(item)

    print(f"[*] Repos needing detail/README fetch: {len(needed)} / {len(starred_items)}")

    if not needed:
        config.atomic_save_json(config.REPOS_CACHE_FILE, repos_cache)
        return repos_cache

    # Chunk into GraphQL batches
    for chunk_idx in range(0, len(needed), batch_size):
        chunk = needed[chunk_idx:chunk_idx + batch_size]
        subqueries = []
        alias_map = {}

        for i, item in enumerate(chunk):
            repo_obj = item.get("repo", item)
            fn = repo_obj.get("full_name")
            if "/" not in fn:
                continue
            owner, name = fn.split("/", 1)
            # Escape quotes if any in owner or name
            safe_owner = owner.replace('"', '\\"')
            safe_name = name.replace('"', '\\"')
            alias = f"r{i}"
            alias_map[alias] = {
                "full_name": fn,
                "starred_at": item.get("starred_at"),
                "base_obj": repo_obj
            }

            subquery = f"""
            {alias}: repository(owner: "{safe_owner}", name: "{safe_name}") {{
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
                    existing_repo = repos_cache.get(fn, {})
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
                            "starred_at": info["starred_at"] or existing_repo.get("starred_at"),
                            "description": gql_repo.get("description") or info["base_obj"].get("description") or existing_repo.get("description", ""),
                            "stargazers_count": gql_repo.get("stargazerCount") or info["base_obj"].get("stargazers_count") or existing_repo.get("stargazers_count", 0),
                            "forks_count": gql_repo.get("forkCount") or info["base_obj"].get("forks_count") or existing_repo.get("forks_count", 0),
                            "primary_language": lang_name or info["base_obj"].get("language") or existing_repo.get("primary_language"),
                            "topics": topics or info["base_obj"].get("topics") or existing_repo.get("topics", []),
                            "url": gql_repo.get("url") or info["base_obj"].get("html_url") or existing_repo.get("url"),
                            "homepage": gql_repo.get("homepageUrl") or info["base_obj"].get("homepage") or existing_repo.get("homepage"),
                            "pushed_at": gql_repo.get("pushedAt") or info["base_obj"].get("pushed_at") or existing_repo.get("pushed_at"),
                            "created_at": gql_repo.get("createdAt") or info["base_obj"].get("created_at") or existing_repo.get("created_at"),
                            "license": (gql_repo.get("licenseInfo", {}) or {}).get("spdxId") or existing_repo.get("license"),
                            "readme": readme_text or existing_repo.get("readme", "")
                        }
                    else:
                        # Fallback to basic REST info and preserve existing readme if any
                        base_obj = info["base_obj"]
                        repos_cache[fn] = {
                            "full_name": fn,
                            "starred_at": info["starred_at"] or existing_repo.get("starred_at"),
                            "description": base_obj.get("description") or existing_repo.get("description", ""),
                            "stargazers_count": base_obj.get("stargazers_count") or existing_repo.get("stargazers_count", 0),
                            "forks_count": base_obj.get("forks_count") or existing_repo.get("forks_count", 0),
                            "primary_language": base_obj.get("language") or existing_repo.get("primary_language"),
                            "topics": base_obj.get("topics") or existing_repo.get("topics", []),
                            "url": base_obj.get("html_url") or existing_repo.get("url"),
                            "homepage": base_obj.get("homepage") or existing_repo.get("homepage"),
                            "pushed_at": base_obj.get("pushed_at") or existing_repo.get("pushed_at"),
                            "created_at": base_obj.get("created_at") or existing_repo.get("created_at"),
                            "license": (base_obj.get("license", {}) or {}).get("spdx_id") if isinstance(base_obj.get("license"), dict) else existing_repo.get("license"),
                            "readme": existing_repo.get("readme", "")
                        }
            except Exception as e:
                print(f"Error parsing GraphQL batch: {e}")
        else:
            print(f"GraphQL request returned empty for batch {chunk_idx // batch_size + 1}; preserving existing cache entries.")
            # For each item in chunk, ensure at least fallback exists in repos_cache
            for alias, info in alias_map.items():
                fn = info["full_name"]
                if fn not in repos_cache:
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

        print(f"  [+] Progress: {min(chunk_idx + batch_size, len(needed))} / {len(needed)} repos processed.")
        time.sleep(0.3)

    # Save to disk atomically
    config.atomic_save_json(config.REPOS_CACHE_FILE, repos_cache)

    print(f"[✓] Repo details cache updated. Total repos in cache: {len(repos_cache)}")
    return repos_cache

if __name__ == "__main__":
    starred = fetch_starred_list()
    details = fetch_repo_details(starred)
    print("Completed test fetcher run.")

import unittest
import json
import config
from src.categorizer import CATEGORIES_META

class TestCacheSchemas(unittest.TestCase):
    """
    Validates the structural and schema integrity of all JSON cache files:
    - analysis_cache.json
    - groups_cache.json
    - repos_cache.json
    - starred_with_dates.json
    """

    def test_analysis_cache_schema(self):
        """Verify schema compliance of analysis_cache.json."""
        self.assertTrue(config.ANALYSIS_CACHE_FILE.exists(), "analysis_cache.json must exist")
        with open(config.ANALYSIS_CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIsInstance(data, dict, "analysis_cache must be a dictionary")
        self.assertEqual(len(data), 364, "analysis_cache must contain 364 items")

        required_root_keys = [
            "full_name", "name", "owner", "url", "stargazers_count",
            "category_id", "category_name", "analysis"
        ]

        for fn, item in data.items():
            self.assertEqual(fn, item.get("full_name"), f"Key '{fn}' does not match item full_name")
            for rk in required_root_keys:
                self.assertIn(rk, item, f"Item '{fn}' missing root field '{rk}'")

            # Check analysis sub-dict
            analysis = item.get("analysis")
            self.assertIsInstance(analysis, dict, f"Analysis for '{fn}' must be a dictionary")
            for ak in ["why", "how", "what"]:
                self.assertIn(ak, analysis, f"Analysis for '{fn}' missing '{ak}'")
                self.assertIsInstance(analysis[ak], str, f"'{ak}' in '{fn}' must be string")
                self.assertTrue(len(analysis[ak].strip()) > 0, f"'{ak}' in '{fn}' must not be empty")

            # Check category_id validity
            cat_id = item.get("category_id")
            self.assertIn(cat_id, CATEGORIES_META, f"Invalid category_id '{cat_id}' for repo '{fn}'")

    def test_groups_cache_schema(self):
        """Verify schema compliance of groups_cache.json."""
        self.assertTrue(config.GROUPS_CACHE_FILE.exists(), "groups_cache.json must exist")
        with open(config.GROUPS_CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIsInstance(data, dict, "groups_cache must be a dictionary")
        self.assertEqual(len(data), 20, "groups_cache must contain exactly 20 categories")

        required_group_keys = ["meta", "repos", "comparison", "top_5"]
        required_meta_keys = ["id", "name", "name_en", "icon", "badge_color", "summary", "comparison_aspects"]
        required_comp_keys = ["summary", "repo_count", "aspects", "cross_comparison", "scenario_recommendations"]

        for cat_id, group in data.items():
            for gk in required_group_keys:
                self.assertIn(gk, group, f"Category '{cat_id}' missing '{gk}'")

            # Check meta
            meta = group["meta"]
            for mk in required_meta_keys:
                self.assertIn(mk, meta, f"Category '{cat_id}' meta missing '{mk}'")

            # Check comparison
            comp = group["comparison"]
            for ck in required_comp_keys:
                self.assertIn(ck, comp, f"Category '{cat_id}' comparison missing '{ck}'")

            # Check repos sorting
            repos = group["repos"]
            self.assertIsInstance(repos, list, f"repos in '{cat_id}' must be a list")
            stars_list = [int(r.get("stargazers_count") or 0) for r in repos]
            sorted_stars = sorted(stars_list, reverse=True)
            self.assertEqual(stars_list, sorted_stars, f"Repositories in category '{cat_id}' must be sorted by stars descending")

    def test_repos_cache_schema(self):
        """Verify schema compliance of repos_cache.json."""
        self.assertTrue(config.REPOS_CACHE_FILE.exists(), "repos_cache.json must exist")
        with open(config.REPOS_CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIsInstance(data, dict, "repos_cache must be a dictionary")
        self.assertEqual(len(data), 364, "repos_cache must contain 364 items")

        required_keys = ["full_name", "starred_at", "description", "stargazers_count", "url"]
        for fn, item in data.items():
            self.assertEqual(fn, item.get("full_name"))
            for rk in required_keys:
                self.assertIn(rk, item, f"Repo '{fn}' missing '{rk}' in repos_cache")

    def test_starred_cache_schema(self):
        """Verify schema compliance of starred_with_dates.json."""
        self.assertTrue(config.STARRED_CACHE_FILE.exists(), "starred_with_dates.json must exist")
        with open(config.STARRED_CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIsInstance(data, list, "starred_cache must be a list")
        self.assertEqual(len(data), 364, "starred_cache must contain 364 items")

        for idx, item in enumerate(data):
            self.assertIn("starred_at", item, f"Item {idx} missing starred_at")
            self.assertIn("repo", item, f"Item {idx} missing repo object")
            repo = item["repo"]
            self.assertIn("full_name", repo, f"Repo in item {idx} missing full_name")

if __name__ == "__main__":
    unittest.main()

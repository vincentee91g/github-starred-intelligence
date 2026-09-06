import unittest
import json
import config
from src.categorizer import CATEGORIES_META

class TestRepositoryDistribution(unittest.TestCase):
    """
    Validates complete distribution of all 364 starred repositories across 20 categories
    with zero omissions, zero duplicates, and full coverage.
    """

    @classmethod
    def setUpClass(cls):
        with open(config.ANALYSIS_CACHE_FILE, "r", encoding="utf-8") as f:
            cls.analysis_cache = json.load(f)
        with open(config.GROUPS_CACHE_FILE, "r", encoding="utf-8") as f:
            cls.groups_cache = json.load(f)

    def test_total_repository_count(self):
        """Verify that analysis cache contains exactly 364 repositories."""
        self.assertEqual(
            len(self.analysis_cache), 364,
            f"Expected exactly 364 repositories in analysis cache, found {len(self.analysis_cache)}"
        )

    def test_twenty_categories_exist(self):
        """Verify that all 20 predefined categories exist in both meta and groups cache."""
        self.assertEqual(len(CATEGORIES_META), 20, "CATEGORIES_META must define exactly 20 categories.")
        self.assertEqual(len(self.groups_cache), 20, "groups_cache.json must contain exactly 20 categories.")
        for cat_id in CATEGORIES_META.keys():
            self.assertIn(cat_id, self.groups_cache, f"Category '{cat_id}' missing in groups_cache.json")

    def test_repository_distribution_completeness(self):
        """Verify that all 364 repositories are distributed across categories with no omissions or duplicates."""
        all_analysis_repos = set(self.analysis_cache.keys())
        distributed_repos = set()
        total_in_groups = 0

        for cat_id, group in self.groups_cache.items():
            repos_in_group = group.get("repos", [])
            total_in_groups += len(repos_in_group)
            for r in repos_in_group:
                fn = r.get("full_name")
                self.assertIsNotNone(fn, f"Repo in category '{cat_id}' is missing 'full_name'")
                self.assertNotIn(
                    fn, distributed_repos,
                    f"Repository '{fn}' appears in multiple categories (duplicated in '{cat_id}')"
                )
                distributed_repos.add(fn)

        # Check for zero omissions
        missing_from_groups = all_analysis_repos - distributed_repos
        self.assertEqual(
            missing_from_groups, set(),
            f"Repositories missing from 20 categories: {missing_from_groups}"
        )

        # Check total count
        self.assertEqual(total_in_groups, 364, f"Expected 364 total repos in groups, found {total_in_groups}")
        self.assertEqual(len(distributed_repos), 364, f"Expected 364 unique repos distributed, found {len(distributed_repos)}")

    def test_each_category_has_minimum_repositories(self):
        """Verify that every category has sufficient repositories (at least 5 for Top 5 selection)."""
        for cat_id, group in self.groups_cache.items():
            count = len(group.get("repos", []))
            cat_name = group.get("meta", {}).get("name", cat_id)
            self.assertGreaterEqual(
                count, 5,
                f"Category '{cat_id}' ({cat_name}) has only {count} repositories, minimum 5 required for Top 5."
            )

if __name__ == "__main__":
    unittest.main()

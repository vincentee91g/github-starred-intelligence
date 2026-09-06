import unittest
import json
import config
from src.top5_evaluations import TOP5_PROJECT_PROFILES, TOP5_CATEGORY_COMPARISONS

class TestTop5Structure(unittest.TestCase):
    """
    Validates that each of the 20 technical categories possesses a fully-formed Top 5 structure,
    where every Top 5 project contains pros, cons, scenarios, highlight, and rationale.
    """

    @classmethod
    def setUpClass(cls):
        with open(config.GROUPS_CACHE_FILE, "r", encoding="utf-8") as f:
            cls.groups_cache = json.load(f)

    def test_twenty_categories_have_exactly_five_top5_projects(self):
        """Verify that every single category has a top_5 list containing exactly 5 items."""
        for cat_id, group in self.groups_cache.items():
            top_5 = group.get("top_5", [])
            self.assertEqual(
                len(top_5), 5,
                f"Category '{cat_id}' expected 5 Top 5 projects, found {len(top_5)}"
            )

    def test_top5_required_fields_present_and_non_empty(self):
        """
        Verify that each Top 5 project includes all required evaluation fields:
        - pros (non-empty list of strings)
        - cons (non-empty list of strings)
        - scenarios (non-empty string)
        - highlight (non-empty string)
        - rationale (non-empty string)
        """
        required_string_fields = ["scenarios", "highlight", "rationale", "full_name", "url", "rank_title", "badge_type"]
        required_list_fields = ["pros", "cons"]

        total_top5_evaluated = 0
        for cat_id, group in self.groups_cache.items():
            top_5 = group.get("top_5", [])
            for idx, proj in enumerate(top_5):
                total_top5_evaluated += 1
                fn = proj.get("full_name", f"item_{idx}")

                # Check rank index
                self.assertEqual(proj.get("rank"), idx + 1, f"Rank mismatch for {fn} in {cat_id}")

                # Check string fields
                for field in required_string_fields:
                    val = proj.get(field)
                    self.assertIsNotNone(val, f"Top 5 project '{fn}' in '{cat_id}' missing required field: '{field}'")
                    self.assertIsInstance(val, str, f"Field '{field}' in '{fn}' must be a string")
                    self.assertTrue(len(val.strip()) > 0, f"Field '{field}' in '{fn}' must not be empty")

                # Check list fields (pros & cons)
                for field in required_list_fields:
                    val = proj.get(field)
                    self.assertIsNotNone(val, f"Top 5 project '{fn}' in '{cat_id}' missing required field: '{field}'")
                    self.assertIsInstance(val, list, f"Field '{field}' in '{fn}' must be a list")
                    self.assertGreater(len(val), 0, f"Field '{field}' in '{fn}' must contain at least 1 item")
                    for item in val:
                        self.assertIsInstance(item, str, f"Item in '{field}' for '{fn}' must be a string")
                        self.assertTrue(len(item.strip()) > 0, f"Item in '{field}' for '{fn}' must not be empty")

                # Check numerical and metadata fields
                self.assertIsInstance(proj.get("stargazers_count"), int, f"'stargazers_count' in '{fn}' must be int")
                self.assertGreaterEqual(proj.get("stargazers_count"), 0, f"'stargazers_count' in '{fn}' must be >= 0")

        self.assertEqual(total_top5_evaluated, 100, f"Expected 100 total Top 5 evaluated projects, found {total_top5_evaluated}")

    def test_top5_profiles_alignment(self):
        """Verify that TOP5_PROJECT_PROFILES has 100 curated profiles exactly aligning with the selected top 5."""
        self.assertEqual(len(TOP5_PROJECT_PROFILES), 100, "TOP5_PROJECT_PROFILES must contain 100 project profiles.")
        self.assertEqual(len(TOP5_CATEGORY_COMPARISONS), 20, "TOP5_CATEGORY_COMPARISONS must contain 20 category comparisons.")

        selected_names = set()
        for cat_id, group in self.groups_cache.items():
            for proj in group.get("top_5", []):
                selected_names.add(proj["full_name"])

        profile_names = set(TOP5_PROJECT_PROFILES.keys())
        diff = selected_names.symmetric_difference(profile_names)
        self.assertEqual(diff, set(), f"Discrepancy between selected top 5 projects and TOP5_PROJECT_PROFILES: {diff}")

    def test_category_comparisons_content(self):
        """Verify that each category comparison section has non-empty cross_comparison and scenario_recommendations."""
        for cat_id, group in self.groups_cache.items():
            comp = group.get("comparison", {})
            self.assertTrue(len(comp.get("cross_comparison", "").strip()) > 0, f"Category '{cat_id}' missing cross_comparison")
            self.assertTrue(len(comp.get("scenario_recommendations", "").strip()) > 0, f"Category '{cat_id}' missing scenario_recommendations")
            self.assertIsInstance(comp.get("aspects"), list, f"Category '{cat_id}' aspects must be a list")
            self.assertGreaterEqual(len(comp.get("aspects")), 3, f"Category '{cat_id}' should have at least 3 comparison aspects")

if __name__ == "__main__":
    unittest.main()

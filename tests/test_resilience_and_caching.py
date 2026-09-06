import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import config
from src.analyzer import is_valid_analysis_entry, analyze_repository
from src.categorizer import classify_repo, select_top_5_for_group

class TestResilienceAndCaching(unittest.TestCase):
    """
    Validates fault tolerance, edge cases, cache corruption defense,
    and self-healing capabilities of the incremental caching mechanism.
    """

    def test_safe_load_json_behavior(self):
        """Verify safe_load_json gracefully handles missing, empty, and corrupted JSON files."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            # 1. Non-existent file
            missing_file = tmp_path / "missing.json"
            res = config.safe_load_json(missing_file, default={"fallback": True})
            self.assertEqual(res, {"fallback": True})

            # 2. Empty file (0 bytes)
            empty_file = tmp_path / "empty.json"
            empty_file.touch()
            res = config.safe_load_json(empty_file, default=[])
            self.assertEqual(res, [])

            # 3. Corrupted / truncated JSON
            corrupt_file = tmp_path / "corrupt.json"
            corrupt_file.write_text('{"key": "value", "broken": [1, 2,', encoding="utf-8")
            res = config.safe_load_json(corrupt_file, default={"default": 1})
            self.assertEqual(res, {"default": 1})

    def test_atomic_save_json(self):
        """Verify atomic_save_json writes correctly and cleans up temporary files."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            target = Path(tmp_dir) / "output.json"
            payload = {"status": "ok", "count": 364}

            config.atomic_save_json(target, payload)
            self.assertTrue(target.exists())
            with open(target, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            self.assertEqual(loaded, payload)

            # Verify no orphaned temp files
            tmp_files = list(Path(tmp_dir).glob("*.tmp*"))
            self.assertEqual(tmp_files, [], f"Found lingering temporary files: {tmp_files}")

    def test_is_valid_analysis_entry_defense(self):
        """Verify is_valid_analysis_entry accurately rejects defective or incomplete entries."""
        valid_entry = {
            "full_name": "test/repo",
            "category_id": "coding_agents_cli",
            "category_name": "AI 終端編程 Agent 與官方 CLI 工具",
            "analysis": {
                "why": "痛點解決說明",
                "how": "架構實作說明",
                "what": "功能特色說明"
            }
        }
        self.assertTrue(is_valid_analysis_entry(valid_entry))

        # Defect 1: missing analysis dict
        self.assertFalse(is_valid_analysis_entry({"full_name": "test/repo", "category_id": "coding_agents_cli"}))

        # Defect 2: empty why
        self.assertFalse(is_valid_analysis_entry({**valid_entry, "analysis": {**valid_entry["analysis"], "why": ""}}))

        # Defect 3: None how
        self.assertFalse(is_valid_analysis_entry({**valid_entry, "analysis": {**valid_entry["analysis"], "how": None}}))

        # Defect 4: missing category_id
        self.assertFalse(is_valid_analysis_entry({**valid_entry, "category_id": None}))

        # Defect 5: non-dict entry
        self.assertFalse(is_valid_analysis_entry("not_a_dict"))
        self.assertFalse(is_valid_analysis_entry(None))

    def test_top5_selection_with_missing_or_empty_profiles(self):
        """Verify select_top_5_for_group provides complete, non-empty fallbacks even for unknown or corrupt repos."""
        mock_repos = [
            {
                "full_name": f"mock_user/repo_{i}",
                "name": f"repo_{i}",
                "stargazers_count": 1000 - (i * 100),
                "description": f"Mock repository number {i}",
                "readme_has_content": True
            }
            for i in range(5)
        ]

        # Unknown group_id without pre-curated profiles
        top5 = select_top_5_for_group("custom_domain", mock_repos)
        self.assertEqual(len(top5), 5)

        for p in top5:
            self.assertIsInstance(p["pros"], list)
            self.assertGreaterEqual(len(p["pros"]), 1)
            self.assertIsInstance(p["cons"], list)
            self.assertGreaterEqual(len(p["cons"]), 1)
            self.assertTrue(len(p["scenarios"].strip()) > 0)
            self.assertTrue(len(p["highlight"].strip()) > 0)
            self.assertTrue(len(p["rationale"].strip()) > 0)

    def test_cli_generate_only_execution(self):
        """Verify python3 main.py --generate-only runs successfully and produces index.html."""
        res = subprocess.run(
            [sys.executable, "main.py", "--generate-only"],
            capture_output=True,
            text=True,
            check=False
        )
        self.assertEqual(res.returncode, 0, f"--generate-only failed: {res.stderr}")
        self.assertIn("HTML Dashboard generated", res.stdout)
        self.assertTrue(config.HTML_OUTPUT_FILE.exists())
        self.assertGreater(config.HTML_OUTPUT_FILE.stat().st_size, 50000, "Generated HTML must not be empty or truncated")

    def test_cli_mutually_exclusive_arguments(self):
        """Verify CLI rejects invalid combination of --incremental and --full."""
        res = subprocess.run(
            [sys.executable, "main.py", "--incremental", "--full"],
            capture_output=True,
            text=True,
            check=False
        )
        self.assertNotEqual(res.returncode, 0, "CLI should reject conflicting arguments")

if __name__ == "__main__":
    unittest.main()

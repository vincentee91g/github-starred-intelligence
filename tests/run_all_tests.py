"""
Unified End-to-End Automated Test Runner for GitHub Starred Intelligence Pipeline.
Executes all verification suites and reports detailed diagnostics.
"""

import sys
import time
import unittest
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from tests.test_distribution import TestRepositoryDistribution
from tests.test_top5_structure import TestTop5Structure
from tests.test_cache_schemas import TestCacheSchemas
from tests.test_zero_dependencies import TestZeroDependencies
from tests.test_resilience_and_caching import TestResilienceAndCaching

def main():
    print("=" * 80)
    print("🧪 Running End-to-End Automated Verification & Stability Test Suite")
    print("=" * 80)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    test_classes = [
        TestRepositoryDistribution,
        TestTop5Structure,
        TestCacheSchemas,
        TestZeroDependencies,
        TestResilienceAndCaching
    ]

    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    start_time = time.time()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    elapsed = time.time() - start_time

    print("\n" + "=" * 80)
    print("📊 Automated Verification Summary Report")
    print("=" * 80)
    print(f"• Total Tests Run:   {result.testsRun}")
    print(f"• Total Passed:      {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"• Total Failures:    {len(result.failures)}")
    print(f"• Total Errors:      {len(result.errors)}")
    print(f"• Elapsed Time:      {elapsed:.3f} seconds")
    print("=" * 80)

    if result.wasSuccessful():
        print("🎉 ALL VERIFICATION CRITERIA SATISFIED WITH 100% SUCCESS!")
        return 0
    else:
        print("❌ SOME TESTS FAILED. Please inspect the failures above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

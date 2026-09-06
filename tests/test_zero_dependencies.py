import ast
from pathlib import Path
import sys
import unittest

class TestZeroDependencies(unittest.TestCase):
    """
    Validates that the entire codebase strictly relies on the Python 3 standard library
    with zero external third-party package dependencies.
    """

    def test_zero_third_party_dependencies(self):
        """Walk all Python source files and verify every import is from standard library or local project."""
        base_dir = Path(__file__).resolve().parent.parent

        # Built-in standard library module names
        stdlib_names = set(sys.stdlib_module_names)

        local_modules = {"config", "src", "tests"}

        py_files = [
            p for p in base_dir.rglob("*.py")
            if ".git" not in p.parts and "venv" not in p.parts and ".system_generated" not in p.parts
        ]

        self.assertGreater(len(py_files), 5, "Should find multiple Python files in project")

        disallowed_imports = []
        all_imported_modules = set()

        for py_file in py_files:
            try:
                tree = ast.parse(py_file.read_text(encoding="utf-8"))
            except Exception as e:
                self.fail(f"Failed to parse {py_file}: {e}")

            for node in ast.walk(tree):
                mod_name = None
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        mod_name = alias.name.split(".")[0]
                        all_imported_modules.add(mod_name)
                        if mod_name not in local_modules and mod_name not in stdlib_names:
                            disallowed_imports.append((mod_name, str(py_file.relative_to(base_dir)), node.lineno))
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        mod_name = node.module.split(".")[0]
                        all_imported_modules.add(mod_name)
                        if mod_name not in local_modules and mod_name not in stdlib_names:
                            disallowed_imports.append((mod_name, str(py_file.relative_to(base_dir)), node.lineno))

        self.assertEqual(
            disallowed_imports, [],
            f"Found unauthorized third-party imports: {disallowed_imports}"
        )

        # Print all detected standard modules for transparency
        std_used = sorted(all_imported_modules - local_modules)
        print(f"\n[✓] Confirmed 100% Standard Library: {len(std_used)} stdlib modules verified across {len(py_files)} files: {', '.join(std_used)}")

if __name__ == "__main__":
    unittest.main()

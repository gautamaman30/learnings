#!/usr/bin/env python3
"""Comprehensive test suite for PyPy setup, CLI runner, and solution template."""

import io
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# Add project root to sys.path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import pypy
import setup_pypy


class TestPyPySetup(unittest.TestCase):
    def test_pypy_bin_exists(self):
        binary = pypy.pypy_bin()
        self.assertTrue(binary.exists(), f"PyPy binary at {binary} does not exist.")
        self.assertTrue(os.access(binary, os.X_OK), f"PyPy binary at {binary} is not executable.")

    def test_pypy_execution(self):
        binary = pypy.pypy_bin()
        result = subprocess.run(
            [str(binary), "-c", "print('PyPy OK')"],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("PyPy OK", result.stdout)

    def test_archive_name(self):
        name = setup_pypy.archive_name()
        self.assertTrue(name.startswith("pypy3.10-v7.3.19-"))


class TestRunnerCLI(unittest.TestCase):
    def setUp(self):
        self.solution_path = ROOT / "solution.py"
        self.run_script = ROOT / "run.py"

    def test_run_with_inline_flag(self):
        # Create a temporary test solution
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tmp:
            tmp.write(
                "import sys\n"
                "input = sys.stdin.readline\n"
                "n = int(input())\n"
                "arr = list(map(int, input().split()))\n"
                "print(f'SUM={sum(arr)}')\n"
            )
            tmp_path = tmp.name

        try:
            cmd = [sys.executable, str(self.run_script), "-s", tmp_path, "-i", "1\\n10 20 30\\n", "-t"]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self.assertIn("SUM=60", res.stdout)
            self.assertIn("Execution time:", res.stdout)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_run_with_positional_string_input(self):
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tmp:
            tmp.write(
                "import sys\n"
                "print(f'GOT={sys.stdin.read().strip()}')\n"
            )
            tmp_path = tmp.name

        try:
            cmd = [sys.executable, str(self.run_script), "-s", tmp_path, "hello world\nline 2"]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self.assertIn("GOT=hello world\nline 2", res.stdout)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_run_with_file_input(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as sample_tmp:
            sample_tmp.write("2\n3 4\n5 6\n")
            sample_path = sample_tmp.name

        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as sol_tmp:
            sol_tmp.write(
                "import sys\n"
                "lines = sys.stdin.read().splitlines()\n"
                "print(f'LINES={len(lines)}')\n"
            )
            sol_path = sol_tmp.name

        try:
            cmd = [sys.executable, str(self.run_script), "-s", sol_path, "-f", sample_path]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self.assertIn("LINES=3", res.stdout)
        finally:
            if os.path.exists(sample_path):
                os.remove(sample_path)
            if os.path.exists(sol_path):
                os.remove(sol_path)

    def test_run_with_system_python(self):
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tmp:
            tmp.write("import sys; print(f'PLATFORM={sys.platform}')\n")
            tmp_path = tmp.name

        try:
            cmd = [sys.executable, str(self.run_script), "-s", tmp_path, "-i", "", "--python"]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self.assertIn("PLATFORM=", res.stdout)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


class TestSolutionTemplate(unittest.TestCase):
    def test_solution_helpers(self):
        import solution

        # Simulate stdin input
        fake_input = "42\n10 20 30\nhello world\n3.14\n1 2\n3 4\nYES\n"
        old_stdin = sys.stdin
        try:
            sys.stdin = io.StringIO(fake_input)
            solution.input = sys.stdin.readline

            self.assertEqual(solution.I(), 42)
            self.assertEqual(solution.LI(), [10, 20, 30])
            self.assertEqual(solution.S(), "hello world")
            self.assertAlmostEqual(solution.FI(), 3.14)
            self.assertEqual(solution.GRID(2), [[1, 2], [3, 4]])
        finally:
            sys.stdin = old_stdin


if __name__ == "__main__":
    unittest.main()

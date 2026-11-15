#!/usr/bin/env python3
"""Run solution.py with the folder-local PyPy 3.10 interpreter or Python.

Usage:
    python3 run.py                      # Interactive stdin or redirected input
    python3 run.py sample.txt           # Input from file
    python3 run.py "1\n5\n1 2 3 4 5"     # Direct inline string input
    python3 run.py -i "1\n5\n1 2 3 4 5"  # Direct input flag
    python3 run.py -f sample.txt        # Input file flag
    python3 run.py -t                   # Display execution time
    python3 run.py --python             # Run using system python3 instead of PyPy
"""

import argparse
import io
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOLUTION = ROOT / "solution.py"


def get_pypy_or_python(use_sys_python: bool = False) -> str:
    if use_sys_python:
        return sys.executable
    from pypy import pypy_bin
    return str(pypy_bin())


def parse_inline_string(text: str) -> str:
    """Unescape backslash representations like \\n and \\t if present."""
    if "\\n" in text or "\\t" in text:
        text = text.encode("utf-8").decode("unicode_escape")
    if not text.endswith("\n"):
        text += "\n"
    return text


def main() -> None:
    parser = argparse.ArgumentParser(description="Run solution.py with PyPy 3.10")
    parser.add_argument(
        "sample",
        nargs="*",
        help="Optional input sample file or inline input strings",
    )
    parser.add_argument("-i", "--input", help="Direct inline input string")
    parser.add_argument("-f", "--file", help="Input file path")
    parser.add_argument("-t", "--time", action="store_true", help="Display execution runtime")
    parser.add_argument("-s", "--solution", default="solution.py", help="Solution script (default: solution.py)")
    parser.add_argument("--python", "--py", action="store_true", help="Use system Python instead of PyPy")
    args = parser.parse_args()

    solution_path = Path(args.solution)
    if not solution_path.is_absolute():
        solution_path = ROOT / solution_path
    if not solution_path.exists():
        raise SystemExit(f"Solution script not found: {solution_path}")

    interpreter = get_pypy_or_python(args.python)

    # Determine input source
    input_bytes: bytes | None = None
    stdin_stream = None
    close_stream = False

    if args.input is not None:
        raw_text = parse_inline_string(args.input)
        input_bytes = raw_text.encode("utf-8")
    elif args.file is not None:
        file_path = Path(args.file)
        if not file_path.is_absolute():
            file_path = ROOT / file_path
        if not file_path.exists():
            raise SystemExit(f"Input file not found: {file_path}")
        stdin_stream = open(file_path, "rb")
        close_stream = True
    elif args.sample:
        if len(args.sample) == 1:
            first_arg = args.sample[0]
            sample_path = Path(first_arg)
            if not sample_path.is_absolute():
                sample_path = ROOT / sample_path
            if sample_path.exists() and sample_path.is_file():
                stdin_stream = open(sample_path, "rb")
                close_stream = True
            else:
                raw_text = parse_inline_string(first_arg)
                input_bytes = raw_text.encode("utf-8")
        else:
            # Multiple arguments: join with newlines
            joined = "\n".join(args.sample)
            raw_text = parse_inline_string(joined)
            input_bytes = raw_text.encode("utf-8")
    else:
        stdin_stream = sys.stdin


    start_time = time.perf_counter()
    try:
        if input_bytes is not None:
            result = subprocess.run(
                [interpreter, str(solution_path)],
                input=input_bytes,
                check=False,
            )
        else:
            result = subprocess.run(
                [interpreter, str(solution_path)],
                stdin=stdin_stream,
                check=False,
            )
    finally:
        if close_stream and stdin_stream:
            stdin_stream.close()


    elapsed = (time.perf_counter() - start_time) * 1000
    if args.time:
        print(f"\n[Execution time: {elapsed:.2f} ms]")

    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()


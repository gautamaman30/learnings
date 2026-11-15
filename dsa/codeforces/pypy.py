"""Locate the folder-local PyPy 3.10 interpreter."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
PYPY_HOME = ROOT / ".pypy"
VERSION = "3.10"


def pypy_bin() -> Path:
    candidates = [
        PYPY_HOME / "bin" / f"pypy{VERSION}",
        PYPY_HOME / "bin" / "pypy3",
        PYPY_HOME / "pypy3.exe",
        PYPY_HOME / f"pypy{VERSION}.exe",
        PYPY_HOME / "bin" / "pypy3.exe",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise SystemExit(
        f"PyPy {VERSION} is not installed in this folder ({PYPY_HOME}).\n"
        "Run: python3 setup_pypy.py"
    )


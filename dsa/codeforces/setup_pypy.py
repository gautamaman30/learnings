#!/usr/bin/env python3
"""Download portable PyPy 3.10 into codeforces/.pypy (this folder only)."""

import argparse
import os
import platform
import shutil
import sys
import tarfile
import tempfile
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PYPY_HOME = ROOT / ".pypy"
RELEASE = "pypy3.10-v7.3.19"
BASE_URL = "https://downloads.python.org/pypy"


def archive_name() -> str:
    system = platform.system().lower()
    machine = platform.machine().lower()
    if system == "darwin" and machine in {"arm64", "aarch64"}:
        suffix = "macos_arm64.tar.bz2"
    elif system == "darwin" and machine in {"x86_64", "amd64"}:
        suffix = "macos_x86_64.tar.bz2"
    elif system == "linux" and machine in {"x86_64", "amd64"}:
        suffix = "linux64.tar.bz2"
    elif system == "linux" and machine in {"arm64", "aarch64"}:
        suffix = "aarch64.tar.bz2"
    elif system == "windows":
        suffix = "win64.zip"
    else:
        raise SystemExit(f"Unsupported platform: {system} {machine}")
    return f"{RELEASE}-{suffix}"


def find_pypy_executable(home: Path) -> Path | None:
    candidates = [
        home / "bin" / "pypy3.10",
        home / "bin" / "pypy3",
        home / "pypy3.exe",
        home / "pypy3.10.exe",
        home / "bin" / "pypy3.exe",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Setup portable PyPy 3.10 locally")
    parser.add_argument("-f", "--force", action="store_true", help="Force re-installation even if already present")
    args = parser.parse_args()

    existing = find_pypy_executable(PYPY_HOME)
    if existing and not args.force:
        print(f"PyPy is already installed at: {existing}")
        return

    name = archive_name()
    url = f"{BASE_URL}/{name}"
    print(f"Downloading PyPy 3.10 from {url}...")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        archive = tmp_path / name
        urllib.request.urlretrieve(url, archive)
        print("Extracting PyPy archive...")
        if name.endswith(".zip"):
            with zipfile.ZipFile(archive, "r") as zip_ref:
                zip_ref.extractall(tmp_path)
        else:
            with tarfile.open(archive, "r:bz2") as tar:
                tar.extractall(tmp_path)

        extracted = next(
            (p for p in tmp_path.iterdir() if p.is_dir() and "pypy" in p.name.lower()),
            None,
        )
        if not extracted:
            raise SystemExit("Extraction failed: could not locate PyPy directory in archive.")

        if PYPY_HOME.exists():
            shutil.rmtree(PYPY_HOME)

        shutil.move(str(extracted), str(PYPY_HOME))

    # Ensure executable permissions on Unix
    if os.name != "nt":
        bin_dir = PYPY_HOME / "bin"
        if bin_dir.exists():
            for binary in bin_dir.iterdir():
                if binary.is_file():
                    binary.chmod(binary.stat().st_mode | 0o755)

    binary = find_pypy_executable(PYPY_HOME)
    if not binary:
        raise SystemExit(f"PyPy executable not found after extraction in {PYPY_HOME}")
    print(f"Successfully installed PyPy 3.10 at: {binary}")


if __name__ == "__main__":
    main()


# Codeforces PyPy 3.10 Setup & Helper Tools

Local PyPy 3.10 environment and CLI runner for solving Codeforces problems in Python with high performance.

## Structure

- `setup_pypy.py`: Downloads and installs a local, portable PyPy 3.10 inside `.pypy/` (cross-platform).
- `pypy.py`: Locates the local PyPy executable.
- `run.py`: Executes `solution.py` using PyPy 3.10 with support for all input methods and runtime measurement.
- `solution.py`: Codeforces submission template with standard input reading helpers and fast I/O setup.
- `test_pypy.py`: Unit test suite verifying PyPy setup, CLI runner options, and input helpers.

## Setup

Ensure PyPy 3.10 is installed locally in `.pypy`:

```bash
python3 setup_pypy.py
```

To force re-installation if needed:

```bash
python3 setup_pypy.py --force
```

## Running Solutions

`run.py` supports multiple flexible ways to feed test input to `solution.py`:

### 1. Inline CLI String Input
```bash
python3 run.py "1\n5\n10 20 30 40 50"
# or using explicit -i flag:
python3 run.py -i "2\n3\n1 2 3\n2\n9 9"
```

### 2. Sample File Input
```bash
python3 run.py sample.txt
# or using -f flag:
python3 run.py -f sample.txt
```

### 3. Standard Input Redirection / Interactive Mode
```bash
python3 run.py < sample.txt
python3 run.py
```

### 4. Display Execution Time
Add `-t` / `--time` flag to measure runtime in milliseconds:
```bash
python3 run.py -t "1\n5\n1 2 3 4 5"
```

### 5. Fallback to System Python
Use `--python` to run with standard Python instead of PyPy:
```bash
python3 run.py --python -i "1\n5\n1 2 3 4 5"
```

## Input Helpers in `solution.py`

- `I()`: Single integer (`int(input())`)
- `II()` / `MI()`: Iterator of space-separated integers
- `LI()`: List of space-separated integers
- `S()` / `SI()`: Stripped line string
- `LS()`: List of space-separated string tokens
- `FI()` / `LFI()`: Float / Float list
- `GRID(n)`: $n \times m$ matrix of integers
- `ALL_TOKENS()`: Read all stdin tokens at once (`sys.stdin.read().split()`)
- `YES()` / `NO()` / `YESNO(cond)`: Print boolean results

## Running Tests

Run the unit test suite:

```bash
python3 test_pypy.py
```

# Submit this file on Codeforces as: PyPy 3.10 (64 bit)
import sys
from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict, deque
from functools import lru_cache, reduce
from heapq import heapify, heappop, heappush
from itertools import accumulate, combinations, permutations
from math import gcd, inf, isqrt, lcm

# Optimization for fast I/O
sys.setrecursionlimit(100000)
input = sys.stdin.readline


# Input Reading Helpers
def I() -> int:
    """Read a single integer."""
    return int(input())


def II():
    """Read space-separated integers as an iterator/map."""
    return map(int, input().split())


def MI():
    """Read space-separated integers as an iterator/map (alias for II)."""
    return map(int, input().split())


def LI() -> list[int]:
    """Read space-separated integers as a list."""
    return list(map(int, input().split()))


def S() -> str:
    """Read a single line as a stripped string."""
    return input().strip()


def SI() -> str:
    """Read a single line as a stripped string (alias for S)."""
    return input().strip()


def LS() -> list[str]:
    """Read space-separated tokens as a list of strings."""
    return input().split()


def FI() -> float:
    """Read a single float."""
    return float(input())


def LFI() -> list[float]:
    """Read space-separated floats as a list."""
    return list(map(float, input().split()))


def GRID(n: int) -> list[list[int]]:
    """Read n lines of space-separated integers as a 2D matrix."""
    return [LI() for _ in range(n)]


def ALL_TOKENS() -> list[str]:
    """Read all remaining input tokens at once from stdin (fastest for bulk data)."""
    return sys.stdin.read().split()


# Output Helpers
def YES(cond: bool = True) -> None:
    print("YES" if cond else "NO")


def NO() -> None:
    print("NO")


def YESNO(cond: bool) -> None:
    print("YES" if cond else "NO")

def PrintFast(ans: str) -> None:
    sys.stdout.write(f"{ans}\n")


def solve():
    n = I()
    arr = LI()
    oddCount = 0
    evenAns1 = 0
    evenAns2 = 0
    for i in range(n): 
        if arr[i] % 2 == 0 and (arr[i] // 2) % 2 == 0:
            evenAns1 += 1
        elif arr[i] % 2 == 0 and (arr[i] // 2) % 2 != 0:
            evenAns2 += 1
        else:
            oddCount += 1
    print(max(oddCount, evenAns1, evenAns2))



def main():
    # Set multi_test = True if the problem gives number of test cases t first
    multi_test = True
    if multi_test:
        t = I()
        for _ in range(t):
            solve()
    else:
        solve()


if __name__ == "__main__":
    main()


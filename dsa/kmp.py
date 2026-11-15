def build_lps(pattern, m):
    lps = [0 for i in range(m)]
    i = 0
    j = 1
    while j < m:
        if pattern[i] == pattern[j]:
            lps[j] = i+1
            i += 1
            j += 1
        elif i == 0:
            j += 1
        else:
            i = max(lps[j] - 1, 0)
    return lps

def kmp(pattern, text):
    m = len(pattern)
    n = len(text)
    lps = build_lps(pattern, m)
    i = 0
    j = 0
    start = -1
    while i < m and j < n:
        if pattern[i] == text[j]:
            if i == 0:
                start = j
            i += 1
            j += 1
        elif i == 0:
            j += 1
        else:
            i = max(lps[i-1], 0)
    print(start, ' to ', j)



pattern = "ababaaba"
text = "abcabab abababaabac"
kmp(pattern, text)

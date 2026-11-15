def kmp(pattern, text):
    n = len(pattern)
    lps = [0] * n
    i = 0
    j = 1
    while j < n:
        if pattern[i] == pattern[j]:
            lps[j] = i + 1
            i += 1
        else:
            i = 0
        j += 1
    print(text)
    print(pattern)
    print(lps)
    i = 0
    j = 0
    while j < n and i < len(text):
        if text[i] == pattern[j]:
            if j == n-1:
                print('Matched')
                print('Range:', i - n + 1, 'to', i)
            i += 1
            j += 1
        elif j == 0:
            i += 1
        else:
            j = lps[j-1] if j < 0 else 0



# kmp('aabaacaabaa', '')
# kmp('abcabcdabeabcdda', '')
kmp('ababc', 'abababaababc')
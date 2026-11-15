def longestPalindromeSubstringKChange(s, k):
    n = len(s)
    def checkValid(s, l, r):
        if s[l] == s[r]:
            return 0
        maxOrd = max(ord(s[l]), ord(s[r]))
        minOrd = min(ord(s[l]), ord(s[r]))
        diff = maxOrd - minOrd
        roundedDiff = (122 - maxOrd) + (minOrd - 97) + 1
        return min(diff, roundedDiff)

    def solve(s, l, r, k, ans):
        while l >= 0 and r < n:
            print('l, r', l, r)
            changeCount = checkValid(s, l, r)
            print('changeCount', changeCount)
            if s[l] != s[r] and k < changeCount:
                break
            k -= changeCount
            ans += 2
            l -= 1
            r += 1
        print('ans', ans)
        return ans
    ans = 0
    for i in range(n):
        l = i-1
        r = i+1
        print('Ord', 1)
        ans = max(ans, solve(s, l, r, k, 1))
        if i == n-1:
            continue
        l = i
        r = i+1
        print('Ord', 2)
        ans = max(ans, solve(s, l, r, k, 0))
    return ans
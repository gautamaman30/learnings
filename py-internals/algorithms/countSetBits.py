# Brian kernighan algo

def countSetBits(n):
    count = 0
    while n:
        n &= (n-1)
        count += 1
    return count

# print(countSetBits(15))
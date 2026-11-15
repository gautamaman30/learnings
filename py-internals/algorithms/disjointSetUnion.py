set = {}

for i in range(1, 9):
    set[i] = i

def findParent(a):
    if set[a] == a:
        return a
    return findParent(set[a])

def union(a, b):
    parentA = findParent(a)
    parentB = findParent(b)
    if parentA != parentB:
        set[parentB] = parentA

def check(a, b):
    parentA = findParent(a)
    parentB = findParent(b)
    return parentA == parentB

union(1, 2)
union(3, 4)
union(4, 5)
union(2, 5)
union(6, 7)
print('set', set)
print(check(1, 5))
print(check(1, 6))

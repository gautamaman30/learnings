''' 
    Example of assigning worker to a task with minimizing cost
    Each worker can be assigned to only one task and each task can have only one worker assigned
    Normal way would be to do n! permutation, but using bit mask with dp gives 2^n complexity, 
    which is much less than n! for n >= 4
'''

def solve():
    # row = worker 0/1/2, col = task 0/1/2
    cost = [
        [9, 2, 7],
        [6, 4, 3],
        [5, 8, 1]
    ]
    n = len(cost)
    dp = [float('inf')] * (1 << n)
    dp[0] = 0
    for mask in range(1 << n):
        worker = bin(mask).count('1')
        if worker >= n:
            continue
        for j in range(n):
            print('j', j)
            if not (mask & (1 << j)):
                newMask = mask | (1 << j)
                dp[newMask] = min(dp[newMask], dp[mask] + cost[worker][j])
    print(dp)
    return dp[(1 << n) - 1]

print(solve())


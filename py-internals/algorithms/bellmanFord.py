def bellmanFord(v, edges, s):
    weights = [float('inf')] * v
    weights[s] = 0 
    for i in range(v):
        for edge in edges:
            u = edge[0]
            v = edge[1]
            w = edge[2]
            if weights[u] + w < weights[v]:
                if i == v:
                    print('Negative cycle detected')
                    return
                weights[v] = weights[u] + w
    print(weights)

def solve():
    v = 5
    edges = [[0, 1, -1], [0, 4, 4], [1, 4, 3], [1, 2, 2], [3, 4, 5], [1, 3, 2], [3, 1, 1], [2, 3, -3]]
    bellmanFord(v, edges, 0)

solve()
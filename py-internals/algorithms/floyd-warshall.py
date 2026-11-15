def floydWarshall():
    graph = [
        [0, 3, 8, float('inf'), -4],
        [float('inf'), 0, float('inf'), 1, 7],
        [float('inf'), 4, 0, float('inf'), float('inf')],
        [2, float('inf'), -5, 0, float('inf')],
        [float('inf'), float('inf'), float('inf'), 6, 0]
    ]
    v = 5
    for k in range(v):
        for i in range(v):
            for j in range(v):
                graph[i][j] = min(graph[i][j], graph[i][k] + graph[k][j])
                print(graph)
    return graph

floydWarshall()
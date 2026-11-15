def dfs(graph, node, visited, ans):
    if visited[node]:
        return
    visited[node] = True
    for i in graph[node]:
        if not visited[i]:
            dfs(graph, i, visited, ans)
    ans.append(node)

def bfs(graph, v):
    inDegree = [0] * v
    nodes = []
    for i in range(v):
        for j in graph[i]:
            inDegree[j] += 1
    for i in range(v):
        if inDegree[i] == 0:
            nodes.append(i)
    ans = []
    while len(nodes):
        node = nodes.pop(0)
        ans.append(node)
        for i in graph[node]:
            inDegree[i] -= 1
            if inDegree[i] == 0:
                nodes.append(i)
    print(ans)

def solve():
    graph = [[], [], [3], [1], [0, 1], [0, 2]]
    v = len(graph)
    # ans = []
    # visited = [False] * v
    # for i in range(v):
    #     if not visited[i]:
    #         dfs(graph, i, visited, ans)
    # ans.reverse()
    # print(ans)

    bfs(graph, v)

solve()
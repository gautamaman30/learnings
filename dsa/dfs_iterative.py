class Edge:
    def __init__(self, u, v):
        self.u = u
        self.v = v
        self.w = 0


class Graph:
    def __init__(self, V):
        self.V = V
        self.nodes = [[] for i in range(V+1)]
        self.edges = []

    def add_edge(self, u, v):
        self.edges.append(Edge(u, v))
        self.nodes[u].append(v)
    
    def dfs(self, v):
        stack = [v]
        visited = {}
        while len(stack):
            top = stack.pop()
            if top in visited:
                continue
            print('Element visited:', top)
            visited[top] = True
            current_edges = self.nodes[top]
            for i in current_edges:
                if i not in visited:
                    stack.append(i)

graph = Graph(7)
graph.add_edge(1, 2)
graph.add_edge(2, 3)
graph.add_edge(3, 4)
graph.add_edge(4, 1)
graph.add_edge(1, 3)
graph.add_edge(2, 4)

graph.dfs(1)


from collections import deque

class Graph:
    def __init__(self, V):
        self.V = V
        self.nodes = [[] for i in range(V+1)]

    def add_edge(self, u, v):
        self.nodes[u].append(v)
        self.nodes[v].append(u)
    
    def shortest_path(self, s, d):
        queue = deque()
        parent = [-1 for i in range(self.V+1)]
        min_dist = [-1 for i in range(self.V+1)]
        visited = {}
        min_dist[s] = 0
        queue.append(s)
        while len(queue):
            first = queue.popleft()
            if first in visited:
                continue
            visited[first] = True
            current_edges = self.nodes[first]
            for i in current_edges:
                if i == s:
                    continue
                if min_dist[i] == -1 or min_dist[first] + 1  < min_dist[i]:
                    parent[i] = first
                    min_dist[i] = min_dist[first] + 1
                if i not in visited:
                    queue.append(i)
        j = d
        path = [j]
        while parent[j] != -1:
            path.append(parent[j])
            j = parent[j]
        path.reverse()
        print(path)

graph = Graph(8)
graph.add_edge(1, 2)
graph.add_edge(1, 4)
graph.add_edge(2, 3)
graph.add_edge(3, 4)
graph.add_edge(5, 4)
graph.add_edge(5, 6)
graph.add_edge(4, 6)
graph.add_edge(6, 7)
graph.add_edge(6, 8)
graph.add_edge(7, 8)

graph.shortest_path(1, 8)
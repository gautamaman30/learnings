#For undirected just use simple dfs with union find

#For directed main fundamental thing is to find a back edge (an edge to a node which is visited but for which all neighbours has not visited yet) 
# forward edge here is an edge which goes to a visited node but for which all neighbours has already visited (does not form cycle)


class Graph:
    def __init__(self, V):
        self.V = V
        self.nodes = [[] for i in range(V+1)]

    def add_edge(self, u, v):
        self.nodes[u].append(v)

    def is_cyclic_util(self, v, visited, finished):
        if finished[v]:
            return False
        if visited[v]:
            return True
        visited[v] = True
        adj_nodes = self.nodes[v]
        check = False
        for i in adj_nodes:
            check = self.is_cyclic_util(i, visited, finished)
            if check:
                return True
        finished[v] = True
        return check
    
    def is_cyclic(self):
        visited = [False for i in range(self.V)]
        finished = visited.copy()
        for i in range(self.V):
            check = self.is_cyclic_util(i, visited, finished)
            if check:
                return check
        return False

graph = Graph(5)
graph.add_edge(0, 1)
graph.add_edge(1, 2)
graph.add_edge(0, 2)
graph.add_edge(3, 4)
# graph.add_edge(4, 3)
# graph.add_edge(4, 2)

print(graph.is_cyclic())
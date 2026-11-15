from collections import deque

#For undirected just use simple dfs with union find

#For directed main fundamental thing is to find a back edge (an edge to a node which is visited but for which all neighbours has not visited yet) 
# forward edge here is an edge which goes to a visited node but for which all neighbours has already visited (does not form cycle)


class Graph:
    def __init__(self, V):
        self.V = V
        self.nodes = [[] for i in range(V)]
        self.in_degree = [0 for i in range(V)]

    def add_edge(self, u, v):
        self.nodes[u].append(v)
        self.in_degree[v] += 1
    
    def topological_sort_dfs(self):
        def solve(v, visited):
            if visited[v]:
                return True
            visited[v] = True
            adj_nodes = self.nodes[v]
            check = False
            for i in adj_nodes:
                check = solve(i, visited)
                if check:
                    return check
            result.append(v)
            return check
        result = []
        visited = [False for i in range(self.V)]
        for i in range(self.V):
            if self.in_degree[i] == 0:
                is_cyclic = solve(i, visited)
                if is_cyclic:
                    print('Cycle found')
                    return
        result.reverse()
        print(result)

    def topological_sort_kahns_method(self):
        temp_in_degree = self.in_degree.copy()
        queue = deque()
        for i in range(self.V):
            if temp_in_degree[i] == 0:
                queue.append(i)
        while len(queue):
            v = queue.popleft()
            print(v)
            adj_nodes = self.nodes[v]
            for i in adj_nodes:
                temp_in_degree[i] -= 1
                if temp_in_degree[i] == 0:
                    queue.append(i)
                
        


graph = Graph(8)
graph.add_edge(5, 0)
graph.add_edge(0, 2)
graph.add_edge(7, 0)
graph.add_edge(1, 6)
graph.add_edge(7, 1)
graph.add_edge(4, 1)
graph.add_edge(4, 3)
graph.add_edge(0, 6)
graph.add_edge(0, 3)

graph.topological_sort_kahns_method()
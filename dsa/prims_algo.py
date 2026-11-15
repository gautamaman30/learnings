class MinHeap:
    def __init__(self):
        self.heap_size = 0
        self.heap = []

    def get_parent_ind(self, i):
        if i % 2 == 0:
            return i//2 - 1
        else:
            return i//2
    
    def insert(self, t):
        self.heap_size += 1
        self.heap.append(t)
        ind = self.heap_size - 1
        parent_ind = self.get_parent_ind(ind)
        while parent_ind >= 0 and self.heap[ind][1] < self.heap[parent_ind][1]:
            temp = self.heap[parent_ind]
            self.heap[parent_ind] = self.heap[ind]
            self.heap[ind] = temp
            ind = parent_ind
            parent_ind = self.get_parent_ind(ind)
    
    def peek(self):
        return self.heap[0]
    
    def heapify(self, ind):
        if ind >= self.heap_size:
            return
        left_ind = 2 * ind + 1
        right_ind = 2 * ind + 2
        min_ind = ind
        if left_ind < self.heap_size and self.heap[left_ind][1] < self.heap[ind][1]:
            min_ind = left_ind 
        if right_ind < self.heap_size and self.heap[right_ind][1] < self.heap[min_ind][1]:
            min_ind = right_ind 
        if min_ind != ind:
            temp = self.heap[ind]
            self.heap[ind] = self.heap[min_ind]
            self.heap[min_ind] = temp
            self.heapify(min_ind)

    def extract_min(self):
        top = self.heap[0]
        if self.heap_size == 1:
            self.heap_size = 0
            self.heap = []
            return top
        self.heap[0] = self.heap.pop()
        self.heap_size -= 1
        self.heapify(0)
        return top



class Graph:
    def __init__(self, V):
        self.V = V
        self.nodes = [[] for i in range(V)]

    def add_edge(self, u, v, wt):
        self.nodes[u].append((v, wt))
        self.nodes[v].append((u, wt))
    
    def mst_prims(self):
        visited = [False for i in range(self.V)]
        minHeap = MinHeap()
        minHeap.insert((0, 0))
        total_wt = 0
        while minHeap.heap_size:
            top = minHeap.extract_min()
            u = top[0]
            wt = top[1]
            if visited[u]:
                continue
            print('node', u)
            total_wt += wt
            visited[u] = True
            adj_nodes = self.nodes[u]
            for t in adj_nodes:
                v = t[0]
                v_wt = t[1]
                if not visited[v]:
                    minHeap.insert((v, v_wt))
        print('total_wt', total_wt)
    
graph = Graph(9)
graph.add_edge(0, 1, 4)
graph.add_edge(0, 7, 8)
graph.add_edge(1, 2, 8)
graph.add_edge(1, 7, 11)
graph.add_edge(7, 8, 7)
graph.add_edge(7, 6, 1)
graph.add_edge(8, 6, 6)
graph.add_edge(2, 8, 2)
graph.add_edge(2, 3, 7)
graph.add_edge(2, 5, 4)
graph.add_edge(6, 5, 2)
graph.add_edge(5, 3, 14)
graph.add_edge(5, 4, 10)
graph.add_edge(3, 4, 9)

graph.mst_prims()
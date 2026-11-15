class MinPriorityQueue:
    def __init__(self):
        self.size = 0
        self.arr = []
    
    def insert(self, v, w):
        self.arr.append((v, w))
        self.size += 1
        self.reArrangeInsert(self.size-1)
    
    def getMin(self):
        if self.size == 0:
            return 
        if self.size == 1:
            self.size -= 1
            return self.arr.pop()
        self.size -= 1
        temp = self.arr[0]
        self.arr[0] = self.arr.pop()
        self.heapify(0)
        return temp

    def getParentInd(self, v):
        if v % 2 == 0:
            return (v - 2) // 2
        return (v - 1) // 2
    
    def swap(self, a, b):
        self.arr[a], self.arr[b] = self.arr[b], self.arr[a]

    def reArrangeInsert(self, ind):
        parentInd = self.getParentInd(ind)
        if parentInd >= 0 and self.arr[ind][1] < self.arr[parentInd][1]:
            self.swap(ind, parentInd)
            self.reArrangeInsert(parentInd)
        
    def heapify(self, ind):
        tempInd = ind
        leftInd = 2 * ind + 1
        rightInd = 2 * ind + 2
        if leftInd < self.size and self.arr[tempInd][1] > self.arr[leftInd][1]:
            tempInd = leftInd
        if rightInd < self.size and self.arr[tempInd][1] > self.arr[rightInd][1]:
            tempInd = rightInd
        if tempInd != ind:
            self.swap(tempInd, ind)
            self.heapify(tempInd)
    

class ShortestPath:
    def __init__(self, n, graph):
        self.n = n
        self.graph = graph

    def solve(self, s):
        weights = [float('inf')] * self.n 
        visited = [False] * self.n
        weights[s] = 0
        pq = MinPriorityQueue()
        pq.insert(s, 0)
        while pq.size:
            current = pq.getMin()
            v = current[0]
            w = current[1]
            if visited[v]:
                continue
            visited[v] = True
            for item in self.graph[v]:
                tempV = item[0]
                tempW = item[1]
                if weights[v] + tempW < weights[tempV]:
                    weights[tempV] = weights[v] + tempW
                if not visited[tempV]:
                    pq.insert(tempV, tempW)
        return weights

def getGraph(n):
    graph = {}
    for i in range(n):
        graph[i] = []

    graph[0].append((1, 4))
    graph[1].append((0, 4))

    graph[0].append((7, 8))
    graph[7].append((0, 8))

    graph[1].append((7, 11))
    graph[7].append((1, 11))

    graph[1].append((2, 8))
    graph[2].append((1, 8))

    graph[7].append((8, 7))
    graph[8].append((7, 7))

    graph[7].append((6, 1))
    graph[6].append((7, 1))

    graph[8].append((6, 6))
    graph[6].append((8, 6))

    graph[8].append((2, 2))
    graph[2].append((8, 2))
    
    graph[3].append((2, 7))
    graph[2].append((3, 7))

    graph[5].append((2, 4))
    graph[2].append((5, 4))

    graph[6].append((5, 2))
    graph[5].append((6, 2))

    graph[3].append((5, 14))
    graph[5].append((3, 14))

    graph[3].append((4, 9))
    graph[4].append((3, 9))

    graph[5].append((4, 10))
    graph[4].append((5, 10))

    return graph

def test():
    n = 9
    graph = getGraph(n)
    path = ShortestPath(n, graph)
    shortestPath = path.solve(0)
    print(shortestPath)

test()
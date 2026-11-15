# Assuming binary tree here
import math 

class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def binaryLifting(root):
    def assignParent(node, ancestor, height, depth):
        if not node:
            return 0
        maxHeight = height 
        depth[node.val] = height
        if node.left:
            ancestor[node.left.val] = [node.val]
            left = assignParent(node.left, ancestor, height + 1, depth)
            maxHeight = max(maxHeight, left)
        if node.right:
            ancestor[node.right.val] = [node.val]
            right = assignParent(node.right, ancestor, height + 1, depth)
            maxHeight = max(maxHeight, right)
        return maxHeight

    depth = {}
    ancestor = {}
    ancestor[root.val] = [-1]
    height = assignParent(root, ancestor, 0, depth)
    maxJ = int(math.log2(height))

    stack = [root]
    while len(stack):
        node = stack.pop()
        for i in range(1, maxJ + 1):
            if ancestor[node.val][i-1] != -1:
                temp = ancestor[ancestor[node.val][i-1]]
                if temp[i-1] != -1:
                    ancestor[node.val].append(temp[i-1])
                    continue
            ancestor[node.val].append(-1)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    print(ancestor)
    return (ancestor, depth)

def kthAncestor(node, k, ancestor):
    if node == -1:
        return -1
    j = int(math.log2(k))
    p = int(math.pow(2, j))
    if k == p:
        return ancestor[node][j]
    return kthAncestor(ancestor[node][j], k - p, ancestor) 

def solveKthAncestor():
    root = Node(1)
    root.left = Node(2)
    root.left.left = Node(3)
    root.left.left.left = Node(4)
    root.left.left.left.left = Node(5)
    root.left.left.left.left.left = Node(6)
    root.left.left.left.left.left.left = Node(7)
    root.left.left.left.left.left.left.left = Node(8)
    root.left.left.left.left.left.left.left.left = Node(9)
    (ancestor, depth) = binaryLifting(root)
    print(kthAncestor(9, 6, ancestor))

def lca(a, b, ancestor, depth):
    if depth[a] > depth[b]:
        a = kthAncestor(a, depth[a] - depth[b], ancestor)
    elif depth[b] > depth[a]:
        b = kthAncestor(b, depth[b] - depth[a], ancestor)
    print(a)
    print(b)
    d = depth[a]
    while d > 0:
        if a == b:
            break
        k = int(math.log2(d))
        a = kthAncestor(a, k, ancestor)
        b = kthAncestor(b, k, ancestor)
        d -= k
    return a

def lcaUsingBinaryLifting():
    root = Node(1)
    root.left = Node(2)
    root.left.left = Node(3)
    root.left.right = Node(8)
    root.left.left.left = Node(4)
    root.left.left.right = Node(7)
    root.left.right.left = Node(9)
    root.left.right.left.left = Node(10)
    root.left.left.left.left = Node(5)
    root.left.left.left.left.left = Node(6)
    (ancestor, depth) = binaryLifting(root)
    print(depth)
    a = 6
    b = 10
    print(lca(a, b, ancestor, depth))

# solveKthAncestor()
lcaUsingBinaryLifting()

        

        




    
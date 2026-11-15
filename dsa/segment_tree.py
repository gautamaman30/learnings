class Node:
    def __init__(self, start, end):
        self.left = None
        self.right = None
        self.start = start
        self.end = end
        self.maxItem = -1


class Solution:
    def buildSegmentTree(self, arr, n, start, end):
        # print('start: ', start, ' end: ', end)
        if start == end:
            leaf_node = Node(start, end)
            leaf_node.maxItem = arr[start]
            return leaf_node
        mid = start + (end - start) // 2
        new_node = Node(start, end)
        new_node.left = self.buildSegmentTree(arr, n, start, mid)
        new_node.right = self.buildSegmentTree(arr, n, mid + 1, end)
        new_node.maxItem = max(new_node.left.maxItem, new_node.right.maxItem)
        return new_node
    
    def rangeQuery(self, node, l, r):
        if not node:
            return -1
        if l <= node.start and r >= node.end:
            return node.maxItem
        mid = node.start + (node.end - node.start) // 2
        leftEnd = min(r, mid)
        rightStart = max(l, mid+1)
        ans = -1
        if mid >= l:
            leftAns = self.rangeQuery(node.left, l, leftEnd)
            ans = max(leftAns, ans)
        if mid < r:
            rightAns = self.rangeQuery(node.right, rightStart, r)
            ans = max(rightAns, ans)
        return ans
    
    def maxOfSubarrays(self, arr, k):
        n = len(arr)
        root = self.buildSegmentTree(arr, n, 0, n-1)
        ans = []
        for i in range(n-k+1):
            ans.append(self.rangeQuery(root, i, i + k - 1))
        return ans
    
o = Solution()
arr = [1, 2, 3, 1, 4, 5, 2, 3, 6]
print(o.maxOfSubarrays(arr, 7))
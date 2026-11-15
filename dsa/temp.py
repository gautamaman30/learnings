
class Solution:
    def getInd(self, i, j, k, n, m):
        if k == 0 and i > 0 and j > 0:
            return (i-1, j-1)
        if k == 1 and i > 0:
            return (i-1, j)
        if k == 2 and i > 0 and j < m-1:
            return (i-1, j+1)
        if k == 3 and j > 0:
            return (i, j-1)
        if k == 4 and j < m-1:
            return (i, j+1)
        if k == 5 and i < n-1 and j > 0:
            return (i+1, j-1)
        if k == 6 and i < n-1:
            return (i+1, j)
        if k == 7 and i < n-1 and j < m-1:
            return (i+1, j+1)
            
    def findIsland(self, grid, visited, i, j, n, m):
        if grid[i][j] == 0:
            return
        if visited[i][j]:
            return
        # print('okay ', i, " ", j)
        visited[i][j] = True
        for k in range(8):
            # print('k', k)
            t = self.getInd(i, j, k, n, m)
            # print('t', t)
            if not t:
                continue
            (a, b) = t
            # print('visited[a][b]', visited[a][b])
            # print('grid[a][b]', grid[a][b])
            if visited[a][b] or grid[a][b] == 0:
                continue
            # print('t', t)
            self.findIsland(grid, visited, a, b, n, m)
            
    
    def numIslands(self, grid):
        n = len(grid)
        m = len(grid[0])
        temp = [False for i in range(m)]
        visited = [temp.copy() for i in range(n)]
        count = 0
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 1 and not visited[i][j]:
                    # print(i, " ", j)
                    # print('visiting')
                    self.findIsland(grid, visited, i, j, n, m)
                    count += 1
        return count

solution = Solution()
grid = [[0, 1, 1, 0, 1], [1, 1, 1, 0, 0], [1, 1, 1, 1, 0], [0, 1, 1, 1, 1], [1, 1, 1, 0, 1]]
print(solution.numIslands(grid))
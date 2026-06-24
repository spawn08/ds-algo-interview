"""
Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.
You may assume all four edges of the grid are all surrounded by water.

Example 1:

Input: grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
Output: 1
Example 2:

Input: grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
Output: 3

"""

from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0

        rows, cols = len(grid), len(grid[0])
        islands: int = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def dfs_iterative(row_index: int, col_index: int):
            grid[row_index][col_index] = '0'  # Mark as visited by changing to water
            stack: List[tuple] = [(row_index, col_index)]

            while stack:
                x, y = stack.pop()
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy

                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == '1':
                        grid[nx][ny] = '0'  # mark as visited
                        stack.append((nx, ny))

        for row_index in range(rows):
            for col_index in range(cols):
                if grid[row_index][col_index] == '1':
                    dfs_iterative(row_index, col_index)
                    islands += 1

        return islands


if __name__ == '__main__':
    solution = Solution()
    grid = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    print(solution.numIslands(grid))  # 3

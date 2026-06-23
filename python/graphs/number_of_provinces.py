"""
There are n cities. Some of them are connected, while some are not. 
If city a is connected directly with city b, and city b is connected directly with city c, then city a is connected indirectly with city c.
A province is a group of directly or indirectly connected cities and no other cities outside of the group.
You are given an n x n matrix isConnected where isConnected[i][j] = 1 if the ith city and the jth city are directly connected, and isConnected[i][j] = 0 otherwise.
Return the total number of provinces.

Example 1:

Input: isConnected = [[1,1,0],[1,1,0],[0,0,1]]
Output: 2

Example 2:

Input: isConnected = [[1,0,0],[0,1,0],[0,0,1]]
Output: 3
"""
from typing import List


class Solution:

	def dfs(self, city: int, size: int, isConnected: List[List[int]], visited_city: List[bool]):
		visited_city[city] = True
		stack: List[int] = [city]
		while stack:
			current_city = stack.pop()
			for neighbour in range(size):
				if not visited_city[neighbour] and isConnected[current_city][neighbour] == 1:
					visited_city[neighbour] = True
					stack.append(neighbour)
	
	def findCircleNum(self, isConnected: List[List[int]]) -> int:
		if not isConnected or not isConnected[0]:
			return 0
		size: int = len(isConnected)
		visited_city: List[bool] = [False] * size
		provinces: int = 0
		
		for city in range(size):
			if not visited_city[city]:
				# dfs
				self.dfs(city, size, isConnected, visited_city)
				provinces += 1
		return provinces


if __name__ == '__main__':
	is_connected = [[1, 1, 0], [1, 1, 0], [0, 0, 1]]
	solution = Solution()
	print(solution.findCircleNum(isConnected=is_connected))

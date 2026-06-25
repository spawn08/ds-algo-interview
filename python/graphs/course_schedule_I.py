"""
There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. 
You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.

For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.
Return true if you can finish all courses. Otherwise, return false.

Example 1:

Input: numCourses = 2, prerequisites = [[1,0]]
Output: true
Explanation: There are a total of 2 courses to take. 
To take course 1 you should have finished course 0. So it is possible.
Example 2:

Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: false
Explanation: There are a total of 2 courses to take. 
To take course 1 you should have finished course 0, and 
to take course 0 you should also have finished course 1. So it is impossible.
"""

from collections import defaultdict, deque
from typing import List


class Solution:
    """
    Kahn's algorithm (BFS topological sort): a valid ordering exists iff every
    course can be processed, i.e. the prerequisite graph is acyclic.

    Time complexity:  O(V + E) -- V = numCourses, E = number of prerequisites;
                      each node and edge is handled once.
    Space complexity: O(V + E) -- adjacency list, in-degree array, and queue.
    """

    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        if not prerequisites:
            return False
        adjacency = defaultdict(list)
        in_degree = [0] * numCourses

        for course, preq in prerequisites:
            adjacency[preq].append(course)
            in_degree[course] += 1
        ready_queue = deque([course_id for course_id in range(numCourses) if in_degree[course_id] == 0])
        completed = 0

        while ready_queue:
            current_course = ready_queue.popleft()
            completed += 1

            for dependent_course in adjacency[current_course]:
                in_degree[dependent_course] -= 1
                if in_degree[dependent_course] == 0:
                    ready_queue.append(dependent_course)
        return completed == numCourses

if __name__ == '__main__':
    numCourses = 2
    prerequisites = [[1,0]]
    solution = Solution()
    print(solution.canFinish(numCourses=numCourses, prerequisites=prerequisites))
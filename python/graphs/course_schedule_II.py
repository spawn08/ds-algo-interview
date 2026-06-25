"""
There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. 
You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.

For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.
Return the ordering of courses you should take to finish all courses. If there are many valid answers, return any of them. 
If it is impossible to finish all courses, return an empty array.

Example 1:

Input: numCourses = 2, prerequisites = [[1,0]]
Output: [0,1]
Explanation: There are a total of 2 courses to take. 
To take course 1 you should have finished course 0. So the correct course order is [0,1].

Example 2:

Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
Output: [0,2,1,3]
Explanation: There are a total of 4 courses to take. 
To take course 3 you should have finished both courses 1 and 2. 
Both courses 1 and 2 should be taken after you finished course 0.
So one correct course order is [0,1,2,3]. Another correct ordering is [0,2,1,3].
Example 3:

Input: numCourses = 1, prerequisites = []
Output: [0]
"""

from collections import defaultdict, deque
from typing import List

class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        if not prerequisites:
            return []
        adjacency = defaultdict(list)
        in_degree = [0] * numCourses

        for course, prereq in prerequisites:
            adjacency[prereq].append(course)
            in_degree[course] += 1
        
        ready_queue = deque([course_id for course_id in range(numCourses) if in_degree[course_id] == 0])
        course_completion_order = []

        while ready_queue:
            current_course = ready_queue.popleft()
            course_completion_order.append(current_course)

            for dependency_course in adjacency[current_course]:
                in_degree[dependency_course] -= 1
                if in_degree[dependency_course] == 0:
                    ready_queue.append(dependency_course)

        if len(course_completion_order) != numCourses:
            return []
        return course_completion_order

if __name__ == '__main__':
    prerequisites = [[1,0],[2,0],[3,1],[3,2]]
    numCourses = 4

    solution = Solution()
    print(solution.findOrder(numCourses, prerequisites))

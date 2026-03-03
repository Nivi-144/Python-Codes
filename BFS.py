from collections import deque
graph = {
    0: [1, 2],
    1: [3],
    2: [3],
    3: []
}
def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start) 
    result = []
    while queue:
        node = queue.popleft()
        result.append(node)       
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)   
    return result
print("BFS Traversal =", bfs(graph, 0))
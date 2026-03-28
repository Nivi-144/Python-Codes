from collections import defaultdict, deque
graph = defaultdict(list)
edges = [(1,2),(1,3),(2,4),(2,5),(3,6)]
for u,v in edges:
    graph[u].append(v)
    graph[v].append(u)
def bfs(start):
    visited, queue = {start}, deque([start])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nb in graph[node]:
            if nb not in visited:
                visited.add(nb); queue.append(nb)
    return order
def dfs(start, visited=None):
    if visited is None: visited = set()
    visited.add(start)
    result = [start]
    for nb in graph[start]:
        if nb not in visited:
            result += dfs(nb, visited)
    return result
print("BFS:", bfs(1))
print("DFS:", dfs(1))

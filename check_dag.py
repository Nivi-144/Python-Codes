from collections import deque

def topological_sort(graph, n):
    in_degree = {i: 0 for i in range(n)}
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1

    queue = deque([u for u in in_degree if in_degree[u] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) == n:
        return order
    else:
        return "Cycle detected - Not a DAG"

graph = {0: [1], 1: [2], 2: []}
result = topological_sort(graph, 3)
print("Topological Order:", ['A','B','C'][i] if isinstance(result, list) else result)

print("Topological Order:", result)

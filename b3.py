def count_components(graph):
    visited = set()
    count = 0

    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)

    for node in graph:
        if node not in visited:
            dfs(node)
            count += 1
    return count

graph = {0: [1], 1: [0], 2: [3], 3: [2]}
print("Connected Components:", count_components(graph))

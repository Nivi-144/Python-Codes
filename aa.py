mport heapq

def astar(graph, start, goal, h):
    open_list = [(h[start], 0, start, [start])]
    visited = set()
    while open_list:
        f, g, node, path = heapq.heappop(open_list)
        if node in visited: continue
        visited.add(node)
        if node == goal: return path, g
        for neighbor, cost in graph.get(node, []):
            if neighbor not in visited:
                ng = g + cost
                heapq.heappush(open_list, (ng + h[neighbor], ng, neighbor, path+[neighbor]))
    return None, float('inf')

# Example: simple graph
graph = {'A':[('B',1),('C',4)],'B':[('C',2),('D',5)],'C':[('D',1)],'D':[]}
h = {'A':7,'B':6,'C':2,'D':0}
path, cost = astar(graph, 'A', 'D', h)
print("Path:", path, "Cost:", cost)

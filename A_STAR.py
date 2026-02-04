import heapq
def a_star(graph,start,goal,heuristic):
    open_list=[]
    heapq.heappush(open_list,(0,start))
    came_from={}
    g_cost={start:0}
    while open_list:
        _,current=heapq.heappop(open_list)
        if current==goal:
            path=[]
            while current in came_from:
                path.append(current)
                current=came_from[current]
            path.append(start)
            return path[::-1]
        for neighbor,cost in graph[current]:
            new_g=g_cost[current]+cost
            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor]=new_g
                f_cost = new_g + heuristic[neighbor]
                heapq.heappush(open_list, (f_cost, neighbor))
                came_from[neighbor] = current
    return None

graph = {
    'A': [('B', 1), ('C', 3)],
    'B': [('D', 1), ('E', 4)],
    'C': [('F', 2)],
    'D': [],
    'E': [('G', 2)],
    'F': [('G', 1)],
    'G': []
}

heuristic = {
    'A': 6,
    'B': 4,
    'C': 4,
    'D': 3,
    'E': 2,
    'F': 2,
    'G': 0
}

path = a_star(graph, 'A', 'G', heuristic)
print("Path found:", path)

    
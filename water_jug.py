from collections import deque

def water_jug(jug1,jug2,target):
    visited = set()
    queue = deque([((0, 0), [])]) 

    while queue:
        (x,y), path = queue.popleft()

        if x == target or y == target:
            path.append((x,y))
            return path

        if (x,y) in visited:
            continue

        visited.add((x,y))
        path = path + [(x,y)]

        states = [
            (jug1,y),            
            (x,jug2),           
            (0,y),               
            (x,0),               
            (x-min(x,jug2-y),y+min(x,jug2-y)),  
            (x+min(y,jug1-x),y-min(y, jug1-x))   
        ]

        for state in states:
            if state not in visited:
                queue.append((state, path))

    return "No solution"

result = water_jug(4, 3, 2)
for step in result:
    print(step)

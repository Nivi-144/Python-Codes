graph={0:[1],1:[0],2:[3],3:[2]}
visited=set()
def dfs(node):
    visited.add(node)
    for n in graph[node]:
        if n not in visited:
            dfs(n)
count=0
for node in graph:
    if node not in visited:
        dfs(node); count+=1
print("Connected Components =",count)

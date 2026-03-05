from collections import deque
graph={0:[1,2],1:[3],2:[3],3:[]}
def bfs(source):
    dist={i:-1 for i in graph}
    dist[source]=0
    q=deque([source])
    while q:
        node=q.popleft()
        for n in graph[node]:
            if dist[n]==-1:
                dist[n]=dist[node]+1
                q.append(n)
    return dist
print("Distances =",list(bfs(0).values()))

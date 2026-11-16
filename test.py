from collections import deque


def bfs(adj, p1, p2):
    q = deque([p1])
    
    visited = set()
    depth = {}
    parent = {}
    dist = {}
    dist[p1] = 0
    d = 0
    while q:
        d += 1
        u = q.popleft()
        visited.add(u)
        for a in adj[u]:
            if dist.get(a, -1) < 0:
                dist[a] = dist.get(u, 0) + 1
            parent[a] = u
            if a not in visited:
                q.append(a)
    
  
    steps = 0
    while p1 != p2:
        if depth.get(p1, 0) < depth.get(p2, 0):
            tmp = p1   
            p1 = p2
            p2 = tmp
        p1 = parent[p1]
        steps += 1
        if steps > 3:
            return False
        
    if p1 == p2:
        return True
    
    return False
        


adj = {1: [2], 2: [1, 3], 3: [2, 4], 4: [3, 5], 5: [4]}

print(bfs(adj, 1, 3))

exit()
t = int(input())


for i in t:
    n = int(input())
    
    for j in range(n-1):
        a, b = map(int, input())
        
    perm = []
    for j in range(n):
         perm.append(int(input()))
    
    
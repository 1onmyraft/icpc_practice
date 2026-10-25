# Tree Hopping (Kattis treehopping, difficulty 5.4)
# Idea: only distance <= 3 matters, so no LCA structure is needed. Root the tree,
# BFS for parent and depth, then for each adjacent pair repeatedly move the deeper
# node up one step; if they meet within 3 steps the distance is <= 3.
import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(data[idx]); idx += 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        adj = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            a = int(data[idx]); b = int(data[idx + 1]); idx += 2
            adj[a].append(b)
            adj[b].append(a)
        perm = [int(x) for x in data[idx:idx + n]]; idx += n

        parent = [0] * (n + 1)
        depth = [-1] * (n + 1)
        depth[1] = 0
        q = deque([1])
        while q:
            u = q.popleft()
            for w in adj[u]:
                if depth[w] < 0:
                    depth[w] = depth[u] + 1
                    parent[w] = u
                    q.append(w)

        ok = 1
        for i in range(n - 1):
            u, v = perm[i], perm[i + 1]
            steps = 0
            while u != v:
                if depth[u] < depth[v]:
                    u, v = v, u
                u = parent[u]
                steps += 1
                if steps > 3:
                    ok = 0
                    break
            if not ok:
                break
        out.append(str(ok))
    print("\n".join(out))

main()

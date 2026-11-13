"""Graphs page. Nodes 0..n-1 (subtract 1 when input is 1-indexed!). Self-test: python3 graphs.py

SPOT IT
  shortest path, all edges weight 1 / grid moves -> BFS
  weights 0 or 1                                 -> 0-1 BFS (deque)
  weights >= 0                                   -> Dijkstra
  negative weights / detect negative cycle       -> Bellman-Ford
  all pairs, n <= 400ish                         -> Floyd-Warshall
  connect everything cheapest                    -> Kruskal (sort edges + DSU)
  groups / connected? / merge online             -> DSU
  order with prerequisites / is there a cycle    -> topological sort
  two colors, no conflict, odd cycle             -> bipartite check
  mutual reachability, 2-SAT                     -> SCC (Kosaraju)
  tree: distance / ancestor queries              -> LCA binary lifting
  tree: farthest pair                            -> diameter (BFS twice)
  max flow / min cut / disjoint paths            -> Dinic
  match workers to jobs                          -> bipartite matching (Kuhn) or Dinic
Python: NO recursive DFS on big graphs (use a stack). Build adj as list of lists.
Reading: n, m then m lines u v (w)  -> adj[u-1].append((v-1, w)); undirected: both ways.
"""
import heapq
from collections import deque

INF = float('inf')


def dijkstra(adj, src, n):
    """adj[u] = list of (v, w), w >= 0. Returns dist list, inf if unreachable."""
    dist = [INF] * n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue                       # stale entry
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


def dijkstra_path(adj, src, dst, n):
    """also returns the path src..dst (or None)"""
    dist, par = [INF] * n, [-1] * n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v], par[v] = d + w, u
                heapq.heappush(pq, (d + w, v))
    if dist[dst] == INF:
        return INF, None
    path, v = [], dst
    while v != -1:
        path.append(v)
        v = par[v]
    return dist[dst], path[::-1]


def bfs(adj, src, n):
    """unweighted shortest paths; -1 = unreachable"""
    dist = [-1] * n
    dist[src] = 0
    q = deque([src])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] < 0:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def grid_bfs(grid, sr, sc):
    """grid of strings, '#' = wall. Returns dist grid (-1 unreachable)."""
    R, C = len(grid), len(grid[0])
    dist = [[-1] * C for _ in range(R)]
    dist[sr][sc] = 0
    q = deque([(sr, sc)])
    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != '#' and dist[nr][nc] < 0:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    return dist


def bfs01(adj, src, n):
    """weights 0/1: 0-edge -> appendleft, 1-edge -> append"""
    dist = [INF] * n
    dist[src] = 0
    dq = deque([src])
    while dq:
        u = dq.popleft()
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                (dq.appendleft if w == 0 else dq.append)(v)
    return dist


def bellman_ford(n, edges, src):
    """edges = [(u, v, w)]. Returns dist, or None if a negative cycle is reachable from src."""
    dist = [INF] * n
    dist[src] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return None
    return dist


def floyd(n, edges):
    """all pairs. d[i][i] < 0 after => i on a negative cycle. O(n^3)."""
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik, di = d[i][k], d[i]
            if dik == INF:
                continue
            for j in range(n):
                if dik + dk[j] < di[j]:
                    di[j] = dik + dk[j]
    return d


class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.sz = [1] * n

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.sz[a] < self.sz[b]:
            a, b = b, a
        self.p[b] = a
        self.sz[a] += self.sz[b]
        return True


def kruskal(n, edges):
    """edges = [(w, u, v)]. Returns (total weight, #edges used). #edges < n-1 => not connected."""
    d, total, used = DSU(n), 0, 0
    for w, u, v in sorted(edges):
        if d.union(u, v):
            total += w
            used += 1
    return total, used


def topo_sort(adj, n):
    """Kahn's algorithm. Returns order, or None if there is a cycle."""
    indeg = [0] * n
    for u in range(n):
        for v in adj[u]:
            indeg[v] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == n else None


def components(adj, n):
    """comp[v] = component id, iterative DFS"""
    comp, c = [-1] * n, 0
    for s in range(n):
        if comp[s] >= 0:
            continue
        comp[s] = c
        st = [s]
        while st:
            u = st.pop()
            for v in adj[u]:
                if comp[v] < 0:
                    comp[v] = c
                    st.append(v)
        c += 1
    return comp, c


def bipartite(adj, n):
    """returns color list (0/1) or None if an odd cycle exists"""
    col = [-1] * n
    for s in range(n):
        if col[s] >= 0:
            continue
        col[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if col[v] < 0:
                    col[v] = col[u] ^ 1
                    q.append(v)
                elif col[v] == col[u]:
                    return None
    return col


def scc(adj, n):
    """Kosaraju, iterative. comp[v] in topological order of the condensation."""
    order, seen = [], [False] * n
    for s in range(n):
        if seen[s]:
            continue
        seen[s] = True
        st = [(s, 0)]
        while st:
            u, i = st.pop()
            if i < len(adj[u]):
                st.append((u, i + 1))
                v = adj[u][i]
                if not seen[v]:
                    seen[v] = True
                    st.append((v, 0))
            else:
                order.append(u)
    radj = [[] for _ in range(n)]
    for u in range(n):
        for v in adj[u]:
            radj[v].append(u)
    comp, c = [-1] * n, 0
    for s in reversed(order):
        if comp[s] >= 0:
            continue
        comp[s] = c
        st = [s]
        while st:
            u = st.pop()
            for v in radj[u]:
                if comp[v] < 0:
                    comp[v] = c
                    st.append(v)
        c += 1
    return comp, c
# 2-SAT: var x -> nodes 2x (true), 2x+1 (false). clause (a or b): edges ~a->b, ~b->a.
# unsatisfiable iff comp[2x] == comp[2x+1]; x = True iff comp[2x] > comp[2x+1].


class LCA:
    """tree with root; binary lifting. O(n log n) build, O(log n) query."""
    def __init__(self, adj, root=0):
        n = len(adj)
        self.LOG = LOG = max(1, n.bit_length())
        self.depth = depth = [0] * n
        up = [[root] * n for _ in range(LOG)]
        seen = [False] * n
        seen[root] = True
        st = [root]
        while st:
            u = st.pop()
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    depth[v] = depth[u] + 1
                    up[0][v] = u
                    st.append(v)
        for k in range(1, LOG):
            prev, cur = up[k - 1], up[k]
            for v in range(n):
                cur[v] = prev[prev[v]]
        self.up = up

    def kth_ancestor(self, v, k):
        for i in range(self.LOG):
            if k >> i & 1:
                v = self.up[i][v]
        return v

    def lca(self, a, b):
        if self.depth[a] < self.depth[b]:
            a, b = b, a
        a = self.kth_ancestor(a, self.depth[a] - self.depth[b])
        if a == b:
            return a
        for k in range(self.LOG - 1, -1, -1):
            if self.up[k][a] != self.up[k][b]:
                a, b = self.up[k][a], self.up[k][b]
        return self.up[0][a]

    def dist(self, a, b):
        return self.depth[a] + self.depth[b] - 2 * self.depth[self.lca(a, b)]


def tree_diameter(adj, n):
    """BFS from any node -> farthest u; BFS from u -> farthest distance"""
    d = bfs(adj, 0, n)
    u = d.index(max(d))
    d2 = bfs(adj, u, n)
    return max(d2)


class Dinic:
    """max flow. add_edge(u, v, cap). O(V^2 E), fast in practice. Min cut = max flow."""
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]      # edge = [to, cap, index of reverse]

    def add_edge(self, u, v, cap):
        self.g[u].append([v, cap, len(self.g[v])])
        self.g[v].append([u, 0, len(self.g[u]) - 1])

    def max_flow(self, s, t):
        flow, g = 0, self.g
        while True:
            level = [-1] * self.n
            level[s] = 0
            q = deque([s])
            while q:
                u = q.popleft()
                for v, cap, _ in g[u]:
                    if cap > 0 and level[v] < 0:
                        level[v] = level[u] + 1
                        q.append(v)
            if level[t] < 0:
                return flow
            it = [0] * self.n
            while True:                          # iterative DFS for blocking flow
                stack, path = [s], []
                found = False
                while stack:
                    u = stack[-1]
                    if u == t:
                        found = True
                        break
                    advanced = False
                    while it[u] < len(g[u]):
                        e = g[u][it[u]]
                        if e[1] > 0 and level[e[0]] == level[u] + 1:
                            stack.append(e[0])
                            path.append(e)
                            advanced = True
                            break
                        it[u] += 1
                    if not advanced:
                        stack.pop()
                        if path:
                            path.pop()
                            it[stack[-1]] += 1
                        level[u] = -1
                if not found:
                    break
                f = min(e[1] for e in path)
                for e in path:
                    e[1] -= f
                    g[e[0]][e[2]][1] += f
                flow += f


def bipartite_matching(adj, nL, nR):
    """Kuhn's algorithm. adj[l] = list of right nodes. Returns (size, matchR)."""
    matchR = [-1] * nR
    size = 0
    for s in range(nL):
        used = [False] * nR
        # iterative augmenting path search
        stack = [(s, 0)]
        parent = {}
        found = -1
        while stack and found < 0:
            l, i = stack.pop()
            while i < len(adj[l]):
                r = adj[l][i]
                i += 1
                if used[r]:
                    continue
                used[r] = True
                parent[r] = l
                if matchR[r] < 0:
                    found = r
                    break
                stack.append((l, i))
                stack.append((matchR[r], 0))
                break
        if found >= 0:
            r = found
            while r != -1:
                l = parent[r]
                prev = next((rr for rr in adj[l] if matchR[rr] == l), -1)
                matchR[r] = l
                r = prev
            size += 1
    return size, matchR


if __name__ == "__main__":
    import random
    from itertools import permutations
    for _ in range(300):
        n = random.randint(1, 8)
        E = [(random.randrange(n), random.randrange(n), random.randint(0, 9)) for _ in range(random.randint(0, 15))]
        adj = [[] for _ in range(n)]
        for u, v, w in E:
            adj[u].append((v, w))
        fl = floyd(n, E)
        assert dijkstra(adj, 0, n) == fl[0]
        bf = bellman_ford(n, E, 0)
        assert bf == fl[0]
        d, p = dijkstra_path(adj, 0, n - 1, n)
        assert d == fl[0][n - 1]
        if p:
            assert p[0] == 0 and p[-1] == n - 1
            assert sum(min(w for uu, vv, w in E if uu == a and vv == b) for a, b in zip(p, p[1:])) == d
        adj01 = [[(v, w % 2) for v, w in adj[u]] for u in range(n)]
        assert bfs01(adj01, 0, n) == floyd(n, [(u, v, w % 2) for u, v, w in E])[0]
        unw = [[v for v, _ in adj[u]] for u in range(n)]
        assert bfs(unw, 0, n) == [x if x < INF else -1 for x in floyd(n, [(u, v, 1) for u, v, _ in E])[0]]
        # negative cycle detection
        En = [(u, v, w - 4) for u, v, w in E]
        fn = floyd(n, En)
        reach = floyd(n, [(u, v, 1) for u, v, _ in En])[0]
        neg = any(fn[i][i] < 0 and reach[i] < INF for i in range(n))
        assert (bellman_ford(n, En, 0) is None) == neg
        # topo sort
        dag = [[] for _ in range(n)]
        for u, v, _ in E:
            dag[u].append(v)
        order = topo_sort(dag, n)
        has_cycle = any(floyd(n, [(u, v, 1) for u, v, _ in E])[i][j] < INF and
                        floyd(n, [(u, v, 1) for u, v, _ in E])[j][i] < INF and i != j
                        for i in range(n) for j in range(n)) or any(u == v for u, v, _ in E)
        assert (order is None) == has_cycle
        if order:
            pos = {v: i for i, v in enumerate(order)}
            assert all(pos[u] < pos[v] for u, v, _ in E)
        # SCC vs reachability
        comp, c = scc(dag, n)
        R = floyd(n, [(u, v, 1) for u, v, _ in E])
        for i in range(n):
            for j in range(n):
                assert (comp[i] == comp[j]) == (R[i][j] < INF and R[j][i] < INF)
                if R[i][j] < INF and comp[i] != comp[j]:
                    assert comp[i] < comp[j]
        # undirected: components, bipartite, kruskal
        und = [[] for _ in range(n)]
        for u, v, _ in E:
            und[u].append(v); und[v].append(u)
        cm, cc = components(und, n)
        RU = floyd(n, [(u, v, 1) for u, v, _ in E] + [(v, u, 1) for u, v, _ in E])
        assert all((cm[i] == cm[j]) == (RU[i][j] < INF) for i in range(n) for j in range(n))
        col = bipartite(und, n)
        bb = any(all(((m >> u) & 1) != ((m >> v) & 1) for u, v, _ in E) for m in range(1 << n))
        assert (col is not None) == bb
        if col:
            assert all(col[u] != col[v] for u, v, _ in E)
        tot, used = kruskal(n, [(w, u, v) for u, v, w in E])
        assert used == n - cc
        # brute MST on small: try all edge subsets of size n-cc forming a forest
        from itertools import combinations
        if len(E) <= 10:
            best = min((sum(e[2] for e in sub) for sub in combinations(E, n - cc)
                        if (lambda s: (lambda d: all(d.union(u, v) for u, v, _ in s))(DSU(n)))(sub)), default=0)
            assert tot == best
    # trees: LCA, diameter
    for _ in range(200):
        n = random.randint(1, 30)
        par = [-1] + [random.randrange(i) for i in range(1, n)]
        adj = [[] for _ in range(n)]
        for v in range(1, n):
            adj[v].append(par[v]); adj[par[v]].append(v)
        L = LCA(adj)
        def anc(v):
            out = [v]
            while par[v] >= 0:
                v = par[v]; out.append(v)
            return out
        for _ in range(30):
            a, b = random.randrange(n), random.randrange(n)
            A = anc(a)
            exp = next(x for x in A if x in set(anc(b)))
            assert L.lca(a, b) == exp
            assert L.dist(a, b) == bfs(adj, a, n)[b]
        assert tree_diameter(adj, n) == max(max(bfs(adj, s, n)) for s in range(n))
    # flow and matching
    for _ in range(300):
        n = random.randint(2, 7)
        E = [(random.randrange(n), random.randrange(n), random.randint(0, 6)) for _ in range(random.randint(0, 12))]
        D = Dinic(n)
        for u, v, c in E:
            D.add_edge(u, v, c)
        f = D.max_flow(0, n - 1)
        # brute min cut
        best = min(sum(c for u, v, c in E if (m >> u) & 1 and not (m >> v) & 1)
                   for m in range(1 << n) if m & 1 and not (m >> (n - 1)) & 1)
        assert f == best, (n, E, f, best)
        nL, nR = random.randint(1, 5), random.randint(1, 5)
        badj = [sorted(random.sample(range(nR), random.randint(0, nR))) for _ in range(nL)]
        size, mR = bipartite_matching(badj, nL, nR)
        def brute(l, usedmask):
            if l == nL:
                return 0
            r0 = brute(l + 1, usedmask)
            for r in badj[l]:
                if not usedmask >> r & 1:
                    r0 = max(r0, 1 + brute(l + 1, usedmask | 1 << r))
            return r0
        assert size == brute(0, 0)
        assert sum(1 for x in mR if x >= 0) == size
        assert all(mR[r] < 0 or r in badj[mR[r]] for r in range(nR))
        assert len({x for x in mR if x >= 0}) == size
    g = ["..#", "...", "#.."]
    assert grid_bfs(g, 0, 0)[2][2] == 4 and grid_bfs(g, 0, 0)[2][0] == -1
    print("graphs: all tests passed")

"""Brute force for NAQ M: enumerate every simple path on tiny graphs.

ASSUMPTIONS (check against the real statement):
  - pairs are unordered, endpoints are distinct vertices (u != v)
  - every distinct simple path between a pair counts once
  - a pair qualifies if abs(vals[u] - vals[v]) == k
"""


def count_brute(n, k, vals, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    def paths(u, target, seen):
        if u == target:
            return 1
        total = 0
        for w in adj[u]:
            if w not in seen:
                seen.add(w)
                total += paths(w, target, seen)
                seen.discard(w)
        return total

    answer = 0
    for u in range(n):
        for v in range(u + 1, n):
            if abs(vals[u] - vals[v]) == k:
                answer += paths(u, v, {u})
    return answer

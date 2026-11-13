"""DP page. Self-test: python3 dp.py

HOW TO WRITE ANY DP (do these 4 in a comment before coding)
  1. STATE:  dp[i][j] = <one sentence, in words>  (what do I need to know to finish?)
  2. CHOICE: what is the last decision?  -> transition
  3. BASE:   smallest cases
  4. ORDER/ANSWER: fill so dependencies come first; which cell is the answer?
Size check: (#states) * (#choices) <= ~1e7 in PyPy.
"number of ways" -> add, mod.   "min/max" -> min/max.   "possible?" -> or.

SPOT IT
  pick items, capacity W           -> knapsack (0/1: loop w DOWN; unbounded: loop w UP)
  count ways to make sum           -> coin change (order matters? loop sum outside)
  longest increasing subsequence   -> LIS with bisect, O(n log n)
  two strings, match/edit          -> LCS / edit distance, dp[i][j] on prefixes
  grid, move right/down            -> dp[r][c] from top and left
  n <= 20, subsets / visit all     -> bitmask DP dp[mask][last]
  merge/split a range, l..r        -> interval DP dp[l][r], loop by length
  count numbers <= N with property -> digit DP (tight flag)
  tree, choose nodes               -> dp[v][taken?] from children (iterative post-order)
"""
from bisect import bisect_left, bisect_right
from functools import lru_cache

MOD = 10**9 + 7
INF = float('inf')


def knapsack01(items, W):
    """items = [(weight, value)], each used at most once. max value with weight <= W"""
    dp = [0] * (W + 1)
    for w, v in items:
        for c in range(W, w - 1, -1):          # DOWN: each item once
            if dp[c - w] + v > dp[c]:
                dp[c] = dp[c - w] + v
    return dp[W]


def knapsack_unbounded(items, W):
    dp = [0] * (W + 1)
    for w, v in items:
        for c in range(w, W + 1):              # UP: item reusable
            if dp[c - w] + v > dp[c]:
                dp[c] = dp[c - w] + v
    return dp[W]


def coin_ways_combinations(coins, S):
    """{1,2} and {2,1} counted ONCE (CSES 1636)"""
    dp = [1] + [0] * S
    for c in coins:                            # coins OUTSIDE
        for s in range(c, S + 1):
            dp[s] = (dp[s] + dp[s - c]) % MOD
    return dp[S]


def coin_ways_ordered(coins, S):
    """{1,2} and {2,1} counted TWICE (CSES 1635)"""
    dp = [1] + [0] * S
    for s in range(1, S + 1):                  # sum OUTSIDE
        t = 0
        for c in coins:
            if c <= s:
                t += dp[s - c]
        dp[s] = t % MOD
    return dp[S]


def min_coins(coins, S):
    dp = [0] + [INF] * S
    for s in range(1, S + 1):
        for c in coins:
            if c <= s and dp[s - c] + 1 < dp[s]:
                dp[s] = dp[s - c] + 1
    return dp[S] if dp[S] < INF else -1


def lis_length(a, strict=True):
    """tails[k] = smallest possible last value of an increasing subsequence of length k+1.
    non-decreasing: use bisect_right."""
    tails = []
    for x in a:
        i = (bisect_left if strict else bisect_right)(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)


def lcs(s, t):
    n, m = len(s), len(t)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    # reconstruct
    out, i, j = [], n, m
    while i and j:
        if s[i - 1] == t[j - 1]:
            out.append(s[i - 1]); i -= 1; j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return dp[n][m], ''.join(reversed(out))


def edit_distance(s, t):
    """insert / delete / replace, each cost 1 (CSES 1639)"""
    n, m = len(s), len(t)
    prev = list(range(m + 1))
    for i in range(1, n + 1):
        cur = [i] + [0] * m
        for j in range(1, m + 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (s[i - 1] != t[j - 1]))
        prev = cur
    return prev[m]


def grid_paths(grid):
    """count right/down paths avoiding '#' (CSES 1638)"""
    n, m = len(grid), len(grid[0])
    dp = [[0] * m for _ in range(n)]
    for r in range(n):
        for c in range(m):
            if grid[r][c] == '#':
                continue
            if r == 0 and c == 0:
                dp[r][c] = 1
                continue
            dp[r][c] = ((dp[r - 1][c] if r else 0) + (dp[r][c - 1] if c else 0)) % MOD
    return dp[n - 1][m - 1]


def tsp(dist):
    """bitmask DP: min cost path starting at 0 visiting all nodes. O(2^n n^2), n <= ~16 in PyPy.
    dp[mask][v] = min cost to visit exactly `mask`, ending at v."""
    n = len(dist)
    full = 1 << n
    dp = [[INF] * n for _ in range(full)]
    dp[1][0] = 0
    for mask in range(full):
        row = dp[mask]
        for v in range(n):
            cur = row[v]
            if cur == INF or not (mask >> v) & 1:
                continue
            for u in range(n):
                if not (mask >> u) & 1:
                    nm = mask | (1 << u)
                    if cur + dist[v][u] < dp[nm][u]:
                        dp[nm][u] = cur + dist[v][u]
    return min(dp[full - 1])


def interval_merge_cost(a):
    """interval DP: merge adjacent piles, cost = sum of the two merged. dp[l][r] over lengths."""
    n = len(a)
    P = [0]
    for x in a:
        P.append(P[-1] + x)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for l in range(n - length + 1):
            r = l + length - 1
            dp[l][r] = min(dp[l][k] + dp[k + 1][r] for k in range(l, r)) + P[r + 1] - P[l]
    return dp[0][n - 1]


def digit_count(N):
    """count x in [0, N] whose digits satisfy a property, via digit DP.
    Example property here: no two adjacent equal digits (CSES 2220 style, leading zeros skipped).
    State: (pos, last digit, tight, started)."""
    D = list(map(int, str(N)))

    @lru_cache(None)
    def go(pos, last, tight, started):
        if pos == len(D):
            return 1
        lim = D[pos] if tight else 9
        total = 0
        for d in range(lim + 1):
            if started and d == last:
                continue
            ns = started or d != 0
            total += go(pos + 1, d if ns else -1, tight and d == lim, ns)
        return total
    return go(0, -1, True, False)


def max_subarray(a):
    """Kadane: best non-empty contiguous sum"""
    best = cur = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best


def tree_max_independent(n, edges):
    """tree DP: max nodes chosen with no two adjacent. Iterative (no recursion limit)."""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    order, parent, stack = [], [-1] * n, [0]
    seen = [False] * n
    seen[0] = True
    while stack:
        v = stack.pop()
        order.append(v)
        for u in adj[v]:
            if not seen[u]:
                seen[u] = True
                parent[u] = v
                stack.append(u)
    take, skip = [1] * n, [0] * n
    for v in reversed(order):                  # children before parents
        p = parent[v]
        if p >= 0:
            take[p] += skip[v]
            skip[p] += max(take[v], skip[v])
    return max(take[0], skip[0])


if __name__ == "__main__":
    import random
    from itertools import combinations, permutations, product
    for _ in range(300):
        items = [(random.randint(1, 6), random.randint(0, 9)) for _ in range(random.randint(0, 7))]
        W = random.randint(0, 15)
        best = 0
        for r in range(len(items) + 1):
            for comb in combinations(items, r):
                if sum(w for w, _ in comb) <= W:
                    best = max(best, sum(v for _, v in comb))
        assert knapsack01(items, W) == best
        # unbounded brute
        ub = [0] * (W + 1)
        for c in range(W + 1):
            for w, v in items:
                if w <= c:
                    ub[c] = max(ub[c], ub[c - w] + v)
        assert knapsack_unbounded(items, W) == ub[W]
        coins = sorted(set(random.randint(1, 5) for _ in range(random.randint(1, 3))))
        S = random.randint(0, 12)
        ordered = combos = 0
        for k in range(S + 1):
            for seq in product(coins, repeat=k):
                if sum(seq) == S:
                    ordered += 1
                    if list(seq) == sorted(seq):
                        combos += 1
        assert coin_ways_ordered(coins, S) == ordered and coin_ways_combinations(coins, S) == combos
        mc = min((k for k in range(S + 1) for seq in product(coins, repeat=k) if sum(seq) == S), default=-1)
        assert min_coins(coins, S) == mc
        a = [random.randint(0, 6) for _ in range(random.randint(1, 9))]
        bs = bn = 0
        for mask in range(1 << len(a)):
            sub_ = [a[i] for i in range(len(a)) if mask >> i & 1]
            if all(x < y for x, y in zip(sub_, sub_[1:])):
                bs = max(bs, len(sub_))
            if all(x <= y for x, y in zip(sub_, sub_[1:])):
                bn = max(bn, len(sub_))
        assert lis_length(a) == bs and lis_length(a, False) == bn
        assert max_subarray([x - 3 for x in a]) == max(sum(a[i:j]) - 3 * (j - i) for i in range(len(a)) for j in range(i + 1, len(a) + 1))
        s = ''.join(random.choice('ab') for _ in range(random.randint(0, 6)))
        t = ''.join(random.choice('abc') for _ in range(random.randint(0, 6)))
        L, seq = lcs(s, t)
        it = iter(s); it2 = iter(t)
        assert len(seq) == L and all(ch in it for ch in seq) and all(ch in it2 for ch in seq)
        bl = max((r for r in range(min(len(s), len(t)) + 1) for c in combinations(s, r)
                  if (lambda c: (lambda it: all(ch in it for ch in c))(iter(t)))(c)), default=0)
        assert L == bl
        @lru_cache(None)
        def ed(i, j):
            if i == 0 or j == 0:
                return i + j
            return min(ed(i - 1, j) + 1, ed(i, j - 1) + 1, ed(i - 1, j - 1) + (s[i - 1] != t[j - 1]))
        assert edit_distance(s, t) == ed(len(s), len(t))
        n = random.randint(1, 6)
        dist = [[random.randint(1, 9) for _ in range(n)] for _ in range(n)]
        bt = min((sum(dist[p[i]][p[i + 1]] for i in range(n - 1)) for p in permutations(range(n)) if p[0] == 0))
        assert tsp(dist) == bt
        piles = [random.randint(1, 9) for _ in range(random.randint(1, 6))]
        def brute_merge(p):
            if len(p) == 1:
                return 0
            return min(p[i] + p[i + 1] + brute_merge(p[:i] + [p[i] + p[i + 1]] + p[i + 2:]) for i in range(len(p) - 1))
        assert interval_merge_cost(piles) == brute_merge(piles)
        N = random.randint(0, 3000)
        assert digit_count(N) == sum(1 for x in range(N + 1) if all(a_ != b_ for a_, b_ in zip(str(x), str(x)[1:])))
        n = random.randint(1, 9)
        edges = [(i, random.randrange(i)) for i in range(1, n)]
        bi = max(bin(m).count('1') for m in range(1 << n) if all(not (m >> u & 1 and m >> v & 1) for u, v in edges))
        assert tree_max_independent(n, edges) == bi
    g = ["....", ".*..", "...*", "*..."]
    g = [row.replace('*', '#') for row in g]
    def brute_paths(r, c):
        if r >= 4 or c >= 4 or g[r][c] == '#':
            return 0
        if (r, c) == (3, 3):
            return 1
        return brute_paths(r + 1, c) + brute_paths(r, c + 1)
    assert grid_paths(g) == brute_paths(0, 0) == 3
    print("dp: all tests passed")

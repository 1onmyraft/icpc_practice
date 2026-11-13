"""Data structures page. Every block is tested by the brute-force check at the bottom
(run: python3 data_structures.py).

WHICH ONE?
  range SUM, array never changes      -> prefix sums          O(1) query
  range SUM, with updates             -> Fenwick              O(log n) both
  range MIN/MAX, array never changes  -> sparse table         O(1) query
  range MIN/MAX/SUM, with updates     -> segment tree         O(log n) both
  min/max of every window of size k   -> monotonic deque      O(n) total
  sum of a rectangle in a grid        -> 2D prefix sums       O(1) query

Neutral fill values: sum -> 0, min -> inf, max -> -inf.
Test edges: (0,0), (0,n-1), (n-1,n-1), and every (l,r) on a small array vs brute force.
"""
from collections import deque

INF = float('inf')


# ---------- 1D prefix sums ----------
# P[k] = a[0] + ... + a[k-1];  sum(a[l..r]) = P[r+1] - P[l]   (0-indexed, inclusive)
def prefix_sums(a):
    P = [0] * (len(a) + 1)
    for i, x in enumerate(a):
        P[i + 1] = P[i] + x
    return P


# ---------- 2D prefix sums ----------
# S[i][j] = sum of g[0..i-1][0..j-1]
# rect(r1,c1,r2,c2) inclusive = S[r2+1][c2+1] - S[r1][c2+1] - S[r2+1][c1] + S[r1][c1]
def prefix_2d(g):
    n, m = len(g), len(g[0])
    S = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(m):
            S[i + 1][j + 1] = g[i][j] + S[i][j + 1] + S[i + 1][j] - S[i][j]
    return S


def rect(S, r1, c1, r2, c2):
    return S[r2 + 1][c2 + 1] - S[r1][c2 + 1] - S[r2 + 1][c1] + S[r1][c1]


# ---------- Fenwick tree (BIT): point add, prefix sum ----------
# 1-INDEXED. T[i] holds the sum of a block ending at i, length = lowest bit of i.
# "set a[k] = u"  ->  add(k, u - a[k]); a[k] = u      (keep the plain array a!)
# range sum a[l..r] = prefix(r) - prefix(l - 1)
# Does NOT do range min (min can't be subtracted) -> use segment tree.
class Fenwick:
    def __init__(self, n):
        self.n = n
        self.T = [0] * (n + 1)

    def add(self, i, d):            # a[i] += d
        T, n = self.T, self.n
        while i <= n:
            T[i] += d
            i += i & -i             # climb to every box that contains i

    def prefix(self, i):            # a[1] + ... + a[i]
        T, s = self.T, 0
        while i > 0:
            s += T[i]
            i -= i & -i             # hop down the staircase
        return s

    def range_sum(self, l, r):      # a[l..r], 1-indexed inclusive
        return self.prefix(r) - self.prefix(l - 1)


# ---------- Sparse table: static range min, O(1) query ----------
# Level i has exactly n - 2^i + 1 blocks (no filler: a bad index crashes loudly).
# Query: two blocks of length 2^k that overlap -- fine for min/max/gcd, WRONG for sum.
def sparse_build(a, f=min):
    n = len(a)
    sp = [a[:]]
    i = 1
    while (1 << i) <= n:
        prev, half = sp[i - 1], 1 << (i - 1)
        sp.append([f(prev[j], prev[j + half]) for j in range(n - (1 << i) + 1)])
        i += 1
    return sp


def sparse_query(sp, l, r, f=min):  # 0-indexed inclusive
    k = (r - l + 1).bit_length() - 1
    return f(sp[k][l], sp[k][r - (1 << k) + 1])


# ---------- Segment tree: point set, range query (any associative op) ----------
# 0-indexed, query is HALF-OPEN [l, r).  Iterative, bottom-up.
# Change op/neutral: min/INF, max/-INF, sum/0, gcd/0.
class SegTree:
    def __init__(self, a, op=min, neutral=INF):
        n = len(a)
        self.n, self.op, self.e = n, op, neutral
        self.t = [neutral] * n + list(a)
        for i in range(n - 1, 0, -1):
            self.t[i] = op(self.t[2 * i], self.t[2 * i + 1])

    def set(self, i, v):            # a[i] = v
        t, op = self.t, self.op
        i += self.n
        t[i] = v
        i >>= 1
        while i:
            t[i] = op(t[2 * i], t[2 * i + 1])
            i >>= 1

    def query(self, l, r):          # op over a[l..r-1]
        t, op = self.t, self.op
        resl = resr = self.e
        l += self.n
        r += self.n
        while l < r:
            if l & 1:
                resl = op(resl, t[l]); l += 1
            if r & 1:
                r -= 1; resr = op(t[r], resr)
            l >>= 1
            r >>= 1
        return op(resl, resr)


# ---------- Monotonic deque: min of every window of size k ----------
# For max: flip the comparison to <=.
def window_mins(a, k):
    dq, out = deque(), []
    for i, x in enumerate(a):
        while dq and a[dq[-1]] >= x:    # bigger ones behind x can never be the min
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:              # front fell out of the window
            dq.popleft()
        if i >= k - 1:
            out.append(a[dq[0]])
    return out


# ---------- Monotonic stack: next smaller element to the right ----------
# res[i] = index of first j > i with a[j] < a[i], or -1.  (next greater: flip to <)
def next_smaller(a):
    res, st = [-1] * len(a), []
    for i, x in enumerate(a):
        while st and a[st[-1]] > x:
            res[st.pop()] = i
        st.append(i)
    return res


if __name__ == "__main__":
    import random
    from math import gcd
    for _ in range(400):
        n = random.randint(1, 25)
        a = [random.randint(-20, 20) for _ in range(n)]
        P = prefix_sums(a)
        sp = sparse_build(a)
        spmax = sparse_build(a, max)
        st = SegTree(a)
        stsum = SegTree(a, lambda x, y: x + y, 0)
        stg = SegTree([abs(x) for x in a], gcd, 0)
        fw = Fenwick(n)
        for i, x in enumerate(a):
            fw.add(i + 1, x)
        for l in range(n):
            for r in range(l, n):
                seg = a[l:r + 1]
                assert P[r + 1] - P[l] == sum(seg)
                assert sparse_query(sp, l, r) == min(seg)
                assert sparse_query(spmax, l, r, max) == max(seg)
                assert st.query(l, r + 1) == min(seg)
                assert stsum.query(l, r + 1) == sum(seg)
                assert fw.range_sum(l + 1, r + 1) == sum(seg)
        b = a[:]
        for _ in range(30):                 # updates
            k, u = random.randrange(n), random.randint(-20, 20)
            fw.add(k + 1, u - b[k]); b[k] = u
            st.set(k, u); stsum.set(k, u); stg.set(k, abs(u))
            l = random.randrange(n); r = random.randint(l, n - 1)
            assert fw.range_sum(l + 1, r + 1) == sum(b[l:r + 1])
            assert st.query(l, r + 1) == min(b[l:r + 1])
            assert stsum.query(l, r + 1) == sum(b[l:r + 1])
            g = 0
            for x in b[l:r + 1]:
                g = gcd(g, abs(x))
            assert stg.query(l, r + 1) == g
        k = random.randint(1, n)
        assert window_mins(a, k) == [min(a[i:i + k]) for i in range(n - k + 1)]
        ns = next_smaller(a)
        for i in range(n):
            exp = next((j for j in range(i + 1, n) if a[j] < a[i]), -1)
            assert ns[i] == exp
        m = random.randint(1, 6)
        g2 = [[random.randint(-9, 9) for _ in range(m)] for _ in range(n)]
        S = prefix_2d(g2)
        for _ in range(20):
            r1 = random.randrange(n); r2 = random.randint(r1, n - 1)
            c1 = random.randrange(m); c2 = random.randint(c1, m - 1)
            assert rect(S, r1, c1, r2, c2) == sum(g2[i][j] for i in range(r1, r2 + 1) for j in range(c1, c2 + 1))
    print("data_structures: all tests passed")

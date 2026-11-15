import sys


def main():
    data = sys.stdin.buffer.read().split()
    T = int(data[0]); p = 1
    out = []
    INF = 1 << 62
    for _ in range(T):
        n = int(data[p]); s = data[p + 1]; p += 2          # s is bytes: s[i] == 87 ('W')
        t = [int(x) for x in data[p:p + n]]; p += n
        q = int(data[p]); p += 1
        W = 87

        # A[i] = t[i] - t[i-1] if person i-1 is W and i is M (the only muggles that matter)
        A = [INF] * n
        # G[j] = gap from wizard j back to the previous wizard (anywhere before it)
        G = [-1] * n
        last_w = -1
        for i in range(n):
            if s[i] == W:
                if last_w >= 0:
                    G[i] = t[i] - t[last_w]
                last_w = i
            elif i > 0 and s[i - 1] == W:
                A[i] = t[i] - t[i - 1]
        # next wizard at or after i
        nxt = [n] * (n + 1)
        for i in range(n - 1, -1, -1):
            nxt[i] = i if s[i] == W else nxt[i + 1]

        # sparse table for range min on A
        sp = [A]
        k = 1
        while (1 << k) <= n:
            prev, half = sp[-1], 1 << (k - 1)
            sp.append([min(prev[j], prev[j + half]) for j in range(n - (1 << k) + 1)])
            k += 1

        def rmin(l, r):                       # inclusive, 0-indexed; empty -> INF
            if l > r:
                return INF
            k = (r - l + 1).bit_length() - 1
            row = sp[k]
            a, b = row[l], row[r - (1 << k) + 1]
            return a if a < b else b

        # per query: D = max d, and the counting range (f+1 .. r) with threshold D
        qs = []
        res_m = [0] * q
        res_d = [0] * q
        for qi in range(q):
            l = int(data[p]) - 1; r = int(data[p + 1]) - 1; p += 2
            D = rmin(l + 1, r)
            res_d[qi] = -1 if D == INF else D
            f = nxt[l]
            if f > r:
                res_m[qi] = 0                 # no wizards at all
            else:
                res_m[qi] = 1                 # first wizard always searches
                if f + 1 <= r:
                    qs.append((D, f + 1, r, qi))

        # offline: count j in [lo, hi] with G[j] >= D.
        # sort queries by D descending, add gaps to a Fenwick tree in descending order.
        gaps = sorted(((G[j], j) for j in range(n) if G[j] >= 0), reverse=True)
        qs.sort(reverse=True)
        tree = [0] * (n + 1)
        gi = 0
        for D, lo, hi, qi in qs:
            while gi < len(gaps) and gaps[gi][0] >= D:
                i = gaps[gi][1] + 1
                while i <= n:
                    tree[i] += 1
                    i += i & -i
                gi += 1
            c = 0
            i = hi + 1
            while i > 0:
                c += tree[i]; i -= i & -i
            i = lo
            while i > 0:
                c -= tree[i]; i -= i & -i
            res_m[qi] += c

        for qi in range(q):
            out.append(f"{res_m[qi]} {res_d[qi]}")
    sys.stdout.write("\n".join(out) + "\n")


main()

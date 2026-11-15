import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0]); p = 1
    out = []
    for _ in range(t):
        n, k = int(data[p]), int(data[p + 1]); p += 2
        m = [0] * n; c = [0] * n
        for i in range(n):
            m[i] = int(data[p]); c[i] = int(data[p + 1]); p += 2

        order = sorted(range(n), key=lambda i: m[i])   # people sorted by m
        ms = [m[i] for i in order]
        # suf[x] = max curiosity among sorted people x..n-1  (suf[n] = -1: nobody)
        suf = [-1] * (n + 1)
        for x in range(n - 1, -1, -1):
            suf[x] = max(suf[x + 1], c[order[x]])

        good = []
        for i in range(n):
            a = suf[bisect_left(ms, m[i] + k)]   # best c among m_j >= m_i + k
            b = suf[bisect_left(ms, m[i])]       # best c among m_j >= m_i
            if a >= c[i] or b >= c[i] + k:
                continue                         # someone beats i -> ineligible
            good.append(i + 1)
        out.append(str(len(good)))
        out.append(' '.join(map(str, good)))
    print('\n'.join(out))


main()

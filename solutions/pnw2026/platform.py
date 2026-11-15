import sys
input = sys.stdin.readline

INF = float('inf')


# ---------- copied from notebook: Data structures -> Sparse table ----------
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


# ---------- copied from notebook: Data structures -> Fenwick ----------
class Fenwick:
    def __init__(self, n_or_list):
        if isinstance(n_or_list, int):
            vals = [0] * n_or_list
        else:
            vals = list(n_or_list)
        self.n = n = len(vals)
        self.a = [0] + vals
        self.T = T = self.a[:]
        for i in range(1, n + 1):
            j = i + (i & -i)
            if j <= n:
                T[j] += T[i]

    def add(self, i, d):            # a[i] += d
        self.a[i] += d
        T, n = self.T, self.n
        while i <= n:
            T[i] += d
            i += i & -i

    def prefix(self, i):            # a[1] + ... + a[i]
        T, s = self.T, 0
        while i > 0:
            s += T[i]
            i -= i & -i
        return s

    def range_sum(self, l, r):      # a[l..r], 1-indexed inclusive
        return self.prefix(r) - self.prefix(l - 1)


def solve():
    n = int(input())
    people = input().strip()
    times = list(map(int, input().split()))

    # muggle_gap[i]: person i is a muggle right after a wizard -> the barrier must close
    #   before them, so d <= times[i] - times[i-1].  (Later muggles in a row are further
    #   from that wizard, so only the first one matters.)  INF = no limit here.
    # wizard_gap[i]: person i is a wizard -> time since the previous wizard.
    #   With barrier duration d, this wizard searches iff wizard_gap[i] >= d.
    muggle_gap = [INF] * n
    wizard_gap = [None] * n
    last_wizard = -1
    for i in range(n):
        if people[i] == 'W':
            if last_wizard != -1:
                wizard_gap[i] = times[i] - times[last_wizard]
            last_wizard = i
        elif i > 0 and people[i - 1] == 'W':
            muggle_gap[i] = times[i] - times[i - 1]

    # next_wizard[i] = index of the first wizard at position >= i (n if none)
    next_wizard = [n] * (n + 1)
    for i in range(n - 1, -1, -1):
        next_wizard[i] = i if people[i] == 'W' else next_wizard[i + 1]

    table = sparse_build(muggle_gap)

    q = int(input())
    answer_count = [0] * q
    answer_d = [0] * q
    to_count = []          # (d, lo, hi, query index): count wizard gaps >= d in [lo, hi]

    for qi in range(q):
        l, r = map(int, input().split())
        l -= 1; r -= 1

        # largest d allowed: smallest muggle gap whose wizard is also inside [l, r]
        d = sparse_query(table, l + 1, r) if l + 1 <= r else INF
        answer_d[qi] = -1 if d == INF else d

        first = next_wizard[l]
        if first > r:
            answer_count[qi] = 0            # no wizards come at all
        else:
            answer_count[qi] = 1            # the first wizard always searches
            if first + 1 <= r:
                to_count.append((d, first + 1, r, qi))

    # Offline counting: handle queries from largest d to smallest, and add wizard gaps
    # to a Fenwick tree from largest to smallest.  When a query is answered, the tree
    # holds exactly the gaps >= its d, so a range sum counts the searching wizards.
    gaps = sorted(((wizard_gap[i], i) for i in range(n) if wizard_gap[i] is not None),
                  reverse=True)
    to_count.sort(reverse=True)
    fw = Fenwick(n)
    g = 0
    for d, lo, hi, qi in to_count:
        while g < len(gaps) and gaps[g][0] >= d:
            fw.add(gaps[g][1] + 1, 1)        # Fenwick is 1-indexed
            g += 1
        answer_count[qi] += fw.range_sum(lo + 1, hi + 1)

    return [f"{answer_count[qi]} {answer_d[qi]}" for qi in range(q)]


def main():
    t = int(input())
    out = []
    for _ in range(t):
        out.extend(solve())
    print('\n'.join(out))


main()

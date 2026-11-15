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


# ---------- copied from notebook: Data structures -> count_ge_offline ----------
def count_ge_offline(a, queries):
    """a: list (0-indexed). queries: list of (l, r, x), 0-indexed inclusive. Returns answers."""
    n = len(a)
    vals = sorted(((v, i) for i, v in enumerate(a)), reverse=True)
    order = sorted(range(len(queries)), key=lambda qi: -queries[qi][2])
    fw = Fenwick(n)
    ans = [0] * len(queries)
    k = 0
    for qi in order:
        l, r, x = queries[qi]
        while k < n and vals[k][0] >= x:
            fw.add(vals[k][1] + 1, 1)
            k += 1
        ans[qi] = fw.range_sum(l + 1, r + 1)
    return ans


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
    wizard_gap = [-1] * n           # -1 = not a wizard / first wizard: never >= d
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
    count_queries = []     # (lo, hi, d): how many wizard gaps >= d in [lo, hi]
    count_owner = []       # which original query each one belongs to

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
                count_queries.append((first + 1, r, d))
                count_owner.append(qi)

    # wizards after the first one search iff their gap >= d  -> offline count (notebook)
    counts = count_ge_offline(wizard_gap, count_queries)
    for qi, c in zip(count_owner, counts):
        answer_count[qi] += c

    return [f"{answer_count[qi]} {answer_d[qi]}" for qi in range(q)]


def main():
    t = int(input())
    out = []
    for _ in range(t):
        out.extend(solve())
    print('\n'.join(out))


main()

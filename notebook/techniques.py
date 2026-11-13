"""Greedy + common techniques page. Self-test: python3 techniques.py

GREEDY: guess a rule, then try to break it with a tiny counterexample before coding.
  max non-overlapping intervals        -> sort by END, take if start >= last end
  min points/arrows hitting intervals  -> sort by END, shoot at end
  min rooms / max overlap              -> sweep: +1 at start, -1 at end, sorted events
  schedule to minimize lateness        -> sort by deadline
  minimize sum of waiting times        -> shortest job first
  pair up to minimize max pair sum     -> sort, pair smallest with largest (two pointers)
  merge cost (always join 2 smallest)  -> heap (Huffman)
  exchange argument: if swapping two adjacent items never helps, the sort key is right
     e.g. sort by a/b  -> compare with cross-multiplication: key=cmp_to_key
TECHNIQUES
  many "add v to a[l..r]" then read all -> difference array
  coordinates up to 1e9 but n small     -> coordinate compression
  pairs/triples with sum target, sorted -> two pointers
  longest window with property          -> sliding window (grow right, shrink left)
  n <= 40, subset sums                  -> meet in the middle
  count subarrays with sum k            -> prefix sum + Counter of seen prefixes
  minimize the maximum / maximize min   -> binary search on the answer (math_nt.first_true)
"""
import heapq
from bisect import bisect_left, bisect_right
from collections import Counter
from functools import cmp_to_key


def max_non_overlapping(intervals):
    """[(s, e)] closed intervals; touching at an endpoint counts as overlapping"""
    cnt, last = 0, float('-inf')
    for s, e in sorted(intervals, key=lambda x: x[1]):
        if s > last:
            cnt += 1
            last = e
    return cnt


def max_overlap(intervals):
    """max intervals covering one point; [s, e) half-open. Ends sort before starts at ties."""
    ev = []
    for s, e in intervals:
        ev.append((s, 1))
        ev.append((e, -1))
    ev.sort()
    cur = best = 0
    for _, d in ev:
        cur += d
        best = max(best, cur)
    return best


def huffman_cost(a):
    """repeatedly merge the two smallest; cost = sum of merged values"""
    h = list(a)
    heapq.heapify(h)
    cost = 0
    while len(h) > 1:
        x = heapq.heappop(h) + heapq.heappop(h)
        cost += x
        heapq.heappush(h, x)
    return cost


def diff_array(n, updates):
    """updates = [(l, r, v)] add v to a[l..r] inclusive. O(n + q)."""
    D = [0] * (n + 1)
    for l, r, v in updates:
        D[l] += v
        D[r + 1] -= v
    out, cur = [], 0
    for i in range(n):
        cur += D[i]
        out.append(cur)
    return out


def compress(a):
    """values -> 0..k-1 keeping order. Returns (ranks, sorted unique values)."""
    vals = sorted(set(a))
    idx = {v: i for i, v in enumerate(vals)}
    return [idx[x] for x in a], vals


def two_sum_sorted(a, target):
    """a sorted. returns indices (i, j), i < j, with a[i] + a[j] == target, or None"""
    i, j = 0, len(a) - 1
    while i < j:
        s = a[i] + a[j]
        if s == target:
            return i, j
        if s < target:
            i += 1
        else:
            j -= 1
    return None


def longest_window_at_most_k_distinct(a, k):
    """sliding window template: grow right, shrink left while invalid"""
    cnt, left, best = Counter(), 0, 0
    for right, x in enumerate(a):
        cnt[x] += 1
        while len(cnt) > k:
            cnt[a[left]] -= 1
            if cnt[a[left]] == 0:
                del cnt[a[left]]
            left += 1
        best = max(best, right - left + 1)
    return best


def count_subarrays_sum(a, k):
    """number of (l, r) with sum(a[l..r]) == k. Works with negatives."""
    seen, pre, total = Counter({0: 1}), 0, 0
    for x in a:
        pre += x
        total += seen[pre - k]
        seen[pre] += 1
    return total


def subset_sums(a):
    sums = [0]
    for x in a:
        sums += [s + x for s in sums]
    return sums


def meet_in_middle_count(a, target):
    """number of subsets with sum == target, n <= ~40. O(2^(n/2) log)"""
    L = subset_sums(a[:len(a) // 2])
    R = sorted(subset_sums(a[len(a) // 2:]))
    return sum(bisect_right(R, target - s) - bisect_left(R, target - s) for s in L)


def sort_by_ratio(items):
    """items (a, b) with b > 0, sort by a/b ascending WITHOUT floats"""
    return sorted(items, key=cmp_to_key(lambda x, y: x[0] * y[1] - y[0] * x[1]))


# bit tricks: x & -x lowest bit | x & (x-1) drop lowest bit | bin(x).count('1') popcount
# iterate submasks of m: s = m; while s: ...; s = (s - 1) & m
# x >> i & 1  is bit i      | 1 << n  is 2^n          | x.bit_length()


if __name__ == "__main__":
    import random
    from itertools import combinations
    for _ in range(500):
        iv = []
        for _ in range(random.randint(0, 8)):
            s = random.randint(0, 15)
            iv.append((s, s + random.randint(0, 6)))
        best = 0
        for r in range(len(iv) + 1):
            for c in combinations(iv, r):
                if all(x[1] < y[0] or y[1] < x[0] for x, y in combinations(c, 2)):
                    best = max(best, r)
        assert max_non_overlapping(iv) == best
        ho = [(s, e) for s, e in iv if s < e]
        assert max_overlap(ho) == max([sum(1 for s, e in ho if s <= t < e) for t in range(25)] + [0])
        n = random.randint(1, 10)
        ups = [(l, random.randint(l, n - 1), random.randint(-5, 5)) for l in [random.randrange(n) for _ in range(6)]]
        brute = [0] * n
        for l, r, v in ups:
            for i in range(l, r + 1):
                brute[i] += v
        assert diff_array(n, ups) == brute
        a = [random.randint(-5, 5) for _ in range(random.randint(0, 10))]
        rk, vals = compress(a)
        assert [vals[r] for r in rk] == a and vals == sorted(set(a))
        sa = sorted(a)
        t = random.randint(-10, 10)
        res = two_sum_sorted(sa, t)
        exists = any(sa[i] + sa[j] == t for i in range(len(sa)) for j in range(i + 1, len(sa)))
        assert (res is not None) == exists and (res is None or sa[res[0]] + sa[res[1]] == t)
        k = random.randint(1, 3)
        assert longest_window_at_most_k_distinct(a, k) == max([j - i for i in range(len(a)) for j in range(i + 1, len(a) + 1) if len(set(a[i:j])) <= k] + [0])
        assert count_subarrays_sum(a, t) == sum(1 for i in range(len(a)) for j in range(i + 1, len(a) + 1) if sum(a[i:j]) == t)
        b = [random.randint(1, 9) for _ in range(random.randint(0, 10))]
        tt = random.randint(0, 30)
        assert meet_in_middle_count(b, tt) == sum(1 for s in subset_sums(b) if s == tt)
        if b:
            def bh(p):
                if len(p) == 1:
                    return 0
                return min(p[i] + p[j] + bh([p[x] for x in range(len(p)) if x not in (i, j)] + [p[i] + p[j]])
                           for i in range(len(p)) for j in range(i + 1, len(p)))
            if len(b) <= 6:
                assert huffman_cost(b) == bh(b)
        it = [(random.randint(0, 9), random.randint(1, 9)) for _ in range(6)]
        srt = sort_by_ratio(it)
        assert all(srt[i][0] / srt[i][1] <= srt[i + 1][0] / srt[i + 1][1] + 1e-12 for i in range(len(srt) - 1))
    print("techniques: all tests passed")

"""Strings page. Self-test: python3 strings.py

SPOT IT
  find pattern in text, count occurrences  -> KMP prefix function or Z  (or s.find / s.count
                                              for small inputs: .count is NON-overlapping!)
  period / smallest repeating unit         -> prefix function: p = n - pi[-1], if n % p == 0
  compare many substrings fast             -> rolling hash (two mods)
  longest palindromic substring            -> Manacher O(n)  (or expand-around-center O(n^2))
  many words, prefix queries               -> trie (dict of dicts)
  sorted suffixes / distinct substrings    -> suffix array (O(n log^2 n) below)
Python: s[::-1], ''.join(list), ord(c)-97, chr(97+i), str.startswith, collections.Counter(s)
Build strings with a list + ''.join, never s += c in a loop.
"""


def prefix_function(s):
    """pi[i] = length of longest proper prefix of s[:i+1] that is also its suffix"""
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        k = pi[i - 1]
        while k and s[i] != s[k]:
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    return pi


def kmp_find(text, pat):
    """all start indices of pat in text (overlapping allowed)"""
    if not pat:
        return list(range(len(text) + 1))
    s = pat + '\x00' + text
    pi = prefix_function(s)
    m = len(pat)
    return [i - 2 * m for i in range(len(s)) if pi[i] == m]


def z_function(s):
    """z[i] = length of longest common prefix of s and s[i:]  (z[0] = n)"""
    n = len(s)
    z = [0] * n
    if n:
        z[0] = n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z


class Hash:
    """rolling hash with two mods. h.get(l, r) = hash of s[l:r] (half-open).
    Equal substrings <=> equal hashes (with overwhelming probability)."""
    M1, M2, B = 10**9 + 7, 998244353, 131

    def __init__(self, s):
        n = len(s)
        M1, M2, B = self.M1, self.M2, self.B
        self.h1 = h1 = [0] * (n + 1)
        self.h2 = h2 = [0] * (n + 1)
        self.p1 = p1 = [1] * (n + 1)
        self.p2 = p2 = [1] * (n + 1)
        for i, ch in enumerate(s):
            c = ord(ch)
            h1[i + 1] = (h1[i] * B + c) % M1
            h2[i + 1] = (h2[i] * B + c) % M2
            p1[i + 1] = p1[i] * B % M1
            p2[i + 1] = p2[i] * B % M2

    def get(self, l, r):
        return ((self.h1[r] - self.h1[l] * self.p1[r - l]) % self.M1,
                (self.h2[r] - self.h2[l] * self.p2[r - l]) % self.M2)


def manacher(s):
    """returns (start, length) of the longest palindromic substring, O(n)"""
    t = '^#' + '#'.join(s) + '#$'
    n = len(t)
    P = [0] * n
    c = r = 0
    for i in range(1, n - 1):
        if i < r:
            P[i] = min(r - i, P[2 * c - i])
        while t[i + P[i] + 1] == t[i - P[i] - 1]:
            P[i] += 1
        if i + P[i] > r:
            c, r = i, i + P[i]
    length, center = max((v, i) for i, v in enumerate(P))
    return (center - length) // 2, length


class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, w):
        node = self.root
        for ch in w:
            node = node.setdefault(ch, {})
            node['#'] = node.get('#', 0) + 1      # words passing through here
        node['$'] = node.get('$', 0) + 1          # words ending here

    def count_prefix(self, p):
        node = self.root
        for ch in p:
            if ch not in node:
                return 0
            node = node[ch]
        return node.get('#', 0)                   # number of words starting with p (p non-empty)

    def contains(self, w):
        node = self.root
        for ch in w:
            if ch not in node:
                return False
            node = node[ch]
        return node.get('$', 0) > 0


def suffix_array(s):
    """O(n log^2 n) prefix doubling. sa[i] = start of i-th smallest suffix."""
    n = len(s)
    rank = [ord(c) for c in s]
    sa = list(range(n))
    k = 1
    while True:
        key = lambda i: (rank[i], rank[i + k] if i + k < n else -1)
        sa.sort(key=key)
        new = [0] * n
        for j in range(1, n):
            new[sa[j]] = new[sa[j - 1]] + (key(sa[j]) != key(sa[j - 1]))
        rank = new
        if n == 0 or rank[sa[-1]] == n - 1:
            return sa
        k <<= 1


def lcp_array(s, sa):
    """Kasai: lcp[i] = common prefix of suffixes sa[i] and sa[i+1].
    distinct substrings = n(n+1)/2 - sum(lcp)"""
    n = len(s)
    rank = [0] * n
    for i, p in enumerate(sa):
        rank[p] = i
    lcp, h = [0] * max(n - 1, 0), 0
    for i in range(n):
        if rank[i] + 1 < n:
            j = sa[rank[i] + 1]
            while i + h < n and j + h < n and s[i + h] == s[j + h]:
                h += 1
            lcp[rank[i]] = h
            if h:
                h -= 1
        else:
            h = 0
    return lcp


def min_rotation(s):
    """index of lexicographically smallest rotation (Booth-like, O(n))"""
    s2, n = s + s, len(s)
    i, j, k = 0, 1, 0
    while i < n and j < n and k < n:
        a, b = s2[i + k], s2[j + k]
        if a == b:
            k += 1
            continue
        if a > b:
            i += k + 1
        else:
            j += k + 1
        if i == j:
            j += 1
        k = 0
    return min(i, j)


if __name__ == "__main__":
    import random
    for _ in range(1500):
        s = ''.join(random.choice('ab') for _ in range(random.randint(0, 14)))
        p = ''.join(random.choice('ab') for _ in range(random.randint(1, 3)))
        assert kmp_find(s, p) == [i for i in range(len(s) - len(p) + 1) if s[i:i + len(p)] == p]
        pi = prefix_function(s)
        for i in range(len(s)):
            assert pi[i] == max(k for k in range(i + 1) if s[:k] == s[i + 1 - k:i + 1])
        z = z_function(s)
        for i in range(len(s)):
            k = 0
            while i + k < len(s) and s[k] == s[i + k]:
                k += 1
            assert z[i] == k
        if s:
            st, L = manacher(s)
            assert s[st:st + L] == s[st:st + L][::-1]
            assert L == max(j - i for i in range(len(s)) for j in range(i + 1, len(s) + 1) if s[i:j] == s[i:j][::-1])
            sa = suffix_array(s)
            assert sa == sorted(range(len(s)), key=lambda i: s[i:])
            lcp = lcp_array(s, sa)
            distinct = len({s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)})
            assert len(s) * (len(s) + 1) // 2 - sum(lcp) == distinct
            r = min_rotation(s)
            assert s[r:] + s[:r] == min(s[i:] + s[:i] for i in range(len(s)))
            h = Hash(s)
            for _ in range(10):
                a = random.randrange(len(s)); b = random.randint(a, len(s))
                c = random.randrange(len(s)); d = c + (b - a)
                if d <= len(s):
                    assert (h.get(a, b) == h.get(c, d)) == (s[a:b] == s[c:d])
    words = [''.join(random.choice('abc') for _ in range(random.randint(1, 4))) for _ in range(200)]
    tr = Trie()
    for w in words:
        tr.insert(w)
    for p in ['a', 'ab', 'abc', 'c', 'cc', 'bab']:
        assert tr.count_prefix(p) == sum(w.startswith(p) for w in words)
        assert tr.contains(p) == (p in words)
    print("strings: all tests passed")

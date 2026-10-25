# Shortest Missing Subsequences (Kattis shortestmissingsubsequences, difficulty 5.5)
# Idea: cut s greedily into blocks, each ending the moment it contains every letter
# of v. With k complete blocks, every string of length k is a subsequence (one letter
# per block) but some string of length k+1 is not, so the shortest missing length is
# L = k + 1. A query is a shortest missing subsequence iff len(q) == L and q is NOT a
# subsequence of s. Subsequence test: per-letter position lists + bisect.
import sys
from bisect import bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    v, s, n = data[0], data[1], int(data[2])
    need = len(v)
    k, seen = 0, set()
    for ch in s:
        seen.add(ch)
        if len(seen) == need:
            k += 1
            seen = set()
    L = k + 1

    pos = {}
    for i, ch in enumerate(s):
        pos.setdefault(ch, []).append(i)

    out = []
    for q in data[3:3 + n]:
        if len(q) != L:
            out.append("0")
            continue
        cur = -1
        missing = False
        for ch in q:
            lst = pos.get(ch)
            if not lst:
                missing = True
                break
            j = bisect_right(lst, cur)
            if j == len(lst):
                missing = True
                break
            cur = lst[j]
        out.append("1" if missing else "0")
    sys.stdout.write("\n".join(out) + "\n")

main()

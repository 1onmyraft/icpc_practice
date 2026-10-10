# Python standard library cheat sheet (only built-in modules, no installs)

Docs: https://docs.python.org/3/library/ (collections, heapq, bisect, itertools, functools, math)

## 1. Input and output
```python
import sys
input = sys.stdin.readline            # fast line reader; includes the trailing newline
n = int(input())                      # one integer
a, b = map(int, input().split())      # several integers on one line
arr = list(map(int, input().split())) # a list of integers
s = input().strip()                   # a string without the newline

data = sys.stdin.buffer.read().split()   # alternative: read everything, walk with an index

print(*arr)                           # numbers separated by spaces
print("\n".join(map(str, arr)))       # one per line, a single print call
print(f"{3.14159:.9f}")               # fixed decimals
```

## 2. Lists, sorting, tuples
```python
nums = [5, 2, 9, 1]
nums.sort()                           # in place
nums.sort(reverse=True)
pairs = [(2, "b"), (1, "z"), (2, "a")]
pairs.sort(key=lambda p: (p[0], p[1]))        # sort by first, then second
words = sorted(["bb", "a", "ccc"], key=len)   # returns a new list
total, biggest = sum(nums), max(nums)
best = max(pairs, key=lambda p: p[1])         # max by a key
grid = [[0] * 4 for _ in range(3)]            # 3 rows x 4 columns (NOT [[0]*4]*3)
prefix = [0]
for x in nums:
    prefix.append(prefix[-1] + x)             # prefix[i] = sum of the first i items
```

## 3. set and dict (hash tables, O(1) average)
```python
seen = set()
seen.add(3); seen.discard(3)          # discard does not raise if missing
print(3 in seen)                      # O(1); never test membership on a list

d = {}
d["x"] = 1
d["x"] = d.get("x", 0) + 1            # default if missing
for key, value in d.items():
    pass
print(sorted(d))                      # sorted keys
```

## 4. collections
```python
from collections import Counter, defaultdict, deque

c = Counter([1, 2, 2, 3, 3, 3])       # counts: c[3] == 3, c[99] == 0 (never KeyError)
print(c.most_common(1))               # [(3, 3)]
for value, count in c.items():
    pass

adj = defaultdict(list)               # graph adjacency list
adj[1].append(2); adj[2].append(1)
freq = defaultdict(int)               # auto 0
freq["a"] += 1

q = deque([1, 2, 3])                  # fast queue (BFS)
q.append(4); first = q.popleft()      # O(1) at both ends
```

## 5. heapq (min-heap)
```python
import heapq
h = []
heapq.heappush(h, (5, "a"))           # tuples compare by first item
heapq.heappush(h, (2, "b"))
smallest = heapq.heappop(h)           # (2, "b")
heapq.heapify(nums)                   # turn a list into a heap in O(n)
# max-heap trick: push negatives
mh = []                               # a separate heap (do not mix ints with tuples)
heapq.heappush(mh, -7); heapq.heappush(mh, -3)
largest = -heapq.heappop(mh)          # 7
```

## 6. bisect (binary search on a SORTED list)
```python
import bisect
a = [1, 3, 3, 5, 9]
bisect.bisect_left(a, 3)    # 1: first index with a[i] >= 3
bisect.bisect_right(a, 3)   # 3: first index with a[i] > 3
count_of_3 = bisect.bisect_right(a, 3) - bisect.bisect_left(a, 3)   # 2
bisect.insort(a, 4)         # insert and keep sorted (O(n) insert)
```

## 7. itertools and functools
```python
from itertools import permutations, combinations, product, accumulate
from functools import lru_cache, cmp_to_key

list(permutations([1, 2, 3], 2))      # ordered choices of 2
list(combinations([1, 2, 3], 2))      # unordered choices of 2
list(product([0, 1], repeat=3))       # all 3-bit strings
list(accumulate([1, 2, 3, 4]))        # [1, 3, 6, 10]: prefix sums

@lru_cache(maxsize=None)              # memoization for recursive DP
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

# custom comparator: return negative, 0, positive
nums.sort(key=cmp_to_key(lambda x, y: (x > y) - (x < y)))
```

## 8. math and numbers
```python
import math
math.gcd(12, 18)            # 6
math.isqrt(17)              # 4  (exact integer square root; never use int(x**0.5) for big x)
math.factorial(5)           # 120
math.comb(5, 2)             # 10 (n choose k, exact)
math.log2(8), math.ceil(7 / 2), 7 // 2, 7 % 2, divmod(7, 2)   # use // for integer division
pow(2, 10, 1_000_000_007)   # modular exponent: (2**10) % mod, fast
pow(3, -1, 11)              # modular inverse (Python 3.8+); for a prime p use pow(x, p-2, p)
float("inf")                # infinity for min/max initial values
```

## 9. Strings
```python
s = "hello world"
s.split()                   # ['hello', 'world']
" ".join(["a", "b"])        # 'a b'
s[::-1]                     # reverse
s.count("l"), s.find("o"), s.startswith("he")
ord("a"), chr(97)           # character <-> code
s.upper(), s.lower(), s.strip()
```

## 10. Safety settings and common mistakes
```python
import sys
sys.setrecursionlimit(1 << 20)        # deep recursion; for n above ~1e5 prefer an iterative stack
```
- `[[0]*m]*n` shares one row n times. Use `[[0]*m for _ in range(n)]`.
- Do not use `x in some_list` inside a loop. Use a set.
- `input()` returns a string, so convert with `int(...)`.
- Reading with `sys.stdin.readline` leaves a trailing newline; `.strip()` strings.
- `/` gives a float; `//` gives an integer.
- Sorting a list of tuples sorts by the first item, then the second, and so on.
- `list.pop(0)` and `list.insert(0, x)` are O(n). Use `deque`.
- Python has no built-in ordered set or sorted container. Use `bisect` on a sorted list, a heap, or switch to C++ `std::set`.

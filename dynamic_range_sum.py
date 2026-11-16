import math
import sys

input = sys.stdin.readline


n, q = map(int, input().split())

array = list(map(int, input().split()))

class Fenwick:
    def __init__(self, n_or_list):
        if isinstance(n_or_list, int):
            vals = [0] * n_or_list
        else:
            vals = list(n_or_list)
        self.n = n = len(vals)
        self.a = [0] + vals                 # plain values, so set() knows the old value
        self.T = T = self.a[:]
        for i in range(1, n + 1):           # O(n) build: push each box into its parent
            j = i + (i & -i)
            if j <= n:
                T[j] += T[i]

    def __len__(self):
        return self.n

    def add(self, i, d):            # a[i] += d
        self.a[i] += d
        T, n = self.T, self.n
        while i <= n:
            T[i] += d
            i += i & -i             # climb to every box that contains i

    def set(self, i, v):            # a[i] = v
        self.add(i, v - self.a[i])

    def get(self, i):
        return self.a[i]

    def prefix(self, i):            # a[1] + ... + a[i]
        T, s = self.T, 0
        while i > 0:
            s += T[i]
            i -= i & -i             # hop down the staircase
        return s

    def range_sum(self, l, r):      # a[l..r], 1-indexed inclusive
        return self.prefix(r) - self.prefix(l - 1)



fent = Fenwick(array)




output = []
for i in range(q):
    option, start, end = map(int, input().split())
    
    if option == 1:
        fent.set(start, end)
        continue
    
    output.append(str(fent.range_sum(start, end)))
    
    
print('\n'.join(output))
    
        
        
            
import sys
input = sys.stdin.readline

def mno(i):
    cnt, last = 0, float('-inf')
    
    for s, e in sorted(i, key= lambda x: x[1]):
        if s >= last:
            cnt += 1
            last = e
            
    return cnt
n = int(input())

# 3 
# 3 5
# 4 9 
# 5 8
# starting len
# 2, 3, 5
movies = [0]*n
for i in range(n):
    s, e = map(int, input().split())
    movies[i] = (s, e)
    
    
print(mno(movies))

    
    
    
    
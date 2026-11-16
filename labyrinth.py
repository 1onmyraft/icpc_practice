import sys

def main():
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    g = bytearray(b"".join(data[2:2 + n]))   # the whole grid as one flat array; cell (i, j) is g[i*m + j]
    FLOOR, WALL, A, B = ord('.'), ord('#'), ord('A'), ord('B')


  
    rooms = 0
    for start in range(n * m):
        if start < len(g) and g[start] == A:
            g[start] = WALL                   # mark visited by turning it into a wall
            stack = [start]
            parent = []
            parents = []
            last = None
            while stack:
                c = stack.pop()
                if last is not None:
                    parent.append(last)
                i, j = divmod(c, m)
                
                
                if i > 0  and c-m < len(g)   and g[c - m] == FLOOR:
                    g[c - m] = WALL; stack.append(c - m)   # up
                    last = 'U'
                if i < n - 1 and c+m < len(g) and g[c + m] == FLOOR:
                    g[c + m] = WALL; stack.append(c + m)   # down
                    last = 'D'
                if j > 0     and c-1 < len(g) and g[c - 1] == FLOOR:
                    g[c - 1] = WALL; stack.append(c - 1)   # left
                    last = 'L'
                if j < m - 1 and c+1 < len(g) and g[c + 1] == FLOOR:
                    g[c + 1] = WALL; stack.append(c + 1)   # right
                    last = 'R'
                    
                if i > 0  and c-m < len(g) and g[c - m] == B:
                    parent.append('U')
                    parents.append(parent.copy())
                if i < n - 1 and c+m < len(g) and g[c + m] == B:
                    parent.append('D')
                    parents.append(parent.copy())
                if j > 0     and c-1 < len(g) and g[c - 1] == B:
                    parent.append('L')
                    parents.append(parent.copy())
                    
                if j < m - 1 and c+1 < len(g) and g[c + 1] == B:
                    parent.append('R')
                    parents.append(parent.copy())
    return parents
                
                
a = main()
print(a)
if len(a) == 0:
    print('NO')
    exit()
answer = min(a, key=len)


if len(answer) == 0:
    print('NO')
else:
    print('YES')
    print(len(answer))
    print(''.join(answer))

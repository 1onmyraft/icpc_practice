import sys
input = sys.stdin.readline

t = int(input())
output = []
for _ in range(t):
    n, q, g = map(int, input().split())

    people = {}              # only keys that have been set
    count = {0: n}           # all n keys start at value 0

    for _ in range(q):
        line = input().split()
        if line[0] == 'P':
            s = int(line[1])
            for p in map(int, line[3:]):
                old = people.get(p, 0)      # missing key means value 0
                count[old] -= 1
                count[s] = count.get(s, 0) + 1
                people[p] = s
        else:
            output.append(count.get(int(line[1]), 0))

print('\n'.join(map(str, output)))

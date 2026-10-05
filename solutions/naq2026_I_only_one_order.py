import sys


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    t = int(data[pos]); pos += 1
    out = []
    for _ in range(t):
        n = int(data[pos]); m = int(data[pos + 1]); pos += 2
        consecutive = set()
        impossible = False
        for _ in range(m):
            a = int(data[pos]); b = int(data[pos + 1]); pos += 2
            if a > b:
                impossible = True
            elif b == a + 1:
                consecutive.add(a)
        if impossible:
            out.append(-1)
        else:
            out.append((n - 1) - len(consecutive))
    print("\n".join(map(str, out)))


main()

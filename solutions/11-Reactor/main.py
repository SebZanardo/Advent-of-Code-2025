from collections import defaultdict
import sys


def DFS(current, target, server, memo) -> int:
    if current == target:
        return 1

    # Handle case if target is 'out' or similar
    if current not in server:
        return 0

    if current not in memo:
        total = 0
        for path in server[current]:
            total += DFS(path, target, server, memo)
        memo[current] = total

    return memo[current]


# Try to read a path to an input file from command line arguments
path = sys.argv[1] if len(sys.argv) > 1 else "input.in"


# Parse input
server = {}
with open(path, "r") as f:
    for line in f.readlines():
        parts = line.strip().split()
        key = parts.pop(0)[:-1]
        server[key] = parts

# Part 1
# DFS
unique = DFS('you', 'out', server, defaultdict(int))
print(f"Part 1:\n{unique}\n")

# Part 2
# There are no loops in the input so only svr -> fft -> dac -> out is possible
# Use memoisation for length of each of these to save computation time
# We just need to find count not actual paths
# Total = (svr -> fft) * (fft -> dac) * (dac -> out)

unique = DFS('svr', 'fft', server, defaultdict(int))
unique *= DFS('fft', 'dac', server, defaultdict(int))
unique *= DFS('dac', 'out', server, defaultdict(int))
print(f"Part 2:\n{unique}\n")

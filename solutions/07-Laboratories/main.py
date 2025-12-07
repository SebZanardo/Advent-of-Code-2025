from queue import deque
import sys


EMPTY = '.'
SPLITTER = '^'
START = 'S'


def recursive(x: int, y: int, memo: dict[tuple[int, int], int]):
    # Continue to move stream down until hit the bottom or a splitter
    while y < height and manifold[y][x] != SPLITTER:
        y += 1

    # Hit the bottom, return 1
    if y == height:
        return 1

    if (x, y) not in memo:
        left = recursive(x - 1, y, memo)
        right = recursive(x + 1, y, memo)
        memo[(x, y)] = left + right

    return memo[(x, y)]


# Try to read a path to an input file from command line arguments
path = sys.argv[1] if len(sys.argv) > 1 else "input.in"


# Parse input
manifold = []
with open(path, "r") as f:
    for line in f.readlines():
        manifold.append(line.strip())

width = len(manifold[0])
height = len(manifold)

# Start should be in centre top row only
start = (width // 2, 0)
assert manifold[start[1]][start[0]] == START

# Don't need to worry about going out of bounds left, or right
# Stream can never move upwards so don't need to worry about that
for y in range(height):
    assert manifold[y][0] == EMPTY
    assert manifold[y][width - 1] == EMPTY

# Part 1
streams = deque()
streams.append(start)

# To record which splitters have been seen because we only want to count once
seen = set()

while streams:
    x, y = streams.popleft()
    y += 1

    # If at bottom of manifold, then skip
    if y >= height:
        continue

    # Ignore duplicate streams
    if (x, y) in seen:
        continue

    if manifold[y][x] == SPLITTER:
        seen.add((x, y))
        streams.append((x - 1, y))
        streams.append((x + 1, y))
    else:
        # Move down
        streams.append((x, y))

print(f"Part 1:\n{len(seen)}\n")

# Part 2
timelines = recursive(*start, {})
print(f"Part 2:\n{timelines}\n")

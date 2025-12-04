from queue import deque
import sys


DIRECTIONS = (
    (0, 1), (0, -1), (1, 0), (-1, 0),
    (1, 1), (1, -1), (-1, 1), (-1, -1)
)
EMPTY_CHAR = '.'
ROLL_CHAR = '@'
MAX_ROLLS = 4

# Try to read a path to an input file from command line arguments
path = sys.argv[1] if len(sys.argv) > 1 else "input.in"


# Parse input
grid = []
with open(path, "r") as f:
    for line in f.readlines():
        grid.append(line.strip())
width = len(grid[0])
height = len(grid)

# Part 1
accessible = 0
for y in range(height):
    for x in range(width):
        # Only perform check for cells with rolls
        if grid[y][x] != ROLL_CHAR:
            continue

        rolls = 0
        for d in DIRECTIONS:
            nx = x + d[0]
            ny = y + d[1]

            if nx < 0 or nx >= width or ny < 0 or ny >= height:
                continue

            if grid[ny][nx] == ROLL_CHAR:
                rolls += 1

                # Early exit condition
                if rolls >= MAX_ROLLS:
                    break

        if rolls < MAX_ROLLS:
            accessible += 1

print(f"Part 1:\n{accessible}\n")

# Part 2

# Keep track of how many adjacent for each roll
count_grid = [[0] * width for _ in range(height)]

# Initialise queue for rolls that can be removed by forklift
removeable_rolls = deque()

for y in range(height):
    for x in range(width):
        # Only perform check for cells with rolls
        if grid[y][x] != ROLL_CHAR:
            continue

        rolls = 0
        for d in DIRECTIONS:
            nx = x + d[0]
            ny = y + d[1]

            if nx < 0 or nx >= width or ny < 0 or ny >= height:
                continue

            if grid[ny][nx] == ROLL_CHAR:
                rolls += 1

        if rolls < MAX_ROLLS:
            # Add to queue as this roll can be removed
            removeable_rolls.append((x, y))
        else:
            # Only add roll counts to grid that are not in queue
            count_grid[y][x] = rolls

# Counter for how many times rolls were removed
accessible = 0

# Add to end and remove from start of queue until queue is empty
# Only need to check if adjacent rolls to removed roll are accessible
# If adjacent is accessible then append to end of queue
while removeable_rolls:
    x, y = removeable_rolls.popleft()
    accessible += 1

    for d in DIRECTIONS:
        nx = x + d[0]
        ny = y + d[1]

        if nx < 0 or nx >= width or ny < 0 or ny >= height:
            continue

        # There is a roll there that isn't in queue
        if count_grid[ny][nx] > 0:
            count_grid[ny][nx] -= 1

            # If is accessible add to queue and record in grid that in queue
            if count_grid[ny][nx] < MAX_ROLLS:
                removeable_rolls.append((nx, ny))
                count_grid[ny][nx] = 0

print(f"Part 2:\n{accessible}\n")

import sys


# Try to read a path to an input file from command line arguments
path = sys.argv[1] if len(sys.argv) > 1 else "input.in"


# Parse input
lines = []
with open(path, "r") as f:
    for line in f.readlines():
        lines.append(line)

# Last line is operations, not numbers so remove
operations = lines.pop().strip().split()

line_width = len(lines[0])
line_height = len(lines)

# Parse lines into 3D matrix of characters preserving spaces
problems = []
slice_start = 0
for x in range(line_width):
    # Check if column is all spaces
    empty = True

    for y in range(line_height):
        if lines[y][x] != ' ':
            empty = False
            break

    if not empty:
        continue

    # Slice string from last space to current space to preserve spacing
    row = []
    for y in range(line_height):
        row.append(lines[y][slice_start:x])
    problems.append(row)

    slice_start = x + 1
else:
    # Add last row
    row = []
    for y in range(line_height):
        row.append(lines[y][slice_start:x])
    problems.append(row)

width = len(problems)
height = len(problems[0])

# Part 1
total = 0
for x in range(width):
    problem_total = int(problems[x][0])
    operator = operations[x]

    for y in range(1, height):
        value = int(problems[x][y])
        if operator == '+':
            problem_total += value
        elif operator == '*':
            problem_total *= value

    total += problem_total

print(f"Part 1:\n{total}\n")

# Part 2
total = 0
for x in range(width):
    problem_total = int(''.join([problems[x][c][0] for c in range(height)]))
    operator = operations[x]

    for y in range(1, len(problems[x][0])):
        value = int(''.join([problems[x][c][y] for c in range(height)]))
        if operator == '+':
            problem_total += value
        elif operator == '*':
            problem_total *= value

    total += problem_total

print(f"Part 2:\n{total}\n")

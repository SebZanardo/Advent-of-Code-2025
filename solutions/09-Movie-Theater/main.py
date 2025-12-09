import sys


# https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
def line_line_intersecting(x1, y1, x2, y2, x3, y3, x4, y4) -> bool:
    denominator = (x2 - x1) * (y4 - y3) - (x4 - x3) * (y2 - y1)
    numerator1 = (x4 - x3) * (y1 - y3) - (x1 - x3) * (y4 - y3)
    numerator2 = (x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)

    if denominator == 0:
        return numerator1 == 0 and numerator2 == 0

    ua = numerator1 / denominator
    ub = numerator2 / denominator

    return ua >= 0 and ua <= 1 and ub >= 0 and ub <= 1


def get_bounds(x1, y1, x2, y2) -> tuple[int, int, int, int]:
    min_x = min(x1, x2)
    min_y = min(y1, y2)
    max_x = max(x1, x2)
    max_y = max(y1, y2)
    return (min_x, min_y, max_x, max_y)


def polygon_covers(points, bounds) -> bool:
    min_x, min_y, max_x, max_y = bounds

    # Inset because having issues with it overlapping on edges if coincident
    min_x += 0.1
    min_y += 0.1
    max_x -= 0.1
    max_y -= 0.1

    lines = (
        (min_x, min_y, max_x, min_y),
        (max_x, min_y, max_x, max_y),
        (max_x, max_y, min_x, max_y),
        (min_x, max_y, min_x, min_y),
    )

    # Iterate over edges of main shape and check for collisions with edges
    prev = points[-1]
    for i in range(len(points)):
        curr = points[i]

        for line in lines:
            if line_line_intersecting(*line, *prev, *curr):
                return False

        prev = curr

    return True


# Try to read a path to an input file from command line arguments
path = sys.argv[1] if len(sys.argv) > 1 else "input.in"


# Parse input
points = []
with open(path, "r") as f:
    for line in f.readlines():
        points.append(tuple([int(i) for i in line.split(',')]))

# Part 1
largest_area = 0
for i in range(len(points)):
    for j in range(i + 1, len(points)):
        width = abs(points[i][0] - points[j][0]) + 1
        height = abs(points[i][1] - points[j][1]) + 1
        area = width * height
        if area > largest_area:
            largest_area = area

print(f"Part 1:\n{largest_area}\n")

# Part 2
largest_area = 0

# Because polygon covers function is expensive, calculate and sort rectangles
rectangles = []

for i in range(len(points)):
    for j in range(i + 1, len(points)):
        bounds = get_bounds(*points[i], *points[j])
        min_x, min_y, max_x, max_y = bounds

        area = (max_x - min_x + 1) * (max_y - min_y + 1)

        rectangles.append((area, bounds))

for area, bounds in sorted(rectangles, reverse=True):
    if polygon_covers(points, bounds):
        largest_area = area
        break

print(f"Part 2:\n{largest_area}\n")

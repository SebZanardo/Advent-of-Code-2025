import sys


def inside_ranges(ingredient: int, ranges: list[tuple[int, int]]) -> bool:
    for left, right in ranges:
        if ingredient >= left and ingredient <= right:
            return True
    return False


# Try to read a path to an input file from command line arguments
path = sys.argv[1] if len(sys.argv) > 1 else "input.in"


# Parse input
ranges = []
ingredients = []

# Walrus operator is king here
with open(path, "r") as f:
    while line := f.readline().strip():
        ranges.append(tuple([int(i) for i in line.split('-')]))

    while line := f.readline().strip():
        ingredients.append(int(line))

# Merge overlapping ranges
merged_ranges = []

# Sorting first ensures we don't miss any merges
for pair in sorted(ranges):
    # Add first range because nothing to compare to yet
    if len(merged_ranges) == 0:
        merged_ranges.append(pair)
        continue

    # Remove last range pair
    last_pair = merged_ranges.pop()

    if pair[0] <= last_pair[1]:
        # Merge current and last range pair
        merged_ranges.append(
            (min(pair[0], last_pair[0]), max(pair[1], last_pair[1]))
        )
    else:
        # Distinct ranges so just add both separately
        merged_ranges.append(last_pair)
        merged_ranges.append(pair)

# Part 1
fresh = 0
for ingredient in ingredients:
    # Check if inside one of the merged ranges
    if inside_ranges(ingredient, merged_ranges):
        fresh += 1

print(f"Part 1:\n{fresh}\n")

# Part 2
fresh = 0
# Iterating over merged ranges ensures we haven't counted any double ups
for left, right in merged_ranges:
    fresh += right - left + 1

print(f"Part 2:\n{fresh}\n")

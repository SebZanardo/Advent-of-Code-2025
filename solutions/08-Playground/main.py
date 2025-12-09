import heapq
import math
import sys


REPEAT_TIMES = 1000
TOP_N = 3


# Try to read a path to an input file from command line arguments
path = sys.argv[1] if len(sys.argv) > 1 else "input.in"


# Parse input
positions = []
with open(path, "r") as f:
    for line in f.readlines():
        positions.append(tuple([int(i) for i in line.split(',')]))

# Part 1

# Calculate distances between all positions
distances = []
for i in range(len(positions)):
    for j in range(i + 1, len(positions)):
        ax, ay, az = positions[i]
        bx, by, bz = positions[j]
        # No need to square root as just comparing distances
        d = (ax - bx) ** 2 + (ay - by) ** 2 + (az - bz) ** 2
        distances.append((d, i, j))

# Hashmap to assign boxes to groups
box_groups = {}

# Hashmap to assign groups to boxes
group_boxes = {}

# Keep track of next unique group index
group_index = 0
repeat_times = REPEAT_TIMES

for d, i, j in sorted(distances):
    if repeat_times <= 0:
        break

    i_group = box_groups.get(i)
    j_group = box_groups.get(j)

    group_index += 1
    new_group = []

    # NOTE: Being lazy here, can handle more cases to move less around. There
    # is no need to create a new group and perform copy and delete everytime
    # we see one of the boxes is in a group

    # Remove old groups from both hashmaps and create new group
    if not i_group:
        new_group.append(i)
    else:
        for b in group_boxes[i_group]:
            new_group.append(b)
        del group_boxes[i_group]

    if not j_group:
        new_group.append(j)
    elif i_group != j_group:
        for b in group_boxes[j_group]:
            new_group.append(b)
        del group_boxes[j_group]

    # Create new group
    group_boxes[group_index] = set(new_group)
    for b in new_group:
        box_groups[b] = group_index

    repeat_times -= 1

longest_circuit_lengths = heapq.nlargest(
    TOP_N, [len(g) for g in group_boxes.values()] + [1] * TOP_N
)

print(f"Part 1:\n{math.prod(longest_circuit_lengths)}\n")

# Part 2

# Hashmap to assign boxes to groups
box_groups = {}

# Hashmap to assign groups to boxes
group_boxes = {}

# Keep track of next unique group index
group_index = 0

solution = 0

for d, i, j in sorted(distances):
    i_group = box_groups.get(i)
    j_group = box_groups.get(j)

    group_index += 1
    new_group = []

    # NOTE: Being lazy here, can handle more cases to move less around. There
    # is no need to create a new group and perform copy and delete everytime
    # we see one of the boxes is in a group

    # Remove old groups from both hashmaps and create new group
    if not i_group:
        new_group.append(i)
    else:
        for b in group_boxes[i_group]:
            new_group.append(b)
        del group_boxes[i_group]

    if not j_group:
        new_group.append(j)
    elif i_group != j_group:
        for b in group_boxes[j_group]:
            new_group.append(b)
        del group_boxes[j_group]

    # Create new group
    group_boxes[group_index] = set(new_group)
    for b in new_group:
        box_groups[b] = group_index

    # Check if all in one circuit
    if len(group_boxes[group_index]) == len(positions):
        # Multiply X positions
        solution = positions[i][0] * positions[j][0]
        break

print(f"Part 2:\n{solution}\n")

import sys


def repeating(id_string: str, times: int) -> bool:
    if len(id_string) % times != 0:
        return False

    part_length = len(id_string) // times

    for i in range(part_length):
        last = id_string[i]
        for j in range(times):
            new = id_string[j * part_length + i]
            if new != last:
                return False
            last = new

    return True


# Try to read a path to an input file from command line arguments
path = sys.argv[1] if len(sys.argv) > 1 else "input.in"


# Parse input
id_ranges = []
with open(path, "r") as f:
    id_ranges = [
        tuple([int(i) for i in r.split('-')]) for r in f.readline().split(',')
    ]

# Part 1
count = 0
for left, right in id_ranges:
    for id_int in range(left, right+1):
        id_string = str(id_int)

        if not repeating(id_string, 2):
            continue

        count += id_int

print(f"Part 1:\n{count}\n")

# Part 2
count = 0
for left, right in id_ranges:
    for id_int in range(left, right+1):
        id_string = str(id_int)

        passed = False

        for i in range(2, len(id_string)+1):
            if repeating(id_string, i):
                passed = True
                break

        if passed:
            count += id_int

print(f"Part 2:\n{count}\n")

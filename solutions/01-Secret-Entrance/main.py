import sys


# Try to read a path to an input file from command line arguments
path = sys.argv[1] if len(sys.argv) > 1 else "input.in"

# Parse input
# Array of positive and negative numbers
rotations = []
with open(path, "r") as f:
    for line in f.readlines():
        letter = line[0]
        number = int(line[1:])

        # Checks to ensure input is as expected
        assert letter in 'LR'
        assert number != 0

        rotations.append(-number if letter == 'L' else number)

# Part 1
pointing = 50
password = 0
for distance in rotations:
    pointing = (pointing + distance) % 100

    if pointing == 0:
        password += 1

print(f"Part 1:\n{password}\n")

# Part 2
pointing = 50
password = 0
for distance in rotations:
    # Need to store last pointing direction before changing it to compare
    last_pointing = pointing
    pointing = (pointing + distance) % 100

    if pointing == 0:
        # Ended rotation facing zero
        password += 1
    elif last_pointing != 0:
        # If turned right and on left of starting position then looped once
        if distance > 0 and pointing < last_pointing:
            password += 1
        # If turned left and on right of starting position then looped once
        elif distance < 0 and pointing > last_pointing:
            password += 1

    # Counts full rotations
    password += abs(distance) // 100

print(f"Part 2:\n{password}\n")

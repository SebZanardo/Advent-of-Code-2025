import sys


def max_joltage(bank: str, digits: int) -> int:
    # Ensure input is valid
    assert digits >= 1
    assert digits < len(bank)

    best = [i for i in range(digits)]

    for i in range(1, len(bank)):
        battery = bank[i]

        # Iterate over all digits ( in order )
        for j in range(digits):
            # Are we overwritting previously set number
            if j > 0 and i <= best[j - 1]:
                continue

            # Do we have space to update preceeding digits without overrun
            if i >= len(bank) - (digits - j - 1):
                continue

            # Is current battery better
            if battery > bank[best[j]]:
                for k in range(digits - j):
                    best[j + k] = i + k
                break

    maximum_joltage = int(''.join([bank[best[i]] for i in range(digits)]))

    return maximum_joltage


# Try to read a path to an input file from command line arguments
path = sys.argv[1] if len(sys.argv) > 1 else "input.in"


# Parse input
banks = []
with open(path, "r") as f:
    for line in f.readlines():
        banks.append(line.strip())

# Part 1
total = 0
for bank in banks:
    total += max_joltage(bank, 2)

print(f"Part 1:\n{total}\n")

# Part 2
total = 0
for bank in banks:
    total += max_joltage(bank, 12)

print(f"Part 2:\n{total}\n")

# I had to do external research and look at other solutions to write this
#
# I have never used a SAT solver for competitive programming before so I found
# this interesting to learn about. Definitely going to come in handy in the
# future!

# https://z3prover.github.io/papers/programmingz3.html


import sys
import z3  # You will need to import z3-solver to run this solution


# Try to read a path to an input file from command line arguments
path = sys.argv[1] if len(sys.argv) > 1 else "input.in"

# Parse input
manual = []
with open(path, "r") as f:
    for line in f.readlines():
        split_line = line.split()

        indicator = split_line[0][1:-1]

        wiring = split_line[1:-1]
        for i, button in enumerate(wiring):
            wiring[i] = [int(v) for v in button[1:-1].split(',')]

        joltage = [int(v) for v in split_line[-1][1:-1].split(',')]
        manual.append((indicator, wiring, joltage))


# Part 2
total_pressed = 0

for target, wiring, joltage in manual:
    opt = z3.Optimize()

    # Convert each button into a constraint. Value cannot be less than zero
    button_list = []

    # Convert buttons switches into bit array for constraint solver
    # (1, 4, 5) -> [0, 1, 0, 0, 1, 1]
    button_definitions = []

    for i, button in enumerate(wiring):
        b = z3.Int(f"b{i}")
        button_list.append(b)
        opt.add(b >= 0)

        definition = [0] * len(target)
        for index in button:
            definition[index] = 1
        button_definitions.append(definition)

    # Add constraint that total presses for each index needs to equal joltage
    for i in range(len(target)):
        opt.add(
            z3.Sum(
                button_definitions[v][i] * button_list[v]
                for v in range(len(wiring))
            ) == joltage[i]
        )

    # Tell the SAT solver we want to minimize the number of presses
    opt.minimize(z3.Sum(button_list))

    # All problems in manual should have a valid solution
    assert opt.check() == z3.sat

    # Count how many were pressed for each button in the best solution
    min_pressed = [opt.model()[button_list[i]].as_long()
                   for i in range(len(wiring))]

    # Sum presses and add to total pressed
    total_pressed += sum(min_pressed)

print(f"Part 2:\n{total_pressed}\n")

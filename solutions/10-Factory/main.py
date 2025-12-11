from queue import deque
import sys


ON = '#'
OFF = '.'


def BFS(target: str, buttons: list[list[int]]) -> list[int]:
    # Indicators start empty
    current = OFF * len(target)

    # BFS search. Search space is small as indicator length is short.
    queue = deque()
    queue.append(current)

    # Record which configurations we have seen to save memory and computation
    seen = set()
    seen.add(current)

    steps = 0

    while queue:
        # Loop over nodes from last step
        for _ in range(len(queue)):
            current = queue.popleft()

            # If current is the target break
            if current == target:
                return steps

            for button in buttons:
                # Copy current into list so can modify
                new_current = list(current)

                for i in button:
                    # Press indexes for button and toggle string
                    new_current[i] = ON if new_current[i] == OFF else OFF

                # Convert char array into string so immutable for hashset
                new_current = ''.join(new_current)

                # Check if in seen hashset
                if new_current in seen:
                    continue

                # If new then add to seen and queue
                seen.add(new_current)
                queue.append(new_current)
        steps += 1


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

# Part 1
total_presses = 0

# Can ignore joltage for part 1
for machine in manual:
    indicator, wiring, joltage = machine
    total_presses += BFS(indicator, wiring)

print(f"Part 1:\n{total_presses}\n")

# Part 2
# NOTE: Couldn't solve this...


def backwards_BFS(
    target: str, buttons: list[list[int]], joltage: list[int]
) -> int:
    steps = 0

    # Same as before but start at end and unpress buttons to get joltage and
    # indicator blank. Should be good enough as there are lots of ways
    # to cut down on time
    #
    # In hindsight this was not true...

    start = [OFF] * len(target)
    start_jolts = tuple([0] * len(target))

    # Indicators start empty at end position
    current = target
    jolts = tuple(joltage.copy())

    pair = (current, jolts)

    # BFS search. Search space is small as indicator length is short.
    queue = deque()
    queue.append(pair)

    # Record which configurations we have seen to save memory and computation
    seen = set()
    seen.add(pair)

    steps = 0

    while queue:
        # Loop over nodes from last step
        for _ in range(len(queue)):
            current, jolts = queue.popleft()

            # If current is start
            if current == start and jolts == start_jolts:
                return steps

            for button in buttons:
                # Copy current into list so can modify
                new_current = list(current)
                new_jolts = list(jolts)

                valid = True
                for i in button:
                    # Press indexes for button and toggle string
                    new_current[i] = ON if new_current[i] == OFF else OFF
                    new_jolts[i] -= 1

                    if new_jolts[i] < 0:
                        valid = False

                # Went into negative jolts so not allowed
                if not valid:
                    continue

                # Convert char array into string so immutable for hashset
                new_current = ''.join(new_current)
                new_jolts = tuple(new_jolts)

                pair = (new_current, new_jolts)

                # Check if in seen hashset
                if pair in seen:
                    continue

                # If new then add to seen and queue
                seen.add(pair)
                queue.append(pair)
        steps += 1

    return steps - 1


# NOTE: Not fully implemented as wasn't sure how to go about counting steps
# in a fast way once we know if solvable or not with remaining joltage
def extended_BFS(
    target: str, buttons: list[list[int]], joltage: list[int]
) -> int:
    # Do previous approach except when we find a solution see if pressing
    # buttons remaining number of times keeps in solved state. Order of presses
    # doesn't matter as it is basically XOR.

    # Indicators start empty
    current = OFF * len(target)
    pressed = tuple([0] * len(target))

    pair = current, pressed

    # BFS search. Search space is small as indicator length is short.
    queue = deque()
    queue.append(pair)

    # Record which configurations we have seen to save memory and computation
    seen = set()
    seen.add(pair)

    steps = 0

    while queue:
        # Loop over nodes from last step
        for _ in range(len(queue)):
            current, pressed = queue.popleft()

            # If current is the target then attempt to complete solve
            if current == target:

                # We know if it is possible if each joltage is even because it
                # will toggle back to solved state
                possible = True
                for v in pressed:
                    if v % 2 != 0:
                        possible = False

                if possible:
                    # NOTE: Counting steps here I got no clue other than some
                    # maths solution. A search is too slow as seen above
                    print("possible!!!", target)
                    return steps

            for button in buttons:
                # Copy current into list so can modify
                new_current = list(current)
                new_pressed = list(pressed)

                for i in button:
                    # Press indexes for button and toggle string
                    new_current[i] = ON if new_current[i] == OFF else OFF
                    new_pressed[i] += 1

                # Convert char array into string so immutable for hashset
                new_current = ''.join(new_current)
                new_pressed = tuple(new_pressed)

                pair = (new_current, new_pressed)

                # Check if in seen hashset
                if pair in seen:
                    continue

                # If new then add to seen and queue
                seen.add(pair)
                queue.append(pair)

        steps += 1


print("Part 2:\nUnsolved ;(\n")

total_presses = 0

# Can ignore joltage for part 1
for machine in manual:
    indicator, wiring, joltage = machine
    # NOTE: Tried backwards BFS from solution but wayyyy too slow for anything
    # other than test input
    # extended_BFS(indicator, wiring, joltage)
    steps = backwards_BFS(indicator, wiring, joltage)
    print(steps)
    total_presses += steps

print("answer=", total_presses)

#! /usr/bin/env python3

# Advent of Code 22 - Day 5


def load_stacks(fp: str) -> tuple[list[str], list[str]]:
    """
    Loads information from file and returns a tuple of the lines
    related to crates and the lines related to instructions.
    """

    with open(fp, "r") as f:
        content = f.read()

    piles, instructions = content.split("\n\n")

    piles = piles.split("\n")[:-1]
    instructions = instructions.split("\n")[:-1]

    return piles, instructions


def create_stacks(piles: list[str]) -> list[list[str]]:
    """
    Takes a list of lines of the piles as input and returns
    a list of the stacks from bottom to top. Higher indexes mean a higher position
    """

    stack_amount = (len(piles[0]) + 1) // 4  # 4 = 3 chars + 1 space `[A] `

    stacks = [list() for _ in range(stack_amount)]
    for line in piles:
        for i in range(stack_amount):
            crate = line[i * 4 + 1]
            if crate != " ":
                stacks[i].insert(0, crate)

    return stacks


def parse_instructions(instructions: list[str]) -> list[tuple[int, int, int]]:
    """
    Transform written instructions into `(amount, src, dst)` tuples.
    """

    output = []
    for line in instructions:
        words = line.split(" ")
        output.append((int(words[1]), int(words[3]), int(words[5])))

    return output


def move(
    stacks: list[list[str]], instruction: tuple[int, int, int], keep_order: bool = False
) -> list[list[str]]:
    """
    `instruction` should be `(amount, src, dst)` where `src` and `dst` are the stack number (NOT list index).

    If `keep_order` is `True`, multiple crates are moved at the same time, preserving their order after the change.

    Returns the result of moving `amount` crates from `stacks[src - 1]` to `stacks[dst - 1]`.
    """

    amount, src, dst = instruction

    if not keep_order:
        for _ in range(amount):
            stacks[dst - 1].append(stacks[src - 1].pop(-1))

    else:
        to_move = list()
        for _ in range(amount):
            to_move.insert(0, stacks[src - 1].pop(-1))
        stacks[dst - 1].extend(to_move)

    return stacks


def main(fp: str = "05/sample.txt"):
    # Part 1
    piles, instructions = load_stacks(fp)
    stacks = create_stacks(piles)
    instructions = parse_instructions(instructions)

    for instruction in instructions:
        stacks = move(stacks, instruction, False)

    print("".join([stack[-1] for stack in stacks]))

    # Part 2
    stacks = create_stacks(piles)
    for instruction in instructions:
        stacks = move(stacks, instruction, True)

    print("".join([stack[-1] for stack in stacks]))


if __name__ == "__main__":
    main("05/input.txt")

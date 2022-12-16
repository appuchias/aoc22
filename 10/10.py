#! /usr/bin/env python3

# Advent of Code 22 - Day 10


def load_instructions(fp: str) -> list[tuple[str, int] | tuple[str]]:
    """Load the instructions from the file"""

    content: list[tuple[str, int] | tuple[str]] = []

    with open(fp, "r") as f:
        for line in f.readlines():
            line = line.strip().split(" ")
            if len(line) > 1:
                line = (line[0], int(line[1]))
            else:
                line = (line[0],)

            content.append(line)

    return content


def run_instructions(
    instructions: list[tuple], x: int, screen: str = ""
) -> int | tuple[int, str]:
    def draw_screen(screen, position, x) -> str:
        if not screen:
            return ""

        while position >= 40:
            position -= 40

        if position in (x - 1, x, x + 1):
            return screen + "#"
        return screen + "."

    total = 0
    addx_amount = 0

    cycle = 0
    idx = 0

    while idx <= len(instructions) - 1:
        instruction = instructions[idx]
        cycle += 1

        screen = draw_screen(screen, cycle - 1, x)

        if (cycle + 20) % 40 == 0:
            total += cycle * x

        if len(instruction) == 1:
            idx += 1
            # screen = draw_screen(screen, cycle, x)
            continue

        if addx_amount != 0:
            x += addx_amount
            addx_amount = 0
            idx += 1
            continue

        # screen = draw_screen(screen, cycle, x)
        addx_amount = instruction[1]

    if screen:
        return total, screen[1:]

    return total


def main(fp: str = "10/sample.txt"):
    instructions = load_instructions(fp)
    x = 1

    # Part 1
    total = run_instructions(instructions, x)
    print(total)

    # Part 2
    total, screen = run_instructions(instructions, x, " ")  # type: ignore
    for idx, char in enumerate(screen):
        if idx % 40 == 0 and idx != 0:
            print()
        print(char, end="")
    print()


if __name__ == "__main__":
    # main()
    main("10/input.txt")  # 13440, PBZGRAZA

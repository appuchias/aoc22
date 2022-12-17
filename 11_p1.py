#! /usr/bin/env python3

# Advent of Code 22 - Day 11

from math import sqrt


def load_monkeys(fp: str) -> ...:
    with open(fp, "r") as f:
        content = f.read()

    monkeys = dict()

    monkeys_lines = [monkey.split("\n") for monkey in content.split("\n\n")]

    for monkey in monkeys_lines:
        n = int(monkey[0][-2])
        monkeys[n] = {
            "Items": [int(i) for i in monkey[1].split(":")[-1].strip().split(",")],
            "Operation": parse_operation(
                "".join(monkey[2].split("=")[-1].split(" ")[2:])  # Get `+4`
            ),
            "Divisible": int(monkey[3].split(" ")[-1]),
            "True": int(monkey[4][-1]),
            "False": int(monkey[5][-1]),
        }

    return monkeys


def parse_operation(operation: str) -> object:
    if operation[0] == "+":
        if operation[1:].isdigit():
            return lambda x: x + int(operation[1:])
        return lambda x: x + x
    elif operation[0] == "*":
        if operation[1:].isdigit():
            return lambda x: x * int(operation[1:])
        return lambda x: x * x
    return None


def run_rounds(
    monkeys: dict, rounds: int = 20, reducer=(lambda x: x // 3)
) -> tuple[dict, list[int]]:

    inspections = [0 for _ in monkeys]

    for _ in range(rounds):
        for monkey_num in monkeys.keys():
            monkey = monkeys[monkey_num]
            for _ in range(len(monkey["Items"])):
                item = monkey["Items"].pop(0)
                inspections[monkey_num] += 1
                worry_after_inspection = reducer(monkey["Operation"](item))

                if worry_after_inspection % monkey["Divisible"] == 0:
                    monkeys[monkey["True"]]["Items"].append(worry_after_inspection)
                else:
                    monkeys[monkey["False"]]["Items"].append(worry_after_inspection)

    return monkeys, inspections


def main(fp: str = "samples/11.txt"):
    # Part 1
    monkeys = load_monkeys(fp)
    monkeys, inspections = run_rounds(monkeys)
    # print([monkeys[monkey]["Items"] for monkey in monkeys])
    # print(inspections)
    top_2 = [inspections.pop(inspections.index(max(inspections))) for _ in range(2)]
    print(top_2[0] * top_2[1])  # 58794

    # Part 2


if __name__ == "__main__":
    # main()
    main("inputs/11.txt")

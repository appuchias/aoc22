#! /usr/bin/env python3

# Advent of Code 22 - Day 11

from dataclasses import dataclass, field
from typing import List, Callable
from functools import reduce


@dataclass(order=True)
class Monkey:
    monkey_id: int
    items: List[int] = field(default_factory=list, compare=False)
    operation: Callable = field(default=lambda x: x, compare=False)
    divide_by: int = field(default=1, compare=False)
    if_true: int = field(default=-1, compare=False)
    if_false: int = field(default=-1, compare=False)

    inspections: int = field(default=0, compare=True)


def load_monkeys(fp: str) -> List[Monkey]:
    with open(fp, "r") as f:
        content = f.read()

    monkeys = list()

    monkeys_lines = [monkey.split("\n") for monkey in content.split("\n\n")]

    for monkey in monkeys_lines:
        monkeys.append(
            Monkey(
                monkey_id=int(monkey[0][-2]),
                items=[int(i) for i in monkey[1].split(":")[-1].strip().split(",")],
                operation=parse_operation(
                    "".join(monkey[2].split("=")[-1].split(" ")[2:])  # Get `+4`
                ),
                divide_by=int(monkey[3].split(" ")[-1]),
                if_true=int(monkey[4][-1]),
                if_false=int(monkey[5][-1]),
            )
        )

    return monkeys


def parse_operation(operation: str) -> Callable:
    if operation[0] == "+":
        if operation[1:].isdigit():
            return lambda x: x + int(operation[1:])
        return lambda x: x + x
    elif operation[0] == "*":
        if operation[1:].isdigit():
            return lambda x: x * int(operation[1:])
        return lambda x: x * x

    return lambda x: x


def run_rounds(
    monkeys: list[Monkey], rounds: int = 20, reducer: Callable = lambda x: x // 3
) -> list[Monkey]:

    for _ in range(rounds):
        for monkey in monkeys:
            for _ in range(len(monkey.items)):
                item = monkey.items.pop(0)
                monkey.inspections += 1
                worry_after_inspection = reducer(monkey.operation(item))

                if worry_after_inspection % monkey.divide_by == 0:
                    monkeys[monkey.if_true].items.append(worry_after_inspection)
                else:
                    monkeys[monkey.if_false].items.append(worry_after_inspection)

    return monkeys


def top_n(monkeys: List[int], n: int) -> List[int]:
    in_list = monkeys[:]

    return [in_list.pop(in_list.index(max(in_list))) for _ in range(n)]


def main(fp: str = "samples/11.txt"):
    # Part 1
    monkeys = load_monkeys(fp)
    monkeys = run_rounds(monkeys)
    inspections = [monkey.inspections for monkey in monkeys]

    top_2 = top_n(inspections, 2)
    print(top_2[0] * top_2[1])  # 58794

    # Part 2
    monkeys = load_monkeys(fp)
    mod = reduce(lambda x, y: x * y, [monkey.divide_by for monkey in monkeys])
    monkeys = run_rounds(monkeys, 10_000, lambda x: x % mod)
    inspections = [monkey.inspections for monkey in monkeys]

    top_2 = top_n(inspections, 2)
    print(top_2[0] * top_2[1])  # 20151213744


if __name__ == "__main__":
    # main()
    main("inputs/11.txt")

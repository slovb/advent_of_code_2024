import itertools
import random
from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class Data:
    wires: dict[str, int]
    gates: list[tuple[str, str, str, str]]
    outputs: list[str]


def process(op: str, left: int, right: int) -> int:
    if op == "AND":
        return left & right
    elif op == "OR":
        return left | right
    elif op == "XOR":
        return left ^ right
    raise Exception("IMPOSSIBLE")


def memory_to_int(prefix: str, memory: dict[str, int]) -> int:
    out = 0
    for name, value in memory.items():
        if name.startswith(prefix):
            multiplier = 2 ** int(name[1:])
            out += value * multiplier
    return out


def int_to_memory(value: int, n: int, prefix: str, memory: dict[str, int]) -> None:
    for i in range(n):
        mid = "0" if i < 10 else ""
        addr = f"{prefix}{mid}{i}"
        memory[addr] = value % 2
        value = value // 2


def calculate(
    memory: dict[str, int],
    unprocessed: list[tuple[str, str, str, str]],
    swaps: list[tuple[str, str]],
):
    changes = {}
    for a, b in swaps:
        changes[a] = b
        changes[b] = a

    while len(unprocessed) > 0:
        progress = False
        i = 0
        while i < len(unprocessed):
            left, op, right, result = unprocessed[i]
            # if left in changes:
            #     left = changes[left]
            # if right in changes:
            #     right = changes[right]
            if result in changes:
                result = changes[result]
            if left in memory and right in memory:
                unprocessed.pop(i)
                memory[result] = process(op, memory[left], memory[right])
                progress = True
            else:
                i += 1
        if not progress:
            return -1
    return memory_to_int("z", memory)


def bitcount(bin: int):
    out = 0
    while bin > 0:
        out += bin % 2
        bin = bin // 2
    return out


def solve(data: Data, size: int) -> str:
    n = 0  # number of bits
    for name in data.wires:
        if name.startswith("x"):
            n = max(n, int(name[1:]) + 1)

    options: list[tuple[str, str]] = []

    swaps: Iterator[tuple[str, str]] = itertools.combinations(data.outputs, 2)

    while True:
        x = random.randint(0, 2**n - 1)
        y = random.randint(0, 2**n - 1)
        z = x + y
        memory: dict[str, int] = {}
        int_to_memory(x, n, "x", memory)
        int_to_memory(y, n, "y", memory)
        unprocessed = list(data.gates)
        no_change = calculate(memory, unprocessed, [])
        # diff_no_change = abs(z - no_change)
        diff_no_change = bitcount(z ^ no_change)
        if diff_no_change == 0:
            print("skip")
            continue

        reduced: list[tuple[str, str]] = []
        for swap in swaps:
            memory: dict[str, int] = {}
            int_to_memory(x, n, "x", memory)
            int_to_memory(y, n, "y", memory)
            unprocessed = list(data.gates)
            value = calculate(memory, unprocessed, [swap])
            # diff = abs(z - value)
            diff = bitcount(z ^ value)
            if diff <= diff_no_change:
                reduced.append(swap)

        options = reduced
        swaps = iter(options)
        if len(options) <= size:
            memory: dict[str, int] = {}
            int_to_memory(x, n, "x", memory)
            int_to_memory(y, n, "y", memory)
            unprocessed = list(data.gates)
            value = calculate(memory, unprocessed, options)
            print(z, value)
            break

    result = []
    for a, b in options:
        result += [a, b]
    return ",".join(sorted(result))


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        wires = {}
        gates = []
        outputs = []
        first_part = True
        for row in rows:
            if row == "":
                first_part = False
                continue
            if first_part:
                name = row.split(":")[0]
                value = int(row[-1])
                wires[name] = value
            else:
                left, op, right, _, result = row.split(" ")
                gates.append((left, op, right, result))
                outputs.append(result)
        outputs = sorted(outputs)
        data = Data(wires=wires, gates=gates, outputs=outputs)
        return data


def main(filename, size=4):
    return solve(read(filename), size)


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_2.txt", "z00,z01,z02,z05", 2),
    ]

    if len(sys.argv) < 2:
        has_failed = False
        for filename, value, size in testcases:
            res = main(filename, size)
            print("{}   {}\n".format(filename, str(res)))
            if res != value:
                print("Failed test")
                has_failed = True
        if not has_failed:
            filename = "input.txt"
            print("{}   {}\n".format(filename, main(filename)))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))

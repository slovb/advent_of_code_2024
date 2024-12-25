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
    expected: list[int] | None = None,
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
            if left in memory and right in memory:
                if result in changes:
                    result = changes[result]
                unprocessed.pop(i)
                value = process(op, memory[left], memory[right])
                if expected is not None and result.startswith("z"):  # stop early
                    znum = int(result[1:])
                    if value != expected[znum]:
                        return -1
                memory[result] = value
                progress = True
            else:
                i += 1
        if not progress:
            return -1
    return memory_to_int("z", memory)


def setup_memory(x: int, y: int, n: int) -> dict[str, int]:
    memory: dict[str, int] = {}
    int_to_memory(x, n, "x", memory)
    int_to_memory(y, n, "y", memory)
    return memory


def bitcount(bin: int):
    out = 0
    while bin > 0:
        out += bin % 2
        bin = bin // 2
    return out


def as_bin_array(z: int, n) -> list[int]:
    i = 0
    out = [0] * n
    while z > 0:
        out[i] = z % 2
        z = z // 2
        i += 1
    return out


def get_dependencies(point: str, gates: list[tuple[str, str, str, str]]) -> list[str]:
    for gate in gates:
        if gate[-1] == point:
            left = gate[0]
            right = gate[2]
            dependencies = []
            if not left.startswith("x") and not left.startswith("y"):
                dependencies += [left] + get_dependencies(left, gates)
            if not right.startswith("x") and not right.startswith("y"):
                dependencies += [right] + get_dependencies(right, gates)
            return dependencies
    raise Exception("problem")


def swap_candidates(data: Data, size: int, n: int) -> set[str]:
    endpoints: set[str] = set()
    for _ in range(1000):
        x = random.randint(0, 2**n - 1)
        y = random.randint(0, 2**n - 1)
        z = x + y
        if size == 2:
            z = x & y
        value = calculate(setup_memory(x, y, n), list(data.gates), [])
        xor = z ^ value
        i = 0
        while xor > 0:
            if xor % 2 == 1:
                endpoints.add(f'z{"0" if i < 10 else ''}{i}')
            xor = xor // 2
            i += 1
    # go up the tree
    candidates: set[str] = set(endpoints)
    for end in endpoints:
        for dependency in get_dependencies(end, data.gates):
            candidates.add(dependency)
    return candidates


def get_faulty_dependencies(
    point: str,
    gates: list[tuple[str, str, str, str]],
    memory: dict[str, int],
    expected: int,
) -> list[str]:
    dependencies: list[str] = []
    if memory[point] == expected:
        return dependencies
    if point.startswith("x") or point.startswith("y"):
        return dependencies
    # dependencies.append(point)

    # find the gate
    for gate in gates:
        if gate[-1] == point:
            break
    if gate[-1] != point:
        raise Exception("problem")

    left = gate[0]
    op = gate[1]
    right = gate[2]

    if op == "AND":
        dependencies += get_faulty_dependencies(left, gates, memory, expected)
        dependencies += get_faulty_dependencies(right, gates, memory, expected)
    elif op == "OR":
        dependencies += get_faulty_dependencies(left, gates, memory, expected)
        dependencies += get_faulty_dependencies(right, gates, memory, expected)
    elif op == "XOR":
        lval = memory[left]
        rval = memory[right]
        if expected == 0:
            dependencies += get_faulty_dependencies(left, gates, memory, rval)
            dependencies += get_faulty_dependencies(right, gates, memory, lval)
        else:
            dependencies += get_faulty_dependencies(left, gates, memory, (rval + 1) % 2)
            dependencies += get_faulty_dependencies(
                right, gates, memory, (lval + 1) % 2
            )
    else:
        raise Exception("PROBLEM")
    if len(dependencies) == 0:
        dependencies.append(point)
    return dependencies


def better_swap_candidates(data: Data, size: int, n: int):
    candidates: set[str] = set()
    for _ in range(1000):
        x = random.randint(0, 2**n - 1)
        y = random.randint(0, 2**n - 1)
        z = x + y
        if size == 2:
            z = x & y

        memory = setup_memory(x, y, n)
        value = calculate(memory, list(data.gates), [])
        if value == z:
            continue
        expected = as_bin_array(z, n + 1)
        for name, v in memory.items():
            if name.startswith("z"):
                i = int(name[1:])
                if v != expected[i]:
                    for candidate in get_faulty_dependencies(
                        name, data.gates, memory, expected[i]
                    ):
                        candidates.add(candidate)
    return candidates


def initial_swaps(outputs, size):
    groups = itertools.combinations(outputs, 2 * size)
    for group in groups:
        remember = set()
        for swap_from in itertools.combinations(group, size):
            remainder = [output for output in group if output not in swap_from]
            for swap_to in itertools.permutations(remainder):
                zippy = []
                for i, a in enumerate(swap_from):
                    b = swap_to[i]
                    zippy.append((min(a, b), max(a, b)))
                zippy = sorted(zippy)
                key = tuple(zippy)
                if key in remember:
                    continue
                remember.add(key)
                yield zippy


def solve(data: Data, size: int) -> str:
    n = 0  # number of bits
    for name in data.wires:
        if name.startswith("x"):
            n = max(n, int(name[1:]) + 1)

    print(len(data.outputs))
    outputs = swap_candidates(data, size, n)
    print(len(outputs))
    outputs = better_swap_candidates(data, size, n)
    print(len(outputs))
    swaps_iterator = initial_swaps(outputs, size)

    while True:
        x = random.randint(0, 2**n - 1)
        y = random.randint(0, 2**n - 1)
        z = x + y
        if size == 2:
            z = x & y

        no_change = calculate(setup_memory(x, y, n), list(data.gates), [])
        diff_no_change = bitcount(z ^ no_change)
        if diff_no_change < size:
            continue

        expected = as_bin_array(z, n + 1)
        reduced: list[list[tuple[str, str]]] = []
        for swaps in swaps_iterator:
            value = calculate(
                setup_memory(x, y, n), list(data.gates), swaps, expected=expected
            )
            if z == value:
                reduced.append(swaps)

        options = list(reduced)
        if len(options) == 0:
            raise Exception("BAD")
        elif len(options) == 1:
            value = calculate(setup_memory(x, y, n), list(data.gates), options[0])
            break
        swaps_iterator = iter(options)

    result = []
    for a, b in options[0]:
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

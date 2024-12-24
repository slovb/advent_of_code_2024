from dataclasses import dataclass


@dataclass(frozen=True)
class Data:
    wires: dict[str, int]
    gates: list[tuple[str, str, str, str]]


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


def solve(data: Data) -> int:
    memory = dict(data.wires)
    unprocessed = list(data.gates)

    while len(unprocessed) > 0:
        i = 0
        while i < len(unprocessed):
            left, op, right, result = unprocessed[i]
            if left in memory and right in memory:
                unprocessed.pop(i)
                memory[result] = process(op, memory[left], memory[right])
            else:
                i += 1
    return memory_to_int("z", memory)


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        wires = {}
        gates = []
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
        data = Data(wires=wires, gates=gates)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 4),
        ("test_1.txt", 2024),
    ]

    if len(sys.argv) < 2:
        has_failed = False
        for filename, value in testcases:
            res = main(filename)
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

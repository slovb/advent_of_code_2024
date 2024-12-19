from dataclasses import dataclass


@dataclass(frozen=True)
class Data:
    towels: set[str]
    designs: list[str]


def viable_designs(design: str, towels: set[str], memory: dict[str, int]) -> int:
    if design in memory:
        return memory[design]
    count = 0
    if design in towels:
        count += 1
    for i in range(1, len(design)):
        start = design[:i]
        end = design[i:]
        if start in towels:
            count += viable_designs(end, towels, memory)
    memory[design] = count
    # print(design, count)
    return count


def solve(data: Data) -> int:
    out = 0
    memory: dict[str, int] = {}
    for design in data.designs:
        count = viable_designs(design, data.towels, memory)
        print(design, count)
        # print(" ")
        out += count
    return out


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        towels = set(rows[0].split(", "))
        designs = rows[2:]
        data = Data(towels=towels, designs=designs)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 16),
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

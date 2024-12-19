from dataclasses import dataclass


@dataclass(frozen=True)
class Data:
    towels: set[str]
    designs: list[str]


def viable_design(design: str, towels: set[str], burnt: set[str]) -> bool:
    if design in towels:
        return True
    elif design in burnt:
        return False
    for i in range(1, len(design)):
        start = design[:i]
        end = design[i:]
        if start in towels:
            if viable_design(end, towels, burnt):
                return True
            else:
                burnt.add(end)
    return False


def solve(data: Data) -> int:
    out = 0
    burnt: set[str] = set()
    for design in data.designs:
        print(design)
        if viable_design(design, data.towels, burnt):
            out += 1
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
        ("test_0.txt", 6),
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

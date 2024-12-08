import itertools
from dataclasses import dataclass


@dataclass(frozen=True)
class Data:
    width: int
    height: int
    antennas: dict[str, list[tuple[int, int]]]


def diff(p, q):
    return (q[0] - p[0], q[1] - p[1])


def in_bounds(p, width, height):
    x, y = p
    return 0 <= x < width and 0 <= y < height


def list_anodes(a, b, width, height):
    out = []
    dab = diff(a, b)

    pos = (a[0] - dab[0], a[1] - dab[1])
    if in_bounds(pos, width, height):
        out.append(pos)

    pos = (b[0] + dab[0], b[1] + dab[1])
    if in_bounds(pos, width, height):
        out.append(pos)
    return out


def display(data: Data, anodes: set):
    to_draw = {}
    for p in anodes:
        to_draw[p] = "#"
    for c, antennas in data.antennas.items():
        for antenna in antennas:
            to_draw[antenna] = c
    lines = []
    for y in range(data.height):
        line = []
        for x in range(data.width):
            p = (x, y)
            line.append(to_draw.get(p, "."))
        lines.append("".join(line))
    print("\n".join(lines))


def solve(data: Data):
    anodes = set()
    for antennas in data.antennas.values():
        for a, b in itertools.combinations(antennas, 2):
            for anode in list_anodes(a, b, data.width, data.height):
                anodes.add(anode)
    display(data, anodes)
    return len(anodes)


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        antennas = {}
        for y, row in enumerate(rows):
            for x, c in enumerate(row):
                if c == ".":
                    continue
                if c not in antennas:
                    antennas[c] = []
                antennas[c].append((x, y))
        data = Data(width=x + 1, height=y + 1, antennas=antennas)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test0.txt", 14),
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

from dataclasses import dataclass
from typing import Set


@dataclass(frozen=True)
class Data:
    start: tuple[int, int]
    width: int
    height: int
    blocks: Set[tuple[int, int]]


def step(pos: tuple[int, int], dir: int) -> tuple[int, int]:
    if dir == 0:
        return (pos[0], pos[1] - 1)
    elif dir == 1:
        return (pos[0] + 1, pos[1])
    elif dir == 2:
        return (pos[0], pos[1] + 1)
    elif dir == 3:
        return (pos[0] - 1, pos[1])
    raise Exception("Bad direction")


def solve(data: Data):
    direction = 0  # UP RIGHT DOWN LEFT
    position = data.start
    positions: Set[tuple[int, int]] = set([position])
    while 0 <= position[0] < data.width and 0 <= position[1] < data.height:
        candidate = step(position, direction)
        while candidate in data.blocks:
            direction = (direction + 1) % 4
            candidate = step(position, direction)
        position = candidate
        positions.add(position)
    return len(positions) - 1


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        start = None
        blocks = set()
        for y, row in enumerate(rows):
            for x, c in enumerate(row):
                if c == ".":
                    pass
                elif c == "^":
                    start = (x, y)
                    pass
                elif c == "#":
                    blocks.add((x, y))
                else:
                    raise Exception(c)
        data = Data(start=start, width=x + 1, height=y + 1, blocks=blocks)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test0.txt", 41),
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

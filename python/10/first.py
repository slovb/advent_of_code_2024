from dataclasses import dataclass


@dataclass(frozen=True)
class Data:
    starts: list[tuple[int, int]]
    heights: dict[tuple[int, int], int]


def add(pos: tuple[int, int], step: tuple[int, int]):
    return (pos[0] + step[0], pos[1] + step[1])


def count_trails_from(pos: tuple[int, int], data: Data, height: int = 0) -> int:
    if height == 9:
        return 1
    out = 0
    for step in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        candidate = add(pos, step)
        if data.heights.get(candidate, -1) == height + 1:
            out += count_trails_from(candidate, data, height + 1)
    return out


def trailends_from(
    pos: tuple[int, int], data: Data, height: int = 0
) -> set[tuple[int, int]]:
    if height == 9:
        return set([pos])
    out: set[tuple[int, int]] = set()
    for step in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        candidate = add(pos, step)
        if data.heights.get(candidate, -1) == height + 1:
            out = out.union(trailends_from(candidate, data, height + 1))
    return out


def solve(data: Data) -> int:
    out = 0
    for start in data.starts:
        out += len(trailends_from(start, data))

    return out


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        starts = []
        heights = {}
        for y, row in enumerate(rows):
            for x, char in enumerate(row):
                height = int(char)
                pos = (x, y)
                heights[pos] = height
                if height == 0:
                    starts.append(pos)
        return Data(starts=starts, heights=heights)


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test0.txt", 1),
        ("test1.txt", 36),
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

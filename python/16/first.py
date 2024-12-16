import heapq
from dataclasses import dataclass


@dataclass(frozen=True)
class Data:
    walls: set[tuple[int, int]]
    start: tuple[int, int]
    end: tuple[int, int]


def step(pos, dir):
    x, y = pos
    if dir == 0:
        return (x + 1, y)
    elif dir == 1:
        return (x, y + 1)
    elif dir == 2:
        return (x - 1, y)
    elif dir == 3:
        return (x, y - 1)
    raise Exception("unexpected input")


def solve(data: Data) -> int:
    visited: dict[tuple[int, int, int], int] = {}
    options = [(0, *data.start, 0)]  # score, x, y, direction
    while True:
        score, x, y, dir = heapq.heappop(options)
        if (x, y) in data.walls:
            continue
        if (x, y) == data.end:
            return score
        if (x, y, dir) in visited:
            old_score = visited[(x, y, dir)]
            if score < old_score:
                raise Exception("This should not happen with heaps")
            continue
        visited[(x, y, dir)] = score
        heapq.heappush(options, (score + 1, *step((x, y), dir), dir))
        heapq.heappush(
            options, (score + 1001, *step((x, y), (dir + 1) % 4), (dir + 1) % 4)
        )
        heapq.heappush(
            options, (score + 1001, *step((x, y), (dir - 1) % 4), (dir - 1) % 4)
        )


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        walls: set[tuple[int, int]] = set()
        for y, row in enumerate(rows):
            for x, c in enumerate(row):
                pos = (x, y)
                if c == "#":
                    walls.add(pos)
                elif c == "S":
                    start = pos
                elif c == "E":
                    end = pos
        data = Data(walls=walls, start=start, end=end)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 7036),
        ("test_1.txt", 11048),
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

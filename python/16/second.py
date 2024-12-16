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


def display(walls, start, end, visited):
    width = 0
    height = 0
    for wall in walls:
        width = max(wall[0] + 1, width)
        height = max(wall[1] + 1, height)
    rows = []
    for y in range(height):
        row = []
        for x in range(width):
            pos = (x, y)
            if pos in visited:
                row.append("O")
            elif pos == start:
                row.append("S")
            elif pos == end:
                row.append("E")
            elif pos in walls:
                row.append("#")
            else:
                row.append(" ")
        rows.append("".join(row))
    return "\n".join(rows)


def solve(data: Data) -> int:
    visited: dict[tuple[int, int, int], int] = {}
    options: list[tuple[int, int, int, int, set[tuple[int, int]]]] = [
        (0, *data.start, 0, set())
    ]  # score, x, y, direction, past
    seating: set[tuple[int, int]] = set()
    solution = None
    while len(options) > 0:
        score, x, y, dir, past = heapq.heappop(options)
        if (x, y) in data.walls:
            continue
        if (x, y) == data.end:
            if solution is None:
                solution = score
            if solution == score:
                seating = seating.union(past)
            elif score < solution:
                raise Exception("Unexpected")
            continue
        if (x, y, dir) in visited:
            old_score = visited[(x, y, dir)]
            if score < old_score:
                raise Exception("This should not happen with heaps")
            elif score > old_score:
                continue
        else:
            visited[(x, y, dir)] = score
        heapq.heappush(
            options, (score + 1, *step((x, y), dir), dir, past.union(set([(x, y)])))
        )
        heapq.heappush(
            options,
            (
                score + 1000,
                # *step((x, y), (dir + 1) % 4),
                x,
                y,
                (dir + 1) % 4,
                past.union(set([(x, y)])),
            ),
        )
        heapq.heappush(
            options,
            (
                score + 1000,
                # *step((x, y), (dir - 1) % 4),
                x,
                y,
                (dir - 1) % 4,
                past.union(set([(x, y)])),
            ),
        )
    seating = seating.union(set([data.end]))
    print(display(data.walls, data.start, data.end, seating))
    return len(seating)


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
        ("test_0.txt", 45),
        ("test_1.txt", 64),
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

from dataclasses import dataclass
from heapq import heappop, heappush


@dataclass(frozen=True)
class Data:
    walls: set[tuple[int, int]]
    start: tuple[int, int]
    end: tuple[int, int]


def step(pos: tuple[int, int], move: tuple[int, int]) -> tuple[int, int]:
    return (pos[0] + move[0], pos[1] + move[1])


dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def find_distances(
    starting: tuple[int, int], walls: set[tuple[int, int]]
) -> dict[tuple[int, int], int]:
    distances: dict[tuple[int, int], int] = {}
    exploring = [(0, starting)]
    while len(exploring) > 0:
        steps, pos = heappop(exploring)
        if pos in distances and distances[pos] <= steps:
            continue
        distances[pos] = steps
        for direction in dirs:
            candidate = step(pos, direction)
            if candidate in walls:
                continue
            heappush(exploring, (steps + 1, candidate))
    return distances


def solve(data: Data, limit: int) -> int:
    cheats: set[tuple[int, int, int, int]] = set()
    distance_from_start = find_distances(data.start, data.walls)
    distance_from_end = find_distances(data.end, data.walls)

    no_cheat = distance_from_start[data.end]
    cutoff = no_cheat - limit
    max_length = 20
    for pos, dfs in distance_from_start.items():
        length = min(max_length, max(0, cutoff - dfs))
        for y in range(-length, length + 1):
            width = length - abs(y)
            for x in range(-width, width + 1):
                candidate = (pos[0] + x, pos[1] + y)
                if candidate not in distance_from_end:
                    continue
                dfe = distance_from_end[candidate]
                distance = dfs + dfe + abs(x) + abs(y)
                if distance <= cutoff:
                    cheat = (*pos, *candidate)
                    cheats.add(cheat)
    return len(cheats)


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


def main(filename, limit=100):
    return solve(read(filename), limit)


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 29, 72),
        ("test_0.txt", 0, 77),
        ("test_0.txt", 3, 76),
        ("test_0.txt", 3, 75),
        ("test_0.txt", 7, 74),
        ("test_0.txt", 7, 73),
        ("test_0.txt", 29, 71),
        ("test_0.txt", 41, 70),
        ("test_0.txt", 285, 50),
    ]

    if len(sys.argv) < 2:
        has_failed = False
        for filename, value, limit in testcases:
            res = main(filename, limit)
            print("{}   {}   {}".format(filename, str(res), str(limit)))
            if res != value:
                print("Failed test")
                has_failed = True
                break
            print(" ")
        if not has_failed:
            filename = "input.txt"
            print("{}   {}\n".format(filename, main(filename)))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))

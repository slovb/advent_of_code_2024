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


def display(walls, wall_hacks, start, end, notable=None):
    width = 0
    height = 0
    for x, y in walls:
        width = max(width, x + 1)
        height = max(height, y + 1)

    for y in range(height):
        row = []
        for x in range(width):
            pos = (x, y)
            if notable is not None and pos == notable:
                row.append("*")
            elif pos in wall_hacks:
                row.append("!")
            elif pos == start:
                row.append("S")
            elif pos == end:
                row.append("E")
            elif pos in walls:
                row.append("#")
            else:
                row.append(" ")
        print("".join(row))


def solve(data: Data, limit: int) -> int:
    cheats: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    wall_hacks: set[tuple[int, int]] = set()
    distance_from_start = find_distances(data.start, data.walls)
    distance_from_end = find_distances(data.end, data.walls)
    no_cheat = distance_from_start[data.end]
    cutoff = no_cheat - limit
    for pos, dfs in distance_from_start.items():
        if dfs + 2 > cutoff:
            # no chance
            continue
        for one_direction in dirs:
            one_step = step(pos, one_direction)
            if one_step not in data.walls:
                # we are looking for the cheat!
                continue
            for two_direction in dirs:
                two_step = step(one_step, two_direction)
                if two_step == pos:
                    continue
                if two_step not in distance_from_end:
                    # we are looking for a small cheat
                    continue
                dfe = distance_from_end[two_step]
                distance = dfs + dfe + 2
                if distance <= cutoff:
                    wall_hacks.add(one_step)
                    cheats.add((pos, two_step))
                    print(f"Saving {no_cheat-distance} @ {pos}")
                    # display(data.walls, wall_hacks, data.start, data.end, pos)
                    # print(" ")
    display(data.walls, wall_hacks, data.start, data.end)
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
        ("test_0.txt", 4, 35),
        ("test_0.txt", 4, 36),
        ("test_0.txt", 3, 37),
        ("test_0.txt", 3, 38),
        ("test_0.txt", 0, 70),
        ("test_0.txt", 30, 4),
    ]

    if len(sys.argv) < 2:
        has_failed = False
        for filename, value, limit in testcases:
            res = main(filename, limit)
            print("{}   {}   {}\n".format(filename, str(res), str(limit)))
            if res != value:
                print("Failed test")
                has_failed = True
                break
        if not has_failed:
            filename = "input.txt"
            print("{}   {}\n".format(filename, main(filename)))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))

from dataclasses import dataclass


@dataclass(frozen=True)
class Data:
    plots: set[tuple[int, int, str]]


def step(u: tuple[int, int, str], v: tuple[int, int]):
    x, y, c = u
    vx, vy = v
    return (x + vx, y + vy, c)


def solve(data: Data) -> int:
    out = 0
    steps = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    processed: set[tuple[int, int, str]] = set()
    for plot in data.plots:
        if plot in processed:
            continue
        processed.add(plot)
        explore = [plot]
        area = 1
        perimiter = 0
        while len(explore) > 0:
            pl = explore.pop()
            for s in steps:
                candidate = step(pl, s)
                if candidate not in data.plots:
                    perimiter += 1
                elif candidate not in processed:
                    area += 1
                    explore.append(candidate)
                    processed.add(candidate)
        out += area * perimiter
    return out


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        plots = set()
        for y, row in enumerate(rows):
            for x, c in enumerate(row):
                plots.add((x, y, c))
        data = Data(plots=plots)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 140),
        ("test_1.txt", 772),
        ("test_2.txt", 1930),
    ]

    if len(sys.argv) < 2:
        has_failed = False
        for filename, value in testcases:
            res = main(filename)
            print("{}   {}\n".format(filename, str(res)))
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

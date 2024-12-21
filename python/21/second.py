import itertools
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Data:
    codes: list[str]


def numval(code: str):
    return int(code[:-1])


def numeric_coord(c: str) -> tuple[int, int]:
    if c == "A":
        return (0, 0)
    n = int(c)
    if n == 0:
        return (-1, 0)
    x = -2 + (n - 1) % 3
    y = -1 - ((n - 1) // 3)
    return (x, y)


def directional_coord(c: str) -> tuple[int, int]:
    if c == "A":
        return (0, 0)
    elif c == ">":
        return (0, 1)
    elif c == "v":
        return (-1, 1)
    elif c == "<":
        return (-2, 1)
    elif c == "^":
        return (-1, 0)
    raise Exception("Clueless")


def transform(
    code: str,
    coord: Callable[[str], tuple[int, int]],
    illegal: tuple[int, int],
) -> dict[str, int]:
    memory: dict[str, int] = {}
    old_x, old_y = coord("A")
    grouping = []
    for c in code:
        x, y = coord(c)
        dx, dy = x - old_x, y - old_y

        left_first = (x, old_y) != illegal
        right_first = (old_x, y) == illegal
        subsequence = []

        if dx < 0 and left_first:
            subsequence += ["<" * abs(dx)]
        if dx > 0 and right_first:
            subsequence += [">" * abs(dx)]

        if dy > 0:
            subsequence += ["v" * abs(dy)]
        if dy < 0:
            subsequence += ["^" * abs(dy)]

        if dx < 0 and not left_first:
            subsequence += ["<" * abs(dx)]
        if dx > 0 and not right_first:
            subsequence += [">" * abs(dx)]

        subsequence.append("A")

        old_x, old_y = x, y
        grouping += subsequence
        if (x, y) == (0, 0):
            # returning to home means we can jumble these for massive memoization
            section = "".join(grouping)
            memory[section] = memory.get(section, 0) + 1
            grouping = []
    if (x, y) != (0, 0):
        raise Exception("assumption")
    return memory


def length(code: str, loops: int) -> int:
    codes = transform(code, numeric_coord, illegal=(-2, 0))

    for _ in range(loops):
        # memoize subresutls to silly degrees
        update: dict[str, int] = {}
        for code, count in codes.items():
            partials = transform(code, directional_coord, illegal=(-2, 0))
            for update_code, partial_count in partials.items():
                update[update_code] = update.get(update_code, 0) + partial_count * count
        codes = update
    out = 0
    for code, count in codes.items():
        out += count * len(code)
    return out


def solve(data: Data, loops: int) -> int:
    out = 0
    for code in data.codes:
        nv = numval(code)
        l = length(code, loops)
        print(code, nv, l)
        out += nv * l
    return out


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        codes = []
        for row in rows:
            codes.append(row)
        data = Data(codes=codes)
        return data


def main(filename, loops=25):
    return solve(read(filename), loops)


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 126384, 2),
    ]

    if len(sys.argv) < 2:
        has_failed = False
        for filename, value, loops in testcases:
            res = main(filename, loops)
            print("{}   {}\n".format(filename, str(res)))
            if res != value:
                print("Failed test")
                has_failed = True
        if not has_failed or True:
            filename = "input.txt"
            print("{}   {}\n".format(filename, main(filename)))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))

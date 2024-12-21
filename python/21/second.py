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
    code: str, coord: Callable[[str], tuple[int, int]], illegal: tuple[int, int]
) -> str:
    sections = []
    old_x, old_y = coord("A")
    for c in code:
        x, y = coord(c)
        dx, dy = x - old_x, y - old_y

        subsequence = []

        # add these in the preferred order so then the first solution is best solution
        if dx < 0:
            subsequence += ["<" * abs(dx)]
        if dy > 0:
            subsequence += ["v" * abs(dy)]
        if dy < 0:
            subsequence += ["^" * abs(dy)]
        if dx > 0:
            subsequence += [">" * abs(dx)]

        if len(subsequence) == 0:
            sections.append("A")
        else:
            for perm in itertools.permutations(subsequence):
                test_x, test_y = old_x, old_y
                is_bad = False
                for c in perm:
                    if c[0] == "<":
                        test_x -= len(c)
                    elif c[0] == "^":
                        test_y -= len(c)
                    elif c[0] == ">":
                        test_x += len(c)
                    elif c[0] == "v":
                        test_y += len(c)
                    if (test_x, test_y) == illegal:
                        is_bad = True
                        break
                if not is_bad:
                    sections.append("".join([*perm, "A"]))
                    break
        old_x, old_y = x, y
    return "".join(sections)


def length(code: str) -> int:
    code = transform(code, numeric_coord, illegal=(-2, 0))

    for _ in range(25):
        code = transform(code, directional_coord, illegal=(-2, 0))
    return len(code)


def solve(data: Data) -> int:
    out = 0
    for code in data.codes:
        nv = numval(code)
        l = length(code)
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


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        # ("test_0.txt", 126384),
    ]

    if len(sys.argv) < 2:
        has_failed = False
        for filename, value in testcases:
            res = main(filename)
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

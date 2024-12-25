import itertools
from dataclasses import dataclass


@dataclass(frozen=True)
class Data:
    locks: list[tuple[int, ...]]
    keys: list[tuple[int, ...]]


def solve(data: Data) -> int:
    out = 0
    for lock, key in itertools.product(data.locks, data.keys):
        if not any([lock[i] + key[i] > 5 for i in range(5)]):
            print(lock, key)
            out += 1
    return out


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        locks: list[tuple[int, ...]] = []
        keys: list[tuple[int, ...]] = []
        new_group = True
        for row in rows:
            if new_group:
                if row[0] == "#":
                    group = [0] * 5
                    in_lock = True
                else:
                    group = [-1] * 5
                    in_lock = False
                new_group = False
                continue
            elif row == "":
                if in_lock:
                    locks.append(tuple(group))
                else:
                    keys.append(tuple(group))
                new_group = True
            else:
                for i, c in enumerate(row):
                    if c == "#":
                        group[i] += 1
        if in_lock:
            locks.append(tuple(group))
        else:
            keys.append(tuple(group))
        data = Data(locks=locks, keys=keys)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 3),
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

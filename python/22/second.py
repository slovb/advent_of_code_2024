from collections import deque
from dataclasses import dataclass
from typing import Deque


@dataclass(frozen=True)
class Data:
    secrets: list[int]


def mix(secret: int, value: int) -> int:
    return secret ^ value


def prune(secret: int, mod: int = 16777216) -> int:
    return secret % mod


def process(secret: int) -> int:
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, secret // 32))
    secret = prune(mix(secret, secret * 2048))
    return secret


def solve(data: Data, loops: int = 2000) -> int:
    long_mem: dict[tuple[int, int, int, int], int] = {}
    for secret in data.secrets:
        previous = None
        diffs: Deque[int] = deque()
        short_mem: set[tuple[int, int, int, int]] = set()
        for _ in range(loops):
            secret = process(secret)
            price = secret % 10
            if previous is not None:
                diff = price - previous
                diffs.append(diff)
                if len(diffs) > 4:
                    diffs.popleft()
            previous = price
            if len(diffs) == 4:
                key: tuple[int, int, int, int] = tuple(diffs)
                if key not in short_mem:
                    short_mem.add(key)
                    long_mem[key] = long_mem.get(key, 0) + price
    return max(long_mem.values())


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        secrets = []
        for row in rows:
            secrets.append(int(row))
        data = Data(secrets=secrets)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_1.txt", 23),
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

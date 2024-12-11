import math
from dataclasses import dataclass


def digits(n):
    if n == 0:
        return 1
    return 1 + int(math.log10(n))


@dataclass(frozen=True)
class Data:
    stones: dict[int, int]


def solve(data: Data) -> int:
    stones = data.stones
    for i in range(75):
        print(i)
        sts = {}
        for value, multiple in stones.items():
            n = digits(value)
            if value == 0:
                value = 1
            elif n % 2 == 0:
                tens = 10 ** (n // 2)
                split = value % tens
                sts[split] = multiple + sts.get(split, 0)
                value = value // tens
            else:
                value *= 2024
            sts[value] = multiple + sts.get(value, 0)
        stones = sts
    total = 0
    for multiple in stones.values():
        total += multiple
    return total


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = map(int, rows[0].split(" "))
        stones = {}
        for i in input:
            if i not in stones:
                stones[i] = 0
            stones[i] = 1 + stones.get(i, 0)
        return Data(stones=stones)


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        # ("test_0.txt", 55312),
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

import math
from dataclasses import dataclass


def digits(n):
    return 1 + int(math.log10(n))


class Stone:
    def __init__(self, value):
        self.value = value
        self.right = None

    def blink(self):
        if self.value == 0:
            self.value = 1
            return self.right, [self.value]
        n = digits(self.value)
        if n % 2 == 0:
            tens = 10 ** (n // 2)
            self.insert_right(self.value % tens)
            self.value = self.value // tens
            return self.right.right, [self.value, self.right.value]
        self.value *= 2024
        return self.right, [self.value]

    def insert_right(self, value):
        stone = Stone(value)
        stone.right = self.right
        self.right = stone


@dataclass(frozen=True)
class Data:
    root: Stone


def solve(data: Data) -> int:
    for _ in range(25):
        # row = []
        stone = data.root
        while stone is not None:
            stone, _ = stone.blink()
            # row += values
        # print(" ".join(map(str, row)))
    stone = data.root
    total = 0
    while stone is not None:
        total += 1
        stone = stone.right
    return total


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = map(int, rows[0].split(" "))
        it = iter(input)
        root = Stone(next(it))
        stone = root
        for v in it:
            stone.insert_right(v)
            stone = stone.right
        data = Data(root=root)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 55312),
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

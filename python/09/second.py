class File:
    def __init__(self, index, size):
        self.index = index
        self.size = size

    def score(self, pos):
        out = 0
        for i in range(self.size):
            out += self.index * (pos + i)
        return out

    def is_file(self) -> bool:
        return True

    def __str__(self):
        return f"File_{self.index}({self.size})"


class Gap:
    def __init__(self, size):
        self.size = size

    def score(self, _):
        return 0

    def is_file(self) -> bool:
        return False

    def __str__(self):
        return f"Gap({self.size})"


def shrink(input: list[File | Gap]) -> list[File | Gap]:
    i = len(input) - 1
    while i > 0:
        if input[i].is_file():
            block = input[i]
            for j in range(i):
                if not input[j].is_file() and input[j].size >= block.size:
                    # I can just leave a gap for scoring purposes, in other cases adjacent gaps should be merged, but that doesn't matter as we are only doing one pass
                    input[i] = Gap(size=block.size)
                    input[j].size -= block.size
                    input = input[:j] + [block] + input[j:]
                    break
        i -= 1
    return input


def score(input: list[File | Gap]) -> int:
    out = 0
    pos = 0
    for block in input:
        out += block.score(pos)
        pos += block.size
    return out


def solve(input: list[File | Gap]) -> int:
    input = shrink(input)
    return score(input)


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        index = 0
        for i, size in enumerate(map(int, rows[0].strip())):
            if i % 2 == 0:
                input.append(File(index=index, size=size))
                index += 1
            else:
                input.append(Gap(size=size))
        return input


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test0.txt", 2858),
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

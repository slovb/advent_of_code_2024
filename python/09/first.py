def solve(input):
    blocks = []
    gaps = []
    index = 0
    for i, x in enumerate(input):
        if i % 2 == 0:
            blocks = blocks + [index] * x
            index += 1
        else:
            gaps.append(x)

    out = 0
    pos = 0
    index = 0
    gapsize = 0
    while len(blocks) > 0:
        if gapsize == 0:
            if blocks[0] == index:
                out += blocks.pop(0) * pos
            else:
                gapsize = gaps.pop(0)
                index += 1
                continue
        else:
            out += blocks.pop() * pos
            gapsize -= 1
        pos += 1
    return out


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = [int(c) for c in rows[0].strip()]
        return input


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test0.txt", 1928),
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

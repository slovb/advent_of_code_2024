def solve(input):
    out = 0
    left, right = zip(*input)
    left = sorted(left)
    right = sorted(right)
    for i, l in enumerate(left):
        r = right[i]
        out += abs(l - r)
    return out


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        for row in rows:
            row = row.split(" ")
            row = map(str.strip, row)
            row = filter(lambda s: s != "", row)
            row = map(int, row)

            input.append(row)
            # input.append(int(row))
            # input.append(list(row))
        return input


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    name = "input.txt"
    # name = "test.txt"

    if len(sys.argv) < 2:
        print("{}\n".format(main(name)))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))

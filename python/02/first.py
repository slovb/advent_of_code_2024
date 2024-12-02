def is_safe(levels):
    last_diff = None
    for i, l in enumerate(levels[:-1]):
        diff = levels[i + 1] - l
        if abs(diff) > 3 or diff == 0:
            return False
        if last_diff is not None:
            if diff * last_diff < 0:
                return False
        last_diff = diff
    return True


def solve(input):
    out = 0
    for row in input:
        if is_safe(list(row)):
            out += 1
    return out


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        for row in rows:
            row = row.split(" ")
            row = map(str.strip, row)
            row = map(int, row)

            input.append(row)
            # input.append(int(row))
            # input.append(list(row))
        return input


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    filename = "input.txt"
    # filename = "test.txt"

    if len(sys.argv) < 2:
        print("{}\n".format(main(filename)))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))

def index_of_fault(levels):
    last_diff = None
    for i, l in enumerate(levels[:-1]):
        diff = levels[i + 1] - l
        if abs(diff) > 3 or diff == 0:
            return i
        if last_diff is not None:
            if diff * last_diff < 0:
                return i
        last_diff = diff
    return None


def is_safe(levels):
    i = index_of_fault(levels)

    # no removal ok?
    if i is None:
        # print(levels)
        return True

    # remove first ok?
    if i == 1:
        part = levels[i:]
        if index_of_fault(part) is None:
            print(i, i - 1, levels, part)
            return True

    # remove i ok?
    part = levels[:i] + levels[i + 1 :]
    if index_of_fault(part) is None:
        print(i, i, levels, part)
        return True

    # remove i + 1 ok?
    part = levels[: i + 1] + levels[i + 2 :]
    if index_of_fault(part) is None:
        print(i, i + 1, levels, part)
        return True
    return False


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

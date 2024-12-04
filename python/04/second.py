def solve(input):
    x_positions = set()
    m_positions = set()
    a_positions = set()
    s_positions = set()

    for y, row in enumerate(input):
        for x, c in enumerate(row):
            pos_c = (x, y)
            if c == "X":
                x_positions.add(pos_c)
            elif c == "M":
                m_positions.add(pos_c)
            elif c == "A":
                a_positions.add(pos_c)
            elif c == "S":
                s_positions.add(pos_c)
            else:
                raise Exception("Error")

    def test_offset(pos_a, offset):
        # offset for the first of two M clockwise
        px, py = pos_a
        ox, oy = offset
        if (px + ox, py + oy) not in m_positions:
            return False
        ox, oy = -oy, ox  # rot 90
        if (px + ox, py + oy) not in m_positions:
            return False
        ox, oy = -oy, ox  # rot 90
        if (px + ox, py + oy) not in s_positions:
            return False
        ox, oy = -oy, ox  # rot 90
        if (px + ox, py + oy) not in s_positions:
            return False
        return True

    out = 0
    offsets = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
    for pos_a in a_positions:
        for offset in offsets:
            if test_offset(pos_a, offset):
                out += 1

    return out


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        for row in rows:
            input.append(row)
        return input


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test0.txt", 9),
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

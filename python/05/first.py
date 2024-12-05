def is_good(update, poset):
    added = set()
    for n in update:
        tests = [m in added for m in poset.get(n, [])]
        if any(tests):
            return False
        added.add(n)
    return True


def solve(input):
    rules, updates = input
    poset = {}
    for a, b in rules:
        if a not in poset:
            poset[a] = []
        poset[a].append(b)

    out = 0
    for update in updates:
        if is_good(update, poset):
            out += update[len(update) // 2]
    return out


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        rules = []
        updates = []
        reading_rules = True
        for row in rows:
            if row == "":
                reading_rules = False
                continue

            if reading_rules:
                a, b = row.split("|")
                rules.append((int(a), int(b)))
            else:
                parts = list(map(int, row.split(",")))
                updates.append(parts)
        return (rules, updates)


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test0.txt", 143),
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

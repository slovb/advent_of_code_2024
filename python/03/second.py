import re


def solve(input):
    out = 0
    for a, b in input:
        out += a * b
    return out


def read(filename):
    with open(filename, "r") as f:
        data = f.read().rstrip()

        input = []
        data = re.findall(r"(?:do\(\)|^)(.*?)(?:don't\(\)|$)", data, flags=re.DOTALL)

        for part in data:
            for match in re.finditer(r"mul\((\d+),(\d+)\)", part):
                input.append((int(match.group(1)), int(match.group(2))))
        return input


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test.txt", 161),
        ("test2.txt", 48),
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

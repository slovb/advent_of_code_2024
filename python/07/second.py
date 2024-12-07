import itertools


def can_hit(target, nums):
    n = len(nums) - 1
    for ops in itertools.product([0, 1, 2], repeat=n):
        val = nums[0]
        for i, op in enumerate(ops):
            if op == 0:
                val += nums[i + 1]
            elif op == 1:
                val *= nums[i + 1]
            else:
                tmp = nums[i + 1]
                while tmp > 0:
                    val *= 10
                    tmp = tmp // 10
                val += nums[i + 1]
            if val > target:
                break
        if val == target:
            return True
    return False


def solve(input):
    out = 0
    for row in input:
        target, nums = row
        if can_hit(target, nums):
            out += target
    return out


def read(filename):
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        for row in rows:
            left, rest = row.split(": ")
            rest = rest.split(" ")
            rest = map(int, rest)
            input.append((int(left), list(rest)))
        return input


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test0.txt", 11387),
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

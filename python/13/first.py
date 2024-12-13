from dataclasses import dataclass

from z3 import Int, Solver


@dataclass(frozen=True)
class Machine:
    button_a: tuple[int, int]
    button_b: tuple[int, int]
    prize: tuple[int, int]

    def cost(self):
        a = Int("a")
        b = Int("b")

        s = Solver()
        s.add(a >= 0)
        s.add(a <= 100)
        s.add(b >= 0)
        s.add(b <= 100)

        s.add(self.prize[0] == a * self.button_a[0] + b * self.button_b[0])
        s.add(self.prize[1] == a * self.button_a[1] + b * self.button_b[1])
        res = s.check()
        if res.r != 1:
            return 0

        # optimize the result
        while res.r == 1:
            model = s.model()
            # print(model)
            best_a = model[a].as_long()
            best_b = model[b].as_long()
            best = 3 * best_a + best_b
            s.push()
            s.add(3 * a + b < best)
            res = s.check()
            s.pop()
        # print(best)
        return best


@dataclass(frozen=True)
class Data:
    input: list[Machine]


def solve(data: Data) -> int:
    out = 0
    for machine in data.input:
        # print(machine)
        out += machine.cost()
    return out


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        for row in rows:
            if row.startswith("Button A:"):
                _, l, r = row.split("+")
                l = l.split(",")[0]
                button_a = (int(l), int(r))
            elif row.startswith("Button B:"):
                _, l, r = row.split("+")
                l = l.split(",")[0]
                button_b = (int(l), int(r))
            elif row.startswith("Prize:"):
                _, l, r = row.split("=")
                l = l.split(",")[0]
                prize = (int(l), int(r))
            else:
                input.append(Machine(button_a=button_a, button_b=button_b, prize=prize))
        input.append(Machine(button_a=button_a, button_b=button_b, prize=prize))
        data = Data(input=input)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 480),
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

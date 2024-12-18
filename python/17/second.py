import math
from dataclasses import dataclass
from pprint import pprint
from tkinter import W


@dataclass(frozen=True)
class Data:
    a: int
    b: int
    c: int
    program: list[int]


def combo(operand: int, reg: list[int]) -> int:
    if operand < 4:
        return operand
    if operand < 7:
        return reg[operand - 4]
    raise Exception("not implemented")


def op(opcode: int, operand: int, reg: list[int], ip: int, out: list[int]) -> int:
    if opcode == 0:
        # adv
        num = reg[0]
        den = 2 ** combo(operand, reg)
        reg[0] = num // den
    elif opcode == 1:
        # bxl
        reg[1] = reg[1] ^ operand
    elif opcode == 2:
        # bst
        reg[1] = combo(operand, reg) % 8
    elif opcode == 3:
        # jnz
        if reg[0] != 0:
            return operand
    elif opcode == 4:
        # bxc
        reg[1] = reg[1] ^ reg[2]
    elif opcode == 5:
        # out
        out.append(combo(operand, reg) % 8)
    elif opcode == 6:
        # bdv
        num = reg[0]
        den = 2 ** combo(operand, reg)
        reg[1] = num // den
    elif opcode == 7:
        # cdv
        num = reg[0]
        den = 2 ** combo(operand, reg)
        reg[2] = num // den
    else:
        raise Exception("not implemented")
    return ip + 2


def run(a: int, data: Data) -> list[int]:
    out = []
    reg = [a, data.b, data.c]
    ip = 0
    while ip < len(data.program):
        opcode = data.program[ip]
        operand = data.program[ip + 1]
        ip = op(
            opcode=opcode,
            operand=operand,
            reg=reg,
            ip=ip,
            out=out,
        )
    return out


def solve(data: Data) -> int:
    print(data)
    program: list[int] = []
    alternatives = [0]
    for target in data.program[::-1]:
        tmp = []
        program = [target, *program]
        print(" ")
        print(program)
        print(list(map(oct, alternatives)))
        for a in alternatives:
            for x in range(8):
                candidate = a * 8 + x
                out = run(candidate, data)
                if out == program:
                    print(oct(a), x, out)
                    tmp.append(candidate)
        alternatives = tmp
    return min(alternatives)


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        a = int(rows[0].split(" ")[-1])
        b = int(rows[1].split(" ")[-1])
        c = int(rows[2].split(" ")[-1])
        program = list(map(int, rows[4].split(" ")[1].split(",")))
        data = Data(a=a, b=b, c=c, program=program)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_1.txt", 117440),
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

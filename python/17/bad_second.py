import math
from dataclasses import dataclass
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


def op(
    opcode: int, operand: int, reg: list[int], ip: int, program: list[int], pc: int
) -> tuple[int, int]:
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
            return operand, pc
    elif opcode == 4:
        # bxc
        reg[1] = reg[1] ^ reg[2]
    elif opcode == 5:
        # out
        out = combo(operand, reg) % 8
        # print(out)
        if pc >= len(program):
            print("!!!")  # this is probably in error
            pass
        elif program[pc] != out:
            pc = -1 - abs(pc)  # indicate error
        else:
            pc += 1
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
    return ip + 2, pc


def solve(data: Data) -> int:
    a = 0
    min_pc = -6  # the pattern appears clearly at 6
    a_step = 1
    while True:
        reg = [a, data.b, data.c]
        ip = 0
        pc = 0  # check where in the program the output should be, negative values indicate error
        while ip < len(data.program):
            opcode = data.program[ip]
            operand = data.program[ip + 1]
            ip, pc = op(
                opcode=opcode,
                operand=operand,
                reg=reg,
                ip=ip,
                program=data.program,
                pc=pc,
            )
            if pc < 0:
                # indication of error
                break
        if pc == len(data.program):  # halts at the right time
            print(oct(a))
            return a
        elif pc < min_pc:
            actual_pc = -1 - pc
            min_pc = pc
            log = int(math.log(a, 8))
            if actual_pc % 2 == 0:
                a_step = 8 ** (int(log) - 1)
            else:
                a_step = 8 ** (int(log) - 1)
            print(oct(a), oct(a_step), actual_pc, log, a)
        a += a_step


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


# 186739162181309 too high
# 732096929558205 too high
# 749689115602621 too high
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

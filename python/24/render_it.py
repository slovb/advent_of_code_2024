from dataclasses import dataclass

from graphviz import Digraph


@dataclass(frozen=True)
class Data:
    wires: dict[str, int]
    gates: list[tuple[str, str, str, str]]
    outputs: list[str]


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        wires = {}
        gates = []
        outputs = []
        first_part = True
        for row in rows:
            if row == "":
                first_part = False
                continue
            if first_part:
                name = row.split(":")[0]
                value = int(row[-1])
                wires[name] = value
            else:
                left, op, right, _, result = row.split(" ")
                gates.append((left, op, right, result))
                outputs.append(result)
        outputs = sorted(outputs)
        data = Data(wires=wires, gates=gates, outputs=outputs)
        return data


def main():
    data = read("input.txt")
    dot = Digraph()

    for name in data.wires:
        dot.node(name, "INPUT")
    for gate in data.gates:
        op = gate[1]
        name = gate[-1]
        dot.node(name, op)
    for gate in data.gates:
        left, op, right, target = gate
        dot.edge(left, target)
        dot.edge(right, target)

    dot.render("graphivz.gv")


if __name__ == "__main__":
    main()

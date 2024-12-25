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

    changes = {
        "z07": "shj",
        "shj": "z07",
        "pfn": "z23",
        "z23": "pfn",
        "z27": "kcd",
        "kcd": "z27",
        "tpk": "wkb",
        "wkb": "tpk",
    }

    for name in data.wires:
        dot.node(name, name)
    for z_ok in [False, True]:
        for gate in data.gates:
            name = gate[-1]
            if name in changes:
                name = changes[name]

            # reorder the rendering
            if name.startswith("z"):
                if not z_ok:
                    continue
            elif z_ok:
                continue

            op = gate[1]
            color = "crimson"
            shape = "triangle"
            if op == "OR":
                color = "forestgreen"
                shape = "invtriangle"
            elif op == "XOR":
                color = "dodgerblue"
                shape = "star"
            label = name
            if name.startswith("z"):
                label += "\n"
            dot.node(name, label, color=color, shape=shape)
    for gate in data.gates:
        left, op, right, target = gate
        dot.edge(left, target)
        dot.edge(right, target)

    dot.render("graphivz.gv")


if __name__ == "__main__":
    main()

from dataclasses import dataclass


@dataclass(frozen=True)
class Data:
    nodes: list[str]
    neighbors: dict[str, list[str]]


def solve(data: Data) -> int:
    sorted_k3s_with_t: set[tuple[str, str, str]] = set()
    nodes_with_t: set[str] = set([node for node in data.nodes if node.startswith("t")])

    for node in data.nodes:
        for i, alpha in enumerate(data.neighbors[node]):
            if alpha < node:
                continue
            for beta in data.neighbors[node][i + 1 :]:
                if beta in data.neighbors[alpha]:
                    if (
                        node in nodes_with_t
                        or alpha in nodes_with_t
                        or beta in nodes_with_t
                    ):
                        print(node, alpha, beta)
                        sorted_k3s_with_t.add((node, alpha, beta))
    return len(sorted_k3s_with_t)


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        nodes_names: set[str] = set()
        neighbors: dict[str, list[str]] = {}
        for row in rows:
            alpha, beta = row.split("-")
            nodes_names.add(alpha)
            nodes_names.add(beta)
            neighbors[alpha] = neighbors.get(alpha, []) + [beta]
            neighbors[beta] = neighbors.get(beta, []) + [alpha]
        nodes = sorted(list(nodes_names))
        for node in nodes:
            neighbors[node] = sorted(neighbors[node])
        data = Data(nodes=nodes, neighbors=neighbors)
        return data


def main(filename):
    return solve(read(filename))


# 2195 too high
if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 7),
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

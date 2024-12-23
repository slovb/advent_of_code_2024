from dataclasses import dataclass


@dataclass(frozen=True)
class Data:
    nodes: list[str]
    neighbors: dict[str, list[str]]


def initial(data: Data) -> set[tuple[str, str, str]]:
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
                        sorted_k3s_with_t.add((node, alpha, beta))
    return sorted_k3s_with_t


def solve(data: Data) -> str:
    k3 = initial(data)
    kn: set[tuple[str, ...]] = set(k3)
    n = 3
    while len(kn) > 1:
        print(f"{n}: {len(kn)}")
        n += 1
        knext: set[tuple[str, ...]] = set()
        for kgroup in kn:
            for node in data.nodes:
                if node in kgroup:
                    continue
                if all([k in data.neighbors[node] for k in kgroup]):
                    extended = tuple(sorted(list(kgroup) + [node]))
                    knext.add(extended)
        kn = knext

    out = next(iter(kn))
    return ",".join(out)


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
        ("test_0.txt", "co,de,ka,ta"),
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

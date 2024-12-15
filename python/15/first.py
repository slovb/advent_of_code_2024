from dataclasses import dataclass


@dataclass(frozen=True)
class Data:
    walls: set[tuple[int, int]]
    boxes: set[tuple[int, int]]
    robot: tuple[int, int]
    moves: list[tuple[int, int]]


def step(pos: tuple[int, int], move: tuple[int, int]) -> tuple[int, int]:
    return (pos[0] + move[0], pos[1] + move[1])


def display(
    walls: set[tuple[int, int]], boxes: set[tuple[int, int]], robot: tuple[int, int]
) -> str:
    width = 0
    height = 0
    for w in walls:
        width = max(width, w[0] + 1)
        height = max(height, w[1] + 1)
    rows = []
    for y in range(height):
        row = []
        for x in range(width):
            pos = (x, y)
            if pos in walls and pos in boxes:
                row.append("$")
                print("ERROR")
            elif pos in walls:
                row.append("#")
            elif pos in boxes:
                row.append("O")
            elif pos == robot:
                row.append("@")
            else:
                row.append(".")
        rows.append("".join(row))
    return "\n".join(rows)


def solve(data: Data) -> int:
    robot = data.robot
    boxes = set(list(data.boxes))
    for move in data.moves:
        # print(display(data.walls, boxes, robot))
        # print(" ")
        # print(move)
        candidate = step(robot, move)
        if candidate in data.walls:
            continue
        elif candidate not in boxes:
            robot = candidate
            continue
        # moving a box
        endpoint = step(candidate, move)
        while endpoint not in data.walls and endpoint in boxes:
            endpoint = step(endpoint, move)
        if endpoint in data.walls:
            continue
        # move the box
        boxes.remove(candidate)
        boxes.add(endpoint)
        robot = candidate
    print(display(data.walls, boxes, robot))

    # score
    out = 0
    for box in boxes:
        out += box[0] + 100 * box[1]
    return out


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        reading_moves = False
        walls: set[tuple[int, int]] = set()
        boxes: set[tuple[int, int]] = set()
        moves: list[tuple[int, int]] = []
        for y, row in enumerate(rows):
            if row == "":
                reading_moves = True
                continue
            if reading_moves:
                for c in row:
                    if c == ">":
                        moves.append((1, 0))
                    elif c == "<":
                        moves.append((-1, 0))
                    elif c == "v":
                        moves.append((0, 1))
                    elif c == "^":
                        moves.append((0, -1))
                    else:
                        raise Exception("Unknown direction")
            else:
                for x, c in enumerate(row):
                    if c == "#":
                        walls.add((x, y))
                    elif c == "O":
                        boxes.add((x, y))
                    elif c == "@":
                        robot = (x, y)
                        print(robot)  # just to make sure there aren't multiple
        return Data(walls=walls, boxes=boxes, robot=robot, moves=moves)


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 2028),
        ("test_1.txt", 10092),
    ]

    if len(sys.argv) < 2:
        has_failed = False
        for filename, value in testcases:
            res = main(filename)
            print("{}   {}\n".format(filename, str(res)))
            if res != value:
                print("Failed test")
                has_failed = True
                break
        if not has_failed:
            filename = "input.txt"
            print("{}   {}\n".format(filename, main(filename)))
    else:
        for f in sys.argv[1:]:
            print("{}:\n{}\n".format(f, main(f)))

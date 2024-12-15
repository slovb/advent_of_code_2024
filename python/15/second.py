from dataclasses import dataclass


@dataclass(frozen=True)
class Data:
    walls: set[tuple[int, int]]
    left_boxes: set[tuple[int, int]]
    right_boxes: set[tuple[int, int]]
    robot: tuple[int, int]
    moves: list[tuple[int, int]]


def step(pos: tuple[int, int], move: tuple[int, int]) -> tuple[int, int]:
    return (pos[0] + move[0], pos[1] + move[1])


def display(
    walls: set[tuple[int, int]],
    left_boxes: set[tuple[int, int]],
    right_boxes: set[tuple[int, int]],
    robot: tuple[int, int],
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
            if pos in walls:
                row.append("#")
            elif pos in left_boxes:
                row.append("[")
            elif pos in right_boxes:
                row.append("]")
            elif pos == robot:
                row.append("@")
            else:
                row.append(".")
        rows.append("".join(row))
    return "\n".join(rows)


def solve(data: Data) -> int:
    robot = data.robot
    left_boxes = set(list(data.left_boxes))
    right_boxes = set(list(data.right_boxes))
    for move in data.moves:
        # print(display(data.walls, left_boxes, right_boxes, robot))
        # print(" ")
        # print(move)
        candidate = step(robot, move)
        if candidate in data.walls:
            continue
        elif candidate not in left_boxes and candidate not in right_boxes:
            robot = candidate
            continue
        # moving a box
        can_move = True
        to_move = [candidate]
        i = 0
        while i < len(to_move):
            pos = to_move[i]
            if pos in data.walls:
                can_move = False
                break
            if pos in left_boxes:
                partner = step(pos, (1, 0))
                if partner not in to_move:
                    to_move.append(partner)
                forward = step(pos, move)
                if forward not in to_move:
                    to_move.append(forward)
            elif pos in right_boxes:
                partner = step(pos, (-1, 0))
                if partner not in to_move:
                    to_move.append(partner)
                forward = step(pos, move)
                if forward not in to_move:
                    to_move.append(forward)
            i += 1
        if not can_move:
            continue
        for pos in to_move[::-1]:
            if pos in left_boxes:
                left_boxes.remove(pos)
                left_boxes.add(step(pos, move))
            elif pos in right_boxes:
                right_boxes.remove(pos)
                right_boxes.add(step(pos, move))
        robot = candidate
    print(display(data.walls, left_boxes, right_boxes, robot))

    # score
    out = 0
    for box in left_boxes:
        out += box[0] + 100 * box[1]
    return out


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        reading_moves = False
        walls: set[tuple[int, int]] = set()
        left_boxes: set[tuple[int, int]] = set()
        right_boxes: set[tuple[int, int]] = set()
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
                        walls.add((2 * x, y))
                        walls.add((2 * x + 1, y))
                    elif c == "O":
                        left_boxes.add((2 * x, y))
                        right_boxes.add((2 * x + 1, y))
                    elif c == "@":
                        robot = (2 * x, y)
        return Data(
            walls=walls,
            left_boxes=left_boxes,
            right_boxes=right_boxes,
            robot=robot,
            moves=moves,
        )


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_1.txt", 9021),
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

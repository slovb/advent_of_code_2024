from dataclasses import dataclass
from heapq import heappop, heappush

from PIL import Image, ImageDraw, ImageFont


@dataclass(frozen=True)
class Data:
    walls: list[tuple[int, int]]
    width: int
    height: int


def display(
    path: list[tuple[int, int]],
    time: int,
    walls: dict[tuple[int, int], int],
    width: int,
    height: int,
):
    pixel_size = 8
    # 2c2c54
    background_color = (0x2C, 0x2C, 0x54)
    # d1ccc0
    wall_color = (0xD1, 0xCC, 0xC0)
    # 34ace0
    path_color = (0x34, 0xAC, 0xE0)

    image = Image.new(
        "RGB", (width * pixel_size, height * pixel_size), background_color
    )
    draw = ImageDraw.Draw(image)

    current = path[-1]
    # time = len(path) + 1
    for y in range(height):
        row = []
        for x in range(width):
            pos = (x, y)
            if pos == current:
                row.append("@")
                draw.rectangle(
                    [
                        (pixel_size * x, pixel_size * y),
                        (pixel_size * (x + 1), pixel_size * (y + 1)),
                    ],
                    fill=path_color,
                )
            elif pos in path:
                row.append("O")
                draw.rectangle(
                    [
                        (pixel_size * x, pixel_size * y),
                        (pixel_size * (x + 1), pixel_size * (y + 1)),
                    ],
                    fill=path_color,
                )
            elif pos in walls and walls[pos] < time:
                row.append("#")
                draw.rectangle(
                    [
                        (pixel_size * x, pixel_size * y),
                        (pixel_size * (x + 1), pixel_size * (y + 1)),
                    ],
                    fill=wall_color,
                )
            else:
                row.append(".")
        print("".join(row))
    return image


def step(pos: tuple[int, int], direction: int) -> tuple[int, int]:
    if direction == 0:
        return (pos[0] + 1, pos[1])
    elif direction == 1:
        return (pos[0], pos[1] + 1)
    elif direction == 2:
        return (pos[0] - 1, pos[1])
    elif direction == 3:
        return (pos[0], pos[1] - 1)
    raise Exception("UNACCEPTABLE!!!")


def collision(
    path: list[tuple[int, int]], time: int, walls: dict[tuple[int, int], int]
) -> bool:
    for pos in path:
        if pos in walls and walls[pos] < time:
            return True
    return False


def solve(data: Data) -> tuple[int, int]:
    walls: dict[tuple[int, int], int] = {}
    for t, w in enumerate(data.walls):
        if w not in walls:
            walls[w] = t

    goal = (data.width - 1, data.height - 1)

    images = []
    path = None
    time = 0
    while time < len(data.walls):
        if path is not None:
            while not collision(path, time, walls):
                time += 1

        paths: list[tuple[int, list[tuple[int, int]]]] = [
            (data.width + data.height, [(0, 0)])
        ]
        memory: dict[tuple[int, int], int] = {}
        # display(paths[0][1], time, walls, data.width, data.height)
        # print(" ")
        can_solve = False
        while len(paths) > 0:
            _, path = heappop(paths)
            # time = len(path) + 1
            pos = path[-1]
            if pos == goal:
                can_solve = True
                images.append(display(path, time, walls, data.width, data.height))
                last_solve = path
                print(" ")
                break

            for dir in range(4):
                candidate = step(pos, dir)
                steps = len(path)
                if candidate in path:
                    # NOT GOING BACK THERE
                    continue
                if candidate in memory and memory[candidate] <= steps:
                    # BETTER PATHS THERE
                    continue
                memory[candidate] = steps
                if not (
                    0 <= candidate[0] < data.width and 0 <= candidate[1] < data.height
                ):
                    # WAHOO!
                    continue
                if candidate in walls and walls[candidate] < time:
                    # BONK
                    continue
                # display(path, time, walls, data.width, data.height)
                # print(" ")
                score = (
                    steps + (data.width - candidate[0]) + (data.height - candidate[1])
                )
                heappush(paths, (score, [*path, candidate]))
        if not can_solve:

            images.append(display(last_solve, time, walls, data.width, data.height))
            fps = 30
            for _ in range(2 * fps):
                images.append(images[-1])
            images[0].save(
                "image/animation.gif",
                save_all=True,
                append_images=images[1:],
                optimize=True,
                duration=1000 // fps,
                loop=0,
            )
            return data.walls[time - 1]
        time += 1
    return (-1, -1)


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        walls: list[tuple[int, int]] = []
        width = 0
        height = 0
        for row in rows:
            parts = tuple(map(int, row.split(",")))
            width = max(width, parts[0] + 1)
            height = max(height, parts[1] + 1)
            walls.append((parts[0], parts[1]))
        data = Data(walls=walls, width=width, height=height)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        # ("test_0.txt", (6, 1)),
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

from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFont


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def scale(self, factor: float):
        return Vector(int(round(factor * self.x)), int(round(factor * self.y)))

    def add(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def mod(self, width, height):
        return Vector(self.x % width, self.y % height)


@dataclass(frozen=True)
class Data:
    input: list[tuple[Vector, Vector]]


def solve(data: Data, width, height) -> int:
    if width % 2 == 0 or height % 2 == 0:
        raise Exception("assumes odd sides")
    half_width = width // 2
    half_height = height // 2

    n = 6444.0
    n_step = 0.01
    # best = 10**18
    best = 0
    images = []
    memory = {}
    while n <= 6446.0:
        n += n_step
        q = [0, 0, 0, 0]
        positions = []
        for pos, vec in data.input:
            future = pos.add(vec.scale(n)).mod(width, height)
            positions.append(future)
            if future.x == half_width or future.y == half_height:
                continue
            index = 0 if future.x < half_width else 1
            index += 0 if future.y < half_height else 2
            q[index] += 1
        metric = max(q) - min(q)
        images.append(display(positions, width, height, memory, n, n_step))
        if metric > best:
            best = metric
            print(f"{n}: {metric}")

    fps = 30
    for _ in range(fps):
        images.append(images[-1])
    images[0].save(
        "image/animation_2.gif",
        save_all=True,
        append_images=images[1:],
        optimize=True,
        duration=1000 // fps,
        loop=0,
    )
    return q[0] * q[1] * q[2] * q[3]


def read(filename) -> Data:
    def read_vector(s):
        _, s = s.split("=")
        l, r = s.split(",")
        return Vector(int(l), int(r))

    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        input = []
        for row in rows:
            p, v = row.split(" ")
            input.append((read_vector(p), read_vector(v)))

        data = Data(input=input)
        return data


def display(
    points: list[Vector],
    width: int,
    height: int,
    memory: dict[tuple[int, int], float],
    n: float,
    n_step: float,
):
    pixel_size = 3
    background_color = (0x0, 0x0, 0x0)
    primary_color = (56, 255, 17)
    # tail_color = (255, 255, 255)
    tail_color = primary_color
    tail_length = 6
    image = Image.new(
        "RGB", (width * pixel_size, height * pixel_size), background_color
    )
    draw = ImageDraw.Draw(image)
    for point in points:
        pos = (point.x, point.y)
        memory[pos] = n
    for y in range(height):
        for x in range(width):
            pos = (x, y)
            if pos in memory:
                diff = (n - memory[pos]) / n_step
                divisor = int(diff) + 1
                if divisor < tail_length:
                    if divisor > 1:
                        color = (
                            tail_color[0] // divisor,
                            tail_color[1] // divisor,
                            tail_color[2] // divisor,
                        )
                    else:
                        color = primary_color
                    draw.rectangle(
                        [
                            (pixel_size * x, pixel_size * y),
                            (pixel_size * (x + 1), pixel_size * (y + 1)),
                        ],
                        fill=color,
                    )
    return image


def main(filename, width=101, height=103):
    return solve(read(filename), width, height)


if __name__ == "__main__":
    import sys

    testcases = [
        # ("test_0.txt", 11, 7, 12),
    ]

    if len(sys.argv) < 2:
        has_failed = False
        for filename, width, height, value in testcases:
            res = main(filename, width, height)
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

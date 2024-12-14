from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFont


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def scale(self, factor: int):
        return Vector(factor * self.x, factor * self.y)

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

    n = 0
    best = 10**18
    images = []
    while True:
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
        # metric = abs(q[0] - q[1]) + abs(q[2] - q[3])
        metric = q[0] * q[1] * q[2] * q[3]
        if metric < best:
            best = metric
            images.append(display(positions, width, height))
            # print(q)
            # print(f"{n}: {metric}")
            # print(" ")
        n += 1
        if best == 69850836:
            break

    fps = 5
    for _ in range(fps):
        images.append(images[-1])
    images[0].save(
        "image/animation.gif",
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


def display(points: list[Vector], width: int, height: int):
    background_color = (0x45, 0x45, 0x45)
    text_color = (56, 255, 17)
    image = Image.new(
        "RGB", (12 + (width + 2) * 6, (height + 2) * 12), background_color
    )
    font = ImageFont.truetype("font.ttf")
    draw = ImageDraw.Draw(image)
    counts: dict[tuple[int, int], int] = {}
    for point in points:
        pos = (point.x, point.y)
        counts[pos] = counts.get(pos, 0) + 1
    for y in range(height):
        row = []
        for x in range(width):
            pos = (x, y)
            if pos in counts:
                n = counts[pos]
                if n > 9:
                    row.append("#")
                else:
                    row.append(str(n))
            else:
                # row.append("·")
                row.append(" ")
        row = "".join(row)
        draw.text((12, 12 + y * 12), row, font=font, fill=text_color)
        print(row)
    print(" ")
    # image.show()
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

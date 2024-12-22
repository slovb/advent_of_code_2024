from dataclasses import dataclass


@dataclass(frozen=True)
class Data:
    secrets: list[int]


def mix(secret: int, value: int) -> int:
    return secret ^ value


def prune(secret: int, mod: int = 16777216) -> int:
    return secret % mod


def process(secret: int) -> int:
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, secret // 32))
    secret = prune(mix(secret, secret * 2048))
    return secret


def solve(data: Data) -> int:
    out = 0
    for secret in data.secrets:
        initial = secret
        for _ in range(2000):
            secret = process(secret)
        out += secret
        print(f"{initial}:\t{secret}")
    return out


def read(filename) -> Data:
    with open(filename, "r") as f:
        rows = [row.rstrip() for row in f.readlines()]
        secrets = []
        for row in rows:
            # row = row.split(",")
            # row = map(str.strip, row)
            # row = map(int, row)

            secrets.append(int(row))
            # input.append(int(row))
            # input.append(list(row))
        data = Data(secrets=secrets)
        return data


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys

    testcases = [
        ("test_0.txt", 37327623),
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

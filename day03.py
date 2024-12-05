from utils import read_to_array
import re

def day03(path: str = "data/day03.txt"):
    # we want all the data as a single line
    data: str = "".join(read_to_array(path))

    # regexes!
    part_1_re: re.Pattern = re.compile(r'mul[(]\d+,\d+[)]')

    # a bit odd that this match returns a tuple, I don't regex enough to figure out how to not make it do that
    part_2_re: re.Pattern = re.compile(r"(mul[(]\d+,\d+[)])|(do[(][)])|(don't[(][)])")

    instructions_1: list[str] = part_1_re.findall(data)
    instructions_2: list[str] = part_2_re.findall(data)

    sum_p1: int = 0
    sum_p2: int = 0

    for instruction in instructions_1:
        # i was thinking of using pattern matching here, but this seemed simpler
        val_str = instruction[4:-1]

        v1, v2 = [int(x.strip()) for x in val_str.split(",")]

        sum_p1 += v1 * v2

    print(f"Day 3 - Part 1: {sum_p1}")

    mul_enabled: bool = True
    for instruction in instructions_2:
        # special handling for the tuple from regex
        i: str = "".join(instruction)

        if i == "do()":
            mul_enabled = True
            continue

        if i == "don't()":
            mul_enabled = False
            continue

        if not mul_enabled:
            continue

        val_str = i[4:-1]

        v1, v2 = [int(x.strip()) for x in val_str.split(",")]

        sum_p2 += v1 * v2

    print(f"Day 3 - Part 2: {sum_p2}")


if __name__ == "__main__":
    print("Test")
    day03("test/day03.txt")
    print("Problem")
    day03("data/day03.txt")

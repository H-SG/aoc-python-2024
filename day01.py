from utils import read_to_array

def day01(path: str = "data/day01.txt"):
    # reusing this function from last year
    data: list[str] = read_to_array(path)

    left: list[int] = []
    right: list[int] = []

    # make a left and right list
    for line in data:
        d_split: list[str] = line.split(" ")
        left.append(int(d_split[0].strip()))
        right.append(int(d_split[-1].strip()))

    # sort them
    left.sort()
    right.sort()

    sum_p1: int = 0
    sum_p2: int = 0

    # do stuff
    for l, r in zip(left, right):
        sum_p1 += abs(l - r)

        sum_p2 += l * right.count(l)

    print(f"Day 1 - Part 1: {sum_p1}")
    print(f"Day 1 - Part 2: {sum_p2}")

if __name__ == "__main__":
    day01()

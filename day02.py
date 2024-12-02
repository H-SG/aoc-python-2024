from utils import read_to_array
from itertools import pairwise

# function to check if safe
def is_safe(levels: list[int]) -> bool:
    sign_neg: bool = False
    sign_pos: bool = False
    for p1, p2 in pairwise(levels):
        if abs(p1 - p2) > 3:
            return False

        if abs(p1 - p2) == 0:
            return False

        if p1 - p2 > 0:
            sign_neg = True

        if p2 - p1 > 0:
            sign_pos = True

        # we have both a positive and negative sign change, big no no
        if sign_pos == sign_neg:
            return False
    
    return True

def day02(path: str = "data/day02.txt"):
    data: list[str] = read_to_array(path)

    sum_p1: int = 0
    sum_p2: int = 0
    for d in data:
        levels: list[int] = [int(x.strip()) for x in d.split(" ")]

        if is_safe(levels):
            sum_p1 += 1

        # let's see if we can identify problematic pairs in the data
        p_index: list[int] = [0 for l in levels]
        s_change: list[int] = []
        for i, (p1, p2) in enumerate(pairwise(levels)):
            if abs(p1 - p2) > 3:
                p_index[i] = 1
                p_index[i + 1] = 1

            if abs(p1 - p2) == 0:
                p_index[i] = 1
                p_index[i + 1] = 1

            if p1 - p2 == 0:
                s_change.append(0)

            if p1 - p2 < 0:
                s_change.append(-1)

            if p2 - p1 < 0:
                s_change.append(1)

        # sign change needs some extra handling, since we need to look at triplets to see which is the outlier
        # maybe
        # it work though
        if abs(sum(s_change)) != len(s_change):
            mean_sign: int = sum(s_change)
            if mean_sign != 0:
                mean_sign //= abs(mean_sign)
            for i, s_i in enumerate(s_change):
                if s_i != mean_sign:
                    p_index[i] = 1
                    p_index[i + 1] = 1

        if sum(p_index) == 0:
            sum_p2 += 1
            continue

        # if the number of faults is greater than 3, no number of removals is going to help us
        if sum(p_index) < 4:
            for i, p in enumerate(p_index):
                if p:
                    new_level = [l for l in levels]
                    new_level.pop(i)

                    if is_safe(new_level):
                        sum_p2 += 1
                        break

    print(f"Day 2 - Part 1: {sum_p1}")
    print(f"Day 2 - Part 2: {sum_p2}")

if __name__ == "__main__":
    # print("Test")
    # day02("test/day02.txt")
    # print("Problem")
    day02("data/day02.txt")

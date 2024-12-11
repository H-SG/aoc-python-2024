from utils import read_to_array   

def get_blinked_stone_dict(stone_dict: dict[int, int]) -> dict[int, int]:
    blinked_stone_dict: dict[int, int] = {}

    for stone, count in stone_dict.items():
        new_stones: list[int] = []

        if stone == 0:
            new_stones.append(1)
        elif len(str(stone)) % 2 == 0:
            s1: int = int(str(stone)[:(len(str(stone))//2)])
            s2: int = int(str(stone)[(len(str(stone))//2):])
            new_stones.append(s1)
            new_stones.append(s2)
        else:
            new_stones.append(stone * 2024)

        for new_stone in new_stones:
            if new_stone not in blinked_stone_dict:
                blinked_stone_dict[new_stone] = 0

            blinked_stone_dict[new_stone] += count

    return blinked_stone_dict

        
def day11(path: str = "data/day11.txt"):
    stones_str: str = read_to_array(path)[0]

    stones: list[int] = [int(x.strip()) for x in stones_str.split(" ")]

    blinks_p1: int = 25
    stone_dict_p1: dict[int, int] = {}
    blinks_p2: int = 75
    stone_dict_p2: dict[int, int] = {}

    for stone in stones:
        if stone not in stone_dict_p1:
            stone_dict_p1[stone] = 0
            stone_dict_p2[stone] = 0

        stone_dict_p1[stone] += 1
        stone_dict_p2[stone] += 1

    for _ in range(blinks_p1):
        stone_dict_p1 = get_blinked_stone_dict(stone_dict_p1)

    for _ in range(blinks_p2):
        stone_dict_p2 = get_blinked_stone_dict(stone_dict_p2)

    print(f"Day 10 - Part 1: {sum([x for x in stone_dict_p1.values()])}")
    print(f"Day 10 - Part 2: {sum([x for x in stone_dict_p2.values()])}")


if __name__ == "__main__":
    print("Test")
    day11("test/day11.txt")
    print("Problem")
    day11("data/day11.txt")
from utils import read_to_array

def get_split_stone_with_dict(stone: int, stone_dict: dict[int, int], curr_blink: int = 0, max_blinks: int = 25) -> dict[int, int]:
    if curr_blink == max_blinks:
        if stone not in stone_dict:
            stone_dict[stone] = 0

        stone_dict[stone] += 1
        return stone_dict
    
    if stone == 0:
        return get_split_stone_with_dict(1, stone_dict, curr_blink + 1, max_blinks=max_blinks)
    
    if len(str(stone)) % 2 == 0:
        s1: int = int(str(stone)[:(len(str(stone))//2)])
        s2: int = int(str(stone)[(len(str(stone))//2):])
    
        stone_dict = get_split_stone_with_dict(s1, stone_dict, curr_blink + 1, max_blinks=max_blinks)
        return get_split_stone_with_dict(s2, stone_dict, curr_blink + 1, max_blinks=max_blinks)
    
    return get_split_stone_with_dict(stone * 2024, stone_dict, curr_blink + 1, max_blinks=max_blinks)



def get_split_stone_count(stone: int, count: int = 0, curr_blink: int = 0, max_blinks: int = 25) -> int:
    if curr_blink == max_blinks:
        return count + 1

    if stone == 0:
        return get_split_stone_count(1, count, curr_blink + 1, max_blinks=max_blinks)
    
    if len(str(stone)) % 2 == 0:
        s1: int = int(str(stone)[:(len(str(stone))//2)])
        s2: int = int(str(stone)[(len(str(stone))//2):])

        count = get_split_stone_count(s1, count, curr_blink + 1, max_blinks=max_blinks)
        return get_split_stone_count(s2, count, curr_blink + 1, max_blinks=max_blinks)
    
    return get_split_stone_count(stone * 2024, count, curr_blink + 1, max_blinks=max_blinks)
    


def day11(path: str = "data/day11.txt"):
    stones_str: str = read_to_array(path)[0]

    stones: list[int] = [int(x.strip()) for x in stones_str.split(" ")]

    blinks: int = 75
    sum_p1: int = 0
    stone_dict: dict[int, int] = {}
    for stone in stones:
        stone_dict = get_split_stone_with_dict(stone, stone_dict, max_blinks=blinks)

    pass

    print(f"Day 10 - Part 1: {sum_p1}")
    # print(f"Day 10 - Part 2: {sum_p2}")


if __name__ == "__main__":
    print("Test")
    day11("test/day11.txt")
    print("Problem")
    day11("data/day11.txt")
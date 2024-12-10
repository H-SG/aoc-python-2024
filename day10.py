from utils import read_to_array

def get_trail_score_p2(current_pos: tuple[int, int], heights: dict[tuple[int, int], int], score: int = 0) -> int:
    current_height: int = heights[current_pos]
    
    if current_height == 9:
        return score + 1
    
    up: tuple[int, int] = (current_pos[0], current_pos[1] - 1)
    down: tuple[int, int] = (current_pos[0], current_pos[1] + 1)
    left: tuple[int, int] = (current_pos[0] - 1, current_pos[1])
    right: tuple[int, int] = (current_pos[0] + 1, current_pos[1])

    neighbours: list[tuple[int, int]] = [up, down, left, right]

    for neighbour in neighbours:
        if neighbour not in heights:
            continue

        neighbour_height: int = heights[neighbour]

        if neighbour_height == current_height + 1:
            score = get_trail_score_p2(neighbour, heights, score)

    return score


def get_trail_score_p1(current_pos: tuple[int, int], heights: dict[tuple[int, int], int], found_heads: set[tuple[int, int]]) -> set[tuple[int, int]]:
    current_height: int = heights[current_pos]
    
    if current_height == 9:
        found_heads.add(current_pos)
        return found_heads
    
    up: tuple[int, int] = (current_pos[0], current_pos[1] - 1)
    down: tuple[int, int] = (current_pos[0], current_pos[1] + 1)
    left: tuple[int, int] = (current_pos[0] - 1, current_pos[1])
    right: tuple[int, int] = (current_pos[0] + 1, current_pos[1])

    neighbours: list[tuple[int, int]] = [up, down, left, right]

    for neighbour in neighbours:
        if neighbour not in heights:
            continue

        neighbour_height: int = heights[neighbour]

        if neighbour_height == current_height + 1:
            found_heads.union(get_trail_score_p1(neighbour, heights, found_heads))

    return found_heads

    
def day10(path: str = "data/day10.txt"):
    hiking_map: list[str] = read_to_array(path)

    heights: dict[tuple[int, int], int] = {}
    trailheads: list[tuple[int, int]] = []

    for y, row in enumerate(hiking_map):
        for x, height in enumerate(row):
            if height == ".":
                continue

            heights[(int(x), int(y))] = int(height)

            if int(height) == 0:
                trailheads.append((int(x), int(y)))

    sum_p2: int = 0
    sum_p1: int = 0

    for trailhead in trailheads:
        sum_p1 += len(get_trail_score_p1(trailhead, heights, found_heads=set()))
        sum_p2 += get_trail_score_p2(trailhead, heights)
        pass

    print(f"Day 10 - Part 1: {sum_p1}")
    print(f"Day 10 - Part 2: {sum_p2}")


if __name__ == "__main__":
    print("Test")
    day10("test/day10.txt")
    print("Problem")
    day10("data/day10.txt")
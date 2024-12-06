from utils import read_to_array
from copy import deepcopy

def replace_char_at_index(string: str, char: str, index: int) -> str:
    return f"{string[:index]}{char}{string[index + 1:]}"

def add_obstacle(obstacle_map: list[str], x, y):
    if obstacle_map[y][x] not in ["#", "^"]:
        obstacle_map[y] = replace_char_at_index(obstacle_map[y], "O", x)

def get_mutated_map(input: list[str], x, y) -> list[str]:
    mutated_map = deepcopy(input)
    if mutated_map[y][x] not in ["#", "^"]:
        mutated_map[y] = replace_char_at_index(mutated_map[y], "#", x)

    return mutated_map

def check_if_looping(new_map: list[str]) -> bool:
    inner_map: list[str] = deepcopy(new_map)

    for y, d in enumerate(inner_map):
        if "^" in d:
            guard_y = y
            guard_x = d.index("^")
            break

    direction: str = "up"

    while (guard_x in range(0, len(inner_map[0]))) and (guard_y in range(0, len(inner_map))):
        up: str = inner_map[(max(0, guard_y - 1))][guard_x]
        down: str = inner_map[min(len(inner_map) - 1, guard_y + 1)][guard_x]
        left: str = inner_map[guard_y][max(0, guard_x - 1)]
        right: str = inner_map[guard_y][min(len(inner_map[0]) - 1, guard_x + 1)]

        match direction:
            case "up":
                if up != "#":
                    match inner_map[guard_y][guard_x]:
                        case "-":
                            inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "+", guard_x)
                        case "+":
                            pass
                        case "*":
                            pass
                        case "^":
                            pass
                        case _:
                            inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "|", guard_x)

                    guard_y -= 1
                    continue

                if inner_map[guard_y][guard_x] == "*":
                    return True

                direction = "right"
                if inner_map[guard_y][guard_x] == "+":
                    inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "*", guard_x)
                else:
                    inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "+", guard_x)
                continue
            case "right":
                if right != "#":
                    match inner_map[guard_y][guard_x]:
                        case "|":
                            inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "+", guard_x)
                        case "+":
                            pass
                        case "*":
                            pass
                        case _:
                            inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "-", guard_x) 

                    guard_x += 1
                    continue

                if inner_map[guard_y][guard_x] == "*":
                    return True

                direction = "down"
                if inner_map[guard_y][guard_x] == "+":
                    inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "*", guard_x)
                else:
                    inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "+", guard_x)
                continue
            case "down":
                if down != "#":
                    match inner_map[guard_y][guard_x]:
                        case "-":
                            inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "+", guard_x)
                        case "+":
                            pass
                        case "*":
                            pass
                        case _:
                            inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "|", guard_x)

                    guard_y += 1
                    continue

                if inner_map[guard_y][guard_x] == "*":
                    return True

                direction = "left"
                if inner_map[guard_y][guard_x] == "+":
                    inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "*", guard_x)
                else:
                    inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "+", guard_x)
                continue
            case "left":
                if left != "#":
                    match inner_map[guard_y][guard_x]:
                        case "|":
                            inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "+", guard_x)
                        case "+":
                            pass
                        case "*":
                            pass
                        case _:
                            inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "-", guard_x)
                    guard_x -= 1
                    continue

                if inner_map[guard_y][guard_x] == "*":
                    return True

                direction = "up"
                if inner_map[guard_y][guard_x] == "+":
                    inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "*", guard_x)
                else:
                    inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "+", guard_x)
                continue

        

    return False

def day06(path: str = "data/day06.txt"):
    # we want all the data as a single line
    travelled_map: list[str] = read_to_array(path)
    original_map: list[str] = read_to_array(path)
    obstacle_map: list[str] = read_to_array(path)

    guard_x: int
    guard_y: int

    for y, d in enumerate(travelled_map):
        if "^" in d:
            guard_y = y
            guard_x = d.index("^")

    initial_y: int = guard_y
    initial_x: int = guard_x

    direction: str = "up"

    while (guard_x in range(0, len(travelled_map[0]))) and (guard_y in range(0, len(travelled_map))):
        up: str = travelled_map[(max(0, guard_y - 1))][guard_x]
        down: str = travelled_map[min(len(travelled_map) - 1, guard_y + 1)][guard_x]
        left: str = travelled_map[guard_y][max(0, guard_x - 1)]
        right: str = travelled_map[guard_y][min(len(travelled_map[0]) - 1, guard_x + 1)]

        if guard_y == 6:
            if guard_x == 3:
                pass

        if check_if_looping(get_mutated_map(original_map, guard_x, guard_y)):
            add_obstacle(obstacle_map, guard_x, guard_y)

        match direction:
            case "up":
                if up != "#":
                    match travelled_map[guard_y][guard_x]:
                        case "-":
                            travelled_map[guard_y] = replace_char_at_index(travelled_map[guard_y], "+", guard_x)
                        case "+":
                            pass
                        case "^":
                            pass
                        case _:
                            travelled_map[guard_y] = replace_char_at_index(travelled_map[guard_y], "|", guard_x)

                    guard_y -= 1
                    continue                    

                direction = "right"
                travelled_map[guard_y] = replace_char_at_index(travelled_map[guard_y], "+", guard_x)
                continue
            case "right":
                if right != "#":
                    match travelled_map[guard_y][guard_x]:
                        case "|":
                            travelled_map[guard_y] = replace_char_at_index(travelled_map[guard_y], "+", guard_x)
                        case "+":
                            pass
                        case _:
                            travelled_map[guard_y] = replace_char_at_index(travelled_map[guard_y], "-", guard_x)
                    
                    guard_x += 1
                    continue

                direction = "down"
                travelled_map[guard_y] = replace_char_at_index(travelled_map[guard_y], "+", guard_x)
                continue
            case "down":
                if down != "#":
                    match travelled_map[guard_y][guard_x]:
                        case "-":
                            travelled_map[guard_y] = replace_char_at_index(travelled_map[guard_y], "+", guard_x)
                        case "+":
                            pass
                        case _:
                            travelled_map[guard_y] = replace_char_at_index(travelled_map[guard_y], "|", guard_x)

                    guard_y += 1
                    continue                    

                direction = "left"
                travelled_map[guard_y] = replace_char_at_index(travelled_map[guard_y], "+", guard_x)
                continue
            case "left":
                if left != "#":
                    match travelled_map[guard_y][guard_x]:
                        case "|":
                            travelled_map[guard_y] = replace_char_at_index(travelled_map[guard_y], "+", guard_x)
                        case "+":
                            pass
                        case _:
                            travelled_map[guard_y] = replace_char_at_index(travelled_map[guard_y], "-", guard_x)
                    guard_x -= 1
                    continue                    

                direction = "up"
                travelled_map[guard_y] = replace_char_at_index(travelled_map[guard_y], "+", guard_x)
                continue
    
    sum_p1: int = 0
    sum_p2: int = 0

    for d in travelled_map:
        sum_p1 += d.count("|")
        sum_p1 += d.count("+")
        sum_p1 += d.count("-")
        sum_p1 += d.count("^")

    for d in obstacle_map:
        sum_p2 += d.count("O")
        
                        

    print(f"Day 6 - Part 1: {sum_p1}")
    print(f"Day 6 - Part 2: {sum_p2}")
    pass


if __name__ == "__main__":
    print("Test")
    day06("test/day06.txt")
    print("Problem")
    day06("data/day06.txt")
from utils import read_to_array

def replace_char_at_index(string: str, char: str, index: int) -> str:
    return f"{string[:index]}{char}{string[index + 1:]}"

def add_obstacle(obstacle_map: list[str], x, y):
    if obstacle_map[y][x] not in ["#", "^"]:
        obstacle_map[y] = replace_char_at_index(obstacle_map[y], "O", x)

def day06(path: str = "data/day06.txt"):
    # we want all the data as a single line
    travelled_map: list[str] = read_to_array(path)
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

        pass

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

                    right_path: str = travelled_map[guard_y][guard_x + 1:]
                    for i, char in enumerate(right_path):
                        if char == "#":
                            if i == 0:
                                break
                            
                            if right_path[i - 1] in ["|", "+"]:
                                add_obstacle(obstacle_map, guard_x, guard_y - 1)
                                break

                    guard_y -= 1
                    # if up in ["^", "-"]:
                    #     add_obstacle(obstacle_map, guard_x, guard_y - 1)
                    
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
                    
                    down_path: str = "".join([travelled_map[y][guard_x] for y in range(guard_y, len(travelled_map))])
                    for i, char in enumerate(down_path):
                        if char == "#":
                            if i == 0:
                                break
                            
                            if down_path[i - 1] in ["-", "+"]:
                                add_obstacle(obstacle_map, guard_x + 1, guard_y)
                                break

                    guard_x += 1

                    #if right in ["^", "|"]:
                        #add_obstacle(obstacle_map, guard_x + 1, guard_y)
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

                    left_path: str = travelled_map[guard_y][:guard_x][::-1]
                    for i, char in enumerate(left_path):
                        if char == "#":
                            if i == 0:
                                break
                            
                            if left_path[i - 1] in ["|", "+"]:
                                add_obstacle(obstacle_map, guard_x, guard_y + 1)
                                break
                    guard_y += 1

                    # if down in ["^", "-"]:
                    #     add_obstacle(obstacle_map, guard_x, guard_y + 1)
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

                    up_path: str = "".join([travelled_map[y][guard_x] for y in range(0, guard_y)])[::-1]
                    for i, char in enumerate(up_path):
                        if char == "#":
                            if i == 0:
                                break
                            
                            if up_path[i - 1] in ["-", "+"]:
                                add_obstacle(obstacle_map, guard_x - 1, guard_y)
                                break

                    # if left in ["^", "|"]:
                    #     add_obstacle(obstacle_map, guard_x - 1, guard_y)
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

    for y, row in enumerate(obstacle_map):
        for x, char in enumerate(row):
            if x == initial_x:
                if y <= initial_y:
                    continue
            if char == "O":
                sum_p2 += 1

            # sum_p2 += o.count("O")
                        

    print(sum_p1)
    print(sum_p2)
    pass


if __name__ == "__main__":
    print("Test")
    day06("test/day06.txt")
    print("Problem")
    day06("data/day06.txt")
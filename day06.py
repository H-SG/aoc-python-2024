from utils import read_to_array
from copy import deepcopy

direction_dict: dict[str, str] = {
    "^":">",
    ">":"v",
    "v":"<",
    "<":"^"
}

path_symbol_dict: dict[str, str] = {
    "|":"+",
    "-":"+",
    "+":"*"
}

move_symbol_dict: dict[str, str] = {
    "^":"|",
    "v":"|",
    "<":"-",
    ">":"-"
}

def add_obstacle(map: list[str], x, y):
    if map[y][x] not in ["#", "^"]:
        map[y] = replace_char_at_index(map[y], "O", x)

def replace_char_at_index(string: str, char: str, index: int) -> str:
    return f"{string[:index]}{char}{string[index + 1:]}"

def update_map(map: list[str], x: int, y: int, new_tile: str):
    map[y] = replace_char_at_index(map[y], new_tile, x)

def get_ahead_tile(map: list[str], x: int, y: int, direction: str) -> None | str:
    match direction:
        case "^":
            if y - 1 < 0:
                return None
            
            return map[y - 1][x]
        case "v":
            if y + 1 >= len(map):
                return None
            
            return map[y + 1][x]
        case "<":
            if x - 1 < 0:
                return None
            
            return map[y][x - 1]
        case ">":
            if x + 1 >= len(map[0]):
                return None
            
            return map[y][x + 1]
        
def add_obstacle_to_ahead_tile(map: list[str], x: int, y: int, direction: str):
    match direction:
        case "^":
            if y - 1 < 0:
                return
            
            return update_map(map, x, y - 1, "#")
        case "v":
            if y + 1 >= len(map):
                return
            
            return update_map(map, x, y + 1, "#")
        case "<":
            if x - 1 < 0:
                return
            
            return update_map(map, x - 1, y, "#")
        case ">":
            if x + 1 >= len(map[0]):
                return
            
            return update_map(map, x + 1, y, "#")

def get_ahead_xy(map: list[str], x: int, y: int, direction: str) -> None | tuple[int, int]:
    match direction:
        case "^":
            if y - 1 < 0:
                return None
            
            return x, y - 1
        case "v":
            if y + 1 >= len(map):
                return None
            
            return x, y + 1
        case "<":
            if x - 1 < 0:
                return None
            
            return x - 1, y
        case ">":
            if x + 1 >= len(map[0]):
                return None
            
            return x + 1, y


class GuardState():
    x: int
    y: int
    direction: str
    current_tile: str
    ahead_tile: None | str
    x_lim: int
    y_lim: int

    def __init__(self, map: list[str]):
        for y, row in enumerate(map):
            if "^" in row:
                self.y = y
                self.x = row.index("^")
                self.direction = "^"                
                break

            if ">" in row:
                self.y = y
                self.x = row.index(">")
                self.direction = ">"
                break

            if "<" in row:
                self.y = y
                self.x = row.index("<")
                self.direction = "<"
                break
            
            if "v" in row:
                self.y = y
                self.x = row.index("v")
                self.direction = "v"
                break

        self.ahead_tile = get_ahead_tile(map, self.x, self.y, self.direction)
        self.current_tile = self.direction

    def _update_pos(self):
        match self.direction:
            case "^":
                self.y -= 1
            case "v":
                self.y += 1
            case "<":
                self.x -= 1
            case ">":
                self.x += 1

    def add_obstacle(self, map: list[str]):
        self.ahead_tile = "#"


    def _current_move_map_tile(self) -> str:
        return path_symbol_dict.get(self.current_tile, move_symbol_dict[self.direction])

    def move(self, map: list[str]) -> bool:
        match self.ahead_tile:
            case None:
                update_map(map, self.x, self.y, self._current_move_map_tile())
                return False
            case "#":
                self.direction = direction_dict[self.direction]
                self.current_tile = map[self.y][self.x]
                update_map(map, self.x, self.y, self._current_move_map_tile())
                self.ahead_tile = get_ahead_tile(map, self.x, self.y, self.direction)
                if self.ahead_tile == "#":
                    self.direction = direction_dict[self.direction]
                    self.ahead_tile = get_ahead_tile(map, self.x, self.y, self.direction)
                return True
            case _:
                self._update_pos()
                self.current_tile = map[self.y][self.x]
                update_map(map, self.x, self.y, self._current_move_map_tile())
                self.ahead_tile = get_ahead_tile(map, self.x, self.y, self.direction)
                return True
            
    def move_check_loop(self, map:list[str]) -> tuple[bool, None | tuple[int, int]]:
        if self.ahead_tile != ".":
            return False, None
        
        temp_map = deepcopy(map)
        add_obstacle_to_ahead_tile(temp_map, self.x, self.y, self.direction)
        xy_pair: None | tuple[int, int] = get_ahead_xy(temp_map, self.x, self.y, self.direction)        
        temp_guard: GuardState = deepcopy(self)
        temp_guard.ahead_tile = "#"
        while temp_guard.move(temp_map):
            if temp_guard.ahead_tile == "*":
                return True, xy_pair
            
        return False, xy_pair
            
    # def move_check_loop(self, map: list[str], obstacle_map: list[str]) -> bool:
    #     match self.ahead_tile:
    #         case None:
    #             update_map(map, self.x, self.y, self._current_move_map_tile())
    #             return False
    #         case "#":
    #             self.direction = direction_dict[self.direction]
    #             self.current_tile = map[self.y][self.x]
    #             update_map(map, self.x, self.y, self._current_move_map_tile())
    #             self.ahead_tile = get_ahead_tile(map, self.x, self.y, self.direction)
    #             # return True
    #         case "*":
    #             return True
    #         case _:
    #             new_guard: GuardState = deepcopy.self()
    #             new_guard.ahead_tile = "#"
                
    #             self._update_pos()
    #             self.current_tile = map[self.y][self.x]
    #             update_map(map, self.x, self.y, self._current_move_map_tile())
    #             self.ahead_tile = get_ahead_tile(map, self.x, self.y, self.direction)
    #             # return True

def day06(path: str = "data/day06.txt"):
    travelled_map: list[str] = read_to_array(path)
    obstacle_map: list[str] = deepcopy(travelled_map)

    guard_p1: GuardState = GuardState(travelled_map)

    is_loop: bool
    possible_obstacle: None | tuple[int, int]
    is_loop, possible_obstacle = guard_p1.move_check_loop(travelled_map)
    if is_loop:
        if possible_obstacle is not None:
            add_obstacle(obstacle_map, *possible_obstacle)

    while guard_p1.move(travelled_map):
        is_loop, possible_obstacle = guard_p1.move_check_loop(travelled_map)
        if is_loop:
            if possible_obstacle is not None:
                temp_map = deepcopy(obstacle_map)
                add_obstacle(temp_map, *possible_obstacle)
                guard_p2: GuardState = GuardState(obstacle_map)
                while guard_p2.move(temp_map):
                    pass
                add_obstacle(obstacle_map, *possible_obstacle)

    flat_map: str = "".join(travelled_map)
    sum_p1: int = len(flat_map) - (flat_map.count(".") + flat_map.count("#"))
    sum_p2: int = "".join(obstacle_map).count("O")

    print(f"Day 6 - Part 1: {sum_p1}")
    print(f"Day 6 - Part 2: {sum_p2}")
    pass

        
        


        











# def get_mutated_map(input: list[str], x, y) -> list[str]:
#     mutated_map = deepcopy(input)
#     if mutated_map[y][x] not in ["#", "^"]:
#         mutated_map[y] = replace_char_at_index(mutated_map[y], "#", x)

#     return mutated_map

# def check_if_looping(inner_map: list[str], guard_x: int, guard_y: int, direction: str) -> bool:
#     while (guard_x in range(0, len(inner_map[0]))) and (guard_y in range(0, len(inner_map))):
#         up: str = inner_map[(max(0, guard_y - 1))][guard_x]
#         down: str = inner_map[min(len(inner_map) - 1, guard_y + 1)][guard_x]
#         left: str = inner_map[guard_y][max(0, guard_x - 1)]
#         right: str = inner_map[guard_y][min(len(inner_map[0]) - 1, guard_x + 1)]

#         match direction:
#             case "up":
#                 if up != "#":
#                     match inner_map[guard_y][guard_x]:
#                         case "-":
#                             inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "+", guard_x)
#                         case "+":
#                             pass
#                         case "*":
#                             pass
#                         case "^":
#                             pass
#                         case _:
#                             inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "|", guard_x)

#                     guard_y -= 1
#                     continue

#                 if inner_map[guard_y][guard_x] == "*":
#                     return True

#                 direction = "right"
#                 if inner_map[guard_y][guard_x] == "+":
#                     inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "*", guard_x)
#                 else:
#                     inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "+", guard_x)
#                 continue
#             case "right":
#                 if right != "#":
#                     match inner_map[guard_y][guard_x]:
#                         case "|":
#                             inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "+", guard_x)
#                         case "+":
#                             pass
#                         case "*":
#                             pass
#                         case _:
#                             inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "-", guard_x) 

#                     guard_x += 1
#                     continue

#                 if inner_map[guard_y][guard_x] == "*":
#                     return True

#                 direction = "down"
#                 if inner_map[guard_y][guard_x] == "+":
#                     inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "*", guard_x)
#                 else:
#                     inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "+", guard_x)
#                 continue
#             case "down":
#                 if down != "#":
#                     match inner_map[guard_y][guard_x]:
#                         case "-":
#                             inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "+", guard_x)
#                         case "+":
#                             pass
#                         case "*":
#                             pass
#                         case _:
#                             inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "|", guard_x)

#                     guard_y += 1
#                     continue

#                 if inner_map[guard_y][guard_x] == "*":
#                     return True

#                 direction = "left"
#                 if inner_map[guard_y][guard_x] == "+":
#                     inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "*", guard_x)
#                 else:
#                     inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "+", guard_x)
#                 continue
#             case "left":
#                 if left != "#":
#                     match inner_map[guard_y][guard_x]:
#                         case "|":
#                             inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "+", guard_x)
#                         case "+":
#                             pass
#                         case "*":
#                             pass
#                         case _:
#                             inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "-", guard_x)
#                     guard_x -= 1
#                     continue

#                 if inner_map[guard_y][guard_x] == "*":
#                     return True

#                 direction = "up"
#                 if inner_map[guard_y][guard_x] == "+":
#                     inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "*", guard_x)
#                 else:
#                     inner_map[guard_y] = replace_char_at_index(inner_map[guard_y], "+", guard_x)
#                 continue

        

#     return False


#     # we want all the data as a single line
#     travelled_map: list[str] = read_to_array(path)
#     original_map: list[str] = read_to_array(path)
#     good_map: list[str] = read_to_array(path)
#     obstacle_map: list[str] = read_to_array(path)

#     guard_x: int
#     guard_y: int

#     for y, d in enumerate(travelled_map):
#         if "^" in d:
#             guard_y = y
#             guard_x = d.index("^")

#     direction: str = "up"

#     initial_x: int = guard_x
#     initial_y: int = guard_y

#     while (guard_x in range(0, len(travelled_map[0]))) and (guard_y in range(0, len(travelled_map))):
#         up: str = travelled_map[(max(0, guard_y - 1))][guard_x]
#         down: str = travelled_map[min(len(travelled_map) - 1, guard_y + 1)][guard_x]
#         left: str = travelled_map[guard_y][max(0, guard_x - 1)]
#         right: str = travelled_map[guard_y][min(len(travelled_map[0]) - 1, guard_x + 1)]

#         if check_if_looping(get_mutated_map(original_map, guard_x, guard_y), initial_x, initial_y, "up"):
#             add_obstacle(good_map, guard_x, guard_y)

#         match direction:
#             case "up":
#                 if check_if_looping(get_mutated_map(travelled_map, guard_x, guard_y - 1), guard_x, guard_y, "up"):
#                     if "".join(good_map).count("O") != "".join(obstacle_map).count("O"):
#                         pass
#                         check_if_looping(get_mutated_map(travelled_map, guard_x, guard_y - 1), guard_x, guard_y, "up")
#                     add_obstacle(obstacle_map, guard_x, guard_y - 1)
#             case "down":
#                 if guard_y + 1 < len(travelled_map):
#                     if check_if_looping(get_mutated_map(travelled_map, guard_x, guard_y + 1), guard_x, guard_y, "down"):
#                         if "".join(good_map).count("O") != "".join(obstacle_map).count("O"):
#                             pass
#                         add_obstacle(obstacle_map, guard_x, guard_y + 1)
#             case "left":
#                 if check_if_looping(get_mutated_map(travelled_map, guard_x - 1, guard_y), guard_x, guard_y, "left"):
#                     if "".join(good_map).count("O") != "".join(obstacle_map).count("O"):
#                         pass
#                     add_obstacle(obstacle_map, guard_x - 1, guard_y)
#             case "right":
#                 if guard_x + 1 < len(travelled_map[0]):
#                     if check_if_looping(get_mutated_map(travelled_map, guard_x + 1, guard_y), guard_x, guard_y, "right"):
#                         if "".join(good_map).count("O") != "".join(obstacle_map).count("O"):
#                             pass
#                         add_obstacle(obstacle_map, guard_x + 1, guard_y)

        
        


#         match direction:
#             case "up":
#                 if up != "#":
#                     match travelled_map[guard_y][guard_x]:
#                         case "-":
#                             travelled_map[guard_y] = replace_char_at_index(travelled_map[guard_y], "+", guard_x)
#                         case "+":
#                             pass
#                         case "^":
#                             pass
#                         case _:
#                             travelled_map[guard_y] = replace_char_at_index(travelled_map[guard_y], "|", guard_x)

#                     guard_y -= 1
#                     continue                    

#                 direction = "right"
#                 travelled_map[guard_y] = replace_char_at_index(travelled_map[guard_y], "+", guard_x)
#                 continue
#             case "right":
#                 if right != "#":
#                     match travelled_map[guard_y][guard_x]:
#                         case "|":
#                             travelled_map[guard_y] = replace_char_at_index(travelled_map[guard_y], "+", guard_x)
#                         case "+":
#                             pass
#                         case _:
#                             travelled_map[guard_y] = replace_char_at_index(travelled_map[guard_y], "-", guard_x)
                    
#                     guard_x += 1
#                     continue

#                 direction = "down"
#                 travelled_map[guard_y] = replace_char_at_index(travelled_map[guard_y], "+", guard_x)
#                 continue
#             case "down":
#                 if down != "#":
#                     match travelled_map[guard_y][guard_x]:
#                         case "-":
#                             travelled_map[guard_y] = replace_char_at_index(travelled_map[guard_y], "+", guard_x)
#                         case "+":
#                             pass
#                         case _:
#                             travelled_map[guard_y] = replace_char_at_index(travelled_map[guard_y], "|", guard_x)

#                     guard_y += 1
#                     continue                    

#                 direction = "left"
#                 travelled_map[guard_y] = replace_char_at_index(travelled_map[guard_y], "+", guard_x)
#                 continue
#             case "left":
#                 if left != "#":
#                     match travelled_map[guard_y][guard_x]:
#                         case "|":
#                             travelled_map[guard_y] = replace_char_at_index(travelled_map[guard_y], "+", guard_x)
#                         case "+":
#                             pass
#                         case _:
#                             travelled_map[guard_y] = replace_char_at_index(travelled_map[guard_y], "-", guard_x)
#                     guard_x -= 1
#                     continue                    

#                 direction = "up"
#                 travelled_map[guard_y] = replace_char_at_index(travelled_map[guard_y], "+", guard_x)
#                 continue
    
#     sum_p1: int = 0
#     sum_p2: int = 0
#     sum_p2_alt: int = 0

#     for d in travelled_map:
#         sum_p1 += d.count("|")
#         sum_p1 += d.count("+")
#         sum_p1 += d.count("-")
#         sum_p1 += d.count("^")

#     for d in obstacle_map:
#         sum_p2 += d.count("O")

#     for d in good_map:
#         sum_p2_alt += d.count("O")
        
                        

#     print(f"Day 6 - Part 1: {sum_p1}")
#     print(f"Day 6 - Part 2: {sum_p2}")
#     print(f"Day 6 - Part 2: {sum_p2_alt}")
#     pass

#     # for y, (o, g) in enumerate(zip(obstacle_map, good_map)):
#     #     for x, (oc, og) in enumerate(zip(o, g)):
#     #         if (oc == "O") and (og != "O"):
#     #             print(oc)
#     #             print(og)
#     #             print((x, y))



if __name__ == "__main__":
    print("Test")
    day06("test/day06.txt")
    print("Problem")
    day06("data/day06.txt")
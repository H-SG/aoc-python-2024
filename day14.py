from utils import read_to_array

class Robot():
    x: int
    y: int
    vel_x: int
    vel_y: int
    max_x: int
    max_y: int

    def __init__(self, starting: str, max_x: int = 11, max_y: int = 7):
        self.max_x = max_x
        self.max_y = max_y

        pos_str: str
        vel_str: str

        pos_str, vel_str = starting.split(" ")

        self.x = int(pos_str[2:].split(",")[0])
        self.y = int(pos_str[2:].split(",")[-1])

        self.vel_x = int(vel_str[2:].split(",")[0])
        self.vel_y = int(vel_str[2:].split(",")[-1])

        pass

    def get_pos_after_n_seconds(self, n_seconds: int = 100) -> tuple[int, int]:
        x: int = (self.x + (n_seconds * self.vel_x)) % self.max_x
        y: int = (self.y + (n_seconds * self.vel_y)) % self.max_y

        if x < 0:
            x = self.max_x + x

        if y < 0:
            y = self.max_y + y

        return (x, y)


def print_robo_pos(positions: set[tuple[int, int]], max_x: int, max_y: int):
    strings: list[list[str]] = [["." for x in range(max_x)] for y in range(max_y)]

    for pos in positions:
        strings[pos[1]][pos[0]] = "X"

    print_str: str = ""
    for string in strings:
        print_str += f"{"".join(string)}\n"

    print(print_str)


def day14_p2(path: str = "data/day14.txt", max_x: int = 101, max_y: int = 103):
    robots: list[str] = read_to_array(path)
    n_seconds: int = 0

    robos: list[Robot] = []
    for robot in robots:
        robo: Robot = Robot(robot, max_x, max_y)
        robos.append(robo)

    while True:
        positions: set[tuple[int, int]] = set()
        for robo in robos:
            pos: tuple[int, int] = robo.get_pos_after_n_seconds(n_seconds)
            if pos in positions:
                break

            positions.add(pos)
        else:
            break

        n_seconds += 1

    print(f"Day 14 - Part 2: {n_seconds}")
    print_robo_pos(positions, max_x, max_y)


def day14_p1(path: str = "data/day14.txt", max_x: int = 11, max_y: int = 7, n_seconds: int = 100):
    robots: list[str] = read_to_array(path)

    positions_count: dict[tuple[int, int], int] = {}

    for robot in robots:
        robo: Robot = Robot(robot, max_x, max_y)
        robo_pos_p1: tuple[int, int] = robo.get_pos_after_n_seconds(n_seconds)

        if robo_pos_p1 not in positions_count:
            positions_count[robo_pos_p1] = 0

        positions_count[robo_pos_p1] += 1

    q1: int = 0
    q2: int = 0
    q3: int = 0
    q4: int = 0
    
    for position, count in positions_count.items():
        in_top: bool
        in_left: bool = position[0] < (max_x // 2)

        if position[1] < (max_y // 2):
            in_top = True

        if position[1] > (max_y // 2):
            in_top = False

        if position[1] == (max_y // 2):
            continue

        if position[0] < (max_x // 2):
            in_left = True

        if position[0] > (max_x // 2):
            in_left = False

        if position[0] == (max_x // 2):
            continue

        match [in_top, in_left]:
            case [True, True]:
                q1 += count
            case [True, False]:
                q2 += count
            case [False, True]:
                q3 += count
            case [False, False]:
                q4 += count
    
    print(f"Day 14 - Part 1: {q1 * q2 * q3 * q4}")

if __name__ == "__main__":
    print("Test")
    day14_p1("test/day14.txt")
    print("Problem")
    day14_p1("data/day14.txt", 101, 103)
    day14_p2()
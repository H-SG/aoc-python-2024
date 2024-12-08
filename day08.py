from utils import read_to_array
from itertools import combinations

def is_valid_pos(pos:  tuple[int,  int], max_x: int, max_y: int) -> bool:
    if pos[0] < 0:
        return False
    
    if pos[0] > max_x:
        return False
    
    if pos[1] < 0:
        return False
    
    if pos[1] > max_y:
        return False
    
    return True

def get_antinodes(ant1: tuple[int, int], ant2: tuple[int, int], max_x: int, max_y: int, multiple: bool = False) -> list[tuple[int, int]]:
    inter_path: tuple[int, int] = (ant1[0] - ant2[0], ant1[1] - ant2[1])

    nodes: list[tuple[int, int]] = []

    node: tuple[int, int] = (ant1[0] + inter_path[0], ant1[1] + inter_path[1])
    while True:
        if not is_valid_pos(node, max_x, max_y):
            break

        nodes.append(node)

        if not multiple:
            break

        node = (node[0] + inter_path[0], node[1] + inter_path[1])

    
    node = (ant2[0] - inter_path[0], ant2[1] - inter_path[1])
    while True:
        if not is_valid_pos(node, max_x, max_y):
            break

        nodes.append(node)

        if not multiple:
            break

        node = (node[0] - inter_path[0], node[1] - inter_path[1])

    if multiple:
        nodes.append(ant1)
        nodes.append(ant2)

    return nodes


def day08(path: str = "data/day08.txt"):
    antenna_map: list[str] = read_to_array(path)

    antenna_dict: dict[str, list[tuple[int, int]]] = {}
    antinodes_p1: list[tuple[int, int]] = []
    antinodes_p2: list[tuple[int, int]] = []

    max_x: int = len(antenna_map[0]) - 1
    max_y: int = len(antenna_map) - 1

    for y, row in enumerate(antenna_map):
        for x, entry in enumerate(row):
            if entry == ".":
                continue

            if entry == "#":
                continue

            if entry not in antenna_dict:
                antenna_dict[entry] = []

            antenna_dict[entry].append((x, y))

    for antennas in antenna_dict.values():
        antenna_pairs: combinations = combinations(antennas, 2)

        for ant1, ant2 in antenna_pairs:
            antinode_p1: list[tuple[int, int]] = get_antinodes(ant1, ant2, max_x, max_y, multiple=False)
            antinode_p2: list[tuple[int, int]] = get_antinodes(ant1, ant2, max_x, max_y, multiple=True)

            for node in antinode_p1:
                if node in antinodes_p1:
                    continue

                antinodes_p1.append(node)

            for node in antinode_p2:
                if node in antinodes_p2:
                    continue

                antinodes_p2.append(node)

    print(f"Day 8 - Part 1: {len(antinodes_p1)}")
    print(f"Day 8 - Part 2: {len(antinodes_p2)}")

if __name__ == "__main__":
    print("Test")
    day08("test/day08.txt")
    print("Problem")
    day08("data/day08.txt")




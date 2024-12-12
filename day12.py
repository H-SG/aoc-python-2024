from utils import read_to_array

# def print_perim_map(perim_map: list[list[int]]):
#     print_str: str = ""
#     for string in perim_map:
#         print_str += f"{"".join([str(x) for x in string])}\n"

#     print(print_str)

# def get_sum_perim_map(perim_map: list[list[int]]) -> int:
#     corners: int = 0
#     for row in perim_map:
#         corners += sum([x for x in row])

#     return corners

# def get_perim_map(region: set[tuple[int, int, str]]) -> list[list[int]]:
#     max_x = max([x for x, *_ in region]) + 2
#     max_y = max([y for _, y, _ in region]) + 2

#     perim_map: list[list[int]] = [[0 for x in range(max_x)] for y in range(max_y)]

#     for plot in region:
#         perim_map[plot[1]][plot[0]] = 0

#     return perim_map

def get_sides_from_stranger(region: list[tuple[int, int]]) -> int:
    min_r = min(r for r, c in region)
    max_r = max(r for r, c in region)
    min_c = min(c for r, c in region)
    max_c = max(c for r, c in region)

    total = 0

    edges = dict()
    for row in range(min_r, max_r + 1):
        prev_in = False
        next_edges = dict()
        for col in range(min_c, max_c + 2):
            if ((row, col) in region) != prev_in:
                prev_in = not prev_in
                next_edges[col] = prev_in
                if edges.get(col) != prev_in:
                    total += 1
        edges = next_edges

    edges = dict()
    for col in range(min_c, max_c + 1):
        prev_in = False
        next_edges = dict()
        for row in range(min_r, max_r + 2):
            if ((row, col) in region) != prev_in:
                prev_in = not prev_in
                next_edges[row] = prev_in
                if edges.get(row) != prev_in:
                    total += 1
        edges = next_edges

    # print(f"Sides: {total}")
    return total

def print_region(region: set[tuple[int, int, str]]):
    max_x = max([x for x, *_ in region]) + 1
    max_y = max([y for _, y, _ in region]) + 1

    strings: list[list[str]] = [["." for x in range(max_x)] for y in range(max_y)]

    for plot in region:
        strings[plot[1]][plot[0]] = plot[2]

    print_str: str = ""
    for string in strings:
        print_str += f"{"".join(string)}\n"

    print(print_str)

def get_region(current_plot: tuple[int, int, str], region_plots: set[tuple[int, int, str]], available_plots: set[tuple[int, int, str]]) -> set[tuple[int, int, str]]:
    region_plots.add(current_plot)
    if current_plot in available_plots:
        available_plots.remove(current_plot)

    left_plot: tuple[int, int, str] = (current_plot[0] - 1, current_plot[1], current_plot[2])
    right_plot: tuple[int, int, str] = (current_plot[0] + 1, current_plot[1], current_plot[2])
    up_plot: tuple[int, int, str] = (current_plot[0], current_plot[1] - 1, current_plot[2])
    down_plot: tuple[int, int, str] = (current_plot[0], current_plot[1] + 1, current_plot[2])

    plots: list[tuple[int, int, str]] = [left_plot, right_plot, up_plot, down_plot]

    for plot in plots:
        if plot in available_plots:
            get_region(plot, region_plots, available_plots)

    return region_plots


def get_sides_following_path(perimeters: list[tuple[int, int]]) -> int:
    perims: set = set(perimeters)

    

def get_sides(perimeters: list[tuple[int, int]]) -> int:
    perims = [p for p in perimeters]
    sides: int = 0
    while len(perimeters) > 0:
        sides += 1
        current_perimeter: tuple[int, int] = perimeters.pop()
        removed: list[tuple[int, int]] = [current_perimeter]

        left_perim: tuple[int, int] = (current_perimeter[0] - 1, current_perimeter[1])
        right_perim: tuple[int, int] = (current_perimeter[0] + 1, current_perimeter[1])
        up_perim: tuple[int, int] = (current_perimeter[0], current_perimeter[1] - 1)
        down_perim: tuple[int, int] = (current_perimeter[0], current_perimeter[1] + 1)

        if (left_perim in perimeters) or (right_perim in perimeters):
            while left_perim in perimeters:
                perimeters.remove(left_perim)
                removed.append(left_perim)
                left_perim = (left_perim[0] - 1, left_perim[1])

            while right_perim in perimeters:
                perimeters.remove(right_perim)
                removed.append(right_perim)
                right_perim = (right_perim[0] + 1, right_perim[1])
        elif (up_perim in perimeters) or (down_perim in perimeters):
            while up_perim in perimeters:
                perimeters.remove(up_perim)
                removed.append(up_perim)
                up_perim = (up_perim[0], up_perim[1] - 1)

            while down_perim in perimeters:
                perimeters.remove(down_perim)
                removed.append(down_perim)
                down_perim = (down_perim[0], down_perim[1] + 1)

    if sides == 79:
        pass
    return sides



def day12(path: str = "data/day12.txt"):
    garden_map: list[str] = read_to_array(path)

    plots: set = set()
    neighbour_type: dict[tuple[int, int], str] = {}
    regions: list[set[tuple[int, int, str]]] = []

    for y, row in enumerate(garden_map):
        for x, type in enumerate(row):
            if type == ".":
                continue
            neighbour_type[(x, y)] = type
            plots.add((x, y, type))

    while len(plots) > 0:
        current_plot: tuple[int, int, str] = plots.pop()
        current_region: set[tuple[int, int, str]] = get_region(current_plot, set(), plots)
        regions.append(current_region)

    regions_area_sides_perimeter: list[tuple[int, int, int]] = []
    for region in regions:
        area: int = 0
        perimeter: int = 0
        perimeter_points: list[tuple[int, int]] = []
        for plot in region:
            type: str = plot[2]
            area += 1

            left_plot: tuple[int, int] = (plot[0] - 1, plot[1])
            right_plot: tuple[int, int] = (plot[0] + 1, plot[1])
            up_plot: tuple[int, int] = (plot[0], plot[1] - 1)
            down_plot: tuple[int, int] = (plot[0], plot[1] + 1)

            neighbour_plots: list[tuple[int, int]] = [(left_plot), right_plot, up_plot, down_plot]

            for n_plot in neighbour_plots:
                if n_plot not in neighbour_type:
                    perimeter += 1
                    perimeter_points.append(n_plot)
                elif neighbour_type[n_plot] != type:
                    perimeter += 1
                    perimeter_points.append(n_plot)

        stranger_sides: int = get_sides_from_stranger(([(r[1], r[0]) for r in region]))
        sides: int = get_sides(perimeter_points)
        assert sides == stranger_sides
        regions_area_sides_perimeter.append((area, perimeter, sides))

    print(sum([area * perimeter for area, perimeter, _ in regions_area_sides_perimeter]))
    print(sum([area * sides for area, _, sides in regions_area_sides_perimeter]))


if __name__ == "__main__":
    # print("Test")
    # day12("test/day12.txt")
    # print("Problem")
    # # day12("data/day12.txt")
    # day12("test/day12debug.txt")

    bad_input: list[tuple[int, int]] = [(97, 91), (97, 93), (89, 97), (99, 102), (96, 87), (95, 88), (88, 100), (91, 86), (90, 85), (98, 105), (97, 106), (93, 107), (92, 108), (86, 95), (92, 96), (91, 97), (88, 100), (88, 102), (96, 89), (95, 88), (84, 89), (86, 83), (96, 93), (95, 94), (84, 91), (93, 98), (95, 98), (94, 97), (89, 105), (90, 106), (98, 91), (98, 93), (91, 86), (88, 85), (94, 94), (88, 103), (89, 104), (93, 94), (92, 98), (97, 100), (95, 106), (94, 107), (84, 85), (97, 91), (96, 90), (92, 105), (85, 93), (86, 94), (88, 86), (89, 85), (88, 86), (99, 101), (98, 100), (88, 99), (89, 98), (86, 94), (93, 107), (95, 106), (99, 104), (98, 105), (89, 97), (91, 97), (90, 107), (91, 108), (94, 85), (93, 84), (88, 97), (84, 84), (85, 83), (92, 95), (96, 99), (95, 98), (92, 105), (96, 106), (89, 98), (91, 98), (92, 105), (96, 90), (84, 90), (85, 96), (86, 95), (86, 97), (94, 85), (97, 100), (96, 99), (93, 98), (89, 104), (91, 98), (84, 92), (85, 93), (95, 88), (93, 94), (92, 95), (88, 102), (83, 86), (84, 85), (86, 97), (88, 97), (87, 98), (88, 86), (91, 86), (91, 85), (92, 84), (88, 84), (87, 83), (92, 105), (96, 93), (86, 101), (87, 100), (87, 102), (100, 103), (99, 102), (99, 104), (100, 92), (99, 91), (99, 93), (83, 87), (84, 88), (90, 106), (96, 86), (95, 85), (84, 88)]
    sides: int = get_sides(bad_input)
    pass
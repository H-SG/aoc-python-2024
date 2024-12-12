from utils import read_to_array

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


def get_num_uncontiguous_sides(sides: set[tuple[int, int]], type: str) -> int:
    sides_count: int = 0
    while len(sides) > 0:
        current_side: tuple[int, int] = sides.pop()
        sides_count += 1

        match type:
            case "vert":
                up_neighbour: tuple[int, int] = (current_side[0], current_side[1] - 1)
                down_neighbour: tuple[int, int] = (current_side[0], current_side[1] + 1)

                while up_neighbour in sides:
                    sides.remove(up_neighbour)
                    up_neighbour = (up_neighbour[0], up_neighbour[1] - 1)

                while down_neighbour in sides:
                    sides.remove(down_neighbour)
                    down_neighbour = (down_neighbour[0], down_neighbour[1] + 1)
            case "hor":
                left_neighbour: tuple[int, int] = (current_side[0] - 1, current_side[1])
                right_neighbour: tuple[int, int] = (current_side[0] + 1, current_side[1])

                while left_neighbour in sides:
                    sides.remove(left_neighbour)
                    left_neighbour = (left_neighbour[0] - 1, right_neighbour[1])
                while right_neighbour in sides:
                    sides.remove(right_neighbour)
                    right_neighbour = (right_neighbour[0] + 1, right_neighbour[1])

    return sides_count


def get_num_sides(region: set[tuple[int, int]]) -> int:
    left_sides: set[tuple[int, int]] = set()
    right_sides: set[tuple[int, int]] = set()
    top_sides: set[tuple[int, int]] = set()
    bottom_sides: set[tuple[int, int]] = set()
    
    for plot in region:
        left: tuple[int, int] = (plot[0] - 1, plot[1])
        right: tuple[int, int] = (plot[0] + 1, plot[1])
        top: tuple[int, int] = (plot[0], plot[1] - 1)
        bottom: tuple[int, int] = (plot[0], plot[1] + 1)

        if top not in region:
            top_sides.add(top)

        if left not in region:
            left_sides.add(left)

        if right not in region:
            right_sides.add(right)

        if bottom not in region:
            bottom_sides.add(bottom)

    return get_num_uncontiguous_sides(left_sides, "vert") + get_num_uncontiguous_sides(right_sides, "vert") + get_num_uncontiguous_sides(top_sides, "hor") + get_num_uncontiguous_sides(bottom_sides, "hor")


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
        for plot in region:
            type: str = plot[2]
            area += 1

            left_plot: tuple[int, int] = (plot[0] - 1, plot[1])
            right_plot: tuple[int, int] = (plot[0] + 1, plot[1])
            up_plot: tuple[int, int] = (plot[0], plot[1] - 1)
            down_plot: tuple[int, int] = (plot[0], plot[1] + 1)
            
            for n_plot in [left_plot, right_plot, up_plot, down_plot]:
                if n_plot not in neighbour_type:
                    perimeter += 1
                    continue
                    
                if neighbour_type[n_plot] != type:
                    perimeter += 1
                    continue

        # print_region(region)
        sides: int = get_num_sides(set([(r[0], r[1]) for r in region]))
        regions_area_sides_perimeter.append((area, perimeter, sides))

    print(f"Day 12 - Part 1: {sum([area * perimeter for area, perimeter, _ in regions_area_sides_perimeter])}")
    print(f"Day 12 - Part 2: {sum([area * sides for area, _, sides in regions_area_sides_perimeter])}")


if __name__ == "__main__":
    print("Test")
    day12("test/day12.txt")
    print("Problem")
    day12("data/day12.txt")
    # day12("test/day12debug.txt")
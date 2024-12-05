from utils import read_to_array
import re

def rotate_string_list(input: list[str]) -> list[str]:
    output: list[str] = []

    columns: int = len(input[0])

    for c in range(columns):
        new_row: str = "".join([r[c] for r in input])[::-1]
        output.append(new_row)

    return output

def get_sub_block(input: list[str], x_r: list[int], y_r:list[int]) -> list[str]:
    output: list[str] = []

    for y in y_r:
        row: str = input[y][x_r[0]:x_r[-1] + 1]
        output.append(row)

    return output


def rotate_string_list_45(input: list[str]) -> list[str]:
    rows: int = len(input)
    l_append: int = rows * 2

    output: list[str] = ["" for r in range((rows * 2) -1)]

    x: int = 0
    y: int = 0
    reduce_l_adjust: bool = True
    for i, d in enumerate(input):
        y = i
        i_inv: int = (-1) - i
        y_inv = i_inv

        while y >= 0:
            x = i - y
            x_inv = (i_inv - 1) - y_inv
            output[i] += input[y][x]
            if i < len(input) - 1:
                output[i_inv] += input[y_inv][x_inv]

            y -= 1
            y_inv += 1

        if i < len(input) - 1:
            output[i_inv] = output[i_inv][::-1]
            

        if l_append == 0:
            reduce_l_adjust = False

        if reduce_l_adjust:
            l_append -= 1
        else:
            l_append += 1

    return output


def day04(path: str = "data/day04.txt"):
    data: list[str] = read_to_array(path)

    xmas_re: re.Pattern = re.compile(r'(XMAS)')
    samx_re: re.Pattern = re.compile(r'(SAMX)')

    mas_re: re.Pattern = re.compile(r'(MAS)')
    sam_re: re.Pattern = re.compile(r'(SAM)')

    sum_p1: int = 0

    # up and down case
    # rotate the list 90 deg
    data90: list[str] = rotate_string_list(data) 
    data45l: list[str] = rotate_string_list_45(data)
    data45r: list[str] = rotate_string_list_45(data90)

    for n, r,in zip(data, data90):
        sum_p1 += len(xmas_re.findall(n))
        sum_p1 += len(samx_re.findall(n))
        sum_p1 += len(xmas_re.findall(r))
        sum_p1 += len(samx_re.findall(r))

    for l45, r45 in zip(data45l, data45r):
        sum_p1 += len(xmas_re.findall(l45))
        sum_p1 += len(samx_re.findall(l45))
        sum_p1 += len(xmas_re.findall(r45))
        sum_p1 += len(samx_re.findall(r45))

    print(f"Day 4 - Part 1: {sum_p1}")

    sum_p2: int = 0

    for x in range(len(data)):
        x_r = [x + i for i in range(3)]
        if x_r[-1] == len(data):
            break

        for y in range(len(data)):
            y_r = [y + i for i in range(3)]
            if y_r[-1] == len(data):
                break

            block = get_sub_block(data, x_r, y_r)

            blockl45 = rotate_string_list_45(block)
            blockr45 = rotate_string_list_45(rotate_string_list(block))

            l_match = len(mas_re.findall(blockl45[2])) + len(sam_re.findall(blockl45[2]))
            r_match = len(mas_re.findall(blockr45[2])) + len(sam_re.findall(blockr45[2]))

            if l_match + r_match == 2:
                sum_p2 += 1

    print(f"Day 4 - Part 2: {sum_p2}")

        


if __name__ == "__main__":
    print("Test")
    day04("test/day04.txt")
    print("Problem")
    day04("data/day04.txt")
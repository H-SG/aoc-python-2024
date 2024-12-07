from utils import read_to_array

def is_equation_valid(current_total: int, r_operands: list[int], part_2: bool = False) -> bool:
    if len(r_operands) == 0:
        return False
    
    first_operand: int = r_operands[0]
    remaining_operands: list[int] = r_operands[1:]

    if len(r_operands) == 1:
        if first_operand == current_total:
            return True

    if current_total < first_operand:
        return False
    
    operation_results: list[bool] = []
    
    operation_results.append(is_equation_valid(current_total - first_operand, remaining_operands, part_2))

    if (current_total / first_operand) == (current_total // first_operand):
        operation_results.append(is_equation_valid(current_total // first_operand, remaining_operands, part_2))

    if part_2:
        if len(str(current_total)) != len(str(first_operand)):
            if int(str(current_total)[-len(str(first_operand)):]) == first_operand:
                operation_results.append(is_equation_valid(int(str(current_total)[:-len(str(first_operand))]), remaining_operands, part_2))

    return any(operation_results)

def day07(path: str = "data/day07.txt"):
    calibrations: list[str] = read_to_array(path)

    sum_p1: int = 0
    sum_p2: int = 0
    for calibration in calibrations:
        total: int = int(calibration.split(":")[0].strip())
        numbers: list[int] = [int(x.strip()) for x in calibration.split(":")[-1].split(" ") if x != ""]
        numbers.reverse()

        if is_equation_valid(total,  numbers):
            sum_p1 += total
            sum_p2 += total
        else:
            if is_equation_valid(total, numbers, part_2=True):
                sum_p2 += total

    print(f"Day 7 - Part 1: {sum_p1}")
    print(f"Day 7 - Part 2: {sum_p2}")



if __name__ == "__main__":
    print("Test")
    day07("test/day07.txt")
    print("Problem")
    day07("data/day07.txt")
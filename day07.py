from utils import read_to_array
from itertools import product

def value_of_equation(line: str) -> int:
    total: int = int(line.split(":")[0].strip())
    numbers: list[int] = [int(x.strip()) for x in line.split(":")[-1].split(" ") if x != ""]

    operators: product = product(["*", "+"], repeat=len(numbers))

    for operator_set in operators:
        sum: int = numbers[0]
        for operator, number in zip(operator_set, numbers[1:]):
            match operator:
                case "*":
                    sum *= number
                case "+":
                    sum += number

            if sum > total:
                break

        if sum == total:
            return total
        
    return 0

def value_of_equation_part_2(line: str) -> int:
    total: int = int(line.split(":")[0].strip())
    numbers: list[int] = [int(x.strip()) for x in line.split(":")[-1].split(" ") if x != ""]

    operators: product = product(["*", "+", "||"], repeat=len(numbers))

    for operator_set in operators:
        if "||" not in operator_set:
            continue
        sum: int = numbers[0]
        for operator, number in zip(operator_set, numbers[1:]):
            match operator:
                case "*":
                    sum *= number
                case "+":
                    sum += number
                case "||":
                    sum = int(f"{sum}{number}")

            if sum > total:
                break

        if sum == total:
            return total
        
    return 0

def day07(path: str = "data/day07.txt"):
    calibrations: list[str] = read_to_array(path)

    sum_p1: int = 0
    sum_p2: int = 0
    for calibration in calibrations:
        p1 = value_of_equation(calibration)
        sum_p1 += p1
        if p1 == 0:
            sum_p2 += value_of_equation_part_2(calibration)
        else:
            sum_p2 += p1

    print(sum_p1)
    print(sum_p2)



if __name__ == "__main__":
    print("Test")
    day07("test/day07.txt")
    print("Problem")
    day07("data/day07.txt")
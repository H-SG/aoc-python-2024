from utils import read_to_array

def is_valid_num_presses(presses: int | float, max_presses: int, part_2: bool = False) -> bool:
    if presses < 0:
        return False
    
    if int(presses) != presses:
        return False
    
    if not part_2:
        if presses > max_presses:
            return False
    
    return True


class EqPair():
    a_presses: int
    b_presses: int

    def __init__(self, ruleset: list[str], max_press_per_button: int = 100,  part_2: bool = False):
        a1: int = 0
        b1: int = 0
        a2: int = 0
        b2: int = 0
        s1: int = 0
        s2: int = 0

        self.a_presses = 0
        self.b_presses = 0

        for i, rule in enumerate(ruleset):
            match i:
                case 0:
                    a1_str = rule.split(" ")[2]
                    b1_str = rule.split(" ")[3]
                    a1 = int(a1_str[1:-1])
                    a2 = int(b1_str[1:])

                    if "-" in a1_str:
                        a1 *= -1

                    if "-" in b1_str:
                        a2 *= -1
                case 1:
                    a2_str = rule.split(" ")[2]
                    b2_str = rule.split(" ")[3]
                    b1 = int(a2_str[1:-1])
                    b2 = int(b2_str[1:])

                    if "-" in a2_str:
                        b1 *= -1

                    if "-" in b2_str:
                        b2 *= -1
                case 2:
                    s1_str = rule.split(" ")[1]
                    s2_str = rule.split(" ")[2]

                    s1 = int(s1_str[2:-1])
                    s2 = int(s2_str[2:])
                    if part_2:

                        s1 += 10000000000000
                        s2 += 10000000000000

        b: float = ((s1*a2)-(s2*a1))/((b1*a2)-(b2*a1))

        if is_valid_num_presses(b, max_press_per_button, part_2):
            a: float = (s1 -(b1*b))/a1
            if is_valid_num_presses(a, max_press_per_button, part_2):
                self.a_presses = int(a)
                self.b_presses = int(b)

    def get_cost(self) -> int:
        return (self.a_presses * 3) + (self.b_presses)


def day13(path: str = "data/day13.txt"):
    claw_machine_options: list[str] = read_to_array(path)

    sum_p1: int = 0
    sum_p2: int = 0
    for i in range(0, len(claw_machine_options), 4):
        ruleset: list[str] = claw_machine_options[i:i+3]
        eq1 = EqPair(ruleset)
        eq2 = EqPair(ruleset, part_2=True)

        sum_p1 += eq1.get_cost()
        sum_p2 += eq2.get_cost()

    print(f"Day 13 - Part 1: {sum_p1}")
    print(f"Day 13 - Part 2: {sum_p2}")


if __name__ == "__main__":
    print("Test")
    day13("test/day13.txt")
    print("Problem")
    day13("data/day13.txt")
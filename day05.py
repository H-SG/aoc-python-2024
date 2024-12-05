from utils import read_to_array

def is_update_valid(update: list[int], forward_dict: dict[int, set[int]], backward_dict: dict[int, set[int]]) -> bool:
    for i, page in enumerate(update):
        pre_pages: None | set[int] = backward_dict.get(page, None)
        post_pages: None | set[int] = forward_dict.get(page, None)

        if (pre_pages is None) and (post_pages is None):
            continue

        pre_set: set[int] = set(update[:i])
        post_set: set[int] = set(update[i + 1:])

        if post_pages is not None:
            if len(pre_set.intersection(post_pages)) > 0:
                return False
            
        if pre_pages is not None:
            if len(post_set.intersection(pre_pages)) > 0:
                return False

    return True

def get_valid_update(update: list[int], forward_dict: dict[int, set[int]], backward_dict: dict[int, set[int]]) -> tuple[bool, list[int]]:
    current_update: list[int] = [x for x in update]
    for i, page in enumerate(update):
        pre_pages: None | set[int] = backward_dict.get(page, None)
        post_pages: None | set[int] = forward_dict.get(page, None)

        if (pre_pages is None) and (post_pages is None):
            continue

        pre_set: set[int] = set(current_update[:i])
        post_set: set[int] = set(current_update[i + 1:])

        if post_pages is not None:
            must_be_left_of: set[int] = pre_set.intersection(post_pages)
            mindex: int = len(update)

            if len(must_be_left_of) > 0:
                for mblo in must_be_left_of:
                    mindex = min(mindex, update.index(mblo))
                current_update.remove(page)
                current_update.insert(mindex, page)
                return get_valid_update(current_update, forward_dict, backward_dict)
                
        if pre_pages is not None:
            must_be_right_of: set[int] = post_set.intersection(pre_pages)
            maxdex: int = 0
            
            if len(must_be_right_of) > 0:
                for mbro in must_be_right_of:
                    maxdex = max(maxdex, update.index(mbro))
                current_update.remove(page)
                current_update.insert(maxdex, page)
                return get_valid_update(current_update, forward_dict, backward_dict)

    return True, update


def day05(path: str = "data/day05.txt"):
    data: list[str] = read_to_array(path)

    forward_dict: dict[int, set[int]] = {}
    backward_dict: dict[int, set[int]] = {}
    updates: list[list[int]] = []

    sum_p1: int = 0
    sum_p2: int = 0

    for d in data:
        if "|" in d:
            x: int
            y: int

            x, y = [int(x.strip()) for x in d.split("|")]

            if x not in forward_dict:
                forward_dict[x] = set()

            if y not in backward_dict:
                backward_dict[y] = set()

            forward_dict[x].add(y)
            backward_dict[y].add(x)

            continue

        if "," in d:
            updates.append([int(x.strip()) for x in d.split(",")])

    for update in updates:
        if is_update_valid(update, forward_dict, backward_dict):
            sum_p1 += update[len(update) // 2]
        else:
            valid: bool
            valid_update: list[int]
            valid, valid_update = get_valid_update(update, forward_dict, backward_dict)
            if valid:
                sum_p2 += valid_update[len(valid_update) // 2]


    print(f"Day 5 - Part 1: {sum_p1}")
    print(f"Day 5 - Part 2: {sum_p2}")
            
if __name__ == "__main__":
    print("Test")
    day05("test/day05.txt")
    print("Problem")
    day05("data/day05.txt")
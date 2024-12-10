from utils import read_to_array

class File():
    size: int
    id: int
    pos: int

    def __init__(self, size: int, pos: int, id: int):
        self.size = size
        self.id = id
        self.pos = pos

    def get_checksum(self) -> int:
        checksum: int = 0
        for i in range(self.size):
            checksum += self.id * (self.pos + i)

        return checksum

class FreeSpace():
    size: int
    pos: int

    def __init__(self, size: int, pos: int):
        self.size = size
        self.pos = pos


def day09(path: str = "data/day09.txt"):
    disk_map: str = read_to_array(path)[0]

    files: list[File] = []
    free_spaces: list[FreeSpace] = []
    file_blocks: list[list[int]] = []
    free_space_indices: list[int] = []
    id: int = 0
    curr_pos: int = 0
    for i in range(0, len(disk_map), 2):
        file_size: int = int(disk_map[i])
        free_space_size: int
        if i + 1 >= len(disk_map):
            free_space_size = 0
        else:
            free_space_size = int(disk_map[i + 1])

        for f_i in range(file_size):
            file_blocks.append([curr_pos + f_i, id])

        files.append(File(
            file_size,
            curr_pos,
            id,
        ))

        id += 1
        curr_pos += file_size

        free_spaces.append(FreeSpace(
            free_space_size,
            curr_pos
        ))

        for s_i in range(free_space_size):
            free_space_indices.append(curr_pos + s_i)

        curr_pos += free_space_size

    file_blocks.reverse()
    for file_block, free_space_index in zip(file_blocks, free_space_indices):
        if file_block[0] > free_space_index:
            file_block[0] = free_space_index
            continue

    
    checksum: int = sum([x * y for x, y in file_blocks])

    files.reverse()

    checksum_p2: int = 0
    for file in files:
        for s_i, free_space in enumerate(free_spaces):
            if free_space.pos > file.pos:
                continue

            if file.size > free_space.size:
                continue

            if file.size == free_space.size:
                file.pos = free_space.pos
                free_spaces.pop(s_i)

                break

            if file.size < free_space.size:
                file.pos = free_space.pos
                new_free_space: FreeSpace = FreeSpace(
                    free_space.size - file.size,
                    free_space.pos + file.size
                )

                free_spaces.pop(s_i)
                free_spaces.insert(s_i, new_free_space)
                break

        checksum_p2 += file.get_checksum()

    
    print(f"Day 9 - Part 1: {checksum}")
    print(f"Day 9 - Part 2: {checksum_p2}")


if __name__ == "__main__":
    print("Test")
    day09("test/day09.txt")
    print("Problem")
    day09("data/day09.txt")
"""
Board module
Author: David Oniani
License: MIT
"""


class Board(list):
    """
    This class implements a galton board
    for particles.
    """
    def __init__(self, size: int) -> None:
        self._size = size
        self._slots = [0] * size
        self._levels_number = size // 2

    def get_size(self) -> int:
        return self._size

    def set_size(self, new_size: int) -> None:
        self._size = [0] * new_size

    size = property(get_size, set_size)

    def get_levels_number(self) -> int:
        return self._levels_number

    def set_levels_number(self, new_levels_number: int) -> None:
        self.levels_number = new_levels_number

    levels_number = property(get_levels_number, set_levels_number)

    def get_slots(self) -> list:
        return self._slots

    def set_slots(self, new_slots: list) -> None:
        self._slots = new_slots

    slots = property(get_slots, set_slots)

    def __getitem__(self, index: int) -> int:
        return self._slots[index]

    def __setitem__(self, index: int, new_value: int) -> None:
        self._slots[index] = new_value

    def __str__(self) -> None:
        result = "\033[41m|\033[0m"
        for slot in self._slots:
            result += f" \033[34m{slot} \033[41m|\033[0m"
        return result
    
    @property
    def number_of_particles(self) -> int:
        return sum(self._slots)

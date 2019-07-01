"""
Board module

Author: David Oniani
Date: 04/05/2019
License: GNU General Public License v3.0
"""


class Board(list):
    """
    This class implements a galton board
    for particles.
    """

    def __init__(self, size: int) -> None:
        self._size = size
        self._slots = [0] * size
        self._levels = size // 2

    def get_size(self) -> int:
        return self._size

    def set_size(self, new_size: int) -> None:
        self._size = [0] * new_size

    size = property(get_size, set_size)

    def get_levels(self) -> int:
        return self._levels

    def set_levels(self, new_levels: int) -> None:
        self._levels = new_levels

    levels = property(get_levels, set_levels)

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

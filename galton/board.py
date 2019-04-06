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
    def __init__(self, slots_number: int) -> None:
        self._slots_number = slots_number
        self._slots = [0] * slots_number
        self._levels_number = slots_number // 2
        self._particles_number = sum(self._slots)

    def get_slots_number(self) -> int:
        return self._slots_number

    def set_slots_number(self, new_slots_number: int) -> None:
        self._slots_number = [0] * new_slots_number

    slots_number = property(get_slots_number, set_slots_number)

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

    def get_particles_number(self) -> int:
        return self._particles_number

    def set_particles_number(self, new_particles_number: int) -> None:
        self._particles_number = new_particles_number

    particles_number = property(get_particles_number, set_particles_number)

    def __getitem__(self, index: int) -> int:
        return self._slots[index]

    def __setitem__(self, index: int, new_value: int) -> None:
        self._slots[index] = new_value
        self._particles_number = sum(self._slots)

    def __str__(self) -> None:
        return str(self._slots)

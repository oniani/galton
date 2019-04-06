"""
Particle module
Author: David Oniani
License: MIT
"""


import time
import random
import threading
from galton.board import Board


class Particle(threading.Thread):
    """
    This class implements a particle thread that operates
    on the board with the given number of slots and levels.
    """
    def __init__(self, name: str, position: int, board: Board):
        threading.Thread.__init__(self, target=self.run)
        self._name = name
        self._position = position
        self._board = board

    def get_name(self):
        """Get the name of the particle."""
        return self._name

    def set_name(self, new_name: str):
        """Set the name of the particle."""
        self.name = new_name

    name = property(get_name, set_name)

    def get_position(self) -> int:
        """Get the current position of the particle."""
        return self._position

    def set_position(self, new_position: int) -> None:
        """Set the current position of the particle."""
        self._position = new_position

    position = property(get_position, set_position)

    def move_left(self) -> None:
        """
        Move one place to the left if the particle
        is not at the leftmost cell. Move to the
        right if the particle is at the leftmost cell.
        """
        if self._position == 0:
            self._position = 1
        else:
            self._position -= 1

    def move_right(self) -> None:
        """
        Move one place to the right if the particle
        is not at the rightmost cell. Move to the
        left if the particle is at the rightmost cell.
        """
        if self._position == self._board.slots_number - 1:
            self._position = self._board._slots_number - 2
        else:
            self._position += 1

    def in_between(self) -> None:
        """
        Notice that in Galton board, there is a case
        when the particle position is in-between the cells.
        This is obviously not convenient for us since in
        the end, every particle must have some cell to reside.
        Because of this, we skip every other level starting
        with the level 0. Notice that, in this case, we will
        always have a third case in which the particle
        position has not changed. Look at the level 0 and level 1.
        It is easy to see that there is a case where the particle
        has not changed its location. It seems like we are jumping
        from level 0 to level 1, but in reality, we are accounting
        for this by having a third move option which is "stay in
        the same position" or "not move". Once again, look at level
        0 and level 1 where the particle does not change its position.
        This is due to the fact that on the level in-between level 0
        and level 1 the particle could have gone back to its initial
        position.


        0                         *
                                *   *
        1                     *   *   *
                            *   *   *   *
        3                 *   *   *   *   *
                        *   *   *   *   *   *
        4             *   *   *   *   *   *   *
                    *   *   *   *   *   *   *   *
        5         *   *   *   *   *   *   *   *   *
                *   *   *   *   *   *   *   *   *   *
            |___|___|___|___|___|___|___|___|___|___|___|

        In this case, the particle does not really move
        neither to the left, nor to the right. We could
        update our position by adding or subtracting 0.5,
        but for simplicity and convenience, it's the best
        to simply not change the position of the particle.
        """
        pass

    def move_random(self) -> None:
        """
        Make a random move either to the left, to the right,
        or stay at the same position.
        """
        direction = random.choices(['move_left', 'move_right', 'in_between'],
                                   weights=[0.25, 0.25, 0.5],
                                   k=1)[0]

        if direction == 'move_left':
            self.move_left()
        elif direction == 'move_right':
            self.move_right()
        else:
            self.in_between()

    def run(self) -> None:
        """
        This method has to be overriden as indicated in
        the documentation of the threading module.
        """
        for _ in range(self._board.levels_number):
            self.move_random()
            time.sleep(0.00025)

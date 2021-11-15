import random
import threading

from .board import Board


class Particle(threading.Thread):
    """Implements a particle thread that operates on the board."""

    def __init__(self, board: Board, name: str, position: int) -> None:
        """Initializes a particle thread with the given board, name, and position."""

        super().__init__(target=self.run)

        self.board: Board = board
        self.name: str = name
        self.position: int = position

    def move_left(self) -> None:
        """Moves one place to the left if the particle is not at the leftmost cell.

        Move one place to the left if the particle is not at the leftmost cell. Move to the right if
        the particle is at the leftmost cell.

        NOTE: `move_left` uses a lock to do the move. Useful for logging intermediate results.
        """

        with threading.Lock():
            self.board[self.position] -= 1

            if self.position == 0:
                self.position = 1
            else:
                self.position -= 1

            self.board[self.position] += 1

    def move_right(self) -> None:
        """Moves one place to the right if the particle is not at the rightmost cell.

        Move one place to the right if the particle is not at the rightmost cell. Move to the left
        if the particle is at the rightmost cell.

        NOTE: `move_right` uses a lock to do the move. Useful for logging intermediate results.
        """

        with threading.Lock():
            self.board[self.position] -= 1

            if self.position == self.board.size - 1:
                self.position = self.board.size - 2
            else:
                self.position += 1

            self.board[self.position] += 1

    def in_between(self) -> None:
        """Does nothing.

        Notice that in Galton board, there is a case when the particle position is in-between the
        cells. This is obviously not convenient for us since in the end, every particle must have
        some cell to reside. Because of this, we skip every other level starting with the level 0.
        Notice that, in this case, we will always have a third case in which the particle position
        has not changed. Look at the level 0 and level 1. It is easy to see that there is a case
        where the particle has not changed its location. It seems like we are jumping from level 0
        to level 1, but in reality, we are accounting for this by having a third move option which
        is "stay in the same position" or "not move". Once again, look at level 0 and level 1 where
        the particle does not change its position. This is due to the fact that on the level
        in-between level 0 and level 1 the particle could have gone back to its initial position.


        # 0                         *
        #                         *   *
        # 1                     *   *   *
        #                     *   *   *   *
        # 3                 *   *   *   *   *
        #                 *   *   *   *   *   *
        # 4             *   *   *   *   *   *   *
        #             *   *   *   *   *   *   *   *
        # 5         *   *   *   *   *   *   *   *   *
        #         *   *   *   *   *   *   *   *   *   *
        #     |___|___|___|___|___|___|___|___|___|___|___|

        In this case, the particle does not really move neither to the left, nor to the right. We
        could update our position by adding or subtracting 0.5, but for convenience and simplicity,
        it's the best to simply not change the position of the particle.
        """

        pass

    def move_random(self) -> None:
        """Performs a random move.

        Make a random move either to the left, to the right, or stay at the same position. Note that
        the randomization has weights. This is due to how the probabilities will be arranged. We
        have 1/4 of the probability that the particle will end up on the left peg, 0.25 that it will
        end up on the right peg, and 1/4 + 1/4 = 0.5 probability that it will end up not moving
        horizontally. Notice that even though the particle does not move horizontally, it obviously
        does move vertically as it goes down the levels of pegs.
        """

        direction = random.choices(["left", "right", "inb"], weights=[0.25, 0.25, 0.5], k=1)[0]

        if direction == "left":
            self.move_left()
        elif direction == "right":
            self.move_right()
        else:
            self.in_between()

    def run(self) -> None:
        """Overrides the method as indicated in the documentation of the threading module."""

        for _ in range(self.board.levels):
            self.move_random()

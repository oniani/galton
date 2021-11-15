class Board:
    """Implements a Galton board containing particles."""

    def __init__(self, size: int) -> None:
        """Initializes the board with the given size."""

        self.size: int = size
        self.slots: list[int] = [0] * size
        self.levels: int = size // 2

    def __getitem__(self, idx: int) -> int:
        """Gets a slot from the board."""

        return self.slots[idx]

    def __setitem__(self, idx: int, val: int) -> None:
        """Sets a slot on the board."""

        self.slots[idx] = val

    def __str__(self) -> str:
        """Implements a custom string representation for the board."""

        purple: str = "\033[95m"
        result: list[str] = [f"{purple}|"]
        for slot in self.slots:
            result.append(f" {purple}{slot} {purple}|")
        result.append("\033[0m")
        return "".join(result)

    @property
    def particles(self) -> int:
        """Gets the number of particles on the board."""

        return sum(self.slots)

from enum import Enum
from .constants import BOARD_SIZE, COLUMN_LABELS, ROW_LABELS, OutOfBoundsError


class Color(Enum):
    BLACK = 0
    WHITE = 1

    def __str__(self) -> str:
        return str(self.name.lower())


class BoardCoordinates:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    @classmethod
    def from_algebra_notation(cls, col: str, row: int):
        parsed_row = 8 - row
        parsed_column = COLUMN_LABELS.index(col)

        return cls(parsed_row, parsed_column)

    def __str__(self):
        return self.letter_notation()

    def __eq__(self, other) -> bool:
        if not isinstance(other, BoardCoordinates):
            raise TypeError("BoardCoordinates can only be compared to BoardCoordinates")

        return self.col == other.col and self.row == other.row

    def is_in_bounds(self) -> bool:
        return 0 <= self.row < BOARD_SIZE and 0 <= self.col < BOARD_SIZE

    def letter_notation(self) -> str:
        if not self.is_in_bounds():
            raise OutOfBoundsError

        return f"{COLUMN_LABELS[self.col]}{ROW_LABELS[self.row]}"


def parse_letter_coordinates(value: str) -> BoardCoordinates:
    col = COLUMN_LABELS.index(value[0])
    row = ROW_LABELS.index(int(value[1]))

    return BoardCoordinates(row, col)

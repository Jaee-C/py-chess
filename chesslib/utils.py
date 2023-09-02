from .constants import BOARD_SIZE, COLUMN_LABELS, ROW_LABELS, OutOfBoundsError


class BoardCoordinates:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def is_in_bounds(self) -> bool:
        return 0 < self.row <= BOARD_SIZE and 0 < self.col <= BOARD_SIZE

    def letter_notation(self) -> str:
        if not self.is_in_bounds():
            raise OutOfBoundsError

        return f"{COLUMN_LABELS[self.col - 1]}{ROW_LABELS[self.row - 1]}"


def parse_letter_coordinates(value: str) -> BoardCoordinates:
    col = COLUMN_LABELS.index(value[0]) + 1
    row = ROW_LABELS.index(value[1]) + 1

    return BoardCoordinates(row, col)

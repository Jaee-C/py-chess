from chesslib.utils import Color, BoardCoordinates, ChessMove
from chesslib.constants import BOARD_SIZE
from .piece import Piece


class Bishop(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self.abbreviation = "B"

    def possible_moves(self, position: BoardCoordinates) -> list[ChessMove]:
        return super().diagonal_moves(position, BOARD_SIZE)


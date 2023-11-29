from chesslib.utils import Color, BoardCoordinates, ChessMove
from .piece import Piece


class King(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self.abbreviation = "K"

    def possible_moves(self, position: BoardCoordinates) -> list[ChessMove]:
        return super().orthogonal_moves(position, 1) + super().diagonal_moves(position, 1)

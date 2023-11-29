from chesslib.utils import Color, BoardCoordinates
from ..chess_move import MoveType, ChessMove
from chesslib.constants import InvalidPiece
from .piece import Piece


class Knight(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self.abbreviation = "N"

    def possible_moves(self, position: BoardCoordinates) -> list[ChessMove]:
        MOVES = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))

        piece = self.board.get_piece_at(position)
        if piece is None:
            raise InvalidPiece

        legal_moves = []
        for x, y in MOVES:
            destination = BoardCoordinates(position.row + y, position.col + x)
            if destination.is_in_bounds() and destination not in self.board.occupied(piece.color):
                legal_moves.append(ChessMove(position, destination, MoveType.REGULAR))

        return legal_moves

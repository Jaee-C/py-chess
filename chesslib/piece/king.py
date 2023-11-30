from chesslib.utils import Color, BoardCoordinates
from chesslib.constants import BOARD_SIZE
from ..chess_move import ChessMove, MoveType
from .piece import Piece
from .rook import Rook

CASTLE_LEFT_ROW = 1
CASTLE_RIGHT_ROW = 6


class King(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self.abbreviation = "K"
        self.moved = False

    def possible_moves(self, position: BoardCoordinates) -> list[ChessMove]:
        legal_moves = super().orthogonal_moves(position, 1) + super().diagonal_moves(position, 1)

        if not self.moved:
            if self.can_castle_left(position):
                legal_moves.append(ChessMove(position, BoardCoordinates(position.row, CASTLE_LEFT_ROW), MoveType.CASTLING))

            if self.can_castle_right(position):
                legal_moves.append(ChessMove(position, BoardCoordinates(position.row, CASTLE_RIGHT_ROW), MoveType.CASTLING))

        return legal_moves

    def can_castle_left(self, position: BoardCoordinates) -> bool:
        rook = self.board.get_piece_at(BoardCoordinates(position.row, 0))

        if rook is not None and isinstance(rook, Rook) and not rook.moved:
            return True

        return False

    def can_castle_right(self, position: BoardCoordinates) -> bool:
        rook = self.board.get_piece_at(BoardCoordinates(position.row, BOARD_SIZE - 1))

        if rook is not None and isinstance(rook, Rook) and not rook.moved:
            return True

        return False

from chesslib.utils import Color, BoardCoordinates
from ..chess_move import MoveType, ChessMove
from .piece import Piece


class Pawn(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self.abbreviation = "P"
        self.first_move = False      # Used to check en passant

        if self.color == Color.WHITE:
            self.home_row = 6
            self.direction = -1
            self.enemy = Color.BLACK
        else:
            self.home_row = 1
            self.direction = 1
            self.enemy = Color.WHITE

    def possible_moves(self, position: BoardCoordinates) -> list[ChessMove]:
        legal_moves = []
        blocked = self.board.occupied(Color.WHITE) + self.board.occupied(Color.BLACK)
        forward = BoardCoordinates(position.row + self.direction, position.col)

        # Can we move forward?
        if forward.is_in_bounds() and forward not in blocked:
            legal_moves.append(ChessMove(position, forward, MoveType.REGULAR))
            if position.row == self.home_row:
                # If pawn in starting position we can do a double move
                double_forward = BoardCoordinates(forward.row + self.direction, forward.col)
                if double_forward.is_in_bounds() and double_forward not in blocked:
                    legal_moves.append(ChessMove(position, double_forward, MoveType.REGULAR))

        # Attacking [-1, 1]
        for a in range(-1, 2, 2):
            attack = BoardCoordinates(position.row + self.direction, position.col + a)
            if attack.is_in_bounds() and attack in self.board.occupied(self.enemy):
                legal_moves.append(ChessMove(position, attack, MoveType.REGULAR))
            elif attack.is_in_bounds() and self._can_en_passant(position, attack):
                legal_moves.append(ChessMove(position, attack, MoveType.EN_PASSANT))

        return legal_moves

    def pawn_is_moved(self, move: ChessMove):
        if move.type == MoveType.REGULAR and move.start.row == self.home_row:
            self.first_move = True
            return

        if self.first_move:
            self.first_move = False

    def _can_en_passant(self, start: BoardCoordinates, end: BoardCoordinates) -> bool:
        if not (start.row + self.direction == end.row or abs(start.col - end.col) == 1):
            return False

        if (not self.home_row + 3 * self.direction == start.row) or self.board.get_piece_at(end) is not None:
            return False

        target_location = BoardCoordinates(start.row, end.col)
        target_pawn = self.board.get_piece_at(target_location)

        if target_pawn is None or target_pawn.abbreviation != "P" or not target_pawn.first_move:
            return False

        return True

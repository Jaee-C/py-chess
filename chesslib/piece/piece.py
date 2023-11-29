from abc import ABC, abstractmethod

from chesslib.utils import BoardCoordinates, Color, ChessMove, MoveType


Direction = tuple[int, int]


class Piece(ABC):
    def __init__(self, color: Color):
        self.color = color
        self.board = None
        self.abbreviation = "None"

    @abstractmethod
    def possible_moves(self, position: BoardCoordinates) -> list[ChessMove]:
        pass

    def place(self, board):
        self.board = board

    def orthogonal_moves(self, position: BoardCoordinates, distance: int) -> list[ChessMove]:
        """Find all possible orthogonal moves from a position up to (and including) `distance` steps"""
        legal_moves = []
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))

        for d in directions:
            legal_moves += self._move_in_direction(position, d, distance)

        return legal_moves

    def diagonal_moves(self, position: BoardCoordinates, distance: int) -> list[ChessMove]:
        """Find all possible diagonal moves from a position up to (and including) `distance` steps"""
        legal_moves = []
        directions = ((1, 1), (-1, 1), (-1, -1), (1, -1))

        for d in directions:
            legal_moves += self._move_in_direction(position, d, distance)

        return legal_moves

    def _move_in_direction(self, position: BoardCoordinates, direction: Direction, distance: int) -> list[ChessMove]:
        collision = False
        moves: list[ChessMove] = []

        for i in range(1, distance+1):
            if collision:
                break

            upcoming = self._increment(position, direction, i)
            if not self._collision(upcoming):
                moves.append(ChessMove(position, upcoming, MoveType.REGULAR))
            elif not upcoming.is_in_bounds() or self._is_own_piece(upcoming):
                collision = True
            else:
                moves.append(ChessMove(position, upcoming, MoveType.REGULAR))
                collision = True

        return moves

    def _increment(self, position: BoardCoordinates, direction: Direction, distance: int) -> BoardCoordinates:
        return BoardCoordinates(position.row + direction[0] * distance, position.col + direction[1] * distance)

    def _collision(self, position: BoardCoordinates) -> bool:
        return not position.is_in_bounds() or self.board.get_piece_at(position) is not None

    def _is_own_piece(self, position: BoardCoordinates) -> bool:
        return self.board.get_piece_at(position) is not None and self.board.get_piece_at(position).color == self.color

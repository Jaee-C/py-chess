from abc import ABC, abstractmethod

from .utils import BoardCoordinates, Color
from .constants import InvalidPiece, BOARD_SIZE


Direction = tuple[int, int]


class Piece(ABC):
    def __init__(self, color: Color):
        self.color = color
        self.board = None
        self.abbreviation = "None"

    @abstractmethod
    def possible_moves(self, position: BoardCoordinates) -> list[BoardCoordinates]:
        pass

    def place(self, board):
        self.board = board

    def orthogonal_moves(self, position: BoardCoordinates, distance: int) -> list[BoardCoordinates]:
        """Find all possible orthogonal moves from a position up to (and including) `distance` steps"""
        legal_moves = []
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))

        for d in directions:
            legal_moves += self._move_in_direction(position, d, distance)

        return legal_moves

    def diagonal_moves(self, position: BoardCoordinates, distance: int):
        """Find all possible diagonal moves from a position up to (and including) `distance` steps"""
        legal_moves = []
        directions = ((1, 1), (-1, 1), (-1, -1), (1, -1))

        for d in directions:
            legal_moves += self._move_in_direction(position, d, distance)

        return legal_moves

    def _move_in_direction(self, position: BoardCoordinates, direction: Direction, distance: int) -> list[BoardCoordinates]:
        collision = False
        moves = []

        for i in range(1, distance):
            if collision:
                break

            upcoming = self._increment(position, direction, i)
            if not self._collision(upcoming):
                moves.append(upcoming)
            elif not upcoming.is_in_bounds() or self._is_own_piece(upcoming):
                collision = True
            else:
                moves.append(upcoming)
                collision = True

        return moves

    def _increment(self, position: BoardCoordinates, direction: Direction, distance: int) -> BoardCoordinates:
        return BoardCoordinates(position.row + direction[0] * distance, position.col + direction[1] * distance)

    def _collision(self, position: BoardCoordinates) -> bool:
        # TODO: check if there's a piece on the board at `position`
        return not position.is_in_bounds() or self.board.get_piece_at(position) is not None

    def _is_own_piece(self, position: BoardCoordinates) -> bool:
        # TODO: check if there a piece of color `self.color` at `position`
        piece = self.board.get_piece_at(position)
        return piece is not None and self.board.get_piece_at(position).color == self.color


class Pawn(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self.abbreviation = "P"

    def possible_moves(self, position: BoardCoordinates) -> list[BoardCoordinates]:
        if self.color == Color.WHITE:
            home_row = 6
            direction = -1
            enemy = Color.BLACK
        else:
            home_row = 1
            direction = 1
            enemy = Color.WHITE

        legal_moves = []
        blocked = self.board.occupied(Color.WHITE) + self.board.occupied(Color.BLACK)
        forward = BoardCoordinates(position.row + direction, position.col)

        # Can we move forward?
        if forward.is_in_bounds() and forward not in blocked:
            legal_moves.append(forward)
            if position.row == home_row:
                # If pawn in starting position we can do a double move
                double_forward = BoardCoordinates(forward.row + direction, forward.col)
                if double_forward.is_in_bounds() and double_forward not in blocked:
                    legal_moves.append(double_forward)

        # Attacking [-1, 1]
        for a in range(-1, 2, 2):
            attack = BoardCoordinates(position.row + direction, position.col + a)
            if attack.is_in_bounds() and attack in self.board.occupied(enemy):
                legal_moves.append(attack)

        return legal_moves


class Knight(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self.abbreviation = "N"

    def possible_moves(self, position: BoardCoordinates) -> list[BoardCoordinates]:
        MOVES = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))

        piece = self.board.get_piece_at(position)
        if piece is None:
            raise InvalidPiece

        legal_moves = []
        for x, y in MOVES:
            destination = BoardCoordinates(position.row + y, position.col + x)
            if destination.is_in_bounds() and destination not in self.board.occupied(piece.color):
                legal_moves.append(destination)

        return legal_moves


class Rook(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self.abbreviation = "R"

    def possible_moves(self, position: BoardCoordinates) -> list[BoardCoordinates]:
        return super().orthogonal_moves(position, BOARD_SIZE)


class Bishop(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self.abbreviation = "B"

    def possible_moves(self, position: BoardCoordinates) -> list[BoardCoordinates]:
        return super().diagonal_moves(position, BOARD_SIZE)


class Queen(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self.abbreviation = "Q"

    def possible_moves(self, position: BoardCoordinates) -> list[BoardCoordinates]:
        return super().orthogonal_moves(position, BOARD_SIZE) + super().diagonal_moves(position, BOARD_SIZE)


class King(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self.abbreviation = "K"

    def possible_moves(self, position: BoardCoordinates) -> list[BoardCoordinates]:
        return super().orthogonal_moves(position, 1) + super().diagonal_moves(position, 1)


def generate_piece(symbol: str) -> Piece:
    if symbol.isupper():
        color = Color.WHITE
    else:
        color = Color.BLACK

    piece = symbol.upper()
    if piece == "P":
        return Pawn(color)
    if piece == "R":
        return Rook(color)
    if piece == "N":
        return Knight(color)
    if piece == "B":
        return Bishop(color)
    if piece == "Q":
        return Queen(color)
    if piece == "K":
        return King(color)

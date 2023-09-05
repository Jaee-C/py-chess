from abc import ABC, abstractmethod

from .utils import BoardCoordinates, Colour
from .constants import InvalidPiece, BOARD_SIZE
from .board import Board


Direction = tuple[int, int]


class Piece(ABC):
    def __init__(self, colour: Colour):
        self.colour = colour
        self.board = None
        self.abbreviation = "None"

    @abstractmethod
    def possible_moves(self, position: BoardCoordinates) -> list[BoardCoordinates]:
        pass

    def place(self, board: Board):
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

        for i in range(distance):
            if not collision:
                break

            upcoming = self._increment(position, direction, i)
            if not self._collision(upcoming):
                moves.append(upcoming)
            elif self._is_own_piece(upcoming) or not upcoming.is_in_bounds():
                collision = True
            else:
                moves.append(upcoming)
                collision = True

        return moves

    def _increment(self, position: BoardCoordinates, direction: Direction, distance: int) -> BoardCoordinates:
        return BoardCoordinates(position.row + direction[0] * distance, position.col + direction[1] * distance)

    def _collision(self, position: BoardCoordinates) -> bool:
        # TODO: check if there's a piece on the board at `position`
        return position.is_in_bounds()

    def _is_own_piece(self, position: BoardCoordinates) -> bool:
        # TODO: check if there a piece of colour `self.colour` at `position`
        return False


class Pawn(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour)
        self.abbreviation = "P"

    def possible_moves(self, position: BoardCoordinates) -> list[BoardCoordinates]:
        pass


class Knight(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour)
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
    def __init__(self, colour: Colour):
        super().__init__(colour)
        self.abbreviation = "R"

    def possible_moves(self, position: BoardCoordinates) -> list[BoardCoordinates]:
        return super().orthogonal_moves(position, BOARD_SIZE)


class Bishop(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour)
        self.abbreviation = "B"

    def possible_moves(self, position: BoardCoordinates) -> list[BoardCoordinates]:
        return super().diagonal_moves(position, BOARD_SIZE)


class Queen(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour)
        self.abbreviation = "Q"

    def possible_moves(self, position: BoardCoordinates) -> list[BoardCoordinates]:
        return super().orthogonal_moves(position, BOARD_SIZE) + super().diagonal_moves(position, BOARD_SIZE)


class King(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour)
        self.abbreviation = "K"

    def possible_moves(self, position: BoardCoordinates) -> list[BoardCoordinates]:
        return super().orthogonal_moves(position, 1) + super().diagonal_moves(position, 1)


def generate_piece(symbol: str) -> Piece:
    if symbol.isupper():
        colour = Colour.WHITE
    else:
        colour = Colour.BLACK

    piece = symbol.upper()
    if piece == "P":
        return Pawn(colour)
    if piece == "R":
        return Rook(colour)
    if piece == "N":
        return Knight(colour)
    if piece == "B":
        return Bishop(colour)
    if piece == "Q":
        return Queen(colour)
    if piece == "K":
        return King(colour)

from enum import Enum
from abc import ABC, abstractmethod


class Colour(Enum):
    BLACK = 0
    WHITE = 1


class Piece(ABC):
    def __init__(self, colour: Colour):
        self.colour = colour

    @abstractmethod
    def possible_moves(self):
        pass


class Pawn(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour)
        self.abbreviation = "P"

    def possible_moves(self):
        pass


class Knight(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour)
        self.abbreviation = "N"

    def possible_moves(self):
        pass


class Rook(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour)
        self.abbreviation = "R"

    def possible_moves(self):
        pass


class Bishop(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour)
        self.abbreviation = "B"

    def possible_moves(self):
        pass


class Queen(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour)
        self.abbreviation = "Q"

    def possible_moves(self):
        pass


class King(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour)
        self.abbreviation = "K"

    def possible_moves(self):
        pass

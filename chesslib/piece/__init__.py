from chesslib.utils import Color
from .piece import Piece
from .king import King
from .pawn import Pawn
from .queen import Queen
from .rook import Rook
from .knight import Knight
from .bishop import Bishop


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
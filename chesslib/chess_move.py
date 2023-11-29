from enum import Enum

from chesslib.utils import BoardCoordinates


class MoveType(Enum):
    REGULAR = 1
    EN_PASSANT = 2


class ChessMove:
    def __init__(self, start: BoardCoordinates, end: BoardCoordinates, type: MoveType):
        self.start = start
        self.end = end
        self.type = type

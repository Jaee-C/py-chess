BOARD_SIZE = 8
COLUMN_LABELS = ("A", "B", "C", "D", "E", "F", "G", "H")
ROW_LABELS = (1, 2, 3, 4, 5, 6, 7, 8)

# FEN Data: https://www.chess.com/terms/fen-chess
INIT_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
GAME_BOARD = 0
FEN_PLAYER_TURN = 1
FEN_CASTLING = 2
FEN_EN_PASSANT = 3
FEN_HALFMOVE_CLOCK = 4
FEN_FULLMOVE_NUMBER = 5


class OutOfBoundsError(Exception): pass
class InvalidPiece(Exception): pass
class NotYourTurn(Exception): pass

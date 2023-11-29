import unittest

from chesslib.board import Board, Color
from chesslib.piece import Piece, King, Pawn, Rook, Knight, Bishop
from chesslib.utils import BoardCoordinates


class TestCheck(unittest.TestCase):
    def test_check_pawn(self):
        test_board = ChessBoardStub()

        test_board.insert(King(Color.BLACK), algebra_coordinates('E', 8))
        test_board.insert(Pawn(Color.WHITE), algebra_coordinates('D', 7))

        result = test_board.check_validator(Color.BLACK)
        self.assertEqual(True, result)

    def test_check_rook(self):
        test_board = ChessBoardStub()

        test_board.insert(King(Color.BLACK), algebra_coordinates('E', 8))
        test_board.insert(Rook(Color.WHITE), algebra_coordinates('A', 8))

        result = test_board.check_validator(Color.BLACK)
        self.assertEqual(True, result)

    def test_check_bishop(self):
        test_board = ChessBoardStub()

        test_board.insert(King(Color.BLACK), algebra_coordinates('E', 8))
        test_board.insert(Bishop(Color.WHITE), algebra_coordinates('A', 4))

        result = test_board.check_validator(Color.BLACK)
        self.assertEqual(True, result)

    def test_check_knight(self):
        test_board = ChessBoardStub()

        test_board.insert(King(Color.BLACK), algebra_coordinates('E', 8))
        test_board.insert(Knight(Color.WHITE), algebra_coordinates('D', 6))

        result = test_board.check_validator(Color.BLACK)
        self.assertEqual(True, result)

    def test_check_knight_blocked(self):
        test_board = ChessBoardStub()

        test_board.insert(King(Color.BLACK), algebra_coordinates('E', 8))
        test_board.insert(Pawn(Color.BLACK), algebra_coordinates('C', 7))
        test_board.insert(Pawn(Color.BLACK), algebra_coordinates('D', 7))
        test_board.insert(Knight(Color.WHITE), algebra_coordinates('D', 6))

        result = test_board.check_validator(Color.BLACK)
        self.assertEqual(True, result)

    def test_check_bishop_blocked(self):
        test_board = ChessBoardStub()

        test_board.insert(King(Color.BLACK), algebra_coordinates('E', 8))
        test_board.insert(Pawn(Color.BLACK), algebra_coordinates('D', 7))
        test_board.insert(Bishop(Color.WHITE), algebra_coordinates('A', 4))

        result = test_board.check_validator(Color.BLACK)
        self.assertEqual(False, result)

    def test_check_pawn_black(self):
        test_board = ChessBoardStub()

        test_board.insert(King(Color.WHITE), algebra_coordinates('E', 1))
        test_board.insert(Pawn(Color.BLACK), algebra_coordinates('D', 2))

        result = test_board.check_validator(Color.WHITE)
        self.assertEqual(True, result)

    def test_no_check(self):
        test_board = ChessBoardStub()

        test_board.insert(King(Color.BLACK), algebra_coordinates('E', 8))
        test_board.insert(Pawn(Color.WHITE), algebra_coordinates('E', 7))

        result = test_board.check_validator(Color.BLACK)
        self.assertEqual(False, result)

    def test_no_check_wrong_player(self):
        test_board = ChessBoardStub()

        test_board.insert(Pawn(Color.WHITE), algebra_coordinates('D', 7))
        test_board.insert(King(Color.WHITE), algebra_coordinates('E', 1))
        test_board.insert(King(Color.BLACK), algebra_coordinates('E', 8))

        result = test_board.check_validator(Color.WHITE)
        self.assertEqual(False, result)

    def test_checkmate(self):
        test_board = ChessBoardStub()

        test_board.insert(Rook(Color.WHITE), algebra_coordinates('H', 1))
        test_board.insert(Rook(Color.WHITE), algebra_coordinates('G', 1))
        test_board.insert(King(Color.BLACK), algebra_coordinates('H', 8))

        result = test_board.is_checkmate(Color.BLACK)
        self.assertEqual(True, result)

    def test_checkmate_move_out(self):
        test_board = ChessBoardStub()

        test_board.insert(Rook(Color.WHITE), algebra_coordinates('H', 1))
        test_board.insert(King(Color.BLACK), algebra_coordinates('H', 8))

        result = test_board.is_checkmate(Color.BLACK)
        self.assertEqual(False, result)

    def test_checkmate_kill_mate(self):
        test_board = ChessBoardStub()

        test_board.insert(Rook(Color.WHITE), algebra_coordinates('H', 1))
        test_board.insert(Rook(Color.WHITE), algebra_coordinates('G', 1))
        test_board.insert(Bishop(Color.BLACK), algebra_coordinates("A", 8))
        test_board.insert(King(Color.BLACK), algebra_coordinates('H', 8))

        result = test_board.is_checkmate(Color.BLACK)
        self.assertEqual(False, result)


class TestSpecialMoves(unittest.TestCase):
    def test_enpassant_valid_white(self):
        test_board = ChessBoardStub()

        test_board.insert(Pawn(Color.WHITE), algebra_coordinates('B', 5))
        test_board.insert(Pawn(Color.BLACK), algebra_coordinates('A', 7))
        
        test_board.set_player(Color.BLACK)
        
        _ = test_board.move(algebra_coordinates('A', 7), algebra_coordinates('A', 5))
        result = test_board.move(algebra_coordinates('B', 5), algebra_coordinates('A', 6))  # En passant

        self.assertEqual(True, result)


class ChessBoardStub(Board):
    def __init__(self):
        super().__init__()
        self.reset_board()

    def reset_board(self):
        self.state = {}

    def insert(self, piece: Piece, position: BoardCoordinates):
        piece.place(self)
        self.state[str(position)] = piece

    def set_player(self, color: Color):
        self.current_player = color


def algebra_coordinates(col: str, row: int) -> BoardCoordinates:
    return BoardCoordinates.from_algebra_notation(col, row)


if __name__ == '__main__':
    unittest.main()

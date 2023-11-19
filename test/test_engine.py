import unittest
from chesslib.board import Board, Color
from chesslib.piece import Piece, King, Pawn, Rook, Knight, Bishop
from chesslib.utils import BoardCoordinates


class TestChessBoard(unittest.TestCase):
    def test_check_pawn(self):
        test_board = ChessBoardStub()

        test_board.insert(King(Color.BLACK), BoardCoordinates.from_algebra_notation('E', 8))
        test_board.insert(Pawn(Color.WHITE), BoardCoordinates.from_algebra_notation('D', 7))

        result = test_board.is_in_check(Color.BLACK)
        self.assertEqual(True, result)

    def test_check_rook(self):
        test_board = ChessBoardStub()

        test_board.insert(King(Color.BLACK), BoardCoordinates.from_algebra_notation('E', 8))
        test_board.insert(Rook(Color.WHITE), BoardCoordinates.from_algebra_notation('A', 8))

        result = test_board.is_in_check(Color.BLACK)
        self.assertEqual(True, result)

    def test_check_bishop(self):
        test_board = ChessBoardStub()

        test_board.insert(King(Color.BLACK), BoardCoordinates.from_algebra_notation('E', 8))
        test_board.insert(Bishop(Color.WHITE), BoardCoordinates.from_algebra_notation('A', 4))

        result = test_board.is_in_check(Color.BLACK)
        self.assertEqual(True, result)

    def test_check_knight(self):
        test_board = ChessBoardStub()

        test_board.insert(King(Color.BLACK), BoardCoordinates.from_algebra_notation('E', 8))
        test_board.insert(Knight(Color.WHITE), BoardCoordinates.from_algebra_notation('D', 6))

        result = test_board.is_in_check(Color.BLACK)
        self.assertEqual(True, result)

    def test_check_knight_blocked(self):
        test_board = ChessBoardStub()

        test_board.insert(King(Color.BLACK), BoardCoordinates.from_algebra_notation('E', 8))
        test_board.insert(Pawn(Color.BLACK), BoardCoordinates.from_algebra_notation('C', 7))
        test_board.insert(Pawn(Color.BLACK), BoardCoordinates.from_algebra_notation('D', 7))
        test_board.insert(Knight(Color.WHITE), BoardCoordinates.from_algebra_notation('D', 6))

        result = test_board.is_in_check(Color.BLACK)
        self.assertEqual(True, result)

    def test_check_bishop_blocked(self):
        test_board = ChessBoardStub()

        test_board.insert(King(Color.BLACK), BoardCoordinates.from_algebra_notation('E', 8))
        test_board.insert(Pawn(Color.BLACK), BoardCoordinates.from_algebra_notation('D', 7))
        test_board.insert(Bishop(Color.WHITE), BoardCoordinates.from_algebra_notation('A', 4))

        result = test_board.is_in_check(Color.BLACK)
        self.assertEqual(False, result)

    def test_check_pawn_black(self):
        test_board = ChessBoardStub()

        test_board.insert(King(Color.WHITE), BoardCoordinates.from_algebra_notation('E', 1))
        test_board.insert(Pawn(Color.BLACK), BoardCoordinates.from_algebra_notation('D', 2))

        result = test_board.is_in_check(Color.WHITE)
        self.assertEqual(True, result)

    def test_no_check(self):
        test_board = ChessBoardStub()

        test_board.insert(King(Color.BLACK), BoardCoordinates.from_algebra_notation('E', 8))
        test_board.insert(Pawn(Color.WHITE), BoardCoordinates.from_algebra_notation('E', 7))

        result = test_board.is_in_check(Color.BLACK)
        self.assertEqual(False, result)

    def test_no_check_wrong_player(self):
        test_board = ChessBoardStub()

        test_board.insert(Pawn(Color.WHITE), BoardCoordinates.from_algebra_notation('D', 7))
        test_board.insert(King(Color.WHITE), BoardCoordinates.from_algebra_notation('E', 1))
        test_board.insert(King(Color.BLACK), BoardCoordinates.from_algebra_notation('E', 8))

        result = test_board.is_in_check(Color.WHITE)
        self.assertEqual(False, result)


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


if __name__ == '__main__':
    unittest.main()

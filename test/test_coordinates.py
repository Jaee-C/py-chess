import unittest
from parameterized import parameterized

from chesslib.constants import BOARD_SIZE
from chesslib.utils import BoardCoordinates


class TestBoardCoordinates(unittest.TestCase):
    @parameterized.expand([
        ("First", 0, 0, "A1"),
        ("Last", 7, 7, "H8"),
        ("Random1", 2, 6, "G3"),
        ("Random2", 6, 3, "D7"),
    ])
    def test_letter_notation(self, name, row, col, expected):
        coordinates = BoardCoordinates(row, col)
        self.assertEqual(coordinates.letter_notation(), expected)

    @parameterized.expand([
        (0, -34, False),
        (0, 0, True),
        (1, 5, True),
        (BOARD_SIZE + 1, 2, False),
        (-1, BOARD_SIZE + 99, False),
        (1, 1, True),
        (BOARD_SIZE, BOARD_SIZE, False)
    ])
    def test_bounds(self, row, col, expected):
        coordinates = BoardCoordinates(row, col)
        self.assertEqual(coordinates.is_in_bounds(), expected)


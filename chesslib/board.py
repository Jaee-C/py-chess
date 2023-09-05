import re

from .constants import INIT_FEN, OutOfBoundsError, NotYourTurn
from .utils import Color, BoardCoordinates
from .piece import Piece, generate_piece


def expand_blanks(match: re.Match[str]) -> str:
    return " " * int(match.group(0))


class Board:
    def __init__(self):
        self.state: dict[str, Piece] = {}
        self.current_player: Color = Color.WHITE

        self.positions = []
        self.highlighted: list[BoardCoordinates] = []

        self.load(INIT_FEN)

    def move(self, start: BoardCoordinates, end: BoardCoordinates):
        if not start.is_in_bounds() or not end.is_in_bounds():
            raise OutOfBoundsError

        moved_piece = self.get_piece_at(start)
        if not moved_piece.color == self.current_player:
            raise NotYourTurn

        self._make_move(start, end)
        self._finish_move(start, end)

    def load(self, config: str):
        """Import state from FEN notation"""
        fen = config.split(" ")
        fen[0] = re.compile(r"\d").sub(expand_blanks, fen[0])
        self.positions = []
        for x, row in enumerate(self._get_rows(fen[0])):
            for y, letter in enumerate(row):
                if self._is_cell_empty(letter):
                    continue
                coords = BoardCoordinates(7 - x + 1, y + 1)
                letter_coords = coords.letter_notation()
                self.state[letter_coords] = generate_piece(letter)
                self.state[letter_coords].place(self)

        if fen[1] == "w":
            self.current_player = Color.WHITE
        else:
            self.current_player = Color.BLACK

    def _make_move(self, start: BoardCoordinates, end: BoardCoordinates):
        moved_piece = self.state[start.letter_notation()]
        self._update_coord_piece(start, None)
        self._update_coord_piece(end, moved_piece)

    def _finish_move(self, start: BoardCoordinates, end: BoardCoordinates):
        enemy = self.get_opponent(self.current_player)
        self.current_player = enemy

        self._print_move(start, end)

    def _update_coord_piece(self, coord: BoardCoordinates, piece: Piece | None):
        """
        Update board state with the piece and coordinate.
        If piece is `None`, the coordinate is unoccupied
        """
        pos = str(coord)
        if piece is None:
            del self.state[pos]
        else:
            self.state[pos] = piece

    def get_opponent(self, color: Color):
        if color == Color.WHITE:
            return Color.BLACK
        return Color.WHITE

    def get_piece_at(self, location: BoardCoordinates) -> Piece | None:
        coordinates = location.letter_notation()

        if coordinates not in self.state:
            return None
        return self.state[coordinates]

    def _print_move(self, source: BoardCoordinates, destination: BoardCoordinates):
        piece = self.get_piece_at(source)
        abbr = piece.abbreviation
        target_piece = self.get_piece_at(destination)

        if target_piece is None:
            movetext = abbr + destination.letter_notation().lower()
        else:
            movetext = abbr + "x" + destination.letter_notation()

        print("move: " + movetext)

    def items(self):
        return self.state.items()

    @staticmethod
    def _get_rows(fen: str) -> list[str]:
        return fen.split("/")

    @staticmethod
    def _is_cell_empty(val: str) -> bool:
        return val == " "

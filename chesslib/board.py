import re
import copy

from .constants import INIT_FEN, OutOfBoundsError, NotYourTurn, InvalidPiece
from .utils import Color, BoardCoordinates, parse_letter_coordinates, get_opponent
from .chess_move import MoveType, ChessMove
from chesslib.piece import generate_piece, Piece, Pawn


def expand_blanks(match: re.Match[str]) -> str:
    return " " * int(match.group(0))


def extract_move(move: ChessMove) -> BoardCoordinates:
    return move.end


class Board:
    def __init__(self):
        self.state: dict[str, Piece] = {}
        self.current_player: Color = Color.WHITE
        self.previous_moved_pawn: BoardCoordinates | None = None

        self.positions = []

        self.load(INIT_FEN)

    def move(self, start: BoardCoordinates, end: BoardCoordinates) -> bool:
        """Move piece from `start` to `end`, only if the move is valid. Prints out a successful move to console."""
        if not start.is_in_bounds() or not end.is_in_bounds():
            raise OutOfBoundsError

        self.previous_moved_pawn = None
        moved_piece = self.get_piece_at(start)
        target = self.get_piece_at(end)
        if not moved_piece.color == self.current_player:
            raise NotYourTurn

        valid_move = self._valid_move(start, end)

        if valid_move is None:
            return False

        self._make_move(valid_move)
        self._finish_move(moved_piece, target, start, end)
        return True

    def _valid_move(self, start: BoardCoordinates, end: BoardCoordinates) -> ChessMove | None:
        moved_piece = self.get_piece_at(start)
        legal_moves = moved_piece.possible_moves(start)

        filtered_move = list(filter(lambda x: x.end == end, legal_moves))

        if len(filtered_move) != 1:
            print("Illegal move")
            return None

        # Check for check
        if self._is_in_check(self.current_player, ChessMove(start, end, MoveType.REGULAR)):
            print("You're in check!")
            return None

        return filtered_move[0]

    def load(self, config: str):
        """Import state from FEN notation"""
        fen = config.split(" ")
        fen[0] = re.compile(r"\d").sub(expand_blanks, fen[0])
        self.positions = []
        for x, row in enumerate(self._get_rows(fen[0])):
            for y, letter in enumerate(row):
                if self._is_cell_empty(letter):
                    continue
                coords = BoardCoordinates(x, 7 - y)
                letter_coords = coords.letter_notation()
                self.state[letter_coords] = generate_piece(letter)
                self.state[letter_coords].place(self)

        if fen[1] == "w":
            self.current_player = Color.WHITE
        else:
            self.current_player = Color.BLACK

    def occupied(self, color: Color) -> list[BoardCoordinates]:
        """Return all coordinates occupied by player `color`"""
        result: list[str] = []

        for coord in self.state:
            if self.state[coord].color == color:
                result.append(coord)

        return list(map(parse_letter_coordinates, result))

    def is_checkmate(self, player: Color) -> bool:
        """Checks whether `player` is check-mated"""
        if not self.check_validator(player):
            return False

        for pos, piece in self.state.items():
            if not piece.color == player:
                continue

            start = parse_letter_coordinates(pos)
            moves = piece.possible_moves(start)

            for move in moves:
                if not self._is_in_check(player, move):
                    return False

        return True

    def _is_in_check(self, player: Color, move: ChessMove) -> bool:
        clone = copy.deepcopy(self)
        clone._make_move(move)

        return clone.check_validator(player)

    def check_validator(self, player: Color) -> bool:
        """Checks whether `player` is currently checked"""
        king_location = self.find_piece("K", player)

        if king_location is None:
            return False

        for pos, piece in self.state.items():
            if piece.color == player:
                continue

            moves = piece.possible_moves(parse_letter_coordinates(pos))

            if king_location in map(extract_move, moves):
                return True

        return False

    def find_piece(self, abbr: str, color: Color) -> BoardCoordinates | None:
        for coord, piece in self.state.items():
            if piece.abbreviation == abbr and piece.color == color:
                return parse_letter_coordinates(coord)
        print("Piece not found")
        return None

    def _make_move(self, move: ChessMove):
        self._move_pawn(move)
        match move.type:
            case MoveType.EN_PASSANT:
                self._make_en_passant_move(move)
            case _:
                self._make_regular_move(move)

    def _make_regular_move(self, move: ChessMove):
        moved_piece = self.state[move.start.letter_notation()]
        self._update_coord_piece(move.start, None)
        self._update_coord_piece(move.end, moved_piece)

    def _make_en_passant_move(self, move: ChessMove):
        moved_piece = self.state[move.start.letter_notation()]
        assert (isinstance(moved_piece, Pawn))

        target_location = BoardCoordinates(move.start.row, move.end.col)
        self._update_coord_piece(target_location, None)
        self._make_regular_move(move)

    def _move_pawn(self, move: ChessMove):
        moved_piece = self.state[move.start.letter_notation()]
        if not isinstance(moved_piece, Pawn):
            return

        self.previous_moved_pawn = move.end

        moved_piece.pawn_is_moved(move)

    def _reset_pawns(self):
        if self.previous_moved_pawn is None:
            return

        for location, p in self.state.items():
            if isinstance(p, Pawn) and parse_letter_coordinates(location) != self.previous_moved_pawn:
                p.first_move = False

    def _finish_move(self, moved_piece: Piece, target: Piece, start: BoardCoordinates, end: BoardCoordinates):
        enemy = get_opponent(self.current_player)
        self.current_player = enemy
        self._reset_pawns()

        self._print_move(moved_piece, target, start, end)

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

    def get_piece_at(self, location: BoardCoordinates) -> Piece | None:
        coordinates = location.letter_notation()

        if coordinates not in self.state:
            return None
        return self.state[coordinates]

    def _print_move(self, moved_piece: Piece, target: Piece, source: BoardCoordinates, destination: BoardCoordinates):
        abbr = moved_piece.abbreviation

        if target is None:
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

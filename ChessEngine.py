import pygame

from constants import BOARD_SIZE, SQUARE_SIZE
from chesslib.utils import BoardCoordinates
from chesslib.board import Board
from chesslib.piece import Piece


class ChessEngine:
    def __init__(self, screen: pygame.display):
        self.board = Board()
        self.screen = screen
        self.icons: dict[str, pygame.image] = {}

        self.load_images()

    def draw_game(self):
        self.draw_squares()
        self.draw_pieces()

    def draw_squares(self):
        colors = [pygame.Color("white"), pygame.Color("gray")]
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                square_color = colors[(row + col) % 2]
                pygame.draw.rect(self.screen, square_color, pygame.Rect(row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                self.draw_piece(row, col)

    def draw_piece(self, row: int, col: int):
        x = col * SQUARE_SIZE
        y = row * SQUARE_SIZE

        piece = self.board.get_piece_at(BoardCoordinates(row, col))
        if piece is None:
            return

        self.screen.blit(self.icons[self._get_piece_name(piece)], pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE))

    def load_images(self):
        color = ["white", "black"]
        piece = ["p", "r", "n", "b", "k", "q"]

        for c in color:
            for p in piece:
                self.icons[c + p] = pygame.image.load(f"img/{c}{p}.png")

    def _get_piece_name(self, piece: Piece) -> str:
        return f"{piece.color}{piece.abbreviation.lower()}"
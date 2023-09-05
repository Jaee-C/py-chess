import pygame

from constants import BOARD_SIZE, SQUARE_SIZE
from chesslib.board import Board


class ChessEngine:
    def __init__(self, screen: pygame.display):
        self.board = Board()
        self.screen = screen

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
        pass

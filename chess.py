import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ChessUI import ChessUI

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    running = True

    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    game = ChessUI(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                game.click(x, y)

        game.draw_game()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()


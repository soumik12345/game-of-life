import copy
import random
import pygame


class GameOfLife:
    def __init__(
        self,
        height: int = 900,
        width: int = 1600,
        frame_rate: int = 10,
        background_color: str = "black",
    ):
        self.height = height
        self.width = width
        self.frame_rate = frame_rate
        self.background_color = background_color
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.screen.fill(pygame.Color(self.background_color))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            pygame.display.flip()
            self.clock.tick(self.frame_rate)


if __name__ == "__main__":
    game = GameOfLife()
    game.run()

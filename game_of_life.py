import copy
import random
import pygame


class GameOfLife:
    def __init__(
        self,
        height: int = 900,
        width: int = 1600,
        cell_size: int = 50,
        frame_rate: int = 10,
        background_color: str = "black",
    ):
        self.pixel_height = height
        self.pixel_width = width
        self.cell_size = cell_size
        self.frame_rate = frame_rate
        self.background_color = background_color

        pygame.init()
        self.num_cells_i = self.pixel_width // self.cell_size
        self.num_cells_j = self.pixel_height // self.cell_size
        self.screen = pygame.display.set_mode((self.pixel_width, self.pixel_height))
        self.clock = pygame.time.Clock()

    def draw_grid(self):
        for i in range(0, self.pixel_width, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("white"), (i, 0), (i, self.pixel_height)
            )
        for j in range(0, self.pixel_height, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("white"), (0, j), (self.pixel_width, j)
            )

    def run(self):
        while True:
            self.screen.fill(pygame.Color(self.background_color))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            self.draw_grid()

            pygame.display.flip()
            self.clock.tick(self.frame_rate)


if __name__ == "__main__":
    game = GameOfLife()
    game.run()

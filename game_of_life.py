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
        life_color: str = "green",
    ):
        self.pixel_height = height
        self.pixel_width = width
        self.cell_size = cell_size
        self.frame_rate = frame_rate
        self.background_color = background_color
        self.life_color = life_color

        self.num_cells_i = self.pixel_width // self.cell_size
        self.num_cells_j = self.pixel_height // self.cell_size

        self.current_game_state = [
            [random.randint(0, 1) for _ in range(self.num_cells_i)]
            for _ in range(self.num_cells_j)
        ]
        self.next_game_state = [
            [0 for _ in range(self.num_cells_i)] for _ in range(self.num_cells_j)
        ]

        pygame.init()
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

    def check_living_status_of_cell(self, x, y):
        num_neighbors = 0
        for j in range(y - 1, y + 2):
            for i in range(x - 1, x + 2):
                if self.current_game_state[j][i] == 1:
                    num_neighbors += 1
        if self.current_game_state[y][x]:
            num_neighbors -= 1
            if num_neighbors == 2 or num_neighbors == 3:
                return 1
            return 0
        else:
            if num_neighbors == 3:
                return 1
            return 0

    def update_game_state(self):
        for x in range(1, self.num_cells_i - 1):
            for y in range(1, self.num_cells_j - 1):
                if self.current_game_state[y][x] == 1:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color(self.life_color),
                        (
                            x * self.cell_size + 2,
                            y * self.cell_size + 2,
                            self.cell_size - 2,
                            self.cell_size - 2,
                        ),
                    )
                self.next_game_state[y][x] = self.check_living_status_of_cell(x, y)
        self.current_game_state = copy.deepcopy(self.next_game_state)

    def run(self):
        while True:
            self.screen.fill(pygame.Color(self.background_color))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            self.draw_grid()
            self.update_game_state()

            pygame.display.flip()
            self.clock.tick(self.frame_rate)


if __name__ == "__main__":
    game = GameOfLife()
    game.run()

import numpy as np
import pygame
import random
from pydantic import BaseModel
import fire


class Resolution(BaseModel):
    width: int
    height: int


class GameOfLifeState:
    def __init__(
        self, resolution: Resolution, cell_size: int = 50, frames_per_second: int = 10
    ):
        self.resolution: Resolution = resolution
        self.cell_size: int = cell_size
        self.frames_per_second: int = frames_per_second
        self.grid_width: int = self.resolution.width // self.cell_size
        self.grid_height: int = self.resolution.height // self.cell_size
        self.current_state_array = np.random.randint(
            2, size=(self.grid_height, self.grid_width)
        )
        self.surface: pygame.Surface = pygame.display.set_mode(
            (self.resolution.width, self.resolution.height)
        )
        self.clock: pygame.time.Clock = pygame.time.Clock()


def draw_grid(game_state: GameOfLifeState):
    for x in range(0, game_state.resolution.width, game_state.cell_size):
        pygame.draw.line(
            game_state.surface,
            pygame.Color("dimgray"),
            (x, 0),
            (x, game_state.resolution.height),
        )
    for y in range(0, game_state.resolution.height, game_state.cell_size):
        pygame.draw.line(
            game_state.surface,
            pygame.Color("dimgray"),
            (0, y),
            (game_state.resolution.width, y),
        )


def simulate_life(game_state: GameOfLifeState) -> GameOfLifeState:
    neighbor_count = np.zeros((game_state.grid_height, game_state.grid_width))
    for dx, dy in [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]:
        neighbor_count += np.roll(
            np.roll(game_state.current_state_array, dy, axis=0), dx, axis=1
        )

    birth = (neighbor_count == 3) & (game_state.current_state_array == 0)
    survival = ((neighbor_count == 2) | (neighbor_count == 3)) & (
        game_state.current_state_array == 1
    )
    game_state.current_state_array = np.where(birth | survival, 1, 0)

    for y in range(game_state.grid_height):
        for x in range(game_state.grid_width):
            if game_state.current_state_array[y, x] == 1:
                rectangle_coordinates = (
                    x * game_state.cell_size + 2,
                    y * game_state.cell_size + 2,
                    game_state.cell_size - 2,
                    game_state.cell_size - 2,
                )
                pygame.draw.rect(
                    game_state.surface,
                    pygame.Color("forestgreen"),
                    rectangle_coordinates,
                )
    return game_state


def execute_game_logic(game_state: GameOfLifeState) -> GameOfLifeState:
    draw_grid(game_state)
    return simulate_life(game_state)


def execute_game_loop(game_state: GameOfLifeState):
    pygame.init()
    while True:
        game_state.surface.fill(pygame.Color("black"))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        game_state = execute_game_logic(game_state)
        pygame.display.flip()
        pygame.display.set_caption(f"FPS: {game_state.clock.get_fps():.3f}")
        game_state.clock.tick(game_state.frames_per_second)


def start_game_of_life(
    resolution_width: int = 1600,
    resolution_height: int = 900,
    cell_size: int = 50,
    frames_per_second: int = 10,
):
    game_state = GameOfLifeState(
        resolution=Resolution(width=resolution_width, height=resolution_height),
        cell_size=cell_size,
        frames_per_second=frames_per_second,
    )
    execute_game_loop(game_state)


if __name__ == "__main__":
    fire.Fire(start_game_of_life)

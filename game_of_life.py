import random
from copy import deepcopy
from typing import List

import fire
import pygame
from pydantic import BaseModel


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
        self.current_state_array = [
            [random.randint(0, 1) for _ in range(self.grid_width)]
            for _ in range(self.grid_height)
        ]
        self.next_state_array = [
            [0 for _ in range(self.grid_width)] for _ in range(self.grid_height)
        ]
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


def check_cell(
    current_state_array: List[List[int]], cell_coordinate_x: int, cell_coordinate_y: int
) -> int:
    neighbor_count = 0
    for j in range(cell_coordinate_y - 1, cell_coordinate_y + 2):
        for i in range(cell_coordinate_x - 1, cell_coordinate_x + 2):
            if current_state_array[j][i] == 1:
                neighbor_count += 1
    if current_state_array[cell_coordinate_y][cell_coordinate_x] == 1:
        neighbor_count -= 1
        if neighbor_count == 2 or neighbor_count == 3:
            return 1
        return 0
    else:
        if neighbor_count == 3:
            return 1
        return 0


def simulate_life(game_state: GameOfLifeState) -> GameOfLifeState:
    for x in range(1, game_state.grid_width - 1):
        for y in range(1, game_state.grid_height - 1):
            if game_state.current_state_array[y][x] == 1:
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
            game_state.next_state_array[y][x] = check_cell(
                game_state.current_state_array, x, y
            )
    game_state.current_state_array = deepcopy(game_state.next_state_array)
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

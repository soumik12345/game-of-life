import pygame
from pydantic import BaseModel


class Resolution(BaseModel):
    width: int
    height: int


class GameOfLifeState:
    resolution: Resolution = Resolution(width=1600, height=900)
    frames_per_second: int = 10
    surface: pygame.Surface = pygame.display.set_mode(
        (resolution.width, resolution.height)
    )
    clock: pygame.time.Clock = pygame.time.Clock()


def execute_gaming_loop(game_state: GameOfLifeState):
    pygame.init()
    while True:
        game_state.surface.fill(pygame.Color("black"))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        pygame.display.flip()
        game_state.clock.tick(game_state.frames_per_second)


if __name__ == "__main__":
    game_state = GameOfLifeState()
    execute_gaming_loop(game_state)

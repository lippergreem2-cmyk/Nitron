import random
import pygame
import config


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        """Place food at a random grid cell."""
        self.position = (
            random.randint(0, config.GRID_WIDTH - 1),
            random.randint(0, config.GRID_HEIGHT - 1),
        )

    def draw(self, surface):
        rect = pygame.Rect(
            self.position[0] * config.CELL_SIZE,
            self.position[1] * config.CELL_SIZE,
            config.CELL_SIZE,
            config.CELL_SIZE,
        )
        pygame.draw.rect(surface, config.RED, rect)
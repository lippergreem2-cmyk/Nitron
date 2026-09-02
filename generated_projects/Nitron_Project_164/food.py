import random
import pygame
from settings import CELL_SIZE, GRID_WIDTH, GRID_HEIGHT, COLOR_FOOD

class Food:
    """Represents the food that the snake eats."""

    def __init__(self, snake):
        self.snake = snake
        self.position = self._random_position()

    def _random_position(self):
        """Find a random position not occupied by the snake."""
        available = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in self.snake.body
        ]
        return random.choice(available) if available else None

    def respawn(self):
        """Place the food at a new random location."""
        self.position = self._random_position()

    def draw(self, surface):
        """Render the food onto the given surface."""
        if self.position is None:
            return
        rect = pygame.Rect(self.position[0] * CELL_SIZE,
                           self.position[1] * CELL_SIZE,
                           CELL_SIZE,
                           CELL_SIZE)
        pygame.draw.rect(surface, COLOR_FOOD, rect)
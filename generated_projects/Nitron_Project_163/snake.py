import random
import pygame
import config


class Snake:
    def __init__(self):
        # Start in the middle of the grid
        start_x = config.GRID_WIDTH // 2
        start_y = config.GRID_HEIGHT // 2
        self.positions = [(start_x, start_y)]
        # Random initial direction
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.growing = False

    def get_head_position(self):
        return self.positions[0]

    def turn(self, direction):
        """Change direction unless it's directly opposite to current."""
        opposite = (-self.direction[0], -self.direction[1])
        if direction != opposite:
            self.direction = direction

    def move(self):
        """Move snake one cell in the current direction."""
        cur_x, cur_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_pos = (cur_x + dir_x, cur_y + dir_y)

        # Insert new head
        self.positions = [new_pos] + self.positions

        # Remove tail unless we have just eaten food
        if self.growing:
            self.growing = False
        else:
            self.positions.pop()

    def grow(self):
        """Trigger growth on the next move."""
        self.growing = True

    def draw(self, surface):
        for pos in self.positions:
            rect = pygame.Rect(
                pos[0] * config.CELL_SIZE,
                pos[1] * config.CELL_SIZE,
                config.CELL_SIZE,
                config.CELL_SIZE,
            )
            pygame.draw.rect(surface, config.GREEN, rect)

    def collides_with_self(self):
        """Check if the head collides with any other part of its body."""
        head = self.get_head_position()
        return head in self.positions[1:]

    def collides_with_wall(self):
        """Check if the head is outside the grid boundaries."""
        head_x, head_y = self.get_head_position()
        return (
            head_x < 0
            or head_x >= config.GRID_WIDTH
            or head_y < 0
            or head_y >= config.GRID_HEIGHT
        )
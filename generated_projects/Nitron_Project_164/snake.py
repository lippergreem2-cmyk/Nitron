import pygame
from settings import CELL_SIZE, GRID_WIDTH, GRID_HEIGHT, COLOR_SNAKE

class Snake:
    """Represents the snake in the game."""

    def __init__(self):
        self.reset()

    def reset(self):
        """Initialize or reset the snake to its starting state."""
        # Start in the middle of the grid with length 3, moving right
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.body = [(start_x - i, start_y) for i in range(3)]
        self.direction = (1, 0)   # (dx, dy) moving right
        self.grow_pending = 0

    @property
    def head(self):
        """Return the coordinate of the snake's head."""
        return self.body[0]

    def change_direction(self, new_dir):
        """Change direction unless it's directly opposite to current."""
        opposite = (-self.direction[0], -self.direction[1])
        if new_dir != opposite:
            self.direction = new_dir

    def move(self):
        """Advance the snake by one cell."""
        dx, dy = self.direction
        new_head = (self.head[0] + dx, self.head[1] + dy)

        # Insert new head
        self.body.insert(0, new_head)

        # Remove tail unless we need to grow
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def grow(self, amount=1):
        """Schedule the snake to grow by `amount` cells."""
        self.grow_pending += amount

    def collides_with_self(self):
        """Check if the snake's head collides with its body."""
        return self.head in self.body[1:]

    def collides_with_wall(self):
        """Check if the snake's head is outside the grid."""
        x, y = self.head
        return not (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT)

    def draw(self, surface):
        """Render the snake onto the given surface."""
        for segment in self.body:
            rect = pygame.Rect(segment[0] * CELL_SIZE,
                               segment[1] * CELL_SIZE,
                               CELL_SIZE,
                               CELL_SIZE)
            pygame.draw.rect(surface, COLOR_SNAKE, rect)
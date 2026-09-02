import curses

# Direction vectors
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

OPPOSITE = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT,
}


class Snake:
    """
    Represents the snake. The body is a list of (y, x) tuples,
    head = body[0].
    """

    def __init__(self, init_body):
        """
        init_body: list of (y, x) tuples, head first.
        """
        self.body = init_body
        self.direction = RIGHT  # default moving right

    def set_direction(self, key):
        """
        Change direction based on pressed key.
        Ignores opposite direction to avoid instant self‑collision.
        """
        new_dir = None
        if key in (curses.KEY_UP, ord('w'), ord('W')):
            new_dir = UP
        elif key in (curses.KEY_DOWN, ord('s'), ord('S')):
            new_dir = DOWN
        elif key in (curses.KEY_LEFT, ord('a'), ord('A')):
            new_dir = LEFT
        elif key in (curses.KEY_RIGHT, ord('d'), ord('D')):
            new_dir = RIGHT

        if new_dir and new_dir != OPPOSITE[self.direction]:
            self.direction = new_dir

    def next_head_position(self):
        """Calculate the next head coordinates without modifying the body."""
        head_y, head_x = self.body[0]
        dy, dx = self.direction
        return (head_y + dy, head_x + dx)

    def move(self, grow=False):
        """
        Advance the snake by one cell.
        If grow is True, the tail is not removed, making the snake longer.
        Returns the new head position.
        """
        new_head = self.next_head_position()
        self.body.insert(0, new_head)
        if not grow:
            self.body.pop()
        return new_head

    def collides_with_self(self):
        """Check if the head collides with any other part of its body."""
        return self.body[0] in self.body[1:]

    def occupies(self, pos):
        """Return True if any part of the snake occupies the given position."""
        return pos in self.body
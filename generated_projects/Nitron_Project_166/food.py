import random


def generate_food(snake_body, width, height):
    """
    Return a coordinate (y, x) for a new food item.
    Guarantees the position is not occupied by the snake.
    """
    while True:
        y = random.randint(1, height - 2)
        x = random.randint(1, width - 2)
        if (y, x) not in snake_body:
            return (y, x)
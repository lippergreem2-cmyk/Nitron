import curses
from config import WIDTH, HEIGHT, SPEED
from snake import Snake
from food import generate_food


def draw_border(win):
    """Draw a simple border around the playing area."""
    win.border()


def render_score(win, score):
    """Render the current score on the top border."""
    score_text = f" Score: {score} "
    # place after the left corner, erase previous content first
    win.addstr(0, 2, " " * (len(score_text) + 2))
    win.addstr(0, 2, score_text)


def game_over(win, score):
    """Display Game Over message and wait for a key press."""
    msg = f" Game Over! Score: {score} "
    win.addstr(HEIGHT // 2, (WIDTH - len(msg)) // 2, msg, curses.A_BOLD)
    win.nodelay(False)
    win.getch()


def main(stdscr):
    # Curses initialization
    curses.curs_set(0)          # hide cursor
    stdscr.nodelay(True)       # make getch non‑blocking
    stdscr.timeout(SPEED)      # control game speed

    # Create a new window for the game
    win = curses.newwin(HEIGHT, WIDTH, 0, 0)
    win.keypad(True)           # enable special keys
    draw_border(win)

    # Initial snake positioned in the middle, moving right
    init_y = HEIGHT // 2
    init_x = WIDTH // 2
    init_body = [(init_y, init_x - i) for i in range(3)]  # head at leftmost part
    snake = Snake(init_body)

    # Draw initial snake
    for y, x in snake.body:
        win.addch(y, x, '#')

    # Initial food
    food = generate_food(snake.body, WIDTH, HEIGHT)
    win.addch(food[0], food[1], '*')

    score = 0
    render_score(win, score)

    while True:
        # Input handling
        try:
            key = win.getch()
        except curses.error:
            key = -1

        if key != -1:
            snake.set_direction(key)

        # Determine next position and whether we eat food
        next_head = snake.next_head_position()
        grow = next_head == food

        # Collision with walls
        if (next_head[0] == 0 or next_head[0] == HEIGHT - 1 or
                next_head[1] == 0 or next_head[1] == WIDTH - 1):
            game_over(win, score)
            break

        # Collision with self
        if next_head in snake.body:
            game_over(win, score)
            break

        # Move snake (grow if we ate food)
        snake.move(grow=grow)

        # Draw new head
        win.addch(snake.body[0][0], snake.body[0][1], '#')

        if grow:
            score += 1
            render_score(win, score)
            # Place new food
            food = generate_food(snake.body, WIDTH, HEIGHT)
            win.addch(food[0], food[1], '*')
        else:
            # Erase tail
            tail_y, tail_x = snake.body[-1]
            win.addch(tail_y, tail_x, ' ')

        # Refresh the window
        win.refresh()


if __name__ == "__main__":
    curses.wrapper(main)
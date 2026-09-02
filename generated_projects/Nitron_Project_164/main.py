import sys
import pygame
from settings import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    COLOR_BG,
    COLOR_TEXT,
    FPS,
)
from snake import Snake
from food import Food

# Mapping of pygame keys to direction vectors
KEY_DIRECTION = {
    pygame.K_UP: (0, -1),
    pygame.K_w: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_s: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_a: (-1, 0),
    pygame.K_RIGHT: (1, 0),
    pygame.K_d: (1, 0),
}

def draw_text(surface, text, size, pos):
    """Render text centered at `pos`."""
    font = pygame.font.SysFont(None, size)
    rendered = font.render(text, True, COLOR_TEXT)
    rect = rendered.get_rect(center=pos)
    surface.blit(rendered, rect)

def game_loop():
    """Main game loop."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food(snake)
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if game_over:
                    # Any key restarts the game
                    snake.reset()
                    food.respawn()
                    game_over = False
                else:
                    if event.key in KEY_DIRECTION:
                        snake.change_direction(KEY_DIRECTION[event.key])

        if not game_over:
            snake.move()

            # Check for collisions
            if snake.collides_with_wall() or snake.collides_with_self():
                game_over = True

            # Check food consumption
            if snake.head == food.position:
                snake.grow()
                food.respawn()

        # Rendering
        screen.fill(COLOR_BG)
        snake.draw(screen)
        food.draw(screen)

        if game_over:
            draw_text(
                screen,
                "Game Over! Press any key to restart.",
                36,
                (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2),
            )

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
import sys
import pygame
import config
from snake import Snake
from food import Food

# Mapping of pygame key constants to direction vectors
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


def draw_grid(surface):
    """Optional visual grid; can be commented out for performance."""
    for y in range(0, config.HEIGHT, config.CELL_SIZE):
        pygame.draw.line(surface, config.WHITE, (0, y), (config.WIDTH, y))
    for x in range(0, config.WIDTH, config.CELL_SIZE):
        pygame.draw.line(surface, config.WHITE, (x, 0), (x, config.HEIGHT))


def main():
    pygame.init()
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption("Nitron Snake")
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food()
    score = 0
    font = pygame.font.SysFont("arial", 24)

    running = True
    while running:
        clock.tick(config.FPS)

        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key in KEY_DIRECTION:
                    snake.turn(KEY_DIRECTION[event.key])

        # --- Game logic ---
        snake.move()

        # Check for collisions
        if snake.collides_with_wall() or snake.collides_with_self():
            # Game over
            running = False
            continue

        # Food consumption
        if snake.get_head_position() == food.position:
            snake.grow()
            score += 1
            # Ensure new food doesn't appear on the snake
            while True:
                food.randomize_position()
                if food.position not in snake.positions:
                    break

        # --- Drawing ---
        screen.fill(config.BLACK)
        # draw_grid(screen)  # Uncomment to see grid lines
        snake.draw(screen)
        food.draw(screen)

        # Draw score
        score_surf = font.render(f"Score: {score}", True, config.WHITE)
        screen.blit(score_surf, (10, 10))

        pygame.display.flip()

    # Game over screen
    game_over(screen, score, font)

    pygame.quit()
    sys.exit()


def game_over(screen, score, font):
    """Display a simple game‑over screen."""
    screen.fill(config.BLACK)
    over_text = font.render("Game Over", True, config.RED)
    score_text = font.render(f"Final Score: {score}", True, config.WHITE)
    prompt_text = font.render("Press any key to exit", True, config.WHITE)

    screen.blit(over_text, (config.WIDTH // 2 - over_text.get_width() // 2, config.HEIGHT // 3))
    screen.blit(score_text, (config.WIDTH // 2 - score_text.get_width() // 2, config.HEIGHT // 2))
    screen.blit(prompt_text, (config.WIDTH // 2 - prompt_text.get_width() // 2, config.HEIGHT * 2 // 3))
    pygame.display.flip()

    # Wait for any key or quit event
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN):
                waiting = False
                break


if __name__ == "__main__":
    main()
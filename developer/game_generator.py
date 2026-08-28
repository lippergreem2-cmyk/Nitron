import os

PROJECTS = os.path.expanduser("~/Nitron/generated_projects")

os.makedirs(PROJECTS, exist_ok=True)


def create_game(name):

    folder = os.path.join(
        PROJECTS,
        name.replace(" ", "_").lower()
    )

    os.makedirs(folder, exist_ok=True)

    code = '''import pygame
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nitron Game")

clock = pygame.time.Clock()

x = 100
y = 100
speed = 5

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= speed

    if keys[pygame.K_RIGHT]:
        x += speed

    if keys[pygame.K_UP]:
        y -= speed

    if keys[pygame.K_DOWN]:
        y += speed

    screen.fill((30,30,30))

    pygame.draw.rect(
        screen,
        (0,255,255),
        (x,y,50,50)
    )

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
'''

    with open(
        os.path.join(folder, "main.py"),
        "w"
    ) as file:

        file.write(code)

    return f"Game '{name}' created successfully in {folder}."


def snake():

    return create_game("Snake")


def platformer():

    return create_game("Platformer")


def racing():

    return create_game("Racing")


def shooter():

    return create_game("Shooter")

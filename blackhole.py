"""
blackhole.py
A stylized black hole simulator: particles orbiting a massive central body,
using simplified Newtonian gravity. Educational visualization, not a
physically exact simulation.
"""

import pygame
import numpy as np
import random

pygame.init()
WIDTH, HEIGHT = 800, 800
CENTER = np.array([WIDTH / 2, HEIGHT / 2])
G = 6.674e-3       # scaled gravitational constant (not real-world units)
M = 2000           # mass of the black hole (arbitrary units)
DT = 0.2

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Black Hole Simulator")
clock = pygame.time.Clock()


class Particle:
    def __init__(self):
        angle = random.uniform(0, 2 * np.pi)
        dist = random.uniform(150, 350)
        self.pos = CENTER + dist * np.array([np.cos(angle), np.sin(angle)])
        # Roughly circular orbital velocity, perpendicular to radius vector
        speed = np.sqrt(G * M / dist) * random.uniform(0.8, 1.2)
        direction = np.array([-np.sin(angle), np.cos(angle)])
        self.vel = speed * direction
        self.trail = []

    def update(self):
        r_vec = CENTER - self.pos
        r = np.linalg.norm(r_vec)
        if r < 20:  # fell past event horizon
            return False
        accel = G * M / (r ** 2) * (r_vec / r)
        self.vel += accel * DT
        self.pos += self.vel * DT
        self.trail.append(self.pos.copy())
        if len(self.trail) > 100:
            self.trail.pop(0)
        return True


particles = [Particle() for _ in range(150)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Event horizon
    pygame.draw.circle(screen, (30, 30, 30), CENTER.astype(int), 20)

    alive_particles = []
    for p in particles:
        if p.update():
            alive_particles.append(p)
            for i, pos in enumerate(p.trail):
                alpha = int(255 * (i / len(p.trail)))
                color = (min(255, alpha), min(150, alpha // 2), 0)
                pygame.draw.circle(screen, color, pos.astype(int), 1)
            pygame.draw.circle(screen, (255, 200, 100), p.pos.astype(int), 2)
    particles = alive_particles

    # Replenish particles that fell in, so the sim keeps going
    while len(particles) < 150:
        particles.append(Particle())

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

import os
import random
import pygame


WIDTH = 960
HEIGHT = 750
CELL = 30
pygame.init()
running = True
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
LIGHT = (60, 120, 80)
DARK = (35, 75, 50)

def draw_checkerboard():
    for col in range(WIDTH // CELL):
        for row in range(HEIGHT // CELL):
            x = col * CELL
            y = row * CELL
            if (col + row) % 2 == 0:
                color = LIGHT
            else:
                color = DARK
            pygame.draw.rect(screen, color, (x, y, CELL, CELL))




while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw_checkerboard()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()

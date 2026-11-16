import os
import random
import pygame

WIDTH = 960
HEIGHT = 760
pygame.init()
running = True
screen = pygame.display.set_mode((WIDTH, HEIGHT))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()

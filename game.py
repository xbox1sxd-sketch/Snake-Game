import random

import pygame

WIDTH = 960
HEIGHT = 720
CELL = 48
pygame.init()
running = True
game_over = False
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
LIGHT = (60, 120, 80)
DARK = (35, 75, 50)
SNAKE_COLOR = (180, 255, 120)
HEAD_COLOR = (0,0,0)
snake = [[5,5], [4,5], [3, 5]]
direction = [1,0]
move_delay = 150
last_move_time = 0
food = [15, 10]
FOOD_COLOR =(255, 80, 80)
WALL_COLOR = (20, 40, 30)

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

def draw_snake():
    for i in range(len(snake)):
        part = snake[i]
        x = part[0] * CELL
        y = part[1] * CELL
        if i == 0:
            color = HEAD_COLOR
        else:
            color = SNAKE_COLOR
        pygame.draw.rect(screen, color, (x, y, CELL, CELL))
        
def draw_food():
    x = food[0] * CELL
    y = food[1] * CELL
    pygame.draw.rect(screen, FOOD_COLOR, (x, y, CELL, CELL))

def draw_wall():
    pygame.draw.rect(screen, WALL_COLOR, (0, 0, WIDTH, HEIGHT), 12)



def move_snake():
    global food, game_over
    head = snake[0]
    new_head = [head[0] + direction[0], head[1] + direction[1]]
    if new_head[0] < 0 or new_head[0] >= 20 or new_head[1] < 0 or new_head[1] >= 15:
        game_over = True
        return
    if new_head in snake:
        game_over = True
        return
    snake.insert(0, new_head)
    if new_head == food:
        food = [random.randint(0, 19), random.randint(0, 14)]
    else:
        snake.pop()
        

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != [0, 1]:
                direction = [0, -1]
            elif event.key == pygame.K_DOWN and direction != [0, -1]:
                direction = [0, 1]
            elif event.key == pygame.K_LEFT and direction != [1, 0]:
                direction = [-1, 0]
            elif event.key == pygame.K_RIGHT and direction != [-1, 0]:
                direction = [1, 0]
    current_time = pygame.time.get_ticks()
    if not game_over and current_time - last_move_time > move_delay:
        move_snake()
        last_move_time = current_time                 
    draw_checkerboard()
    draw_snake()
    draw_food()
    draw_wall()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()

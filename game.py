import os
import random

import pygame

score = 0
OFFSET = 12
WIDTH = 960 + OFFSET * 2
HEIGHT = 720 + OFFSET * 2
CELL = 48
pygame.init()
running = True
difficulty = "Normal"
base_speed = 140
pillar_count = 9
in_menu = True
big_font = pygame.Font(None, 100)
game_over = False
paused = False
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
clock = pygame.time.Clock()
font = pygame.Font(None, 40)
LIGHT = (60, 120, 80)
DARK = (35, 75, 50)
SNAKE_COLOR = (180, 255, 120)
HEAD_COLOR = (0,255,200)
snake = [[5,5, SNAKE_COLOR], [4,5, SNAKE_COLOR], [3, 5, SNAKE_COLOR]]
direction = [1,0]
next_direction = [1,0]
is_fullscreen = False
last_move_time = 0
highscore = 0
death_font = pygame.Font(None, 55)
can_change_direction = True
ghost_pos = [-1, -1]
ghost_timer = 0
ghost_spawn_time = pygame.time.get_ticks() + random.randint(20000, 45000)
ghost_font = pygame.Font(None, 30)
pause_start_time = 0

oops_messages = [
    "oops",
    "You died",
    ":(",
    "???",
    "Well that was silly",
    "Defeat.",
    "Try harder next time",
    "Did you get that on camera?",
    "What did you do that for!",
    "You lived a good life",
    "Silly goose!",
    "WASTED"
]

insult_messages = [
    "Have you tried dodging?",
    "Now thats just humiliating",
    "Thats all you can do? ;-;",
    "Who writes these messages",
    "Whelp",
    "Better luck next time",
    "You gave it your all",
    "Git Gud",
]
death_title = ""
death_insult = ""

#godot so much better for colors
FOOD_COLORS =[
    (200, 0, 0),
    (255, 255, 0),
    (255, 165, 0),
    (0, 100, 255),
    (150, 32, 240)
]
WALL_COLOR = (20, 40, 30)

# Creates pillars (just black boxes) that if you run into you die
def make_pillars():
    global pillars
    pillars = []
    while len(pillars) < pillar_count:
        p = [random.randint(1, 18), random.randint(1, 13)]
        if p[0] >= 2 and p[0] <= 8 and p[1] >= 3 and p[1] <= 7:
            continue
        too_close = False
        for existing in pillars:
            if abs(p[0] - existing[0]) <= 2 and abs(p[1] - existing[1]) <= 2:
                too_close = True
        if p not in [s[:2] for s in snake] and p not in pillars and not too_close:
            pillars.append(p)

make_pillars()

# Draws the backround
def draw_checkerboard():
    for col in range(WIDTH // CELL):
        for row in range(HEIGHT // CELL):
            x = col * CELL + OFFSET
            y = row * CELL + OFFSET
            if (col + row) % 2 == 0:
                color = LIGHT
            else:
                color = DARK
            pygame.draw.rect(screen, color, (x, y, CELL, CELL))

#Goes throught the snake list, if the first item is index 0 it draws the head cyan and draws the eyes.
def draw_snake():
    for i in range(len(snake)):
        part = snake[i]
        x = part[0] * CELL + OFFSET
        y = part[1] * CELL + OFFSET
        if i == 0:
            color = HEAD_COLOR
        else:
            color = part[2]
        pygame.draw.rect(screen, color, (x, y, CELL, CELL))
        if i == 0:
            if direction == [1, 0]:
                pygame.draw.circle(screen, (0, 0, 0), (x + 35, y + 14), 5)    
                pygame.draw.circle(screen, (0, 0, 0), (x + 35, y + 34), 5)
            elif direction == [-1, 0]:
                pygame.draw.circle(screen, (0, 0, 0), (x + 13, y + 14), 5)
                pygame.draw.circle(screen, (0, 0, 0), (x + 13, y + 34), 5)
            elif direction == [0, -1]:
                pygame.draw.circle(screen, (0, 0, 0), (x + 14, y + 13), 5)
                pygame.draw.circle(screen, (0, 0, 0), (x + 34, y + 13), 5)
            elif direction == [0, 1]:
                pygame.draw.circle(screen, (0, 0, 0), (x + 14, y + 35), 5)
                pygame.draw.circle(screen, (0, 0, 0), (x + 34, y + 35), 5)
                    
#Draws a square with whatever is stored in food_color
def draw_food():
    x = food[0] * CELL + OFFSET
    y = food[1] * CELL + OFFSET
    pygame.draw.rect(screen, food_color, (x, y, CELL, CELL))
       
#If the ghost powerup is on the board it draws a square, and if the ghost timer is active it calculated how many seconds are left.     
def draw_ghost():
    if ghost_pos[0] != -1:
        x = ghost_pos[0] * CELL + OFFSET
        y = ghost_pos[1] * CELL + OFFSET
        pygame.draw.rect(screen, (200, 100, 255), (x, y, CELL, CELL ))
    if pygame.time.get_ticks() < ghost_timer:
        time_left = int((ghost_timer - pygame.time.get_ticks()) /1000) + 1
        ghost_text = ghost_font.render(f"GHOST: {time_left}s", True, (200, 100, 255))
        screen.blit(ghost_text, (WIDTH - 250, 60))

#Draws a border around the screen
def draw_wall():
    pygame.draw.rect(screen, WALL_COLOR, (0, 0, WIDTH, HEIGHT), 12)

#Finds a good place to spawn the food, using a while true loop to keep picking random grid spots
def spawn_food():
    while True:
        position = [random.randint(1, 18), random.randint(1, 13)]
        in_pillar = False
        for p in pillars:
            if p[0] == position[0] and p[1] == position[1]:
                in_pillar = True
        in_snake = False
        for s in snake:
            if s[0] == position[0] and s[1] == position[1]:
                in_snake = True
        if in_pillar == False and in_snake == False and position != ghost_pos:
            return position
food = spawn_food()
food_color = random.choice(FOOD_COLORS)

#Loops through the pillars list and draws a black square at each position
def draw_pillars():
    for p in pillars:
        pygame.draw.rect(screen, (0, 0, 0), (p[0] * CELL + OFFSET, p[1] * CELL + OFFSET, CELL, CELL))
    
#The biggest one, calculates where the head will be, if it hits something, if it eats something, and if we got a powerup
def move_snake():
    global food, game_over, direction, next_direction, food_color, score, highscore, death_title, death_insult, ghost_pos, ghost_timer, ghost_spawn_time  # noqa: PLW0602
    direction = next_direction
    head = snake[0]
    new_head = [head[0] + direction[0], head[1] + direction[1], SNAKE_COLOR]
    if new_head[0] < 0 or new_head[0] >= 20 or new_head[1] < 0 or new_head[1] >= 15:
        end_game()
        return
    for p in pillars:
        if new_head[0] == p[0] and new_head[1] == p[1] and pygame.time.get_ticks() >= ghost_timer:
            end_game()        
            return
    ate_food = new_head[:2] == food
    if ate_food:
        body_to_check = snake
    else:
        body_to_check = snake[:-1]
    hit_self = False
    for s in body_to_check:
        if s[0] == new_head[0] and s[1] == new_head[1]:
            hit_self = True
    if hit_self:
        end_game()     
        return

    snake.insert(0, new_head)
    if ate_food:
        new_head[2] = food_color
        food = spawn_food()
        food_color = random.choice(FOOD_COLORS)
        score += 1
    else:
        snake.pop()
    if new_head[0] == ghost_pos[0] and new_head[1] == ghost_pos[1]:
        ghost_timer = pygame.time.get_ticks() + 5000
        ghost_pos = [-1, -1]
        ghost_spawn_time = pygame.time.get_ticks() + random.randint(20000, 45000)

# Draws the text in the top left and right. Also uses offset to make sure it doesnt hit the wall.
def draw_score():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20 + OFFSET, 15 + OFFSET)) #used ai for just this line
    hs_text = font.render(f"High Score: {highscore}", True, (255, 215, 0))
    screen.blit(hs_text, (WIDTH - 250 - OFFSET, 15 + OFFSET))

def end_game():
    global game_over, highscore, death_title, death_insult
    game_over = True
    if score > highscore:
        highscore = score
        save_highscore(highscore)
    death_title = random.choice(oops_messages)
    death_insult = random.choice(insult_messages)

#If it finds highscore.txt if reads the number, and if there isnt a number it just returns zero
#Used ai for this function
def load_highscore():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            try:
                return int(f.read())
            except ValueError:
                return 0
    else:
        return 0

#Opens the highscore file and writes the new number into it
def save_highscore(hs):
    with open("highscore.txt", "w") as f:
        f.write(str(hs))
        
highscore = load_highscore()

#Controls everything, inputs, the backround, restarts, colors and more
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not in_menu and not game_over and not paused:
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != [0, 1]  and can_change_direction:
                    next_direction = [0, -1]
                    can_change_direction = False
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != [0, -1]  and can_change_direction:
                    next_direction = [0, 1]
                    can_change_direction = False
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != [1, 0]  and can_change_direction:
                    next_direction = [-1, 0]
                    can_change_direction = False
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != [-1, 0]  and can_change_direction:
                    next_direction = [1, 0]
                    can_change_direction = False
            if in_menu:
                if event.key == pygame.K_1:
                    difficulty = "Easy"
                    base_speed = 170
                    pillar_count = 5
                elif event.key == pygame.K_2:
                    difficulty = "Normal"
                    base_speed = 140
                    pillar_count = 9
                elif event.key == pygame.K_3:
                    difficulty = "Hard"
                    base_speed = 110
                    pillar_count = 14
            if event.key == pygame.K_SPACE and in_menu:
                in_menu = False
                last_move_time = pygame.time.get_ticks()
                can_change_direction = True
                make_pillars()
                food = spawn_food()
                food_color = random.choice(FOOD_COLORS)
            if event.key == pygame.K_p and not in_menu and not game_over:
                if paused == False:
                    paused = True
                    pause_start_time = pygame.time.get_ticks()
                else:
                    paused = False
                    pause_duration = pygame.time.get_ticks() - pause_start_time
                    if ghost_timer > pause_start_time:
                        ghost_timer = ghost_timer + pause_duration
                    ghost_spawn_time = ghost_spawn_time + pause_duration
                    last_move_time = pygame.time.get_ticks()
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
                is_fullscreen = not is_fullscreen
            if (event.key == pygame.K_r or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE) and game_over:
                game_over = False
                snake = [[5,5, SNAKE_COLOR ], [4, 5, SNAKE_COLOR], [3, 5, SNAKE_COLOR]]
                direction = [1,0]
                next_direction = [1,0]
                score = 0
                can_change_direction = True
                last_move_time = pygame.time.get_ticks()
                make_pillars()
                ghost_pos = [-1, -1]
                ghost_timer = 0
                ghost_spawn_time = pygame.time.get_ticks() + random.randint(20000, 45000)
                food = spawn_food()
                food_color = random.choice(FOOD_COLORS)
    move_delay = base_speed - (len(snake) * 2)

    move_delay = max(move_delay, 60)
    if ghost_pos[0] == -1 and pygame.time.get_ticks() > ghost_spawn_time and not in_menu and not game_over and not paused:
        bad_spot = True
        while bad_spot:
            ghost_pos = [random.randint(1, 18), random.randint(1, 13)]
            bad_spot = False
            if ghost_pos == food:
                bad_spot = True
            for s in snake:
                if s[:2] == ghost_pos:
                    bad_spot = True
            for p in pillars:
                if p == ghost_pos:
                    bad_spot = True
    current_time = pygame.time.get_ticks()
    if not in_menu and not game_over and not paused and current_time - last_move_time >= move_delay:
        move_snake()
        can_change_direction = True
        last_move_time = current_time                 
    draw_checkerboard()
    draw_snake()
    draw_food()
    draw_ghost()
    draw_pillars()
    draw_wall()
    draw_score()
    if in_menu:
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
        text = big_font.render("SNAKE GAME", True, (255, 255, 255))
        screen.blit(text, (280, 250))
        text2 = font.render("Press SPACE to start", True, (255, 255, 0))
        screen.blit(text2, (370, 400))
        text3 = font.render("WASD or Arrow keys to move", True, (150, 150, 150))
        screen.blit(text3, (340, 480))
        text4 = font.render("P to pause", True, (150, 150, 150))
        screen.blit(text4, (420, 530))
        text5 = font.render("F11 to Fullscreen", True, (150, 150, 150))
        screen.blit(text5, (385, 580))
        text6 = font.render(f"Difficulty (1, 2, 3): {difficulty}", True, (255, 255, 255))
        screen.blit(text6, (100, 700))
    if game_over:
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
        text = death_font.render(death_title, True, (255, 80, 80))
        screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 80))
        text2 = font.render(death_insult, True, (255, 255, 255))
        screen.blit(text2, (WIDTH // 2 - 150, HEIGHT // 2 + 10))
        text3 = font.render("Press ENTER to restart", True, (150, 150, 150))
        screen.blit(text3, (WIDTH // 2 - 155, HEIGHT // 2 + 80))
    if paused:
        pygame.draw.rect(screen, (20, 30, 50), (0, 0, WIDTH, HEIGHT))
        text = big_font.render("PAUSED", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - 155, HEIGHT // 2 - 80))
        text2 = font.render("Press P to resume", True, (150, 150, 150))
        screen.blit(text2, (WIDTH // 2 - 130, HEIGHT // 2 + 30))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()

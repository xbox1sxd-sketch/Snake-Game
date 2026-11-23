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
last_move_time = 0
highscore = 0
death_font = pygame.Font(None, 55)
can_change_direction = True
ghost_pos = [-1, -1]
ghost_timer = 0
ultimate_pos = [-1, -1]
ultimate_timer = 0
ultimate_spawn_time = pygame.time.get_ticks() + random.randint(60000, 120000)
ghost_spawn_time = pygame.time.get_ticks() + random.randint(20000, 45000)
ghost_font = pygame.Font(None, 30)
double_points_pos = [-1, -1]
double_points_timer = 0
double_points_spawn_time = pygame.time.get_ticks() + random.randint(45000, 75000)
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
    "WASTED",
    "Cmon I gave ya powerups!"
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
    "Get better"
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
    if food is not None:
        x = food[0] * CELL + OFFSET
        y = food[1] * CELL + OFFSET
        pygame.draw.rect(screen, food_color, (x, y, CELL, CELL))
       
#If the ghost powerup is on the board it draws a square, and if the ghost timer is active it calculated how many seconds are left.     
def draw_ghost():
    if ghost_pos[0] != -1:
        x = ghost_pos[0] * CELL + OFFSET
        y = ghost_pos[1] * CELL + OFFSET
        pygame.draw.rect(screen, (200, 100, 255), (x, y, CELL, CELL ))
    if paused:
        current_time = pause_start_time
    else:
        current_time = pygame.time.get_ticks()
    if current_time < ghost_timer:
        time_left = int((ghost_timer - current_time) /1000) + 1
        ghost_text = ghost_font.render(f"GHOST: {time_left}s", True, (200, 100, 255))
        screen.blit(ghost_text, (WIDTH - 250, 60))

def draw_ultimate():
    if ultimate_pos[0] != -1:
        x = ultimate_pos[0] * CELL + OFFSET
        y = ultimate_pos[1] * CELL + OFFSET
        pygame.draw.rect(screen, (255, 215, 0), (x, y, CELL, CELL ))
    if paused:
        current_time = pause_start_time
    else:
        current_time = pygame.time.get_ticks()
    if current_time < ultimate_timer:
        time_left = int((ultimate_timer - current_time)/ 1000) + 1
        ultimate_text = ghost_font.render(f"ULTIMATE POWERUP: {time_left}s", True, (255, 215, 0))
        screen.blit(ultimate_text, (WIDTH - 250, 110))

def draw_double_point():
    if double_points_pos[0] != -1:
        x = double_points_pos[0] * CELL + OFFSET
        y = double_points_pos[1] * CELL + OFFSET
        pygame.draw.rect(screen, (255, 80, 180), (x, y, CELL, CELL))
    if paused:
        current_time = pause_start_time
    else:
        current_time = pygame.time.get_ticks()
    if current_time < double_points_timer:
        time_left = int((double_points_timer - current_time)/ 1000) + 1
        double_text = ghost_font.render(f"DOUBLE POINTS:{time_left}s", True, (255, 80, 100))
        screen.blit(double_text, (WIDTH - double_text.get_width() - 20, 160))

#Draws a border around the screen
def draw_wall():
    pygame.draw.rect(screen, WALL_COLOR, (0, 0, WIDTH, HEIGHT), 12)

def get_free_cells(ignore = None):
    free_cells = []
    for x in range(1, 19):
        for y in range(1, 14):
            spot = [x, y]
            if spot not in [s[:2] for s in snake] and spot not in pillars:  # noqa: SIM102
                if spot != ghost_pos and spot != ultimate_pos and spot != double_points_pos and spot != ignore:
                    free_cells.append(spot)
    return free_cells

#Finds a good place to spawn the food, using a while true loop to keep picking random grid spots
def spawn_food():
    available = get_free_cells()
    if len(available) > 0:
        return random.choice(available)
    return None
food = spawn_food()
food_color = random.choice(FOOD_COLORS)

def spawn_ghost():
    available = get_free_cells(ignore = food)
    if len(available) > 0:
        return random.choice(available)
    return None

def spawn_ultimate():
    available = get_free_cells(ignore = food)
    if len(available) > 0:
        return random.choice(available)
    return None

def spawn_double_points():
    available = get_free_cells(ignore = food)
    if len(available) > 0:
        return random.choice(available)
    return None

#Loops through the pillars list and draws a black square at each position
def draw_pillars():
    for p in pillars:
        pygame.draw.rect(screen, (0, 0, 0), (p[0] * CELL + OFFSET, p[1] * CELL + OFFSET, CELL, CELL))
    
#The biggest one, calculates where the head will be, if it hits something, if it eats something, and if we got a powerup
def move_snake():
    global food, game_over, direction, next_direction, food_color, score, highscore, death_title, death_insult, ghost_pos, ghost_timer, ghost_spawn_time, ultimate_pos, ultimate_timer, ultimate_spawn_time, double_points_pos, double_points_timer, double_points_spawn_time  # noqa: PLW0602
    direction = next_direction
    head = snake[0]
    new_head = [head[0] + direction[0], head[1] + direction[1], SNAKE_COLOR]
    if new_head[0] < 0 or new_head[0] >= 20 or new_head[1] < 0 or new_head[1] >= 15:
        end_game()
        return
    for p in pillars:
        if new_head[0] == p[0] and new_head[1] == p[1] and pygame.time.get_ticks() >= ghost_timer and pygame.time.get_ticks() >= ultimate_timer:
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
    if hit_self and pygame.time.get_ticks() >= ultimate_timer:
        end_game()     
        return

    snake.insert(0, new_head)
    if ate_food:
        new_head[2] = food_color
        food = spawn_food()
        food_color = random.choice(FOOD_COLORS)
        if pygame.time.get_ticks() < double_points_timer:
            score += 2
        else:
            score += 1
    else:
        snake.pop()
    if new_head[0] == ghost_pos[0] and new_head[1] == ghost_pos[1]:
        ghost_timer = pygame.time.get_ticks() + 5000
        ghost_pos = [-1, -1]
        ghost_spawn_time = pygame.time.get_ticks() + random.randint(20000, 45000)
    if new_head[0] == ultimate_pos[0] and new_head[1] == ultimate_pos[1]:
        ultimate_timer = pygame.time.get_ticks() + 20000
        ultimate_pos = [-1, -1]
        ultimate_spawn_time = pygame.time.get_ticks() + random.randint(60000, 120000)
    if new_head[0] == double_points_pos[0] and new_head[1] == double_points_pos[1]:
        double_points_timer = pygame.time.get_ticks() + 10000
        double_points_pos = [-1, -1]
        double_points_spawn_time = pygame.time.get_ticks() + random.randint(60000, 75000)

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
    try:
        with open("highscore.txt", "r") as f:
                return int(f.read())
    except:  # noqa: E722
        return 0

#Opens the highscore file and writes the new number into it
def save_highscore(hs):
    try:
        with open("highscore.txt", "w") as f:
            f.write(str(hs))
    except:  # noqa: E722, S110
        pass
        
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
                double_points_pos = [-1, -1]
                double_points_timer = 0
                double_points_spawn_time = pygame.time.get_ticks() + random.randint(45000, 75000)
                food = spawn_food()
                food_color = random.choice(FOOD_COLORS)
                ghost_spawn_time = pygame.time.get_ticks() + random.randint(20000, 45000)
                ultimate_pos = [-1, -1]
                ultimate_timer = 0
                ultimate_spawn_time = pygame.time.get_ticks() + random.randint(60000, 120000)
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
                    if ultimate_timer > pause_start_time:
                        ultimate_timer = ultimate_timer + pause_duration
                    ultimate_spawn_time = ultimate_spawn_time + pause_duration
                    if double_points_timer > pause_start_time:
                        double_points_timer = double_points_timer + pause_duration
                    double_points_spawn_time = double_points_spawn_time + pause_duration
            if (event.key == pygame.K_r or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE) and game_over:
                game_over = False
                snake = [[5,5, SNAKE_COLOR ], [4, 5, SNAKE_COLOR], [3, 5, SNAKE_COLOR]]
                direction = [1,0]
                next_direction = [1,0]
                score = 0
                can_change_direction = True
                last_move_time = pygame.time.get_ticks()
                make_pillars()
                double_points_pos = [-1, -1]
                double_points_timer = 0
                double_points_spawn_time = pygame.time.get_ticks() + random.randint(45000, 75000)
                ghost_pos = [-1, -1]
                ghost_timer = 0
                ghost_spawn_time = pygame.time.get_ticks() + random.randint(20000, 45000)
                food = spawn_food()
                food_color = random.choice(FOOD_COLORS)
                ultimate_pos = [-1, -1]
                ultimate_timer = 0
                ultimate_spawn_time = pygame.time.get_ticks() + random.randint(60000, 120000)
    move_delay = base_speed - (len(snake) * 2)
    if pygame.time.get_ticks() < ultimate_timer:
        move_delay = move_delay - 40
    move_delay = max(move_delay, 20)
    current_time = pygame.time.get_ticks()
    if not in_menu and not game_over and not paused and current_time - last_move_time >= move_delay:
        move_snake()
        if not game_over:
            can_change_direction = True
        last_move_time = current_time
    if ghost_pos[0] == -1 and pygame.time.get_ticks() > ghost_spawn_time and not in_menu and not game_over and not paused:
        new_ghost = spawn_ghost()
        if new_ghost is not None:
            ghost_pos = new_ghost 
    if ultimate_pos[0] == -1 and pygame.time.get_ticks() > ultimate_spawn_time and not in_menu and not game_over and not paused:
        new_ultimate = spawn_ultimate()
        if new_ultimate is not None:
            ultimate_pos = new_ultimate
    if double_points_pos[0] == -1 and pygame.time.get_ticks() > double_points_spawn_time and not in_menu and not game_over and not paused:
        new_double_points = spawn_double_points()
        if new_double_points is not None:
            double_points_pos = new_double_points
    draw_checkerboard()
    draw_pillars()
    draw_food()
    draw_snake()
    draw_ghost()
    draw_ultimate()
    draw_double_point()
    draw_wall()
    draw_score()
    if in_menu:
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
        text = big_font.render("SNAKE GAME", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=(WIDTH// 2, 250)))
        text2 = font.render("Press SPACE to start", True, (255, 255, 0))
        screen.blit(text2,text2.get_rect(center =(WIDTH// 2, 400)))
        text3 = font.render("WASD or Arrow keys to move", True, (150, 150, 150))
        screen.blit(text3, text3.get_rect(center =(WIDTH// 2, 480)))
        text4 = font.render("P to pause", True, (150, 150, 150))
        screen.blit(text4, text4.get_rect(center =(WIDTH // 2, 530)))
        text6 = font.render(f"Difficulty (1, 2, 3): {difficulty}", True, (255, 255, 255))
        screen.blit(text6, text6.get_rect(center = (WIDTH // 2, 700)))
    if game_over:
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
        text = death_font.render(death_title, True, (255, 80, 80))
        screen.blit(text, text.get_rect(center=(WIDTH // 2 , HEIGHT // 2 - 80)))
        text2 = font.render(death_insult, True, (255, 255, 255))
        screen.blit(text2, text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10)))
        text3 = font.render("Press ENTER to restart", True, (150, 150, 150))
        screen.blit(text3, text3.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80)))
    if paused:
        pygame.draw.rect(screen, (20, 30, 50), (0, 0, WIDTH, HEIGHT))
        text = big_font.render("PAUSED", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80)))
        text2 = font.render("Press P to resume", True, (150, 150, 150))
        screen.blit(text2, text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()

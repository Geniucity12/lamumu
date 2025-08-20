import pygame, random
pygame.init()
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('background.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)


white = (255, 255, 255)
black = (0,0,0)
gray = (128,128,128)
green = (34, 139, 34)
red = ((255, 0, 0))
WIDTH = 600
HEIGHT = 800
background = white


player = pygame.image.load('peel.png') 
fps = 60
font = pygame.font.Font('FreeSansBold.ttf', 16)
timer = pygame.time.Clock()

score = 0
high_score = 0
game_over = False

player_x = 230
player_y = 600

# platforms = [[252, 720, 80, 10], [135, 595, 70, 10], [400, 595, 70, 10], [252, 420, 80, 10], [135, 300, 70, 10], [400, 300, 70, 10], [252, 100, 80, 10]]
platforms = [
    [252, 720, 80, 10],  # center bottom
    [120, 560, 70, 10],  # left
    [410, 560, 70, 10],  # right (same height as left for the “8” look)
    [252, 400, 80, 10],  # center middle
    [120, 240, 70, 10],  # left
    [410, 240, 70, 10],  # right (same height as left again)
    [252, 80, 80, 10],   # center top
]

jump = False
y_change = 0
x_change = 0
player_speed = 3
score_last = 0
super_jumps = 2
jump_last = 0

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('P33LS JUMPER')

def generate_platform(existing_platforms, player_y):
    x_positions = [120, 252, 410]
    width_choices = {120: 70, 252: 80, 410: 70}

    highest_y = min(p[1] for p in existing_platforms)

    max_jump_height = 150  # adjust based on your jump physics

    min_new_y = max(player_y - max_jump_height, highest_y - 180)
    max_new_y = highest_y - 140

    min_y = int(min_new_y)
    max_y = int(max_new_y)
    if min_y > max_y:
        min_y, max_y = max_y, min_y

    new_y = random.randint(min_y, max_y)

    tries = 0
    while tries < 10:
        new_x = random.choice(x_positions)
        too_close = False
        for p in existing_platforms:
            if abs(p[1] - new_y) < 40 and abs(p[0] - new_x) < 100:
                too_close = True
                break
        if not too_close:
            break
        tries += 1

    new_width = width_choices[new_x]
    return [new_x, new_y, new_width, 10]




def check_collisions(rect_list, j):
    global player_x
    global player_y
    global y_change
    for i in range(len(rect_list)):
        if rect_list[i].colliderect([player_x, player_y + 60, 125, 40]) and jump == False and y_change > 0:
            j = True
    return j

def update_player(y_pos):
    global jump
    global y_change
    jump_height = 15
    gravity = 0.6
    if jump:
        y_change = -jump_height
        jump = False
    y_pos += y_change
    y_change += gravity
    return y_pos



def update_platforms(my_list, player_y, change):
    global score 
    if player_y < 250 and change < 0:
        for i in range(len(my_list)):
            my_list[i][1] -= change

        for i in range(len(my_list)):
            if my_list[i][1] > HEIGHT:
                my_list[i] = generate_platform(my_list, player_y)
                score += 1
    return my_list




running = True
while running == True:
    timer.tick(fps)
    screen.fill(background)
    screen.blit(player, (player_x, player_y))
    blocks = []
    score_text = font.render('Highest P33L: ' + str(high_score), True, black, background)
    screen.blit(score_text, (465, 30))
    high_score_text = font.render('P33L: ' + str(score), True, black, background)
    screen.blit(high_score_text, (465, 50))

    score_text = font.render('Air Jumps (Spacebar): ' + str(super_jumps), True, black, background)
    screen.blit(score_text, (30, 30))
    # if game_over:
    #     game_over_text = font.render('YOU GOT P33LED (Spacebar restart) ' + str(score), True, red, background)
    #     screen.blit(game_over_text, (200, 380))
    if game_over:
        big_font = pygame.font.Font('FreeSansBold.ttf', 28)  # Larger font size
        game_over_text = big_font.render('YOU GOT P33LED (Spacebar restart)', True, red, background)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 380))  # Centered horizontally


    for i in range(len(platforms)):
        block = pygame.draw.rect(screen, black, platforms[i], 0,3)
        blocks.append(block)

    for event in pygame.event.get():
        if event.type ==  pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                game_over = False
                score = 0
                player_x = 230
                player_y = 600
                background = white
                score_last = 0
                super_jumps = 2
                jump_last = 0
                platforms = [
                            [252, 720, 80, 10],  # center bottom
                            [120, 560, 70, 10],  # left
                            [410, 560, 70, 10],  # right (same height as left for the “8” look)
                            [252, 400, 80, 10],  # center middle
                            [120, 240, 70, 10],  # left
                            [410, 240, 70, 10],  # right (same height as left again)
                            [252, 80, 80, 10],]   # center top
            if event.key == pygame.K_SPACE and not game_over and super_jumps > 0:
                super_jumps -=1
                y_change = -25
            if event.key == pygame.K_a:
                x_change = - player_speed
            if event.key == pygame.K_d:
                x_change =  player_speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                x_change = 0
            if event.key == pygame.K_d:
                x_change =  0
            

    jump = check_collisions(blocks, jump)
    player_y = update_player(player_y)

    if player_y < 750:
        player_x += x_change
    else: 
        game_over = True
        y_change = 0
        x_change = 0

    platforms = update_platforms(platforms, player_y, y_change)
    # player_x = max(0, min(player_x, WIDTH - player.get_width()))

    if player_x < -30:
        player_x = -30
    elif player_x > 530:
        player_x = 530

    if x_change > 0:
        player = pygame.image.load('peel.png')
    elif x_change < 0:

        player = pygame.transform.flip(pygame.image.load('peel.png'), 1, 0)
    if score > high_score:
        high_score = score

    if score - score_last > 15:
        score_last = score
        background = (random.randint(1, 255), random.randint(1, 255),random.randint(1, 255))

    if score - jump_last > 50:
        jump_last = score
        super_jumps += 1
        
    pygame.display.flip()

pygame.quit()
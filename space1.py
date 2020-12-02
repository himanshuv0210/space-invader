import pygame
import random
import math

from pygame import mixer

x1 = pygame.init()
pygame.font.init()

# Creating window
screen_width = 1000
screen_height = 600
gamewindow = pygame.display.set_mode((screen_width, screen_height))

# Title and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo_1.png')
pygame.display.set_icon(icon)
pygame.display.update()

# Background Image
bg = pygame.image.load('background3.png')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)  # for play untill exit game (infinte loop play -1)

# RGB colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Players_coordinates_and_images
player_img = pygame.image.load('spaceship1.png')
player_x = 470
player_y = 500
player_chg = 0
fps = 60
clock = pygame.time.Clock()

# Enemy_coordinates_and_images
enemy_img = []
enemy_x = []
enemy_y = []
enemyx_chg = []
enemyy_chg = []
n_enemies = 20  # Create multiple enemies
for i in range(n_enemies):
    enemy_img.append(pygame.image.load('ufo22.png'))
    enemy_x.append(random.randint(0, 936))
    enemy_y.append(random.randint(30, 300))
    enemyx_chg.append(5)
    enemyy_chg.append(40)
# fps = 60
# clock = pygame.time.Clock()

# Fire a Bullet
# ready = you cant see the bullet on screen
# fire = the bullet  is currently  moving
bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 500
bulletx_chg = 0
bullety_chg = 10
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 5
text_y = 5

# GAMEOVER VARIABLE DEFINE
over_font = pygame.font.Font('freesansbold.ttf', 64)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gamewindow.blit(screen_text, [x, y])


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (white))
    gamewindow.blit(score, (x, y))


def gameover_text(enemyX, enemyY, playerX, playerY):
    distance1 = math.sqrt((math.pow(playerX - enemyX, 2)) + (math.pow(playerY - enemyY, 2)))
    if distance1 < 50:
        return True
    else:
        return False


exitgame = False
gameover = False


def player(x, y):
    gamewindow.blit(player_img, (x, y))


def enemy(x, y, i):
    gamewindow.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    gamewindow.blit(bullet_img, (x + 16, y + 10))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 30:
        return True
    else:
        return False


# Gameloop
while not exitgame:
    if gameover:
        for event in pygame.event.get():
            # print(event)
            if (event.type == pygame.QUIT):
                exitgame = True
    else:

        gamewindow.blit(bg, (0, 0))
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                exitgame = True
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_LEFT):
                    player_chg = -8
                if (event.key == pygame.K_RIGHT):
                    player_chg = 8
                if (event.key == pygame.K_SPACE):
                    if (bullet_state is "ready"):
                        bullet_sound = mixer.Sound('laser.wav')
                        bullet_sound.play()
                        bullet_x = player_x  # Shoot from x coordinate of player
                        fire_bullet(player_x, bullet_y)

        # set the boundaries of player spaceship
        player_x += player_chg
        if (player_x <= 0):
            player_x = 0
        elif player_x >= 936:
            player_x = 936

        # Enemy movement
        for i in range(n_enemies):
            enemy_x[i] += enemyx_chg[i]
            if (enemy_x[i] <= 0):
                enemyx_chg[i] = 5
                enemy_y[i] += enemyy_chg[i]  # change the rows
            elif enemy_x[i] >= 936:
                enemyx_chg[i] = -5
                enemy_y[i] += enemyy_chg[i]  # change the rows

            # Collision
            collision = iscollision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
            if collision:
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                bullet_y = 500
                bullet_state = "ready"
                score_value += 5
                # print(score)
                enemy_x[i] = random.randint(0, 936)
                enemy_y[i] = random.randint(20, 300)

            enemy(enemy_x[i], enemy_y[i], i)

            # Game over
            overgame = gameover_text(enemy_x[i], enemy_y[i], player_x, player_y)
            if overgame:
                over_text = over_font.render("GAME OVER", True, (white))
                gamewindow.blit(over_text, (300, 250))
                gameover = True
            # ------------------------------------------------

        # Bullet Movement
        if (bullet_y <= 0):  # for multiple shoots to enemy
            bullet_y = 500
            bullet_state = "ready"

        if (bullet_state is "fire"):
            fire_bullet(bullet_x, bullet_y)
            bullet_y -= bullety_chg

        player(player_x, player_y)
        show_score(text_x, text_y)
        pygame.display.update()
        clock.tick(fps)

pygame.quit()
quit()

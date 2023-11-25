import pygame
import random
import math

pygame.init()

# Buat screen 
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Tittle and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player 
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 64))
    enemyX_change.append(4)
    enemyY_change.append(32)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bullets = []
for i in range(2):  # Jumlah peluru maksimum yang bisa ditembakkan secara simultan
    bullets.append({"x": 0, "y": 480, "state": "ready"})

bulletY_change = 1

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 10, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                for bullet in bullets:
                    if bullet["state"] == "ready":
                        bullet["x"] = playerX
                        bullet["y"] = playerY
                        bullet["state"] = "fire"
                        break

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 768:
        playerX = 768

    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 768:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        for bullet in bullets:
            collision = isCollision(enemyX[i], enemyY[i], bullet["x"], bullet["y"])
            if collision:
                bullet["y"] = 480
                bullet["state"] = "ready"
                score_value += 1
                enemyX[i] = random.randint(32, 768)
                enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    for bullet in bullets:
        if bullet["state"] == "fire":
            fire_bullet(bullet["x"], bullet["y"])
            bullet["y"] -= bulletY_change

            if bullet["y"] <= 0:
                bullet["state"] = "ready"

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

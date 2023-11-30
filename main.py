import math
import random
import pygame
from pygame import mixer

# Initialize pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invader")

# Load images and sounds
background = pygame.image.load('background.png')
icon = pygame.image.load('enemy.png')
pygame.display.set_icon(icon)

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Sound effects
bullet_sound = mixer.Sound("laser.wav")
explosion_sound = mixer.Sound("explosion.wav")

# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('player.png')
        self.rect = self.image.get_rect()
        self.rect.x = 370
        self.rect.y = 480
        self.x_change = 0
        self.bullets = pygame.sprite.Group()  # Grup untuk melacak peluru
        self.max_bullets = 2  # Batasan jumlah peluru

    def move(self, direction):
        self.x_change = direction

    def shoot(self):
        if len(self.bullets) < self.max_bullets:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            self.bullets.add(bullet)
            bullets.add(bullet)
            bullet_sound.play()  # Mainkan suara tembakan

    def update(self):
        self.rect.x += self.x_change
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x >= 736:
            self.rect.x = 736

        self.bullets.update()

    def draw(self):
        screen.blit(self.image, self.rect)
        self.bullets.draw(screen)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('enemy.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_change = 5
        self.y_change = 40

    def update(self):
        self.rect.x += self.x_change
        if self.rect.x <= 0 or self.rect.x >= 736:
            self.x_change = -self.x_change
            self.rect.y += self.y_change

    def draw(self):
        screen.blit(self.image, self.rect)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('bullet.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y_change = 1

    def update(self):
        self.rect.y -= self.y_change
        if self.rect.y < 0:
            self.kill()

    def draw(self):
        screen.blit(self.image, self.rect)

# Game class
class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = pygame.sprite.Group()
        for _ in range(6):
            enemy = Enemy(random.randint(0, 736), random.randint(50, 150))
            self.enemies.add(enemy)
            all_sprites.add(enemy)
        self.bullet = Bullet(self.player.rect.centerx, self.player.rect.top)
        all_sprites.add(self.player)
        all_sprites.add(self.bullet)
        self.score = 0
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.over_font = pygame.font.Font('freesansbold.ttf', 64)

    def show_score(self):
        score = self.font.render("Score : " + str(self.score), True, (255, 255, 255))
        screen.blit(score, (10, 10))

    def game_over_text(self):
        over_text = self.over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (200, 250))

    def check_collision(self):
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hits:
            return True

        hits = pygame.sprite.groupcollide(self.enemies, bullets, True, True)
        for hit in hits:
            explosion_sound.play()  # Mainkan suara ledakan
            self.score += 1
            enemy = Enemy(random.randint(0, 736), random.randint(50, 150))
            self.enemies.add(enemy)
            all_sprites.add(enemy)

        return False

    def update(self):
        all_sprites.update()

    def draw(self):
        all_sprites.draw(screen)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.move(-4)
                    elif event.key == pygame.K_RIGHT:
                        self.player.move(4)
                    elif event.key == pygame.K_SPACE:
                        self.player.shoot()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.player.move(0)

            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))

            self.update()
            self.draw()

            if self.check_collision():
                self.game_over_text()
                pygame.display.flip()
                pygame.time.wait(2000)
                running = False

            self.show_score()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

# Create an instance of the Game class and run the game
game = Game()
game.run()

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
        self.y_change = 0
        self.max_bullets = 4  # Maximum bullets player can shoot
        self.bullet_cooldown = 0  # Cooldown between shots

    def move(self, direction):
        self.x_change = direction

    def move_up(self, direction):
        self.y_change = direction

    def move_down(self, direction):
        self.y_change = direction

    def shoot(self):
        if self.bullet_cooldown <= 0 and len(bullets) < self.max_bullets:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            bullet_sound.play()
            self.bullet_cooldown = 20  # Set cooldown between shots

    def update(self):
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x >= 736:
            self.rect.x = 736

        if self.rect.y <= 0:
            self.rect.y = 0
        elif self.rect.y >= 536:  # Adjusted limit to avoid going off the screen
            self.rect.y = 536

        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= 1


# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('enemy.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 736)
        self.rect.y = random.randint(50, 150)
        self.x_change = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.y_change = 40

    def update(self):
        self.rect.x += self.x_change
        if self.rect.x <= 0 or self.rect.x >= 736:
            self.x_change = -self.x_change
            self.rect.y += self.y_change

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('bullet.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y -= 5
        if self.rect.y < 0:
            self.kill()

# Game class
class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = pygame.sprite.Group()
        self.spawn_enemies(6)  # Initial number of enemies
        all_sprites.add(self.player)
        self.score = 0
        self.level = 1
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.over_font = pygame.font.Font('freesansbold.ttf', 64)

    def show_score(self):
        score = self.font.render(f"Score: {self.score}   Level: {self.level}", True, (255, 255, 255))
        screen.blit(score, (10, 10))

    def game_over_text(self):
        over_text = self.over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (200, 250))

    def check_collision(self):
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hits:
            return True

        # Check bullet-enemy collisions
        for bullet in bullets:
            enemy_hits = pygame.sprite.spritecollide(bullet, self.enemies, True)
            for enemy in enemy_hits:
                explosion_sound.play()
                self.score += 1
                bullet.kill()

        return False

    def update(self):
        all_sprites.update()

        # Check if the player advances to the next level
        if len(self.enemies) == 0:
            self.level += 1
            self.spawn_enemies(3 * self.level)  # Increase the number of enemies

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
                        game.player.move(-5)
                    elif event.key == pygame.K_RIGHT:
                        game.player.move(5)
                    elif event.key == pygame.K_UP:
                        game.player.move_up(-5)
                    elif event.key == pygame.K_DOWN:
                        game.player.move_down(5)
                    elif event.key == pygame.K_SPACE:
                        game.player.shoot()

                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        game.player.move(0)
                    elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                        game.player.move_up(0)
                        game.player.move_down(0)

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

    def spawn_enemies(self, num_enemies):
        for _ in range(num_enemies):
            enemy = Enemy()
            self.enemies.add(enemy)
            all_sprites.add(enemy)

# Create an instance of the Game class and run the game
game = Game()
game.run()

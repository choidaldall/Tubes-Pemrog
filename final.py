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

# Restart button
restart_button_img = pygame.image.load("restart_button.png")
restart_button_rect = restart_button_img.get_rect(center=(400, 300))

# Game over flag
game_over = False


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
        self.max_bullets = 3  # Maximum bullets player can shoot
        self.bullet_cooldown = 0  # Cooldown between shots
        self.count_bullet = 0

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
            self.bullet_cooldown = 15  # Set cooldown between shots
            self.count_bullet += 1

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

        # Reset y_change to 0 when KEYUP event for up or down arrow keys is detected
        if self.y_change != 0 and (self.rect.y == 0 or self.rect.y == 536):
            self.y_change = 0

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('enemy.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([0, 736])  # Start from either the left or right side
        self.rect.y = random.randint(50, 150)
        self.horizontal_speed = random.uniform(3, 8)  # Random horizontal speed
        self.vertical_speed = random.uniform(5, 8)  # Random vertical speed
        self.vertical_speed_increase = 3.0  # Rate of increase per level
        self.direction = -1 if self.rect.x == 736 else 1

    def update(self):
        self.rect.x += self.direction * self.horizontal_speed

        if self.rect.x <= 0 or self.rect.x >= 736:
            self.rect.y += self.vertical_speed  # Move down
            self.vertical_speed += math.log(self.vertical_speed_increase * game.level)  # Increase vertical speed based on level
            self.direction = -self.direction  # Change direction


# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('bullet.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y -= 8
        if self.rect.y < 0:
            self.kill()


# Game class
class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = pygame.sprite.Group()
        self.spawn_enemies(6)  # Initial number of enemies
        all_sprites.add(self.player)
        all_sprites.add(self.enemies)
        self.score = 0
        self.level = 1
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.over_font = pygame.font.Font('freesansbold.ttf', 64)
        self.running = True
        self.game_over = False  # Add game_over attribute to the Game class
        self.restart_requested = False
        self.bullet_hit = 0
        self.count_bullet = 0

        # Call the efficiency calculation method
        self.calculate_efficiency()

    def show_score(self):
        score = self.font.render(
            f"Score: {self.score}", True,
            (255, 255, 255))
        level = self.font.render(f"Level: {self.level}", True,(255, 255, 255) )
        effisiensi = self.font.render(f"Efficiency: {self.calculate_efficiency()}%", True,(255, 255, 255))
        screen.blit(score, (10, 10))
        screen.blit(level, (10, 40))
        screen.blit(effisiensi, (10, 70))


    def calculate_efficiency(self):
        hitung_peluru = self.player.count_bullet
        effisien = self.bullet_hit / hitung_peluru * 100 if hitung_peluru != 0 else 0
        return round(effisien, 2)

    def game_over_text(self):
        screen.fill((0, 0, 0))
        over_text = self.over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (200, 150))
        screen.blit(restart_button_img, restart_button_rect)

    def restart_game(self):
        # Reset player position
        self.player.rect.x = 370
        self.player.rect.y = 480

        # Reset player y_change to 0
        self.player.y_change = 0

        # Remove all bullets
        bullets.empty()

        # Remove all enemies
        for enemy in self.enemies:
            enemy.kill()

        # Spawn initial enemies
        self.spawn_enemies(6)

        # Reset score and level
        self.score = 0
        self.level = 1

        # Reset Efficiency
        self.bullet_hit = 0
        self.player.count_bullet = 0


        # Reset game over flag
        self.game_over = False
        print("Game restarted!")

    def check_collision(self):
        # Check if enemies exceed the lower part of the window
        for enemy in self.enemies:
            if enemy.rect.y >= 550:
                self.game_over = True
                return True

        # Check collisions with player and enemies
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hits:
            self.game_over = True
            return True

        # Check bullet-enemy collisions
        for bullet in bullets:
            enemy_hits = pygame.sprite.spritecollide(bullet, self.enemies, True)
            for enemy in enemy_hits:
                explosion_sound.play()
                self.score += 1
                bullet.kill()
                self.bullet_hit += 1

        # Check if enemies are all gone (for level advancement)
        if len(self.enemies) == 0:
            self.game_over = False  # Reset game over flag when advancing to the next level

        return False

    def update(self):
        all_sprites.update()

        # Check if the player advances to the next level
        if len(self.enemies) == 0:
            self.level += 1
            self.spawn_enemies(3 * self.level)  # Increase the number of enemies

    def draw(self):
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)

        # Display restart button when game is over
        if self.game_over:
            self.game_over_text()

            # Check for restart button click
            mouse_click = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()

            if restart_button_rect.collidepoint(mouse_pos):
                if mouse_click[0]:
                    print("Restart button clicked!")
                    self.restart_game()
                    self.game_over = False

        # Draw score, level, and efficiency
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        level_text = self.font.render(f"Level: {self.level}", True, (255, 255, 255))
        efficiency_text = self.font.render(f"Efficiency: {self.calculate_efficiency()}%", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 40))
        screen.blit(efficiency_text, (10, 70))

        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if not self.game_over:  # Handle events only if the game is not over
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

            self.handle_mouse_events()  # Call the function to handle mouse events

            if not self.game_over:  # Update and draw only if the game is not over
                self.update()
                self.draw()
                if self.check_collision():
                    self.game_over_text()
                    pygame.display.flip()
                    self.game_over = True

                self.show_score()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def handle_mouse_events(self):
        # Check for restart button click
        mouse_click = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if restart_button_rect.collidepoint(mouse_pos) and mouse_click[0]:
            print("Restart button clicked!")
            self.restart_game()
            self.game_over = False

    def spawn_enemies(self, num_enemies):
        for _ in range(num_enemies):
            enemy = Enemy()
            self.enemies.add(enemy)
            all_sprites.add(enemy)

# Create an instance of the Game class and run the game
game = Game()
game.run()

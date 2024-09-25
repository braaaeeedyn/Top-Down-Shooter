import pygame
import random

# Initialize pygame
pygame.init()

# Game window settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Clock to control frame rate
clock = pygame.time.Clock()

# Font for score and messages
font = pygame.font.Font(None, 36)

# Score and missed enemies counters
score = 0
missed_enemies = 0
max_missed_enemies = 5

# Game state variable
game_state = "playing"  # can be "playing" or "won"

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.speed = 6.25  # Increased by 25%

    def update(self):
        keys = pygame.key.get_pressed()
        
        # Movement controls using Arrow Keys
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < screen_height:
            self.rect.y += self.speed
        
        # Movement controls using WASD
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < screen_width:
            self.rect.x += self.speed
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < screen_height:
            self.rect.y += self.speed

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((14, 14))  # Increased size
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > screen_width:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = random.uniform(1.15, 2.25)  # Random speed between 1.15 and 2.25

        # Determine color based on speed
        if self.speed <= 1.75:
            self.image = pygame.Surface((38, 38))
            self.image.fill((0, 0, 255))  # Blue for slowest
        elif self.speed <= 2.0:
            self.image = pygame.Surface((38, 38))
            self.image.fill((0, 255, 0))  # Green for middle speed
        else:
            self.image = pygame.Surface((38, 38))
            self.image.fill((255, 0, 0))  # Red for fastest
        
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(screen_width - 100, screen_width)
        self.rect.y = random.randint(50, screen_height - 50)

    def update(self):
        global missed_enemies
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
            missed_enemies += 1

def spawn_wave(all_sprites, enemies):
    for _ in range(3):  # Adjust the number of enemies per wave
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

def reset_game(all_sprites, enemies):
    global score, missed_enemies, game_state
    score = 0
    missed_enemies = 0
    game_state = "playing"
    
    # Clear all enemies and projectiles
    enemies.empty()
    all_sprites.empty()

    # Re-add the player to the sprite group
    player = Player()
    all_sprites.add(player)

def draw_winner_message():
    win_text = font.render("You Won!", True, WHITE)
    restart_text = font.render("Press R to Restart", True, WHITE)
    screen.blit(win_text, (screen_width // 2 - win_text.get_width() // 2, screen_height // 2 - 20))
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 20))

def game_loop():
    global score, missed_enemies, game_state

    # Sprite groups
    all_sprites = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # Player instance
    player = Player()
    all_sprites.add(player)

    # Main game loop
    running = True
    spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_event, 1250)  # Decreased spawn interval (approximately 1250 ms)

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_state == "playing":
                    projectile = Projectile(player.rect.centerx, player.rect.centery, WHITE)
                    all_sprites.add(projectile)
                    projectiles.add(projectile)
                if event.key == pygame.K_r and game_state == "won":
                    reset_game(all_sprites, enemies)  # Restart the game

            if event.type == spawn_event and game_state == "playing":
                spawn_wave(all_sprites, enemies)

        # Update game objects
        all_sprites.update()

        # Collision detection: Projectiles hitting enemies
        for projectile in projectiles:
            enemy_hits = pygame.sprite.spritecollide(projectile, enemies, False)
            if enemy_hits:  # If the projectile hits any enemies
                # Iterate through each enemy hit
                for enemy in enemy_hits:
                    # Check the color of the enemy and assign points accordingly
                    if enemy.image.get_at((0, 0)) == (0, 0, 255, 255):  # Blue
                        score += 75
                    elif enemy.image.get_at((0, 0)) == (0, 255, 0, 255):  # Green
                        score += 100
                    elif enemy.image.get_at((0, 0)) == (255, 0, 0, 255):  # Red
                        score += 125

                projectile.kill()  # Remove the projectile after hitting
                for enemy in enemy_hits:
                    enemy.kill()  # Remove the enemies after being hit

        # Check if score reaches 10000
        if score >= 10000 and game_state == "playing":
            game_state = "won"  # Change the game state to won

        # Check if more than 5 enemies have passed the screen
        if missed_enemies > 0:
            score -= missed_enemies * 25  # Subtract 25 points for each missed enemy
            missed_enemies = 0  # Reset missed enemies after penalty is applied

        # Drawing everything
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Draw score on screen
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # If the game is won, draw the winning message
        if game_state == "won":
            draw_winner_message()

        pygame.display.flip()

        # Control frame rate
        clock.tick(60)

    pygame.quit()

# Start the game loop
if __name__ == "__main__":
    game_loop()
import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Motor Bike Racing")

# Colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Clock
clock = pygame.time.Clock()

# Player bike
bike_width = 40
bike_height = 60
player_x = WIDTH // 2
player_y = HEIGHT - 80
speed = 5

# Enemy bike
enemy_x = random.randint(50, WIDTH - 50)
enemy_y = -100
enemy_speed = 5

# Score
score = 0
font = pygame.font.SysFont(None, 30)

# Game loop
running = True
while running:
    screen.fill(GRAY)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= speed
    if keys[pygame.K_RIGHT]:
        player_x += speed

    # Keep player inside road
    player_x = max(50, min(WIDTH - 50, player_x))

    # Move enemy
    enemy_y += enemy_speed

    # Reset enemy when it goes off screen
    if enemy_y > HEIGHT:
        enemy_y = -100
        enemy_x = random.randint(50, WIDTH - 50)
        score += 1
        enemy_speed += 0.2  # Increase difficulty

    # Draw road
    pygame.draw.rect(screen, WHITE, (40, 0, 5, HEIGHT))
    pygame.draw.rect(screen, WHITE, (WIDTH-45, 0, 5, HEIGHT))

    # Draw player bike
    pygame.draw.rect(screen, BLUE, (player_x, player_y, bike_width, bike_height))

    # Draw enemy bike
    pygame.draw.rect(screen, RED, (enemy_x, enemy_y, bike_width, bike_height))

    # Collision detection
    player_rect = pygame.Rect(player_x, player_y, bike_width, bike_height)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, bike_width, bike_height)

    if player_rect.colliderect(enemy_rect):
        print("Game Over! Score:", score)
        pygame.quit()
        sys.exit()

    # Display score
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()

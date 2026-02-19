import pygame
import sys

# Initialize pygame
pygame.init()

# Screen size
WIDTH = 600
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Car Game")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Car properties
car_width = 50
car_height = 30
car_x = WIDTH // 2
car_y = HEIGHT // 2
speed = 5

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Key press detection
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car_x -= speed
    if keys[pygame.K_RIGHT]:
        car_x += speed
    if keys[pygame.K_UP]:
        car_y -= speed
    if keys[pygame.K_DOWN]:
        car_y += speed

    # Keep car inside window
    car_x = max(0, min(WIDTH - car_width, car_x))
    car_y = max(0, min(HEIGHT - car_height, car_y))

    # Drawing
    screen.fill(WHITE)

    # Draw car (rectangle)
    pygame.draw.rect(screen, BLUE, (car_x, car_y, car_width, car_height))

    # Update display
    pygame.display.update()

    # Frame rate
    pygame.time.Clock().tick(60)

import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Real-Life Treasure Hunt")

clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Load images (replace with your real-life images in 'images/' folder)
player_img = pygame.image.load("images/cat.png").convert_alpha()
treasure_img = pygame.image.load("images/gif_chest_smaller.gif").convert_alpha()
beast_img = pygame.image.load("images/sprite-0042.png").convert_alpha()
background_img = pygame.image.load("images/game-background.png").convert()

# Resize images
player_img = pygame.transform.scale(player_img, (50, 50))
treasure_img = pygame.transform.scale(treasure_img, (40, 40))
beast_img = pygame.transform.scale(beast_img, (60, 60))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Player settings
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 5
score = 0
health = 3

# Treasure list
treasures = []
treasure_timer = 0
TREASURE_INTERVAL = 120  # spawn every 2 seconds

# Beast list
beasts = []
BEAST_INTERVAL = 300  # spawn every 3 seconds
beast_timer = 0
beast_speed = 1

# Main game loop
running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed

    # Keep player on screen
    player_pos[0] = max(0, min(WIDTH - 50, player_pos[0]))
    player_pos[1] = max(0, min(HEIGHT - 50, player_pos[1]))

    # Spawn treasures
    treasure_timer += 1
    if treasure_timer >= TREASURE_INTERVAL:
        treasures.append([random.randint(0, WIDTH - 40), random.randint(0, HEIGHT - 40)])
        treasure_timer = 0

    # Spawn beasts
    beast_timer += 1
    if beast_timer >= BEAST_INTERVAL:
        spawn_side = random.choice(["top", "bottom", "left", "right"])
        if spawn_side == "top":
            beasts.append([random.randint(0, WIDTH - 60), 0])
        elif spawn_side == "bottom":
            beasts.append([random.randint(0, WIDTH - 60), HEIGHT - 60])
        elif spawn_side == "left":
            beasts.append([0, random.randint(0, HEIGHT - 60)])
        else:
            beasts.append([WIDTH - 60, random.randint(0, HEIGHT - 60)])
        beast_timer = 0

    # Move beasts toward player
    for beast in beasts:
        if beast[0] < player_pos[0]:
            beast[0] += beast_speed
        elif beast[0] > player_pos[0]:
            beast[0] -= beast_speed
        if beast[1] < player_pos[1]:
            beast[1] += beast_speed
        elif beast[1] > player_pos[1]:
            beast[1] -= beast_speed

    # Collision: player collects treasure
    for treasure in treasures[:]:
        if pygame.Rect(player_pos[0], player_pos[1], 50, 50).colliderect(pygame.Rect(treasure[0], treasure[1], 40, 40)):
            treasures.remove(treasure)
            score += 1

    # Collision: beast hits player
    for beast in beasts[:]:
        if pygame.Rect(player_pos[0], player_pos[1], 50, 50).colliderect(pygame.Rect(beast[0], beast[1], 60, 60)):
            beasts.remove(beast)
            health -= 1
            if health <= 0:
                print("Game Over! Final Score:", score)
                running = False

    # Draw background
    screen.blit(background_img, (0, 0))

    # Draw treasures
    for treasure in treasures:
        screen.blit(treasure_img, (treasure[0], treasure[1]))

    # Draw beasts
    for beast in beasts:
        screen.blit(beast_img, (beast[0], beast[1]))

    # Draw player
    screen.blit(player_img, (player_pos[0], player_pos[1]))

    # Draw score & health
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    health_text = font.render(f": {health}", True, RED)
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 50))

    pygame.display.flip()

pygame.quit()
sys.exit()

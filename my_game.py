import pygame
import random
import sys

#Initialize the Pygame
pygame.init()

#Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Falling Blocks")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 70]
player_speed = 7

# Block
block_size = 50
block_list = []
spawn_delay = 30  # Frames until next block spawns
score = 0

# Font
font = pygame.font.SysFont("Arial", 30)

clock = pygame.time.Clock()

def create_block():
    x_pos = random.randint(0, WIDTH - block_size)
    block_list.append([x_pos, 0])

def draw_blocks():
    for block in block_list:
        pygame.draw.rect(screen, RED, (block[0], block[1], block_size, block_size))

def move_blocks():
    global score
    for block in block_list:
        block[1] += 5  # Falling speed
        if block[1] > HEIGHT:
            block_list.remove(block)
            score += 1  # Increase score for each avoided block

def check_collision():
    for block in block_list:
        if (abs(block[0] - player_pos[0]) < block_size and
            abs(block[1] - player_pos[1]) < block_size):
            return True
    return False

# Game loop
running = True
frame_count = 0
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += player_speed

    # Spawn new blocks
    if frame_count % spawn_delay == 0:
        create_block()

    move_blocks()

    # Draw player
    pygame.draw.rect(screen, GREEN, (player_pos[0], player_pos[1], player_size, player_size))
    draw_blocks()

    # Check for collision
    if check_collision():
        game_over_text = font.render(f"Game Over! Score: {score}", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)
    frame_count += 1
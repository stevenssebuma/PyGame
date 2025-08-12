import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Falling Blocks - Animated Edition")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (210, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 215, 0)
CYAN = (0, 255, 255)
GRAY = (50, 50, 50)

# --- BACKGROUND / ANIMATIONS ---
def draw_background():
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(230 * (1 - t))
        g = int(240 * (1 - t))
        b = int(255 * (1 - t))
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

# Clouds
clouds = [{"x": random.randint(0, WIDTH), "y": random.randint(50, 200), "speed": random.uniform(0.3, 0.8)}
          for _ in range(5)]
def update_clouds():
    for c in clouds:
        c["x"] += c["speed"]
        if c["x"] > WIDTH + 60:
            c["x"] = -60
            c["y"] = random.randint(50, 200)
def draw_clouds():
    for c in clouds:
        pygame.draw.ellipse(screen, WHITE, (c["x"], c["y"], 60, 30))
        pygame.draw.ellipse(screen, WHITE, (c["x"]+20, c["y"]-10, 50, 25))

# Birds
birds = []
def spawn_bird():
    birds.append({"x": -40, "y": random.randint(50, 150), "speed": random.uniform(2, 4)})
def update_birds():
    for b in birds[:]:
        b["x"] += b["speed"]
        if b["x"] > WIDTH + 40:
            birds.remove(b)
def draw_birds():
    for b in birds:
        pygame.draw.polygon(screen, BLACK, [(b["x"], b["y"]),
                                            (b["x"]+10, b["y"]-5),
                                            (b["x"]+20, b["y"])])

# Ground animals
animals = []
def spawn_animal():
    kind = random.choice(["cat", "dog"])
    animals.append({"kind": kind, "x": -50, "y": HEIGHT - 50, "speed": random.uniform(1, 2)})
def update_animals():
    for a in animals[:]:
        a["x"] += a["speed"]
        if a["x"] > WIDTH + 50:
            animals.remove(a)
def draw_animals():
    for a in animals:
        if a["kind"] == "cat":
            pygame.draw.circle(screen, (150, 75, 0), (int(a["x"]), int(a["y"])), 12)
            pygame.draw.circle(screen, (150, 75, 0), (int(a["x"]-10), int(a["y"]-10)), 6)
        else:
            pygame.draw.circle(screen, (100, 100, 100), (int(a["x"]), int(a["y"])), 14)
            pygame.draw.circle(screen, (100, 100, 100), (int(a["x"]-12), int(a["y"]-12)), 7)

# Grass sway
def draw_grass(frame):
    for x in range(0, WIDTH, 10):
        sway = math.sin((frame+x) * 0.05) * 2
        pygame.draw.line(screen, (34, 139, 34), (x, HEIGHT - 20), (x, HEIGHT - 40 + sway), 2)

# Particles
particles = []
def spawn_particles(x, y, color):
    for _ in range(6):
        particles.append({"x": x, "y": y,
                          "vx": random.uniform(-2, 2),
                          "vy": random.uniform(-2, -1),
                          "life": random.randint(15, 25),
                          "color": color})
def update_particles():
    for p in particles[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["vy"] += 0.1
        p["life"] -= 1
        if p["life"] <= 0:
            particles.remove(p)
def draw_particles():
    for p in particles:
        pygame.draw.circle(screen, p["color"], (int(p["x"]), int(p["y"])), 3)

# --- PLAYER ---
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 70]
player_speed = 7
player_color = GREEN
jump_vel = -12
on_ground = True
vertical_vel = 0
shield_active = False
shield_timer = 0
multiplier = 1
multiplier_timer = 0

# --- BLOCKS ---
class Block:
    def __init__(self, x, w, h, vy, color, split=False, split_count=2):
        self.x = x
        self.y = 0
        self.w = w
        self.h = h
        self.vy = vy
        self.color = color
        self.split = split
        self.split_count = split_count
    def update(self, dt):
        self.y += self.vy * dt
        return self.y <= HEIGHT
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))

blocks = []
spawn_delay = 40
score = 0

def create_block():
    w = random.choice([40, 50, 60])
    h = random.choice([40, 50, 60])
    x_pos = random.randint(0, max(0, WIDTH - w))
    vy = random.uniform(3.0, 6.0)
    color = random.choice([RED, BLUE, GRAY, (180,0,180)])
    blocks.append(Block(x_pos, w, h, vy, color))
def update_blocks(dt):
    global blocks, score
    to_remove = []
    for b in blocks:
        alive = b.update(dt)
        if not alive:
            to_remove.append(b)
            score += 1
            spawn_particles(b.x + b.w//2, HEIGHT-20, b.color)
    for b in to_remove:
        if b in blocks:
            blocks.remove(b)
def draw_blocks():
    for b in blocks:
        b.draw()

# --- POWER-UPS ---
class PowerUp:
    def __init__(self, x, y, kind):
        self.x = x
        self.y = y
        self.kind = kind
        self.vy = 2.5
        self.size = 28
        self.col = YELLOW
        if kind == "slow":
            self.col = CYAN
        elif kind == "mult":
            self.col = BLUE
        elif kind == "heal":
            self.col = GREEN
    def update(self, dt):
        self.y += self.vy * dt
        return self.y <= HEIGHT
    def draw(self):
        pygame.draw.circle(screen, self.col, (int(self.x), int(self.y)), self.size // 2)

powerups = []
def spawn_powerup():
    kind = random.choice(["slow", "mult", "heal"])
    pu = PowerUp(random.randint(20, WIDTH-20), -20, kind)
    powerups.append(pu)
def update_powerups(dt):
    for p in powerups[:]:
        if not p.update(dt):
            powerups.remove(p)
def draw_powerups():
    for p in powerups:
        p.draw()
def apply_powerup(pu):
    global shield_active, shield_timer, multiplier, multiplier_timer
    if pu.kind == "mult":
        multiplier += 1
        multiplier_timer = 600
    elif pu.kind == "heal":
        shield_active = True
        shield_timer = 600

# --- COLLISION ---
def check_collision():
    global shield_active
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    for b in blocks:
        if pygame.Rect(b.x, b.y, b.w, b.h).colliderect(player_rect):
            if shield_active:
                shield_active = False
                blocks.remove(b)
                return False
            return True
    for pu in powerups[:]:
        if pygame.Rect(pu.x-pu.size//2, pu.y-pu.size//2, pu.size, pu.size).colliderect(player_rect):
            apply_powerup(pu)
            powerups.remove(pu)
    return False

# --- FONT & CLOCK ---
font = pygame.font.SysFont("Arial", 28)
clock = pygame.time.Clock()

# --- GAME LOOP ---
running = True
frame_count = 0
slow_factor = 1.0
while running:
    draw_background()

    # Update background animations
    update_clouds()
    update_birds()
    update_animals()
    update_particles()
    draw_clouds()
    draw_birds()
    draw_animals()
    draw_grass(frame_count)
    draw_particles()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= int(player_speed)
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += int(player_speed)
    if keys[pygame.K_SPACE] and on_ground:
        vertical_vel = jump_vel
        on_ground = False

    # Gravity
    vertical_vel += 0.5
    player_pos[1] += int(vertical_vel)

    # Ground
    if player_pos[1] >= HEIGHT - player_size - 20:
        player_pos[1] = HEIGHT - player_size - 20
        vertical_vel = 0
        on_ground = True

    # Spawn blocks & background actors
    if frame_count % int(spawn_delay / slow_factor) == 0:
        create_block()
    if frame_count % 500 == 0:
        spawn_bird()
    if frame_count % 800 == 0:
        spawn_animal()
    if frame_count % 600 == 0 and random.random() < 0.25:
        spawn_powerup()

    # Update objects
    update_blocks(1)
    update_powerups(1)

    # Collision check
    if check_collision():
        game_over_text = font.render(f"Game Over! Score: {score}  Mult: x{multiplier}", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - 230, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    # Power-up timers
    if multiplier_timer > 0:
        multiplier_timer -= 1
        if multiplier_timer == 0:
            multiplier = max(1, multiplier - 1)
    if shield_active:
        shield_timer -= 1
        if shield_timer <= 0:
            shield_active = False

    # Draw player
    if shield_active:
        pygame.draw.rect(screen, (0, 200, 255), (player_pos[0]-5, player_pos[1]-5, player_size+10, player_size+10), 3)
    pygame.draw.rect(screen, player_color, (player_pos[0], player_pos[1], player_size, player_size))

    # Draw blocks and powerups
    draw_blocks()
    draw_powerups()

    # Score
    score_text = font.render(f"Score: {score}  Mult: x{multiplier}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Lives
    lives = 3
    for i in range(lives):
        pygame.draw.circle(screen, RED, (WIDTH - 20 - i*22, 20), 6)

    # Display update
    pygame.display.flip()
    clock.tick(60)
    frame_count += 1

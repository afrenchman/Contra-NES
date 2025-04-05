import pygame
import sys

# === Init Pygame ===
pygame.init()
WIDTH, HEIGHT = 256, 224
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Contra Stage 1")
clock = pygame.time.Clock()

# === Constants ===
NES_BLUE = (0, 47, 87)  # Transparency color key
PLAYER_SPEED = 2
JUMP_FORCE = -4
GRAVITY_FORCE = 0.2
DOWN_THROUGH_PLATFORM_SPEED = 3  # Speed when moving down through platforms

# Set ground level to 0 (no ground collision)
GROUND_Y = HEIGHT + 100  # Set far below screen so it's effectively disabled

# Sprite adjustment values to account for transparent borders
SPRITE_X_OFFSET = 15
SPRITE_Y_OFFSET = 15
SPRITE_WIDTH_ADJUSTMENT = 30  # 15 pixels on each side
SPRITE_HEIGHT_ADJUSTMENT = 30  # 15 pixels on each side

# === Load Background ===
bg_image = pygame.image.load("graphics/NES - Contra - Stage 1.png").convert()
bg_image.set_colorkey(NES_BLUE)
bg_width = bg_image.get_width()
scroll_x = 0

# Original dimensions vs new dimensions for scaling
ORIGINAL_WIDTH = 6771
ORIGINAL_HEIGHT = 480
NEW_WIDTH = 3456
NEW_HEIGHT = 220

# Platform thickness
pt = 10

# === Load Walk Frames ===
player_walk = []
for i in range(6):
    img = pygame.image.load(f"graphics/Bill_Rizer/RUN_NO_GUN/player_run_{i}.png").convert()
    img.set_colorkey(NES_BLUE)
    player_walk.append(img)

# === Load Jump Frames ===
player_jump = []
for i in range(4):
    img = pygame.image.load(f"graphics/Bill_Rizer/JUMP/player_jump_{i}.png").convert()
    img.set_colorkey(NES_BLUE)
    player_jump.append(img)


# === Platform Setup ===
def scale_platform(x, y, w, h):
    scaled_x = int(x * (NEW_WIDTH / ORIGINAL_WIDTH))
    scaled_y = int(y * (NEW_HEIGHT / ORIGINAL_HEIGHT) + 10)
    scaled_w = int(w * (NEW_WIDTH / ORIGINAL_WIDTH))
    scaled_h = int(h * (NEW_HEIGHT / ORIGINAL_HEIGHT))
    return scaled_x, scaled_y, scaled_w, scaled_h


# Original platform coordinates
original_platforms = [
    (570, 407, 110, pt),
    (500, 340, 55, pt),
    (690, 340, 55, pt),
    (312, 283, 180, pt),
    (62, 217, 1430, pt),
    (814, 280, 110, pt),
    (1194, 404, 110, pt),
    (1255, 313, 175, pt),
    (1765, 223, 300, pt),  # First Blink
    (2320, 223, 490, pt),
    (2765, 410, 175, pt),
    (2698, 155, 996, pt),
    (2950, 320, 117, pt),
    (3141, 270, 410, pt),
    (3389, 406, 370, pt),
    (3681, 218, 390, pt),
    (3765, 345, 120, pt),
    (3952, 344, 120, pt),
    (4013, 153, 310, pt),
    (4140, 312, 55, pt),
    (4264, 280, 180, pt),
    (4390, 218, 120, pt),  # First Discontinuity
    (4575, 405, 12, pt),
    (4575, 278, 120, pt),
    (4639, 216, 120, pt),  # Second Discontinuity
    (4829, 405, 55, pt),
    (4828, 277, 120, pt),
    (4891, 343, 180, pt),
    (5081, 218, 120, pt),
    (5143, 406, 55, pt),
    (5142, 155, 120, pt),
    (5206, 312, 55, pt),  # Third Discontinuity
    (5332, 218, 120, pt),
    (5392, 281, 310, pt),
    (5582, 408, 180, pt),  # Fourth Discontinuity
    (5832, 344, 120, pt),  # Final Discontinuity
    (6020, 281, 120, pt),
    (6146, 218, 240, pt),
    (6146, 406, 400, pt),
    (6208, 312, 180, pt),
    (6396, 280, 55, pt),
    (6460, 342, 55, pt),
]

# Scale platform coordinates
world_platforms = []
for platform in original_platforms:
    x, y, w, h = scale_platform(platform[0], platform[1], platform[2], platform[3])
    world_platforms.append(pygame.Rect(x, y, w, h))

# === Player Setup ===
player_index = 0
jump_index = 0
player_image = player_walk[0]

# Create the visual rect (full sprite size)
visual_rect = player_image.get_rect(midbottom=(50, 0))  # Start above a platform

# Create the collision rect (adjusted for sprite borders)
player_rect = pygame.Rect(
    visual_rect.x + SPRITE_X_OFFSET,
    visual_rect.y + SPRITE_Y_OFFSET,
    visual_rect.width - SPRITE_WIDTH_ADJUSTMENT,
    visual_rect.height - SPRITE_HEIGHT_ADJUSTMENT
)

x_velocity = 0
y_velocity = 0
on_ground = False
facing_right = True  # Track sprite direction
player_world_x = 0  # Player's position in the world
passing_through = False  # Track if player is passing through platform


def kill_player():
    global player_rect, visual_rect, y_velocity, x_velocity, on_ground
    # Reset player to starting position
    visual_rect = player_image.get_rect(midbottom=(50, 50))
    player_rect = pygame.Rect(
        visual_rect.x + SPRITE_X_OFFSET,
        visual_rect.y + SPRITE_Y_OFFSET,
        visual_rect.width - SPRITE_WIDTH_ADJUSTMENT,
        visual_rect.height - SPRITE_HEIGHT_ADJUSTMENT
    )
    y_velocity = 0
    x_velocity = 0
    on_ground = False


def update_animation():
    global player_image, player_index, jump_index, player_walk, player_jump

    # Get the original image based on state
    if not on_ground:
        # Jump animation
        jump_index = (jump_index + 0.1) % len(player_jump)
        original_image = player_jump[int(jump_index)]
    else:
        # On ground - either walking or standing
        if x_velocity != 0:
            # Walking animation
            player_index = (player_index + 0.1) % len(player_walk)
            original_image = player_walk[int(player_index)]
        else:
            # Standing still
            original_image = player_walk[0]

    # Apply direction flipping if needed
    if facing_right:
        player_image = original_image
    else:
        player_image = pygame.transform.flip(original_image, True, False)


def update_visual_rect():
    visual_rect.x = player_rect.x - SPRITE_X_OFFSET
    visual_rect.y = player_rect.y - SPRITE_Y_OFFSET


def check_platform_collision():
    global y_velocity, on_ground, passing_through

    # If player is moving down through platforms, skip collision
    if passing_through:
        on_ground = False
        return

    # Check if player is falling (not rising)
    if y_velocity < 0:
        return

    on_ground = False
    player_bottom = player_rect.bottom + 1  # Check slightly below the player

    # Create a thin collision rect at the player's feet
    feet_rect = pygame.Rect(player_rect.left, player_bottom - 2, player_rect.width, 2)

    # Check if player fell off the bottom of the screen
    if player_rect.top > HEIGHT:
        kill_player()
        return

    # Convert world platforms to screen coordinates for collision detection
    for platform in world_platforms:
        screen_platform = pygame.Rect(
            platform.x - scroll_x,  # Adjust for camera scroll
            platform.y,
            platform.width,
            platform.height
        )

        # Only check collision if platform is on screen and player's feet collide with it
        if (screen_platform.right > 0 and
                screen_platform.left < WIDTH and
                feet_rect.colliderect(screen_platform)):
            player_rect.bottom = screen_platform.top
            y_velocity = 0
            on_ground = True
            break


# === Main Game Loop ===
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                y_velocity = JUMP_FORCE
                on_ground = False
            if event.key == pygame.K_DOWN:
                passing_through = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                passing_through = False

    # === Input ===
    keys = pygame.key.get_pressed()
    x_velocity = 0  # Reset velocity every frame

    if keys[pygame.K_RIGHT]:
        x_velocity = PLAYER_SPEED
        facing_right = True
    elif keys[pygame.K_LEFT]:
        x_velocity = -PLAYER_SPEED
        facing_right = False

    # Handle downward movement through platforms
    if keys[pygame.K_DOWN] and on_ground:
        passing_through = True
        y_velocity = DOWN_THROUGH_PLATFORM_SPEED
        on_ground = False

    # === Handle player position and scrolling ===
    player_world_x += x_velocity

    if player_rect.centerx > WIDTH // 2 and x_velocity > 0 and scroll_x < bg_width - WIDTH:
        scroll_x += x_velocity
    else:
        player_rect.x += x_velocity

    # Keep player in bounds
    if player_rect.left < 0:
        player_rect.left = 0
        player_world_x = scroll_x + player_rect.centerx
    if player_rect.right > WIDTH:
        player_rect.right = WIDTH
        player_world_x = scroll_x + player_rect.centerx

    # === Gravity and Jumping ===
    if not passing_through:  # Only apply gravity if not moving down through platform
        y_velocity += GRAVITY_FORCE
    player_rect.y += y_velocity

    # Check collision with platforms
    check_platform_collision()

    # Update visual rect position based on collision rect
    update_visual_rect()

    # === Animate Player ===
    update_animation()

    # === Drawing ===
    screen.fill((50, 50, 50))
    screen.blit(bg_image, (-scroll_x, 0))

    # Draw player at the visual rect position
    screen.blit(player_image, visual_rect)

    pygame.display.update()
    clock.tick(60)
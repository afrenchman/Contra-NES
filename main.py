import pygame
import sys
import math

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 256, 224
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Contra Stage 1")
clock = pygame.time.Clock()

# Game States
MENU_SLIDE_IN = 0
MENU = 1
GAME = 2
game_state = MENU_SLIDE_IN

# Load Assets
title_image = pygame.image.load("graphics/Contra-title.png").convert()
title_image = pygame.transform.scale(title_image, (WIDTH, HEIGHT))
cursor_image = pygame.image.load("graphics/cursor.png").convert_alpha()
cursor_image = pygame.transform.scale(cursor_image, (24, 24))
cursor_image.set_colorkey((0,0,0))

# Menu Variables
menu_x = WIDTH  # Start off-screen right
menu_slide_speed = 2
cursor_pos = 0  # 0=1 Player, 1=2 Players
cursor_blink_timer = 0
cursor_visible = True
cursor_blink_interval = 30
cursor_positions = [(31, 141), (31, 156)]  # (x,y) for each option

# Game Constants
NES_BLUE = (0, 47, 87)
PLAYER_SPEED = 2
JUMP_FORCE = -4.3
GRAVITY_FORCE = 0.2
DOWN_THROUGH_SPEED = 3

# Player Sprite Setup
SPRITE_X_OFFSET = 15
SPRITE_Y_OFFSET = 15
SPRITE_WIDTH_ADJUST = 30
SPRITE_HEIGHT_ADJUST = 30

# Load Background
bg_image = pygame.image.load("graphics/NES - Contra - Stage 1.png").convert()
bg_image.set_colorkey(NES_BLUE)
bg_width = bg_image.get_width()
scroll_x = 0

# Platform Scaling
ORIGINAL_WIDTH = 6771
ORIGINAL_HEIGHT = 480
NEW_WIDTH = 3456
NEW_HEIGHT = 220
pt = 10  # platform thickness


def scale_platform(x, y, w, h):
    return (
        int(x * (NEW_WIDTH / ORIGINAL_WIDTH)),
        int(y * (NEW_HEIGHT / ORIGINAL_HEIGHT) + 10),
        int(w * (NEW_WIDTH / ORIGINAL_WIDTH)),
        int(h * (NEW_HEIGHT / ORIGINAL_HEIGHT))
    )


# Platform Data
platform_data = [
    (570, 407, 110, pt), (500, 340, 55, pt), (690, 340, 55, pt),
    (312, 283, 180, pt), (62, 217, 1430, pt), (814, 280, 110, pt),
    (1194, 404, 110, pt), (1255, 313, 175, pt), (1765, 223, 300, pt),
    (2320, 223, 490, pt), (2765, 410, 175, pt), (2698, 155, 996, pt),
    (2950, 320, 117, pt), (3141, 270, 410, pt), (3389, 406, 370, pt),
    (3681, 218, 390, pt), (3765, 345, 120, pt), (3952, 344, 120, pt),
    (4013, 153, 310, pt), (4140, 312, 55, pt), (4264, 280, 180, pt),
    (4390, 218, 120, pt), (4575, 405, 12, pt), (4575, 278, 120, pt),
    (4639, 216, 120, pt), (4829, 405, 55, pt), (4828, 277, 120, pt),
    (4891, 343, 180, pt), (5081, 218, 120, pt), (5143, 406, 55, pt),
    (5142, 155, 120, pt), (5206, 312, 55, pt), (5332, 218, 120, pt),
    (5392, 281, 310, pt), (5582, 408, 180, pt), (5832, 344, 120, pt),
    (6020, 281, 120, pt), (6146, 218, 240, pt), (6146, 406, 400, pt),
    (6208, 312, 180, pt), (6396, 280, 55, pt), (6460, 342, 55, pt)
]

world_platforms = [pygame.Rect(*scale_platform(*p)) for p in platform_data]

# Player Setup
player_walk = [
    pygame.image.load(f"graphics/Bill_Rizer/RUN_NO_GUN/player_run_{i}.png").convert()
    for i in range(6)
]
player_jump = [
    pygame.image.load(f"graphics/Bill_Rizer/JUMP/player_jump_{i}.png").convert()
    for i in range(4)
]

for img in player_walk + player_jump:
    img.set_colorkey(NES_BLUE)

player_index = jump_index = 0
player_image = player_walk[0]
visual_rect = player_image.get_rect(midbottom=(50, 0))
player_rect = pygame.Rect(
    visual_rect.x + SPRITE_X_OFFSET,
    visual_rect.y + SPRITE_Y_OFFSET,
    visual_rect.width - SPRITE_WIDTH_ADJUST,
    visual_rect.height - SPRITE_HEIGHT_ADJUST
)

# Player Movement
x_velocity = y_velocity = 0
on_ground = False
facing_right = True
player_world_x = 0
passing_through = False


def update_animation():
    global player_image, player_index, jump_index

    if not on_ground:
        jump_index = (jump_index + 0.1) % len(player_jump)
        img = player_jump[int(jump_index)]
    else:
        if x_velocity != 0:
            player_index = (player_index + 0.1) % len(player_walk)
            img = player_walk[int(player_index)]
        else:
            img = player_walk[0]

    player_image = img if facing_right else pygame.transform.flip(img, True, False)


def update_visual_rect():
    visual_rect.x = player_rect.x - SPRITE_X_OFFSET
    visual_rect.y = player_rect.y - SPRITE_Y_OFFSET


def check_platform_collision():
    global y_velocity, on_ground

    if passing_through and y_velocity > 0:
        on_ground = False
        return

    if y_velocity < 0:
        return

    on_ground = False
    feet_rect = pygame.Rect(player_rect.left, player_rect.bottom - 1, player_rect.width, 2)

    for platform in world_platforms:
        screen_platform = pygame.Rect(
            platform.x - scroll_x,
            platform.y,
            platform.width,
            platform.height
        )

        if (0 < screen_platform.right and screen_platform.left < WIDTH and
                feet_rect.colliderect(screen_platform)):
            player_rect.bottom = screen_platform.top
            y_velocity = 0
            on_ground = True
            break


# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_state == MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = GAME
                elif event.key == pygame.K_UP:
                    cursor_pos = max(0, cursor_pos - 1)
                elif event.key == pygame.K_DOWN:
                    cursor_pos = min(1, cursor_pos + 1)
        elif game_state == GAME:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and on_ground:
                    y_velocity = JUMP_FORCE
                    on_ground = False
                elif event.key == pygame.K_DOWN:
                    passing_through = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    passing_through = False

    # Update cursor blink
    cursor_blink_timer = (cursor_blink_timer + 1) % cursor_blink_interval
    cursor_visible = cursor_blink_timer < cursor_blink_interval / 2

    if game_state == MENU_SLIDE_IN:
        menu_x = max(0, menu_x - menu_slide_speed)
        if menu_x == 0:
            game_state = MENU

        screen.fill((0, 0, 0))
        screen.blit(title_image, (menu_x, 0))
        pygame.display.update()
        clock.tick(60)
        continue

    elif game_state == MENU:
        screen.blit(title_image, (0, 0))
        if cursor_visible:
            screen.blit(cursor_image, cursor_positions[cursor_pos])
        pygame.display.update()
        clock.tick(60)
        continue

    # Game Logic
    elif game_state == GAME:
        # Handle input
        keys = pygame.key.get_pressed()
        x_velocity = PLAYER_SPEED if keys[pygame.K_RIGHT] else -PLAYER_SPEED if keys[pygame.K_LEFT] else 0

        if x_velocity > 0:
            facing_right = True
        elif x_velocity < 0:
            facing_right = False

        if keys[pygame.K_DOWN] and on_ground:
            passing_through = True
            y_velocity = DOWN_THROUGH_SPEED
            on_ground = False

        # Update player position
        player_world_x += x_velocity

        if player_rect.centerx > WIDTH // 2 and x_velocity > 0 and scroll_x < bg_width - WIDTH:
            scroll_x += x_velocity
        else:
            player_rect.x += x_velocity

        player_rect.left = max(0, player_rect.left)
        player_rect.right = min(WIDTH, player_rect.right)

        # Apply gravity
        if not passing_through or y_velocity <= 0:
            y_velocity += GRAVITY_FORCE
        player_rect.y += y_velocity

        # Check collisions
        check_platform_collision()

        # Check if player fell
        if player_rect.top > HEIGHT:
            game_state = MENU_SLIDE_IN
            menu_x = WIDTH
            player_rect.midbottom = (50, 0)
            scroll_x = 0
            y_velocity = x_velocity = 0
            on_ground = False
            continue

        update_visual_rect()
        update_animation()

        # Draw everything
        screen.fill((50, 50, 50))
        screen.blit(bg_image, (-scroll_x, 0))
        screen.blit(player_image, visual_rect)
        pygame.display.update()
        clock.tick(60)
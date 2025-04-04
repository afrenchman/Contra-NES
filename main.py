import pygame
import sys
from sprites import Sprites
from sidescroll import Camera

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (50, 50, 50)
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 896
GRAVITY = 1
FRAME_COOLDOWN = 100

# Init
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Contra")
clock = pygame.time.Clock()

# Load images
stage_bg = pygame.transform.scale(
    pygame.image.load("graphics/NES - Contra - Stage 1.png").convert(),
    (13700, 980)
)
bill_sheet_img = pygame.transform.scale(
    pygame.image.load("graphics/Bill_Rizer/BillRizerSpriteSheet.png").convert_alpha(),
    (8192, 128)
)

# Init sprite sheet
bill_sheet = Sprites(bill_sheet_img)

# Player sprite data (13 animations)
player_sprites = [6, 6, 2, 2, 6, 6, 4, 1, 2, 2, 2, 2, 2]

# Build animations
master_animation = []
step = 0
for frames in player_sprites:
    animation = []
    for _ in range(frames):
        animation.append(bill_sheet.get_image(step, 128, 128, 2, BLACK))
        step += 1
    master_animation.append(animation)

# Player class
class Player:
    def __init__(self, animations):
        self.master_animation = animations
        self.action = 0
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.x, self.y = 100, SCREEN_HEIGHT - 150
        self.speed = 5
        self.velocity_y = 0
        self.is_jumping = False
        self.direction = 1

    def handle_input(self, keys):
        if keys[pygame.K_d]:
            self.x += self.speed
            self.direction = 1
            self.set_action(0)
        elif keys[pygame.K_a]:
            self.set_action(0)  # No camera movement for left
        else:
            self.set_action(2)  # Standing still gun up (example idle)

    def update(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        if self.y >= SCREEN_HEIGHT - 150:
            self.y = SCREEN_HEIGHT - 150
            self.is_jumping = False

        now = pygame.time.get_ticks()
        if now - self.last_update >= FRAME_COOLDOWN:
            self.last_update = now
            if self.frame >= len(self.master_animation[self.action]) - 1:
                self.frame = 0
            else:
                self.frame += 1

    def set_action(self, action):
        if 0 <= action < len(self.master_animation):
            if action != self.action:
                self.action = action
                self.frame = 0

    def draw(self, screen, camera):
        try:
            img = self.master_animation[self.action][self.frame]
        except IndexError:
            print(f"[ERROR] Action {self.action}, Frame {self.frame}")
            img = self.master_animation[0][0]
            self.action = 0
            self.frame = 0

        if self.direction == -1:
            img = pygame.transform.flip(img, True, False)

        screen.blit(img, (camera.apply(self.x), self.y))


# Game class
class Game:
    def __init__(self):
        self.bg = stage_bg
        self.player = Player(master_animation)
        self.camera = Camera(self.bg.get_width(), SCREEN_WIDTH)

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.update()
            clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        self.player.update()
        self.camera.update(self.player.x)

    def draw(self):
        screen.fill(BG_COLOR)
        screen.blit(self.bg, (self.camera.apply_bg(), 0))
        self.player.draw(screen, self.camera)


Game().run()

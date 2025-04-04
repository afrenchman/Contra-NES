import pygame
from config import *

class Sprites(object):
    def __init__(self, image):
        self.sprite_sheet = pygame.image.load(image).convert_alpha()

    def get_image(self, frame, width, height, scale, color):
        # Blank surface image
        image = pygame.Surface((width, height)).convert_alpha()

        # Copy and scale image to surface
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))

        # Black transparency
        image.set_colorkey(color)

        return image

# init graphics
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()

screen = pygame.display.set_mode(screenSize)

#init start screen

menu = pygame.image.load("graphics/NES - Contra - Menu.png").convert_alpha()

#init bg

l1_bg = pygame.image.load("graphics/NES - Contra - Stage 1.png").convert()

#init player

master_animation = []
player_sprites = [6, #0 FORWARD NO GUN
                  6, #1 FORWARD GUN
                  2, #2 STILL GUN UP
                  2, #3 CROUCH GUN
                  6, #4 TOP RIGHT GUN
                  6, #5 BOTTOM RIGHT GUN
                  4, #6 FLIP
                  1, #7 SPLASH
                  2, #8 SWIM NO GUN
                  2, #9 SWIM FORWARD GUN
                  2, #10 SWIM TOP RIGHT GUN
                  2, #11 SWIM STILL UP GUN
                  2, #12 RIPPLE
                  ]
action = 0
updates = pygame.time.get_ticks()
cooldown = 100
frame = 1
step_counter = 0


# BILL RIZER ANIMATIONS
for animation in player_sprites:
    temp_img_list = []
    for _ in range(animation):
        temp_img_list.append(BILL_SHEET.get_image(step_counter, 128, 128, 2, BLACK))
        step_counter += 1
    master_animation.append(temp_img_list)
import pygame
import os


# Init Display properties
title = "Contra"
screenSize = (1024,896)
fps = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Sidescroll

left_side = 0
right_side = -13700

# Player

PLAYER_HEALTH = 20
PLAYER_POSX = 100
PLAYER_ACC = 0.5
PLAYER_FRC = -0.12
PLAYER_WIDTH = 35
PLAYER_HEIGHT = 55
GRAVITY = 1
JUMP_HEIGHT = 15
BLINK_TIME = 10
BLINK_DISTANCE = 300
BLINK_SPEED = 20
BLINK_RETRACT = 500
ANIM_SPEED = 5  # Lower the faster

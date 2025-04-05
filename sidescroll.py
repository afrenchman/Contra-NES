import pygame

class Camera(object):
    def __init__(self, width, display_width):
        self.offset_X = 0
        self.level_width = width
        self.screen_width = display_width
        self.half = width // 2

    def update(self, x):
        if x > self.half:
            target_off = x - self.half
            max_off = self.level_width - self.screen_width
            self.offset_X = min(target_off, max_off)

    def apply(self, x):
        return x - self.offset_X

    def apply_bg(self):
        return -self.offset_X

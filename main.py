import pygame
import sys
import sprites

# init pygame
pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# init display
screen = pygame.display.set_mode((1024,896)) #w,h double normal contra gameplay
pygame.display.set_caption("Contra")
clock = pygame.time.Clock()
bg_color = (50,50,50)

#init images
stage_1_bg = pygame.transform.scale(pygame.image.load("graphics/NES - Contra - Stage 1.png").convert(),
                                            (13700, 980))
BILL_RIZER = pygame.transform.scale(pygame.image.load("graphics/Bill_Rizer/BillRizerSpriteSheet.png").convert_alpha(),
                                            (8192, 128))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                action = 0
                frame = 0
            if event.key == pygame.K_e:
                action = 1
                frame = 0
            if event.key == pygame.K_s:
                action = 3
                frame = 0

    # screen color
    screen.fill(bg_color)

    # still images
    screen.blit(stage_1_bg, (0,0))

    # animation updates
    time = pygame.time.get_ticks()
    if time - updates >= cooldown:
        frame += 1
        updates = time
        if frame >= len(master_animation[action]):
            frame = 0

    # animations
    screen.blit(master_animation[action][frame], (0, 0))

    # movement

    #WIP

    # misc
    pygame.display.update()
    clock.tick(60)
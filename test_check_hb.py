import math
import time
import pygame
from models.constants.general import *
from models.constants import state
from models.entities import tanks_classes as tnk_cls

screen_width = 200
screen_height = 200
FPS = 60

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))

test_tank = tnk_cls.TankModel3(screen, rev=False, pt0=(screen_width/2, screen_height/2))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))
    test_tank.draw()
    test_tank.draw_hitbox(screen)
    pygame.display.flip()

pygame.quit()


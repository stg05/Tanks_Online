import sys
import pygame

sys.path.append("..")
from models import constants as const
from models import interface_objects as io


def play_range(screen):
    while const.scene_type == 'range':
        screen.fill(const.WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                const.scene_type = 'quit'

        pygame.display.flip()

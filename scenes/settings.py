import sys
import pygame

sys.path.append("..")
from models import constants as const
from models import interface_objects as io


def play_settings(screen):
    print('playing settings')
    button_exit = io.Button(const.WIDTH * 0.95, const.HEIGHT * 0.05, const.WIDTH * 0.10, const.HEIGHT * 0.10, const.RED,
                            const.BLACK, "Exit", io.menu)

    buttons = [button_exit]
    while const.scene_type == 'settings':
        screen.fill(const.WHITE)
        io.check_all_buttons(buttons, screen)
        pygame.display.flip()
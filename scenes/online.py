import sys
import pygame

sys.path.append("..")
from models.constants import general, color
from models import interface_objects as io


def play_online(screen):
    print('playing online')
    button_exit = io.Button(general.WIDTH * 0.95, general.HEIGHT * 0.05, general.WIDTH * 0.10, general.HEIGHT * 0.10,
                            color.RED,
                            color.BLACK, "Exit", io.menu)

    buttons = [button_exit]
    while general.scene_type == 'online':
        screen.fill(color.WHITE)
        io.check_all_buttons(buttons, screen)
        pygame.display.flip()

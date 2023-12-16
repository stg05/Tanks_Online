
import pygame

from models.constants import state
from models.constants.color import *
from models.constants.general import *
from models import interface_objects as io


def play_online(screen):
    print('playing online')
    button_exit = io.Button(WIDTH * 0.95, HEIGHT * 0.05, WIDTH * 0.10, HEIGHT * 0.10,
                            RED,
                            BLACK, "Exit", io.menu)

    buttons = [button_exit]
    while state.scene_type == 'online':
        screen.fill(WHITE)
        io.check_all_buttons(buttons, screen)
        pygame.display.flip()

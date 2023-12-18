import pygame
from models.constants import state
from models.constants.color import *
from models.constants.general import *
from models import interface_objects as io


class SettingsScene:
    def __init__(self, screen):
        print('playing settings')
        button_exit = io.Button(screen, WIDTH * 0.95, HEIGHT * 0.05, WIDTH * 0.10, HEIGHT * 0.10,
                                RED,
                                BLACK, "Exit", io.menu)
        button_left_return = io.Button(screen, WIDTH * (0.3 - 0.05), HEIGHT * 0.7, WIDTH * 0.05, HEIGHT * 0.05,
                                       RED,
                                       BLACK, "<", io.menu)
        button_left_forward = io.Button(screen, WIDTH * (0.3 + 0.05), HEIGHT * 0.7, WIDTH * 0.05, HEIGHT * 0.05,
                                        RED,
                                        BLACK, ">", io.menu)
        button_right_return = io.Button(screen, WIDTH * (0.7 - 0.05), HEIGHT * 0.7, WIDTH * 0.05, HEIGHT * 0.05,
                                       RED,
                                       BLACK, "<", io.menu)
        button_right_forward = io.Button(screen, WIDTH * (0.7 + 0.05), HEIGHT * 0.7, WIDTH * 0.05, HEIGHT * 0.05,
                                       RED,
                                       BLACK, ">", io.menu)
        buttons = [button_exit, button_left_return, button_left_forward, button_right_return, button_right_forward]
        while state.scene_type == 'settings':
            screen.fill(WHITE)
            io.draw_all_buttons(buttons)

            for event in pygame.event.get():
                io.check_all_buttons(event, buttons)
            pygame.display.flip()

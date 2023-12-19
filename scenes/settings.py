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
        button_left_previous = io.Button(screen, WIDTH * (0.3 - 0.05), HEIGHT * 0.7, WIDTH * 0.05, HEIGHT * 0.05,
                                         RED,
                                         BLACK, "<", io.previous_left_tank_number)
        button_left_next = io.Button(screen, WIDTH * (0.3 + 0.05), HEIGHT * 0.7, WIDTH * 0.05, HEIGHT * 0.05,
                                     RED,
                                     BLACK, ">", io.next_left_tank_number)
        button_right_previous = io.Button(screen, WIDTH * (0.7 - 0.05), HEIGHT * 0.7, WIDTH * 0.05, HEIGHT * 0.05,
                                          RED,
                                          BLACK, "<", io.previous_right_tank_number)
        button_right_next = io.Button(screen, WIDTH * (0.7 + 0.05), HEIGHT * 0.7, WIDTH * 0.05, HEIGHT * 0.05,
                                      RED,
                                      BLACK, ">", io.next_right_tank_number)
        buttons = [button_exit, button_left_previous, button_left_next, button_right_previous, button_right_next]
        while state.scene_type == 'settings':
            screen.fill(WHITE)
            io.draw_all_buttons(buttons)
            tank_left = io.create_current_tank_model(screen, rev=False, pt0=(WIDTH * 0.3, 300))
            tank_right = io.create_current_tank_model(screen, rev=True, pt0=(WIDTH * 0.7, 300))
            tanks = [tank_left, tank_right]
            io.draw_all_tanks(tanks)
            for event in pygame.event.get():
                io.check_all_buttons(event, buttons)
            pygame.display.flip()

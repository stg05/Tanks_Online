import pygame
from models.constants.color import *
from models.constants import state
from models import interface_objects as io


def play_menu(screen):
    button_range = io.Button(screen, 700, 150, 400, 80, RED, BLACK, "Range", io.range, font_dir='fonts/Army.ttf')
    button_offline = io.Button(screen, 700, 250, 400, 80, RED, BLACK, "Local multiplayer", io.offline,
                               font_dir='fonts/Army.ttf')
    button_online = io.Button(screen, 700, 350, 400, 80, RED, BLACK, "Online multiplayer", io.online,
                              font_dir='fonts/Army.ttf')
    button_settings = io.Button(screen, 700, 450, 400, 80, RED, BLACK, "Settings", io.settings,
                                font_dir='fonts/Army.ttf')

    buttons = [button_range, button_offline, button_online, button_settings]
    # необходим подцикл, т к если создавать кнопки внутри цикла, они будут нажиматься через раз
    while state.scene_type == 'menu':
        screen.fill(WHITE)
        io.draw_all_buttons(buttons)
        for event in pygame.event.get():
            io.check_all_buttons(event, buttons)

        pygame.display.flip()

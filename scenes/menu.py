import pygame
from models.constants.color import *
from models.constants import state
from models import interface_objects as io
from models.constants.general import WIDTH, HEIGHT


def play_menu(screen):
    button_range = io.Button(screen, WIDTH/2, 150, 400, 80, GREY, BLACK, "Range", io.range, font_dir='fonts/Army.ttf')
    button_offline = io.Button(screen, WIDTH/2, 250, 400, 80, GREY, BLACK, "Local multiplayer", io.offline,
                               font_dir='fonts/Army.ttf')
    button_online = io.Button(screen, WIDTH/2, 350, 400, 80, GREY, BLACK, "Online multiplayer", io.online,
                              font_dir='fonts/Army.ttf')
    button_settings = io.Button(screen, WIDTH/2, 450, 400, 80, GREY, BLACK, "Settings", io.settings,
                                font_dir='fonts/Army.ttf')

    buttons = [button_range, button_offline, button_online, button_settings]

    # необходим подцикл, т к если создавать кнопки внутри цикла, они будут нажиматься через раз
    while state.scene_type == 'menu':
        screen.fill(WHITE)
        background_image = io.current_background_image()
        screen.blit(background_image, (0, 0))
        io.draw_all_buttons(buttons)
        for event in pygame.event.get():
            io.check_all_buttons(event=event, buttons=buttons)

        pygame.display.flip()

import sys
import pygame

sys.path.append("..")
from models.constants import color, general
from models import interface_objects as io


def play_menu(screen):
    button_range = io.Button(700, 150, 150, 80, color.RED, color.BLACK, "Стрельбище", io.range)
    button_offline = io.Button(700, 250, 150, 80, color.RED, color.BLACK, "Оффлайн", io.offline)
    button_online = io.Button(700, 350, 150, 80, color.RED, color.BLACK, "Оnline", io.online)
    button_settings = io.Button(700, 450, 150, 80, color.RED, color.BLACK, "Settings", io.settings)

    buttons = [button_range, button_offline, button_online, button_settings]
    # необходим подцикл, т к если создавать кнопки внутри цикла, они будут нажиматься через раз
    while general.scene_type == 'menu':
        screen.fill(color.WHITE)
        io.check_all_buttons(buttons, screen)
        pygame.display.flip()

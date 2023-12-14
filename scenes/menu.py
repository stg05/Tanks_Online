import sys
import pygame

sys.path.append("..")
from models import constants as const
from models import interface_objects as io

def play_menu(screen):
    button_range = io.Button(300, 250, 200, 100, "Стрельбище", io.range)
    #необходим подцикл, т к если создавать кнопки внутри цикла, они будут нажиматься через раз
    while const.scene_type == 'menu':
        screen.fill(const.WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                const.scene_type = 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    button_range.check_click(event.pos)
        button_range.draw(screen)
        pygame.display.flip()


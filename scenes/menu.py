import sys
import pygame

sys.path.append("..")
from models import constants as const
from models import interface_objects as io
def play_menu(screen):
    print('playing menu')
    screen.fill(const.WHITE)
    button = io.Button(300, 250, 200, 100, "Кнопка")
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                button.check_click(event.pos, 1)
    button.draw(screen)
    pygame.display.update()


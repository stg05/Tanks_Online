import sys
import pygame

sys.path.append("..")
from models import constants as const
from models import interface_objects as io


def play_range(screen):
    print('playing range')
    button_exit = io.Button(const.WIDTH * 0.90, const.HEIGHT * 0, const.WIDTH * 0.10, const.HEIGHT * 0.10,
                            const.RED, const.BLACK, "Exit", io.menu)

    buttons = [button_exit]
    while const.scene_type == 'range':
        screen.fill(const.WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                const.scene_type = 'quit'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in buttons:
                        button.check_click(event.pos)
        for button in buttons:
            button.draw(screen)
        pygame.display.flip()

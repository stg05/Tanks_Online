import pygame
import sys

sys.path.append("..")
from models import constants as const


def menu():
    const.scene_type = 'menu'


def quit():
    const.scene_type = 'quit'


def range():
    const.scene_type = 'range'


class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, const.RED, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, const.BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.action()

import pygame
import sys

sys.path.append("..")
from models import constants as const


# нужно прописывать все эти функции отдельно потому что в функции кнопки не должно быть скобок
def menu():
    const.scene_type = 'menu'


def quit():
    const.scene_type = 'quit'


def range():
    const.scene_type = 'range'


def offline():
    const.scene_type = 'offline'


def online():
    const.scene_type = 'online'


def settings():
    const.scene_type = 'settings'


class Button:
    def __init__(self, x, y, width, height, color, text_color, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = color
        self.text_color = text_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.action()

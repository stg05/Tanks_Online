import pygame

from models.constants import state
from models.constants.color import *


# нужно прописывать все эти функции отдельно потому что в функции кнопки не должно быть скобок
def menu():
    state.scene_type = 'menu'


def quit():
    state.scene_type = 'quit'


def range():
    state.scene_type = 'range'


def offline():
    state.scene_type = 'offline'


def online():
    state.scene_type = 'online'


def settings():
    state.scene_type = 'settings'


def check_all_buttons(buttons, screen, extra_actions=lambda event: None):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state.scene_type = 'quit'
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in buttons:
                    button.check_click(event.pos)
        if event.type == pygame.MOUSEBUTTONUP:
            for button in buttons:
                button.check_release()
                button.draw(screen)
        if event.type == pygame.MOUSEMOTION:
            for button in buttons:
                button.check_hover(event.pos)
        extra_actions(event)
    for button in buttons:
        button.draw(screen)


class Button:
    def __init__(self, x, y, width, height, color, text_color, text, action):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect0 = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)
        self.rect = self.rect0
        self.text = text
        self.action = action
        self.color = color
        self.text_color = text_color
        self.hovered = False
        self.clicked = False
        self.k_small = 0.9  # коэффициент уменьшения

    def draw(self, screen):
        if self.clicked:
            self.rect = pygame.Rect(self.x - self.width * self.k_small / 2, self.y - self.height * self.k_small / 2,
                                    self.width * self.k_small,
                                    self.height * self.k_small)  # Уменьшаем размер кнопки при нажатии
        else:
            self.rect = self.rect0
        pygame.draw.rect(screen, self.color, self.rect)  # Возвращаем исходный цвет кнопки
        if self.hovered:
            pygame.draw.rect(screen, BLACK, self.rect, 3)  # Рисуем рамку при наведении
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            print('pressed')
            self.clicked = True

    def check_release(self):
        if self.clicked:
            print('released')
            self.clicked = False
            self.action()

    def check_hover(self, pos):
        if self.rect.collidepoint(pos):
            self.hovered = True
        else:
            self.hovered = False


class Text:
    def __init__(self, x, y, width, height, text: str | list | tuple, color, text_color=BLACK, text_size=36):
        self.text_size = text_size
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)
        if isinstance(text, str):
            self.text = [text]
        else:
            self.text = text
        self.color = color
        self.text_color = text_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, self.text_size)
        lines = len(self.text)
        dh = self.height / lines
        i = -float(lines-1) / 2
        for line in self.text:
            text = font.render(line, True, self.text_color)
            text_rect = text.get_rect(center=(self.rect.center[0], self.rect.center[1] + i * dh))
            screen.blit(text, text_rect)
            i += 1

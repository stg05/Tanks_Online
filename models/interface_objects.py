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


def check_all_buttons(buttons, screen):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            const.scene_type = 'quit'
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in buttons:
                    button.check_click(event.pos)
        if event.type == pygame.MOUSEBUTTONUP:
            for button in buttons:
                button.check_release()
        if event.type == pygame.MOUSEMOTION:
            for button in buttons:
                button.check_hover(event.pos)

    for button in buttons:
        button.draw(screen)


class Button:
    def __init__(self, x, y, width, height, color, text_color, text, action):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)
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
        pygame.draw.rect(screen, self.color, self.rect)  # Возвращаем исходный цвет кнопки
        if self.hovered:
            pygame.draw.rect(screen, const.BLACK, self.rect, 3)  # Рисуем рамку при наведении
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.clicked = True

    def check_release(self):
        if self.clicked:
            self.clicked = False
            self.action()

    def check_hover(self, pos):
        if self.rect.collidepoint(pos):
            self.hovered = True
        else:
            self.hovered = False

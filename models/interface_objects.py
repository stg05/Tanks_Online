import pygame
from models.constants import state
from models.constants.color import *
from models.constants.general import *
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


def check_all_buttons(event, buttons, extra_actions=lambda event: None):
    if event.type == pygame.QUIT:
        state.scene_type = 'quit'
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
    extra_actions(event)


def draw_all_buttons(buttons):
    for button in buttons:
        button.draw()


def draw_all_tanks(tanks):
    for tank in tanks:
        tank.draw()


def draw_all_missiles(missiles):
    for b in missiles:
        b.draw()


def move_all_tanks(tanks):
    pass
def check_tank_events(event, tank, missiles):
    if event.type == pygame.KEYDOWN:
        key = event.dict.get('key')
        print(key)
        if tank.rev == True:
            if key == pygame.K_UP:
                tank.gun.state = UP
            elif key == pygame.K_DOWN:
                tank.gun.state = DOWN

            elif key == pygame.K_LEFT:
                tank.targetVx = -V
            elif key == pygame.K_RIGHT:
                tank.targetVx = V
            elif key == pygame.K_RETURN:
                tank.gun.fire2_start(event)
            elif key == pygame.K_RSHIFT:
                tank.gun.alterType()

        elif tank.rev == False:
            if key == pygame.K_w:
                tank.gun.state = UP
            elif key == pygame.K_s:
                tank.gun.state = DOWN
            elif key == pygame.K_a:
                tank.targetVx = -V
            elif key == pygame.K_d:
                tank.targetVx = V
            elif key == pygame.K_f:
                tank.gun.fire2_start(event)
            elif key == pygame.K_r:
                tank.gun.alterType()

    elif event.type == pygame.KEYUP:
        key = event.dict.get('key')
        if tank.rev == True:
            if key == pygame.K_UP:
                tank.gun.state = NONE
            elif key == pygame.K_DOWN:
                tank.gun.state = NONE
            elif key == pygame.K_LEFT:
                tank.targetVx = 0
            elif key == pygame.K_RIGHT:
                tank.targetVx = 0
            elif key == pygame.K_RETURN:
                res = tank.gun.fire2_end(event)
                if res is not None:
                    missiles.append(res)

        elif tank.rev == False:
            if key == pygame.K_w:
                tank.gun.state = NONE
            elif key == pygame.K_s:
                tank.gun.state = NONE
            elif key == pygame.K_a:
                tank.targetVx = 0
            elif key == pygame.K_d:
                tank.targetVx = 0
            elif key == pygame.K_f:
                res = tank.gun.fire2_end(event)
                if res is not None:
                    missiles.append(res)


class Button:
    def __init__(self, screen, x, y, width, height, color, text_color, text, action):
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
        self.screen = screen
        self.k_small = 0.9  # коэффициент уменьшения

    def draw(self):
        if self.clicked:
            self.rect = pygame.Rect(self.x - self.width * self.k_small / 2, self.y - self.height * self.k_small / 2,
                                    self.width * self.k_small,
                                    self.height * self.k_small)  # Уменьшаем размер кнопки при нажатии
        pygame.draw.rect(self.screen, self.color, self.rect)  # Возвращаем исходный цвет кнопки
        if self.hovered:
            pygame.draw.rect(self.screen, BLACK, self.rect, 3)  # Рисуем рамку при наведении
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        self.screen.blit(text, text_rect)

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

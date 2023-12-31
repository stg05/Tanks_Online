import pygame

import models.constants.state
from models.constants import state
from models.constants.color import *
from models.constants.general import *
from models.constants import state
from models.constants.color import *
from models.constants.general import *
from models.entities import tanks_classes as tnk_cls
from scenes import background_set as bck_set
from time import time


#  BACKGROUND


def next_background_index():
    bck_set.current_background_index += 1
    bck_set.current_background_index %= len(bck_set.backgrounds)


def previous_background_index():
    bck_set.current_background_index -= 1
    bck_set.current_background_index %= len(bck_set.backgrounds)


def current_background_image():
    bck = bck_set.backgrounds[bck_set.current_background_index]
    return bck


# нужно прописывать все эти функции отдельно потому что в функции кнопки не должно быть скобок

def next_left_tank_number():
    models.constants.state.current_left_class_index += 1
    models.constants.state.current_left_class_index %= len(tnk_cls.all_classes_of_tanks)


def previous_left_tank_number():
    models.constants.state.current_left_class_index -= 1
    models.constants.state.current_left_class_index %= len(tnk_cls.all_classes_of_tanks)


def next_right_tank_number():
    models.constants.state.current_right_class_index += 1
    models.constants.state.current_right_class_index %= len(tnk_cls.all_classes_of_tanks)


def previous_right_tank_number():
    models.constants.state.current_right_class_index -= 1
    models.constants.state.current_right_class_index %= len(tnk_cls.all_classes_of_tanks)


def create_current_tank_model(screen, rev, pt0):
    if not rev:
        left_tank = tnk_cls.all_classes_of_tanks[models.constants.state.current_left_class_index](screen, rev=rev,
                                                                                                  pt0=pt0)
        return left_tank
    elif rev:
        right_tank = tnk_cls.all_classes_of_tanks[models.constants.state.current_right_class_index](screen, rev=rev,
                                                                                                    pt0=pt0)
        return right_tank


def menu():
    state.scene_type = 'menu'


def quit():
    state.scene_type = 'quit'


def range():
    state.scene_type = 'range'


def offline():
    state.result = [0, 0]
    state.scene_type = 'offline'


def online():
    state.scene_type = 'online_connection'


def settings():
    state.scene_type = 'settings'


def check_all_buttons(event, buttons, extra_actions=lambda event: None):
    if event.type == pygame.QUIT:
        state.scene_type = 'quit'
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            for button in buttons:
                button.draw()
                button.check_hover(event.pos)
                extra_actions(event)
                if not button.disabled:
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
    if not tank.controlled_externally:
        if event.type == pygame.KEYDOWN:
            key = event.dict.get('key')
            if tank.rev:
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

            elif not tank.rev:
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
            if tank.rev:
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

            elif not tank.rev:
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
    def __init__(self, screen, x, y, width, height, color, text_color, text, action, args=(), text_size=36,
                 font_dir=None,
                 disable_color=GREY):
        if font_dir:
            self.font = pygame.font.Font(font_dir, text_size)
        else:
            self.font = pygame.font.Font(None, text_size)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect0 = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)
        self.rect = self.rect0
        self.text = text
        self.action = action
        self.args = args
        self.color = color
        self.text_color = text_color
        self.hovered = False
        self.clicked = False
        self.disabled = False
        self.disable_color = disable_color
        self.screen = screen
        self.k_small = 0.9  # коэффициент уменьшения

    def disable(self, value):
        self.disabled = value

    def draw(self):
        if self.clicked and not self.disabled:
            self.rect = pygame.Rect(self.x - self.width * self.k_small / 2, self.y - self.height * self.k_small / 2,
                                    self.width * self.k_small,
                                    self.height * self.k_small)  # Уменьшаем размер кнопки при нажатии
        else:
            self.rect = self.rect0
        pygame.draw.rect(self.screen, self.disable_color if self.disabled else self.color,
                         self.rect)  # Возвращаем исходный цвет кнопки
        if self.hovered:
            pygame.draw.rect(self.screen, BLACK, self.rect, 3)  # Рисуем рамку при наведении
        text = self.font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        self.screen.blit(text, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.clicked = True

    def check_release(self):
        if self.clicked:
            self.clicked = False
            self.rect = self.rect0
            self.action(*self.args)

    def check_hover(self, pos):
        if self.rect.collidepoint(pos):
            self.hovered = True
        else:
            self.hovered = False


class Text:
    def __init__(self, x, y, width, height, text: str | list | tuple, color, text_color=BLACK, text_size=36,
                 font_dir=None):
        self.text_size = text_size
        if font_dir:
            self.font = pygame.font.Font(font_dir, text_size)
        else:
            self.font = pygame.font.Font(None, text_size)
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
        lines = len(self.text)
        dh = self.height / lines
        i = -float(lines - 1) / 2
        for line in self.text:
            text = self.font.render(line, True, self.text_color)
            text_rect = text.get_rect(center=(self.rect.center[0], self.rect.center[1] + i * dh))
            screen.blit(text, text_rect)
            i += 1


class PopUp:
    def __init__(self, x, y, width, height, alpha):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)
        self.alpha = alpha

    def draw(self, screen):
        s = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        s.set_alpha(int(255 * self.alpha))
        s.fill(BLACK)
        pygame.draw.rect(s, (255, 255, 255), pygame.Rect(5, 5, s.get_width() - 10, s.get_height() - 10))
        screen.blit(s, (self.x - self.width / 2, self.y - self.height / 2))


class TextPrompt:
    def __init__(self, x, y, width, height, text, text_size=36, font_dir=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)
        self.text0 = text
        self.text = None
        self.color = (255, 0, 0)
        self.disabled = False
        if font_dir:
            self.font = pygame.font.Font(font_dir, text_size)
        else:
            self.font = pygame.font.Font(None, text_size)

    def update_text(self, text):
        self.text0 = text

    def disable(self, value: bool):
        self.disabled = value

    def set_status(self, ok):
        if ok:
            self.color = (0, 255, 0)
        else:
            self.color = (255, 0, 0)

    def draw(self, screen):

        if int(time() * 2) % 2 < 1:
            self.text = self.font.render(self.text0 + ' ', True, self.color)
        else:
            self.text = self.font.render(self.text0 + '_', True, self.color)
        rect = self.text.get_rect(center=(self.x, self.y))
        pygame.draw.rect(screen, (0, 0, 0), rect)
        if not self.disabled:
            screen.blit(self.text, rect)


class CountSign:
    def __init__(self, x, y, width, height, count, text_size=48, font_dir='fonts/Hack-Bold.ttf'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)
        self.count = count
        if font_dir:
            self.font = pygame.font.Font(font_dir, text_size)
        else:
            self.font = pygame.font.Font(None, text_size)

    def draw(self, screen):
        text_left = self.font.render(str(self.count[0]), True, (255, 0, 0))
        text_right = self.font.render(str(self.count[1]), True, (0, 0, 255))
        rect_left = text_left.get_rect(center=(self.x - self.width / 4, self.y))
        rect_right = text_right.get_rect(center=(self.x + self.width / 4, self.y))
        pygame.draw.rect(screen, (0, 0, 0), self.rect)
        screen.blit(text_left, rect_left)
        screen.blit(text_right, rect_right)

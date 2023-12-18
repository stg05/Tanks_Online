import pygame
from models.constants import state
from models.constants.color import *
from models.constants.general import *
from models.constants import state
from models.constants.color import *
from models.constants.general import *
from time import time


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
                button.draw()
                button.check_hover(event.pos)
                extra_actions(event)
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
        # print(key)
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
    def __init__(self, screen, x, y, width, height, color, text_color, text, action, text_size=36, font_dir=None):
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
        else:
            self.rect = self.rect0
        pygame.draw.rect(self.screen, self.color, self.rect)  # Возвращаем исходный цвет кнопки
        pygame.draw.rect(self.screen, self.color, self.rect)  # Возвращаем исходный цвет кнопки
        if self.hovered:
            pygame.draw.rect(self.screen, BLACK, self.rect, 3)  # Рисуем рамку при наведении
        text = self.font.render(self.text, True, self.text_color)
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
            self.rect = self.rect0
            self.action()

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
        self.suppressed = False
        if font_dir:
            self.font = pygame.font.Font(font_dir, text_size)
        else:
            self.font = pygame.font.Font(None, text_size)

    def update_text(self, text):
        self.text0 = text

    def suppress(self, value: bool):
        self.suppressed = value

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
        if not self.suppressed:
            screen.blit(self.text, rect)

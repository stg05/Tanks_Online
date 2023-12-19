import math
import pygame
from models.constants.color import *
from models.constants.general import *
from tools.geometry import *
from time import time


class Divider:
    _xAmp = 100
    _yAmp = 100
    _y0 = 400
    _nu = 5e-1
    _width = 10

    def __init__(self, screen):
        self.x = 0
        self.y = 0
        self._prev = 0
        self.screen = screen
        self.update()

    def update(self):
        self.x = WIDTH / 2 + self._xAmp * math.sin(self._nu * time()) + self._xAmp * math.sin(
            math.pi * self._nu * time())

        self.y = self._y0 + self._yAmp * math.sin(math.pi * self._nu * time()) + self._yAmp * math.sin(
            math.pi ** 2 * self._nu * time())

    def draw(self):
        pygame.draw.rect(self.screen,
                         color=BLACK,
                         rect=[self.x - self._width, self.y, self._width, HEIGHT - self.y])

    def check_collision(self, missile):
        missile_path = ((missile.x, missile.y), (missile.prev_x, missile.prev_y))
        return intersect_pol_seg(((self.x, self.y), (self.x, HEIGHT)), missile_path)


class AimCircle:
    _xAmp = 100
    _yAmp = 100
    _y0 = 400
    _x0 = WIDTH-200
    _nu = 5e-1
    _width = 10

    def __init__(self, screen):
        self.x = 0
        self.y = 0
        self.size = 300
        self._prev = 0
        self.screen = screen
        self.update()

    def update(self):
        self.x = self._x0
        self.y = self._y0

    def draw(self):
        pygame.draw.rect(self.screen,
                         color=BLACK,
                         rect=[self.x - self._width, self.y, self._width, HEIGHT - self.y])

    def check_collision(self, x, y, vx):
        if y > self.y:
            a = -1 if vx < 0 else 1
            if self._prev * a < 0 < (x - self.x) * a:
                self._prev = (x - self.x)
                return True
        self._prev = (x - self.x)
        return None

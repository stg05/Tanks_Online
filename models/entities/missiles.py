import math
import pygame

from models.constants.general import *
from models.constants.color import *


class Missile:
    def __init__(self, screen: pygame.Surface, x, y, shell_type, rev=False):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.live = 30
        self.an = 1
        self.alpha = -1 if rev else 1
        self.type = shell_type

    def move(self, tick):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx * tick
        self.y -= self.vy * tick
        self.vy -= (G + self.vy * ETA) * tick
        self.vx -= self.vx * ETA * tick
        self.an = math.atan(self.vy / self.vx)

    def draw(self):
        sin = math.sin(self.an)
        cos = math.cos(self.an)
        wid = 5
        length = 20

        pts = [(self.x - self.alpha * wid * sin, self.y - self.alpha * wid * cos),
               (self.x + self.alpha * wid * sin, self.y + self.alpha * wid * cos),
               (self.x + self.alpha * length * cos, self.y - self.alpha * length * sin)]
        pygame.draw.polygon(self.screen,
                            DARKGREY,
                            pts)

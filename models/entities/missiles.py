import math
import pygame

from models.constants.general import *
from models.constants.color import *


class Missile:
    def __init__(self, screen: pygame.Surface, x, y, shell_type, rev=False, guided_externally=False):
        self.screen = screen
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.live = 30
        self.an = 1
        self.alpha = -1 if rev else 1
        self.type = shell_type
        self.first_frame = True
        self.damage_aps = DAMAGE_APS
        self.damage_hefs = DAMAGE_HEFS
        self.wid = 5
        self.length = 20
        self.guided_externally = guided_externally

    def move(self, tick):
        self.first_frame = False
        self.prev_x = self.x
        self.prev_y = self.y
        self.x += self.vx * tick
        self.y -= self.vy * tick
        self.vy -= (G + self.vy * ETA) * tick
        self.vx -= self.vx * ETA * tick
        self.an = math.atan(self.vy / self.vx)

    def draw(self):
        sin = math.sin(self.an)
        cos = math.cos(self.an)

        pts = [(self.x - self.alpha * self.wid * sin, self.y - self.alpha * self.wid * cos),
               (self.x + self.alpha * self.wid * sin, self.y + self.alpha * self.wid * cos),
               (self.x + self.alpha * self.length * cos, self.y - self.alpha * self.length * sin)]
        pygame.draw.polygon(self.screen,
                            DARKGREY,
                            pts)


class RocketMissile(Missile):
    pass


class BulletMissile(Missile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.damage_aps = 60
        self.damage_hefs = 30
        self.wid = 3
        self.length = 10

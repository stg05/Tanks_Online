import math
import pygame

from models.constants import state
from models.constants.general import *
from models.constants.color import *
from models.constants.online_events import *
from time import time_ns


class Missile:
    def __init__(self, screen: pygame.Surface, x, y, shell_type, rev=False, guided_externally=False,
                 reversed_externally=False, missile_no=None):
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
        self.new = True
        self.alpha = -1 if rev else 1
        self.type = shell_type
        self.first_frame = True
        self.damage_aps = DAMAGE_APS
        self.damage_hefs = DAMAGE_HEFS
        self.wid = 5
        self.length = 20
        self.guided_externally = guided_externally
        self.reversed_externally = reversed_externally
        if missile_no:
            self.missile_no = missile_no
        else:
            self.missile_no = time_ns() << 1
            if state.socket_order == state.MASTER:
                self.missile_no += 1

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

    def __str__(self):
        res = ''
        res += f'{self.missile_no}'
        res += ' ' + f'{self.x} {self.y}'
        res += ' ' + f'{self.vx} {self.vy}'
        return res

    @staticmethod
    def handle_info(msg, missiles):
        data = msg.split('\n')
        for line in data:
            if line != '':
                data_local = line.split(' ')
                for missile in missiles:
                    if missile.missile_no == int(data_local[0]):
                        if state.right_handed ^ missile.reversed_externally:
                            missile.x = WIDTH - float(data_local[1])
                            missile.vx = -float(data_local[3])
                        else:
                            missile.x = float(data_local[1])
                            missile.vx = float(data_local[3])
                        missile.y = float(data_local[2])
                        missile.vy = float(data_local[4])
                        missile.an = math.atan(missile.vy / missile.vx)
                        break

    @staticmethod
    def report_event(status, missile):
        res = ''
        if status == STATUS_DEL:
            res += 'DEL' + ' ' + str(missile.missile_no)
        elif status == STATUS_CREATE:
            res += 'CREATE' + ' ' + str(missile.missile_no)
            res += ' ' + f'{missile.x} {missile.y}'
            res += ' ' + f'{missile.alpha == -1}'
            res += ' ' + f'{missile.type}'
            res += ' ' + f'{missile.missile_no}'
        return res

    @staticmethod
    def handle_event(screen, msg, missiles):
        data = msg.split(' ')
        head = data[0]
        if head == 'DEL':
            for missile in missiles:
                if missile.missile_no == int(data[1]):
                    missiles.remove(missile)
                    del missile
                    break
        elif head == 'CREATE':
            missile = Missile(screen, x=float(data[2]), y=float(data[3]),
                              rev=not state.right_handed, reversed_externally=bool(data[4]),
                              shell_type=int(data[5]), guided_externally=True, missile_no=int(data[6]))
            missiles.append(missile)


class RocketMissile(Missile):
    pass


class BulletMissile(Missile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.damage_aps = 60
        self.damage_hefs = 30
        self.wid = 3
        self.length = 10

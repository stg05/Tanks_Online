import math
import pygame

import models.constants.state
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
                        if not state.right_handed ^ missile.reversed_externally:
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
    def report_event(status, missile, target=None):
        res = ''
        if status == STATUS_DEL:
            res += 'DEL' + ' ' + str(missile.missile_no)
        elif status == STATUS_CREATE:
            res += 'CREATE' + ' ' + str(missile.missile_no)
            res += ' ' + f'{missile.x} {missile.y}'
            res += ' ' + f'{missile.alpha == -1}'
            res += ' ' + f'{missile.type}'
            res += ' ' + f'{missile.missile_no}'
            res += ' ' + f'{isinstance(missile, BulletMissile)}'
        elif status == STATUS_HIT:
            res += 'HIT'
            res += ' ' + f'{missile.missile_no}'
            res += ' ' + f'{target}'
        elif status == STATUS_DEADLY_HIT:
            res += 'DEADLY_HIT'
            res += ' ' + f'{missile.missile_no}'
        return res

    @staticmethod
    def handle_event(screen, msg, missiles, trg_tank=None):
        from models.entities.tanks_physics import TOWER, GUN, TRACK
        data = msg.split(' ')
        head = data[0]
        if head == 'DEL':
            for missile in missiles:
                if missile.missile_no == int(data[1]):
                    missiles.remove(missile)
                    del missile
                    break

        if head == 'DEADLY_HIT':
            trg_tank.hp = 0
            trg_tank.health_bar.update(trg_tank.x, trg_tank.y, trg_tank.hp)
            trg_tank.health_bar.draw()
            if state.right_handed:
                state.result[0] += 1
            else:
                state.result[1] += 1
            models.constants.state.scene_type = 'commence_online'

        if head == 'HIT':
            for missile in missiles:
                if missile.missile_no == int(data[1]):
                    if missile.type == APS:
                        trg_tank.hp -= missile.damage_aps
                    elif missile.type == HEFS:
                        trg_tank.hp -= missile.damage_hefs
                        target = int(data[2])
                        if target == TOWER:
                            trg_tank.towerDisabled = DISABLE_FOR
                        elif target == TRACK:
                            trg_tank.trackDisabled = DISABLE_FOR
                        elif target == GUN:
                            trg_tank.gun.disabled = DISABLE_FOR
                            trg_tank.gun.f2_power = trg_tank.gun.basicPower
                    missiles.remove(missile)
                    del missile
                    break
        elif head == 'CREATE':
            if data[7] == 'True':
                missile = BulletMissile(screen, x=float(data[2]), y=float(data[3]),
                                        rev=not state.right_handed, reversed_externally=data[4] == 'True',
                                        shell_type=int(data[5]), guided_externally=True, missile_no=int(data[6]))
                missiles.append(missile)
            else:
                missile = Missile(screen, x=float(data[2]), y=float(data[3]),
                                  rev=not state.right_handed, reversed_externally=data[4] == 'True',
                                  shell_type=int(data[5]), guided_externally=True, missile_no=int(data[6]))
                missiles.append(missile)


class RocketMissile(Missile):
    pass


class BulletMissile(Missile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.damage_aps = 40
        self.damage_hefs = 20
        self.wid = 3
        self.length = 10

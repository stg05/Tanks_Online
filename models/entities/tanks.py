import pygame
import math
from models.entities.missiles import Missile
from models.constants.color import *
from models.constants.general import *

# HITBOX PARAMS
TOWER = 1
TRACK = 2

# GUN STATES
UP = 1
DOWN = -1
NONE = 0

# ENVIR PARAMS
G = 4000
ETA = 1.0


class HealthBar:
    length = 100
    def __init__(self, screen, dx, dy):
        self.screen = screen
        self.dx = dx
        self.dy = dy
        self.x = 0
        self.y = 0
        self.hp = 1.0

    def update(self, x, y, hp):
        self.x = x
        self.y = y
        self.hp = hp

    def draw(self):
        pygame.draw.line(self.screen, GREY, (self.x + self.dx - self.length/2, self.y + self.dy),
                         (self.x + self.dx + self.length/2, self.y + self.dy), width=3)
        pygame.draw.line(self.screen, GREEN, (self.x + self.dx - self.length / 2, self.y + self.dy),
                         (self.x + self.dx - self.length / 2 + self.length*self.hp, self.y + self.dy), width=3)


class HitBox:
    class Rectangle:
        def __init__(self, pt0, pt1):
            self.pt0 = (min(pt0[0], pt1[0]), min(pt0[1], pt1[1]))
            self.pt1 = (max(pt0[0], pt1[0]), max(pt0[1], pt1[1]))

    def reverse(self):
        for rect in self.rectangles:
            rect.pt0 = (min(-rect.pt0[0], -rect.pt1[0]), min(rect.pt0[1], rect.pt1[1]))
            rect.pt1 = (max(-rect.pt0[0], -rect.pt1[0]), max(rect.pt0[1], rect.pt1[1]))

    def __init__(self, arr):
        self.rectangles = arr
        self.x = 0
        self.y = 0

    def update(self, x, y):
        self.x = x
        self.y = y

    def check_collision(self, missile):
        rect = self.rectangles[0]
        hit = (rect.pt0[0] <= missile.x - self.x <= rect.pt1[0]
               and rect.pt0[1] <= missile.y - self.y <= rect.pt1[1])
        if hit:
            return True, TRACK
        rect = self.rectangles[1]
        hit = (rect.pt0[0] <= missile.x - self.x <= rect.pt1[0]
               and rect.pt0[1] <= missile.y - self.y <= rect.pt1[1])
        if hit:
            return True, TOWER
        return False, None


class Tank:
    def __init__(self, screen, pt0=(50, 450), gun_pos=(20, -60),
                 vrt=((60, 0), (80, -10), (80, -40), (20, -40), (30, -50), (30, -70), (-30, -70), (-30, -50),
                      (-20, -40), (-80, -40), (-80, -10), (-60, -0)), color=ARMYGREEN, rev=False,
                 hitbox_params=None):
        if hitbox_params is None:
            hitbox_params = [HitBox.Rectangle((80, 0), (-80, -40)), HitBox.Rectangle((30, -40), (-30, -70))]
        self.color = color
        self.gun_pos = gun_pos
        self.alpha = -1 if rev else 1
        self.vrt = vrt
        self.rev = rev
        self.hp = TANK_HP
        self.x = pt0[0]
        self.y = pt0[1]
        self.health_bar = HealthBar(screen, 0, 20)
        self.health_bar.update(self.x, self.y, float(self.hp)/TANK_HP)

        self.hp = TANK_HP
        self.hitbox = HitBox(hitbox_params)
        if rev:
            self.hitbox.reverse()
        self.hitbox.update(self.x, self.y)
        self.gun = Gun(screen, self.color, self.rev, pt0[0] + self.alpha * gun_pos[0], pt0[1] + gun_pos[1])
        self.vx = 0
        self.targetVx = 0
        self.picVertices = []
        self.calc_coords()
        self.screen = screen
        # self.origin = None
        self.bound1 = None
        self.bound2 = None
        self.towerDisabled = 0
        self.trackDisabled = 0

    def check_collision(self, missile):
        hit, target = self.hitbox.check_collision(missile)
        if hit:
            if missile.type == HEFS:
                self.hp -= DAMAGE_HEFS
                self.health_bar.update(self.x, self.y, float(self.hp) / TANK_HP)
                if target == TOWER:
                    self.towerDisabled = DISABLE_FOR
                elif target == TRACK:
                    self.trackDisabled = DISABLE_FOR
                return hit, target
            elif missile.type == APS:
                self.health_bar.update(self.x, self.y, float(self.hp) / TANK_HP)
                self.hp -= DAMAGE_APS
                return hit, NONE

        return False, None

    def calc_coords(self):
        self.picVertices = []
        for elem in self.vrt:
            self.picVertices.append((self.alpha * elem[0] + self.x, elem[1] + self.y))

    def move(self, tick):
        if not self.trackDisabled > 0:
            self.vx += (self.targetVx - self.vx) * K * tick
            if self.bound2 and self.bound1:
                if (self.vx > 0 and self.x < self.bound2) or (self.vx < 0 and self.x > self.bound1):
                    self.x += self.vx * tick
            else:
                self.x += self.vx * tick
            self.gun.x = self.x + self.alpha * self.gun_pos[0]
            self.gun.y = self.y + self.gun_pos[1]
            self.hitbox.update(self.x, self.y)
            self.health_bar.update(self.x, self.y, float(self.hp) / TANK_HP)

    def move_gun(self, tick):
        if not self.towerDisabled != 0:
            if self.gun.state == UP and self.gun.an > AN_MIN:
                self.gun.an -= OMEGA * tick
            elif self.gun.state == DOWN and self.gun.an < AN_MAX:
                self.gun.an += OMEGA * tick

    def processDisabled(self, tick):
        if self.towerDisabled > 0:
            self.towerDisabled -= tick
            if self.towerDisabled < 0:
                self.towerDisabled = 0
        if self.trackDisabled > 0:
            self.trackDisabled -= tick
            if self.trackDisabled < 0:
                self.trackDisabled = 0

    def draw(self):
        # self.hitbox.draw()
        self.gun.draw()
        self.calc_coords()
        self.health_bar.draw()
        pygame.draw.polygon(self.screen,
                            self.color,
                            self.picVertices)

    def set_bounds(self, x1, x2):
        self.bound1 = x1
        self.bound2 = x2


class TankModel1(Tank):

    def __init__(self, *args, **kwargs):
        kwargs.update({"color": ARMYGREEN,
                       "vrt": ((60, 0), (80, -10), (80, -40), (20, -40), (30, -50), (30, -70), (-30, -70), (-30, -50),
                               (-20, -40), (-80, -40), (-80, -10), (-60, -0)),
                       "gun_pos": (20, -60),
                       "hitbox_params": [HitBox.Rectangle((80, 0), (-80, -40)),
                                         HitBox.Rectangle((30, -40), (-30, -70))]})
        super().__init__(*args, **kwargs)


class TankModel2(Tank):

    def __init__(self, *args, **kwargs):
        kwargs.update({"color": KHAKI,
                       "vrt": ((60, 0), (80, -12), (80, -30), (60, -38), (55, -48), (30, -48), (30, -66), (-10, -72),
                               (-30, -69), (-30, -48), (-80, -48), (-75, -8), (-60, -0)),
                       "hitbox_params": [HitBox.Rectangle((80, 0), (-80, -48)),
                                         HitBox.Rectangle((30, -48), (-30, -70))]})
        super().__init__(*args, **kwargs)



class Gun:
    maxPow = 100
    basicLength = 20
    gunLength = 100
    basicPower = 10

    def __init__(self, screen, color, rev, x0, y0):
        self.screen = screen
        self.f2_power = self.basicPower
        self.alpha = -1 if rev else 1
        self.f2_on = 0
        self.an = -0.5
        self.color = color
        self.aimColor = GREY
        self.x = x0
        self.y = y0
        self.state = NONE
        self.edgeCrd = (0, 0)
        self.rev = rev
        self.type = APS

    def alterType(self):
        if self.type == APS:
            self.type = HEFS
            self.aimColor = ORANGE

        elif self.type == HEFS:
            self.type = APS
            self.aimColor = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        new_missile = Missile(self.screen, self.edgeCrd[0], self.edgeCrd[1], self.type, rev=self.rev)
        new_missile.origin = self
        new_missile.vx = self.alpha * self.f2_power * math.cos(self.an) * MISSILE_V
        new_missile.vy = - self.f2_power * math.sin(self.an) * MISSILE_V
        self.f2_on = 0
        self.f2_power = self.basicPower
        return new_missile

    def draw(self):
        alpha = -1 if self.rev else 1
        cos = math.cos(self.an)
        sin = math.sin(self.an)
        length = self.basicLength + (self.gunLength - self.basicLength) * (self.f2_power - self.basicPower) / (
                self.maxPow - self.basicPower)
        wid = 5
        aim_pts = [(self.x + self.alpha * wid * sin, self.y - wid * cos),
                   (self.x - self.alpha * wid * sin, self.y + wid * cos),
                   (self.x - self.alpha * wid * sin + self.alpha * length * cos, self.y + wid * cos + length * sin),
                   (self.x + self.alpha * wid * sin + self.alpha * length * cos, self.y - wid * cos + length * sin)]
        self.edgeCrd = (self.x + self.alpha * self.gunLength * cos, self.y + self.gunLength * sin)
        pts = [(self.x + self.alpha * wid * sin, self.y - wid * cos),
               (self.x - self.alpha * wid * sin, self.y + wid * cos),
               (self.x - self.alpha * wid * sin + self.alpha * self.gunLength * cos,
                self.y + wid * cos + self.gunLength * sin),
               (self.x + self.alpha * wid * sin + self.alpha * self.gunLength * cos,
                self.y - wid * cos + self.gunLength * sin)]

        pygame.draw.polygon(self.screen,
                            self.color,
                            pts)
        pygame.draw.polygon(self.screen,
                            self.aimColor,
                            aim_pts)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < self.maxPow:
                self.f2_power += 1

import pygame
import math
from models.entities.missiles import Missile
from models.constants.color import *
from models.constants.general import *
from tools.geometry import intersect_pol_seg

# HITBOX PARAMS
TOWER = 1
TRACK = 2
GUN = 3

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
        pygame.draw.line(self.screen, GREY, (self.x + self.dx - self.length / 2, self.y + self.dy),
                         (self.x + self.dx + self.length / 2, self.y + self.dy), width=3)
        pygame.draw.line(self.screen, GREEN, (self.x + self.dx - self.length / 2, self.y + self.dy),
                         (self.x + self.dx - self.length / 2 + self.length * self.hp, self.y + self.dy), width=3)


class HitBox:
    class Polygon:
        def __init__(self, vrt_arr):
            self.pts = vrt_arr

    def __init__(self, tank):
        self.tank = tank

    def check_collision(self, missile):
        missile_path = ((missile.x, missile.y), (missile.prev_x, missile.prev_y))
        hull = self.tank.recalc_verts[0]
        if intersect_pol_seg(hull, missile_path):
            return True, TRACK
        tower = self.tank.recalc_verts[1]
        if len(tower) > 0:
            if intersect_pol_seg(tower, missile_path):
                return True, TOWER
        gun = self.tank.gun.get_pts()
        if intersect_pol_seg(gun, missile_path):
            return True, GUN
        return False, None


class Tank:
    def __init__(self, screen, pt0, gun_pos,
                 vrt_hull,
                 vrt_tower, color,
                 rev):
        self.color = color
        self.gun_pos = gun_pos
        self.alpha = -1 if rev else 1
        self.vrt_hull = vrt_hull
        self.vrt_tower = vrt_tower
        self.rev = rev
        self.hp = TANK_HP
        self.x = pt0[0]
        self.y = pt0[1]
        self.health_bar = HealthBar(screen, 0, 20)
        self.health_bar.update(self.x, self.y, float(self.hp) / TANK_HP)

        self.hp = TANK_HP
        self.hitbox = HitBox(self)
        self.gun = Gun(screen, self.color, self.rev, pt0[0] + self.alpha * gun_pos[0], pt0[1] + gun_pos[1])
        self.vx = 0
        self.targetVx = 0
        self.recalc_verts = [[], []]
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
                elif target == GUN:
                    self.gun.disabled = DISABLE_FOR
                    self.gun.f2_power = self.gun.basicPower
                return hit, target
            elif missile.type == APS:
                self.health_bar.update(self.x, self.y, float(self.hp) / TANK_HP)
                self.hp -= DAMAGE_APS
                return hit, NONE

        return False, None

    def calc_coords(self):
        self.recalc_verts = [[], []]
        for elem in self.vrt_hull:
            self.recalc_verts[0].append((self.alpha * elem[0] + self.x, elem[1] + self.y))
        for elem in self.vrt_tower:
            self.recalc_verts[1].append((self.alpha * elem[0] + self.x, elem[1] + self.y))

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
        if self.gun.disabled > 0:
            self.gun.disabled -= tick
            if self.gun.disabled < 0:
                self.gun.disabled = 0

    def draw(self):
        self.gun.draw()
        self.calc_coords()
        self.health_bar.draw()
        pygame.draw.polygon(self.screen,
                            self.color,
                            self.recalc_verts[0])
        pygame.draw.polygon(self.screen,
                            self.color,
                            self.recalc_verts[1])

    def set_bounds(self, x1, x2):
        self.bound1 = x1
        self.bound2 = x2


class TankModel1(Tank):
    def __init__(self, *args, **kwargs):
        kwargs.update({"color": ARMYGREEN,
                       "vrt_hull": (
                           (60, 0), (80, -10), (80, -40), (20, -40), (-20, -40), (-80, -40), (-80, -10), (-60, -0)),
                       "vrt_tower": ((20, -40), (30, -50), (30, -70), (-30, -70), (-30, -50), (-20, -40)),
                       "gun_pos": (20, -60)})
        super().__init__(*args, **kwargs)


class TankModel2(Tank):

    def __init__(self, *args, **kwargs):
        kwargs.update({"color": KHAKI,
                       "vrt_hull": (
                           (60, 0), (80, -12), (80, -30), (60, -38), (55, -48), (-80, -48), (-75, -8), (-60, -0)),
                       "vrt_tower": ((30, -48), (30, -66), (-10, -72), (-30, -69), (-30, -48)),
                       "gun_pos": (20, -60)})
        super().__init__(*args, **kwargs)


class Gun:
    maxPow = 100
    basicLength = 20
    gunLength = 100
    basicPower = 10

    def __init__(self, screen, color, rev, x0, y0):
        self.disabled = 0
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
        self.f2_on = True

    def fire2_end(self, event):
        if self.disabled == 0:
            new_missile = Missile(self.screen, self.edgeCrd[0] + 1 * self.alpha, self.edgeCrd[1] - 1, self.type,
                                  rev=self.rev)
            new_missile.origin = self
            new_missile.vx = self.alpha * self.f2_power * math.cos(self.an) * MISSILE_V
            new_missile.vy = - self.f2_power * math.sin(self.an) * MISSILE_V
            self.f2_on = False
            self.f2_power = self.basicPower
            return new_missile

    def draw(self):
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

    def get_pts(self):
        wid = 5
        cos = math.cos(self.an)
        sin = math.sin(self.an)
        return [(self.x + self.alpha * wid * sin, self.y - wid * cos),
                (self.x - self.alpha * wid * sin, self.y + wid * cos),
                (self.x - self.alpha * wid * sin + self.alpha * self.gunLength * cos,
                 self.y + wid * cos + self.gunLength * sin),
                (self.x + self.alpha * wid * sin + self.alpha * self.gunLength * cos,
                 self.y - wid * cos + self.gunLength * sin)]

    def power_up(self):
        if self.f2_on and self.disabled == 0:
            if self.f2_power < self.maxPow:
                self.f2_power += 1

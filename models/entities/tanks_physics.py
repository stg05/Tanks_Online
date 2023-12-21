import pygame
import math
from models.entities.missiles import *
from models.constants.color import *
from models.constants.general import *
from tools.geometry import intersect_pol_seg
import random

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
    scale_factor = 0.3

    def __init__(self, screen, dx, dy):
        self.screen = screen
        self.dx = dx
        self.dy = dy
        self.x = 0
        self.y = 0
        self.hp = 1.0
        self.tower_pic = pygame.image.load('models/entities/modules_models/tower.png').convert_alpha()
        self.gun_pic = pygame.image.load('models/entities/modules_models/gun.png').convert_alpha()
        self.track_pic = pygame.image.load('models/entities/modules_models/track.png').convert_alpha()
        self.tower_pic = pygame.transform.rotozoom(self.tower_pic, 0, self.scale_factor)
        self.gun_pic = pygame.transform.rotozoom(self.gun_pic, 0, self.scale_factor)
        self.track_pic = pygame.transform.rotozoom(self.track_pic, 0, self.scale_factor)

    def update(self, x, y, hp):
        self.x = x
        self.y = y
        self.hp = hp

    def set_crit(self, dest, val):
        if val:
            if dest == TOWER:
                self.tower_pic = pygame.image.load('models/entities/modules_models/tower_cr.png').convert_alpha()
                self.tower_pic = pygame.transform.rotozoom(self.tower_pic, 0, self.scale_factor)
            if dest == GUN:
                self.gun_pic = pygame.image.load('models/entities/modules_models/gun_cr.png').convert_alpha()
                self.gun_pic = pygame.transform.rotozoom(self.gun_pic, 0, self.scale_factor)

            if dest == TRACK:
                self.track_pic = pygame.image.load('models/entities/modules_models/track_cr.png').convert_alpha()
                self.track_pic = pygame.transform.rotozoom(self.track_pic, 0, self.scale_factor)
        else:
            if dest == TOWER:
                self.tower_pic = pygame.image.load('models/entities/modules_models/tower.png').convert_alpha()
                self.tower_pic = pygame.transform.rotozoom(self.tower_pic, 0, self.scale_factor)
            if dest == GUN:
                self.gun_pic = pygame.image.load('models/entities/modules_models/gun.png').convert_alpha()
                self.gun_pic = pygame.transform.rotozoom(self.gun_pic, 0, self.scale_factor)
            if dest == TRACK:
                self.track_pic = pygame.image.load('models/entities/modules_models/track.png').convert_alpha()
                self.track_pic = pygame.transform.rotozoom(self.track_pic, 0, self.scale_factor)

    def draw(self):
        pygame.draw.line(self.screen, GREY, (self.x + self.dx - self.length / 2, self.y + self.dy),
                         (self.x + self.dx + self.length / 2, self.y + self.dy), width=3)
        pygame.draw.line(self.screen, GREEN, (self.x + self.dx - self.length / 2, self.y + self.dy),
                         (self.x + self.dx - self.length / 2 + self.length * self.hp, self.y + self.dy), width=3)
        rect_tower = self.tower_pic.get_rect(center=(self.x, self.y + 50))
        self.screen.blit(self.tower_pic, rect_tower)
        rect_gun = self.gun_pic.get_rect(center=(self.x-50, self.y + 50))
        self.screen.blit(self.gun_pic, rect_gun)
        rect_track = self.track_pic.get_rect(center=(self.x + 50, self.y + 50))
        self.screen.blit(self.track_pic, rect_track)


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
                 rev, speed_ratio, tank_full_hp,
                 image_name,
                 controlled_externally=False,
                 reversed_externally=False):
        self.color = color
        self.gun_pos = gun_pos
        self.alpha = -1 if rev else 1
        self.vrt_hull = vrt_hull
        self.vrt_tower = vrt_tower
        self.rev = rev
        self.full_hp = tank_full_hp
        self.x = pt0[0]
        self.y = pt0[1]
        self.controlled_externally = controlled_externally
        self.reversed_externally = reversed_externally
        self.hp = tank_full_hp
        self.health_bar = HealthBar(screen, 0, 20)
        self.health_bar.update(self.x, self.y, float(self.hp) / self.hp)
        self.image_name = image_name
        self.full_image_name = "models/entities/tank_models/" + self.image_name

        self.hitbox = HitBox(self)
        self.gun_x = pt0[0] + self.alpha * gun_pos[0]
        self.gun_y = pt0[1] + gun_pos[1]
        self.gun = TankGun(screen, self.color, self.rev, self.gun_x, self.gun_y)
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
        self.speed_ratio = speed_ratio
        self.__hb_omitted = False

    def omit_healthbar(self):
        self.__hb_omitted = True

    def __str__(self):
        res = ''
        if self.rev:
            res = f'{WIDTH - self.x}'
        else:
            res = f'{self.x}'
        res += f'\n{self.gun.an}'
        res += f'\n{self.gun.f2_power}'
        res += f'\n{self.gun.type}'
        return res

    def append_incoming(self, msg):
        data = msg.split('\n')
        x = float(data[0])
        self.gun.an = float(data[1])
        self.gun.f2_power = float(data[2])
        self.gun.setType(int(data[3]))
        self.x = WIDTH - x if self.rev else x

    def init_params(self):
        res = ''
        from models.entities.tanks_classes import all_classes_of_tanks
        for i in range(0, len(all_classes_of_tanks)):
            if isinstance(self, all_classes_of_tanks[i]):
                res += str(i)
        res += '\n' + str(self.rev)
        return res

    def check_collision(self, missile):
        if self.gun is missile.origin:
            return False, None
        hit, target = self.hitbox.check_collision(missile)
        if hit:
            if missile.type == HEFS:
                self.hp -= missile.damage_hefs
                self.health_bar.update(self.x, self.y, float(self.hp) / self.full_hp)
                if target == TOWER:
                    self.towerDisabled = DISABLE_FOR
                elif target == TRACK:
                    self.trackDisabled = DISABLE_FOR
                elif target == GUN:
                    self.gun.disabled = DISABLE_FOR
                    self.gun.f2_power = self.gun.basicPower
                self.health_bar.set_crit(target, True)
                return hit, target
            elif missile.type == APS:
                self.health_bar.update(self.x, self.y, float(self.hp) / self.full_hp)
                self.hp -= missile.damage_aps
                return hit, None

        return False, None

    def calc_coords(self):
        self.recalc_verts = [[], []]
        for elem in self.vrt_hull:
            self.recalc_verts[0].append((self.alpha * elem[0] + self.x, elem[1] + self.y))
        for elem in self.vrt_tower:
            self.recalc_verts[1].append((self.alpha * elem[0] + self.x, elem[1] + self.y))

    def move(self, tick):
        if not self.trackDisabled > 0:
            self.vx += (self.targetVx * self.speed_ratio - self.vx) * self.speed_ratio * tick
            if self.bound2 and self.bound1:
                if (self.vx > 0 and self.x < self.bound2) or (self.vx < 0 and self.x > self.bound1):
                    self.x += self.vx * tick
            else:
                self.x += self.vx * tick
            self.gun.x = self.x + self.alpha * self.gun_pos[0]
            self.gun.y = self.y + self.gun_pos[1]
            self.health_bar.update(self.x, self.y, float(self.hp) / self.full_hp)

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
                self.health_bar.set_crit(TOWER, False)
        if self.trackDisabled > 0:
            self.trackDisabled -= tick
            if self.trackDisabled < 0:
                self.trackDisabled = 0
                self.health_bar.set_crit(TRACK, False)
        if self.gun.disabled > 0:
            self.gun.disabled -= tick
            if self.gun.disabled < 0:
                self.gun.disabled = 0
                self.health_bar.set_crit(GUN, False)

    def draw(self):
        self.gun.draw()
        self.calc_coords()
        if not self.__hb_omitted:
            self.health_bar.draw()
        image = pygame.image.load(self.full_image_name).convert_alpha()
        if self.rev:
            image = pygame.transform.flip(image, True, False)
        rect = image.get_rect(center=(self.x, self.y))
        self.screen.blit(image, rect)

    def draw_hitbox(self, screen):
        self.gun.draw()
        self.calc_coords()
        self.health_bar.draw()
        pygame.draw.polygon(screen,
                            MAGENTA,
                            self.recalc_verts[0])
        pygame.draw.polygon(screen,
                            GREEN,
                            self.recalc_verts[1])

    def set_bounds(self, x1, x2):
        self.bound1 = x1
        self.bound2 = x2


class TankFast(Tank):
    def __init__(self, *args, **kwargs):
        kwargs.update({"speed_ratio": 3,
                       "tank_full_hp": 500})
        super().__init__(*args, **kwargs)


class TankMiddle(Tank):
    def __init__(self, *args, **kwargs):
        kwargs.update({"speed_ratio": 2,
                       "tank_full_hp": 750})
        super().__init__(*args, **kwargs)


class TankSlow(Tank):

    def __init__(self, *args, **kwargs):
        kwargs.update({"speed_ratio": 1,
                       "tank_full_hp": 1000})
        super().__init__(*args, **kwargs)


class Gun:
    # maxPow = 100
    # basicLength = 20
    # gunLength = 100
    # basicPower = 10

    def __init__(self, screen, color, rev, x0, y0, maxPow, basicLength, gunLength, basicPower, wid):
        self.maxPow = maxPow
        self.basicLength = basicLength
        self.gunLength = gunLength
        self.basicPower = basicPower
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
        self.wid = wid

    def alterType(self):
        if self.type == APS:
            self.type = HEFS
            self.aimColor = ORANGE

        elif self.type == HEFS:
            self.type = APS
            self.aimColor = GREY

    def setType(self, typ):
        if typ == HEFS:
            self.type = HEFS
            self.aimColor = ORANGE

        elif typ == APS:
            self.type = APS
            self.aimColor = GREY

    def fire2_start(self, event):
        self.f2_on = True

    def fire2_end(self, event):
        self.f2_on = False
        if self.disabled == 0:
            new_missile = Missile(self.screen, self.edgeCrd[0] + 1 * self.alpha, self.edgeCrd[1] - 1, self.type,
                                  rev=self.rev)
            new_missile.origin = self
            new_missile.vx = self.alpha * self.f2_power * math.cos(self.an) * MISSILE_V
            new_missile.vy = - self.f2_power * math.sin(self.an) * MISSILE_V
            self.f2_power = self.basicPower
            return new_missile

    def fire_action(self, missiles):
        pass

    def draw(self):
        cos = math.cos(self.an)
        sin = math.sin(self.an)
        length = self.basicLength + (self.gunLength - self.basicLength) * (self.f2_power - self.basicPower) / (
                self.maxPow - self.basicPower)

        aim_pts = [(self.x + self.alpha * self.wid * sin, self.y - self.wid * cos),
                   (self.x - self.alpha * self.wid * sin, self.y + self.wid * cos),
                   (self.x - self.alpha * self.wid * sin + self.alpha * length * cos,
                    self.y + self.wid * cos + length * sin),
                   (self.x + self.alpha * self.wid * sin + self.alpha * length * cos,
                    self.y - self.wid * cos + length * sin)]
        self.edgeCrd = (self.x + self.alpha * self.gunLength * cos, self.y + self.gunLength * sin)
        pts = [(self.x + self.alpha * self.wid * sin, self.y - self.wid * cos),
               (self.x - self.alpha * self.wid * sin, self.y + self.wid * cos),
               (self.x - self.alpha * self.wid * sin + self.alpha * self.gunLength * cos,
                self.y + self.wid * cos + self.gunLength * sin),
               (self.x + self.alpha * self.wid * sin + self.alpha * self.gunLength * cos,
                self.y - self.wid * cos + self.gunLength * sin)]

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


class TankGun(Gun):
    def __init__(self, *args, **kwargs):
        kwargs.update({"maxPow": 100, "basicLength": 20, "gunLength": 100, "basicPower": 10, "wid": 5})
        super().__init__(*args, **kwargs)


class MiniGun(Gun):
    delta_angle_max = 0.1

    def __init__(self, *args, **kwargs):
        kwargs.update({"maxPow": 100, "basicLength": 7, "gunLength": 30, "basicPower": 40, "wid": 2})
        self.minigun_previous_fire_time = 0
        self.delta_time_minigun = 100
        self.time_after_previous_fire = 0
        self.max_fire_time = 2000
        self.reload_time = 4500
        self.minigun_start_fire_time = 0
        self.start_reload_time = 0
        super().__init__(*args, **kwargs)

    def fire_action(self, missiles):
        self.time_after_previous_fire = pygame.time.get_ticks() - self.minigun_previous_fire_time
        if (pygame.time.get_ticks() - self.minigun_start_fire_time) > self.max_fire_time and self.disabled == 0:
            self.disabled = 1
            self.start_reload_time = pygame.time.get_ticks()
        if self.disabled == 1 and (pygame.time.get_ticks() - self.start_reload_time) > self.reload_time:
            self.disabled = 0
        if self.f2_on and self.time_after_previous_fire > self.delta_time_minigun and self.disabled == 0:
            new_missile = BulletMissile(self.screen, self.edgeCrd[0] + 1 * self.alpha, self.edgeCrd[1] - 1, self.type,
                                        rev=self.rev)
            rand_angle = self.an + random.uniform(-self.delta_angle_max, self.delta_angle_max)
            new_missile.origin = self
            new_missile.vx = self.alpha * self.f2_power * math.cos(rand_angle) * MISSILE_V
            new_missile.vy = - self.f2_power * math.sin(rand_angle) * MISSILE_V
            self.minigun_previous_fire_time = pygame.time.get_ticks()
            missiles.append(new_missile)

    def fire2_start(self, event):
        self.f2_on = True
        self.minigun_previous_fire_time = pygame.time.get_ticks()
        self.minigun_start_fire_time = pygame.time.get_ticks()

    def fire2_end(self, event):
        self.f2_on = False
        self.f2_power = self.basicPower

import math
import pygame
from models.constants.color import *
from models.constants.general import *
from tools.geometry import *
from time import time
from scenes import background_set as bck_set


class Divider:
    _xAmp = WIDTH * 0.05
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
        if bck_set.current_background_index == 0:
            divider_image = pygame.image.load("models/entities/divider_models/divider_water.png").convert_alpha()
        else:
            divider_image = pygame.image.load("models/entities/divider_models/divider_lava.png").convert_alpha()
        rect = divider_image.get_rect(center=(self.x, self.y + 2.75 * self._yAmp))
        self.screen.blit(divider_image, rect)


    def check_collision(self, missile):
        missile_path = ((missile.x, missile.y), (missile.prev_x, missile.prev_y))
        return intersect_pol_seg(((self.x, self.y), (self.x, HEIGHT)), missile_path)


class AimCircle:
    _xAmp = 100
    _yAmp = 100
    _y0 = 250
    _x0 = WIDTH-250
    _nu = 5e-1
    _width = 10
    _length = 200

    def __init__(self, screen):
        self.x = 0
        self.y = 0
        self.size = 200
        self._prev = 0
        self.screen = screen
        self.update()
        self.score = 0
        self.image = pygame.image.load("models/entities/divider_models/aim_circle.png").convert_alpha()


    def update(self):
        self.x = self._x0
        self.y = self._y0

    def draw(self):
        rect = self.image.get_rect(center=(self.x, self.y + self._length/2))
        self.screen.blit(self.image, rect)

    def check_collision(self, x, y, vx):
        if y > self.y:
            a = -1 if vx < 0 else 1
            if self._prev * a < 0 < (x - self.x) * a:
                self._prev = (x - self.x)
                self.check_points(x, y)
                return True
        self._prev = (x - self.x)
        return None

    def check_points(self, x, y):
        distance_from_center = abs(y - self.y - self._length/2)
        max_distance = self._length / 2  # Максимальное расстояние от центра
        normalized_distance = 1 - (distance_from_center / max_distance)  # Нормализуем расстояние
        points = int(self._length * normalized_distance)  # Определяем количество очков
        self.score += points

    def display_score(self, pt0, font_dir, text_size, color):
        font = pygame.font.Font(font_dir, text_size)
        score_text = font.render(f"Score: {self.score}", True, color)
        self.screen.blit(score_text, pt0)
import math
import time
import pygame
from models.entities import tanks as tk
from models.constants.general import *
from models.constants import state
from scenes import menu
from scenes import range
from scenes import offline
from scenes import online
from scenes import settings

# COLOR DEFINITIONS

# GENERAL GRAPHICS PARAMS
WIDTH = 1500
HEIGHT = 600
FPS = 60


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
        self.x = WIDTH / 2 + self._xAmp * math.sin(self._nu * time.time()) + self._xAmp * math.sin(
            math.pi * self._nu * time.time())

        self.y = self._y0 + self._yAmp * math.sin(math.pi * self._nu * time.time()) + self._yAmp * math.sin(
            math.pi ** 2 * self._nu * time.time())

    def draw(self):
        pygame.draw.rect(self.screen,
                         color=tk.BLACK,
                         rect=[self.x - self._width, self.y, self._width, HEIGHT - self.y])

    def check_collision(self, x, y, vx):
        if y > self.y:
            a = -1 if vx < 0 else 1
            if self._prev * a < 0 < (x - self.x) * a:
                self._prev = (x - self.x)
                return True
        self._prev = (x - self.x)
        return False


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

missiles = []

clock = pygame.time.Clock()
tank1 = tk.TankModel1(screen, rev=False, pt0=(100, 450))
tank2 = tk.TankModel2(screen, rev=True, pt0=(WIDTH - 100, 450))
tank1.set_bounds(80, WIDTH / 2 - 400)
tank2.set_bounds(WIDTH / 2 + 300, WIDTH - 80)
tanks = [tank1, tank2]
div = Divider(screen)

# snd = sound.SoundLoader()
#io.change_scene('menu')
while not state.scene_type == 'quit':
    if state.scene_type == 'menu':
        menu.play_menu(screen)
    elif state.scene_type == 'range':
        range.play_range(screen)
    elif state.scene_type == 'offline':
        offline.play_offline(screen)
    elif state.scene_type == 'online':
        online.play_online(screen)
    elif state.scene_type == 'settings':
        settings.play_settings(screen)

pygame.quit()

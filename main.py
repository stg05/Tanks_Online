import math
import time
import pygame
from models.constants.general import *
from models.entities import tanks_classes as tnk_cls
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



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF, 32)

missiles = []

Clock = pygame.time.Clock
# snd = sound.SoundLoader()
# io.change_scene('menu')
tank1 = tnk_cls.TankModel1(screen, rev=False, pt0=(100, 450))
tank2 = tnk_cls.TankModel2(screen, rev=True, pt0=(WIDTH - 100, 450))
while not state.scene_type == 'quit':
    if state.scene_type == 'menu':
        menu.play_menu(screen)
    elif state.scene_type == 'range':
        range.play_range(screen)
    elif state.scene_type == 'offline':
        offline.OfflineScene(screen)
    elif state.scene_type == 'online':
        online.OnlineInputScene(screen)
    elif state.scene_type == 'settings':
        settings.SettingsScene(screen)

pygame.quit()

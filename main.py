import math
import time
import pygame
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



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

missiles = []


# snd = sound.SoundLoader()
#io.change_scene('menu')
while not state.scene_type == 'quit':
    if state.scene_type == 'menu':
        menu.play_menu(screen)
    elif state.scene_type == 'range':
        range.play_range(screen)
    elif state.scene_type == 'offline':
        offline.OfflineScene(screen)
    elif state.scene_type == 'online':
        online.OnlineScene(screen)
    elif state.scene_type == 'settings':
        settings.play_settings(screen)

pygame.quit()

import pygame

import models.interface_objects as io
from models.constants import state
from scenes import menu
from scenes import offline
from scenes import online
from scenes import range
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
left_tank = io.create_current_tank_model(screen, rev=False, pt0=(100, 450))
right_tank = io.create_current_tank_model(screen, rev=True, pt0=(WIDTH - 100, 450))
tanks = [left_tank, right_tank]
cur_scene = None
while not state.scene_type == 'quit':
    if state.scene_type == 'menu':
        menu.play_menu(screen)
    elif state.scene_type == 'range':
        range.play_range(screen)
    elif state.scene_type == 'offline':
        offline.OfflineScene(screen)
    elif state.scene_type == 'online_connection':
        cur_scene = online.OnlineInputScene(screen)
        del cur_scene
    elif state.scene_type == 'commence_offline':
        state.scene_type = 'offline'
    elif state.scene_type == 'online':
        cur_scene = online.OnlineScene(screen, state.socket)
        del cur_scene
        state.socket.settimeout(None)
    elif state.scene_type == 'commence_online':
        print('commenced')
        state.scene_type = 'online'
    elif state.scene_type == 'settings':
        settings.SettingsScene(screen)

pygame.quit()

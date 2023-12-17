import random

import pygame
from tools import conn
from models.constants import state
from models.constants.color import *
from models.constants.general import *
from models import interface_objects as io


class OnlineScene:
    @staticmethod
    def init_connection():
        host = input()
        srv = None
        count = 0
        while srv is None and count < 5:
            port = random.randint(40000, 49999)
            srv = conn.open_port(host, port)
            count += 1

    def __init__(self, screen):
        self.port = None
        self.srv = None
        ip = conn.find_ip()
        popup = io.PopUp(WIDTH*0.5, HEIGHT*0.5, WIDTH*0.35, WIDTH*0.35, 0.8)
        button_exit = io.Button(WIDTH * 0.95, HEIGHT * 0.05, WIDTH * 0.10, HEIGHT * 0.10,
                                RED,
                                BLACK, "Exit", io.menu)

        button_client = io.Button(WIDTH * 0.50, HEIGHT * 0.38, WIDTH * 0.20, HEIGHT * 0.10,
                                  BLUE,
                                  BLACK, 'Connect to...', lambda: None)
        button_server = io.Button(WIDTH * 0.50, HEIGHT * 0.52, WIDTH * 0.20, HEIGHT * 0.10,
                                  BLUE,
                                  BLACK, 'Initiate...', self.init_connection)

        buttons = [button_exit]
        if not ip:
            text = io.Text(WIDTH * 0.50, HEIGHT * 0.50, WIDTH * 0.40, HEIGHT * 0.60,
                           ("You're not connected to the internet", "Try again later!"),
                           RED,
                           BLACK,
                           48)
        else:
            text = io.Text(WIDTH * 0.50, HEIGHT * 0.10, WIDTH * 0.35, HEIGHT * 0.20,
                           ('Please use following IP:', f'IP: {conn.find_ip()}', f'PORT: NONE'),
                           GREEN,
                           BLACK)
            buttons.append(button_client)
            buttons.append(button_server)

        while state.scene_type == 'online':
            screen.fill(WHITE)
            text.draw(screen)
            io.check_all_buttons(buttons, screen)
            popup.draw(screen)
            pygame.display.flip()

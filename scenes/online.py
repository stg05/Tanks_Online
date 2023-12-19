import random
import re
import threading

import pygame
from tools import conn
from models.constants import state
from models.constants.color import *
from models.constants.general import *
from models import interface_objects as io


class OnlineInputScene:
    def wait_incoming(self, ip, port):
        self.srv = conn.wait_incoming(ip, port)

    def init_connection(self):
        if self.key_handler.ok:
            self.button_client.disable(True)
            self.button_server.disable(True)
            self.key_handler.disable(True)
            ip, port = self.key_handler.content.split(":")
            port = int(port)
            print('starting')
            t = threading.Thread(target=self.wait_incoming, args=(ip, port))
            t.start()

    def connect_to(self):
        if self.key_handler.ok:
            ip, port = self.key_handler.content.split(":")
            port = int(port)
            print('connecting')
            t = threading.Thread(target=conn.wait_incoming, args=(ip, port))
            t.start()

    def __init__(self, screen):
        self.key_handler = None
        self.port = None
        self.ip = conn.find_ip()
        self.port = conn.find_port()
        self.srv = None
        ip = conn.find_ip()
        self.button_exit = io.Button(screen, WIDTH * 0.95, HEIGHT * 0.05, WIDTH * 0.10, HEIGHT * 0.10,
                                     RED, BLACK, "Exit", io.menu, text_size=36, font_dir='fonts/Army.ttf')

        self.button_client = io.Button(screen, WIDTH * 0.50, HEIGHT * 0.38, WIDTH * 0.20, HEIGHT * 0.10,
                                       BLUE, BLACK, 'Connect to...', lambda: None, text_size=36,
                                       font_dir='fonts/Army.ttf')
        self.button_server = io.Button(screen, WIDTH * 0.50, HEIGHT * 0.52, WIDTH * 0.20, HEIGHT * 0.10,
                                       BLUE, BLACK, 'Initiate...', self.init_connection, text_size=36,
                                       font_dir='fonts/Army.ttf')

        buttons = [self.button_exit]
        to_draw = []
        if not ip:
            text = io.Text(WIDTH * 0.50, HEIGHT * 0.50, WIDTH * 0.40, HEIGHT * 0.60,
                           ("You're not connected to the internet", "Try again later!"),
                           RED,
                           BLACK,
                           48)
        else:
            text = io.Text(WIDTH * 0.50, HEIGHT * 0.10, WIDTH * 0.40, HEIGHT * 0.20,
                           ('Please use following address:', f'IP: {self.ip}', f'PORT: {self.port}'),
                           GREEN, BLACK, text_size=36, font_dir='fonts/Army.ttf')
            ip_prompt = io.TextPrompt(WIDTH * 0.50, HEIGHT * 0.30, WIDTH * 0.20, HEIGHT * 0.10, '',
                                      text_size=20, font_dir='fonts/Hack-Bold.ttf')
            hint = io.Text(WIDTH * 0.50, HEIGHT * 0.28, WIDTH * 0.40, HEIGHT * 0.10,
                           ('Please enter connection parameters:', ''),
                           BLACK,
                           (255, 255, 255),
                           text_size=20, font_dir='fonts/Hack-Bold.ttf')
            self.key_handler = KeyboardHandler(ip_prompt)
            to_draw.append(hint)
            to_draw.append(ip_prompt)
            buttons.append(self.button_client)
            buttons.append(self.button_server)

        while state.scene_type == 'online':
            screen.fill(WHITE)
            text.draw(screen)
            for elem in to_draw:
                elem.draw(screen)
            io.draw_all_buttons(buttons)
            # popup.draw(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if self.key_handler:
                    self.key_handler(event)
                io.check_all_buttons(event, buttons)


class KeyboardHandler:
    ipv4_ptr = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?):[1-5][0-9]{4}$'''

    def __init__(self, prompt):
        self.disabled = False
        self.prompt = prompt
        self.content = ''
        self.state = 0
        self.dig_state = [0, 0, 0, 0, 0]
        self.ok = False

    def disable(self, value):
        self.disabled = value
    def get_status(self):
        return self.ok

    def __call__(self, event, *args, **kwargs):
        if not self.disabled:
            if event.type == pygame.KEYDOWN:
                key = event.dict.get('key')
                if pygame.K_0 <= key <= pygame.K_9:
                    if self.state <= 3:
                        if self.dig_state[self.state] <= 2:
                            self.content += str(key - pygame.K_0)
                            self.dig_state[self.state] += 1

                    elif self.dig_state[4] <= 4:
                        self.content += str(key - pygame.K_0)
                        self.dig_state[self.state] += 1
                        if len(re.findall(self.ipv4_ptr, self.content)) > 0:
                            self.prompt.set_status(True)
                            self.ok = True
                if key == pygame.K_BACKSPACE and len(self.content) > 0:
                    self.prompt.set_status(False)
                    self.ok = False
                    if self.content[len(self.content) - 1] == '.':
                        self.state -= 1
                    elif self.content[len(self.content) - 1] == ':':
                        self.state -= 1
                    else:
                        self.dig_state[self.state] -= 1
                    self.content = self.content[:-1]
                if key == pygame.K_PERIOD:
                    if self.dig_state[self.state] > 0 and self.state < 3:
                        self.content += '.'
                        self.state += 1
                if key == pygame.K_SEMICOLON:
                    if self.state == 3 and self.dig_state[3] > 0:
                        self.content += ':'
                        self.state += 1

                self.prompt.update_text(self.content)

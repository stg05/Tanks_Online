import random
import re

import pygame
from tools import conn
from models.constants import state
from models.constants.color import *
from models.constants.general import *
from models import interface_objects as io


class OnlineScene:
    @staticmethod
    def init_connection():
        print('conn')
        host = input()
        srv = None
        count = 0
        while srv is None and count < 5:
            port = random.randint(40000, 49999)
            srv = conn.open_port(host, port)
            count += 1

    def __init__(self, screen):
        global key_handler
        self.port = None
        self.srv = None
        ip = conn.find_ip()
        button_exit = io.Button(screen, WIDTH * 0.95, HEIGHT * 0.05, WIDTH * 0.10, HEIGHT * 0.10,
                                RED, BLACK, "Exit", io.menu, text_size=36, font_dir='fonts/Army.ttf')

        button_client = io.Button(screen, WIDTH * 0.50, HEIGHT * 0.38, WIDTH * 0.20, HEIGHT * 0.10,
                                  BLUE, BLACK, 'Connect to...', lambda: None, text_size=36, font_dir='fonts/Army.ttf')
        button_server = io.Button(screen, WIDTH * 0.50, HEIGHT * 0.52, WIDTH * 0.20, HEIGHT * 0.10,
                                  BLUE, BLACK, 'Initiate...', self.init_connection, text_size=36,
                                  font_dir='fonts/Army.ttf')

        buttons = [button_exit]
        to_draw = []
        if not ip:
            text = io.Text(WIDTH * 0.50, HEIGHT * 0.50, WIDTH * 0.40, HEIGHT * 0.60,
                           ("You're not connected to the internet", "Try again later!"),
                           RED,
                           BLACK,
                           48)
        else:
            text = io.Text(WIDTH * 0.50, HEIGHT * 0.10, WIDTH * 0.35, HEIGHT * 0.20,
                           ('Please use following IP:', f'IP: {conn.find_ip()}', f'PORT: NONE'),
                           GREEN, BLACK, text_size=36, font_dir='fonts/Army.ttf')
            ip_prompt = io.TextPrompt(WIDTH * 0.50, HEIGHT * 0.30, WIDTH * 0.20, HEIGHT * 0.10, '',
                                      text_size=20, font_dir='fonts/Hack-Bold.ttf')
            hint = io.Text(WIDTH * 0.50, HEIGHT * 0.28, WIDTH * 0.35, HEIGHT * 0.10,
                           ('Please enter connection parameters:', ''),
                           BLACK,
                           (255, 255, 255),
                           text_size=20, font_dir='fonts/Hack-Bold.ttf')
            key_handler = KeyboardHandler(ip_prompt)
            to_draw.append(hint)
            to_draw.append(ip_prompt)
            buttons.append(button_client)
            buttons.append(button_server)

        while state.scene_type == 'online':
            screen.fill(WHITE)
            text.draw(screen)
            for elem in to_draw:
                elem.draw(screen)
            io.draw_all_buttons(buttons)
            # popup.draw(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if key_handler:
                    key_handler(event)
                io.check_all_buttons(event, buttons)


class KeyboardHandler:
    ipv4_ptr = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?):[3-5]{5}$'''

    def __init__(self, prompt):
        self.prompt = prompt
        self.content = ''
        self.state = 0
        self.dig_state = [0, 0, 0, 0, 0]

    def __call__(self, event, *args, **kwargs):
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
            if key == pygame.K_BACKSPACE and len(self.content) > 0:
                self.prompt.set_status(False)
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
                print('gachi')
                if self.state == 3 and self.dig_state[3] > 0:
                    self.content += ':'
                    self.state += 1

            self.prompt.update_text(self.content)

import random
import re
import socket
from multiprocessing import Process
from threading import Thread

import pygame
from tools import conn
from sounds import sound
from models.constants import state
from models.constants.color import *
from models.constants.general import *
from models.entities import tanks_classes as tnk_cls
from models.entities import tanks_physics as tnk_ph
from models import interface_objects as io


class OnlineInputScene:
    def wait_incoming(self, ip, port):
        self.order = state.MASTER
        self.status_bar.text[1] = 'Waiting for incoming connections...'
        self.status_bar.color = BLACK
        self.srv = conn.wait_incoming(ip, port)

    def wait_connection(self, ip, port):
        self.order = state.SLAVE
        self.status_bar.text[1] = 'Connection trial...'
        self.status_bar.color = BLACK
        self.srv = conn.send_inquiry(ip, port)

    def check_for_connection(self):
        while True:
            if self.srv is not None:
                if type(self.srv) == socket.socket:
                    print(self.srv)
                    state.scene_type = 'online'
                    state.socket = self.srv
                    state.order = self.order
                    break
                elif self.srv == conn.REFUSED:
                    self.status_bar.text[1] = 'Connection failed: REFUSED'
                    self.status_bar.color = RED
                    self.button_client.disable(False)
                    self.button_server.disable(False)
                    self.key_handler.disable(False)
                    break
                elif self.srv == conn.TIMEOUT:
                    self.status_bar.text[1] = 'Connection failed: TIMEOUT'
                    self.status_bar.color = RED
                    self.button_client.disable(False)
                    self.button_server.disable(False)
                    self.key_handler.disable(False)
                    break
                elif self.srv == conn.WRONGADDRESS:
                    self.status_bar.text[1] = 'Connection failed: WRONG ADDRESS'
                    self.status_bar.color = RED
                    self.button_client.disable(False)
                    self.button_server.disable(False)
                    self.key_handler.disable(False)
                    break

    def init_connection(self):
        if self.key_handler.ok:
            self.srv = None
            self.button_client.disable(True)
            self.button_server.disable(True)
            self.key_handler.disable(True)
            ip, port = self.key_handler.content.split(":")
            port = int(port)
            t = Thread(target=self.wait_incoming, args=(ip, port))
            t.start()
            t2 = Thread(target=self.check_for_connection)
            t2.start()

    def connect_to(self):
        if self.key_handler.ok:
            self.srv = None
            self.button_client.disable(True)
            self.button_server.disable(True)
            self.key_handler.disable(True)
            ip, port = self.key_handler.content.split(":")
            port = int(port)
            t = Thread(target=self.wait_connection, args=(ip, port))
            t.start()
            t2 = Thread(target=self.check_for_connection)
            t2.start()

    def __init__(self, screen):
        self.order = None
        self.key_handler = None
        self.port = None
        self.screen = screen
        self.ip = conn.find_ip()
        self.port = conn.find_port()
        self.srv = None
        ip = conn.find_ip()
        self.button_exit = io.Button(screen, WIDTH * 0.95, HEIGHT * 0.05, WIDTH * 0.10, HEIGHT * 0.10,
                                     RED, BLACK, "Exit", io.menu, text_size=36, font_dir='fonts/Army.ttf')

        self.button_client = io.Button(screen, WIDTH * 0.50, HEIGHT * 0.45, WIDTH * 0.20, HEIGHT * 0.10,
                                       BLUE, BLACK, 'Connect to...', self.connect_to, text_size=36,
                                       font_dir='fonts/Army.ttf')
        self.button_server = io.Button(screen, WIDTH * 0.50, HEIGHT * 0.60, WIDTH * 0.20, HEIGHT * 0.10,
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

            self.status_bar = io.Text(WIDTH * 0.50, HEIGHT * 0.90, WIDTH, HEIGHT * 0.20,
                                 ['-S-T-A-T-U-S-', ''],
                                 BLACK, (255, 255, 255), text_size=36, font_dir='fonts/Hack-Bold.ttf')
            self.key_handler = KeyboardHandler(ip_prompt)
            to_draw.append(hint)
            to_draw.append(ip_prompt)
            to_draw.append(self.status_bar)
            buttons.append(self.button_client)
            buttons.append(self.button_server)

        while state.scene_type == 'online_connection':
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


class OnlineScene:
    def __init__(self, screen, socket, count=(0, 0)):
        print('playing online')
        button_exit = io.Button(screen, WIDTH * 0.95, HEIGHT * 0.05, WIDTH * 0.10, HEIGHT * 0.10,
                                RED,
                                BLACK, "Exit", io.menu)

        buttons = [button_exit]
        self.count = count
        self.socket = socket
        missiles = []

        clock = pygame.time.Clock()
        tank1 = tnk_cls.TankModel2(screen, rev=False, pt0=(100, 450), controlled_externally=False)
        tank2 = tnk_cls.CruiserWithMinigun(screen, rev=True, pt0=(WIDTH - 100, 450), controlled_externally=True)
        tank1.set_bounds(80, WIDTH / 2 - 400)
        tank2.set_bounds(WIDTH / 2 + 300, WIDTH - 80)
        tanks = [tank1, tank2]

        finished = False
        snd = sound.SoundLoader()

        while state.scene_type == 'online':
            screen.fill(WHITE)

            # DRAWING PART
            io.draw_all_missiles(missiles)
            io.draw_all_tanks(tanks)
            io.draw_all_buttons(buttons)
            clock.tick(FPS)
            tick = 1.0 / FPS
            pygame.display.update()

            # CHECKING EVENTS
            for event in pygame.event.get():
                io.check_all_buttons(event, buttons)
                io.check_tank_events(event, tank1, missiles)
                io.check_tank_events(event, tank2, missiles)

            # MOVEMENT
            for tank in tanks:
                tank.move_gun(tick)
                tank.move(tick)
                tank.processDisabled(tick)
                tank.gun.power_up()
                tank.gun.fire_action(missiles)

            # PROJECTILE PROCESSING
            for b in missiles:
                b.move(tick)
                if b.y > HEIGHT:
                    missiles.remove(b)
                    del b
                    continue

                for t in tanks:
                    hit, target = t.check_collision(b)
                    if hit:
                        if t.hp <= 0:
                            t.hp = 0
                            t.health_bar.update(t.x, t.y, t.hp)
                            t.health_bar.draw()
                            pygame.display.update()
                            if t == tank1:
                                snd.play_sound(sound.READY, sound.DE)
                            elif t == tank2:
                                snd.play_sound(sound.READY, sound.PL)
                            pygame.time.delay(3000)
                            state.scene_type = 'online'
                            break
                        if not target:
                            if t == tank2:
                                snd.play_sound(sound.HOORAY, sound.PL)
                            elif t == tank1:
                                snd.play_sound(sound.HOORAY, sound.DE)
                        if target == tnk_ph.TRACK:
                            if t == tank2:
                                snd.play_sound(sound.TRACK, sound.DE)
                            if t == tank1:
                                snd.play_sound(sound.TRACK, sound.PL)
                        if target == tnk_ph.TOWER:
                            if t == tank2:
                                snd.play_sound(sound.TOWER, sound.DE)
                            if t == tank1:
                                snd.play_sound(sound.TOWER, sound.PL)
                        if target == tnk_ph.GUN:
                            if t == tank2:
                                snd.play_sound(sound.GUN, sound.DE)
                            if t == tank1:
                                snd.play_sound(sound.GUN, sound.PL)
                        missiles.remove(b)
                        break

import re
import socket
import pygame

from threading import Thread

from models.entities.missiles import Missile
from sounds import sound
from tools import conn

from models.constants import state
from models.constants.color import *
from models.constants.general import *
from models.constants.online_events import *
from models import interface_objects as io
from models.entities.envobjects import Divider
from models.entities import tanks_classes as tnk_cls
from models.entities import tanks_physics as tnk_ph


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
            state.socket_order = state.MASTER
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
            state.socket_order = state.SLAVE
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
    def __init__(self, screen, count=(0, 0)):
        button_exit = io.Button(screen, WIDTH * 0.95, HEIGHT * 0.05, WIDTH * 0.10, HEIGHT * 0.10,
                                RED,
                                BLACK, "Exit", io.menu)

        buttons = [button_exit]
        self.count = count
        missiles = []
        ev_queue_in = []
        ev_queue_out = []
        pt0 = (WIDTH - 100, 450) if state.right_handed else (100, 450)
        pt0_rem = (100, 450) if state.right_handed else (WIDTH - 100, 450)

        self.div = Divider(screen, state.right_handed, state.socket_order != state.MASTER)

        target_class_local = tnk_cls.all_classes_of_tanks[
            state.current_right_class_index if state.right_handed else state.current_left_class_index]
        tank_local = target_class_local(screen, rev=state.right_handed, pt0=pt0, controlled_externally=False)

        remote_init_data = []
        if state.socket_order == state.MASTER:
            state.socket.send(bytes(tank_local.init_params(), 'utf-8'))
            msg = state.socket.recv(1024)
            remote_init_data.extend(msg.decode('utf-8').split('\n'))
        else:
            msg = state.socket.recv(1024)
            remote_init_data.extend(msg.decode('utf-8').split('\n'))
            state.socket.send(bytes(tank_local.init_params(), 'utf-8'))

        target_class_remote = tnk_cls.all_classes_of_tanks[int(remote_init_data[0])]
        tank_remote = target_class_remote(screen, rev=not state.right_handed, pt0=pt0_rem,
                                          controlled_externally=True,
                                          reversed_externally=remote_init_data[1] == 'TRUE')

        clock = pygame.time.Clock()

        if state.right_handed:
            tank_remote.set_bounds(80, WIDTH * 0.3)
            tank_local.set_bounds(WIDTH * 0.7, WIDTH - 80)
        else:
            tank_local.set_bounds(80, WIDTH * 0.3)
            tank_remote.set_bounds(WIDTH * 0.7, WIDTH - 80)
        tanks = [tank_local, tank_remote]

        snd = sound.SoundLoader()

        def communicate():
            while state.scene_type == 'online':
                mis_info = '\n'
                for missile in missiles:
                    if not missile.guided_externally:
                        mis_info += str(missile) + '\n'

                ev_info = '\n'
                for ev in ev_queue_out:
                    ev_info += ev + '\n'
                    ev_queue_out.remove(ev)

                if state.socket_order == state.MASTER:
                    # TANKS POSITIONS
                    state.socket.send(bytes(str(tank_local), 'utf-8'))
                    tank_remote.append_incoming(state.socket.recv(1024).decode('utf-8'))
                    # MISSILE EVENTS
                    state.socket.send(bytes(mis_info, 'utf-8'))
                    Missile.handle_info(state.socket.recv(1024).decode('utf-8'), missiles)
                    # MISSILES' POSITIONS
                    state.socket.send(bytes(ev_info, 'utf-8'))
                    events_incoming = state.socket.recv(1024).decode('utf-8').strip('\n').split('\n')
                    for ev in events_incoming:
                        Missile.handle_event(screen, ev, missiles, tank_local)
                    # DIVIDER'S POSITION
                    state.socket.send(bytes(str(self.div), 'utf-8'))
                    state.socket.recv(1024)
                else:
                    # TANKS POSITIONS
                    tank_remote.append_incoming(state.socket.recv(1024).decode('utf-8'))
                    state.socket.send(bytes(str(tank_local), 'utf-8'))
                    # MISSILE EVENTS
                    Missile.handle_info(state.socket.recv(1024).decode('utf-8'), missiles)
                    state.socket.send(bytes(mis_info, 'utf-8'))
                    # MISSILES' POSITIONS
                    events_incoming = state.socket.recv(1024).decode('utf-8').strip('\n').split('\n')
                    for ev in events_incoming:
                        Missile.handle_event(screen, ev, missiles, tank_local)
                    state.socket.send(bytes(ev_info, 'utf-8'))
                    # DIVIDER'S POSITION
                    self.div.append_incoming(state.socket.recv(1024).decode('utf-8'))
                    state.socket.send(bytes('T-A-N-K-S RECEIVED', 'utf-8'))

        t = Thread(target=communicate)
        t.start()

        while state.scene_type == 'online':
            screen.fill(WHITE)

            # DRAWING PART
            background_image = io.current_background_image()
            screen.blit(background_image, (0, 0))
            io.draw_all_missiles(missiles)
            io.draw_all_tanks(tanks)
            io.draw_all_buttons(buttons)
            self.div.draw()

            clock.tick(FPS)
            tick = 1.0 / FPS
            pygame.display.update()

            if not self.div.guided_externally:
                self.div.update()

            # CHECKING EVENTS
            for event in pygame.event.get():
                io.check_all_buttons(event, buttons)
                io.check_tank_events(event, tank_local, missiles)
                io.check_tank_events(event, tank_remote, missiles)

            # MOVEMENT
            for tank in tanks:
                tank.move_gun(tick)
                tank.move(tick)
                tank.processDisabled(tick)
                tank.gun.power_up()
                tank.gun.fire_action(missiles)

            # PROJECTILE PROCESSING
            for event in ev_queue_in:
                Missile.handle_event(screen, event, missiles)
                ev_queue_in.remove(event)

            for b in missiles:
                if not b.guided_externally:
                    b.move(tick)
                    if b.new:
                        b.new = False
                        ev_queue_out.append(Missile.report_event(STATUS_CREATE, b))

                    if b.y > HEIGHT:
                        missiles.remove(b)
                        ev_queue_out.append(Missile.report_event(STATUS_DEL, b))
                        del b
                        continue

                    if self.div.check_collision(b):
                        snd.play_sound(sound.FAIL, sound.DE)
                        missiles.remove(b)
                        ev_queue_out.append(Missile.report_event(STATUS_DEL, b))
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
                                ev_queue_out.append(Missile.report_event(STATUS_DEADLY_HIT, b, target))
                                if t == tank_local:
                                    snd.play_sound(sound.READY, sound.DE)
                                elif t == tank_remote:
                                    snd.play_sound(sound.READY, sound.PL)
                                pygame.time.delay(3000)
                                state.scene_type = 'online'
                                break
                            if not target:
                                if t == tank_remote:
                                    snd.play_sound(sound.HOORAY, sound.PL)
                                elif t == tank_local:
                                    snd.play_sound(sound.HOORAY, sound.DE)
                            if target == tnk_ph.TRACK:
                                if t == tank_remote:
                                    snd.play_sound(sound.TRACK, sound.DE)
                                if t == tank_local:
                                    snd.play_sound(sound.TRACK, sound.PL)
                            if target == tnk_ph.TOWER:
                                if t == tank_remote:
                                    snd.play_sound(sound.TOWER, sound.DE)
                                if t == tank_local:
                                    snd.play_sound(sound.TOWER, sound.PL)
                            if target == tnk_ph.GUN:
                                if t == tank_remote:
                                    snd.play_sound(sound.GUN, sound.DE)
                                if t == tank_local:
                                    snd.play_sound(sound.GUN, sound.PL)
                            ev_queue_out.append(Missile.report_event(STATUS_HIT, b, target))
                            missiles.remove(b)
                            del b
                            break

import pygame

from models import interface_objects as io
from models.constants import state
from models.constants.color import *
from models.constants.general import *
from models.entities import tanks_physics as tnk_ph
from models.entities.envobjects import Divider
from sounds import sound


class OfflineScene:

    def __init__(self, screen):
        button_exit = io.Button(screen, WIDTH * 0.96, HEIGHT * 0.03, WIDTH * 0.08, HEIGHT * 0.06,
                                GREY,
                                BLACK, "Exit", io.menu, font_dir='fonts/Army.ttf')

        buttons = [button_exit]

        missiles = []

        count_sign = io.CountSign(WIDTH * 0.5, HEIGHT * 0.10, WIDTH * 0.2, HEIGHT * 0.10, state.result)

        clock = pygame.time.Clock()
        tank_left = io.create_current_tank_model(screen, rev=False, pt0=(100, 450))
        tank_right = io.create_current_tank_model(screen, rev=True, pt0=(WIDTH - 100, 450))
        tank_left.set_bounds(80, WIDTH * 0.30)
        tank_right.set_bounds(WIDTH * 0.70, WIDTH - 80)
        tanks = [tank_left, tank_right]
        div = Divider(screen)

        snd = sound.SoundLoader()

        while state.scene_type == 'offline':
            screen.fill(WHITE)

            # DRAWING PART
            background_image = io.current_background_image()
            screen.blit(background_image, (0, 0))
            io.draw_all_missiles(missiles)
            io.draw_all_tanks(tanks)
            io.draw_all_buttons(buttons)
            div.update()
            div.draw()
            clock.tick(FPS)
            tick = 1.0 / FPS
            count_sign.draw(screen)
            pygame.display.update()

            # CHECKING EVENTS
            for event in pygame.event.get():
                io.check_all_buttons(event, buttons)
                io.check_tank_events(event, tank_left, missiles)
                io.check_tank_events(event, tank_right, missiles)

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

                if div.check_collision(b):
                    if b.origin == tank_left.gun:
                        snd.play_sound(sound.FAIL, sound.PL)
                    elif b.origin == tank_right.gun:
                        snd.play_sound(sound.FAIL, sound.DE)
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
                            if t.rev:
                                state.result[0] += 1
                            else:
                                state.result[1] += 1
                            pygame.display.update()
                            if t == tank_left:
                                snd.play_sound(sound.READY, sound.DE)
                            elif t == tank_right:
                                snd.play_sound(sound.READY, sound.PL)
                            pygame.time.delay(1500)
                            state.scene_type = 'commence_offline'
                            break
                        if not target:
                            if t == tank_right:
                                snd.play_sound(sound.HOORAY, sound.PL)
                            elif t == tank_left:
                                snd.play_sound(sound.HOORAY, sound.DE)
                        if target == tnk_ph.TRACK:
                            if t == tank_right:
                                snd.play_sound(sound.TRACK, sound.DE)
                            if t == tank_left:
                                snd.play_sound(sound.TRACK, sound.PL)
                        if target == tnk_ph.TOWER:
                            if t == tank_right:
                                snd.play_sound(sound.TOWER, sound.DE)
                            if t == tank_left:
                                snd.play_sound(sound.TOWER, sound.PL)
                        if target == tnk_ph.GUN:
                            if t == tank_right:
                                snd.play_sound(sound.GUN, sound.DE)
                            if t == tank_left:
                                snd.play_sound(sound.GUN, sound.PL)
                        missiles.remove(b)
                        break

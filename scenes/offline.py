import pygame

from models.constants import state
from models.constants.color import *
from models.constants.general import *
from models.entities.envobjects import Divider
from models.entities import tanks_physics as tnk_ph
from models.entities import tanks_classes as tnk_cls
from models import interface_objects as io
from sounds import sound


class OfflineScene:

    def __init__(self, screen):
        print('playing offline')
        button_exit = io.Button(screen, WIDTH * 0.95, HEIGHT * 0.05, WIDTH * 0.10, HEIGHT * 0.10,
                                RED,
                                BLACK, "Exit", io.menu)

        buttons = [button_exit]

        missiles = []

        clock = pygame.time.Clock()
        tank1 = tnk_cls.TankModel2(screen, rev=False, pt0=(100, 450))
        tank2 = tnk_cls.CruiserWithMinigun(screen, rev=True, pt0=(WIDTH - 100, 450))
        tank1.set_bounds(80, WIDTH / 2 - 400)
        tank2.set_bounds(WIDTH / 2 + 300, WIDTH - 80)
        tanks = [tank1, tank2]
        div = Divider(screen)

        finished = False
        snd = sound.SoundLoader()

        while state.scene_type == 'offline':
            screen.fill(WHITE)

            # DRAWING PART
            io.draw_all_missiles(missiles)
            io.draw_all_tanks(tanks)
            io.draw_all_buttons(buttons)
            div.update()
            div.draw()
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

                if div.check_collision(b):
                    if b.origin == tank1.gun:
                        snd.play_sound(sound.FAIL, sound.PL)
                    elif b.origin == tank2.gun:
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
                            pygame.display.update()
                            if t == tank1:
                                snd.play_sound(sound.READY, sound.DE)
                            elif t == tank2:
                                snd.play_sound(sound.READY, sound.PL)
                            pygame.time.delay(3000)
                            state.scene_type = 'menu'
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

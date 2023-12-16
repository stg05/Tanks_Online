import pygame

from models.constants import state
from models.constants.color import *
from models.constants.general import *
from models.entities.envobjects import Divider
from models.entities import tanks as tnk
from models import interface_objects as io
from sounds import sound


class OfflineScene:
    @staticmethod
    def check_events(buttons, screen, event, tank1, tank2, missiles):

        if event.type == pygame.QUIT:
            finished = True

        elif event.type == pygame.KEYDOWN:
            key = event.dict.get('key')
            if key == pygame.K_UP:
                tank2.gun.state = UP
            elif key == pygame.K_DOWN:
                tank2.gun.state = DOWN

            elif key == pygame.K_LEFT:
                tank2.targetVx = -V
            elif key == pygame.K_RIGHT:
                tank2.targetVx = V
            elif key == pygame.K_w:
                tank1.gun.state = UP
            elif key == pygame.K_s:
                tank1.gun.state = DOWN
            elif key == pygame.K_a:
                tank1.targetVx = -V
            elif key == pygame.K_d:
                tank1.targetVx = V
            elif key == pygame.K_RETURN:
                tank2.gun.fire2_start(event)
            elif key == pygame.K_f:
                tank1.gun.fire2_start(event)
            elif key == pygame.K_r:
                tank1.gun.alterType()
            elif key == pygame.K_RSHIFT:
                tank2.gun.alterType()

        elif event.type == pygame.KEYUP:
            key = event.dict.get('key')
            if key == pygame.K_UP:
                tank2.gun.state = NONE
            elif key == pygame.K_DOWN:
                tank2.gun.state = NONE
            elif key == pygame.K_LEFT:
                tank2.targetVx = 0
            elif key == pygame.K_RIGHT:
                tank2.targetVx = 0
            elif key == pygame.K_w:
                tank1.gun.state = NONE
            elif key == pygame.K_s:
                tank1.gun.state = NONE
            elif key == pygame.K_a:
                tank1.targetVx = 0
            elif key == pygame.K_d:
                tank1.targetVx = 0
            elif key == pygame.K_RETURN:
                missiles.append(tank2.gun.fire2_end(event))
            elif key == pygame.K_f:
                missiles.append(tank1.gun.fire2_end(event))

    def __init__(self, screen):
        print('playing offline')
        button_exit = io.Button(WIDTH * 0.95, HEIGHT * 0.05, WIDTH * 0.10, HEIGHT * 0.10,
                                RED,
                                BLACK, "Exit", io.menu)

        buttons = [button_exit]

        missiles = []

        clock = pygame.time.Clock()
        tank1 = tnk.TankModel1(screen, rev=False, pt0=(100, 450))
        tank2 = tnk.TankModel2(screen, rev=True, pt0=(WIDTH - 100, 450))
        tank1.set_bounds(80, WIDTH / 2 - 400)
        tank2.set_bounds(WIDTH / 2 + 300, WIDTH - 80)
        tanks = [tank1, tank2]
        div = Divider(screen)

        finished = False
        snd = sound.SoundLoader()

        while state.scene_type == 'offline':
            screen.fill(WHITE)
            button_exit.draw(screen)
            for tank in tanks:
                tank.draw()
            for b in missiles:
                b.draw()
            div.update()
            div.draw()
            clock.tick(FPS)
            tick = 1.0 / FPS
            pygame.display.update()

            io.check_all_buttons(buttons, screen,
                                 extra_actions=lambda event: self.check_events(buttons, screen,
                                                                               event, tank1,
                                                                               tank2,
                                                                               missiles))

            # MOVEMENT
            for tank in tanks:
                tank.move_gun(tick)
                tank.move(tick)
                tank.processDisabled(tick)
                tank.gun.power_up()

            # PROJECTILE PROCESSING
            for b in missiles:
                b.move(tick)
                if b.y > HEIGHT:
                    missiles.remove(b)
                    del b
                    continue

                if div.check_collision(b.x, b.y, b.vx):

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
                            finished = True
                            break
                        if not target:
                            if t == tank2:
                                snd.play_sound(sound.HOORAY, sound.PL)
                            elif t == tank1:
                                snd.play_sound(sound.HOORAY, sound.DE)
                        if target == tnk.TRACK:
                            if t == tank2:
                                snd.play_sound(sound.TRACK, sound.DE)
                            if t == tank1:
                                snd.play_sound(sound.TRACK, sound.PL)
                        if target == tnk.TOWER:
                            if t == tank2:
                                snd.play_sound(sound.TOWER, sound.DE)
                            if t == tank1:
                                snd.play_sound(sound.TOWER, sound.PL)
                        missiles.remove(b)
                        break

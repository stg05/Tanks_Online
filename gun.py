import math
import time
import pygame
import sound
from models import tanks as tk

# COLOR DEFINITIONS

# GENERAL GRAPHICS PARAMS
WIDTH = 1500
HEIGHT = 600
FPS = 30


class Divider:
    _xAmp = 100
    _yAmp = 100
    _y0 = 400
    _nu = 5e-1
    _width = 10

    def __init__(self, screen):
        self.x = 0
        self.y = 0
        self._prev = 0
        self.screen = screen
        self.update()

    def update(self):
        self.x = WIDTH / 2 + self._xAmp * math.sin(self._nu * time.time()) + self._xAmp * math.sin(
            math.pi * self._nu * time.time())

        self.y = self._y0 + self._yAmp * math.sin(math.pi * self._nu * time.time()) + self._yAmp * math.sin(
            math.pi ** 2 * self._nu * time.time())

    def draw(self):
        pygame.draw.rect(self.screen,
                         color=tk.BLACK,
                         rect=[self.x - self._width, self.y, self._width, HEIGHT - self.y])

    def check_collision(self, x, y, vx):
        if y > self.y:
            a = -1 if vx < 0 else 1
            if self._prev * a < 0 < (x - self.x) * a:
                self._prev = (x - self.x)
                return True
        self._prev = (x - self.x)
        return False


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

missiles = []

clock = pygame.time.Clock()
tank1 = tk.TankModel1(screen, rev=False, pt0=(100, 450))
tank2 = tk.TankModel2(screen, rev=True, pt0=(WIDTH - 100, 450))
tank1.set_bounds(80, WIDTH / 2 - 400)
tank2.set_bounds(WIDTH / 2 + 300, WIDTH - 80)
tanks = [tank1, tank2]
div = Divider(screen)

finished = False
snd = sound.SoundLoader()

while not finished:
    screen.fill(tk.WHITE)
    for tank in tanks:
        tank.draw()
    for b in missiles:
        b.draw()
    div.update()
    div.draw()
    pygame.display.update()

    clock.tick(FPS)
    tick = 1.0 / FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            key = event.dict.get('key')
            if key == pygame.K_UP:
                tank2.gun.state = tk.UP
            elif key == pygame.K_DOWN:
                tank2.gun.state = tk.DOWN

            elif key == pygame.K_LEFT:
                tank2.targetVx = -tk.V
            elif key == pygame.K_RIGHT:
                tank2.targetVx = tk.V
            elif key == pygame.K_w:
                tank1.gun.state = tk.UP
            elif key == pygame.K_s:
                tank1.gun.state = tk.DOWN
            elif key == pygame.K_a:
                tank1.targetVx = -tk.V
            elif key == pygame.K_d:
                tank1.targetVx = tk.V
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
                tank2.gun.state = tk.NONE
            elif key == pygame.K_DOWN:
                tank2.gun.state = tk.NONE
            elif key == pygame.K_LEFT:
                tank2.targetVx = 0
            elif key == pygame.K_RIGHT:
                tank2.targetVx = 0
            elif key == pygame.K_w:
                tank1.gun.state = tk.NONE
            elif key == pygame.K_s:
                tank1.gun.state = tk.NONE
            elif key == pygame.K_a:
                tank1.targetVx = 0
            elif key == pygame.K_d:
                tank1.targetVx = 0
            elif key == pygame.K_RETURN:
                missiles.append(tank2.gun.fire2_end(event))
            elif key == pygame.K_f:
                missiles.append(tank1.gun.fire2_end(event))

    # MOVEMENT
    for tank in tanks:
        tank.move_gun(tick)
        tank.move(tick)
        tank.processDisabled(tick)
        tank.gun.power_up()
        print(tank.x)

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
                if target == tk.TRACK:
                    if t == tank2:
                        snd.play_sound(sound.TRACK, sound.DE)
                    if t == tank1:
                        snd.play_sound(sound.TRACK, sound.PL)
                if target == tk.TOWER:
                    if t == tank2:
                        snd.play_sound(sound.TOWER, sound.DE)
                    if t == tank1:
                        snd.play_sound(sound.TOWER, sound.PL)
                missiles.remove(b)
                break

pygame.quit()

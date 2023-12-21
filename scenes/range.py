import pygame

from models.constants import state
from models.constants.color import *
from models.constants.general import *
from models.entities.envobjects import AimCircle
from models.entities import tanks_physics as tnk_ph
from models.entities import tanks_classes as tnk_cls
from models import interface_objects as io
from scenes import background_set as bck_set
from sounds import sound


def play_range(screen):
    button_exit = io.Button(screen, WIDTH * 0.96, HEIGHT * 0.03, WIDTH * 0.08, HEIGHT * 0.06,
                                 GREY,
                                 BLACK, "Exit", io.menu, font_dir='fonts/Army.ttf')
    missiles = []
    tank_left = io.create_current_tank_model(screen, rev=False, pt0=(100, 450))
    tank_left.set_bounds(100, WIDTH * 0.3)
    aim_circle = AimCircle(screen)
    tanks = [tank_left]
    buttons = [button_exit]
    clock = pygame.time.Clock()
    if bck_set.current_background_index == 0:
        score_color = BLACK
    else:
        score_color = GREY

    while state.scene_type == 'range':
        screen.fill(WHITE)
        background_image = io.current_background_image()
        screen.blit(background_image, (0, 0))
        io.draw_all_missiles(missiles)
        io.draw_all_tanks(tanks)
        io.draw_all_buttons(buttons)
        aim_circle.update()
        aim_circle.draw()
        aim_circle.display_score(pt0 = (80, 130), font_dir= 'fonts/Army.ttf',text_size= 36 ,color= score_color)
        clock.tick(FPS)
        tick = 1.0 / FPS


        for event in pygame.event.get():
            io.check_all_buttons(event, buttons)
            io.check_tank_events(event, tank_left, missiles)
        pygame.display.flip()

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
            if b.y > HEIGHT - 150:
                missiles.remove(b)
                del b
                continue
            if aim_circle.check_collision(b.x, b.y, b.vx):
                missiles.remove(b)
                del b
                continue


        pygame.display.flip()


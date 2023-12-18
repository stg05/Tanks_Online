import pygame
import pygame.image
import pygame

from models.constants import state
from models.constants.color import *
from models.constants.general import *
from models.entities.envobjects import Divider
from models.entities import tanks_physics as tnk_ph
from models.entities import tanks_classes as tnk_cls
from models import interface_objects as io
from sounds import sound


"""нужен был для скачивания пнг моделей танков, может еще понадобится"""


# Создаем экземпляр класса Pygame
pygame.init()

# Создаем экран, на котором будет отображаться объект
screen_width = 200
screen_height = 200
screen = pygame.display.set_mode((screen_width, screen_height))

# Создаем объект
tank = tnk_cls.TankModel2(screen, rev=False, pt0=(screen_width/2, screen_height/2))

# Создаем поверхность с поддержкой альфа-канала
image_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

# Рисуем объект на поверхности
tank.draw_hitbox(image_surface)

# Сохраняем изображение объекта в формате PNG с прозрачным фоном
pygame.image.save(image_surface, "models/entities/tank_models/object.png")

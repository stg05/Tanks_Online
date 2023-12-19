from models.entities.tanks_classes import TankModel2
import pygame
from models.constants.general import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF, 32)
t = TankModel2(screen=screen, pt0=(50, 100), rev=False)

print(str(t))

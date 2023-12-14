import pygame
import sys
sys.path.append("..")
from models import constants as const

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, const.RED, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, const.BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def check_click(self, pos, button_action):
        if self.rect.collidepoint(pos):
            button_action()
import pygame
from settings import *

class Drawable_Object(pygame.sprite.Sprite):
    def __init__(self,pos,groups, img_path = "./assets/placeholder tile.png"):
        super().__init__(groups)
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        
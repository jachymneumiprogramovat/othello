import pygame as pg
from constants import *

class Stone(pg.sprite.Sprite):
    """Class for the stone object"""
    def __init__(self, color:tuple, width, height):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface((width, height), pg.SRCALPHA).convert_alpha()
        self.image.fill(TILE_COLOR)

        self.rect = pg.draw.circle(
            self.image,
            color,
            self.image.get_rect().center,
            width // 2,
        )
    def move_to(self,x,y)->None:
        self.rect.center = (int(x), int(y))

import pygame as pg

class Stone(pg.sprite.Sprite):
    """Class for the stone object"""
    def __init__(self, color, width, height):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface((width, height), pg.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect = pg.draw.circle(
            self.image,
            color,
            self.rect.center,
            width // 2,
        )
    def move_to(self,x,y)->None:
        self.rect = pg.Rect(x, y, self.rect.width, self.rect.height)



import pygame as pg
import loguru as logger
from constants import *


class Game:
    """Class for handeling visuals"""
    def __init__(self,screen:pg.Surface):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.cell_width = self.width // 8
        self.cell_height = self.height // 8


    def setup_board(self):
        """Inits board class"""
        ...

    def _draw_grid(self):
        """Draws lines over a background"""
        background = pg.Surface(self.screen.get_size())
        background = background.convert()
        background.fill(TILE_COLOR)

        for width in range(0,self.width,self.cell_width):
            pg.draw.line(self.screen,(100,100,100),(width,0),(width,self.height))

        for height in range(0,self.height,self.cell_height):
            pg.draw.line(self.screen,(100,100,100),(0,height),(self.width,height))

    def setup_screen(self):
        """Blits the initial position and game board"""
        self._draw_grid()



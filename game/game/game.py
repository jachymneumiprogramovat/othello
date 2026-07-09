import pygame as pg
from loguru import logger
from game.constants import *
from game.stone import Stone


class Game:
    """Class for handeling visuals"""
    def __init__(self,screen:pg.Surface):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.cell_width = self.width // 8
        self.cell_height = self.height // 8

    def _draw_grid(self):
        """Draws lines over a background"""
        background = pg.Surface(self.screen.get_size())
        background = background.convert()
        background.fill(TILE_COLOR)
        self.screen.blit(background,(0,0))

        for width in range(0,self.width,self.cell_width):
            pg.draw.line(self.screen,BLACK_COLOR,(width,0),(width,self.height),2)

        for height in range(0,self.height,self.cell_height):
            pg.draw.line(self.screen,BLACK_COLOR,(0,height),(self.width,height),2)

    def _draw_stone(self,target:tuple,color:tuple)->pg.Rect:
        """Draws a stone on target and returns changed rect."""
        stone = Stone(color=color,
                        width=self.cell_width - MARGIN,
                        height=self.cell_height - MARGIN
                      )

        stone.move_to(target[0],target[1])
        self.screen.blit(stone.image,stone.rect)

        return stone.rect

    def _draw_initial_stones(self):
        """Places four stones in the middle of the board"""
        for i in range(2):
            self._draw_stone((
                (3.5 + i) * self.cell_width,
                (3.5 + i) * self.cell_height,
                ),
            color=WHITE_COLOR
            )

        for i in range(2):
            self._draw_stone((
                (4.5 - i) * self.cell_width,
                (3.5 + i) * self.cell_height,
                ),
            color=BLACK_COLOR
            )

    def setup_screen(self):
        """Blits the initial position and game board"""
        self._draw_grid()
        self._draw_initial_stones()

    def draw_squares(self,squares:list[tuple],color:tuple)->list:
        """Draw all the squares provided with color. Returns list of affected
        rects."""
        logger.debug(f'dostal jsem na nakresleni {squares}')
        affected_rects = []
        for tile in squares:
            coordinates = tuple(reversed([(x+0.5)*self.cell_height for x in tile]))
            affected_rects.append(
                self._draw_stone(
                    target=coordinates,
                    color=color
                    )
                )
        logger.debug(f'vracim seznam rectu {affected_rects}')
        return affected_rects

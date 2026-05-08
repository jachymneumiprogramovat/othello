import pygame as pg
import loguru as logger
from constants import *
from stone import Stone


class Game:
    """Class for handeling visuals"""
    def __init__(self,screen:pg.Surface):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.cell_width = self.width // 8
        self.cell_height = self.height // 8

        # self.white_stones = []
        # self.black_stones = []

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
        """Draws a stone on target and returns affected rect."""
        stone = Stone(color=color,
                        width=self.cell_width - MARGIN,
                        height=self.cell_height - MARGIN
                      )

        stone.move_to(target[0],target[1])
        self.screen.blit(stone.image,stone.rect)

        # asi nepotrebuju color_stones ale zatim to tu necham 
        # if color==WHITE_COLOR:
        #     self.white_stones.append(stone)
        # elif color==BLACK_COLOR:
        #     self.black_stones.append(stone)


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

    # def _draw_stone(self,target:tuple,color:tuple)->pg.Rect:
    #     """Draws a stone on target and returns affected rect."""
    #     stone = Stone(color=color,
    #                      width=self.cell_width,
    #                      height=self.cell_height)
    #     stone.move_to(target[0],target[1])
    #     self.screen.blit(stone.image,stone.rect)
    #     return stone.rect
        


    def draw_move(self,squares:list[tuple],color:tuple)->list:
        """Draw all the necesary squares to make a move happen. Returns list of
        affected rects."""
        
        affected_rects = []
        for target in squares:
            affected_rects.append(
                self._draw_stone(
                    target=target,
                    color=color
                    )
                )

        return affected_rects

    def highlite_moves(self,squares:list)->list:
        """ Draws a highlite stone on all the possible moves """

        affected_rects = []
        for target in squares:
            affected_rects.append(
                self._draw_stone(
                    target=target,
                    color=(*HIGHLITE_COLOR,128)
                    )
                )

        return affected_rects





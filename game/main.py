import pygame as pg 
from loguru import logger
import os
import sys
import pathlib
import numpy as np

from constants import *
from game import Game
from board import Board


def main():
    """Main function"""

    # Initing pygame
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT),pg.SRCALPHA)
    pg.display.set_caption(CAPTION)
    logger.info('Pygame setup')

    clock = pg.time.Clock()
    running = True

    
    game = Game(screen)
    game.setup_screen()
    pg.display.flip()
    logger.info('screen setup')

    board = Board()
    board.setup_board()
    logger.info('logic setup')

    board.play_move((2,4))
    logger.info(f'{board.board}')



    while running:
        clock.tick(TIKS)


        for event in pg.event.get():
            # Check quit event
            if event.type == pg.QUIT:
                logger.info("Quit signal received. Exiting...")
                running = False
            # Check mouse click
            if event.type == pg.MOUSEBUTTONDOWN:
                logger.debug("Mouse click signal received.")
                tile = tuple(np.array(event.pos)//100)
                logger.info(str(tuple(int(x) for x in reversed(tile))))
                
                board.get_possible_moves()
                to_change = board.play_move(reversed(tile))
                curr_color = 'white' if board.player ==-1 else 'black'
                game.draw_move(to_change,curr_color)






if __name__ == "__main__":
    base_dir = pathlib.Path(__file__).parent.resolve()
    logger.remove()
    logger.add(
        os.path.join(base_dir, "main.log"),
        colorize=True,
        format="<green>{file}/{function}/{line}</green> <level>{message}</level>",
        level="INFO",
    )
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{file}/{function}/{line}</green> <level>{message}</level>",
        level="INFO",
    )
    main()


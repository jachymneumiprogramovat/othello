import pygame as pg 
from loguru import logger
import os
import sys
import pathlib
import numpy as np

from game.constants import *
from game.game import Game
from game.board import Board

def main():
    """Main function"""

    os.environ['SDL_VIDEO_WINDOW_POS'] = "1100,200"
    pg.mixer.pre_init(44100, -16, 2, 2048)
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

    logger.info(f'{board.board}')


    poss_moves = board.get_possible_moves()
    pg.display.update(game.draw_squares(poss_moves,HIGHLITE_COLOR))
    logger.info(f'poss_moves')
    while running:
        clock.tick(TIKS)
        rect_to_change = []

        for event in pg.event.get():
            # Check quit event
            if event.type == pg.QUIT:
                logger.info("Quit signal received. Exiting...")
                running = False
            # Check mouse click
            if event.type == pg.MOUSEBUTTONDOWN:
                logger.debug("Mouse click signal received.")
                tile = tuple(np.array(event.pos)//100)
                tile = (tile[1],tile[0])
                logger.info(str(tuple(int(x) for x in tile)))
                
                poss_moves = board.poss_moves[board.player]
                logger.info(f'{tile},{[x for x in poss_moves]}')
                
                if not tile in poss_moves:
                    continue

                # play the move 
                new_board, to_change = board.play_move(tile)
                board.board=new_board
                curr_color = WHITE_COLOR if board.player ==-1 else BLACK_COLOR
                rect_to_change=game.draw_squares(to_change,curr_color)

                #check for end of the game
                if board.is_game_over():
                    winner = board.determine_winner()
                    logger.info(f'game won by player {winner}')
                    break

                #prepare board for next turn
                board.player *=-1
                next_poss_moves = board.get_possible_moves()

                poss_moves.remove(tile)
                rect_to_change+=game.draw_squares(poss_moves, TILE_COLOR)
                rect_to_change+=game.draw_squares(next_poss_moves,HIGHLITE_COLOR)

                logger.info(rect_to_change)
        pg.display.update(rect_to_change)





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


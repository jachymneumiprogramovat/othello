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
    os.environ['SDL_VIDEO_WINDOW_POS'] = "1100,200"
    pg.mixer.pre_init(44100, -16, 2, 2048)
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT),pg.SRCALPHA)
    pg.display.set_caption(CAPTION)
    logger.success('Pygame setup')

    clock = pg.time.Clock()
    running = True

    game = Game(screen)
    game.setup_screen()
    pg.display.flip()
    logger.success('screen setup')

    board = Board()
    board.setup_board()
    logger.success('logic setup')
    logger.info(f'{board.board}')

    poss_moves = board.get_possible_moves()
    pg.display.update(game.draw_squares(poss_moves,HIGHLITE_COLOR))
    logger.info(f'poss_moves')

    while running:
        clock.tick(TIKS)
        rects_to_change = []

        for event in pg.event.get():
            # Check quit event
            if event.type == pg.QUIT:
                logger.info("Quit signal received. Exiting...")
                running = False
            # Check mouse click
            if event.type == pg.MOUSEBUTTONDOWN:
                logger.debug("Mouse click signal received.")
                tile_width = WIDTH//100
                tile_height = HEIGHT//100

                # process the tile click
                x, y = event.pos
                tile = (y // tile_height, x // tile_width)
                logger.info(f'{tile}')
                
                poss_moves = board.poss_moves[board.player]
                logger.info(f'{tile},{[x for x in poss_moves]}')
                
                if not tile in poss_moves:
                    logger.error(f'bro doslova mas vyznacene ty kam muzes :sob:')
                    continue

                # play the move 
                tile_to_change = board.play_move(tile)
                curr_color = WHITE_COLOR if board.player ==-1 else BLACK_COLOR
                rects_to_change=game.draw_squares(tile_to_change,curr_color)

                #check for end of the game
                if board.is_game_over():
                    winner = board.determine_winner()
                    logger.info(f'game won by player {winner}')
                    break

                #prepare board for next turn
                board.player *=-1
                next_poss_moves = board.get_possible_moves()

                poss_moves.remove(tile)
                rects_to_change+=game.draw_squares(poss_moves, TILE_COLOR)
                rects_to_change+=game.draw_squares(next_poss_moves,HIGHLITE_COLOR)

                logger.info(rects_to_change)
        pg.display.update(rects_to_change)





if __name__ == "__main__":
    base_dir = pathlib.Path(__file__).parent.resolve()
    logger.remove()
    info_filter = lambda record: record["level"].name == "INFO"
    success_filter = lambda record: record["level"].name == "SUCCESS"
    error_filter = lambda record: record["level"].name == "ERROR"

    logger.add(
        os.path.join(base_dir, "main.log"),
        colorize=True,
        format="<green>{file}/{function}/{line}</green> <level>{message}</level>",
        filter=info_filter,
    )
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{file}/{function}/{line}</green> <level>{message}</level>",
        filter=info_filter,
    )
    logger.add(
        os.path.join(base_dir, "main.log"),
        colorize=True,
        format="<yellow>{file} {message} </yellow>",
        filter=success_filter
    )
    logger.add(
        sys.stdout, 
        colorize=True,
        format="<yellow>{file} {message} </yellow>",
        filter=success_filter
    )
    logger.add(
        os.path.join(base_dir, "main.log"),
        colorize=True,
        format="<red>{file}/{function}/{line} {message}</red>",
        filter=error_filter,
    )
    logger.add(
        sys.stdout,
        colorize=True,
        format="<red>{file}/{function}/{line} {message}</red>",
        filter=error_filter,
    )
    main()


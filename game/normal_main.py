import pygame as pg 
from loguru import logger
import os
import sys
import pathlib
import numpy as np

from random import choice

from game.constants import *
from game.game import Game
from game.board import Board

def normal_main(screen):
    """Main function"""
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
    while running:
        clock.tick(TIKS)
        rects_to_change = []

        for event in pg.event.get():
            if event.type == pg.QUIT:
                logger.info(choice(GOODBYE_MESSAGES))
                running = False
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
                new_board, to_change = board.play_move(tile)
                board.board=new_board
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

                logger.info(rect_to_change)
        pg.display.update(rect_to_change)

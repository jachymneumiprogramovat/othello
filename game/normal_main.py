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
    logger.info('screen setup')

    board = Board(parent=None)
    board.setup_board()
    logger.info('logic setup')

    logger.info(f'{board.board}')


    poss_moves = board.get_possible_moves()
    pg.display.update(game.draw_squares(poss_moves,HIGHLITE_COLOR))
    while running:
        clock.tick(TIKS)
        rect_to_change = []
        poss_moves = board.get_possible_moves()
            
        if not np.any(poss_moves):
            if board.is_game_over():
                winner = board.determine_winner()
                logger.info(f'Hru vyhrává hráč {winner}')
                break
            else:
                logger.info(f'Hráč {board.player} nemá tahy, skipuju.')
                board.player *= -1
                continue 

        for event in pg.event.get():
            if event.type == pg.QUIT:
                logger.info(choice(GOODBYE_MESSAGES))
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                logger.debug("Mouse click signal received.")
                tile = tuple(np.array(event.pos)//100)
                index = tile[1]*8+tile[0]
                move = np.zeros(64)
                move[index] =1
                logger.info(f'toto je index {index}')

                poss_moves = board.poss_moves[board.player]
                logger.info(f'{tile},{[x for x in poss_moves]}')

                if not poss_moves[index]:
                    continue

                # play the move
                new_board, to_change = board.play_move(index)
                to_change[index]=1
                board.board=new_board
                curr_color = WHITE_COLOR if board.player ==-1 else BLACK_COLOR
                rect_to_change=game.draw_squares(to_change,curr_color)

                #check for end of the game
                if board.is_game_over():
                    break

                #prepare board for next turn
                board.player *=-1
                next_poss_moves = board.get_possible_moves()

                poss_moves[index] =0
                rect_to_change+=game.draw_squares(poss_moves, TILE_COLOR)
                rect_to_change+=game.draw_squares(next_poss_moves,HIGHLITE_COLOR)

                logger.info(rect_to_change)
        pg.display.update(rect_to_change)
    if board.is_game_over():
        winner = board.determine_winner()
        game.award_winner(winner,board.stones[-1],board.stones[1])
        pg.display.flip()
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    logger.info(choice(GOODBYE_MESSAGES))
                    running = False

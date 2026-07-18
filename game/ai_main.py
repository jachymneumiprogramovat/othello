import numpy as np
import sys
import os
import pathlib

from random import choice

import pygame as pg
from time import time
from loguru import logger
from tqdm import tqdm


from ai.mts import MTS
from ai.mts_node import MTSNode
from ai.mts_constants import *

from game.board import Board
from game.game import Game
from game.constants import *


mts = MTS()
def get_mcts_move(board:list,player:int,rollout_count,simulation_count):
    root = MTSNode(board =board,player=-player,move=None)
    for _ in tqdm(range(rollout_count)):
        mts.rollout(root=root,simulation_count=simulation_count)
    child = mts.select_best_child(root)
    return child.move

def ai_main(screen,rollout_count=100,simulation_count=5):
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

    pg.display.update(game.draw_squares(board.poss_moves[1],HIGHLITE_COLOR))
    move_made = False
    while running:
        poss_moves = board.get_possible_moves()
        
        if not poss_moves:
            if board.is_game_over():
                winner = board.determine_winner()
                logger.info(f'Hru vyhrává hráč {winner}')
                break
            else:
                logger.info(f'Hráč {board.player} nemá tahy, skipuju.')
                board.player *= -1
                continue 

        # human player plays
        if board.player == 1:
            clock.tick(TIKS)
            rect_to_change = []

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    logger.info(choice(GOODBYE_MESSAGES))
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    move = tuple(np.array(event.pos)//100)
                    move = (move[1],move[0])
                    logger.info(f'kliknul jsi na policko {move}')
                    move_made = True
        # AI plays
        else:
            move = get_mcts_move(
                board.board,
                -board.player,
                rollout_count=rollout_count,
                simulation_count=simulation_count
            )
            logger.info(f'AI si vybralo tah {move}')
            poss_moves = board.get_possible_moves()
            move_made = True

        if move_made:
            # generic resolving of the move
            if move not in poss_moves:
                logger.info('nepodváděj kámo')
                continue

            # play the move
            new_board, to_change = board.play_move(move)
            board.board=new_board
            logger.info(f'zahral jsem tah {move} a deska je {board.board}')
            curr_color = BLACK_COLOR if board.player ==1 else WHITE_COLOR
            rect_to_change=game.draw_squares(to_change,curr_color)

            #check for end of the game
            if board.is_game_over():
                break

            #prepare board for next turn
            board.player *=-1
            next_poss_moves = board.get_possible_moves()

            poss_moves.remove(move)
            rect_to_change+=game.draw_squares(poss_moves, TILE_COLOR)
            rect_to_change+=game.draw_squares(next_poss_moves,HIGHLITE_COLOR)
            
            move_made = False

        pg.display.update(rect_to_change)

    if board.is_game_over():
        winner = board.determine_winner()
        game.award_winner(winner,board.stones[1],board.stones[-1])
        pg.display.flip()
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    logger.info(choice(GOODBYE_MESSAGES))
                    running = False


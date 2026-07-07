import numpy as np
import sys
import os
import pathlib

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

logger.remove()
logger.add(sys.stderr, level="ERROR")

mts = MTS()
def get_mcts_move(board:list,player:int):
    root = MTSNode(board =board,player=-player,move=None)
    for _ in tqdm(range(ROLLOUT_COUNT)):
        mts.rollout(root=root)
    child = mts.select_best_child(root)
    return child.move

def ai_main():
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

    pg.display.update(game.draw_squares(board.poss_moves[1],HIGHLITE_COLOR))
    move_made = False
    while running:
        poss_moves = board.get_possible_moves()
        
        if not poss_moves:
            if board.is_game_over():
                winner = board.determine_winner()
                logger.info(f'Game won by player {winner}')
                break
            else:
                logger.info(f'Player {board.player} has no valid plays. Passing turn.')
                board.player *= -1
                continue 

        # human player plays
        if board.player == 1:
            clock.tick(TIKS)
            rect_to_change = []

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    logger.info("Quit signal received. Exiting...")
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    logger.debug("Mouse click signal received.")
                    move = tuple(np.array(event.pos)//100)
                    move = (move[1],move[0])
                    move_made = True
        # AI plays
        else:
            move = get_mcts_move(board.board,-board.player)
            poss_moves = board.get_possible_moves()
            move_made = True

        if move_made:
            # generic resolving of the move
            if move not in poss_moves:
                continue
            if not poss_moves:
                board.player *=-1
                continue

            # play the move
            new_board, to_change = board.play_move(move)
            board.board=new_board
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
            logger.info(rect_to_change)
            
            move_made = False

        pg.display.update(rect_to_change)

    if board.is_game_over():
        winner = board.determine_winner()
        logger.info(f'game won by player {winner}')

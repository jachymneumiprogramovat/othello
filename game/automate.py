from game.board import Board
import numpy as np
from random import randint
import matplotlib.pyplot as plt
import time
from loguru import logger
from tqdm import tqdm
"""
Othello played automatically and randomly to gather inside of the game
"""

logger.remove()

ITERATIONS = 1

board = Board()
board.setup_board()

number_poss_moves = []
number_of_moves = 0
board.get_possible_moves()
white_stones = []
end_states = set()
start = time.time()


for i in range(ITERATIONS):
    moves_chosen = []
    while not board.is_game_over():
        poss_moves = board.get_possible_moves()

        number_poss_moves.append(len(poss_moves))
        white_stones.append(board.stones[-1])
        if not poss_moves:
            board.player *=-1
            continue
        number_of_moves+=1

        move = poss_moves[randint(0,len(poss_moves)-1)]
        moves_chosen.append(move)
        board.board, _ = board.play_move(move)
        board.player *=-1
    end_states.add(str(board.board))
    # print(moves_chosen)
    board.setup_board()
    board.stones[-1] = 0
    board.stones[1] = 0
    for row in board.board:
        for tile in row:
            board.stones[tile]+=1
    # print(board.is_game_over())
end=time.time()
# print(board.determine_winner())
#print(number_poss_moves)
#print(number_of_moves)
print(end-start)
print(len(end_states))
white_poss_moves = number_poss_moves[::2]
#print(white_poss_moves)
#plt.plot(range(len(white_poss_moves)),white_poss_moves,color='blue')
#print(white_stones)
#plt.plot(range(len(white_stones[::2])),white_stones[::2],color='red')

#plt.plot(range(len(number_poss_moves)),number_poss_moves)
#plt.show()





board = Board()
board.setup_board()
board.get_possible_moves()
print(board.poss_moves,board.poss_anchors)

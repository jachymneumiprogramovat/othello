from board import Board
import numpy as np
from random import randint
import matplotlib.pyplot as plt

"""
Othello played automatically and randomly to gather inside of the game
"""

board = Board()
board.setup_board()

number_poss_moves = []
number_of_moves = 0
board.get_possible_moves()
white_stones = []
while not board.is_game_over():
    poss_moves = board.get_possible_moves()
    print(poss_moves, board.poss_moves)
    
    number_poss_moves.append(len(poss_moves))
    white_stones.append(len(board.white_stones))
    if not poss_moves:
        board.player *=-1
        continue
    number_of_moves+=1

    move = poss_moves[randint(0,len(poss_moves)-1)]
    board.play_move(move)
    board.player *=-1
print(board.determine_winner())
print(number_poss_moves)
print(number_of_moves)

white_poss_moves = number_poss_moves[::2]
print(white_poss_moves)
plt.plot(range(len(white_poss_moves)),white_poss_moves,color='blue')
print(white_stones)
plt.plot(range(len(white_stones)),white_stones,color='red')


#plt.plot(range(len(number_poss_moves)),number_poss_moves)
plt.show()

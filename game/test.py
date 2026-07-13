import numpy as np

from game.board import Board

def pretty_print(board):
    repr=[]
    for i in range(64):
        if board[1][i]:
            repr.append(' 1')
        elif board[-1][i]:
            repr.append('-1')
        else:
            repr.append(' 0')
    repr_string = ''
    for i in range(8):
        repr_string+= ' '.join(repr[i*8:(i+1)*8])
        repr_string+='\n'
    print(repr_string)


board = Board()
board.setup_board()
pretty_print(board.board)
pretty_print([0,board.poss_moves[1],np.zeros(64)])

board.board, _ =board.play_move(19)
board.player *=-1

pretty_print(board.board)
board.get_possible_moves()
pretty_print([0,np.zeros(64),board.poss_moves[-1]])

from game.constants import *
from loguru import logger
import numpy  as np
from copy import deepcopy

class Board:
    """Class for handeling the logic behind the game"""
    def __init__(self):
        self.board = [None, np.zeros(64), np.zeros(64)]
        self.player = 1
        self.dirs = [1,-1,8,-8,7,-7,9,-9]

        self.stones = [0, 0,0]
        self.poss_moves = [0, [], []] #na indexu hrace je seznam moznych tahu

    def __repr__(self)->str:
        repr=[]
        for i in range(64):
            if self.board[1][i]:
                repr.append(' 1')
            elif self.board[-1][i]:
                repr.append('-1')
            else:
                repr.append(' 0')
        repr_string = ''
        for i in range(8):
            repr_string+= ' '.join(repr[i*8:(i+1)*8])
            repr_string+='\n'
        return repr_string
    def setup_board(self):
        """Prepares the board for a new game."""
        self.player=1

        self.board = [None, np.zeros(64), np.zeros(64)]
        self.board[-1][3*8 + 3] = 1
        self.board[-1][4*8+4]=1
        self.stones[-1] =2

        self.board[1][3*8+4]=1
        self.board[1][4*8+3]=1
        self.stones[1] =2

        #one large board with ones where the player can move
        self.poss_moves = [0, np.zeros(64), np.zeros(64)]

        #setting up the initial possible moves
        for i in [19,26,37,44]:
            self.poss_moves[1][i] =1

        # no anchors in this version the play_move function has to find them on
        # its own
    def _valid_neighbor(self,index1,index2)->bool:
        if 0>index1 or index1>=64:
            return False
        if 0>index2 or index2>=64:
            return False
        if abs(index1//8 -index2//8)>1 or abs(index1%8 - index2%8)>1:
            return False
        return True



    def _has_anchors(self,index:int)->bool:
        """ Checks if index has an anchor and returns the truth value of that
        statement ."""

        op_player = -self.player
        for dir in self.dirs:
            nindex = dir+index
            if not self._valid_neighbor(nindex,index):
                continue

            if not self.board[op_player][nindex]: # op tam nema kamen - ma tam nulu
                continue

            it_index = nindex
            while True:
                enemy_stone = self.board[op_player][it_index]
                my_stone = self.board[self.player][it_index]

                if enemy_stone:
                    pass
                elif my_stone:
                    return True
                else:
                    break

                if not self._valid_neighbor(it_index,it_index+dir):
                    break
                it_index += dir
        return False

    def play_move(self,index:int)->tuple[list]:
        """ Returns a new board with the move played and the tiles that
        changed. """

        board = deepcopy(self.board)

        # placing the actual stone
        logger.debug(f'kliknute policko: {index}')
        board[self.player][index] =1

        self.stones[self.player] +=1


        if not self.poss_moves[self.player][index]:
            logger.error(f'tah na {index} neni v moznych tazich, idk jak se tohle deje kamo')
        changed = []
        op_player = -self.player
        for dir in self.dirs:
            nindex = dir+index
            if not self._valid_neighbor(nindex,index):
                continue
            
            if not self.board[op_player][nindex]: # op tam nema kamen - ma tam nulu
                continue
            logger.debug(f'nasel jsem opa na {nindex}')

            it_index = nindex
            to_convert = []
            while True:
                enemy_stone = self.board[op_player][it_index]
                my_stone = self.board[self.player][it_index]

                if enemy_stone:
                    logger.debug(f'enemy stone on {it_index}')
                    to_convert.append(it_index)
                
                elif my_stone:
                    logger.debug(f'my stone on {it_index},{dir},{to_convert}')
                    changed.append(to_convert)
                    for i in to_convert:
                        logger.debug(f'konvertuju {i}')
                        board[op_player][i] = 0
                        board[self.player][i] = 1

                        self.stones[self.player] += 1
                        self.stones[op_player] -= 1
                    break
                else:
                    break

                if not self._valid_neighbor(it_index,it_index+dir):
                    break
                it_index += dir
        return (board,changed)

    def get_possible_moves(self):
        """ Overwrites and returns list of possible moves for the current player """

        poss_index = []
        for index in range(64):
            if self.board[self.player][index] or self.board[-self.player][index]:
                continue
            if self._has_anchors(index):
                poss_index.append(index)

        poss_moves = np.zeros(64)
        logger.debug(f'mozne indexy jsou {poss_index}')
        for i in poss_index:
            poss_moves[i]=1

        if np.sum(poss_moves)==0:
            poss_moves = np.append(poss_moves,1)
        else:
            poss_moves = np.append(poss_moves,0)

        self.poss_moves[self.player] = poss_moves
        logger.debug(f'{self.poss_moves[self.player]}, {len(self.poss_moves[self.player])}')

        return poss_moves

    def is_game_over(self):
        """Determins if the game is over. Either because one player does not
        have stones or both are impotent."""

        if not self._stones_left():
            return True
        
        if not np.sum(self.poss_moves[1])-self.poss_moves[1][64]:
            if not np.sum(self.poss_moves[-1])-self.poss_moves[-1][64]:
                if self.stones[1] + self.stones[-1] != 4:
                    return True
        return False

    def determine_winner(self):
        """Checks the number of stones left and return the number of winning
        player"""

        if self.stones[-1]>self.stones[1]:
            return -1
        if self.stones[-1]<self.stones[1]:
            return 1
        return 0

    def _stones_left(self):
        """Checks if any player is out of stones"""

        if not self.stones[1]:
            return False
        if not self.stones[-1]:
            return False
        return True



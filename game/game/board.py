from game.constants import *
from loguru import logger
import numpy  as np
from copy import deepcopy

class Board:
    """Class for handeling the logic behind the game"""
    def __init__(self):
        self.board = np.array([[0 for _ in range(8)] for _ in range(8)])
        self.player = 1
        self.dirs = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,-1),(-1,1)]

        self.stones = [0, 0,0]
        self.poss_moves = [0, [], []] #na indexu hrace je seznam moznych tahu
        self.poss_anchors = [None, [], []]

    def setup_board(self):
        self.board[3][3]=-1
        self.board[4][4]=-1
        self.stones[-1] +=2

        self.board[3][4]=1
        self.board[4][3]=1
        self.stones[1] +=2
        logger.info(f'{self.board}',f'{self.stones}')

    def _find_anchors(self,tile:tuple[int])->list:
        """ Finds all the anchors and returns them ."""

        anchors = []
        op_player = -self.player
        for dir in self.dirs:
            try:
                if self.board[tuple(np.add(tile,dir))]!=op_player:
                    continue
            except:
                continue

            for i in range(1,len(self.board)):
                examined = tuple(np.add(tile,tuple(np.array(dir)*i)))
                try:
                    teritory = self.board[examined]
                except:
                    continue
                # does not break only if in this direction are stones of
                # opposite color
                # print(f'on tile: {examined} is player: {teritory}, {self.player}, {anchors}')
                if teritory == self.player:
                    #logger.info(f'pridal jsem pole {examined} jako anchor pro {tile}')
                    anchors.append(examined)
                    break
                elif teritory == 0:
                    break
        return anchors

    def play_move(self,tile:tuple[int]):
        """ Returns a new board with the move played and the tiles that
        changed. """

        board = np.array(deepcopy(self.board))

        # placing the actual stone
        tile = tuple(tile)
        # logger.info(f'kliknute policko: {tile}, hrac na tomto policku:{board[tuple(tile)]}')
        board[tile] = self.player
        self.stones[self.player] +=1
        # converting stones
        anchors = []
        # logger.info(f'mozne tahy: {self.poss_moves}, jejich anchori: {self.poss_anchors}')

        anchor_index = self.poss_moves[self.player].index(tile)
        anchors = self.poss_anchors[self.player][anchor_index]
        if not anchors:
            logger.error('Alegedly possible tile without anchors, wtf')
        #logger.info(f'anchori jsou {anchors}')

        converted = []
        for anchor in anchors:
            difference = tuple(anchor[i]-tile[i] for i in range(2))
            distance = max([abs(x) for x in difference])
            direction = tuple(np.array(difference)//distance)
            # logger.info(f'difference:{difference},distanece:{distance},direction:{direction}')

            for i in range(1,distance):
                vzdalenost = tuple(int(x)*i for x in direction)
                looking_at = tuple(np.add(tile,vzdalenost))

                converted.append(looking_at)
                # logger.info(f'konvertoval jsem {looking_at}')
                board[looking_at] *= -1
                self.stones[self.player]+=1
                self.stones[-self.player]-=1
                # logger.info(f'bily ma {self.stones[-1]} kamenu a cerny ma {self.stones[1]} kamenu')

                if board[looking_at] == 0:
                    logger.error('There should always be stone between tile and anchor')
        converted.append(tile)
        # logger.info(f'pole{board}, aktualni hrac na tahu: {self.player}')
        return (board,converted)

    def get_possible_moves(self):
        """ Overwrites list of possible move for the current player """

        poss_moves = []
        all_anchors = []
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                tile = (row,column)
                if self.board[tile]!=0:
                    continue
                anchors = self._find_anchors(tile)
                if anchors:
                    poss_moves.append(tile)
                    all_anchors.append(anchors)
        self.poss_moves[self.player] = poss_moves
        self.poss_anchors[self.player] = all_anchors
        return poss_moves

    def is_game_over(self):
        """Determins if the game is over. Either because one player does not
        have stones or both are impotent."""

        if not self._stones_left():
            return True
        
        if not self.poss_moves[1] and not self.poss_moves[-1]:
            return True
        return False

    def determine_winner(self):
        """Checks the number of stones left and return the number of winning
        player"""

        white_won = self.stones[-1]>self.stones[1]
        if self.stones[-1]>self.stones[1]:
            return -1
        elif self.stones[-1]<self.stones[1]:
            return 1
        return 0

    def _stones_left(self):
        """Checks if any player is out of stones"""

        if not self.stones[1]:
            return False
        if not self.stones[-1]:
            return False
        return True



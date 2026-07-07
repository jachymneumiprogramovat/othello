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
        self.board = np.array([
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0]
            ])
        self.board[3][3]=-1
        self.board[4][4]=-1
        self.stones[-1] =2

        self.board[3][4]=1
        self.board[4][3]=1
        self.stones[1] =2

        self.poss_moves = [0, [(2, 3), (3, 2), (4, 5), (5, 4)], []]
        self.poss_anchors = [None, [[(np.int64(4), np.int64(3))],
                                    [(np.int64(3), np.int64(4))],
                                    [(np.int64(4), np.int64(3))],
                                    [(np.int64(3), np.int64(4))]], []]

    def _find_anchors(self,tile:tuple[int])->list:
        """ Finds all the anchors and returns them ."""

        anchors = []
        op_player = -self.player
        x,y = tile
        for dx,dy in self.dirs:
            nx,ny = x+dx, y+dy
            if not(0<=nx<8 and 0<=ny<8):
                continue
            
            if self.board[nx, ny] != op_player:
                continue

            curr_x, curr_y = nx + dx, ny + dy

            while 0 <= curr_x < 8 and 0 <= curr_y < 8:
                territory = self.board[curr_x, curr_y]

                if territory == self.player:
                    anchors.append((curr_x, curr_y))
                    break
                elif territory == 0:
                    break
                    
                # If it's another opponent stone, keep moving in the same direction
                curr_x += dx
                curr_y += dy                  
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

        if tile not in self.poss_moves[self.player]:
            logger.error(f'tah {tile} neni v moznych tazich, idk jak se tohle deje kamo')
        anchor_index = self.poss_moves[self.player].index(tile)
        anchors = self.poss_anchors[self.player][anchor_index]
        if not anchors:
            logger.error('Alegedly possible tile without anchors, wtf')
        #logger.info(f'anchori jsou {anchors}')

        converted = []
        for anchor in anchors:
            difference = tuple(anchor[i]-tile[i] for i in range(2))
            distance = max([abs(x) for x in difference])
            direction = tuple(np.array(difference)//distance) # normalizing
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
        """ Overwrites and returns list of possible moves for the current player """

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
        self.poss_moves[self.player] = deepcopy(poss_moves)
        self.poss_anchors[self.player] = all_anchors
        return poss_moves

    def is_game_over(self):
        """Determins if the game is over. Either because one player does not
        have stones or both are impotent."""

        if not self._stones_left():
            return True
        
        if not self.poss_moves[1] and not self.poss_moves[-1]:
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



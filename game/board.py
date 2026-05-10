from constants import *
from loguru import logger
import numpy  as np

class Board:
    """Class for handeling the logic behind the game"""
    def __init__(self):
        self.board = np.array([[0 for _ in range(8)] for _ in range(8)])
        self.player = 1
        self.dirs = [(1,0),(0,1),(-1,0),(0,-1)]

        self.white_stones = []
        self.black_stones = []

        self.passed = False
        self.poss_moves_white = []
        self.poss_moves_black = []

    def setup_board(self):
        self.board[3][3]=1
        self.board[4][4]=1
        self.white_stones.append((3,3),(4,4))

        self.board[3][4]=-1
        self.board[4][3]=-1
        self.black_stones.append((3,4),(4,3))
        logger.info(f'{self.board}',f'{self.white_stones,self.black_stones}')

    def _find_anchor(self,tile:tuple[int])->list:
        """Finds the nearest same-colored piece to which the whole path is
        filled with enemies."""

        opposites = []
        curr_player = self.board[tile]
        if curr_player == 0:
            logger.error('This should not be called for empty tiles')
            return None

        for dir in self.dirs:
            pices_left = 7 - abs(tile[0]*dir[0] + tile[1]*dir[1])
            #meaby the seven is wrong 6 7 nevertheless

            if pices_left == 0:
                continue

            for i in range(1,pices_left):
                difference = tuple(np.array(dir)*i)
                looking_at = tuple(np.add(tile,difference))

                if curr_player == self.board[looking_at]:
                    opposites.append(difference)
                if self.board[looking_at] == 0:
                    break
        return opposites

    def play_move(self,tile:tuple[int]):
        """ Converts all the necesarry tile on board to make the move happen
        and returns converted indicies for the Game to draw them. """

        # placing the actual stone
        self.board[tile] = self.player
        self.player *= -1
        
        # converting stones
        anchors = self._find_anchor(tile)
        converted = []
        for difference in anchors:
            distance = abs(difference[0]+difference[1])
            direction = tuple(np.array(difference)/distance)
            logger.info(f'difference:{difference},distanece:{distance},direction:{direction}') 

            for i in range(1,distance):
                vzdalenost = tuple(int(x)*i for x in direction) 
                looking_at = tuple(np.add(tile,vzdalenost))

                converted.append(looking_at)
                self.board[looking_at] *= -1

                if self.board[looking_at] == 0:
                    logger.error('There should always be stone between tile and anchor')

    def get_possible_moves(self):
        ...
    def _is_viable(self,tile:tuple):
        ...
    #somethig to handle the passing, preferably in this class so it is all
    # self-ontained.                        
    def is_game_over(self):
        """Determins if the game is over because one player is out of stones or
        that both players passed"""

        if not self._stones_left():
            return True
        if self.player==1:
            opposite_poss_moves = self.poss_moves_black
        else:
            opposite_poss_moves = self.poss_moves_white
        if self.passed and not opposite_poss_moves:
            return True
        return False

    def determine_winner(self):
        """Checks the number of stones left and return the number of winning
        player"""

        white_won = len(self.white_stones)>len(self.black_stones)
        if white_won:
            return 1
        else:
            return -1

    def _stones_left(self):
        """Checks if any player is out of stones"""

        if not self.white_stones:
            return False
        if not self.black_stones:
            return False
        return True



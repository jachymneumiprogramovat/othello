from constants import *
from loguru import logger
import numpy  as np

class Board:
    """Class for handeling the logic behind the game"""
    def __init__(self):
        self.board = np.array([[0 for _ in range(8)] for _ in range(8)])
        self.player = -1
        self.dirs = [(1,0),(0,1),(-1,0),(0,-1)]

        self.white_stones = []
        self.black_stones = []

        self.poss_moves = [None,[],[]]

    def setup_board(self):
        self.board[3][3]=-1
        self.board[4][4]=-1
        self.white_stones.extend([(3,3),(4,4)])

        self.board[3][4]=1
        self.board[4][3]=1
        self.black_stones.extend([(3,4),(4,3)])
        logger.info(f'{self.board}',f'{self.white_stones,self.black_stones}')

    def _find_anchors(self,tile:tuple[int])->list:
        """ Finds all the anchors and returns them ."""

        anchors = []
        op_player = -self.player
        for dir in self.dirs:
            print(tile,dir,tuple(np.add(tile,dir)))
            try:
                if self.board[tuple(np.add(tile,dir))]!=op_player:
                    continue
            except:
                continue
            for i in range(1,len(self.board)):
                examined = tuple(np.add(tile,tuple(np.array(dir)*i)))
                teritory = self.board[examined]

                # does not break only if in this direction are stones of
                # opposite color
                print(f'on tile: {examined} is player: {teritory}, {self.player}, {anchors}')
                if teritory == self.player:
                    logger.info('pridal jsem shit jako anchor')
                    anchors.append(examined)
                    break
                elif teritory == 0:
                    break
        return anchors

    def play_move(self,tile:tuple[int]):
        """ Converts all the necesarry tiles on board to make the move happen
        and returns converted indicies for the Game to draw them. """

        # placing the actual stone
        tile = list(tile)
        self.board[tile] = self.player
        self.player *= -1
        # converting stones
        anchors = []
        for poss_move in self.poss_moves[self.player]:
            if poss_move[0]==tile:
                anchors = poss_move[1:]
        if not anchors:
            logger.info('Alegedly possible tile without anchors, wtf')

        converted = []
        for anchor in anchors:
            distance = max(anchor)
            difference = abs(tile-anchor)
            direction = tuple(np.array(difference)/distance)
            logger.info(f'difference:{difference},distanece:{distance},direction:{direction}')

            for i in range(1,distance):
                vzdalenost = tuple(int(x)*i for x in direction)
                looking_at = tuple(np.add(tile,vzdalenost))

                converted.append(looking_at)
                self.board[looking_at] *= -1

                if self.board[looking_at] == 0:
                    logger.error('There should always be stone between tile and anchor')

        return converted.append(tile)

    def get_possible_moves(self):
        """ Overwrites list of possible move for the current player """

        new_moves = []
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                tile = (row,column)
                if self.board[tile]!=0:
                    continue
                anchors = self._find_anchors(tile)
                if anchors:
                    new_moves.append([tile,anchors])
        self.poss_moves[self.player] = new_moves

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

        white_won = len(self.white_stones)>len(self.black_stones)
        if white_won:
            return -1
        return 1

    def _stones_left(self):
        """Checks if any player is out of stones"""

        if not self.white_stones:
            return False
        if not self.black_stones:
            return False
        return True



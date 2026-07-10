import math
from loguru import logger 

from game.board import Board
from ai.mts_constants import *

class MTSNode(Board):
    """Tree node for the monte carlo tree search."""

    def __init__(self,board,player,move):
        super().__init__()
        self.board = board # this overwrites the empty board from Board
        self.player = player
        self.move = move # how was this state achived from its parent
        self.children:list[MTSNode] = []
        self.poss_children:list[tuple] = self.get_possible_moves()
        logger.debug(f'nastavil jsem mozne deti jakoze {self.poss_moves}')
        self.visited:int = 0
        self.results:list[int] = [0,0,0] # [draw, wins for 1, wins for -1]
        self.board_state:list = []
        self.rating:float = 0

        self._count_stones()
        
    def calculate_score(self,parent_value:float):
        """Returns the score based on self.visited and self.results"""
        if self.visited == 0:
            logger.error('I tried to calculate score for a node without visits.')
            return None
        return self.results[-1]/self.visited + EXPLORATION*math.sqrt((parent_value/self.visited))

    def _count_stones(self):
        """Counts the stone from the board so it can be intialized nontriviali
        and the counts are still accurate."""
        for row in self.board:
            for tile in row:
                self.stones[tile]+=1 #no one cares about the zeroth spot.

    def get_children(self):
        """Returns MTSNode objects for all the possible succesors of this node"""
        poss_moves = self.get_possible_moves()
        for poss_move in poss_moves:
            children_board, _ = self.play_move(poss_move)
            children = MTSNode(board=children_board,player=-self.player,move=poss_move)
            self.children.append(children)
        return self.children

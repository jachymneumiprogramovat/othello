from game.board import Board
from loguru import logger 
from ai.mts_constants import *
import math


class MTSNode(Board):
    def __init__(self,board,player):
        super().__init__()
        self.board = board # this overwrites the empty board from Board
        self.player = player
        self.children:list[MTSNode] = []
        self.visited:int = 0
        self.results:list[int] = [0,0,0] # [draw,win,loss]
        self.board_state:list = []
        self.rating:float = 0

        self._count_stones()
        
        # logger.info(f'hodnoty kamenu jsem inicializoval jako {self.stones}')

    def calculate_score(self,paren_value:float):
        """Returns the score based on self.visited and self.results"""
        if self.visited == 0:
            return float('inf')
        print(self.player,self.results[-self.player],self.results[-1]/self.visited,EXPLORATION*math.sqrt((paren_value/self.visited)))
        return self.results[-1]/self.visited + EXPLORATION*math.sqrt((paren_value/self.visited))

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
            children = MTSNode(board=children_board,player=-self.player)
            self.children.append(children)
        return self.children

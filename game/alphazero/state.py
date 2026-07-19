from game.board import Board 

from alphazero.alpha_constants import *

import numpy as np
import torch

from loguru import logger

class State(Board):
    """ Board state node for the MCTS modified for alpha zero. """

    def __init__(
                 self,
                 board:list,
                 player:int,
                 move:list,
                 parent:'State',
                 prob:float=0
                 ):

        super().__init__(parent)
 
        self.board = board # this overwrites the empty board from Board
        self.player = player # player to move from this state
        self.move = move # how was this state achived from its parent

        self.children:list[State] = []
        self.visited:int = 0
        self.total_value:float = 0

        self.prob = prob #given to this node by Model

        # setting up the initial values for stones and poss_moves
        self._count_stones()
        self.get_possible_moves()


    def _count_stones(self):
        """Counts the stone from the board so it can be intialized nontriviali
        and the counts are still accurate."""
        for tile in self.board[1]:
            if tile:
                self.stones[1]+=1 #no one cares about the zeroth spot.
        for tile in self.board[-1]:
            if tile:
                self.stones[-1]+=1
    @torch.no_grad()
    def get_ucb(self,parent_value:float):
        """Calculate the UCB for a given child node."""
        if self.visited == 0:
            q_value = 0
        else:
            q_value = 1 - ((self.total_value / self.visited) + 1) / 2

        ucb = (
            q_value
            + EXPLORATION
            * (np.sqrt(parent_value) / (self.visited + 1))
            * self.prob
        )
        return ucb
    def is_expanded(self):
        return len(self.children)>0

    def get_children(self):
        
        for index,tile in enumerate(self.poss_moves[self.player]):
            if tile:
                poss_move = np.zeros(64)
                poss_move[index] = 1
                new_board,_ = self.play_move(index)
                children = State(board = new_board,player=-self.player, move = poss_move, parent=self)
                self.children.append(children)
        return self.children

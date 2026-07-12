from game.board import Board 

from alphazero.alpha_constants import *

import numpy as np

from loguru import logger


class State(Board):
    """ Board state node for the MCTS modified for alpha zero. """

    def __init__(
                 self,
                 board:list,
                 player:int,
                 move:list,
                 prob:float=0
                 ):

        super().__init__()

        self.board = board # this overwrites the empty board from Board
        self.player = player # player to move from this state
        self.move = move # how was this state achived from its parent

        self.children:list[State] = []
        self.visited:int = 0
        self.total_value:float = 0

        self.prob = prob #given to this node by Model
        self._count_stones()


    def _count_stones(self):
        """Counts the stone from the board so it can be intialized nontriviali
        and the counts are still accurate."""
        for row in self.board:
            for tile in row:
                self.stones[tile]+=1 #no one cares about the zeroth spot.

    def get_ucb(self,parent_value:float):
        """Calculate the UCB for a given child node."""
        if self.visit_count == 0:
            q_value = 0
        else:
            q_value = 1 - ((self.value_sum / self.visited) + 1) / 2

        ucb = (
            q_value
            + EXPLORATION
            * (np.sqrt(parent_value) / (self.visited + 1))
            * self.prior
        )
        return ucb

    def get_children(self):
        for tile in self.poss_moves:
            if tile:
                poss_move = np.zeros(64)
                poss_move[tile] = 1
                new_board,_ = self.play_move(poss_move)
                children = State(board = new_board,player=-self.player, move = poss_move)
                self.children.append(children)
        return self.children

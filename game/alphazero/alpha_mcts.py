import numpy as np
import torch

from ai.mts import MTS
from ai.mts_node import MTSNode

from alphazero.model import Model
from alphazero.state import State

from loguru import logger

class AMCTS():
    """ Special version os MCTS algorithm for alpha zero. """
    def __init__(self,model:Model):
        self.model = model

        
    def select_best_child(self,node:State):
        """Either the one with default rating value or the one with the biggest
        one."""
        if not node.children:
            logger.error('jaktoze kurva nema deti dopice')
            return None
        return max(node.children, key=lambda x: x.get_ucb(parent_value=node.visited))

    def model_quessing(self,node:State):
        """Asks the model for its opinion and tell him which moves are possible"""
        if node.is_game_over():
            return node.determine_winner()
        board = torch.as_tensor(node.board)
        policies,value =  self.model(board)
        poss_moves = node.get_possible_moves()
        valid_policies = policies * poss_moves
        nonzero_policies = filter(lambda x: x>0,valid_policies)

        return nonzero_policies,value

    def expand(self,node:State):
        children = node.get_children()
        return children

    def back_propagate(self,path:list[State], value: int):
        for node in path:
            node.total_value += value
            node.visit_ed += 1
            # Change to opponent's value
            value = -value

    def select(self,node:State):
        path = []
        while True:
            path.append(node)
            if node.is_fully_expanded():
                return path
            if node.is_game_over():
                return path
            node = self.select_best_child(node)

    def rollout(self,root:State):
        """Performs the selection, expansion, model quessing and back
        propagation from node once."""
        path = self.select(root)
        logger.debug(f'cesta k vrcholu je f{[x.board for x in path]}')
        leaf = path[-1]
        logger.debug(f'listem je MTSNode s boardem {leaf.board}')
        new_layer = self.expand(leaf)
        policies, value = self.model_quessing(leaf)

        for polici, child in zip(policies,new_layer):
            child.prob = polici
        logger.debug(f'synove listu jsou {[x.board for x in leaf.children]}')
        self.back_propagate(path,value)

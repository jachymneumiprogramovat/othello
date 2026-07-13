import numpy as np
import torch
from collections import defaultdict

from ai.mts import MTS
from ai.mts_node import MTSNode

from alphazero.model import Model
from alphazero.state import State
from alphazero.alpha_constants import *

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

        stacked = np.stack([node.board[1],node.board[-1]], axis=0)
        batched = stacked[np.newaxis, ...]
        model_input = torch.tensor(batched, dtype=torch.float32, device=self.model.device)

        policies,value =  self.model(model_input)
        poss_moves = node.get_possible_moves()
        poss_moves = torch.from_numpy(poss_moves)

        logger.debug(f' co se deje kurva doprdele {len(policies)},{len(poss_moves)}')
        valid_policies = torch.multiply(policies, poss_moves)
        logger.debug(valid_policies)
        valid_policies/= torch.sum(valid_policies)


        return valid_policies,value

    def expand(self,node:State):
        children = node.get_children()
        return children

    def back_propagate(self,path:list[State], value: int):
        for node in path:
            node.total_value += value
            node.visited += 1
            # Change to opponent's value
            value = -value

    def select(self,node:State):
        path = []
        logger.info(f'selectuju z rootu {node}')
        while True:
            path.append(node)
            logger.info(f'{path}')
            if not node.is_expanded():
                return path
            if node.is_game_over():
                return path
            node = self.select_best_child(node)

    def rollout(self,root:State):
        """Performs the selection, expansion, model quessing and back
        propagation from node once."""
        path = self.select(root)
        logger.debug(f'cesta k vrcholu je f{[x for x in path]}')
        leaf = path[-1]
        logger.debug(f'listem je MTSNode s boardem {leaf}')
        new_layer = self.expand(leaf)
        logger.debug(f'jeho syny jsou {[x for x in new_layer]}')
        policies, value = self.model_quessing(leaf)

        logger.debug(f'policie {[x for x in policies]}, deti {new_layer}')
        for polici, child in zip(policies,new_layer):
            child.prob = polici
        logger.debug(f'synove listu jsou {[x.board for x in leaf.children]}')
        self.back_propagate(path,value)

    def calculate_probs(self,node:State,temperature:float)->list:
        """Calculates the \pi value for all children of `node. 
        child.visited / node.visited
        """
        # calculating the \pi values
        probs = defaultdict(int)
        for child in node.children:
            probs[child.move] += child.visited
        visited_sum = sum(child.visited for child in node.children)

        for child in node.children:
            probs[child.move] /= visited_sum

        prob_vector = sum(move*prob for move,prob in probs.items())
        print(prob_vector,"mel by to byt proste 1d vektor")

        prob_vector = prob_vector ** 1/temperature
        prob_vector /= np.sum(prob_vector)

        return prob_vector


    def choose_move(self,root:State)->State:
        """ Iterates the rollout function and then chooses the best next move. """
        for _ in range(ROLLOUT_COUNT):
            self.rollout(root)
        poss_moves = sum(child.move for child in root.children)
        probs = self.calculate_probs(root,TEMPERATURE)
        return (np.random.choice(poss_moves, p=probs),probs)

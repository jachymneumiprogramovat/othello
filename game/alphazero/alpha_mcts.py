import numpy as np
import torch
from tqdm import tqdm
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
            return np.zeros(64, dtype=np.float32), float(node.determine_winner())

        stacked = np.stack([node.board[1], node.board[-1]], axis=0).astype(np.float32)
        batched = stacked[np.newaxis, ...]
        
        model_input = torch.from_numpy(batched).to(self.model.device)

        with torch.inference_mode():
            policies, value = self.model(model_input)
            policies = torch.softmax(policies[0]).cpu().numpy()  
            value = value.item()                 

        poss_moves = node.get_possible_moves()
        valid_policies = policies * poss_moves
        valid_policies/= np.sum(valid_policies)

        return valid_policies,value

    def expand(self,node:State):
        children = node.get_children()
        return children

    def back_propagate(self,path:list[State], value: float):
        for node in path:
            node.total_value += value
            node.visited += 1
            # Change to opponent's value
            value = -value

    def select(self,node:State):
        path = []
        while True:
            path.append(node)
            if not node.is_expanded():
                return path
            if node.is_game_over():
                return path
            node = self.select_best_child(node)

    def rollout(self,root:State):
        """Performs the selection, expansion, model quessing and back
        propagation from node once."""
        path = self.select(root)
        leaf = path[-1]
        new_layer = self.expand(leaf)
        policies, value = self.model_quessing(leaf)
        policies = policies[0]

        for child in new_layer:
            child.prob = np.sum(child.move * policies)
        self.back_propagate(path,value)

    def calculate_probs(self,node:State,temperature:float)->list:
        """Calculates the \pi value for all children of `node. 
        child.visited / node.visited
        """
        # calculating the \pi values
        visited_sum = sum(child.visited for child in node.children)

        prob_vector = sum(child.move*(child.visited/visited_sum) for child in node.children)

        for i in range(len(prob_vector)):
            if prob_vector[i] <0:
                prob_vector[i] = 0
        prob_vector /= np.sum(prob_vector)

        prob_vector = prob_vector ** (1/temperature)
        prob_vector /= np.sum(prob_vector)

        return prob_vector


    def choose_move(self,root:State)->State:
        """ Iterates the rollout function and then chooses the best next move. """
        for _ in range(ROLLOUT_COUNT):
            self.rollout(root)
        probs = self.calculate_probs(root,TEMPERATURE)
        tile_index = np.random.choice(range(64), p=probs)
        new_move = np.zeros(64)
        new_move[tile_index] = 1

        new_node = None
        for child in root.children:
            if np.array_equal(child.move, new_move):
                new_node = child
        if not new_node:
            logger.error(f'nenasel jsem tah {new_move} wtf')

        return (new_node,probs)

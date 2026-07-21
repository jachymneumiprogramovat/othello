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
import torch

class AMCTS():
    """ Special version os MCTS algorithm for alpha zero. """
    def __init__(self,model:Model):
        self.model = model


    @torch.no_grad()
    def select_best_child(self,node:State):
        """Calculates UCB values for all the children of `node and returns the
        maximal children."""
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
            policies = torch.softmax(policies[0],0,dtype=torch.float32).cpu().numpy()
            value = value.item()

        # TODO spravit dirichlet noise
        # policies = (1 - EPSILON) + EPSILON * np.random.dirichlet([ALPHA] * 64, size=64)

        poss_moves = node.poss_moves[node.player]
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
        if leaf.is_game_over():
            self.back_propagate(path,leaf.determine_winner())
        new_layer = self.expand(leaf)
        policies, value = self.model_quessing(leaf)
        # logger.info(f'pro stav \n{leaf} mam hodnoty \n{policies}')

        for child in new_layer:
            child.prob = np.sum(child.move * policies)
            # logger.info(f'davam \n{policies} a mam syny {new_layer}')
        if not new_layer:
            self.back_propagate(path,value)
        else:
            self.back_propagate(path+[new_layer[0]],value)

    def calculate_probs(self,node:State,temperature:float)->list:
        """Calculates the \pi value for all children of `node. 
        child.visited / node.visited
        """
        # calculating the \pi values
        visited_sum = sum(child.visited for child in node.children)
        # logger.info(visited_sum)

        prob_vector = sum(child.move*(child.visited/visited_sum) for child in node.children)

        # logger.info(f'pro tahy a jejich visit county {[(child,child.visited) for child in node.children]}')

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

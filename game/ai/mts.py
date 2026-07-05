# toto je file na monte-carlo tree search
from ai.mts_node import MTSNode
from game.board import Board
from loguru import logger
from random import choice
from copy import deepcopy
from ai.mts_constants import *
import math
import numpy as np 
from tqdm import tqdm


class MTS():
    """Class which performs expansion, selection, simulation and
    backpropagation on the game tree node."""

    def select_best_child(self,node:MTSNode):
        """Either the one with default rating value or the one with the biggest
        one."""
        if not node.children:
            return None
        parent_value = math.log(node.visited)
        return max(node.children,key=lambda x: x.calculate_score(parent_value))

    def select(self,node:MTSNode):
        """Returns the path to first unexplored descendant of node."""
        path = []
        while True:
            path.append(node)
            if not node.children:
                return path
            # bro tady vybira jeste vybira syny co nejsou expandtnute a s nima
            # tu cestu rovnou vraci idk proc ale tohle by snad melo delat neco
            # podobneho
            node = self.select_best_child(node)


    def expand(self,node:MTSNode)->list[MTSNode]:
        """Returns all children for a given node."""
        if node.children:
            return 
        return node.get_children()

    def simulate(self,node:MTSNode)->int:
        """ Randomly plays the game from node till the end and returns the outcome """
        board = deepcopy(node)
        board.get_possible_moves()
        while not board.is_game_over():
            poss_moves = board.get_possible_moves()

            if not poss_moves:
                board.player *=-1
                continue

            move = choice(poss_moves)
            new_board,_ = board.play_move(move)
            board.board = new_board
            board.player *=-1
        return board.determine_winner()

    def backpropagate(self,path:list[MTSNode],reward):
        """ Backpropagates the reward down the path """
        for node in reversed(path):
            node.visited += 1
            node.results[reward*node.player] += 1

    def rollout(self,root:MTSNode):
        """ Performs select and expand in need, then simulate and finally
        backpropagate """
        path = self.select(root)
        logger.info(f'cesta k vrcholu je f{[x.board for x in path]}')
        leaf = path[-1]
        logger.info(f'listem je MTSNode s boardem {leaf.board}')
        self.expand(leaf)
        logger.info(f'synove listu jsou {[x.board for x in leaf.children]}')
        for _ in tqdm(range(SIMULATION_COUNT)):
            reward = self.simulate(leaf)
            self.backpropagate(path,reward)

    def train(self):
        """ Rollsout many times from the initial board position """
        root = MTSNode(board=DEFAULT_BOARD,player=-1)
        for _ in tqdm(range(ROLLOUT_COUNT)):
            self.rollout(root)
        return root # TODO smazat return, slouzi jen pro debug

    def store(self,root):
        """ PUTs all the MTSNodes and their best_children into the db. """


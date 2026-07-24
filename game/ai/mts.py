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
            logger.error('jaktoze kurva nema deti dopice')
            return None
        parent_value = math.log(node.visited)
        logger.debug([(child.move,child.results,child.visited) for child in node.children])
        return max(node.children, key=lambda x: x.calculate_score(parent_value))

    def select(self,node:MTSNode):
        """Returns the path to first unexplored descendant of node."""
        path = []
        while True:
            logger.debug(f'koukam se na {node}')
            path.append(node)
            if not node.poss_children and not node.children:
                return path
            if node.poss_children:
                return path
            node = self.select_best_child(node)


    def expand(self,node:MTSNode)->list[MTSNode]:
        """Returns random, previously not existent children for a node without
        all children."""
        poss_moves = node.poss_children
        if not poss_moves:
            if node.is_game_over():
                return node
            pass_child = MTSNode(board=deepcopy(node.board), player=-node.player, move=None)
            return pass_child

        move = poss_moves.pop()
        child = MTSNode(board=node.play_move(move)[0], player=-node.player, move=move)
        return child

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
        for node in path:
            node.visited += 1
            node.results[reward] += 1
            logger.debug(f'nastavil jsem visity pro {node.board} na {node.visited}')

    def rollout(self,root:MTSNode,simulation_count:int):
        """ Performs select and expand in need, then simulate and finally
        backpropagate """
        path = self.select(root)
        logger.debug(f'cesta k vrcholu je f{[x.board for x in path]}')
        leaf = path[-1]
        logger.debug(f'listem je MTSNode s boardem {leaf.board}')
        new_node = self.expand(leaf)
        if new_node != leaf:
            leaf.children.append(new_node)
            path.append(new_node)
        logger.debug(f'synove listu jsou {[x.board for x in leaf.children]}')
        for _ in range(simulation_count):
            reward = self.simulate(leaf)
            self.backpropagate(path,reward)



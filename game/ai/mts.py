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
        for child in node.children:
            logger.info('dite')
            logger.info(f'{child.board}, {child.visited}')
        children_scores = [child.calculate_score(parent_value=parent_value) for child in node.children]
        logger.info(children_scores)
        return max(children_scores)

    def select(self,node:MTSNode):
        """Returns the path to first unexplored descendant of node."""
        path = []
        while True:
            logger.info(f'koukam se na {node.board}')
            path.append(node)
            if node.poss_children:
                return path
            node = self.select_best_child(node)


    def expand(self,node:MTSNode)->list[MTSNode]:
        """Returns random, previously not existent children for a node without
        all children."""
        move = node.poss_children.pop()
        child = MTSNode(board = node.play_move(move)[0], player= -node.player, move = move)
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
            logger.info(f'nastavil jsem visity pro {node.board} na {node.visited}')



    def rollout(self,root:MTSNode):
        """ Performs select and expand in need, then simulate and finally
        backpropagate """
        path = self.select(root)
        logger.info(f'cesta k vrcholu je f{[x.board for x in path]}')
        leaf = path[-1]
        # logger.info(f'listem je MTSNode s boardem {leaf.board}')
        new_node = self.expand(leaf)
        leaf.children.append(new_node)
        path.append(new_node)
        # logger.info(f'synove listu jsou {[x.board for x in leaf.children]}')
        for _ in tqdm(range(SIMULATION_COUNT)):
            reward = self.simulate(leaf)
            self.backpropagate(path,reward)
            logger.info(f'nody v ceste maji takoveto resulty a visity')
            for node in path:
                logger.info(f'resulty: {node.results}, visity: {node.visited}')



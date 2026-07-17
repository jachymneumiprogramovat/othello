from loguru import logger
import numpy as np

from alphazero.model import Model
from alphazero.alpha_mcts import AMCTS
from alphazero.state import State
from alphazero.alpha_constants import *

class AlphaZero():
    """Class that combines the NN model and MCTS in selfplaying and traning."""
    def __init__(self,model:Model):
        self.mode:Model = model
        self.mcts:AMCTS = AMCTS(model=model)
        self.board:list = DEFAULT_BOARD

    def selfplay(self)->list[tuple]:
        """
        Plays with itself once. Returns list of tuples in the form
        (board,\pi values, move choosen, result) for all the states of the
        game.
        """

        game_memory = []
        player = 1
        node = State(board = DEFAULT_BOARD,player=player,move = None)
        turn = 0
        for i in range(100):
            # logger.info(f'------ tah {i} -----')
            turn+=1

            #no moves so skipping the turn
            poss_moves = node.get_possible_moves()
            if not np.any(poss_moves):
                node.player = -node.player      # pass the turn
                continue

            new_node,probs = self.mcts.choose_move(node)
            game_memory.append((node.board,probs,new_node.move))
            poss_moves = new_node.get_possible_moves()
            if new_node.is_game_over():
                logger.info(f'{new_node}')
                winner = new_node.determine_winner()
                for i in range(len(game_memory)):
                    game_memory[i] = (*game_memory[i],winner)

                logger.info(f'hra trvala {turn} tahu')
                return game_memory

            node = new_node
            node.player = -node.player
        logger.error('hra trvala dele nez 60 tahu coz je picovina')
        return None


    def train(self,examples:list):
        """ Back propagates the losses calculated from examples and the
        predictions. """

    def learn(self):
        """ Runs all the iterations. Each iteration produces a lot of examples
       by selfplay and then runs all the epochs of training on them."""

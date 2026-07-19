from loguru import logger
import numpy as np
from copy import deepcopy

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
        node = State(board = DEFAULT_BOARD,player=player,move = None,parent=None)
        turn = 0  
        passed = 0
        while not node.is_game_over():
            logger.info(f'------ tah {turn} -----')
            logger.info(f'toto je stav \n{node} skoncila hra uz? {node.is_game_over()}')
            # logger.info(f'toto jsou mozne tahy:')
            # logger.info(f'{node.poss_moves},{node.player}')
            # pretty_print([0,node.poss_moves[node.player],np.zeros(64)])
            # logger.info(f'toto je hrac {node.player}')
            turn+=1

            if turn >100:
                logger.error(f'hra je ve stavu \n{node} a trva vic nez 100 tahu')
                break

            #no moves so skipping the turn
            poss_moves = node.poss_moves[node.player]
            if passed ==2:
                logger.info(f'uz jsem dvakrat passnul ve stavu {node}')
                break

            if not np.any(poss_moves):
                logger.info(f'skipuju za boardu \n{node} jako hrac {node.player} a moje tahy jsou {node.poss_moves}')
                passed +=1
                new_node=State(board=deepcopy(node.board),player=-node.player,parent=node,move=np.zeros(64))   # pass the turn
                node = new_node
                continue
            else:
                passed = 0
            new_node,probs = self.mcts.choose_move(node)
            game_memory.append((node.board,probs,new_node.move)) #mozna to budu muset kopirovat
            poss_moves = new_node.poss_moves[new_node.player]

            node = new_node


        winner = node.determine_winner()
        for i in range(len(game_memory)):
            game_memory[i] = (*game_memory[i],winner)

        return game_memory



    def train(self,examples:list):
        """ Back propagates the losses calculated from examples and the
        predictions. """

    def learn(self):
        """ Runs all the iterations. Each iteration produces a lot of examples
       by selfplay and then runs all the epochs of training on them."""

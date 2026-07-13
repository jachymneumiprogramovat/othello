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
        node = State(board = self.board,player=player,move = None)
        while True:
            new_node,probs = self.mcts.choose_move(node)
            game_memory.append((node.board,probs,new_node.move))

            if new_node.is_game_over():
                """pridat do vsechn examplu v ceste vysledek te hry"""
                break

            node = new_node
            node.player = -node.player

        return game_memory

    def train(self,examples:list):
        """ Back propagates the losses calculated from examples and the
        predictions. """

    def learn(self):
        """ Runs all the iterations. Each iteration produces a lot of examples
        by selfplay and then runs all the epochs of training on them."""
